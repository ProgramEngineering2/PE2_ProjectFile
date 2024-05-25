import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET

from datetime import datetime
from tqdm import tqdm

import src.pandas_frame
from src.outils import search_xml

from src.ivcurve import plot_iv_data
from src.ref_transmission import plot_transmission_spectra
from src.transmission import plot_transmission_spectra_all
from src.flat_transmission import plot_flat_transmission_spectra

def main():
    # CSV 파일을 저장할 디렉토리 경로
    csv_directory = os.path.join('res', 'CSV')
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    # 여러 디렉토리 경로
    target_folder = './dat'
    xml_files = search_xml(target_folder)
    final_df = src.pandas_frame.pandas_data(xml_files)
    print(final_df)

    csv_name = datetime.strftime(datetime.now(), '%Y%m%dT%H%M%S')
    csv_file_path = os.path.join(csv_directory, f'{csv_name}.csv')  # res/CSV 디렉토리에 있는 pandas.csv 파일 경로
    final_df.to_csv(csv_file_path, index=False)

    # Plot
    for xml_file in tqdm(xml_files):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        plt.figure(figsize=(24, 12))

        # Transmission spectra - as measured
        ax = plt.subplot(2, 3, 1)
        plot_transmission_spectra_all(ax, root)

        # Plot Transmission spectra - Processed and fitting
        ax = plt.subplot(2, 3, 2)
        plot_transmission_spectra(ax, root)

        # Flat Transmission spectra - as measured
        ax = plt.subplot(2, 3, 3)
        # plot_flat_transmission_spectra_measured(transmission_spectras, best_fit)
        plot_flat_transmission_spectra(ax, root)

        # IV raw data & fitted dat
        ax = plt.subplot(2, 3, 4)
        plot_iv_data(ax, root)

        # 차트 표시
        plt.subplots_adjust(left=0.1,
                            bottom=0.1, 
                            right=0.9, 
                            top=0.9, 
                            wspace=0.4, 
                            hspace=0.35)

        fig_path = os.path.join('./res/JPG', xml_file.replace('.xml', '.jpg'))
        os.makedirs(os.path.dirname(fig_path), exist_ok=True)
        plt.savefig(fig_path, dpi=300)

if __name__ == "__main__":
    main()
