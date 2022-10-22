from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import joblib
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV


class CClassification():
    def __init__(self, X=None, y=None, test_size=0.2):
        self._X = X
        self._y = y
        self._clf = None

        self._test_size = test_size
        self._xtr = None
        self._ytr = None
        self._xts = None
        self._yts = None

    def _shuffle_split(self):
        self._X, self._y = shuffle(self._X, self._y)
        self._xtr, self._xts, self._ytr, self._yts = train_test_split(
            self._X,
            self._y,
            test_size=self._test_size,
            random_state=77
        )

    def run(self):
        self._shuffle_split()

        clf = GridSearchCV(
            estimator=svm.SVC(kernel="linear"),
            param_grid={'C': [0.01, 0.1, 1, 10, 100]},
        )

        clf.fit(self._xtr, self._ytr)
        y_pred = clf.predict(self._xts)
        acc = np.mean((y_pred == self._yts))

        print(f"Hyperparameter estimation (5-fold xval)\n"
              f"\t- Best parameters set found on development set: {clf.best_params_}\n"
              f"\t- Grid scores on development set:")
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("\t\t\t%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

        print("Mean test accuracy: {:.1%} +/- {:.1%}\n".format(acc.mean(), 2 * acc.std()))
        
        joblib.dump(self._clf.best_estimator_, "clf.pkl")

    def roc_score(self):
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

