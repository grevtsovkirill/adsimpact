import pickle
import os
import xgboost

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
