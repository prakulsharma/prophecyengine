# Convert xls to csv [X]
# Convert time to iso [X]
# Merge time columns together [X]
# Transpose file [X]
# Set time column as index
# Split file into smaller chunks
# Merge files into one
# Convert from long format to wide

# The input and output of any method in this file will be a filename.

import csv
from datetime import datetime

import pandas as pd
import pytz

from util.check_in_out_files import *
from util.temp_files import *
from util.helpers import *


@check_in_out_files
def excel_to_csv(in_file, out_file, sheet_name):
    """
    Converts individual sheets within an XLS or XLSX files to a CSV file.
    :param in_file: str - Path to the file to be converted.
    :param out_file: str - Path where the resultant CSV file should be created.
    :param sheet_name: str - The name of the sheet within the XLS or XLSX file that should be converted.
    :return: Nothing.
    """

    df = pd.read_excel(in_file, sheet_name=sheet_name)
    df.to_csv(out_file, index=False)

    print('Successfully converted excel file to csv - Output available at {}'.format(out_file))


@check_files_for_merge
def merge_normalized_csv_files(in_files: list, out_file):
    """
    Merges multiple DataFrames using an outer join on the timestamp column.
    :param in_files: list - List of paths to the csv files to be merged.
    :param out_file: str - Path where the new merged file should be created.
    :return: Nothing
    """
    dfs = []
    for file in in_files:
        df = pd.read_csv(file)
        df.set_index('timestamp', drop=True, inplace=True)
        dfs.append(df)

    out_df = pd.concat(dfs, axis=1)

    out_df.to_csv(out_file, index_label='timestamp')


@check_in_out_files
def delete_empty_rows(in_file, out_file):
    """
    Deletes empty rows from a CSV file.
    :param in_file: str - Path to the file with empty rows.
    :param out_file: str - Path where the new file without empty rows should be created.
    :return: Nothing.
    """

    _delete_empty_rows(in_file, out_file)
    clean_temp_files()
    print('Successfully removed empty rows - Output available at {}'.format(out_file))


@check_in_out_files
def delete_rows_and_columns(in_file, out_file, columns_to_delete, rows_to_delete):
    """
    Deletes specific rows and/or columns from a CSV file.
    :param in_file: str - Path to the file with the rows and/or columns to delete.
    :param out_file: str - Path where the new file without the specified rows and/or columns should be created.
    :param columns_to_delete: list - List of column indices that should be deleted.
    :param rows_to_delete: list - List of row indices that should be deleted.
    :return: Nothing.
    """

    _delete_rows_and_columns(in_file, out_file, columns_to_delete, rows_to_delete)
    clean_temp_files()
    print('Successfully deleted rows and columns - Output available at {}'.format(out_file))


@check_in_out_files
def transpose_csv_file(in_file, out_file, transpose_chunksize=1000):
    """
    Transposes a CSV file
    :param in_file: str - Path to the file that should be transposed.
    :param out_file: str - Path where the new transposed file should be created.
    :param transpose_chunksize: int - In order to avoid situations where large CSV files are loaded into
    limited available memory, a chunksize can be given to operate on the given file in smaller chunks. This number
    denotes the number of rows that will be used in each chunk during the transpose operation.
    :return: Nothing.
    """

    n_cols = get_number_of_columns(in_file)
    if transpose_chunksize <= 0:
        transpose_chunksize = 1000

    for x in range(0, n_cols, min(n_cols, transpose_chunksize)):
        chunk = pd.read_csv(in_file,
                            usecols=range(x, min(n_cols, x + transpose_chunksize)),
                            index_col=False,
                            header=None)
        chunk = chunk.transpose()
        chunk.to_csv(out_file, mode='a', index=False, header=False)

    print('Successfully transposed csv file - Output available at {}'.format(out_file))


@check_in_out_files
def add_header(in_file, out_file, header):
    """
    Adds a header to a CSV file
    :param in_file: str - Path to the file to which a header needs to be added.
    :param out_file: str - Path where the new file with the added header should be created.
    :param header: list - A list of column names that constitute the header that needs to be added.
    :return: Nothing.
    """

    # Check number of columns in header and in the file
    n = get_number_of_columns(file=in_file)
    l = len(header)

    if n != l:
        raise ValueError('The number of headers does not match the number of columns in the file.')

    # Add header
    with open(in_file, 'r') as source:
        reader = csv.reader(source)
        with open(out_file, 'w') as destination:
            writer = csv.writer(destination)
            writer.writerow(header)
            for row in reader:
                writer.writerow(row)

    print('Successfully added header - Output available at {}'.format(out_file))


