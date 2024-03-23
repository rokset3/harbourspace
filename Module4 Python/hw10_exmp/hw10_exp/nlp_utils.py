import os
import yaml
import nltk
import pandas as pd

from collections.abc import Iterable

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import nltk

from sklearn.feature_extraction import text as sk_text
from bs4 import BeautifulSoup
import unicodedata
import re


def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item


def remove_stopwords(text):   
    t = [token for token in text if token.lower() not in stopwords.words("english")]
    text = ' '.join(t)    
    return text 

def remove_punctuation(text):
    return re.sub(r'[^a-zA-Z0-9]', ' ', text)

def word_count(text):
    return len(text.split())

def remove_irr_char(text):
    return re.sub(r'[^a-zA-Z]', ' ', text)    

def remove_extra_whitespaces(text):
    return re.sub(r'^\s*|\s\s*', ' ', text).strip()

def remove_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_url_func(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

def remove_html_tags_func(text):
    return BeautifulSoup(text, 'html.parser').get_text()

def preprocess(text):
    text = text.lower()
    text = remove_punctuation(text)
    text = remove_irr_char(text)
    text = remove_extra_whitespaces(text)
    text = remove_accented_chars(text)
    text = remove_url_func(text)
    text = remove_html_tags_func(text)
    text = remove_stopwords(text)
    return text

def simple_tokenizator(text):
    text = text.lower()
    text = word_tokenize(text)
    return(text)

def pos_tokenization(data, POS):
    print(f'Collecting n-grams for {POS} tokes')
    data = data.copy()
    data['overview'] = data['overview'].map(sent_tokenize)
    data['overview'] = data['overview'].apply(lambda x: [word_tokenize(sentence) for sentence in x])
    data['overview'] = data['overview'].apply(lambda tokens_sentences: [pos_tag(tokens) for tokens in tokens_sentences])
    data['overview'] = data['overview'].apply(
      lambda x: [
                [
                    word_POS[0] for word_POS in sentence if (word_POS[1] == POS)
                ] 
                for sentence in x
          ]
      )
    data['overview'] = data['overview'].apply(lambda x: ' '.join(list(flatten(x))))
    data['overview'] = data['overview'].str.lower()
    return data

def lemmatize_text(text):
    
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    
    return [lemmatizer.lemmatize(w.lower()) for w in w_tokenizer.tokenize(text)]

def lemmatize_df(data):
    data = data.copy()
    data['overview'] = data.overview.apply(lemmatize_text)

    return data

 
