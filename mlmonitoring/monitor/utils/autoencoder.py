from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
import numpy as np


# https://i-systems.github.io/teaching/ML/iNotes/15_Autoencoder.html
class MLPRegressorAutoEncoder:
    def __init__(self,
                 layer_sizes=(64, 32, 10),
                 activation='tanh',
                 solver='adam',
                 learning_rate_init=0.0001,
                 max_iter=20,
                 tol=0.0000001,
                 **kwargs):
        self._layer_sizes = layer_sizes
        hidden_layer_sizes = list(layer_sizes) + list(layer_sizes)[:-1][::-1]
        self._regressor = MLPRegressor(
            hidden_layer_sizes=hidden_layer_sizes,
            activation=activation,
            solver=solver,
            learning_rate_init=learning_rate_init,
            max_iter=max_iter,
            tol=tol,
            **kwargs
        )
        self._scaler = MinMaxScaler()
    
    def fit(self, X):
        X = self._scaler.fit_transform(X)
        self._regressor.fit(X, X)
        return self
        
    def encode(self, X):
        X = self._scaler.transform(X)
        encoder = np.asmatrix(X)
        for i in range(len(self._layer_sizes)):
            encoder = encoder * self._regressor.coefs_[i]
            + self._regressor.intercepts_[i]
            encoder = (
                np.exp(encoder) - np.exp(-encoder)
            ) / (np.exp(encoder) + np.exp(-encoder))
        return np.asarray(encoder)
    
    def fit_encode(self, X):
        self._fit(X)
        return self.encode(X)
