import pandas as pd
import os


class ProductData:
    def __init__(self, data_dir = './', filename1 = 'partA.csv', filename2 = 'partB.csv'):
        self.data_dir=data_dir
        self.filename1=filename1
        self.filename2=filename2

    def df_clean(self,df):
        df = df.fillna(0)
        df = df.drop_duplicates()
        return df
    
    def load_data(self):
        data1 = pd.read_csv(self.data_dir+self.filename1)
        data2 = pd.read_csv(self.data_dir+self.filename2)
        data1 = self.df_clean(data1)
        data2 = self.df_clean(data2)
        result = pd.merge(data1, data2, on=['Product', 'Channel','WeekStart'])
        result = result.sort_values(by=['WeekStart'])
        self.cleandata = result

