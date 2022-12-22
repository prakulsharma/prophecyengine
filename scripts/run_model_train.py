from model_widgets import train_workbench, score_workbench
from analysis import read_time_series_csv
import os


df = read_time_series_csv("../data/raw-data/ogc_train_file2.csv", date_format='%Y-%m-%dT%H:%M:%S')
trained_model_name = "ogc_trained_artifact"
trained_filename = trained_model_name + str(".pickled")
trained_model_path = os.path.join("../models", trained_filename)


if __name__ == "__main__":
    train_workbench(df, config_yml_path="../config/ogc_config.yaml", trained_model_path=trained_model_path)
