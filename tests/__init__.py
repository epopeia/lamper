from collections import namedtuple

def dict_to_namedtuple(dictionary):
    for key, value in dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = dict_to_namedtuple(value)
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)
