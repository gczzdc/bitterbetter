import pandas as pd
import numpy as np
import matplotlib
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import colors
import json
import pickle
import copy
import string
import unicodedata

from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn import base
from sklearn.feature_extraction.text import TfidfVectorizer
from custom_transformers import NumberDestroyer

with open('weights.json','r') as f:
	feature_coef_dic = json.load(f)
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

bigram_regressor = Pipeline([
    ('preprocessing',column_bigram_transformer),
    #('estimator',SGDRegressor(alpha=.0002, max_iter=30000))
    ('estimator',Ridge(alpha=3))
    ])

with open('regressor.pickle','rb') as f:
    fitted_regressor = pickle.load(f)

#would be better if color map were not hard-coded here and below but rather a global variable

def colors_from_coef(coef, vmin = -40, vmax = 40, cmap = cm.coolwarm, cutoffs = [-6,6]):
    norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    if coef < cutoffs[0] or coef > cutoffs[1]:
        normalized_coef = norm(coef)
        mapped_color = cmap(normalized_coef)
        hex_color = colors.to_hex(mapped_color)
        return hex_color
    else:
        return False


def build_colors_plt(text, feature_coef_dic):
    words = text.split()
    ans_dic ={}    
    for word in words:
        if word in feature_coef_dic:
            coef = feature_coef_dic[word]
            hex_col = colors_from_coef(coef)
            if hex_col:
                ans_dic[word]={'hex_color':hex_col, 'coefficient':coef}
    return ans_dic

def clean(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] not in ("C","P"))


def bag_of_words_paragraph(text,features_coef_dic=feature_coef_dic):
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
            para.append('class="tooltip"')
            para.append('style="background: ')
            para.append(working_dic[word]['hex_color'])
            para.append('"')
            para.append('>')
            para.append(word)
            para.append('<span ')
            para.append('class="tooltiptext" ')
            para.append('style="color: ')
            para.append(working_dic[word]['hex_color'])           
            para.append('"')
            para.append('>')
            coef = working_dic[word]['coefficient']
            if coef > 0:
                para.append('+')    
            para.append(str(int(coef)))
            para.append('</span >')
            para.append('</span >')
            para.append(' ')
            counter+=1
    final= ''.join(para)
    return final


def best_predictor(text, abv=5.5, style='Pale Ale - American / APA'):
    if style == 'not specified':
        style = 'Pale Ale - American / APA' #fix this later
    return fitted_regressor.predict(pd.DataFrame([{'text': text,'abv': abv, 'style': style},]))

def generate_gradient(gradient_name='coolwarm', with_text=True, filename = 'static/gradient.png'):
	gradient = np.linspace(0, 1, 256)
	gradient = np.vstack((gradient, gradient))

	figh = 0.72
	plt.figure(figsize=(6.4, figh))
	ax=plt.gca()

    # axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

	ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(gradient_name))
	if with_text:
		ax.text(.2, 1.3, 'less bitter', 
				va='center', 
				ha='right', 
				fontsize=16, 
				fontname="arial",
				transform=ax.transAxes) 
		ax.text(1, 1.3, 'more bitter', 
				va='center', 
				ha='right', 
				fontsize=16, 
				fontname="arial",
				transform=ax.transAxes) 
    
	ax.set_axis_off()
	# plt.show()

	f =ax.get_figure()
	f.savefig(filename, bbox_inches="tight", transparent=True)