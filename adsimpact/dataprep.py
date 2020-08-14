import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

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

    def cat_encode(self,varlist = ['Product', 'Channel']):
        df = self.cleandata
        
        for var in varlist:
            df = pd.concat([df,pd.get_dummies(df[var], prefix=var)],axis=1)

        df = df.drop(columns=varlist)
        df = df.drop(columns=['WeekStart'])
        #df = df.drop(columns=['Price'])
        df.StoresAvailability = df.StoresAvailability/100
        for v in ['QuantitySold','TV','Online']:
            if v in df.columns:
                df[v] = np.log1p(df[v])
            else:
                print("{} is not in dataset".format(v))
        self.prepdata = df

    def data_prep(self):
        self.load_data()
        self.cat_encode()
        Y = self.prepdata.pop('QuantitySold')
        self.Y = Y
        X = self.prepdata
        self.X = X

    def data_train(self):
        self.data_prep()
        x_train, x_test, y_train, y_test = train_test_split(self.X, self.Y, test_size = 0.3, random_state = 123)
        self.prod_fracs(self.X,x_train, x_test)
        self.x_test = x_test
        self.y_test = y_test
        self.x_train = x_train
        self.y_train = y_train

    def prod_fracs(self,x, x_test,x_train):
        df = x.filter(like='Product_', axis=1).sum().to_frame(name="tot")
        df=df/len(x)
        df['test'] = x_test.filter(like='Product_', axis=1).sum()/len(x_test)
        df['train'] = x_train.filter(like='Product_', axis=1).sum()/len(x_train)
        df.plot.barh().invert_yaxis()

        if not os.path.exists('Plots'):
            os.makedirs('Plots')
        plt.savefig("Plots/split.png", transparent=True)
