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

    def cat_encode(self,varlist = ['Product', 'Channel','isPromoPeriod']):
        df = self.cleandata
        for var in varlist:
            df = pd.concat([df,pd.get_dummies(df[var], prefix=var)],axis=1)

        df = df.drop(columns=varlist)
        df = df.drop(columns=['WeekStart'])
        self.prepdata = df

    def data_prep(self):
        self.load_data()
        self.cat_encode()
        Y = self.prepdata.pop('QuantitySold')
        self.Y = Y
        X = self.prepdata
        self.X = X
