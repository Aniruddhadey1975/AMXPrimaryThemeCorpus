def get_values(iterables, key_to_find):
    return list(filter(lambda x:key_to_find in x, iterables))