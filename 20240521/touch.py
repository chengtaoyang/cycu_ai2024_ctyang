import re, io
import requests
import datetime
import pandas as pd

class M05A_online_list:
    def __init__(self) :
        #read url and get the html content
        self.url = '''https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/'''

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
 

        self.csv_cols = ['TimeInterval','GantryFrom','GantryTo','VehicleType','SpaceMeanSpeed','TrafficVolume']
    @staticmethod
    def download_url_to_file(url, filename):
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)

    def download(self, file_date = datetime.date(2024,5,10)):
        
        file_str = file_date.strftime("%Y%m%d")
        if file_str in self.targz_list:
            file_name = f"M05A_{file_str}.tar.gz"

            file_url  = self.url + file_name

            #download tar file
            M05A_online_list.download_url_to_file(file_url, file_name)

        elif file_str in self.csv_list:
            target_df = pd.DataFrame(columns=self.csv_cols)
            for hour in range(24):
                for minute in range(0, 60, 5):
                    file_name = f"TDCS_M05A_{file_str}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                    file_url  = f"{self.url}{file_str}/{str(hour).zfill(2)}/{file_name}"
                    
                    r = requests.get(file_url)

                    # convert r to dataframe without column names in the first row
                    # specify header=None to avoid the first row being treated as column names
                    # columns' name set to self.csv_cols
                    # self.csv_cols = ['TimeInterval','GantryFrom','GantryTo','VehicleType','SpaceMeanSpeed','TrafficVolume']

                    df = pd.read_csv(io.StringIO(r.text), header=None)
                    df.columns = self.csv_cols
                    #df['date'] = pd.to_datetime(df['date_string'])
                    df['TimeInterval'] = pd.to_datetime(df['TimeInterval'])
                    
                    target_df = pd.concat([target_df, df], ignore_index=True)
                    print (target_df.shape)

            output_filename = f'M05A_{file_str}.pkl'
            #write to matlab file
            target_df.to_pickle(output_filename)

call = M05A_online_list()
call.download( datetime.date(2024,7,30) )
