
import pandas as pd
import os
import yaml
from hw10_exp.settings import BASE_PARAMS_DIR
from hw10_exp.nlp_utils import pos_tokenization
from hw10_exp.nlp_utils import lemmatize_df

def get_data(BASE_PARAMS_DIR=BASE_PARAMS_DIR):


    with open(BASE_PARAMS_DIR,'r') as fd:
      cfg = yaml.safe_load(fd)

    drop_cols = ['homepage',
                  'imdb_id',
                  'belongs_to_collection',
                  'original_title', 
                  'spoken_languages', 
                  'tagline', 
                  'title',
                  'poster_path',           
                  'production_companies',  #we might want to use this    
                  'production_countries',  #we might want to use this
                  'genres',                #we might want to extract data from these jsons
                  'release_date',]         #we might wanna keep this, to further create more features based on that
      
    cat_cols = ['original_language',
                  'status']

    included_features = cfg.get('data')['included_features']

    main_data = pd.read_csv(cfg.get('data')['main_data_path'])
    main_data["id"] = pd.to_numeric(main_data["id"], errors="coerce", downcast="integer")
    main_data = main_data.drop_duplicates(subset=['id'])
    main_data["budget"] = pd.to_numeric(main_data["budget"], errors="coerce")
    main_data["popularity"] = pd.to_numeric(main_data["popularity"], errors = "coerce")
    main_data['overview'] = main_data['overview'].astype(str)

    main_data = main_data[~main_data['video'].isna()]
    main_data['video'] = main_data['video'].astype(int)
    main_data = main_data[main_data['adult'].isin(['True','False'])]
    main_data['adult'] = main_data['adult'].map({'True':1,
                                                  'False':0})
    main_data['years'] = pd.DatetimeIndex(pd.to_datetime(main_data["release_date"], errors="coerce")).year                                               
    main_data['years'] = max(main_data['years']) - main_data['years']      #we might wanna consider taking monthes too, 
                                                                            #and adding 'time of year' feature indicating Summer/Winter and etc...
      
    main_data = main_data[~main_data.status.isna()]
      
    main_data = main_data[~main_data['release_date'].isna()]
    main_data = main_data[~main_data['years'].isna()]
    main_data = main_data.drop(drop_cols, axis=1)
    main_data.set_index('id', inplace=True)

      #getting median of votes
    median_vote = main_data.vote_average.median()

      #creating 'target' column
    main_data['target'] = (main_data['vote_average']>median_vote).astype(int)
    main_data = main_data.drop('vote_average', axis=1)
      
    if cfg.get('data')['use_categorical'] == 1:
      categorical_data = pd.get_dummies(main_data[cat_cols], drop_first=True)
      main_data = pd.concat([main_data, categorical_data], axis=1)
      
    if cfg.get('data')['joined_data_name'] == 'credits':
      joined_data = pd.read_csv(cfg.get('data')['additional_data']['credits'])
      joined_data.drop_duplicates(subset="id", inplace = True)
      main_data = main_data.merge(joined_data, how="left", left_on = "id", right_on = "id").copy()
      
    if cfg.get('data')['joined_data_name'] == 'ratings':
      joined_data = pd.read_csv(cfg.get('data')['additional_data']['ratings'])
      joined_data.drop(['userId','timestamp'], axis=1, inplace=True)
      joined_data = joined_data.groupby('movieId').mean()
      main_data = main_data.join(joined_data, how='left')

    if cfg.get('data')['joined_data_name'] == 'ratings_small':
      joined_data = pd.read_csv(cfg.get('data')['additional_data']['ratings_small'])
      joined_data = pd.read_csv(cfg.get('data')['additional_data']['ratings'])
      joined_data.drop(['userId','timestamp'], axis=1, inplace=True)
      joined_data = joined_data.groupby('movieId').mean()
      main_data = main_data.join(joined_data, how='left')
      
    if cfg.get('data')['joined_data_name'] == 'None':
      pass
        
    if (cfg.get('experiment')['preprocessing_type'] == 2):
      main_data = pos_tokenization(data=main_data, POS='NN')
      
    if (cfg.get('experiment')['preprocessing_type'] == 3):
      main_data = pos_tokenization(data=main_data, POS='NNP')
      
      
    main_data = main_data.drop(cat_cols, axis=1)
    main_data = lemmatize_df(main_data)
    main_data['overview'] = main_data['overview'].apply(lambda x: ' '.join(x))
    main_data = main_data.dropna(axis='rows')                                   # better idea:  impute/ffil na's
    main_data = main_data[included_features]                                   
    return main_data
