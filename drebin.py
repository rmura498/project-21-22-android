import os
from os.path import join

import createSingleDataset
import readDataset
from vectorizeDataset import vectorize_dataset
from settings import DATASET
from utils import load_json


def main():
    dataset_path = join(DATASET, "dataset.json")
    if not os.path.isfile(dataset_path):
        pr = os.fork()
        if pr == 0:
            readDataset.run()
        else:
            cpe = os.wait()
            createSingleDataset.merge_json_files()
            create_vectorized_dataset()
    else:
        create_vectorized_dataset()


def create_vectorized_dataset():
    dataset_path = join(DATASET, "dataset.json")
    dataset = load_json(dataset_path)

    X = vectorize_dataset(dataset)
    print("\n\n1/4 of sample1's vectorized features:\n")
    print(X[1, :X.shape[1] // 4])


if __name__ == '__main__':
    main()
