import requests
from bs4 import BeautifulSoup
import pandas as pd

# 獲取網頁內容
response = requests.get('https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx')

# 解析網頁內容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的表格元素
tables = soup.find_all('table')

# 將 HTML 表格轉換為 DataFrame
df1 = pd.read_html(str(tables[0]))[0]
df2 = pd.read_html(str(tables[1]))[0]

# 印出 DataFrame
print(df1)
print(df2)

# 將 DataFrame 寫入 CSV 檔案
df2.to_csv("C:/Users/USER/Desktop/oil.csv", index=False)

# df2 只保留前5個欄位的資料
df2 = df2.iloc[:, :5]

# 去除值是NaN的資料
df2 = df2.dropna()

# 把第一欄的資料型態 轉成 datetime
df2[df2.columns[0]] = pd.to_datetime(df2[df2.columns[0]])

print (df2)

# 使用 matplotlib x,y 散佈圖 , x 軸是日期 , 後面四個欄位是 油價 ，分別是 92無鉛汽油,95無鉛汽油,98無鉛汽油,超級柴油 
import matplotlib.pyplot as plt
plt.plot(df2[df2.columns[0]], df2[df2.columns[1]], label='92無鉛汽油')
plt.plot(df2[df2.columns[0]], df2[df2.columns[2]], label='95無鉛汽油')
plt.plot(df2[df2.columns[0]], df2[df2.columns[3]], label='98無鉛汽油')
plt.plot(df2[df2.columns[0]], df2[df2.columns[4]], label='超級柴油')
plt.legend(loc='upper left')
plt.show()
