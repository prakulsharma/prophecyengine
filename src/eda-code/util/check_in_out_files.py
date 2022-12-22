import os


def check_in_out_files(method):

    def check(*args, **kwargs):

        if 'in_file' in kwargs:
            in_file = kwargs['in_file']
            out_file = kwargs['out_file']
        else:
            in_file = args[0]
            out_file = args[1]

        if in_file is None or out_file is None:
            raise Exception('in_file and out_file cannot be None.')

        if type(in_file) != str or type(out_file) != str:
            raise Exception('in_file and out_file must be strings.')

        if in_file.strip() == '' or out_file.strip() == '':
            raise Exception('in_file and out_file cannot be empty.')

        if in_file == out_file:
            raise Exception('in_file and out_file cannot be the same.')

        if os.path.exists(out_file):
            raise Exception('{} already exists and cannot be overwritten.'.format(out_file))

        method(*args, **kwargs)

    return check


def check_files_for_merge(method):

    def check(*args, **kwargs):

        if 'in_files' in kwargs:
            in_files = kwargs['in_files']
            out_file = kwargs['out_file']
        else:
            in_files = args[0]
            out_file = args[1]

        if in_files is None or out_file is None:
            raise Exception('in_files and out_file cannot be None.')

        if type(in_files) != list or not all(type(x) == str for x in in_files):
            raise Exception('in_files must be a list of strings.')

        if len(in_files) <= 1:
            raise Exception('2 or more in_files must be provided.')

        if type(out_file) != str:
            raise Exception('out_file must be a string.')

        if any(x.strip() == '' for x in in_files) or out_file.strip() == '':
            raise Exception('in_files and out_file cannot be empty strings.')

        if any(x == out_file for x in in_files):
            raise Exception('Any of the in_files and out_file cannot be the same.')

        if os.path.exists(out_file):
            print('{} already exists and cannot be overwritten. Skipping merge.'.format(out_file))
            return

        method(*args, **kwargs)

    return check
