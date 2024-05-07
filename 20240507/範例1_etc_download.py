import os
import time
import random
import datetime
import requests
import pandas as pd
from dateutil import relativedelta
import tarfile
import requests
from pandas.tseries.offsets import MonthEnd

def check_files(day_beg, day_end):
    problem_files = []  # 初始化一個空的 list 來儲存有問題的檔案

    for day_cur in pd.date_range(day_beg, day_end):
        time.sleep(0.001 * random.randint(1, 2000)  )
        day_cur_str = day_cur.strftime("%Y%m%d")
        
        url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/M04A_" + str(day_cur_str) + ".tar.gz"
        print(url)

        try:
            r = requests.get(url, stream=True)
            if r.status_code != 200:
                problem_files.append(url)

        except requests.exceptions.RequestException as e:
            problem_files.append(url)

    return problem_files

def download_and_extract_files(day_beg, day_end, download_dir):

    err_tree = {}
    df_csv_list = []     # 初始化一個空的 list
    day_cur = day_beg

    for day_cur in pd.date_range(start=day_beg, end=day_end):
        # 檔案路徑與檔案網址
        day_cur_str = day_cur.strftime("%Y%m%d")
        file_path   = os.path.join(download_dir, "M04A_" + str(day_cur_str) + ".tar.gz")
        url         = "https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/M04A_" + str(day_cur_str) + ".tar.gz"
        
        err_tree[day_cur_str] = {}

        # 下載 .tar.gz 檔案
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(file_path, "wb") as code:
                code.write(r.content)

        except requests.exceptions.RequestException as err:
            err_tree[day_cur_str]['download'] = err
            continue

        # 解壓縮 .tar.gz 檔案
        try:
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(path=download_dir)
        except tarfile.ReadError as err:
            err_tree[day_cur_str]['extract'] = err
            continue

        # 讀取 .csv 檔案
        # 這裡的檔案路徑要注意一下，因為解壓縮後的檔案會放在 download_dir/M04A/日期/小時/檔案.csv  所以要用 os.path.join() 來組合路徑
        # 例如：download_dir = '/home/user/Downloads'，日期為 20190101，小時為 00，檔案為 TDCS_M04A_20190101_000000.csv
        # 則檔案路徑為 /home/user/Downloads/M04A/20190101/00/TDCS_M04A_20190101_000000.csv
        step_delta = datetime.timedelta(minutes=5)
        step_1st   = datetime.datetime.combine(day_cur, datetime.time(0, 0, 0))
        step_end   = datetime.datetime.combine(day_cur, datetime.time(23, 55, 0))
        for step in pd.date_range(start=step_1st, end=step_end, freq=step_delta):
            hour_str = step.strftime("%H")
            minutes_str = step.strftime("%M")
            csv_file_path = f"{download_dir}/M04A/{day_cur_str}/{hour_str}/TDCS_M04A_{day_cur_str}_{hour_str}{minutes_str}00.csv"

            try:    
                df_csv = pd.read_csv(csv_file_path, names=["c1", "c2", "c3", "c4", "c5", "c6"])
                df_csv_list.append(df_csv)

            except FileNotFoundError:   
                err_tree[day_cur_str][f"step_{hour_str}{minutes_str}"] = "FileNotFoundError"
                continue    

    #check if there is any error
    for day_str, err_day in err_tree.items():
        #if err_day is not empty then print
        if err_day:
            print (day_str, err_day)

    
    #concat df_csv_list to df
    print (day_beg,day_end,(day_end - day_beg).days ,'file_number=', len(df_csv_list))
    return pd.concat(df_csv_list)
 
if __name__ == '__main__':
 
    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # for loop for the first month(the first day) to the last month(the first day of the last month)
    # for each month
    month_beg = datetime.datetime(2016, 10, 1, 0, 0, 0)
    month_end = datetime.datetime(2016, 12, 31, 0, 0, 0)

    #check if the files are available
    problem_files = check_files(month_beg, month_end)
    print (problem_files)

    for month_beg in pd.date_range(start=month_beg, end=month_end, freq='MS'):
        #get the first day of the month
        day_beg = month_beg
        #get the last day of the month
        day_end = month_beg + MonthEnd()

        df = download_and_extract_files(day_beg, day_end, download_dir)
        file_path = os.path.join(download_dir, f"M04A_{day_beg.strftime('%Y%m')}.pdbinary.zip")

        print (day_beg, file_path, df.shape, df.dtypes)
        print (df.head(1))
        print (df.tail(1))

        #compress df to zip file
        df.to_pickle(file_path, compression='zip')