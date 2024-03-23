import os
import yaml


ROOT_DIR = os.path.join(os.getcwd(), 'hw10_exp') 
BASE_PARAMS_DIR = os.path.join(ROOT_DIR, 'params.yaml') 

with open(BASE_PARAMS_DIR,'r') as fd:
    cfg = yaml.safe_load(fd)

EXPERIMENT_DIR = os.path.join(ROOT_DIR, 'data')
request_number = 1
PATH = os.path.join(EXPERIMENT_DIR, f'exp{request_number}')

while os.path.exists(PATH):
    request_number +=1
    PATH = os.path.join(EXPERIMENT_DIR, f'exp{request_number}')

DATA_PATH = PATH
PARAMS_DIR = os.path.join(DATA_PATH, 'experiment_params.yaml')

print(ROOT_DIR)
print(BASE_PARAMS_DIR)
