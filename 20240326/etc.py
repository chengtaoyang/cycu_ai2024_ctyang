
import requests

url = 'http://tisvcloud.freeway.gov.tw/history/TDCS/00'

filename ='''TDCS_M03A_20240325_000000.csv'''
# filename 最後面的數字代表的是小時 分鐘 與秒，例如 000000 代表 00:00:00 
# 000500 代表 00:05:00
# 如果每5分鐘一筆資料,利用迴圈產生檔名
# 例如: TDCS_M03A_20240325_000000.csv
#        TDCS_M03A_20240325_000500.csv
for i in range(0, 1):
    for j in range(0, 60, 5):
        filename = 'TDCS_M03A_20240325_' + str(i).zfill(2) + str(j).zfill(2) + '00.csv'
        print(filename)

        urletc = url + filename

        #get the data from the url


        response = requests.get(urletc)
        response.encoding = 'big5'
        # save the data to a file
        with open(filename, 'w') as f:
            f.write(response.text)