import os


def get_number_of_columns(file):
    with open(file, 'r') as f:
        line = f.readline()
    return line.count(',') + 1


def get_number_of_rows(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def get_column_headers(file):

    with open(file, 'r') as f:
        header_line = f.readline()
        column_headers_list = [x.strip() for x in header_line.split(',')]
    return column_headers_list


def delete_all_temp_files(directory, identifying_word):

    files = os.listdir(directory)
    temp_files = [x for x in files if identifying_word in x]
    for file in temp_files:
        os.remove(os.path.join(directory, file))

    print('Successfully deleted all files in "{}" that contained the letters "{}"'.format(directory, identifying_word))