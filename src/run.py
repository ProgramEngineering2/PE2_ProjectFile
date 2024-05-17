import matplotlib.pyplot as plt
from memo import plot_iv_data
from memo import plot_transmission_spectra_all
from memo import plot_transmission_spectra
from memo import plot_flat_transmission_spectra

fig, ax = plt.subplots()

plot_iv_data(ax)
plot_transmission_spectra_all(ax,root)
plot_transmission_spectra(ax,root)
plot_flat_transmission_spectra(ax,root)
plt.show()
