import os
from os import listdir
from os.path import isfile, join
from threading import Thread
import numpy as np

from ApkDetectO import staticAnalyzer
from Others.settings import WORKING_DIR, DATASET, SAMPLE_TYPES
from Others.utils import save_json, load_json


class CDatasetProcessing():
    def __init__(self,
                 dataset_path=join(DATASET, "dataset.json"),
                 labels_path=join(DATASET, "labels.json")):
        self.X = None
        self.y = None

        self._dataset_path = dataset_path
        self._labels_path = labels_path

        if os.path.isfile(self._dataset_path):
            self._dataset = load_json(self._dataset_path)
        else:
            self._dataset = None

    @staticmethod
    def _find_apks(path):
        apks = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".apk")]
        return apks

    @staticmethod
    def _analyze_apks(apk_list, path):
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

    def _find_unique(self):
        """
        Create a dictionary with unique features of the dataset
        as keys, and the corresponding index as value.
        :param dataset: json dataset loaded in memory
        :return: dictionary containing {unique feature | index}
        """
        # json_list = load_json(filename)
        unique_features = {}
        for sample in self._dataset:
            unique_features.update(sample)

        unique_features = (sorted(unique_features))

        index_list = list(range(len(unique_features)))
        unique_features = dict(zip(unique_features, index_list))

        return unique_features

    def _get_feature_id(self, features, feature):
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

    def _read_dataset(self):
        samples = list(SAMPLE_TYPES.keys())
        paths = [join(DATASET, samples[0]),
                 join(DATASET, samples[1])]
        for i, path in enumerate(paths):
            apks = self._find_apks(path)
            self._analyze_apks(apks, samples[i])

    def _create_single_dataset(self):
        json_dataset = []
        labels = []

        apk_types = list(SAMPLE_TYPES.keys())
        for type in apk_types:
            cur_path = join(WORKING_DIR, type)
            analyzed_apks = [f for f in listdir(cur_path)]
            label = SAMPLE_TYPES[type]
            for apk_dir in analyzed_apks:
                json_path = join(cur_path, apk_dir, "results")
                json_file = [f for f in listdir(json_path) if isfile(join(json_path, f)) and f.endswith(".json")]
                _json = load_json(join(json_path, json_file[0]))
                json_dataset.append(_json)
                labels.append(label)

        print(json_dataset)
        print(labels)

        save_json(self._dataset_path, json_dataset)
        save_json(self._labels_path, labels)
        self._dataset = load_json(self._dataset_path)

    def _vectorize_dataset(self):
        """
        Create a numpy array for the vectorized dataset
        :param dataset: json dataset loaded in memory
        """
        features = self._find_unique()

        n_samples = len(self._dataset)
        n_features = len(features)
        X = np.zeros([n_samples, n_features])

        for (i, sample) in enumerate(self._dataset):
            for feature in sample:
                f_id = self._get_feature_id(features, feature)
                if f_id == -1:
                    continue
                X[i, f_id] = 1

        self.X = X
        self.y = np.array(load_json(self._labels_path))

    def process(self):
        if self._dataset is None:
            pr = os.fork()
            if pr == 0: # Child
                self._read_dataset()
                return 0
            else:
                cpe = os.wait()
                self._create_single_dataset()
                self._vectorize_dataset()
                return 1

        else:
            self._vectorize_dataset()



