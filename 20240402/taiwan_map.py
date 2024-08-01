#尋找台灣的區界地圖 shape file/ geojson file
#https://data.gov.tw/dataset/7441

#read 20240402/tract_20140313.json as geopanas
import geopandas as gpd
import pandas as pd

#read shape file
taiwan=gpd.read_file('20240402/county/county_moi_1090820.shp')
import os
#print cwd
print (taiwan)

#plot taiwan using matplotlib
import matplotlib.pyplot as plt

#輸出台灣地圖的時候 圖面顯示的範圍 緯度最低為21.5度 緯度最高為25.5度 經度最低為119度 經度最高為122度
taiwan.plot()
plt.xlim(119,122)
plt.ylim(21.5,25.5)
plt.show()
#save to png file
plt.savefig('20240402/taiwan_map.png')
