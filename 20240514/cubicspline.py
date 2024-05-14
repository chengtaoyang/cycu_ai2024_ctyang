import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# 假設的數據
x = np.array([0, 1, 2, 3, 4, 5])  # 時間 (小時)
y = np.array([0, 1.2, 2.9, 6.8, 12.3, 20.0])  # 高程 (公尺)
z = np.array([22, 21, 20.5, 21.5, 23, 24])  # 溫度 (攝氏度)

# 使用 scipy 的 CubicSpline 來擬合 x 對 y 的關係
cs = CubicSpline(x, y)

# 畫出擬合後的曲線
x_new = np.linspace(0, 5, 100)
y_new = cs(x_new)

plt.figure(figsize=(8, 4))
plt.plot(x, y, 'o', label='原始數據')
plt.plot(x_new, y_new, label='Cubic Spline 擬合曲線')
plt.xlabel('時間 (小時)')
plt.ylabel('高程 (公尺)')
plt.title('時間對高程的 Cubic Spline 擬合')
plt.legend()
plt.show()