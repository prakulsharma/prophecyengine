import datetime
import warnings
from datetime import timedelta
from typing import List
import json
import numpy as np
import pandas as pd
import yaml
from analyticexecution.analytic_model import DataPayload
from analyticexecution.analytic_model import DataPoint
from matplotlib import pyplot as plt


def get_parameter(name, var_type, data, default=None):
    try:
        s = data.parameters.get(name, None)
        c = var_type(s)
        return c
    except Exception as e:
        return default


def construct_output_score(anomalies: pd.DataFrame, cfs: pd.DataFrame, mappings) -> List[DataPoint]:
    outputs = []
    for i, r in anomalies.iterrows():
        if cfs is None:
            d = DataPoint(timestamp=i, asset_id=mappings['anomaly_score'][0], channel_key=mappings['anomaly_score'][1],
                          value=r['anomaly_score'], context={})
        else:
            cf_dict = dict(cfs.loc[i])
            context_dict = {}
            for key, val in cf_dict.items():
                mapping_tup = mappings[key]
                asset_id_context = mapping_tup[0]
                channel_key_context = mapping_tup[1]
                dct = {key: {"value": val, "asset_id": int(asset_id_context), "channel_key": channel_key_context}}
                context_dict.update(dct)

            d = DataPoint(timestamp=i, asset_id=mappings['anomaly_score'][0], channel_key=mappings['anomaly_score'][1],
                          value=r['anomaly_score'],context=context_dict)
        outputs.append(d)
    return outputs


def construct_output_threshold(anomalies: pd.DataFrame, asset_id: str, channel_key: str) \
        -> List[DataPoint]:
    outputs = []
    for i, r in anomalies.iterrows():
        d = DataPoint(timestamp=i, asset_id=asset_id, channel_key=channel_key, value=r['anomaly_threshold'], context={})
        outputs.append(d)
    return outputs


def silent_numerify(s):
    try:
        return int(s)
    except:
        pass
    try:
        return float(s)
    except:
        pass
    try:
        return json.loads(s)
    except:
        pass
    return s


def simple_voting(labels_arrays: np.ndarray, scores_arrays: np.ndarray, agreement_factor=0.5):
    if not isinstance(scores_arrays, np.ndarray):
        return None
    if scores_arrays.ndim > 1:
        if any([x for x in scores_arrays if not isinstance(x, np.ndarray)]):
            return None
    elif scores_arrays.ndim == 1:
        return scores_arrays
    else:
        return None
    expected_labels_length = len(scores_arrays[0])
    if any([x for x in scores_arrays if len(x) != expected_labels_length]):
        return None

    number_methods = len(scores_arrays)
    total_labels = sum(labels_arrays)
    total_scores = sum(scores_arrays) / number_methods  # average score
    result = list(map(lambda x: 1 if x / number_methods > agreement_factor else 0, total_labels))
    out = []
    for i in range(0, len(result)):
        if result[i] == 0:
            out.append(0)
        else:
            out.append(total_scores[i])
    return np.array(out)


def simple_mean_of_cfs(combined_anomalies: pd.DataFrame, cfs: list) -> pd.DataFrame:
    cleaned_cfs = []
    for cf in cfs:
        if cf is None or not isinstance(cf, pd.DataFrame) or not all(cf.shape):
            print('WARNING - A method that was used did not return valid contributing factors.')
            continue
        cleaned_cfs.append(cf.loc[[x for x in cf.index if x in combined_anomalies.index]])

    if len(cleaned_cfs) == 0:
        return None

    df_concat = pd.concat([x for x in cleaned_cfs])
    df_cf = df_concat.groupby(df_concat.index).mean()
    return df_cf


def test_plot_anomalies(combined_anomaly_labels, data, method_name=''):
    plt.plot(data.df)
    # plt.legend(data.df.columns.values, loc='upper left')
    plt.vlines(data.df.index[np.where(np.array(combined_anomaly_labels) > 0)],
               ymax=max(data.df.max()),
               ymin=min(data.df.min()),
               colors='r')
    plt.title(method_name)
    plt.show()


