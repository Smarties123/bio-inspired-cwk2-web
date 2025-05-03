# backend/models/som_knn.py
import numpy as np
from minisom import MiniSom
from ..utils import accuracy

class SOMKNN:
    """SOM + KNN average denoiser."""
    def __init__(self, patterns, m=20, n=20, K=5):
        self.K = K
        self.som = MiniSom(m, n, patterns.shape[1], sigma=4, learning_rate=0.5)
        self.som.random_weights_init(patterns)
        self.som.train_random(patterns, 1000)
        self.codes = self.som.get_weights().reshape(-1, patterns.shape[1])

    def recall(self, x01):
        d = np.linalg.norm(self.codes - x01, axis=1)
        avg = self.codes[np.argsort(d)[:self.K]].mean(0)
        recon = (avg*255).astype(np.uint8)
        return recon, accuracy((x01*255).astype(np.uint8), recon)
