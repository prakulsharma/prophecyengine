import math
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from util.filter_columns import filter_columns


@filter_columns
def isolation_forest(df: pd.DataFrame, columns=None, use_column_indices=False, plot=False,
                     outlier_marker_min=None, outlier_marker_max=None, **kwargs):
    """
    Applies isolation forest on a DataFrame to pick out outliers.
    :param df: pandas.DataFrame - DataFrame with the data to be analyzed.
    :param columns: list - List of column names or indices to use during the analysis (works as a filter).
    :param use_column_indices: bool - If True, it assumes that the elements of the "columns" argument are integers
    that represent the column indices. If False, it assumes that the elements of the "columns" argument are string
    column names.
    :param plot: bool - If True, produces a plot of the results.
    :param outlier_marker_min: numeric - The lower limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :param outlier_marker_max: numeric - The upper limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :param kwargs: keyword-arguments - Other keyword arguments for the sklearn.ensemble.IsolationForest class.
    :return: pandas.DataFrame - The original DataFrame (df) with an additional column called "outliers" that indicate
    the presence of outliers in the data with a binary value.
    """
    test_df = df.dropna(how='any')
    clf = IsolationForest(n_estimators=100, warm_start=True)
    clf.fit(test_df.values)
    outlier_labels = clf.predict(test_df.values)
    outlier_labels = [1 if x == -1 else 0 for x in outlier_labels]
    test_df['outliers'] = outlier_labels
    df = pd.concat([df, test_df['outliers']], axis=1)

    if plot:
        _plot_result_dfs(dfs=[df], titles=['Outlier detection using Isolation Forest'],
                         ymin=outlier_marker_min, ymax=outlier_marker_max, figsize=(20, 10))

    return df


@filter_columns
def elliptic_envelope(df: pd.DataFrame, columns=None, use_column_indices=False, plot=False,
                      outlier_marker_min=None, outlier_marker_max=None, **kwargs):
    """
    Applies elliptic envelope on a DataFrame to pick out outliers.
    :param df: pandas.DataFrame - DataFrame with the data to be analyzed.
    :param columns: list - List of column names or indices to use during the analysis (works as a filter).
    :param use_column_indices: bool - If True, it assumes that the elements of the "columns" argument are integers
    that represent the column indices. If False, it assumes that the elements of the "columns" argument are string
    column names.
    :param plot: bool - If True, produces a plot of the results.
    :param outlier_marker_min: numeric - The lower limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :param outlier_marker_max: numeric - The upper limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :param kwargs: keyword-arguments - Other keyword arguments for the sklearn.covariance.EllipticEnvelope class.
    :return: pandas.DataFrame - The original DataFrame (df) with an additional column called "outliers" that indicate
    the presence of outliers in the data with a binary value.
    """
    test_df = df.dropna(how='any')
    clf = EllipticEnvelope(**kwargs)
    clf.fit(test_df.values)
    outlier_labels = clf.predict(test_df.values)
    outlier_labels = [1 if x == -1 else 0 for x in outlier_labels]
    test_df['outliers'] = outlier_labels
    df = pd.concat([df, test_df['outliers']], axis=1)

    if plot:
        _plot_result_dfs(dfs=[df], titles=['Outlier detection using Elliptic Envelope'],
                         ymin=outlier_marker_min, ymax=outlier_marker_max, figsize=(20, 10))

    return df


