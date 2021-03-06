from pyod.models.auto_encoder import AutoEncoder
from pyod.models.pca import PCA
from mlmonitoring.monitor.utils import _calculate_psi
import numpy as np
import pandas as pd


def psi_drift(X_train, X_test, feature_names, feature_importances, **kwargs):
    X_train, X_test = np.array(X_train), np.array(X_test)
    drift = [_calculate_psi(
        X_train[:, i], X_test[:, i],
        **kwargs, axis=1)
        for i in range(X_train.shape[1])]
    result = list(map(list, zip(feature_names, feature_importances, np.array(drift))))
    result = pd.DataFrame(result, columns=['feature', 'importance', 'psi'])
    return result


def pca_outlier_detection(X_train, X_test, **kwargs):
    detector = PCA(**kwargs)
    detector.fit(X_train)
    prob = detector.predict_proba(X_test)[:, -1]

    if isinstance(X_test, pd.DataFrame):
        return pd.Series(prob, name='outlier', index=X_test.index)
    return pd.Series(prob, name='outlier')


def autoencoder_outlier_detection(X_train, X_test, **kwargs):
    detector = AutoEncoder(**kwargs)
    detector.fit(X_train)
    prob = detector.predict_proba(X_test)[:, -1]

    if isinstance(X_test, pd.DataFrame):
        return pd.Series(prob, name='outlier', index=X_test.index)
    return pd.Series(prob, name='outlier')
