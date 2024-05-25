import os
import xml.etree.ElementTree as ET
import lmfit
import numpy as np
import matplotlib.pyplot as plt

# 여러 디렉토리 경로
directories = [
    'dat/HY202103/D07/20190715_190855',
    'dat/HY202103/D08/20190526_082853',
    'dat/HY202103/D08/20190528_001012',
    'dat/HY202103/D08/20190712_113254',
    'dat/HY202103/D23/20190528_101900',
    'dat/HY202103/D23/20190531_072042',
    'dat/HY202103/D23/20190603_204847',
    'dat/HY202103/D24/20190528_105459',
    'dat/HY202103/D24/20190528_111731',
    'dat/HY202103/D24/20190531_151815',
    'dat/HY202103/D24/20190603_225101'
]

# 모든 XML 파일 경로를 담을 리스트
xml_files = []

# 각 디렉토리마다 'LMZ'가 들어가는 XML 파일만을 찾아서 리스트에 추가
for directory in directories:
    file_list = os.listdir(directory)
    xml_files.extend([os.path.join(directory, file) for file in file_list if 'LMZ' in file and file.endswith(".xml")])

for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    def plot_flat_transmission_spectra(ax):

        WavelengthSweep = list(root.findall('.//WavelengthSweep'))

        # 모든 WavelengthSweep 요소 반복
        for WavelengthSweep in root.findall('.//WavelengthSweep'):
            # DCBias 속성 값 가져오기
            dc_bias = float(WavelengthSweep.get('DCBias'))

            # LengthUnit과 transmission 요소의 text 값 가져오기
            length_values = []
            measured_transmission_values = []
            for L in WavelengthSweep.findall('.//L'):
                length_text = L.text
                length_text = length_text.replace(',', ' ')
                length_values.extend([float(value) for value in length_text.split() if value.strip()])

            for IL in WavelengthSweep.findall('.//IL'):
                measured_transmission_text = IL.text
                measured_transmission_text = measured_transmission_text.replace(',', ' ')
                measured_transmission_values.extend(
                    [float(value) for value in measured_transmission_text.split() if value.strip()])

        # 다항식 차수 범위 설정
        poly_degrees = range(1, 7)

        # 각 차수에 대한 fitting 결과 저장할 리스트 초기화
        fitting_results = []

        # 1차부터 6차까지의 fitting 결과 저장
        for degree in range(1, 7):
            coeffs = np.polyfit(length_values, measured_transmission_values, degree)
            p = np.poly1d(coeffs)
            yhat = p(length_values)
            ybar = np.sum(measured_transmission_values) / len(measured_transmission_values)
            ssreg = np.sum((yhat - ybar) ** 2)
            sstot = np.sum((measured_transmission_values - ybar) ** 2)
            r_squared = ssreg / sstot
            fitting_results.append((coeffs, r_squared))

        best_degree = np.argmax([result[1] for result in fitting_results]) + 1
        best_coeffs = fitting_results[best_degree - 1][0]

        x_values = np.linspace(min(length_values), max(length_values), 5000)
        best_y_values = p(x_values)

        # 그래프에 그릴 데이터를 담을 리스트 초기화
        data_to_plot = []

        WavelengthSweep = list(root.findall('.//WavelengthSweep'))

        # 모든 WavelengthSweep 요소 반복
        for WavelengthSweep in root.findall('.//WavelengthSweep'):
            # DCBias 속성 값 가져오기
            dc_bias = float(WavelengthSweep.get('DCBias'))

            # LengthUnit과 transmission 요소의 text 값 가져오기
            length_values = []
            measured_transmission_values = []
            for L in WavelengthSweep.findall('.//L'):
                length_text = L.text
                length_text = length_text.replace(',', ' ')
                length_values.extend([float(value) for value in length_text.split() if value.strip()])

            for IL in WavelengthSweep.findall('.//IL'):
                measured_transmission_text = IL.text
                measured_transmission_text = measured_transmission_text.replace(',', ' ')
                measured_transmission_values.extend(
                    [float(value) for value in measured_transmission_text.split() if value.strip()])

                # 전체 그래프에서 ref fitting 빼기
                measure_minus_ref_transmission_values = measured_transmission_values - best_y_values

                # 6번째 WavelengthSweep(DC bias=0.5V)에 대한 처리
                if dc_bias == 0.5:
                    # 스플라인 근사화
                    from scipy.interpolate import UnivariateSpline
                    from scipy.signal import find_peaks

                    # 스플라인 근사화
                    sixth_spline = UnivariateSpline(length_values, measured_transmission_values - best_y_values)

                    # 스플라인 근사 그래프
                    sixth_x = np.linspace(min(length_values), max(length_values), 1000)
                    spline_approximation = sixth_spline(sixth_x)

                    # 스플라인 근사 그래프에서 피크 찾기
                    peaks_indexes, _ = find_peaks(spline_approximation, distance=10, prominence=0.1)
                    peaks = [spline_approximation[i] for i in peaks_indexes]
                    peak_length_values = [sixth_x[i] for i in peaks_indexes]

                    # peak 값을 1차 함수로 적합시켜야 함.
                    alpha_coefficients = np.polyfit(peak_length_values, peaks, 1)

                    # 계수를 사용하여 alpha 함수를 정의합니다.
                    def alpha_function(length):
                        return alpha_coefficients[0] * np.array(length) + alpha_coefficients[1]

                    # alpha 함수 호출
                    alpha = alpha_function(length_values)

                    flat_transmission_values = np.array(measure_minus_ref_transmission_values) - np.array(alpha)

                else:
                    flat_transmission_values = measure_minus_ref_transmission_values

                # 데이터를 데이터 플롯 리스트에 추가
                data_to_plot.append((dc_bias, length_values, flat_transmission_values))

        # 그래프 그리기
        for dc_bias, length_values, flat_transmission_values in data_to_plot:
            plt.plot(length_values, flat_transmission_values, label=f'DCBias={dc_bias}V')

        # Peak 값을 1차 함수로 근사한 방정식 출력(alpha 함수)
        a, b = alpha_coefficients
        alpha_equation_text = "Alpha function: {:.2f}x + {:.2f}".format(a, b)

        # 그래프에 방정식 텍스트 추가
        ax.text(0.2, 0.95, alpha_equation_text, fontsize='small', color='red', transform=ax.transAxes)

        ax.set_xlabel('Wavelength [nm]')
        ax.set_ylabel('Flat Measured Transmission [dB]')
        ax.set_title(f'Transmission Spectra - as measured')
        ax.legend(title='DC Bias', loc='upper right', bbox_to_anchor=(1.5, 1), fontsize='small')
        ax.grid(True)