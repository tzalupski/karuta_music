import helper

def get_list_from_file(path):
    list_from_file = _open_file_and_get_list(path)
    list_from_file = helper.remove_unwanted_items_from_list(path)
    return list_from_file



def _open_file_and_get_list(path):
    list_from_file = []
    with open(path) as input_file:
        data_from_file = input_file.read()
        list_from_file = data_from_file.split('\n')
    return list_from_file

