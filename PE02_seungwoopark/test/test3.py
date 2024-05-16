import numpy as np
import matplotlib.pyplot as plt

# 상수 정의
Is = 1e-12  # 포화 전류 (A)
n = 1.5  # 이상 계수
Vt = 0.025  # 열전압 (Volt)

# 전압 범위 설정
V = np.linspace(-0.2, 0.7, 400)  # -0.2V부터 0.7V까지

# 쇼클리 다이오드 방정식 계산
I = Is * (np.exp(V / (n * Vt)) - 1)

# 0 이하의 값은 그래프에 로그 스케일로 표현할 때 문제를 일으킬 수 있으므로 필터링


# 그래프 그리기
plt.figure(figsize=(8, 6))
plt.semilogy(V, I, label='Diode Current (log scale)')
plt.title('Shockley Diode Equation on Log Scale')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (log scale)')
plt.grid(True)
plt.legend()
plt.show()