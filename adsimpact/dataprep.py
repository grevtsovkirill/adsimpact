import pandas as pd
import os


class ProductData:
    def __init__(self, data_dir = './', filename1 = 'partA.csv', filename2 = 'partB.csv'):
        self.data_dir=data_dir
        self.filename1=filename1
        self.filename2=filename2

