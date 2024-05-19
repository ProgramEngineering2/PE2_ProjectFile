import matplotlib.pyplot as plt
import pandasall

def main():
    final_df = pandasall.pandas_data()
    print(final_df)
    final_df.to_csv('./pandas.csv')

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
