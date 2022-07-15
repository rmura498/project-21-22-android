from settings import DATASET
from utils import load_json

from os.path import join
import numpy as np


def find_unique(dataset):
    """
    Create a dictionary with unique features of the dataset
    as keys, and the corresponding index as value.
    :param dataset: json dataset loaded in memory
    :return: dictionary containing {unique feature | index}
    """
    # json_list = load_json(filename)
    unique_features = {}
    for sample in dataset:
        unique_features.update(sample)

    unique_features = (sorted(unique_features))

    index_list = list(range(len(unique_features)))
    unique_features = dict(zip(unique_features, index_list))

    return unique_features


def get_feature_id(features, feature):
    """
    Retrieve the feature id from a dictionary of unique features (with
    keys as the features, and values the corresponding id).
    :param features: unique features dictionary from a dataset
    :param feature: the feature you want to get the id
    :return: feature_id, -1 if an error occurred (the feature is not present)
    """
    feature_id = -1
    try:
        feature_id = features[feature]
    except KeyError:
        print(f"There's no such feature: {feature}")

    return feature_id


def vectorize_dataset(dataset):
    """
    Create a numpy array for the vectorized dataset
    :param dataset: json dataset loaded in memory
    :return: numpy array of vectorized dataset
    """
    features = find_unique(dataset)

    n_samples = len(dataset)
    n_features = len(features)
    X = np.zeros([n_samples, n_features])

    for (i, sample) in enumerate(dataset):
        for feature in sample:
            f_id = get_feature_id(features, feature)
            if f_id == -1:
                continue
            X[i, f_id] = 1

    return X


def main():
    dataset_path = join(DATASET, "dataset.json")
    dataset = load_json(dataset_path)

    unique_features = find_unique(dataset)
    X = vectorize_dataset(dataset, unique_features)
    print("1/4 of sample1's vectorized features")
    print(X[1, :X.shape[1] // 4])

    # test on feature 1 of first sample of the dataset
    feature0 = list(dataset[0].keys())[1]
    print("Feature 1 of the first sample of the dataset: ", feature0)
    id_f = unique_features[feature0]
    print("Id of feature 1: ", unique_features[feature0])
    print("Features of first sample:\n",  dataset[0].keys())
    print("Is feature 1 set to 1 in the array? ", X[0, id_f] == 1)


if __name__ == '__main__':
    main()
