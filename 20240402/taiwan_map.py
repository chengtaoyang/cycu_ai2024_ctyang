#尋找台灣的區界地圖 shape file/ geojson file
#https://data.gov.tw/dataset/7441

#read 20240402/tract_20140313.json as geopanas
import geopandas as gpd
import pandas as pd

#read shape file
taiwan=gpd.read_file('20240402/county/county_moi_1090820.shp')
import os
#print cwd
print (taiwan.shape)

#plot taiwan using matplotlib
import matplotlib.pyplot as plt
taiwan.plot()
plt.show()
#save to png file
plt.savefig('20240402/taiwan_map.png')
