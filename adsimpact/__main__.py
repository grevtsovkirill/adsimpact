from adsimpact import dataprep
    
def main():

    '''
    Prepare data for training: 
    '''
    data = dataprep.ProductData()
    data.load_data()
    print(data.cleandata.head())

if __name__ == "__main__":
    main()