@filter_columns
def local_outlier_factor(df: pd.DataFrame, columns=None, use_column_indices=False, plot=False,
                         outlier_marker_min=None, outlier_marker_max=None, **kwargs):
    """
    Applies local outlier factor (LOF) on a DataFrame to pick out outliers.
    :param df: pandas.DataFrame - DataFrame with the data to be analyzed.
    :param columns: list - List of column names or indices to use during the analysis (works as a filter).
    :param use_column_indices: bool - If True, it assumes that the elements of the "columns" argument are integers
    that represent the column indices. If False, it assumes that the elements of the "columns" argument are string
    column names.
    :param plot: bool - If True, produces a plot of the results.
    :param outlier_marker_min: numeric - The lower limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :param outlier_marker_max: numeric - The upper limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :param kwargs: keyword-arguments - Other keyword arguments for the sklearn.neighbors.LocalOutlierFactor class.
    :return: pandas.DataFrame - The original DataFrame (df) with an additional column called "outliers" that indicate
    the presence of outliers in the data with a binary value.
    """
    test_df = df.dropna(how='any')
    clf = LocalOutlierFactor(**kwargs)
    outlier_labels = clf.fit_predict(test_df.values)
    outlier_labels = [1 if x == -1 else 0 for x in outlier_labels]
    test_df['outliers'] = outlier_labels
    df = pd.concat([df, test_df['outliers']], axis=1)

    if plot:
        _plot_result_dfs(dfs=[df], titles=['Outlier detection using Local outlier factor'],
                         ymin=outlier_marker_min, ymax=outlier_marker_max, figsize=(20, 10))

    return df


def create_outlier_detection_ensemble(dfs: List[pd.DataFrame], agreement_factor=0.5, plot=False,
                                      outlier_marker_min=None, outlier_marker_max=None):
    """
    Combines results from multiple outlier methods into one using a voting algorithm.
    :param dfs: list - A list of DataFrames that were results of other outlier detection methods.
    :param agreement_factor: float - A number > 0 and <= 1 that denotes the percentage of result datasets that should
    agree on a datapoint being an outlier for the ensemble algorithm to consider an outlier. For example, if three
    datasets have been provided to this method and 2 out of 3 datasets consider point X to be an outlier, an
    agreement factor of <= 0.66 will be required to consider point X an outlier in the ensemble.
    :param plot: bool - If True, produces a plot of the results.
    :param outlier_marker_min: numeric - The lower limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :param outlier_marker_max: numeric - The upper limit of the vertical lines that are drawn on the results plot that
    indicate the time position of an outlier.
    :return: pandas.DataFrame - The original DataFrame (df) with an additional column called "outliers" that indicate
    the presence of outliers in the data with a binary value.
    """
    if len(dfs) < 1:
        print('No DFs supplied to ensemble function.')
        return
    if len(dfs) == 1:
        return dfs[0]
    if agreement_factor <= 0 or agreement_factor > 1.0:
        print('Agreement factor must be between non-inclusive 0 and inclusive 1.')
        return

    n = len(dfs)
    vote_threshold = math.ceil(n * agreement_factor)

    summed_outlier_labels = sum([df.iloc[:, -1] for df in dfs])
    voting_outlier_labels = [x if x >= vote_threshold else 0 for x in summed_outlier_labels]
    ensemble_df = dfs[0].iloc[:, 0:-1]
    ensemble_df['outliers'] = voting_outlier_labels

    if plot:
        _plot_result_dfs(dfs=[ensemble_df],
                         titles=['Outlier detection (Ensemble with agreement factor = {}'.format(agreement_factor)],
                         vote_threshold=vote_threshold,
                         ymin=outlier_marker_min, ymax=outlier_marker_max, figsize=(20, 10))

    return ensemble_df


# Private methods


