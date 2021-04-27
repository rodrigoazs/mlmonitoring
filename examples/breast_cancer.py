import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from mlmonitoring import MLmonitoring, Check
from mlmonitoring.monitor.model_drift.feature import (
    scikit_autoencoder_outlier_detection
)

# load breast cancer sample dataset
data = load_breast_cancer()

# define X and y matrices
X = data.data
y = data.target

# separate samples for future prediction
X, X_unseen, y, y_unseen = train_test_split(X, y, train_size=0.7, shuffle=True)

# store cross-validation metrics
metrics = {}

# cross-validation
kf = KFold(n_splits=10)
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # train model
    clf = LogisticRegression(solver='liblinear')
    clf.fit(X_train, y_train)

    # predict test set
    y_pred = clf.predict(X_test)

    # store metrics
    metrics.setdefault('accuracy_score', []).append(accuracy_score(y_test, y_pred))
    metrics.setdefault('precision_score', []).append(precision_score(y_test, y_pred))
    metrics.setdefault('recall_score', []).append(recall_score(y_test, y_pred))
    metrics.setdefault('roc_auc_score', []).append(roc_auc_score(y_test, y_pred))

# calculate mean and st
print("Accuracy score: {:.2f} +/- {:.2f}".format(
    np.mean(metrics['accuracy_score']),
    1.96 * np.std(metrics['accuracy_score'])
))
print("Precision score: {:.2f} +/- {:.2f}".format(
    np.mean(metrics['precision_score']),
    1.96 * np.std(metrics['precision_score'])
))
print("Recall score: {:.2f} +/- {:.2f}".format(
    np.mean(metrics['recall_score']),
    1.96 * np.std(metrics['recall_score'])
))
print("AUC ROC score: {:.2f} +/- {:.2f}".format(
    np.mean(metrics['roc_auc_score']),
    1.96 * np.std(metrics['roc_auc_score'])
))

# train production model
clf = LogisticRegression(solver='liblinear')
clf.fit(X, y)

# predict
y_pred = clf.predict(X_unseen)

# monitoring
monitor = MLmonitoring() \
    .set_connection('http://localhost:8000') \
    .set_project('breast_cancer') \
    .append(
        'feature_outlier',
        scikit_autoencoder_outlier_detection,
        (X, X_unseen),
        low_risk=Check.gt(0.5),
        high_risk=Check.gt(0.8))

# run monitor
monitor.run()
