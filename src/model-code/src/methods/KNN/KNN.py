import pandas as pd
import numpy as np
from ..AnomalyDetectionMethod import AnomalyDetectionMethod
from pyod.models.knn import KNN as pyod_KNN


class KNN(AnomalyDetectionMethod):

    def __init__(self, **kwargs):
        super(KNN, self).__init__()
        self.params = kwargs
        self.detector = pyod_KNN(**self.params)

    def check_configuration(self, config_dict):
        return True

    def check_input_data(self, data):
        return True

    def fit(self, data):
        return self.detector.fit(data)

    def predict(self, data):
        return self.detector.predict(data)

    def calculate_contributing_factors(self, df, labels):

        anomalous_point_indices = np.where(labels == 1)[0]
        k_nearest_neighs = self.detector.tree_.query(df.iloc[anomalous_point_indices, :],
                                                     k=5, return_distance=False)
        nearest_neighs = [x[0] for x in [points for points in k_nearest_neighs]]

        j = 0
        cf_df = pd.DataFrame(columns=df.columns.values)
        for i in df.index[np.where(labels == 1)]:
            cf = (df.loc[i] - self.detector.neigh_._fit_X[nearest_neighs[j]])
            cf = cf ** 2
            cf_sum = sum(cf)
            cf = 100 * cf / cf_sum
            cf_df = cf_df.append(pd.Series(cf, name=i))
            j += 1

        return cf_df
