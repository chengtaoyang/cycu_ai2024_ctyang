import re, io
import tarfile
import requests
import datetime
import pandas as pd
import time

class M05A_online_list:
    def __init__(self) :
        #read url and get the html content
        self.url = '''https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/'''

        self.csv_cols = ['TimeInterval','GantryFrom','GantryTo','VehicleType','SpaceMeanSpeed','TrafficVolume']

        response = requests.get(self.url)
        html_content = response.text

        self.targz_list = []
        self.csv_list   = []
    
        #download all href links from the html content like this:
        #'''<a href="20240731/">'''
        #its regular expression pattern is '''<a href="(20\d{6}/)">'''
        self.csv_list = re.findall('''<a href="(20\\d{6})/">''', html_content)

        #obtain all href links from the html content like this:
        #'''<a href="M05A_20151104.tar.gz">'''
        #its regular expression pattern is '''<a href="M05A_(20\\d{6})\\.tar\\.gz">'''
        self.targz_list = re.findall(r'<a href="M05A_(20\d{6})\.tar\.gz">', html_content)

        self.csv_today = datetime.date.today().strftime("%Y%m%d")

        #remove the today's date from the  csv_list
        self.csv_list = [x for x in self.csv_list if x != self.csv_today]
 


    @staticmethod
    def download_url_to_file(url, filename):
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)

    def download(self, file_date = datetime.date(2024,5,10)):
        file_str = file_date.strftime("%Y%m%d")
        target_df = pd.DataFrame(columns=self.csv_cols)
        #check if the file is in the targz_list
        if file_str in self.targz_list:
            file_name = f"M05A_{file_str}.tar.gz"
            file_url  = self.url + file_name
            #download tar file
            M05A_online_list.download_url_to_file(file_url, file_name)
            #extract tar file to tempary folder
            with tarfile.open(file_name, 'r:gz') as tar:
                tar.extractall()
            #read all csv files in the tempary folder
            for hour in range(24):
                for minute in range(0, 60, 5):
                    elem_name               = f"TDCS_M05A_{file_str}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                    elem_path               = f"M05A/{file_str}/{str(hour).zfill(2)}/{elem_name}"
                    df                      = pd.read_csv(elem_path, header=None)
                    df.columns              = self.csv_cols
                    df['TimeInterval']      = pd.to_datetime(df['TimeInterval'])
                    target_df = pd.concat([target_df, df], ignore_index=True)
                    #for debug, print (target_df.shape)

        #check if the file is in the csv_list
        elif file_str in self.csv_list:
            for hour in range(24):
                for minute in range(0, 60, 5):
                    file_name = f"TDCS_M05A_{file_str}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                    file_url  = f"{self.url}{file_str}/{str(hour).zfill(2)}/{file_name}"
                    #download csv file
                    csv_content = requests.get(file_url)
                    df = pd.read_csv(io.StringIO(csv_content.text), header=None)
                    df.columns = self.csv_cols
                    #df['date'] = pd.to_datetime(df['date_string'])
                    df['TimeInterval'] = pd.to_datetime(df['TimeInterval'])
                    
                    target_df = pd.concat([target_df, df], ignore_index=True)
                    #for debug, print (target_df.shape)
        #if the file is not available
        else:
            print(f"file {file_str} is not available")

        output_filename = f'M05A_{file_str}.nsg.pkl.gz'

        #write to gzip pickle file
        target_df.to_pickle(output_filename, compression='gzip')

        #read output_filename to check if the file is downloaded successfully
        df = pd.read_pickle(output_filename, compression='gzip')
        print('check', file_str,df.head(), df.shape)

    def data_day_range(self):
        beg =datetime.datetime.strptime(self.targz_list[-1], "%Y%m%d")    
        end =datetime.datetime.strptime(self.csv_list[0], "%Y%m%d")
        print(beg, end)
        return beg, end
    
if __name__ == '__main__':
    datalist = M05A_online_list()
    beg, end = datalist.data_day_range()

    days = (end - beg).days + 1

    for thisday in range(days - 1, -1, -1):  
        time.sleep(0.05)

        current_day = beg + datetime.timedelta(days=thisday)
        datalist.download(current_day)
        print(thisday, current_day)
    