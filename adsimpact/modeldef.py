import pickle
import os
import xgboost
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path


def load_model():
    try: 
        print("read pre-trained model")
        with open('model_xgb_def.pickle', 'rb') as f:
            model = pickle.load(f)
            return model
    except:
        print("model doesn't exist - please train it!")


def get_model(x,y,opt='baseline'):

    if opt == 'load' and os.path.exists('model_xgb_def.pickle'):
        model = load_model()        
    elif opt == 'optimize':
        print("Optimize model parameters")
        clf = xgboost.XGBRegressor('reg:squarederror')
        best_pars = GridSearchCV(clf, {
                                       "learning_rate":[0.001,0.01,0.1],
                                       "min_child_weight":[0.5,0.7,1.0,1.2,1.5],
                                       'max_depth': [3,6,10,15],
                                       'reg_lambda': [0.5,1,1.5,2],
                                       'reg_alpha': [0.5,1,1.5,2],
                                       'n_estimators': [500,1000,2000,5000,10000]},
                                 #},
                                 verbose=2)
        best_pars.fit(x,y)        
        model = xgboost.XGBRegressor(**best_pars.best_params_)
        print("train model")
        model.fit(x,y)
        print("model with best params")
        print(model.get_xgb_params())

        with open('model_xgb_def.pickle', 'wb') as f:
            pickle.dump(model, f)
    else:
        print("build baseline model")
        model = build_model()
        print("train baseline model")
        model.fit(x,y)
        print(model.get_xgb_params())
        with open('model_xgb_def.pickle', 'wb') as f:
            pickle.dump(model, f)        

    return model

def build_model():
    param = {}
    param['objective'] = 'reg:squarederror'
    param['learning_rate'] = 0.01
    param['max_depth'] = 10
    param['min_child_weight'] = 1.
    param['reg_lambda'] = 2
    param['reg_alpha'] = 2
    param['n_estimators'] = 10000
    
    model = xgboost.XGBRegressor(**param)

    return model


def do_perf_map(y,pred):
    Path("Plots").mkdir(parents=True, exist_ok=True)
    plt.figure("pred")
    fig = plt.figure(figsize=(20, 8))
    hx = y
    hy = np.abs((pred-y)/y*100)
    plt.hist2d(hx, hy, bins=(130, 12000), cmap=plt.cm.jet)
    plt.colorbar()
    plt.ylabel("Absolute error: abs[true-predict]/true, %")
    plt.xlabel("QuantitySold")
    plt.ylim(0, 40) 
    plt.savefig("Plots/abs_diff.png", transparent=True)

    
def mean_absolute_percentage_error_plot(y_true, y_pred,try_true, try_pred): 

    Path("Plots").mkdir(parents=True, exist_ok=True)
    plt.figure("mape") 
    ape = np.abs((y_true - y_pred) / y_true)*100
    apetr = np.abs((try_true - try_pred) / try_true)*100
    sns.distplot(ape,kde=False, bins=7000,label="Test") # kde=False,
    sns.distplot(apetr, kde=False, bins=2000, label="Train")
    plt.xlim(0, 80)
    plt.legend(prop={'size': 12})
    plt.xlabel("Absolute error: abs[true-predict]/true, %")
    plt.savefig("Plots/mape.png", transparent=True)

def mean_absolute_percentage_error(y_true, y_pred): 
    ape = np.abs((y_true - y_pred) / y_true)
    mape = np.sum(ape)/len(y_true) * 100
    return mape

def do_summary(Y,Y_pred,trY,trY_pred):
    with open("summary.txt", "w") as f:
        f.write("Parameters test(train):\n")
        f.write("MAE = {} ({}) \n".format(mean_absolute_error(Y,Y_pred),mean_absolute_error(trY,trY_pred)))
        f.write("MAPE = {} ({}) \n".format(mean_absolute_percentage_error(Y,Y_pred),mean_absolute_percentage_error(trY,trY_pred)))
        f.write("MSE = {} ({}) \n".format(mean_squared_error(Y,Y_pred),mean_squared_error(trY,trY_pred)))
        f.write("RMSE = {} ({}) \n".format(np.sqrt(mean_squared_error(Y,Y_pred)),np.sqrt(mean_squared_error(trY,trY_pred)) ))
        f.write("mean Ytest={} \n".format(Y.mean()))

    mean_absolute_percentage_error_plot(Y,Y_pred,trY,trY_pred)
    print("MAE = {} ({}) ".format(mean_absolute_error(Y,Y_pred),mean_absolute_error(trY,trY_pred)))
    print("MAPE = {} ({}) \n".format(mean_absolute_percentage_error(Y,Y_pred),mean_absolute_percentage_error(trY,trY_pred)))
    print("MSE = {} ({}) ".format(mean_squared_error(Y,Y_pred),mean_squared_error(trY,trY_pred)))
    print("RMSE = {} ({}) \n".format(np.sqrt(mean_squared_error(Y,Y_pred)),np.sqrt(mean_squared_error(trY,trY_pred)) ))
    print("mean Ytest= ",Y.mean())
