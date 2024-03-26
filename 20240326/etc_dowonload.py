import os
import requests
import time

# filename 最後面的數字代表的是小時 分鐘 與秒，例如 000000 代表 00:00:00 
# 000500 代表 00:05:00
# 如果每5分鐘一筆資料,利用迴圈產生檔名
# 例如: TDCS_M03A_20240325_000000.csv
#        TDCS_M03A_20240325_000500.csv

for i in range(0,24):
    for j in range(0, 60, 5):

        time.sleep(1)
        url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/' + str(i).zfill(2) + '/'
        filename = 'TDCS_M03A_20240325_' + str(i).zfill(2) + str(j).zfill(2) + '00.csv'

        urletc = url + filename

        print(urletc)
        #get the data from the url

        response = requests.get(urletc)
        response.encoding = 'big5'
        # save the data to a file
        with open( os.path.join('20240326', filename), 'w') as f:
            f.write(response.text)
        
        response.close()