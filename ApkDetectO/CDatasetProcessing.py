import os
from os import listdir
from os.path import isfile, join
import re
import numpy as np


from ApkDetectO import staticAnalyzer
from Others.settings import WORKING_DIR, DATASET, SAMPLE_TYPES
from Others.utils import save_json, load_json


class CDatasetProcessing:
    """
    The class is responsible for processing a dataset made of .apk files. It makes
    use of a static analyzer to check the presence of different API Calls. After
    that static analysis it generates a vectorized dataset ready to train an ML model.
    """
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
        """
        Looks for apk files inside a specific path.
        :param path: the directory where the apks have to be searched
        :return: the apk list
        """
        apks = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".apk")]
        return apks

    @staticmethod
    def _analyze_apks(apk_list):
        """
        Statically analyze the apk files, looking for API calls etc.
        :param apk_list: the list of apks in the DATASET folder
        :return: None
        """
        for apk in apk_list:
            regex = r"^dataset/(\w*)/(\w*)\.apk$"
            apk_info = re.match(regex, apk)
            apk_type = apk_info.groups()[0]
            apk_name = apk_info.groups()[1]

            staticAnalyzer.run(
                join(DATASET, apk_type, f"{apk_name}.apk"),
                join(WORKING_DIR, apk_type, apk_name)
            )

    def _find_unique(self):
        """
        Create a dictionary with unique features of the dataset
        as keys, and the corresponding index as value.
        :param dataset: json dataset loaded in memory
        :return: dictionary containing {unique feature | index}
        """
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
        """
        Reads each .apk file inside the dataset folder and sends them to the analysis.
        :return: None
        """
        print("Starting to read the apk files...", flush=True)
        apks = []

        for dirpath, _, filenames in os.walk(DATASET):
          for filename in [f for f in filenames if f.endswith(".apk")]:
            apks.append(join(dirpath, filename))
        self._analyze_apks(apks)

    def _create_single_dataset(self):
        """
        Creates a single dataset representation from the static analysis files.
        :return: None
        """
        print("Creating a single dataset.json file from the multiple jsons...\n")
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
        Creates the vector representation of the dataset stored in the class' instance.
        :return: None
        """
        print("Vectorizing the dataset...\n")
        features = self._find_unique()
        save_json("unique_features.json", features)

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
        save_json("vectorized_dataset.json", self.X)
        print(f"# of features: {len(features)}")
        print(f"# of samples: {len(self.X)}")
        self.y = np.array(load_json(self._labels_path))

    def process(self):
        """
        Start the dataset processing routine. If the dataset file
        has already been generated then only the vectorization
        part is executed.
        :return: None
        """
        if self._dataset is None:
            self._read_dataset()
            self._create_single_dataset()

        self._vectorize_dataset()



