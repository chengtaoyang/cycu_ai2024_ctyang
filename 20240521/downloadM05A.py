import datetime

# 第1題 (30%)
# 期中考作業 寫一個爬蟲程式可以下載 2024 1月1日 到4月30日的每日資料 etc 資料
# 資料格式有兩種
## 第一種格式: 2024 1 月 1 日 的檔案 是一個壓縮檔案 
### 格式大概如下
### https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_20240101.tar.gz

## 第二種格式: 2024 4 月 16 日 是這種形式的檔案，每5分鐘一個檔案
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000000.csv
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000500.csv
# /00/ 代表是 00 時.   000500 24 小時制的時間 代表 00:05:00
# 也就是 2024 4 月 16 日 的 00:05:00 的資料
# 每一天有 288 個檔案, 對於這種檔案我們需要一個一個抓下來然後合併。
# 這種狀況會隨時間改變，所以我們無法確定每一天的檔案的狀態。import requests
# 所以需要一個程式可以判斷 每一天的在網路上的資料 是哪一種形式，然後下載。


import requests
import datetime
import tarfile

def url_exists(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else Happened",err)
        return False
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return False
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return False
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return False

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

class M05A:
    def __init__(self, date):
        self.date = date

        self.file_direrctory = "data"

        self.file_date = date.strftime("%Y%m%d")

        self.file_name  = f"M05A_{self.file_date}.tar.gz"

        self.file_url   = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{self.file_name}"

        self.targz_url_exists = url_exists(self.file_url)

        self.csv_filelist = []

        if self.targz_url_exists == False:
            for hour in range(24):
                for minute in range(0, 60, 5):
                    csv_file_name = f"TDSC_M05A_{self.file_date}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                    file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{self.file_date}/{str(hour).zfill(2)}/{csv_file_name}"
                    if url_exists(file_url):
                        self.csv_filelist.append([file_url,csv_file_name])

        self.csv_url_exists = ( len(self.csv_filelist) == 288)

class M05A_data:
    def __init__(self, start_date = datetime.date(2024, 6, 10), end_date = datetime.date(2024, 6, 17)  ) :
        current_date = start_date

        self.M05A_list = []
        while current_date <= end_date:
            self.M05A_list.append(M05A(current_date))
            current_date += datetime.timedelta(days=1)

def download_M05A(start_date = datetime.date(2024, 6, 10), end_date = datetime.date(2024, 6, 17)):
    
    current_date = start_date
    file_direrctory = "data"

    while current_date <= end_date:
        file_date = current_date.strftime("%Y%m%d")
        tar_file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_{file_date}.tar.gz"
        tar_file_name = f"M05A_{file_date}.tar.gz"

        print (tar_file_name, tar_file_url)
        
        if url_exists(tar_file_url):
            #download tar file
            download_file(tar_file_url, tar_file_name)

        else:
            for hour in range(24):
                for minute in range(0, 60, 5):
                    file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{file_date}/{str(hour).zfill(2)}/TDCS_M05A_{file_date}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                    if url_exists(file_url):
                        file_name = f"M05A_{file_date}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                        download_file(file_url, file_name)
        
        current_date += datetime.timedelta(days=1)

if __name__ == '__main__':

    beg = datetime.date(2024, 7, 10) 
    end = datetime.date(2024, 7, 17)

    abc = M05A_data(beg, end)

    for i in abc.M05A_list:
        print (i.date, i.targz_url_exists, i.csv_url_exists, len(i.csv_filelist))

    
    #download_M05A(datetime.date(2024, 7, 10), datetime