import pandas as pd
import json
import pickle
import unicodedata

from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn import base
from sklearn.feature_extraction.text import TfidfVectorizer
from custom_transformers import NumberDestroyer

feature_coef_file = 'weights.json'
regressor_file = 'regressor.pickle'
no_style_regressor_file = 'no_style_regressor.pickle'



tfidf_bigram_vectorizer = TfidfVectorizer(
        strip_accents='unicode',
        decode_error='ignore',
        stop_words = 'english',
        ngram_range=(1,2),
        max_df = .85,
        min_df = 5)


text_bigram_pipe = Pipeline([
    ('number_destroyer',NumberDestroyer()),
    ('vectorizer',tfidf_bigram_vectorizer)])


column_bigram_transformer = ColumnTransformer([
    ('text_encoder',text_bigram_pipe,'text'),
    ('style_encoder',OneHotEncoder(handle_unknown='ignore'),['style']),
    ('abv_scaler',StandardScaler(),['abv',])
    ])

no_style_column_transformer = ColumnTransformer([
    ('text_encoder',text_bigram_pipe,'text'),
    ('abv_scaler',StandardScaler(),['abv',])
    ])

bigram_regressor = Pipeline([
    ('preprocessing',column_bigram_transformer),
    #('estimator',SGDRegressor(alpha=.0002, max_iter=30000))
    ('estimator',Ridge(alpha=3))
    ])


#would be better if color map were not hard-coded here and below but rather a global variable


def strength_dic(feature_coef_file=feature_coef_file):
    with open(feature_coef_file,'r') as f:
        feature_coef_dic = json.load(f)
    return feature_coef_dic


def best_predictor(text, abv=5.5, style='Pale Ale - American / APA'):
    if style == 'not specified':
        with open(no_style_regressor_file,'rb') as f:
            fitted_no_style_regressor = pickle.load(f)
        return fitted_no_style_regressor.predict(pd.DataFrame([{'style': style, 'abv': abv,'text': text},]))
    with open(regressor_file,'rb') as f:
        fitted_regressor = pickle.load(f)
    return fitted_regressor.predict(pd.DataFrame([{'style': style, 'abv': abv,'text': text },]))



def get_strongest_and_weakest(regressor_file=regressor_file, cutoffs=(-16.25,23)):
    with open(regressor_file,'rb') as f:
        regressor = pickle.load(f)
    features = regressor.named_steps['preprocessing'].transformers_[0][1].named_steps['vectorizer'].get_feature_names()
    coefs = regressor.named_steps['estimator'].coef_
    weight_dic = {features[i]:coefs[i] for i in range(len(features))}
    return sorted([(entry,weight_dic[entry]) for entry in weight_dic \
        if not (cutoffs[0]< weight_dic[entry]< cutoffs[1])], key = lambda x : x[1])



