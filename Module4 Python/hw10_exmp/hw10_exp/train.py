import yaml
import os
from hw10_exp.settings import ROOT_DIR, BASE_PARAMS_DIR, EXPERIMENT_DIR, PATH, DATA_PATH, PARAMS_DIR
from hw10_exp.custom_pipeline import split_data, make_pipeline
from hw10_exp.my_utils import get_data

from sklearn.metrics import classification_report, precision_score, recall_score, accuracy_score, adjusted_mutual_info_score, roc_auc_score, log_loss
import pandas as pd
import numpy as np
import joblib

def train_clf():
    with open(BASE_PARAMS_DIR,'r') as fd:
      cfg = yaml.safe_load(fd)



    TRAIN_PATH = DATA_PATH +'/train_data.csv'
    VAL_PATH = DATA_PATH +'/val_data.csv'
    
    if not ((os.path.exists(TRAIN_PATH) and (os.path.exists(VAL_PATH)))):
      split_data(get_data())
    

    train_data = pd.read_csv(TRAIN_PATH).dropna(axis='rows')   
    val_data = pd.read_csv(VAL_PATH).dropna(axis='rows')

    X_train, y_train = train_data.drop(['id','target'],axis=1), train_data.target   
    X_val, y_val = val_data.drop(['id','target'],axis=1), val_data.target
    
    pipe, params = make_pipeline()
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_val)
    preds_proba = pipe.predict_proba(X_val)

    metrics_dict = {
    'precision_score': float(precision_score(y_pred=preds, y_true=y_val)),
    'recall_score': float(recall_score(y_pred=preds, y_true=y_val)),
    'accuracy_score': float(accuracy_score(y_pred=preds, y_true=y_val)),
    'adjusted_mutual_info_score': float(adjusted_mutual_info_score(y_val, preds)),
    'roc_auc_score': float(roc_auc_score(y_val, preds_proba[:,1])),
    'log_loss': float(log_loss(y_val, preds_proba[:,1])),
    }


    with open(DATA_PATH + '/report.yaml', 'w') as f:
      yaml.dump(metrics_dict, f, default_flow_style=False)

    joblib.dump(pipe, DATA_PATH + '/model.pkl')


    with open(PARAMS_DIR, 'w') as f:
      documents = yaml.dump(cfg, f)




