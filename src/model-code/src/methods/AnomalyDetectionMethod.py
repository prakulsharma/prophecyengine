from __future__ import print_function

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class AnomalyDetectionMethod(ABC):

    @abstractmethod
    def check_configuration(self, config_dict) -> bool:
        pass

    @abstractmethod
    def check_input_data(self, data) -> bool:
        pass

    @abstractmethod
    def fit(self, data):
        pass

    @abstractmethod
    def predict(self, data):
        pass

    @abstractmethod
    def calculate_contributing_factors(self, test_df: pd.DataFrame, test_labels: np.ndarray) \
            -> pd.DataFrame:
        pass

    @staticmethod
    def normalize_output(df_anomalies):
        """
        Ensures that the output of each method is in the same format.
        :param df_anomalies:
        :return:
        """
        return df_anomalies
