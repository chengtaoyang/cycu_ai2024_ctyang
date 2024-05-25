# 中原大學 土木系 ＡＩ於土木之應用 第二次期中考：
# 撰寫一個爬蟲程式，能夠下載2024年1月1日至4月30日的高速公路交通資料。並完成以下要求：

# 2024年1月1日的檔案是壓縮檔案的形式，如下所示：
# https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_20240101.tar.gz
# 這個檔案裡面包含了2024年1月1日的288個檔案，每個檔案代表一個5分鐘的時間區間。
# 請下載並解壓縮這個檔案，然後將裡面的288個檔案合併成一個檔案。 命名為 M05A_20240101.csv。

# 2024年4月16日的檔案則可能是以下這種形式：
# https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000000.csv
# https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000500.csv
# 其中，"/00/"代表的是00時，"000500"則是24小時制的時間，代表00:05:00。
# 也就是說，這是2024年4月16日00:05:00的資料。
# 每一天有288個檔案，對於這種檔案，我們需要一個一個下載並進行合併。 命名為 M05A_20240416.csv。

#（請注意期中考要求要合併，上星期的課堂作業不需要合併）
# 檔案的實際狀況會隨著時間改變，我們無法確定每一天的檔案狀態。
# 因此，我們需要一個程式，能夠判斷每一天在網路上的資料是哪一種形式，然後進行下載。
# M05A_20240101.csv 這些檔案的格式需重新整理成以下的樣式：
# 車道代碼, 車道方向, 車道編號, 車流量, 平均速度, 平均佔有率, 發生時間

#2 動態網頁地圖


#3 特徵化時間與空間資訊

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