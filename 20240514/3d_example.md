import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# 生成隨機數據
np.random.seed(0)
x = np.random.normal(0, 1, 100)
y = np.random.normal(0, 1, 100)
z = x**3 + y**3 + 3*x**2*y + 3*x*y**2 + np.random.normal(0, 0.1, 100)

# 建立立方擬合模型
coefficients = np.polyfit(x + y, z, 3)
model = np.poly1d(coefficients)

# 使用擬合模型預測z值
z_pred = model(x + y)

# 繪制原始數據和擬合曲線
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, color='r', label='Actual data')
ax.scatter(x, y, z_pred, color='b', label='Fitted data')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.legend()
plt.show()
