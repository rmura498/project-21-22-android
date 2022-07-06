from utils import save_json, load_json
from os import listdir
from os.path import join, isfile

from settings import WORKING_DIR, malware_goodware


def merge_json_files(path=WORKING_DIR):
    json_dataset = []
    labels = []

    apk_types = [f for f in listdir(path)]
    for type in apk_types:
        cur_path = join(WORKING_DIR, type)
        analyzed_apks = [f for f in listdir(cur_path)]
        label = malware_goodware[type]
        for apk_dir in analyzed_apks:
            json_path = join(cur_path, apk_dir, "results")
            json_file = [f for f in listdir(json_path) if isfile(join(json_path, f)) and f.endswith(".json")]
            _json = load_json(join(json_path, json_file[0]))
            json_dataset.append(_json)
            labels.append(label)

    print(json_dataset)
    print(labels)

    save_json(join(WORKING_DIR, "dataset.json"), json_dataset)
    save_json(join(WORKING_DIR, "labels.json"), labels)


