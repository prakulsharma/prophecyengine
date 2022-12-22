import pandas as pd
import numpy as np
from ..AnomalyDetectionMethod import AnomalyDetectionMethod
from pyod.models.ocsvm import OCSVM as pyod_OCSVM


class OCSVM(AnomalyDetectionMethod):

    def __init__(self, **kwargs):
        super(OCSVM, self).__init__()
        self.params = kwargs
        self.detector = pyod_OCSVM(**self.params)

    def check_configuration(self, config_dict):
        return True

    def check_input_data(self, data):
        return True

    def fit(self, data):
        return self.detector.fit(data)

    def predict(self, data):
        return self.detector.predict(data)

    def calculate_contributing_factors(self, df, labels):

        cf_df = pd.DataFrame(columns=df.columns.values)
        cleaned_support_indices = [np.where(self.detector.support_ == x)[0][0]
                                   for x in self.detector.support_
                                   if x not in np.where(self.detector.labels_ == 1)[0]]
        cleaned_support_vectors = self.detector.support_vectors_[cleaned_support_indices]
        for i in df.index[np.where(labels == 1)]:
            distances = [np.linalg.norm(df.loc[i] - x) for x in cleaned_support_vectors]
            d = np.array(distances)
            j = np.where(d == d.min())[0][0]
            cf = (df.loc[i] - cleaned_support_vectors[j])
            cf = cf ** 2
            cf_sum = sum(cf)
            cf = 100 * cf / cf_sum
            cf_df = cf_df.append(pd.Series(cf, name=i))

        return cf_df