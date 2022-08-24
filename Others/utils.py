import ujson as json


def load_json(filename):
    # Load JSON file
    with open(filename) as f:
        json_obj = json.load(f)

    return json_obj


def save_json(path, content):
    jsonFileName = path
    jsonFile = open(jsonFileName, "a+")
    jsonFile.write(json.dumps(content))
    jsonFile.close()
