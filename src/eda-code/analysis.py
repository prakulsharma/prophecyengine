# Input to all functions (except read_csv) in this file will be a DataFrame. The output will vary.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from util.filter_columns import filter_columns
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def read_csv_with_mixed_types(filename):
    """

    :param filename:
    :return:
    """
    return read_time_series_csv(filename, convert_to_numeric=False)


def read_time_series_csv(filename, datetime_col=0, date_format=None, convert_to_numeric=True, infer_datetime=False):
    """

    Parameters
    ----------
    filename: csv filepath
    datetime_col: datetime column number in csv (starts with 0), default 0
    date_format: datetime format in csv file , i.e '%Y-%m-%dT%H:%M:%S' etc
    convert_to_numeric: default is True, it converts all non-numeric to NaN if set True
    infer_datetime: default False, use True with extreme caution. It is known to create incorrect inferring

    Returns
    -------
    A dataframe with timeindexed timestamp as index

    """
    # infer_datetime use
    if date_format is None:
        infer_datetime = True
    # Read file
    df = pd.read_csv(filename, dtype=object, index_col=datetime_col)

    # Convert timestamp column to datetime
    df.index = pd.to_datetime(df.index, format=date_format, infer_datetime_format=infer_datetime)

    if convert_to_numeric:
        # Convert all data to numeric
        df = df.apply(pd.to_numeric, errors='coerce')

    return df


def timeindex_data(data, datetime_col=0, date_format=None, convert_to_numeric=True, infer_datetime=False):
    """
    parameters:
    ----------
    data : pandas DataFrame or a csv filepath
    datetime_col : datetime column in pandas dataframe or csv - provide index only
    date_format : datetime format in csv file or pandas dataframe, '%Y-%m-%dT%H:%M:%S'
    convert_to_numeric: default is True, it converts all non-numeric to NaN if set True
    infer_datetime: default False, use True with extreme caution. It is known to create incorrect inferring
    # TODO: add the dateformat list and options in docstring
    ----------
    Returns:
    pandas dataframe  with TimeIndexed datetime as index
    """
    if isinstance(data, pd.DataFrame):
        df = data
        try:
            df.index = pd.to_datetime(df.index, format=date_format, infer_datetime_format=infer_datetime)
        except:
            df.set_index(list(df.columns)[datetime_col], inplace=True)
            df.index = pd.to_datetime(df.index, format=date_format, infer_datetime_format=infer_datetime)
    else:
        df = pd.read_csv(data, index_col=datetime_col)
        df.index = pd.to_datetime(df.index, format=date_format, infer_datetime_format=infer_datetime)
    if convert_to_numeric:
        # Convert all data to numeric
        df = df.apply(pd.to_numeric, errors='coerce')

    return df


def read_events_csv(filename):
    # Read file
    df = pd.read_csv(filename, dtype=object)

    # Convert timestamp column to datetime
    df.timestamp = pd.to_datetime(df.timestamp, format='%Y-%m-%dT%H:%M:%S')
    df.set_index('timestamp', drop=True, inplace=True)
    df = df[~df.index.isnull()]

    return df


def generate_data_hygiene_report(df: pd.DataFrame):
    report_dict = dict()

    # Find empty columns
    # report_dict['empty_columns'] = _find_empty_columns(df)
    # Find nulls per column
    report_dict['missing%'] = _find_percent_nulls_per_column(df)
    # Find stale columns
    report_dict['stale%'] = _find_stale_columns(df)
    # Find Negative % data
    report_dict['negative%'] = _find_percent_negative_per_column(df)
    # Find non-numeric columns
    # Find mixed columns
    df_ret = pd.DataFrame(report_dict)

    # stat description
    df_stat = round(df.describe().T, 1)
    df_ret = df_ret.merge(df_stat, how='inner', left_index=True, right_index=True)
    df_ret.drop(['count'], axis=1, inplace=True)

    return df_ret


@filter_columns
def plot_time_series(df: pd.DataFrame, columns=None, use_column_indices=False, event_timestamps=None, subplots=False,
                     normalized=False, standardized=False):
    if normalized and standardized:
        print('Normalized and standardized have been set to True. Normalization will take precedence.')

    if normalized:
        scaled_df = (df - df.min()) / (df.max() - df.min())
    elif standardized:
        scaled_df = (df - df.mean()) / df.std()
    else:
        scaled_df = df

    if subplots:
        fig, ax = plt.subplots(nrows=scaled_df.shape[1], ncols=1, figsize=(20, 10))
        subplot_number = 0
        for col in scaled_df.columns:
            subplot_number += 1
            ax[subplot_number - 1].plot(scaled_df[col])
            ax[subplot_number - 1].set_title(col)
            if event_timestamps is not None:
                ax[subplot_number - 1].vlines(event_timestamps, ymin=min(scaled_df[col]), ymax=max(scaled_df[col]))
        fig.tight_layout()
    else:
        scaled_df.plot(figsize=(20, 10))
        if event_timestamps is not None:
            plt.vlines(event_timestamps, ymin=min(scaled_df.select_dtypes(include=[np.number]).min()),
                       ymax=max(scaled_df.select_dtypes(include=[np.number]).max()))

    plt.show()


