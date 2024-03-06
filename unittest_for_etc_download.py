import unittest
import os
import datetime
import requests
import tarfile
from pandas.tseries.offsets import MonthEnd
from unittest.mock import patch, MagicMock
from etc_download import check_files, download_and_extract_files  

class TestDownloadScript(unittest.TestCase):

    def setUp(self):
        # 設定下載目錄為當前用戶的"Downloads"文件夾
        self.download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        # 設定測試的月份範圍
        self.month_beg = datetime.datetime(2016, 10, 1, 0, 0, 0)
        self.month_end = datetime.datetime(2016, 12, 31, 0, 0, 0)
        # 設定測試的日期範圍
        self.day_beg = self.month_beg
        self.day_end = self.month_beg + MonthEnd()

    @patch('requests.get')
    def test_check_files(self, mock_get):
        # 創建模擬的回應
        mock_response = MagicMock()
        mock_response.status_code = 200  # 模擬回應的狀態碼為200
        mock_get.return_value = mock_response  # 將模擬的回應設定為get請求的返回值

        # 測試check_files函數
        problem_files = check_files(self.day_beg, self.day_end)
        # 驗證返回的問題文件列表是否為空
        self.assertEqual(problem_files, [])

        # 修改模擬回應的狀態碼為404
        mock_response.status_code = 404
        # 再次測試check_files函數
        problem_files = check_files(self.day_beg, self.day_end)
        # 驗證返回的問題文件列表是否不為空
        self.assertNotEqual(problem_files, [])
        print(problem_files)

if __name__ == '__main__':
    unittest.main()