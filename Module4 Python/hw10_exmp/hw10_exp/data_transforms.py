from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
import numpy as np
from hw10_exp.nlp_utils import pos_tokenization



class Hw5_1Transform(TransformerMixin):
  def fit(self, X, y=None):
    X = X.copy()                            
    self.vectorizer = TfidfVectorizer(min_df=20,
                                      stop_words='english')
    self.vectorizer.fit(X.overview)
    return self

  def transform(self, X, y=None):
    X = X.copy()                                 
    transformed_features = self.vectorizer.transform(X.overview)
    transformed_features = pd.DataFrame(transformed_features.toarray(),
                                        columns=self.vectorizer.get_feature_names(),
                                        index= X.index)
    X = X.drop('overview',axis=1)
    X = X.join(transformed_features, rsuffix='_feature')
    return X

  def fit_transform(self, X, y=None):
    X = X.copy()
    self.fit(X, y=None)
    X = self.transform(X, y=None)
    return X
  
  def predict(self, X, y=None):
    X = X.copy()
    X = self.transform(X, y=None)
    return X


class Hw5_2Transform(TransformerMixin):
  def fit(self, X, y=None):
    X = X.copy()                            
    self.vectorizer = TfidfVectorizer(min_df=10,
                                      stop_words='english')
    self.vectorizer.fit(X.overview)
    return self

  def transform(self, X, y=None):
    X = X.copy()                                 
    transformed_features = self.vectorizer.transform(X.overview)
    transformed_features = pd.DataFrame(transformed_features.toarray(),
                                        columns=self.vectorizer.get_feature_names(),
                                        index= X.index)
    X = X.join(transformed_features, rsuffix='_feature')
    X = X.drop('overview',axis=1)
    return X
    
  def fit_transform(self, X, y=None):
    X = X.copy()
    self.fit(X, y=None)
    X = self.transform(X, y=None)
    return X
  
  def predict(self, X, y=None):
    X = X.copy()
    X = self.transform(X, y=None)
    return X



class Hw5_3Transform(TransformerMixin):
  def fit(self, X, y=None):
    X = X.copy()
    self.vectorizer = TfidfVectorizer(min_df=10, 
                                      stop_words='english',
                                      ngram_range=(2,2))
    self.vectorizer.fit(X.overview)
    return self

  def transform(self, X, y=None):
    X = X.copy()
    transformed_features = self.vectorizer.transform(X.overview)
    transformed_features = pd.DataFrame(transformed_features.toarray(),
                                        columns=self.vectorizer.get_feature_names(),
                                        index= X.index)
    X = X.join(transformed_features, rsuffix='_feature')
    X = X.drop('overview',axis=1)
    return X
    
  def fit_transform(self, X, y=None):
    X = X.copy()
    self.fit(X, y=None)
    X = self.transform(X, y=None)
    return X
  
  def predict(self, X, y=None):
    X = X.copy()
    X = self.transform(X, y=None)
    return X

class Hw5_4Transform(TransformerMixin):
  def fit(self, X, y=None):
    X = X.copy()                            
    self.vectorizer = TfidfVectorizer(min_df=10,
                                      stop_words='english',
                                      analyzer='char',
                                      ngram_range=(2,2))
    self.vectorizer.fit(X.overview)
    return self

  def transform(self, X, y=None):
    X = X.copy()                                 
    transformed_features = self.vectorizer.transform(X.overview)
    transformed_features = pd.DataFrame(transformed_features.toarray(),
                                        columns=self.vectorizer.get_feature_names(),
                                        index= X.index)
    X = X.join(transformed_features, rsuffix='_feature')
    X = X.drop('overview',axis=1)
    return X

  def fit_transform(self, X, y=None):
    X = X.copy()
    self.fit(X, y=None)
    X = self.transform(X, y=None)
    return X
  
  def predict(self, X, y=None):
    X = X.copy()
    X = self.transform(X, y=None)
    return X

class PCA_transform(BaseEstimator, TransformerMixin):
  def __init__(self, condition, transformer):
    self.condition = condition
    self.transformer = transformer

  def fit(self, X, y=None):
    if self.condition:
      self.transformer.fit(X, y)
    return self

  def transform(self, X, y=None):
    if self.condition:
      X = self.transformer.transform(X)
    return X
  
