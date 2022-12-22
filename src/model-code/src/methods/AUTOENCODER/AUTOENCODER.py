import numpy as np
import pandas as pd
from pyod.models.auto_encoder import AutoEncoder as pyod_AutoEncoder

from ..AnomalyDetectionMethod import AnomalyDetectionMethod


class AUTOENCODER(AnomalyDetectionMethod):

    def __init__(self, **kwargs):
        super(AUTOENCODER, self).__init__()
        self.params = kwargs
        self.detector = pyod_AutoEncoder(**self.params)

    def check_configuration(self, config_dict) -> bool:
        return True

    def check_input_data(self, data) -> bool:
        return True

    def fit(self, data):
        return self.detector.fit(data)

    def predict(self, data):
        return self.detector.predict(data)

    def calculate_contributing_factors(self, df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
        try:
            x_test = np.array(df)
            anomalous_point = x_test[np.where(labels == 1)]
            reconstruct = self.detector.model_.predict(anomalous_point)
            residual = anomalous_point - reconstruct
            residual = abs(residual)
            cf = [100 * x / sum(x) for x in residual]
            df_cf = pd.DataFrame(data=cf,
                                 index=df.index[np.where(labels == 1)],
                                 columns=df.columns.values)
            return df_cf
        except Exception as e:
            print(e)
            return None
