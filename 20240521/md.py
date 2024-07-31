# 中原大學 土木系 ＡＩ於土木之應用 第二次期中考：
# 第一題： 爬蟲程式
# 撰寫一個爬蟲程式，能夠下載2024年1月1日至4月30日的高速公路交通資料(M05A)。並完成以下要求：

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
############################################################################################################
#（請注意期中考要求要合併，上星期的(2024/05/21 課堂作業不需要合併）
############################################################################################################
# 檔案的實際狀況會隨著時間改變，我們無法確定每一天的檔案狀態。
# 因此，我們需要一個能夠自動判斷每一天在網路上的資料是哪一種形式檔案，然後進行下載。
####################################################################
# M05A : 原始的檔案資料欄位如下
# TimeInterval、GantryFrom、GantryTo、VehicleType、SpaceMeanSpeed、交通量

# 合併檔案的格式需重新整理成以下的型態：
# TimeInterval、GantryFrom、GantryTo、SpaceMeanSpeed（只要小客車 31)、交通量(小客車 31)
# 、交通量(小貨車 32)、交通量(大客車 41)、交通量(大貨車 42)、交通量(聯結車 5)


# 第二題: 資料特徵化（時間）與 （空間）資訊
# 請將合併後的檔案進行資料特徵化，將TimeInterval欄位改為每天的第n個（5分鐘）

# 增加新的欄位. WeekDay 為星期幾 （0~6）0代表星期日

# 增加新的欄位. HellDay 為假日 （0,1, -1）0代表非假日, 1代表假日, -1代表假日前一天 
#    假日定義為星期六或星期日: ‘中秋節’‘元旦’‘春節’‘清明節’‘端午節’‘國慶日’‘勞動節’
#    ‘雙十節’‘元宵節’‘重陽節’‘除夕’‘春節’‘端午節’‘中秋節’‘元宵節’‘重陽節’‘除夕’
#    假日前一天為假日前一天的星期五或連續假期的前一天

# 增加新的欄位. WayIDFrom 為起使門架的編號前三碼. (字串)
# 增加新的欄位. WayIDTo   為終點門架的編號前三碼. (字串)
# 增加新的欄位. WayMilageFrom 為起使門架的里程. (數值)
# 增加新的欄位. WayMilageTo   為終點門架的里程. (數值)
# 增加新的欄位. WayDirectionFrom 為起使門架的方向. (字串   N:北, S:南, W:西, E:東)
# 增加新的欄位. WayDirectionTo   為終點門架的方向. (字串   N:北, S:南, W:西, E:東)

# 增加新的欄位. 速度分級  SpeedClass  (0,1,2,3,4,5) 
# 0代表速度為0 （或者沒有車量與沒有資料）, 1代表速度小於20, 2代表速度介於20~40, 
# 3代表速度介於40~60, 4代表速度介於60~80, 5代表速度大於80 

# 特徵化後的檔案命名如 M05A_20240416_feature.csv

# 第三題: 資料特視覺化繳交html 檔,
# 表現 2024 /04/29 的交通量 與 車速 隨時間與高速公路里程的變化。

import urllib.request
import requests
import datetime
import tarfile

def url_exists(url):
    response = requests.head(url)
    return response.status_code == 200

start_date = datetime.date(2024, 7, 10)
end_date = datetime.date(2024, 7, 15)

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