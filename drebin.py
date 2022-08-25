from ApkDetectO.CDatasetProcessing import CDatasetProcessing
from ApkDetectO.CClassification import CClassification
# import joblib


def main():
    dataset_processor = CDatasetProcessing()
    pr = dataset_processor.process()

    if pr == 1:
        classification = CClassification(dataset_processor.X,
                                         dataset_processor.y)
        classification.run()
        # clf = joblib.load("clf.pkl")


if __name__ == '__main__':
    main()