def persist_and_latch_anomalies(filename, anomaly_column, anomaly_threshold,
                                persistence_limit, persistence_window,
                                latch_window):
    df = pd.read_csv(filename, index_col='datetime')
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)

    df['breached'] = [1 if x > anomaly_threshold else 0 for x in df[anomaly_column]]
    df['persist_count'] = df['breached'].rolling(persistence_window).sum()
    df['latched_anomalies'] = pd.Series()

    latched = False
    for i, row in df.iterrows():
        if not latched:
            if row['persist_count'] >= persistence_limit:
                latched = True
                latch_start = i
                df.loc[i, 'latched_anomalies'] = round(100.0 * row['persist_count'] / persistence_window)
        else:
            if i - latch_start >= timedelta(hours=latch_window - 1):
                latched = False

    anomaly_indices = df[~df['latched_anomalies'].isna()].index
    out_df = pd.DataFrame(columns=df.columns.values, index=anomaly_indices)

    for i in anomaly_indices:
        window_df = df.loc[:i].tail(persistence_window)
        out_df.loc[i] = window_df[window_df['breached'] == 1].mean()
        out_df.loc[i]['latched_anomalies'] = df.loc[i]['latched_anomalies']

    return out_df


# def test_plot_out_json(filename):
#
#     with open(filename, 'r') as f:
#         data = json.load(f)
#     d = data['outputs']
#     df = pd.DataFrame(columns=[x for x in d[0]['context'].keys()])
#     for point in d:
#         df.loc[point['ts']] = point['context']
#     df['anomaly-score'] = [x['value'] for x in d]
#     df.index = pd.to_datetime(df.index, infer_datetime_format=True)
#
#     f, axes = plt.subplots(2, 1, sharex='all')
#     axes[0].bar(df.index, height=df['anomaly-score'])
#     axes[1].plot(df[["TIC1420.MV",
#                     "AI1023",
#                      "AI1003A",
#                      "AI1003B"
#                     ]], '.-')
#     axes[1].legend(labels=["PG TO 105C CO2 STRP RBLR",
#                     "CO2 Slip at 142D2 Outlet",
#                     "106D CO outlet",
#                     "106D CO2 outlet"])
#
#     plt.show()


# def out_json_to_csv(filename):
#
#     with open(filename, 'r') as f:
#         data = json.load(f)
#     d = data['outputs']
#     df = pd.DataFrame(columns=[x for x in d[0]['context'].keys() if x != 'AI1023'])
#     for point in d:
#         point['context'].pop('AI1023')
#         df.loc[point['ts']] = \
#             {key: (100*value/sum(point['context'].values())) for key, value in point['context'].items()}
#     df['anomaly-score'] = [x['value'] for x in d]
#     df.index = pd.to_datetime(df.index, infer_datetime_format=True)
#     df['AI1023'] = 0
#     df.to_csv(filename.replace('.json', '') + '.csv', index_label='datetime')

def str2bool(s: str):
    if s.lower() == 'true' or s.lower() == 'yes' or s.lower() == 'y' or s == '1':
        return True
    try:
        i = int(s)
        if i == 1:
            return True
        else:
            return False
    except:
        return False


def timeindex_data(data, datetime_col=0, date_format=None):
    """
    parameters:
    ----------
    data : pandas DataFrame or a csv filepath
    datetime_col : datetime column in pandas dataframe or csv - provide index only
    format : datetime format in csv file or pandas dataframe
    # TODO: add the dateformat list and options in docstring
    ----------
    Returns a dataframe  with TimeIndexed datetime as index
    """
    if isinstance(data, pd.DataFrame):
        df = data
        try:
            df.index = pd.to_datetime(df.index, format=date_format)
        except:
            df.set_index(list(df.columns)[datetime_col], inplace=True)
            df.index = pd.to_datetime(df.index, format=date_format)
    else:
        df = pd.read_csv(data, index_col=datetime_col)
        df.index = pd.to_datetime(df.index, format=date_format)

    return df


def df_between_dates(df, datetime_col=0, format=None, sd=None, ed=None, csv=False):
    """
    slicing dataframe between two dateranges
    Parameters:
    ------------
    df : pandas dataframe or csv filepath (make sure csv=True if filepath is provided)
    datecolumn: datetime column in pandas dataframe -provide index only
    format: datetime format in csv file or pandas dataframe
    sd: start date tuple (Y,m,d,H,M,S)--> (2019,12,26,0,0,0) no paddings for single digit month/dates
    ed: end date tuple (Y,m,d,H,M,S)--> (2019,12,28,0,0,0) no paddings for single digit month/dates
    if sd and ed are by default start and end date of dataframe
    """
    if csv:
        df = pd.read_csv(df, index_col=datetime_col)
        df.index = pd.to_datetime(df.index, format=format)
    else:
        try:
            df.index = pd.to_datetime(df.index, format=format)
        except:
            df.set_index(list(df.columns)[datetime_col], inplace=True)
            df.index = pd.to_datetime(df.index, format=format)
    if sd is None and ed is not None:
        ed_dt = pd.datetime(*ed)
        df_cut = df[df.index <= ed_dt]
    elif sd is not None and ed is None:
        sd_dt = pd.datetime(*sd)
        df_cut = df[df.index >= sd_dt]
    elif sd is not None and ed is not None:
        ed_dt = pd.datetime(*ed)
        sd_dt = pd.datetime(*sd)
        if sd_dt >= ed_dt:
            raise Exception('start date is larger than end date')
        df_cut = df[(df.index <= ed_dt) & (df.index >= sd_dt)]
    elif sd is None and ed is None:
        df_cut = df
    return df_cut