@filter_columns
def plot_correlation_matrix(df: pd.DataFrame, columns=None, use_column_indices=False, **kwargs):
    f = plt.figure(figsize=(20, 10))
    ax = plt.gca()
    im = ax.matshow(df.corr(**kwargs), cmap=plt.cm.get_cmap('RdBu').reversed(), vmin=-1, vmax=1)
    ax.set_xticks([x for x in range(df.shape[1])])
    ax.set_xticklabels(df.columns, rotation=90)
    ax.set_yticks(range(df.shape[1]))
    ax.set_yticklabels(df.columns)
    cb = f.colorbar(im)
    cb.ax.tick_params(labelsize=8)
    f.tight_layout()
    plt.show()


@filter_columns
def plot_distributions(df: pd.DataFrame, columns=None, use_column_indices=False, subplots=False, **kwargs):
    if subplots:
        df.hist(**kwargs)
    else:
        for col in df.columns:
            f = plt.figure(figsize=(20, 10))
            ax = plt.gca()
            ax.hist(df[col], **kwargs)
            ax.set_title(col)

    plt.show()


@filter_columns
def plot_scatter(df: pd.DataFrame, columns: list, use_column_indices=False, normalized=False, standardized=False,
                 **kwargs):
    if len(columns) < 2:
        raise Exception('\'columns\' must have a minimum of two elements.')
    if len(columns) > 2:
        print('There are more than 2 columns passed. Using only first two columns in scatter plot.')

    if normalized and standardized:
        print('Normalized and standardized have been set to True. Normalization will take precedence.')

    if normalized:
        scaled_df = (df - df.min()) / (df.max() - df.min())
    elif standardized:
        scaled_df = (df - df.mean()) / df.std()
    else:
        scaled_df = df

    f = plt.figure()
    ax = plt.gca()
    ax.scatter(scaled_df.iloc[:, 0], scaled_df.iloc[:, 1], **kwargs)
    ax.set_xlabel(scaled_df.columns.values[0])
    ax.set_ylabel(scaled_df.columns.values[1])
    plt.show()


# Private methods


def _find_empty_columns(df: pd.DataFrame):
    return [col for col in df.columns if df[col].isnull().all()]


def _find_percent_nulls_per_row(df: pd.DataFrame):
    """

    Parameters
    ----------
    df: pandas dataframe

    Returns
    -------
    a dictionary with key as row indices  and % missing data as value

    """
    total_column_count = df.shape[1]
    null_column_count = df.isnull().sum(axis=1)
    null_percent = round(100.0 * null_column_count / total_column_count, 1)
    result_dict = dict(null_percent)

    return result_dict


def dropped_rows(df: pd.DataFrame, result_dict, percent):
    """

    Parameters
    ----------
    df : pandas dataframe
    result_dict: dictionary with key as row indiced and % missing values data as value
    percent: % of missing row value above which rows to be dropped

    """
    # Temporary dictionary
    r = dict()
    r['missing_rows'] = result_dict
    dataframe = pd.DataFrame(r)
    rows_to_drop = list(dataframe[dataframe["missing_rows"] > percent].index)
    df.drop(rows_to_drop, inplace=True)
    return df


def _find_percent_nulls_per_column(df: pd.DataFrame):
    """

    Parameters
    ----------
    df: pandas dataframe

    Returns
    -------
    a dictionary with key as column names and % missing data as value

    """
    total_row_count = df.shape[0]
    null_row_count = df.isnull().sum(axis=0)
    null_percent = round(100.0 * null_row_count / total_row_count, 1)
    result_dict = dict(null_percent)

    return result_dict


def _find_stale_columns(df: pd.DataFrame, stale_threshold=30):
    """

    Parameters
    ----------
    df: pandas dataframe
    stale_threshold: consecutive points to be exactly same for defining data block as stale, default=30

    Returns
    -------
    a dictionary containing dataframe column names as key and % of stale datapoints as value

    """
    result_dict = dict()
    total_row_count = df.shape[0]
    col_name_list = df.columns.tolist()

    for col in col_name_list:
        df_col = df[[col]].copy()
        df_col['block'] = (df_col[col] != df_col[col].shift(1)).cumsum()
        block_group = df_col.groupby('block').count()[col]
        stale_data = block_group[block_group >= stale_threshold]
        stale_data_count = stale_data.sum()
        result_dict[col] = round(100.0 * (stale_data_count / total_row_count), 1)
    return result_dict


def _find_percent_negative_per_column(df: pd.DataFrame):
    """

    Parameters
    ----------
    df: Pandas Dataframe

    Returns
    -------
    a dictionary with columns as key and % NEGATIVE data per column as value

    """
    total_row_count = df.shape[0]
    negative_row_count = (df <= 0).sum(axis=0)
    negative_percent = round(100.0 * negative_row_count / total_row_count, 1)
    result_dict = dict(negative_percent)

    return result_dict


# plotly charting functions


