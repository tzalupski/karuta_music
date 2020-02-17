def remove_unwanted_items_from_list(items_list, unwanted_set={'','\n'}):
    items_list = [item for item in items_list if item not in unwanted_set]
    return items_list