import xml.etree.ElementTree as ET
import numpy as np
import warnings
import matplotlib.pyplot as plt

# Suppress rank warnings from numpy
warnings.filterwarnings("ignore", category=np.RankWarning)

# Parse XML file with ElementTree
tree = ET.parse("example.xml")
root = tree.getroot()  # Get the root element of the XML tree

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
    plt.plot(x, [y1 - y2 - (slope * x_val + intercept) for y1, y2, x_val in zip(y_meas, function(x), x)], label=f'{label}V', linestyle='-')
for label, x, y_meas in ref_data:
    x = np.array(x, dtype=float)
    y_meas = np.array(y_meas, dtype=float)
    plt.plot(x, [y1 - y2 for y1, y2 in zip(y_meas, y)], label=f'{label}V', linestyle='-')

plt.legend(ncol=3)
plt.xlabel('Wavelength [nm]')
plt.ylabel('Measured transmission [dB]')
plt.title('Transmission spectra - as measured')

plt.show()