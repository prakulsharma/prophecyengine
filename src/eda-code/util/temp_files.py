import os

temporary_storage_path = '../src/temp'
latest_temp_file_location = None


def get_new_temp_file_location():

    global latest_temp_file_location
    files = os.listdir(temporary_storage_path)
    temp_files = [x for x in files if 'temp' in x]
    if len(temp_files) == 0:
        path = os.path.join(temporary_storage_path, 'temp.0')
        latest_temp_file_location = path
        return path
    serials = [int(x.split('.')[1]) for x in temp_files]
    new_file_location = os.path.join(temporary_storage_path, 'temp.' + str(max(serials) + 1))
    latest_temp_file_location = new_file_location
    return new_file_location


def get_latest_temp_file_location():

    global latest_temp_file_location
    if latest_temp_file_location is None:
        return os.path.join(temporary_storage_path, 'temp.0')
    return str(latest_temp_file_location)


def clean_temp_files():

    # Delete all temporary files
    for file in os.listdir(temporary_storage_path):
        if 'temp' in file:
            os.remove(os.path.join(temporary_storage_path, file))

    global latest_temp_file_location
    latest_temp_file_location = None

