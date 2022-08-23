from sklearn.utils import shuffle
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn import svm
import numpy as np
import pickle

"""
    Create a module which:
- mix & split the vectorized dataset
- trains a classifier like SVM
- k-fold validation / cross validation (?)
- save the model

"""


def run(X, y):
    X, y = shuffle(X, y)
    clf = GridSearchCV(estimator=svm.SVC(kernel="linear"), param_grid={'C': [0.01, 0.1, 1, 10, 100]})

    splitter = ShuffleSplit(n_splits=5, random_state=100, train_size=0.8)
    acc = np.zeros(shape=(splitter.get_n_splits()))
    for i, (tr_idx, ts_idx) in enumerate(splitter.split(X, y)):
        xtr = X[tr_idx, :]
        ytr = y[tr_idx]
        xts = X[ts_idx, :]
        yts = y[ts_idx]

        clf.fit(xtr, ytr)
        ypred = clf.predict(xts)
        acc[i] = np.mean((ypred == yts))

    print("Hyperparameter estimation (5-fold xval)")
    print("    - Best parameters set found on development set:", clf.best_params_)
    print("    - Grid scores on development set:")
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("        %0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

    print("Mean test accuracy: {:.1%} +/- {:.1%}\n".format(acc.mean(), 2 * acc.std()))
    file_clf = open('clf.obj', 'wb')
    pickle.dump(clf, file_clf)
    file_clf.close()
