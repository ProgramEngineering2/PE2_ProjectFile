import xml.etree.ElementTree as ET
import matplotlib.pyplot as mp
import numpy as np
import sklearn.metrics as sm


tree=ET.parse("C:/Users/seung/OneDrive/바탕 화면/2024-1 수업자료/공학 프로그래밍 2/HY202103_D07_(0,0)_LION1_DCM_LMZC-1/HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()
# print(root.tag)
# print(root.attrib)
# for child in root:
#     print(child.tag, child.attrib)


iv_measurement_element = root.find('.//IVMeasurement')
current_unit = iv_measurement_element.get('CurrentUnit')
voltage_unit = iv_measurement_element.get('VoltageUnit')
# print(iv_measurement_element.attrib)
# print("CurrentUnit:", current_unit)
# print("VoltageUnit:", voltage_unit)
voltage_text = iv_measurement_element.find('.//Voltage').text
current_text = iv_measurement_element.find('.//Current').text


# print(voltage_text)
# print(current_text)

voltage_text = voltage_text.replace(",", " ")
current_text = current_text.replace(",", " ")


voltage_text = [float(text) for text in voltage_text.split()]
current_text = [float(text) for text in current_text.split()]

print(voltage_text)
print(current_text)
# 절댓값 적용
current_values_abs = np.abs(current_text)

# 로그 스케일 적용 (0값은 처리되지 않도록 조정)
# current_values_log = np.where(current_values_abs > 0, np.log(current_values_abs), 0)

# 그래프 그리기
# mp.figure(figsize=(10, 6))
# mp.plot(voltage_text, current_values_log, marker='o')

x=np.array(voltage_text)
y=np.array(current_values_abs)
fit=np.polyfit(x,y,13)


num=len(x)

for i in range(num):
    fit=-6.36817000e-05*x**13 -1.80879530e-04*x**12  +8.68776787e-04*x**11  +4.68638421e-03*x**10+7.40906362e-03*x**9  +2.50094781e-03*x**8 -4.98258828e-03*x**7 -4.79205712e-03*x**6-1.62052413e-04*x**5  +1.19588231e-03*x**4  +3.01204806e-04*x**3 -5.66322337e-05*x**2-1.70862949e-05*x  +3.49864485e-11


mp.xlabel('Voltage[V]')
mp.ylabel('Current[A]')
mp.title('Voltage vs Logarithmic Absolute Current')

mp.scatter(x, y)
mp.yscale('log')
mp.plot(x, y)
mp.show()




# 그리드 추가
mp.grid(True)

# 그래프 표시
# mp.show(fit)

