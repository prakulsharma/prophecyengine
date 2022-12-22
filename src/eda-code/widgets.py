from analysis import *
from outlier_detection import *
import os
from sklearn.ensemble import RandomForestRegressor
from analysis import _find_percent_nulls_per_row


def filter_df_on_column(df: pd.DataFrame, column: str, value1, value2=None, column_type='numeric', filter_type='keep'):
    """
    Filters rows of the DataFrame based on values in a particular column.
    :param df: pandas.DataFrame - DataFrame to be filtered.
    :param column: str - The name of the column to be used for filtering.
    :param value1: any - For numeric columns, this is the start of the range of numbers. For text or boolean columns,
    this is the value that will be matched exactly.
    :param value2: any - For numeric columns only, this is the end of the range of numbers.
    :param column_type: str - The type of column that is being used for filtering. Supports 'numeric', 'text', and
     'boolean'.
    :param filter_type: str - If value is 'keep', the filters retains the values that are matched. Otherwise,
    it removes the matched values.
    :return: pandas.DataFrame - Filtered DataFrame.
    """

    keep = filter_type == 'keep'
    if column not in df.columns.values:
        raise Exception('{} is not a column in the given DataFrame.'.format(column))

    if column_type == 'numeric':
        if value2 is None:
            value2 = value1
        if keep:
            return df[(df[column] >= value1) & (df[column] <= value2)]
        else:
            return df[(df[column] < value1) | (df[column] > value2)]

    elif column_type == 'text' or column_type == 'boolean':
        if keep:
            return df[df[column] == value1]
        else:
            return df[df[column] != value1]

    else:
        raise Exception('Did not understand column_type.')


def column_filter_df(df: pd.DataFrame, columns: list, filter_type='keep'):
    """
    Removes or keeps a list of columns in a DataFrame.
    :param df: pandas.DataFrame - DataFrame whose columns are to be pruned.
    :param columns: list[str] - List of column names to be used for filtering.
    :param filter_type: str - If value is 'keep', the filters retains the columns in 'columns' argument.
    Otherwise, it removes them.
    :return: pandas.DataFrame - DataFrame with the filtered columns.
    """

    keep = filter_type == 'keep'
    if len(columns) == 0:
        raise Exception('Columns list must have at least one element.')

    if keep:
        return df[columns]
    else:
        df = df.drop(columns=columns, axis=1)
        return df


def handle_missing_values_in_df(df, model='interpolate', method=None):
    """
    Fills missing values of rows using dropna. fillna, or interpolate.
    :param df: pandas.DataFrame - DataFrame with the missing rows.
    :param model: str - One out of 'dropna', 'fillna', or 'interpolate'.
    :param method: str - The following options are supported for each value of 'model':
            interpolate ----> 'linear'(default)
            fillna ----> None will add zero for all the values
            fillna ----> ffill (fill forward)
            fillna ----> bfill (fill backward)
            dropna ----> drop the rows with nan
    :return: pandas.DataFrame - DataFrame with missing values handled.
    """

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
    else:
        print('Did not understand model argument. No interpolation done.')
    return df


# Add docstring of plotly later
def visualize_df(df: pd.DataFrame, plot_type='time_series', columns=None, use_column_indices=False, subplots=False,
                 normalized=False, standardized=False, plotly=True, h=700, w=1100, debug=False):
    """
    Visualizes a DataFrame in multiple ways based on arguments.
    :param df: pandas.DataFrame - DataFrame to be visualized.
    :param plot_type: str - Indicates the type of visualization. Supports 'time_series', 'correlation_matrix',
     'distributions', and 'scatter'.
    :param columns: list[str] or list[int] - LIst of column names or indices that should be visualized.
    :param use_column_indices: bool - If True, it assumes that the elements of the "columns" argument are integers
    that represent the column indices. If False, it assumes that the elements of the "columns" argument are string
    column names.
    :param subplots: bool - If True, for visualizations of type 'time_series', each column of the DataFrame will be
    plotted in a separate subplot. If False, all columns are plotted in the same sub-plot.
    :param normalized: bool - If True, data is normalized before plotting.
    :param standardized: bool - If True, data is standardized before plotting.
    :param plotly: pass
    :param h: pass
    :param w: pass
    :param debug: pass
    If normalized and standardized are True, normalization is done and standardization is ignored.
    :return: a fig object

    """
    if not plotly:
        if plot_type == 'time_series':
            plot_time_series(df, columns=columns, use_column_indices=use_column_indices, normalized=normalized,
                             standardized=standardized, subplots=subplots)

        elif plot_type == 'correlation_matrix':
            plot_correlation_matrix(df, columns=columns, use_column_indices=use_column_indices)

        elif plot_type == 'distributions':
            plot_distributions(df, columns=columns, use_column_indices=use_column_indices, subplots=subplots)

        elif plot_type == 'scatter':
            plot_scatter(df, columns=columns, use_column_indices=use_column_indices,
                         normalized=normalized, standardized=standardized)

        else:
            raise Exception('Did not understand plot_type.')
    else:
        if plot_type == 'time_series':
            fig = plot_time_series_plotly(df, columns=columns, normalized=normalized,
                                          standardized=standardized, subplots=subplots, h=h, w=w, debug=debug)

        elif plot_type == 'correlation_matrix':
            fig = plot_correlation_matrix_plotly(df, columns=columns, h=h, w=w, debug=debug)

        elif plot_type == 'distributions':
            fig = plot_distributions_plotly(df, columns=columns, h=h, w=w, debug=debug)

        elif plot_type == 'scatter':
            fig = plot_scatter_plotly(df, columns=columns, normalized=normalized,
                                      standardized=standardized, subplots=subplots, h=h, w=w, debug=debug)

        else:
            raise Exception('Did not understand plot_type.')

    return fig


