import numpy as np
import pandas as pd
from ..AnomalyDetectionMethod import AnomalyDetectionMethod
from pyod.models.pca import PCA as pyod_PCA


class PCA(AnomalyDetectionMethod):

    def __init__(self, **kwargs):
        super(PCA, self).__init__()
        self.params = kwargs
        self.detector = pyod_PCA(**self.params)

    def check_configuration(self, config_dict):
        return True

    def check_input_data(self, data):
        return True

    def fit(self, data):
        return self.detector.fit(data)

    def predict(self, data):
        return self.detector.predict(data)

    def calculate_contributing_factors(self, df, labels):
        try:
            x_test = np.array(df)
            anomalous_points = x_test[np.where(labels == 1)]
            reconstruct = self.detector.detector_.inverse_transform(self.detector.detector_.transform(anomalous_points))
            residual = anomalous_points - reconstruct
            residual = abs(residual)
            cf = [100*x/sum(x) for x in residual]
            df_cf = pd.DataFrame(data=cf,
                                 index=df.index[np.where(labels == 1)],
                                 columns=df.columns.values)
            return df_cf
        except Exception as e:
            print(e)
            return None