def _plot_result_dfs(dfs: List[pd.DataFrame], titles=None, normalized=False, standardized=False, vote_threshold=None,
                     ymin=None, ymax=None, figsize=None):
    if len(dfs) < 1:
        print('No DFs supplied to plot function.')
        return

    if any(type(x) != pd.DataFrame for x in dfs):
        print('One of the DFs supplied to the plot function is not a pandas Dataframe.')
        return

    if normalized and standardized:
        print('Normalized and standardized have been set to True. Normalization will take precedence.')

    if titles is None:
        titles = ['Unnamed dataset ' + (i + 1).__str__() for i in range(len(dfs))]

    if len(titles) < len(dfs):
        to_extend = ['Unnamed dataset ' + (i + 1).__str__() for i in range(len(dfs) - len(titles))]
        titles.extend(to_extend)

    fig, ax = plt.subplots(nrows=len(dfs), ncols=1, figsize=figsize)
    subplot_number = 0

    if len(dfs) == 1:

        df = dfs[0]
        data_df = df.iloc[:, 0: -1]

        if normalized:
            scaled_df = (data_df - data_df.min()) / (data_df.max() - data_df.min())
        elif standardized:
            scaled_df = (data_df - data_df.mean()) / data_df.std()
        else:
            scaled_df = data_df

        data = df[df.iloc[:, -1] >= 1]
        if vote_threshold is not None:
            colors = list(['r' if x > vote_threshold else 'k' for x in data['outliers']])
        else:
            colors = None

        if ymin is None:
            ymin = scaled_df.values.min()
        if ymax is None:
            ymax = scaled_df.values.max()

        ax.vlines(data.index, ymin=ymin, ymax=ymax, colors=colors)
        ax.plot(scaled_df)
        ax.set_title(titles[subplot_number - 1])

    else:

        for df in dfs:

            subplot_number += 1
            data_df = df.iloc[:, 0: -1]

            if normalized:
                scaled_df = (data_df - data_df.min()) / (data_df.max() - data_df.min())
            elif standardized:
                scaled_df = (data_df - data_df.mean()) / data_df.std()
            else:
                scaled_df = data_df

            data = df[df.iloc[:, -1] >= 1]
            if vote_threshold is not None:
                colors = list(['r' if x > vote_threshold else 'k' for x in data['outliers']])
            else:
                colors = None

            if ymin is None:
                ymin = scaled_df.values.min()
            if ymax is None:
                ymax = scaled_df.values.max()

            ax[subplot_number - 1].vlines(data.index, ymin=ymin, ymax=ymax, colors=colors)
            ax[subplot_number - 1].plot(scaled_df)
            ax[subplot_number - 1].set_title(titles[subplot_number - 1])

    plt.show()
    return fig, ax


def box_filter(df, iqr_factor=3):
    '''
    removes outlier using box method
    parameters
    ----------
    df:pandas DataFrame
    iqr_factor : multiplier to inter quartile range
    ----------
    returns dataframe after removing the outliers
    '''
    col_list = df.columns.tolist()
    for i in col_list:
        s = df[i]
        per25 = s.quantile(0.25)
        per50 = s.quantile(0.5)
        per75 = s.quantile(0.75)
        iqr = per75 - per25
        lcl = per50 - iqr_factor * iqr
        ucl = per50 + iqr_factor * iqr
        df = df[df[i] > lcl]
        df = df[df[i] < ucl]

    return df


def median_filter(df, window=5):
    '''
    removing outlier by running median median_filter
    Parameters
    ----------
    df : DataFrame to be filtered
    window: moving window for median filtering

    Return : Filtered Dataframe
    Note: Actual value at given timestamp can change
    '''
    df1 = df.rolling(5, center=True).median()
    df1.ffill(inplace=True)
    df1.bfill(inplce=True)
    return df1


def min_max_filter(df, data_range, fmt='df'):
    '''
    Filters data based on predefined data_range (Min-Max)
    Parameters
    ----------
    df : original DataFrame
    data_range: a dictionary with data_range
               {'tag1': [0,100],
                'tag2': [20,80],
                ............}
    Note that tag1, tag2 are the column names of the dataframe df
    '''
    df_raw = df.copy(deep=True)
    cols = df_raw.columns.tolist()
    if not fmt == 'df':
        for tag in cols:
            df_raw = df_raw.loc[df_raw[tag].between(data_range[tag][0], data_range[tag][1])]
    elif fmt == 'df':
        for tag in cols:
            rng = data_range[tag]
            min_rng = rng['min_rng']
            max_rng = rng['max_rng']
            df_raw = df_raw.loc[df_raw[tag].between(min_rng, max_rng)]

    return df_raw


def data_filter(df, iqr_factor=1.5, window=5, data_range=None, fmt='df', method=None):
    if method == 'median':
        df_out = median_filter(df, window=window)
    elif method == 'min_max':
        df_out = min_max_filter(df, data_range, fmt=fmt)
    elif method == 'box':
        df_out = box_filter(df, iqr_factor=iqr_factor)
    return df_out
