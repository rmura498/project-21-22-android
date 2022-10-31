from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve, roc_auc_score

import numpy as np
import matplotlib.pyplot as plt
import joblib


class CClassification:
    """
    The class is responsible for training an ML model for classifying apk files.
    The chosen model is a LinearSVC. A grid search approach is used to
    find the best parameters for the classifier. After that the accuracy
    is computed as well as the ROC curve and the AUC metric, to evaluate the
    classifier's performance.
    """

    def __init__(self, X=None, y=None, test_size=0.2):
        self._X = X
        self._y = y
        self._clf = None
        self._estim = svm.LinearSVC(penalty="l1", dual=False)


        self._test_size = test_size
        self._xtr = None
        self._ytr = None
        self._xts = None
        self._yts = None

    def _shuffle_split(self):

        '''
        Shuffles and splits the dataset into train and test set.
        :return: None
        '''
        self._X, self._y = shuffle(self._X, self._y)
        self._xtr, self._xts, self._ytr, self._yts = train_test_split(
            self._X,
            self._y,
            test_size=self._test_size,
            random_state=77
        )

    def fit_model(self):
        """
        Takes the given estimator and performs a grid search to find the
        best parameters for the model to fit the dataset.
        :return: None
        """
        self._clf = GridSearchCV(
            estimator=self._estim,
            param_grid={'C': [0.01, 0.1, 1, 10, 100]},
        )

        self._clf.fit(self._xtr, self._ytr)

    def roc_score(self):
        """
        Computes the AUC (area under the curve) of the trained model.
        It also creates a plot of the ROC curve, and it saves it locally.
        :return: None
        """
        y_pred = self._clf.decision_function(self._xts)
        auc = roc_auc_score(self._yts, y_pred)
        print('SVM AUC = %.3f' % auc)
        fpr, tpr, _ = roc_curve(self._yts, y_pred)
        plt.plot(fpr, tpr, marker='.', label='SVM (AUC = %0.3f)' % auc)
        plt.title("ROC Curve")
        plt.xlabel("False positive rate")
        plt.ylabel("True positive rate")
        plt.savefig("roc_curve.png")
        plt.close()


    def predict_and_evaluate(self):
        """
        Performs a prediction using the test set to compute the
        accuracy of the model and then the AUC.
        :return: None
        """
        y_pred = self._clf.predict(self._xts)
        acc = np.mean((y_pred == self._yts))

        print(f"Hyperparameter estimation (5-fold xval)\n"
              f"\t- Best parameters set found on development set: {self._clf.best_params_}\n"
              f"\t- Grid scores on development set:")
        means = self._clf.cv_results_['mean_test_score']
        stds = self._clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, self._clf.cv_results_['params']):
            print("\t\t\t%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

        print("Mean test accuracy: {:.1%} +/- {:.1%}\n".format(acc.mean(), 2 * acc.std()))

        self.roc_score()

    def save_model(self, name="clf"):
        joblib.dump(self._clf.best_estimator_, f"{name}.pkl")

    def run(self):
        """
        Run the entire classification and (model) evaluation routine.
        :return: None
        """
        self._shuffle_split()
        self.fit_model()
        self.predict_and_evaluate()
        self.save_model()
        