def run_ensemble(methods: list, df: pd.DataFrame, columns=None, use_column_indices=False,
                 agreement_factor=0.5, outlier_marker_min=None, outlier_marker_max=None, plot=False):
    """
    Runs multiple outlier detection algorithms and combines the results through voting.
    :param methods: list[str] - Names of the methods to be used in the analysis. Supports 'isolation_forest',
    'elliptic_envelope', and 'local_outlier_factor'.
    :param df: pandas.DataFrame - DataFrame that contains the data to be analyzed.
    :param columns: list[str] or list[int] - LIst of column names or indices that should be visualized.
    :param use_column_indices: bool - If True, it assumes that the elements of the "columns" argument are integers
    that represent the column indices. If False, it assumes that the elements of the "columns" argument are string
    column names.
    :param agreement_factor: float - A number > 0.0 and <= 1.0 that indicates the percentage of methods that must agree
    on a datapoint being an outlier for the ensemble to consider it an outlier.
    :param outlier_marker_min: numeric - Outliers are marked with a vertical line on the resultant graph. This argument
    defines the lower end of the outlier marking line position on the graph.
    :param outlier_marker_max: numeric - Outliers are marked with a vertical line on the resultant graph. This argument
    defines the higher end of the outlier marking line position on the graph.


    :return: pandas.DataFrame - DataFrame with the data and the resultant outliers after ensemble combination in an
    addtional column.
    """
    if len(methods) == 0:
        raise Exception('At least one method must be specified in the methods argument')

    result_dfs = []

    if 'isolation_forest' in methods:
        result_dfs.append(isolation_forest(df=df, columns=columns, use_column_indices=use_column_indices, plot=plot,
                                           outlier_marker_min=outlier_marker_min,
                                           outlier_marker_max=outlier_marker_max))

    if 'elliptic_envelope' in methods:
        result_dfs.append(elliptic_envelope(df=df, columns=columns, use_column_indices=use_column_indices, plot=plot,
                                            outlier_marker_min=outlier_marker_min,
                                            outlier_marker_max=outlier_marker_max))

    if 'local_outlier_factor' in methods:
        result_dfs.append(local_outlier_factor(df=df, columns=columns, use_column_indices=use_column_indices, plot=plot,
                                               outlier_marker_min=outlier_marker_min,
                                               outlier_marker_max=outlier_marker_max))

    return create_outlier_detection_ensemble(dfs=result_dfs, agreement_factor=agreement_factor, plot=plot,
                                             outlier_marker_min=outlier_marker_min,
                                             outlier_marker_max=outlier_marker_max)


def remove_outliers_from_df(df: pd.DataFrame):
    """
    Removes rows from a DataFrame that has a column called outliers with binary indication of outlier where 1 is an outlier.
    :param df: pandas.DataFrame - DataFrame with outliers that are marked with a 1 in a column called 'outliers'.
    :return: pandas.DataFrame - DataFrame with outliers removed.
    """

    if 'outliers' not in df:
        raise Exception('DataFrame does not have the required \'outliers\' column.')

    return df[df['outliers'] < 1]


def read_data(data_file, data_type, fmt=None):
    data_path = './user_data/' + str(data_file)
    if str(data_type) == 'Numeric':
        df = read_time_series_csv(data_path, fmt=fmt)
    else:
        df = read_csv_with_mixed_types(data_path, fmt=fmt)

    return df


def chart_difference(raw_df, df, col_list):
    fig, ax1 = plt.subplots(figsize=(20, 10))
    ax1.scatter(raw_df.index, raw_df[col_list])
    ax1.scatter(df.index, df[col_list])
    plt.show()
    return


