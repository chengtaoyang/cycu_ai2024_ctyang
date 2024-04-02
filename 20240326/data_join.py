import os
import time
import pandas as pd
# filename 最後面的數字代表的是小時 分鐘 與秒，例如 000000 代表 00:00:00 
# 000500 代表 00:05:00
# 如果每5分鐘一筆資料,利用迴圈產生檔名
# 例如: TDCS_M03A_20240325_000000.csv
#        TDCS_M03A_20240325_000500.csv

for i in range(0,24):
    for j in range(0, 60, 5):

        time.sleep(1)

        filename = 'TDCS_M03A_20240325_' + str(i).zfill(2) + str(j).zfill(2) + '00.csv'
        path = os.path.join('20240326', filename)
        # read data from the path to a DataFrame
        df = pd.read_csv(path)
        print(path, df.shape)
        