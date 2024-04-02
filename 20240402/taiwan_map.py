#尋找台灣的區界地圖 shape file/ geojson file
#https://data.gov.tw/dataset/7441

#read 20240402/tract_20140313.json as geopanas
import geopandas as gpd
import pandas as pd

#read geojson file
taiwan=gpd.read_file('20240402/tract_20140313.json')
import os
#print cwd
print (taiwan.shape)