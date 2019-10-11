from sklearn import base
import copy

class NumberDestroyer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self):
        pass
   
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        d= {str(a):'' for a in range(10)}
        X_copy = copy.copy(X)
        for k in d:
            X_copy = X_copy.str.replace(k,d[k])
        return (X_copy)