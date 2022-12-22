from model_widgets import train_workbench, score_workbench
from analysis import read_time_series_csv
import os


df = read_time_series_csv("../data/raw-data/air_comp_testing_data.csv", date_format='%Y-%m-%dT%H:%M:%S')
trained_filename = "comp_trained_artifact.pickled"
models_folder_path = "../models"
trained_model_path = os.path.join(models_folder_path, trained_filename)

if __name__ == "__main__":
    df_cf, max_len, fig = score_workbench(df, config_yml_path="../config/air_comp_config.yaml", trained_model_fpath=trained_model_path,
                                          outpath="../output/score.json")

    print ("vggvg")
