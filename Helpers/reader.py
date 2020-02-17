def get_list_from_file(path):
    list_from_file = []
    with open(path) as input_file:
        data_from_file = input_file.read()
        list_from_file = data_from_file.split('\n')
    try:
        list_from_file.remove('')
    except:
        pass
    return list_from_file