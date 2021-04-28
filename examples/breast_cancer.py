import numpy as np
import pandas as pd
import logging
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from mlmonitoring import MLmonitoring, Check
from mlmonitoring.monitor.model_drift.feature import (
    psi_drift,
    autoencoder_outlier_detection
)


logging.basicConfig(level=logging.INFO)


def recall_score_monitoring(y_true, y_pred):
    recall = recall_score(y_true, y_pred)
    df = pd.DataFrame(
        [[pd.Timestamp.now(), recall]],
        columns=['timestamp', 'recall']
    ).set_index('timestamp')
    return df.iloc[:, 0]


def perform_monitoring_example():
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
        metrics.setdefault('accuracy_score', []).append(
            accuracy_score(y_test, y_pred)
        )
        metrics.setdefault('precision_score', []).append(
            precision_score(y_test, y_pred)
        )
        metrics.setdefault('recall_score', []).append(
            recall_score(y_test, y_pred)
        )
        metrics.setdefault('roc_auc_score', []).append(
            roc_auc_score(y_test, y_pred)
        )

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

    # feature information
    feature_importances = [abs(coef) / sum(abs(clf.coef_[0])) for coef in clf.coef_[0]]
    feature_names = data.feature_names

    # monitoring
    monitor = MLmonitoring() \
        .set_connection('http://localhost:8000') \
        .set_project('breast_cancer') \
        .append(
            'average_recall',
            recall_score_monitoring,
            param_args=(
                y_unseen,
                y_pred,
            ),
            low_risk=Check.lt(0.95)) \
        .append(
            'feature_outlier',
            autoencoder_outlier_detection,
            param_args=(
                X,
                X_unseen
            ),
            param_kwargs={
                'hidden_neurons': [8, 4, 4, 8],
                'verbose': 0,
            },
            low_risk=Check.gt(0.5),
            high_risk=Check.gt(0.8)) \
        .append(
            'psi_drift',
            psi_drift,
            param_args=(
                X,
                X_unseen,
                feature_names,
                feature_importances))

    # run monitor
    results = monitor.run()
    print(results)


if __name__ == "__main__":
    perform_monitoring_example()