@check_in_out_files
def normalize_timestamps(in_file, out_file, time_column_names, time_column_formats, timezone):
    """
    Converts one or more columns with datetime information into a normal form (YYYY-MM-DDTHH:MM:SS).
    :param in_file: str - Path to the file with the unnormalized datetime columns.
    :param out_file: str - Path where the new file with the normalized timestamp column should be created.
    :param time_column_names: list - List of column names in the in_file that should be used to create a normalized timestamp.
    :param time_column_formats: list - List of strptime formats for each column mentioned in time_column_names.
    :param timezone: str - The timezone in which the time information in in_file is represented.
    Valid timezone strings can be found here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones under the
    column called TZ database name. For example: Asia/Kolkata.
    :return: Nothing.
    """

    temp_out_file = _delete_empty_rows(in_file, get_new_temp_file_location())

    # Combine all time columns and formats
    time_df = pd.read_csv(get_latest_temp_file_location(), usecols=time_column_names, dtype=str)
    combined_time = time_df[time_column_names].apply(lambda x: ' '.join(x), axis=1)
    combined_format = ' '.join(time_column_formats)

    # Convert the combined time columns using the combined format
    datetime_combined = [datetime.strptime(x, combined_format) for x in combined_time]

    # If datetime is timezone unaware, add timezone
    d = datetime_combined[0]
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        if timezone is not None:
            try:
                tz = pytz.timezone(timezone)
            except Exception as e:
                print('Timezone could not be found or is invalid. Assuming UTC and ingesting data. '
                      'Error - {}'.format(e.__str__()))
                tz = pytz.utc
        else:
            tz = pytz.utc
        datetime_combined = [tz.localize(x) for x in datetime_combined]

    # Convert to iso format and add a column header 'datetime'
    datetime_column = [x.isoformat() for x in datetime_combined]
    datetime_column.insert(0, 'timestamp')

    # Delete the existing time columns
    time_column_indices = [get_column_headers(in_file).index(x) for x in time_column_names]
    temp_out_file = _delete_rows_and_columns(temp_out_file, get_new_temp_file_location(), time_column_indices, [])

    # Add a new timestamp column in iso format
    with open(temp_out_file, 'r') as r:
        with open(out_file, 'a') as w:
            i = -1
            for line in r:
                i += 1
                w.write(datetime_column[i] + ',' + line)

    clean_temp_files()
    print('Successfully normalized timestamps - Output available at {}'.format(out_file))


@check_in_out_files
def apply_tag_map(in_file, out_file, tag_map, time_columns, strict):
    """
    Uses a dictionary map to change column names of a CSV file.
    :param in_file: str - Path to the file whose column names needs to be mapped.
    :param out_file: str - Path where the new file with the new column names should be created.
    :param tag_map: dict - Python dictionary with the format <existing_column_name> : <new_column_name>.
    :param time_columns: list - List of columns that have time information. This is needed so that when strict = True,
    we don't delete the columns with the time information from the file.
    :param strict: bool - If True, resulting file will only have the columns in the tag_map dictionary.
    :return: Nothing.
    """
    with open(in_file, 'r') as f:

        header_line = f.readline()
        tags_list = [x.strip() for x in header_line.split(',')]

        if strict:

            indices = []
            for key, value in tag_map.items():
                try:
                    index = tags_list.index(key)
                    if value is not None:
                        indices.append(index)
                        tags_list[index] = value
                except ValueError:
                    continue
            for column_name in time_columns:  # Ensure time columns don't get removed during strict application
                try:
                    index = tags_list.index(column_name)
                    indices.append(index)
                except ValueError:
                    continue

            indices = sorted(indices)
            tags_list = [tags_list[i] for i in indices]

        else:
            for key, value in tag_map.items():
                try:
                    tags_list[tags_list.index(key)] = value
                except ValueError:
                    continue

        with open(out_file, 'a') as n:
            n.write(','.join(tags_list) + os.linesep)
            for line in f:
                if strict:  # Drop columns that have been removed by strict application
                    values = [x.strip() for x in line.split(',')]
                    new_line = ','.join([values[i] for i in indices])
                    n.write(new_line + '\n')
                else:
                    n.write(line)

    return tags_list


# Private methods


def _delete_empty_rows(in_file, out_file):
    with open(in_file, 'r') as r:
        with open(out_file, 'a') as w:
            for line in r:
                check_line = line.replace(',', '').replace("\n", '').strip()
                if len(check_line) > 1:
                    w.write(line)
    return out_file


def _delete_rows_and_columns(in_file, out_file, columns_to_delete, rows_to_delete):

    with open(in_file, 'r') as source:
        reader = csv.reader(source)
        row_column_deleted_file = out_file
        with open(row_column_deleted_file, 'w') as destination:
            writer = csv.writer(destination)
            i = -1
            for row in reader:
                i += 1
                if i not in rows_to_delete:
                    new_row = [row[x] for x in range(0, len(row)) if x not in columns_to_delete]
                    writer.writerow(new_row)
    return out_file


def _parse_timestamp_spec(self):

    timestamp_spec = self.spec.get('timestamp_spec', None)
    if timestamp_spec is None:
        raise ValueError('\'timestamp_spec\' not found.')

    time_columns = timestamp_spec.get('columns', None)
    if time_columns is None:
        raise ValueError('\'columns\' not found in \'timestamp_spec\'.')
    if len(time_columns) == 0:
        raise ValueError('Length of \'columns\' in \'timestamp_spec\' is zero.')

    column_names = [x.get('name', None) for x in time_columns]
    column_formats = [x.get('format', None) for x in time_columns]
    if any(x is None for x in column_names):
        raise ValueError('One or more column names is empty in \'timestamp_spec\'.')
    if any(x is None for x in column_formats):
        raise ValueError('One or more column formats is empty in \'timestamp_spec\'.')

    timezone = timestamp_spec.get('timezone', None)

    return column_names, column_formats, timezone