def plot_correlation_matrix_plotly(df: pd.DataFrame, columns=None, h=500, w=1000, debug=True, **kwargs):
    if columns is not None:
        df = df[columns]
    else:
        columns = list(df.columns)
    df_corr = df.corr()
    fig = go.Figure(data=go.Heatmap(
        z=df_corr.values,
        x=list(df_corr.columns),
        y=list(df_corr.columns),
        colorscale='Tropic',
        hoverongaps=False))
    fig.update_layout(height=800, width=1000)
    if debug:
        fig.show()

    return fig


def plot_scatter_plotly(df: pd.DataFrame, columns=None, event_timestamps=None, subplots=False, normalized=False,
                        standardized=False, h=500, w=1000, debug=True):
    if columns is not None:
        df = df[columns]
    else:
        columns = list(df.columns)
    if normalized and standardized:
        print('Normalized and standardized have been set to True. Normalization will take precedence.')

    if normalized:
        scaled_df = (df - df.min()) / (df.max() - df.min())
    elif standardized:
        scaled_df = (df - df.mean()) / df.std()
    else:
        scaled_df = df

    if subplots:
        subplot_no = len(columns)
        col_val = 2
        row_val = math.ceil(subplot_no / col_val)

        fig = make_subplots(
            cols=2,
            rows=row_val,
            subplot_titles=columns,
            vertical_spacing=0.2,
            horizontal_spacing=0.2
        )
        for i, column in enumerate(columns):
            j = i + 1
            row_num = math.ceil(j / 2)
            if j % 2 == 0:
                col_num = 2
            else:
                col_num = 1
            fig.add_trace(go.Scatter(x=scaled_df.index, y=scaled_df[column], mode='markers'), row=row_num, col=col_num)
        fig.update_layout(height=h / 2 * row_val, width=w, showlegend=False, )
    else:
        fig = go.Figure()
        for column in columns:
            fig.add_trace(go.Scatter(x=scaled_df.index, y=scaled_df[column], name=column, mode='markers'))
        fig.update_layout(height=h, width=w, legend_orientation="h")
    if debug:
        fig.show()

    return fig


def plot_distributions_plotly(df: pd.DataFrame, columns=None, normalized=False, standardized=False, h=500, w=1000,
                              debug=True):
    if columns is not None:
        df = df[columns]
    else:
        columns = list(df.columns)
    if normalized and standardized:
        print('Normalized and standardized have been set to True. Normalization will take precedence.')

    if normalized:
        scaled_df = (df - df.min()) / (df.max() - df.min())
    elif standardized:
        scaled_df = (df - df.mean()) / df.std()
    else:
        scaled_df = df

    subplot_no = len(columns)
    col_val = 2
    row_val = math.ceil(subplot_no / col_val)

    fig = make_subplots(
        cols=2,
        rows=row_val,
        subplot_titles=columns,
        vertical_spacing=0.2,
        horizontal_spacing=0.2
    )
    for i, column in enumerate(columns):
        j = i + 1
        row_num = math.ceil(j / 2)
        if j % 2 == 0:
            col_num = 2
        else:
            col_num = 1
        fig.add_trace(go.Histogram(x=scaled_df[column]), row=row_num, col=col_num)
    fig.update_layout(height=h / 2 * row_val, width=w, showlegend=False)
    if debug:
        fig.show()

    return fig


def plot_time_series_plotly(df: pd.DataFrame, columns=None, event_timestamps=None, subplots=False, normalized=False,
                            standardized=False, h=500, w=1000, debug=True):
    if columns is not None:
        df = df[columns]
    else:
        columns = list(df.columns)
    if normalized and standardized:
        print('Normalized and standardized have been set to True. Normalization will take precedence.')

    if normalized:
        scaled_df = (df - df.min()) / (df.max() - df.min())
    elif standardized:
        scaled_df = (df - df.mean()) / df.std()
    else:
        scaled_df = df

    if subplots:
        subplot_no = len(columns)
        col_val = 2
        row_val = math.ceil(subplot_no / col_val)

        fig = make_subplots(
            cols=2,
            rows=row_val,
            subplot_titles=columns,
            horizontal_spacing=0.2,
            vertical_spacing=0.2
        )
        for i, column in enumerate(columns):
            j = i + 1
            row_num = math.ceil(j / 2)
            if j % 2 == 0:
                col_num = 2
            else:
                col_num = 1
            fig.add_trace(go.Scatter(x=scaled_df.index, y=scaled_df[column]), row=row_num, col=col_num)
        fig.update_layout(height=h / 2 * row_val, width=w, showlegend=False)
    else:
        fig = go.Figure()
        for column in columns:
            fig.add_trace(go.Scatter(x=scaled_df.index, y=scaled_df[column], name=column))
        fig.update_layout(height=h, width=w, legend_orientation="h", )
    #                     paper_bgcolor='rgba(0,0,0,0)',
    #                      plot_bgcolor='rgb(255,255,255)')
    #    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgb(230,230,230)')
    #    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgb(230,230,230)')
    #    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='rgb(230,230,230)')
    #    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='rgb(230,230,230)')
    if debug:
        fig.show()

    return fig
