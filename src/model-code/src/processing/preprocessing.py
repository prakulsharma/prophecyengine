import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class NumericalImputer(BaseEstimator, TransformerMixin):
    """Numerical missing value imputer."""

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        # persist mode in a dictionary
        self.imputer_dict_ = {}
        for feature in self.variables:
            self.imputer_dict_[feature] = X[feature].mode()[0]
        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature].fillna(self.imputer_dict_[feature], inplace=True)
        return X


class KeepRequiredFeatures(BaseEstimator, TransformerMixin):

    def __init__(self, tags_to_keep=[]):
        self.tags_to_keep = tags_to_keep

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # keep only required tags
        X = X[self.tags_to_keep].copy()

        return X


class FeatureRangeCheck(BaseEstimator, TransformerMixin):

    def __init__(self, data_range={}):
        self.data_range = data_range

    def fit(self, X):
        return self

    def transform(self, X):
        df_rdata = X[list(self.data_range.keys())].copy()
        df_rdata.reset_index(drop=True, inplace=True)
        df_range = pd.DataFrame.from_dict(data=self.data_range, orient='columns')
        df_left = df_rdata - df_range.iloc[0]
        df_right = df_rdata - df_range.iloc[1]
        df_right_sign = (df_right <= 0).astype(int)
        df_left_sign = (df_left >= 0).astype(int)

        df_dec = df_right_sign.multiply(df_left_sign)
        df_final = df_rdata.multiply(df_dec)

        del df_rdata, df_range, df_left, df_right, df_left_sign, df_right_sign
        return df_final


class MedianFilter(BaseEstimator, TransformerMixin):

    def __init__(self, filter_value=0):
        self.filter_value = filter_value

    def fit(self, X):
        return self

    def transform(self, X):
        df_raw = X.copy(deep=True)
        df_data = df_raw.rolling(self.filter_value, center=True, min_periods=1).median()

        return df_data
