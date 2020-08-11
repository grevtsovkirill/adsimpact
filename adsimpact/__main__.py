from adsimpact import dataprep,modeldef
    
def main():

    '''
    Prepare data for training: 
    '''
    data = dataprep.ProductData()
    data.data_train()
    model = modeldef.get_model(data.x_train,data.y_train,'load')

    y_pred = model.predict(data.x_test)
    try_pred = model.predict(data.x_train)

    modeldef.do_train(data.y_test,y_pred)
    modeldef.do_summary(data.x_test,data.y_test,y_pred,data.x_train,data.y_train,try_pred)
if __name__ == "__main__":
    main()
