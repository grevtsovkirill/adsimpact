from adsimpact import dataprep
    
def main():

    '''
    Prepare data for training: 
    '''
    data = dataprep.ProductData()
    data.data_prep()
    print(data.prepdata.head())

if __name__ == "__main__":
    main()
