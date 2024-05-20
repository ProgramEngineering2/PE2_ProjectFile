import os
import xml.etree.ElementTree as ET
import pandas_frame as pd
import lmfit
import numpy as np
import matplotlib.pyplot as plt

# 여러 디렉토리 경로
directories = [
    '..\\HY202103\\D07\\20190715_190855',
    '..\\HY202103\\D08\\20190526_082853',
    '..\\HY202103\\D08\\20190528_001012',
    '..\\HY202103\\D08\\20190712_113254',
    '..\\HY202103\\D23\\20190528_101900',
    '..\\HY202103\\D23\\20190531_072042',
    '..\\HY202103\\D23\\20190603_204847',
    '..\\HY202103\\D24\\20190528_105459',
    '..\\HY202103\\D24\\20190528_111731',
    '..\\HY202103\\D24\\20190531_151815',
    '..\\HY202103\\D24\\20190603_225101'
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
    
    def plot_transmission_spectra_all(ax, root):

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

            # 데이터를 데이터 플롯 리스트에 추가
            data_to_plot.append((dc_bias, length_values, measured_transmission_values))

        # 그래프 그리기
        for dc_bias, length_values, measured_transmission_values in data_to_plot:
            plt.plot(length_values, measured_transmission_values, label=f'DCBias={dc_bias}V')

        ax.set_xlabel('Wavelength [nm]')
        ax.set_ylabel('Measured Transmission [dB]')
        ax.set_title(f'Transmission Spectra - as measured')
        ax.legend(title='DC Bias', loc='upper right')
        ax.grid(True)
