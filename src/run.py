import matplotlib.pyplot as plt
import pandasall
import os

def main():
    # CSV 파일을 저장할 디렉토리 경로
    csv_directory = os.path.join('res', 'CSV')
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    final_df = pandasall.pandas_data()
    print(final_df)
    csv_file_path = os.path.join(csv_directory, 'pandas.csv')  # res/CSV 디렉토리에 있는 pandas.csv 파일 경로
    final_df.to_csv(csv_file_path, index=False)


if __name__ == "__main__":
    main()

from ivcurve import plot_iv_data
from transmission import plot_transmission_spectra_all
from ref_transmission import plot_transmission_spectra
from flat_transmission import plot_flat_transmission_spectra

fig, ax = plt.subplots()

plot_iv_data(ax)
plot_transmission_spectra_all(ax,root)
plot_transmission_spectra(ax,root)
plot_flat_transmission_spectra(ax,root)
plt.show()
