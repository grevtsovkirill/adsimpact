import pickle
import os
import xgboost
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

def load_model():
    try: 
        print("read pre-trained model")
        with open('model_xgb_def.pickle', 'rb') as f:
            model = pickle.load(f)
            return model
    except:
        print("model doesn't exist - please train it!")


def get_model(x,y,opt='train'):

    if opt == 'load' and os.path.exists('model_xgb_def.pickle'):
        model = load_model()        
    else:
        print("build model")
        model = build_model()
        print("train model")
        model.fit(x,y)
        with open('model_xgb_def.pickle', 'wb') as f:
            pickle.dump(model, f)
        
    return model

def build_model():
    param = {}
    param['objective'] = 'reg:squarederror'
    param['eta'] = 0.1
    param['max_depth'] = 4
    param['nthread'] = 4

    model = xgboost.XGBRegressor(**param)

    return model

def do_train(y,pred):
    heatmap, xedges, yedges = np.histogram2d(y, np.abs(pred-y), bins=50)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap.T,  extent=extent, origin='lower')
    plt.savefig("Plots/abs_diff.png", transparent=True)

def do_summary(X,Y,Y_pred,trX,trY,trY_pred):
    with open("summary.txt", "w") as f:
        f.write("Parameters test(train):\n")
        f.write("MAE = {} ({}) \n".format(mean_absolute_error(Y,Y_pred),mean_absolute_error(trY,trY_pred)))
        f.write("MSE = {} ({}) \n".format(mean_squared_error(Y,Y_pred),mean_squared_error(trY,trY_pred)))
        f.write("mean Ytest={} \n".format(Y.mean()))
        f.write("act MAE = {}, MSE = {}) \n".format(np.exp(mean_absolute_error(Y,Y_pred)), np.exp(mean_squared_error(Y,Y_pred))))
        f.write("act mean Ytest= {}\n".format(np.exp(Y.mean())) )

    print("MAE = {} ({}) ".format(mean_absolute_error(Y,Y_pred),mean_absolute_error(trY,trY_pred)))
    print("MSE = {} ({}) ".format(mean_squared_error(Y,Y_pred),mean_squared_error(trY,trY_pred)))
    print("mean Ytest= ",Y.mean())
    print("act MAE = {}, MSE = {}) ".format(np.exp(mean_absolute_error(Y,Y_pred)), np.exp(mean_squared_error(Y,Y_pred))))
    print("act mean Ytest= ",np.exp(Y.mean()))
