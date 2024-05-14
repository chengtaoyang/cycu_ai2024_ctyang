import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame as  df 
from pandas import read_csv
from scipy.interpolate import CubicSpline

# M03A : TimeInterval、GantryID、Direction、VehicleType、交通量
# M04A : TimeInterval、GantryFrom、GantryTo、VehicleType、TravelTime、交通量
# M05A : TimeInterval、GantryFrom、GantryTo、VehicleType、SpaceMeanSpeed、交通量
# M06A : VehicleType、DetectionTime_O、GantryID_O、DetectionTime_D、GantryID_D、TripLength、TripEnd、TripInformation

# the columns of TDCS_M05A_20240429_5.csv  lists as follows:
# TimeInterval,GantryFrom,GantryTo,SpaceMeanSpeed,tv31,tv32,tv41,tv42,tv5

#read ('TDCS_M05A_20240429_5.csv', index=False) as df
# the first line is column names

dataframe1 = read_csv('TDCS_M05A_20240429_5.csv', index_col=False)


#  TimeInterval format as 2024/04/29 00:00
# convert TimeInterval to integer to represent nth 5-minute interval of the day
# the first interval is 0
dataframe1['TimeInterval'] = dataframe1['TimeInterval'].str.split(' ').str[1].str.split(':').str[0].astype(int)*12 + dataframe1['TimeInterval'].str.split(' ').str[1].str.split(':').str[1].astype(int)/5

# GantryFrom format as 03F0000S
# spearte the number first 3 characters as highwaynumber ,the 4-7th characters as millage, the 8th character as direction
dataframe1['highwaynumber'] = dataframe1['GantryFrom'].str[0:3]
dataframe1['millage'] = dataframe1['GantryFrom'].str[3:7] 
dataframe1['direction'] = dataframe1['GantryFrom'].str[7]


# GantryTo format as 03F0000S
# spearte the number first 3 characters as highwaynumber ,the 4-7th characters as millage, the 8th character as direction
dataframe1['to_highwaynumber'] = dataframe1['GantryTo'].str[0:3]
dataframe1['to_millage'] = dataframe1['GantryTo'].str[3:7]
dataframe1['to_direction'] = dataframe1['GantryTo'].str[7]


#filter the data with timeinterval = 0.0 , highwaynumber = '01F' and direction = 'S'
dataframe1 = dataframe1[(dataframe1['TimeInterval'] == 0.0) & (dataframe1['highwaynumber'] == '01F') & (dataframe1['direction'] == 'S')]

#filter the data with to_highwaynumber = '01F' and to_direction = 'S'
dataframe1 = dataframe1[(dataframe1['to_highwaynumber'] == '01F') & (dataframe1['to_direction'] == 'S')]

#convert the millage to integer
dataframe1['millage'] = dataframe1['millage'].astype(int)
print(dataframe1.head(), dataframe1.tail(), dataframe1.shape)

# sort the dataframe by millage
dataframe1 = dataframe1.sort_values(by='millage')
x = dataframe1['millage']
y = dataframe1['tv31']


cs = CubicSpline(x, y)

new_x = np.linspace(x.min(), x.max(), 500)
new_y = cs(new_x)

# # 畫出擬合後的曲線
fig = plt.figure()
plt.plot(x, y, 'o', label='data')
plt.plot(new_x, new_y, label="spline")
plt.legend()
plt.savefig('cubicspline.png')