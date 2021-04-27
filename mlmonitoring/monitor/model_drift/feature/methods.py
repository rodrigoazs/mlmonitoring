from pyod.models.auto_encoder import AutoEncoder
from pyod.models.pca import PCA
from sparkle.monitor.utils import _calculate_psi
import numpy as np


def psi_drift(X_train, X_test, **kwargs):
    X_train, X_test = np.array(X_train), np.array(X_test)
    drift = [_calculate_psi(
        X_train[:, i], X_test[:, i],
        **kwargs, axis=1)
        for i in range(X_train.shape[1])]
    return np.array(drift)


def pca_outlier_detection(X_train, X_test, **kwargs):
    detector = PCA(**kwargs)
    detector.fit(X_train)
    return detector.predict_proba(X_test)[:, -1]


def autoencoder_outlier_detection(X_train, X_test, verbose=0, **kwargs):
    detector = AutoEncoder(verbose=0, **kwargs)
    detector.fit(X_train)
    return detector.predict_proba(X_test)[:, -1]
