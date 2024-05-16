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

x=np.array(voltage_text)
y_data=np.array((current_text))
y_data_abs=np.abs(current_text)
num=len(x)

fit1=np.polyfit(x, y_data_abs, 12)
print(fit1)
graph=np.poly1d(fit1)
print(graph)
y_data_abs[2]=3.510694e-08


for i in range(num):
    fit1= 2.33051521e-04*x**12  +1.74838027e-03*x**11  +4.97096180e-03*x**10  +6.02174783e-03*x**9 +9.53557123e-04*x**8 -4.71357352e-03*x**7 -3.74378886e-03*x**6 + 8.41739066e-05*x**5 +9.87173550e-04*x**4  +2.26321283e-04*x**3 -4.73096899e-05*x**2 -1.34132477e-05*x**1 + 3.49865490e-11




# plt.plot(x, fit1)

plt.legend()
plt.xlabel('Voltage[V]')
plt.ylabel('|Current[A]|')
plt.title('Voltage vs Logarithmic Absolute Current')
plt.scatter(x, y_data_abs, color='black')
plt.yscale('log')

plt.show()



