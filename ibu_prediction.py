import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import colors
import seaborn as sns
import json
import pickle
import copy
import string
import unicodedata



import io
from graphic_tools import build_colors_plt


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



#probably better to redo this from the fitted regressor

# class NumberDestroyer(base.BaseEstimator, base.TransformerMixin):
#     def __init__(self):
#         pass
   
#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         d= {str(a):'' for a in range(10)}
#         X_copy = copy.copy(X)
#         for k in d:
#             X_copy = X_copy.str.replace(k,d[k])
#         return (X_copy)


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


def clean(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] not in ("C","P"))


def bag_of_words_paragraph(text,feature_coef_file=feature_coef_file):
    with open(feature_coef_file,'r') as f:
        feature_coef_dic = json.load(f)
    '''
    renders an html paragraph given a textual description

    the input text here has not been verified and needs to be cleaned.
    '''
    clean_text = clean(text)
    working_dic = build_colors_plt(clean_text,feature_coef_dic)
    words = clean_text.split()
    para = []
    style = []
    counter = 1
    for word in words:
        if word not in working_dic:
            para.append(word)
            para.append(' ')
        else:
            para.append('<span ')
            
            para.append('onmouseover="changeContent(\'desc')
            para.append(str(counter))
            para.append('\')"')

            para.append('onmouseout="resetContent()"')

            para.append('class="tooltip"')

            para.append('style="background: ')
            para.append(working_dic[word]['hex_color'])
            para.append('"')

            para.append('>')

            para.append(word)

            coef = working_dic[word]['coefficient']
            if coef > 0:
                coef_string = '+'+str(round(coef,1))
            else:
                coef_string = str(round(coef,1))

            para.append('</span >')

            para.append('<input type="hidden" id="desc')
            para.append(str(counter))
            para.append('" value="')
            para.append(coef_string)
            para.append('">')


            para.append(' ')
            counter+=1
    final= ''.join(para)
    return final


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



