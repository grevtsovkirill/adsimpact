from adsimpact import dataprep,modeldef

import numpy as np

def main():

    '''
    Prepare data for training: 
    '''
    data = dataprep.ProductData()
    data.data_train()
    
    model = modeldef.get_model(data.x_train,data.y_train,'baseline') #

    y_pred = np.expm1(model.predict(data.x_test))
    try_pred = np.expm1(model.predict(data.x_train))

    modeldef.do_perf_map(np.expm1(data.y_test),y_pred)
    modeldef.do_summary(np.expm1(data.y_test),y_pred,np.expm1(data.y_train),try_pred)

if __name__ == "__main__":
    main()
