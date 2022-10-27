from ApkDetectO.CDatasetProcessing import CDatasetProcessing
from ApkDetectO.CClassification import CClassification


def main():
    dataset_processor = CDatasetProcessing()
    dataset_processor.process()

    classification = CClassification(
        dataset_processor.X,
        dataset_processor.y
    )
    classification.run()


if __name__ == '__main__':
    main()
