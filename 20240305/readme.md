
# 今日重點 國道智慧交通管理創意競賽& 爬蟲
https://www.gov.tw/News_Content_11_715821.html

## 我需要一個網路爬蟲的程式來爬梳
以下的網址
https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx

這個網址的內容包含兩個 html 的table 元素
我希望可以解析它的內容把它變成兩個 pandas dataframe

首先，我們需要使用 `requests` 和 `BeautifulSoup` 來獲取和解析網頁內容。然後，我們可以使用 `pandas` 的 `read_html` 函數來將 HTML 表格轉換為 DataFrame。

以下是詳細的步驟：

1. 導入所需的模組。
2. 使用 `requests.get` 函數來獲取網頁內容。
3. 使用 `BeautifulSoup` 來解析網頁內容。
4. 使用 `soup.find_all('table')` 來找到所有的表格元素。
5. 使用 `pandas.read_html` 函數來將 HTML 表格轉換為 DataFrame。
6. 將兩個 DataFrame 儲存為變數。

以下是相應的 Python 程式碼：