class DataPayloadTransformer:

    def transform(self, data):
        """
        Convert AnalyticJob object to DataPayload
        :param data: A AnalyticJob expressed in the form of a dictionary
        :return: DataPayload
        """

        timestamps = data['timestamps']
        columns = data['analytic_inputs']
        rows = data['data']
        if len(rows) == 0 or len(rows[0]) == 0:
            value_rows = [[]]
            context_rows = None
            df = pd.DataFrame()
        elif isinstance(rows[0][0], dict):
            value_rows = [[x['value'] for x in r] for r in rows]
            context_rows = [[x['context'] for x in r] for r in rows]
            df = pd.DataFrame(columns=columns, data=value_rows, index=timestamps)
        #           df.dropna(inplace=True)
        else:
            value_rows = rows
            context_rows = None
            df = pd.DataFrame(columns=columns, data=value_rows, index=timestamps)
        #            df.dropna(inplace=True)

        data_payload = DataPayload()
        # If this is an ACE analytic, the one and only analytic interface will map to a channel called anomaly-score.
        # If this is the case, set the assetId in data_payload.
        if len(data['mappings']) > 0:
            if data['mappings'][0].get('channelKey', '') == 'anomaly-score':
                data_payload.asset_id = data['mappings'][0]['assetId']
        data_payload.analytic_id = data['analytic']['id']
        data_payload.analytic_name = data['analytic']['name']
        data_payload.analytic_version = data['analytic']['version']
        data_payload.parameters = data['parameters']
        data_payload.model_name = data['model_name']
        data_payload.mappings = {x['analyticInterfaceName']: (x['assetId'], x['channelKey']) for x in data['mappings']}
        data_payload.df = df
        if context_rows is not None:
            data_payload.measurements = []
            data_payload.measurements_dict = {}
            for i in range(0, len(timestamps)):
                data_payload.measurements_dict[timestamps[i]] = []
                for j in range(0, len(columns)):
                    point = {'timestamp': timestamps[i],
                             'value': value_rows[i][j],
                             'context': context_rows[i][j],
                             'channelKey': columns[j],
                             'assetId': data['mappings'][j]['assetId']}
                    data_payload.measurements.append(point)
                    data_payload.measurements_dict[timestamps[i]].append(point)

        return data_payload


def missing_val_handling(df, model='interpolate', method=None):
    '''
    estimates and fills missing values of remove rows with missing values
    parameters:
    ---------
    df:TimeIndexed dataframe
    model: 'interpolate', 'fillna','dropna' (interpolate is default)
    method:
          interpolate ---> 'linear'(default)
          fillna ----> None will add zero for all the values
          fillna ----> ffill (fill forward)
          fillna -----> bfill (fill backward)
          fillna: ----->any other pandas supported method
          dropna ------> drop the rows with nan
    ----------
    return a dataframe with estimated or removed missing values
    This df can be used for further analysis

    '''

    if model == 'interpolate':
        if not method:
            method = 'linear'
        df.interpolate(method=method, inplace=True)
    elif model == 'fillna':
        if not method:
            df.fillna(0, inplace=True)
        else:
            df.fillna(method=method, inplace=True)
    elif model == 'dropna':
        df.dropna(inplace=True)
    return df


def fxn():
    warnings.warn("deprecated", DeprecationWarning)
    return


def fetch_allowed_tag_list(data):
    try:
        allowed_tags = json.loads(data.parameters.get('allowed_tags', data.df.columns.values))
    except Exception as e:
        allowed_tags = data.parameters.get('allowed_tags', data.df.columns.values)
    if allowed_tags is None:
        allowed_tags = data.df.columns.values
    return allowed_tags
