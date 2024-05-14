import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame as  df 
from pandas import read_csv
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d import Axes3D

#read ('TDCS_M05A_20240429_cub.csv', index=False) as df
# the first line is column names

dataframe1 = read_csv('TDCS_M05A_20240429_cub.csv', index_col=False)


#filter the data with timeinterval = 0.0 , highwaynumber = '01F' and direction = 'S'
#then filter the data with to_highwaynumber = '01F' and to_direction = 'S'
dataframe1 = dataframe1[(dataframe1['highwaynumber'] == '01F') & (dataframe1['direction'] == 'S')]
dataframe1 = dataframe1[(dataframe1['to_highwaynumber'] == '01F') & (dataframe1['to_direction'] == 'S')]


# data 是車流量觀測數據，是一個包含時間 (TimeInterval 、里程 (millage) 和車流量 (tv31) 的 NumPy 數組
# 將 dataframe['TimeInterval'] , dataframe['millage'] 和 dataframe['tv31'] 轉換為 NumPy 數組
# dataframe1['millage'] = dataframe1['millage'].astype(int)
#data = np.array([[時間1, 里程1, 車流量1], [時間2, 里程2, 車流量2], ...])
data = np.array([dataframe1['TimeInterval'], dataframe1['millage'].astype(int), dataframe1['tv31']]).T

print (data)
# 創建一個新的圖形 
# 畫出多視角圖形  重 111, 110, 101, 100
# add four subplots to the figure
# subplot(111) is subplot(111,portjection='3d')

# 對時間和里程數據進行網格化
# 假設 x (時間) 和 y (里程) 已經是規則的網格數據
x = np.linspace(data[:, 0].min(), data[:, 0].max(), num=50)  # 調整 num 以匹配數據點的密度
y = np.linspace(data[:, 1].min(), data[:, 1].max(), num=50)
x, y = np.meshgrid(x, y)

# 插值找到每個 (x, y) 點對應的 z (車流量)
from scipy.interpolate import griddata
z = griddata((data[:, 0], data[:, 1]), data[:, 2], (x, y), method='cubic')


fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
# 繪製曲面圖
surf = ax.plot_surface(x, y, z, cmap='viridis')

# 添加顏色條
#fig.colorbar(surf)

# 設置坐標軸標籤
ax.set_xlabel('Time')
ax.set_ylabel('Mileage')
ax.set_zlabel('Traffic Volume')


ax1 = fig.add_subplot(122, projection='3d')
# 繪製曲面圖
surf = ax1.plot_surface(x, y, z, cmap='viridis')
# 設置坐標軸標籤
ax1.set_xlabel('Time')
ax1.set_ylabel('Mileage')
ax1.set_zlabel('Traffic Volume')
ax1.view_init(elev=45, azim=60)

plt.tight_layout()
# 顯示圖形
plt.savefig('cubicspline_2v.png')
print(data)