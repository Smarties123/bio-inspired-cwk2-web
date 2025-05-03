# backend/models/hopfield_pi.py
import numpy as np
from ..utils import accuracy

class HopfieldPseudoInverse:
    """Hopfield net with pseudo-inverse learning."""
    def __init__(self, patterns):
        P = (patterns*2-1)              # to ±1
        C = P @ P.T
        W = P.T @ np.linalg.inv(C) @ P
        np.fill_diagonal(W, 0)
        self.W = W / patterns.shape[0]

    def recall(self, x01, steps:int=15):
        x = x01*2-1
        N = x.size
        for _ in range(steps):
            for i in np.random.permutation(N):
                x[i] = 1 if self.W[i] @ x >= 0 else -1
        recon01 = (x+1)/2
        return (recon01*255).astype(np.uint8), accuracy((x01*255).astype(np.uint8), (recon01*255).astype(np.uint8))
