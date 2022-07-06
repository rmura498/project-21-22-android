import staticAnalyzer
from os import listdir
from os.path import isfile, join
from settings import DATASET
from settings import WORKING_DIR

from threading import Thread


def find_apks(path):
    apks = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".apk")]
    return apks


def analyze_apks(apk_list, path="goodware"):
    """
    Create different threads, one for each apk file in the DATASET folder, to analyse it
    with staticAnalyzer.py.
    :param apk_list: the list of apks in the DATASET folder
    :param path: or the type of apk file from which the apks come from
    :return: None
    """
    threads = [Thread(target=staticAnalyzer.run, args=(join(DATASET, path, apk),
                                                       join(WORKING_DIR, path, apk.replace(".apk", ""))))
               for apk in apk_list]
    # start the threads
    for thread in threads:
        thread.start()

def run():
    goodware_path = join(DATASET, "goodware")
    malware_path = join(DATASET, "malware")
    goodwares = find_apks(goodware_path)
    malwares = find_apks(malware_path)

    analyze_apks(goodwares)
    analyze_apks(malwares, "malware")


run()