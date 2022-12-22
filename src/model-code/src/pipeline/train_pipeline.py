from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from processing import preprocessing as pp


def get_data_pipe(allowed_tags):

    return Pipeline([('allowed_tags', pp.KeepRequiredFeatures(tags_to_keep=allowed_tags)),
                     ('scale_data', MinMaxScaler((-1, 1))),
                     ])
