import utils


def find_unique(filename):

    json_list = utils.load_json(filename)
    unsorted_dict_json = {}
    for key in json_list:
        unsorted_dict_json.update(key)

    sorted_list = (sorted(unsorted_dict_json))

    index_list = list(range(len(sorted_list)))
    dict_json = dict(zip(sorted_list, index_list))

    return dict_json


