import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import lmfit


tree=ET.parse("./HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()

iv_measurement_element = root.find('.//IVMeasurement')

voltage_text = iv_measurement_element.find('.//Voltage').text
current_text = iv_measurement_element.find('.//Current').text

voltage_text = voltage_text.replace(",", " ")
current_text = current_text.replace(",", " ")

voltage_text = [float(text) for text in voltage_text.split()]
current_text = [float(text) for text in current_text.split()]

x_data=np.array(voltage_text)
y_data=np.array((current_text))
y_data_abs=np.abs(current_text)

def diode_equation(V, Is, n, Vt, V_linear, Ilinear):
    current = []
    for v in V:
        if v >= V_linear:
            current.append(Is * (np.exp(v / (n * Vt)) - 1))
        else:
            current.append(Ilinear * v)
    return current

# 초기 추정값 설정
Is_guess = y_data[0]
n_guess = 1.0
Vt_guess = 0.0256
Ilinear_guess = 0.0
Vlinear_guess =0.0

# 매개변수 및 초기 추정값 정의
params = lmfit.Parameters()
params.add('Is', value=Is_guess, min=0)  # 포화 전류
params.add('n', value=n_guess, min=1)     # 이상성 지수
params.add('Vt', value=Vt_guess, min=0)  # 열전압
params.add('Ilinear', value=Ilinear_guess)  # 음수 전압 영역에서의 전류
params.add('V_linear', value=Vlinear_guess)  # 음수 전압 영역에서의 선형 근사 전압

# 적합 실행 (알고리즘 변경)
result = lmfit.minimize(
    # 잔차 함수
    lambda params, x, y: np.array(diode_equation(x, **params)) - np.array(y),
    # 매개변수 및 데이터
    params, args=(x_data, y_data),
    # 알고리즘 변경
    method='least squares'
)

# 적합된 값 얻기
best_fit = np.abs(y_data) + result.residual

# R-squared 값 계산
ss_residual = np.sum(result.residual ** 2)
ss_total = np.sum(np.abs(y_data) - np.abs(np.mean(y_data)) ** 2)
r_squared = 1 - (ss_residual / ss_total)

ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan=1)
ax1.plot(x_data, best_fit,  color='red', label=f'R^2={r_squared}')
ax1.text(x_data[0], y_data[0], f'({x_data[0]}, {y_data[0]})', fontsize=10, ha='left')
ax1.text(x_data[4], y_data[4], f'({x_data[4]}, {y_data[4]})', fontsize=10, ha='left',)
ax1.text(x_data[12], y_data[12], f'({x_data[12]}, {y_data[12]})', fontsize=10, ha='right')
ax1.legend(prop={'size': 8})
ax1.set_xlabel('Voltage[V]')
ax1.set_ylabel('|Current[A]|')
ax1.set_title('Voltage vs Logarithmic Absolute Current')
ax1.scatter(x_data, y_data_abs, color='black')
ax1.set_yscale('log')

#
# #변수명 잘 적어주기 (디테일)
# #바이모델 (두개를 피팅)
# #로그 플롯인데 오른쪽만 맞아도 상대적으로 잘 나올 수 있음
#
# #-----------------------------------------------------------------------------
# #Transmission line
tree=ET.parse("./HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()
ax2 = plt.subplot2grid((2, 2), (0, 1))

for wavelength_sweep in root.findall('.//WavelengthSweep'):
    dc_bias = wavelength_sweep.get('DCBias')
    length = wavelength_sweep.find('.//L').text
    transm = wavelength_sweep.find('.//IL').text
    length_text = length.replace(",", " ")
    transm_text = transm.replace(",", " ")
    length_float = [float(text) for text in length_text.split()]
    transm_float= [float(text) for text in transm_text.split()]
    data_length=np.array(length_float)
    data_transm=np.array(transm_float)
    ax2.plot(data_length, data_transm, label=f'DCBias={dc_bias}')


ax2.set_title('Transmission Spectrum')
ax2.set_ylabel('Transmission (dB)')
ax2.set_xlabel('Length (nm)')
ax2.legend(ncol=3, prop={'size': 6}, loc='lower center')


#-------------------------------------------------------------------------------
#Transmission fitting
ax3 = plt.subplot2grid((2, 2), (1, 0))

for wavelength_sweep in root.findall('.//WavelengthSweep'):
    dc_bias = wavelength_sweep.get('DCBias')
    length = wavelength_sweep.find('.//L').text
    transm = wavelength_sweep.find('.//IL').text
    length_text0 = length.replace(",", " ")
    transm_text0 = transm.replace(",", " ")
    length_float0 = [float(text) for text in length_text0.split()]
    transm_float0= [float(text) for text in transm_text0.split()]
    if length_float0[0]==1530.0005:
        data_length0=np.array(length_float0)
        data_transm0=np.array(transm_float0)

for i in range(7):
    fit=np.polyfit(data_length0, data_transm0, i+1)
    graph=np.poly1d(fit)
    fit2=np.polyval(fit, data_length0)
    ax3.scatter(data_length0, data_transm0, color='pink')
    ax3.plot(data_length0, fit2, label=f'Dgree={i+1}')

ax3.set_title('Fittied-Transmission Line')
ax3.set_xlabel('Length(nm)')
ax3.set_ylabel('transmission(dB)')
ax3.legend(ncol=3, prop={'size':6})

#--------------------------------------------------------------
#Flat transmission
#
# tree=ET.parse("./HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
# root = tree.getroot()
# ax4 = plt.subplot2grid((2, 2), (1, 1))
#
# def call_trans():
#
#
#
# ax4.set_title('Transmission Spectrum')
# ax4.set_ylabel('Transmission (dB)')
# ax4.set_xlabel('Length (nm)')
# ax4.legend(ncol=3, prop={'size': 6}, loc='lower center')
plt.show()