def data_filter(df, iqr_factor=1.5, window=5, data_range=None, fmt='df', method=None):
    if method == 'median':
        df_out = median_filter(df, window=window)
    elif method == 'min_max':
        df_out = min_max_filter(df, data_range, fmt=fmt)
    elif method == 'box':
        df_out = box_filter(df, iqr_factor=iqr_factor)
    return df_out


def data_hygiene_table(df):
    """

    Parameters
    ----------
    df: Pandas Dataframe

    Returns
    -------
    a dataframe table with df stat and data hygiene report

    """

    df_table = generate_data_hygiene_report(df)
    return df_table


def clean_data(df, raw_data_filename,  # data_fpath = None,
               percent_cols_to_drop=25,
               percent_rows_to_drop=25,
               missing_data_method='interpolation',
               methods=["isolation_forest"]):
    """

    Parameters
    ----------
    df: pandas dataframe
    # data_fpath: data folder directory path, from where raw data is read
    raw_data_filename: filename of raw data
    percent_cols_to_drop: % of missing data above which the column should be dropped
    percent_rows_to_drop: % of missing data above which the row should be dropped
    missing_data_method: list of methods to be used for missing data estimation: fill forward, fill backward,
    interpolation or drop row
    methods: list of methods to be used for outlier detection isolation_forest, elliptic_envelope, local_outlier_factor

    Returns
    -------
    writes the clean data file in data folder with a name ending with  _clean
    returns the data cleaning report dataframe

    """
    hygiene_table = data_hygiene_table(df)
    columns_to_drop = list(hygiene_table[hygiene_table["missing%"] > percent_cols_to_drop].index)
    original_data_columns = df.shape[1]
    original_data_rows = df.shape[0]
    total_nan_count = df.isnull().sum().sum()
    df = df.drop(columns_to_drop, axis=1)
    df = dropped_rows(df, _find_percent_nulls_per_row(df), percent_rows_to_drop)
    if missing_data_method == 'fill_forward':
        df = handle_missing_values_in_df(df, 'fillna', 'ffill')
    elif missing_data_method == 'fill_backward':
        df = handle_missing_values_in_df(df, 'fillna', 'bfill')
    elif missing_data_method == 'drop_na':
        df = handle_missing_values_in_df(df, 'dropna')
    else:
        df = handle_missing_values_in_df(df)

    total_nan_after_clean = df.isnull().sum().sum()
    if "no_outlier_removal" not in methods:
        df = run_ensemble(methods, df)
        df_clean = remove_outliers_from_df(df)
        df_clean.drop(["outliers"], axis=1, inplace=True)
        clean_data_rows = df_clean.shape[0]
        clean_data_columns = df_clean.shape[1]
        outlier_data_points = original_data_rows - clean_data_rows
        outlier_percent = round(outlier_data_points / original_data_rows * 100.0, 1)

    else:
        df_clean = df.copy()
        clean_data_rows = df_clean.shape[0]
        clean_data_columns = df_clean.shape[1]
        outlier_data_points = 0
        outlier_percent = 0.0
    index_list = ['rows', 'columns', 'missing', 'outlier', 'outlier%']
    cleaning_data_report = pd.DataFrame(index=index_list)
    cleaning_data_report['raw data'] = [original_data_rows, original_data_columns,
                                        total_nan_count, outlier_data_points, outlier_percent]
    cleaning_data_report['clean data'] = [clean_data_rows, clean_data_columns,
                                          total_nan_after_clean, 0, 0]
    # raw_data_name = os.path.splitext(raw_data_filename)[0]
    # clean_data_name = raw_data_name + "_clean" + ".csv"
    #
    # clean_data_fpath = os.path.join(data_fpath, clean_data_name)
    # df_clean.to_csv(clean_data_fpath)

    return cleaning_data_report


def feature_importance(df, y_name, method="corr"):
    if method == "corr":
        df_corr = df.corr()
        corr = df_corr[y_name]
        corr_abs = abs(corr[1:])
        corr_abs.sort_values(ascending=False, inplace=True)
        corr_abs20 = corr_abs[:20]
        corr_20 = corr[corr_abs20.index]
        corr_20_sorted = corr_20.sort_values(ascending=False)

        return corr_20_sorted
    elif method == "random_forest":
        y_df = df[y_name]
        x_df = df.drop(y_df.name, axis=1)
        rf = RandomForestRegressor()
        rf.fit(x_df, y_df)
        feature_importance = rf.feature_importances_
        param_names = list(x_df.columns)
        s_fimp = pd.Series(data=feature_importance, index=param_names)
        s_fimp.sort_values(ascending=False, inplace=True)

        return s_fimp


def imp_bar_chart(s_fimp, n, h=700, w=1100):
    s_fimp_10 = s_fimp[:n]
    fig = go.Figure([go.Bar(x=s_fimp_10.index, y=s_fimp_10.values)])
    fig.update_layout(height=h, width=w)

    return fig
