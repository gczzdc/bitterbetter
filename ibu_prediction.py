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
ensemble_regressor_file = 'full_ensemble_regressor_final.pickle'


def strength_dic(feature_coef_file=feature_coef_file):
    with open(feature_coef_file,'r') as f:
        feature_coef_dic = json.load(f)
    return feature_coef_dic


def best_predictor(text, abv=5.5, style='Pale Ale - American / APA'):
    if style == 'not specified':
        filename = no_style_regressor_file
    else:
        filename = ensemble_regressor_file
    fitted_regressor = get_regressor(filename)
    return fitted_regressor.predict(pd.DataFrame([{'style': style, 'abv': abv,'text': text },]))

def get_regressor(filename):
    with open(filename,'rb') as f:
        regressor = pickle.load(f)
    return regressor


def get_strongest_and_weakest(regressor_file=regressor_file, cutoffs=(-16.25,23)):
    regressor=get_regressor(regressor_file)
    features = regressor.named_steps['preprocessing'].transformers_[0][1].named_steps['vectorizer'].get_feature_names()
    coefs = regressor.named_steps['estimator'].coef_
    weight_dic = {features[i]:coefs[i] for i in range(len(features))}
    return sorted([(entry,weight_dic[entry]) for entry in weight_dic \
        if not (cutoffs[0]< weight_dic[entry]< cutoffs[1])], key = lambda x : x[1])



