import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Model
from scipy.optimize import curve_fit

tree=ET.parse("./HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()

iv_measurement_element = root.find('.//IVMeasurement')
current_unit = iv_measurement_element.get('CurrentUnit')
voltage_unit = iv_measurement_element.get('VoltageUnit')

voltage_text = iv_measurement_element.find('.//Voltage').text
current_text = iv_measurement_element.find('.//Current').text

voltage_text = voltage_text.replace(",", " ")
current_text = current_text.replace(",", " ")

voltage_text = [float(text) for text in voltage_text.split()]
current_text = [float(text) for text in current_text.split()]

x_data=np.array(voltage_text)
y_data=np.array((current_text))
y_data_abs=np.abs(current_text)

# Define a modified diode current model with linear and exponential components
def diode_current(VD, IS, n, VT, V_linear, I_linear, Rs):
    return np.where(VD < V_linear, I_linear * VD, IS * (np.exp(VD/ (n * VT)) - 1))

# Initialize the model
model = Model(diode_current)
params = model.make_params(IS=1, n=1, VT=0.025, V_linear=0, I_linear=-6.4391e-09, Rs=0)  # Initial guess for parameters

# Fit the model to the data
result = model.fit(y_data, params, VD=x_data)

# Print the fitting results
print(result.fit_report())

# Plot the original data and the fitted curve
plt.scatter(x_data, y_data_abs, label='Data')
plt.plot(x_data, result.best_fit, 'r-', label='Fitted curve')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.yscale('log')
plt.legend()
plt.show()
