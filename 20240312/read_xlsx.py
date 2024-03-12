import pandas as pd


#得到這個檔案 __file__ 是這個檔案的路徑
import os
path = os.path.abspath(__file__)
#get the folder of this file
path = os.path.dirname(path)


# 從 Excel 文件讀取數據
excel_file = '112年1-10月交通事故簡訊通報資料.xlsx'

filepath = os.path.join(path ,excel_file)


# 讀取 Excel 文件
df = pd.read_excel(filepath, sheet_name='交通事故簡報通報資料')

#篩選 欄位名稱 為'國道名稱' 的資料， 我只要名稱為'國道1號'的資料
df1 = df[df['國道名稱'] == '國道1號']

#把 欄位 '年' '月' '日' '時' '分'
#合併成一個欄位 '日期' , 並且轉換成日期格式
df1['日期'] = df1['年'].astype(str) + '-' + df1['月'].astype(str) + '-' + df1['日'].astype(str) + ' ' + df1['時'].astype(str) + ':' + df1['分'].astype(str)

#drop 欄位 '年' '月' '日' '時' '分'
df1 = df1.drop(columns=['年', '月', '日', '時', '分'])

print(df1)

