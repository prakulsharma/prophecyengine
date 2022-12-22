# Remove empty columns
# Remove empty rows
# Remove specified columns
# Remove specified rows
# Remove data between time range
# Interpolate missing data points
# Convert column data based on a mapping
# Replace text in specified columns or all
# Standardize data in specified columns or all
# Normalize data in specified columns or all
# Create derived columns
# Split data based on time-range
# Split data based on specified columns
# Tag mapping [X]

# The input and output of any method in this file will be a DataFrame.

import pandas as pd
import datetime

def apply_tag_map_to_df(df: pd.DataFrame, tag_map: dict, strict=False):
    """
    Uses a dictionary map to change column names of a DataFrame.
    :param df: pandas.DataFrame - DataFrame whose columns need to be changed.
    :param tag_map: dict - Python dictionary with the format <existing_column_name> : <new_column_name>.
    :param strict: bool - If True, resulting DataFrame will only have the columns in the tag_map dictionary.
    :return: pandas.DataFrame - DataFrame with the new column names.
    """

    if strict:
        df = df.loc[:, df.columns.isin(list(tag_map.keys()))]

    df.rename(columns=tag_map, inplace=True)
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
        if isinstance(ed, datetime.datetime):
            ed_dt = ed
        else:
            ed_dt = pd.datetime(ed[0], ed[1], ed[2], ed[3], ed[4], ed[5])
        df_cut = df[df.index <= ed_dt]
    elif sd is not None and ed is None:
        if isinstance(sd, datetime.datetime):
            sd_dt = sd
        else:
            sd_dt = pd.datetime(sd[0], sd[1], sd[2], sd[3], sd[4], sd[5])
        df_cut = df[df.index >= sd_dt]
    elif sd is not None and ed is not None:
        if isinstance(ed, datetime.datetime):
            ed_dt = ed
        else:
            ed_dt = pd.datetime(ed[0], ed[1], ed[2], ed[3], ed[4], ed[5])
        if isinstance(sd, datetime.datetime):
            sd_dt = sd
        else:
            sd_dt = pd.datetime(sd[0], sd[1], sd[2], sd[3], sd[4], sd[5])
        if sd_dt >= ed_dt:
            raise Exception('start date is larger than end date')
        df_cut = df[(df.index <= ed_dt) & (df.index >= sd_dt)]
    elif sd is None and ed is None:
        df_cut = df
    return df_cut


def slice_df_by_time_range(df: pd.DataFrame, start_time, end_time):
    """
    Slices a normalized dataframe using the 'timestamp' column between the parameters start_time and end_time.
    :param df: pandas.DataFrame - DataFrame that needs to be sliced
    :param start_time: str - Timestamp that indicates the beginning of the time-range for which data is required. It
    must be inferable by pandas.datetime().
    :param end_time: str - Timestamp that indicates the end of the time-range for which data is required. It must be
    inferable by pandas.datetime().
    :return: pandas.DataFrame - The sliced DataFrame
    """

    start_timestamp = pd.to_datetime(start_time, infer_datetime_format=True)
    end_timestamp = pd.to_datetime(end_time, infer_datetime_format=True)

    return df[(df.index >= start_timestamp) & (df.index <= end_timestamp)]


def convert_df_to_numeric(df: pd.DataFrame, drop_non_numeric_columns=True):
    """
    Converts all values in a DataFrame to numeric if possible.
    :param df: pandas.DataFrame - DataFrame with non-numeric columns.
    :param df: bool - If True, all fully non-numeric columns will be removed from resulting DataFrame.
    :return: pandas.DataFrame - DataFrame with non-numeric columns removed.
    """
    df = df.apply(pd.to_numeric, errors='coerce')
    if drop_non_numeric_columns:
        return df.dropna(axis=1, how='all')
    else:
        return df
