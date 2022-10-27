import ujson as json


def load_json(filename):
    """
    Load a .json file.
    :param filename: filename of the json file to load
    :return: json_obj - the loaded json data structure
    """
    with open(filename) as f:
        json_obj = json.load(f)

    return json_obj


def save_json(path, content):
    """
    Save a data structure into a .json file.
    :param path: where to save the json file
    :param content: the content to be saved in the json
    :return: None
    """
    jsonFileName = path
    jsonFile = open(jsonFileName, "w")
    jsonFile.write(json.dumps(content))
    jsonFile.close()
