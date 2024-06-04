import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 創建一個新的圖形
fig = plt.figure()

# 添加一個 3D 座標軸
ax = fig.add_subplot(111, projection='3d')

# 生成一些示例資料
x = np.random.standard_normal(100)
y = np.random.standard_normal(100)
z = np.random.standard_normal(100)

# 在 3D 座標軸上繪製散點圖
ax.scatter(x, y, z)

# 設置座標軸標籤
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# 顯示圖形
plt.show()