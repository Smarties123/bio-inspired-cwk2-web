import numpy as np
from ..utils import accuracy

class HopfieldNetwork:
    def __init__(self):
        self.W = None  # (N,N)

    def train(self, patterns):
        N = patterns[0].size
        self.W = np.zeros((N,N))
        for p in patterns:
            v = p.flatten()*2-1  # map {0,1}→{‑1,+1}
            self.W += np.outer(v, v)
        np.fill_diagonal(self.W, 0)
        self.W /= N

    def recall(self, pattern, steps=10):
        v = pattern.flatten()*2-1
        for _ in range(steps):
            v = np.sign(self.W @ v)
        recon = ((v+1)/2).reshape(pattern.shape)
        return recon.astype(np.float32), accuracy(pattern, recon)