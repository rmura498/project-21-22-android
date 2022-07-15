import os
from os.path import join
from settings import WORKING_DIR, SAMPLE_TYPES


def clean_static_dir():
    goodware_path = join(WORKING_DIR, list(SAMPLE_TYPES.keys())[0])
    malware_path = join(WORKING_DIR, list(SAMPLE_TYPES.keys())[1])
    paths = [goodware_path, malware_path]

    os.system("rm -rf " + WORKING_DIR)
    os.system("mkdir " + WORKING_DIR)
    for path in paths:
        os.system("mkdir " + path)


if __name__ == '__main__':
    clean_static_dir()