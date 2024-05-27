import os
import xml.etree.ElementTree as ET
import lmfit
import numpy as np
import matplotlib.pyplot as plt


def plot_flat_transmission_spectra(ax, root):

    # Initialize list to store data
    data = []

    # Extract data by iterating over all WavelengthSweep elements
    for Wavelength_Sweep_element in root.findall('.//WavelengthSweep'):
        label = Wavelength_Sweep_element.get('DCBias')
        # Extract attributes L and IL of WavelengthSweep element
        x = [float(v) for v in Wavelength_Sweep_element.find('.//L').text.split(',')]
        y = [float(v) for v in Wavelength_Sweep_element.find('.//IL').text.split(',')]
        data.append((label, x, y))  # Append tuple of label, x, and y to data list

    # Ensure x and y are numpy arrays of type float
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    # Polynomial fitting
    degree = 6
    coefficients = np.polyfit(x, y, degree)  # 6th degree polynomial fitting
    function = np.poly1d(coefficients)  # Create the fitted polynomial function

    # Calculate R-squared value
    y_pred = function(x)  # Predicted y values
    y_mean = np.mean(y)  # Mean of y values
    ssr = np.sum((y_pred - y_mean) ** 2)  # Sum of squares due to regression
    sst = np.sum((y - y_mean) ** 2)  # Total sum of squares
    r_squared = ssr / sst  # R-squared value

    # Initialize lists to store maximum peaks
    max_peak_x = []
    max_peak_y = []

    # Find maximum peaks in each range
    for label, x, y_meas in data:
        x = np.array(x, dtype=float)
        y_meas = np.array(y_meas, dtype=float)
        for i in range(3):  # Three ranges
            start_index = int(i * len(x) / 3)
            end_index = int((i + 1) * len(x) / 3)
            range_x = x[start_index:end_index]
            range_y = [y1 - y2 for y1, y2 in zip(y_meas[start_index:end_index], function(range_x))]
            max_index = np.argmax(range_y)
            max_peak_x.append(range_x[max_index])
            max_peak_y.append(range_y[max_index])

    # Linear regression for maximum peaks
    slope = (max_peak_y[2] - max_peak_y[0]) / (max_peak_x[2] - max_peak_x[0])
    intercept = max_peak_y[0] - slope * max_peak_x[0]
    x_values = np.linspace(min(max_peak_x) - 10, max(max_peak_x) + 10, 100)
    y_values = slope * x_values + intercept

    transmission_data = data[:-1]

    ref_data = [data[-1]]  # Assign the last item to ref_data as a list
    x = np.array(ref_data[0][1], dtype=float)  # Get already split x values
    y = np.array(ref_data[0][2], dtype=float)  # Get already split y values
    ref_data = [(ref_data[0][0], x, y)]  # Reassign ref_data with the modified data

    # Ensure x and y_meas are numeric
    for label, x, y_meas in transmission_data:
        plt.plot(x, [y1 - y2 - (slope * x_val + intercept) for y1, y2, x_val in zip(y_meas, function(x), x)],
                 label=f'{label}V', linestyle='-')
    for label, x, y_meas in ref_data:
        x = np.array(x, dtype=float)
        y_meas = np.array(y_meas, dtype=float)
        plt.plot(x, [y1 - y2 for y1, y2 in zip(y_meas, y)], label=f'{label}V', linestyle='-')

    #ax.legend(ncol=3)

    ax.set_xlabel('Wavelength [nm]')
    ax.set_ylabel('Flat Measured Transmission [dB]')
    ax.set_title(f'Transmission Spectra - as measured')
    ax.legend(title='DC Bias', loc='upper right', bbox_to_anchor=(1.5, 1), fontsize='small')
    ax.grid(True)


def plot_and_save_graphs(jpgs_directory, xml_files):
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 새로운 그래프 생성
        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        # 데이터를 이용하여 그래프 그리기
        plot_flat_transmission_spectra(ax, root)

        # 그래프 저장
        filename = os.path.splitext(os.path.basename(xml_file))[0] + '_flat_transmission.jpg'
        plt.savefig(os.path.join(jpgs_directory, filename))
        plt.close()  # 그래프 초기화

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

# JPG 파일 저장 디렉토리 생성
jpgs_directory = os.path.join('res', 'jpgs')
if not os.path.exists(jpgs_directory):
    os.makedirs(jpgs_directory)

# 그래프 생성 및 저장
plot_and_save_graphs(jpgs_directory, xml_files)
#