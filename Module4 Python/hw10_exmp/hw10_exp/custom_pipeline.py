import os
import yaml

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

from hw10_exp.my_utils import get_data
from hw10_exp.settings import ROOT_DIR, BASE_PARAMS_DIR, EXPERIMENT_DIR, PATH, DATA_PATH, PARAMS_DIR
from hw10_exp.data_transforms import Hw5_1Transform, Hw5_2Transform, Hw5_3Transform, Hw5_4Transform, PCA_transform

def make_pipeline(BASE_PARAMS_DIR=BASE_PARAMS_DIR, pipe_type=None, pca=None, n_components=None, ):

  with open(BASE_PARAMS_DIR,'r') as fd:
    cfg = yaml.safe_load(fd)

  pca = cfg.get('experiment')['pca']
  n_components = cfg.get('experiment')['n_components']
  pipe_type = cfg.get('experiment')['preprocessing_type']
  random_state =  cfg.get('experiment')['random_state']
  isOverview = 'overview' in cfg.get('data')['included_features']
  
  clf_type = cfg.get('experiment')['classifier']
  

  if clf_type == 'LogisticRegression':
    params = cfg.get('params_logreg')
    clf = LogisticRegression(**params,random_state=random_state)
    
  if clf_type == 'DecisionTree':
    params = cfg.get('params_dectree')
    clf = DecisionTreeClassifier(**params, random_state=random_state)
  
  if clf_type =='RandomForest':
    params = cfg.get('params_randomforest')
    clf = RandomForestClassifier(**params, random_state=random_state)

  else:
    clf = LogisticRegression(random_state=random_state)

  if not isOverview:
    pipe = Pipeline([
    ('standard-scaler', StandardScaler()),
    ('PCA', PCA_transform(condition=pca, transformer=PCA(n_components=n_components))),
    ('clf', clf),
    ])

  if (pipe_type == 1) and (isOverview):
    pipe = Pipeline([
    ('data-transforms', Hw5_1Transform()),
    ('standard-scaler', StandardScaler()),
    ('PCA', PCA_transform(condition=pca, transformer=PCA(n_components=n_components))),
    ('clf', clf),
    ])    
  if (pipe_type == 2) and (isOverview):
    pipe = Pipeline([
    ('data-transforms', Hw5_2Transform()),
    ('standard-scaler', StandardScaler()),
    ('PCA', PCA_transform(condition=pca, transformer=PCA(n_components=n_components))),
    ('clf', clf),
    ])

  if (pipe_type == 3) and (isOverview):
    pipe = Pipeline([
    ('data-transforms', Hw5_3Transform()),
    ('standard-scaler', StandardScaler()),
    ('PCA', PCA_transform(condition=pca, transformer=PCA(n_components=n_components))),
    ('clf', clf),
    ])

  if (pipe_type == 4) and (isOverview):  
    pipe = Pipeline([
    ('data-transforms', Hw5_4Transform()),
    ('standard-scaler', StandardScaler()),
    ('PCA', PCA_transform(condition=pca, transformer=PCA(n_components=n_components))),
    ('clf', clf),
    ])    
  return pipe, params

def split_data(data,
               BASE_PARAMS_DIR=BASE_PARAMS_DIR,
               EXPERIMENT_DIR=EXPERIMENT_DIR,
               PATH=PATH,
               DATA_PATH=DATA_PATH,
               PARAMS_DIR=PARAMS_DIR,):
    
    with open(BASE_PARAMS_DIR,'r') as fd:
      cfg = yaml.safe_load(fd)
    

  
    data = data.copy()
  
    train_data, val_data = train_test_split(data, 
                                             test_size=cfg.get('experiment')['test_size'],
                                             random_state=cfg.get('experiment')['random_state'],
                                             stratify=data.target if cfg.get('experiment')['stratify'] else None
                                             )
   

    try:
      os.makedirs(DATA_PATH, exist_ok=True)
    except FileExistsError:
      pass

    train_data.to_csv(DATA_PATH + '/train_data.csv',)
    val_data.to_csv(DATA_PATH+'/val_data.csv',)



    



    


