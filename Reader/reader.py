def get_list_from_file(path):
    list_from_file = []
    with open(path) as input_file:
        list_from_file = input_file.read()
    return list_from_file.split('\n')