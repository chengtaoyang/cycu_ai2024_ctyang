import datetime

#期中考作業 寫一個爬蟲程式可以下載 2024 1月1日 到4月30日的每日資料 etc 資料
#2024 1 月 1 日 的檔案 是一個壓縮檔案 
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_20240101.tar.gz

#2024 4 月 16 日 是這種形式的檔案
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000000.csv
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000500.csv
# /00/ 代表是 00 時.   000500 24 小時制的時間 代表 00:05:00
# 也就是 2024 4 月 16 日 的 00:05:00 的資料
# 每一天有 288 個檔案, 對於這種檔案我們需要一個一個抓下來然後合併。
# 這種狀況會隨時間改變，所以我們無法確定每一天的檔案的狀態。import urllib.request
# 所以需要一個程式可以判斷 每一天的在網路上的資料 是哪一種形式，然後下載。

import urllib.request
import requests
import datetime
import tarfile

def url_exists(url):
    response = requests.head(url)
    return response.status_code == 200

start_date = datetime.date(2024, 4, 20)
end_date = datetime.date(2024, 4, 15)

current_date = start_date
while current_date <= end_date:
    file_date = current_date.strftime("%Y%m%d")
    tar_file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_{file_date}.tar.gz"
    tar_file_name = f"M05A_{file_date}.tar.gz"
    
    if url_exists(tar_file_url):
        urllib.request.urlretrieve(tar_file_url, tar_file_name)
        with tarfile.open(tar_file_name, 'r:gz') as tar:
            tar.extractall()
    else:
        for hour in range(24):
            for minute in range(0, 60, 5):
                file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{file_date}/{str(hour).zfill(2)}/TDCS_M05A_{file_date}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                if url_exists(file_url):
                    file_name = f"M05A_{file_date}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                    urllib.request.urlretrieve(file_url, file_name)
    
    current_date += datetime.timedelta(days=1)