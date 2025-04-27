# ===== backend/models/hopfield.py =====
import numpy as np
from ..utils import accuracy

class HopfieldNetwork:
    """Binary Hopfield network with Hebbian outer‑product learning."""
    def __init__(self):
        self.W: np.ndarray | None = None  # (N,N)

    def train(self, patterns: list[np.ndarray]):
        if not patterns:
            raise ValueError("Need at least one pattern to train Hopfield network")
        N = patterns[0].size
        self.W = np.zeros((N, N))
        for p in patterns:
            v = p.flatten() * 2 - 1  # map {0,255} → {‑1,+1}
            self.W += np.outer(v, v)
        np.fill_diagonal(self.W, 0)
        self.W /= N

    def recall(self, pattern: np.ndarray, steps: int = 15):
        if self.W is None:
            raise RuntimeError("Hopfield network has not been trained yet")
        v = pattern.flatten() * 2 - 1
        for _ in range(steps):
            v = np.sign(self.W @ v)
        recon = ((v + 1) / 2).reshape(pattern.shape) * 255
        recon = recon.astype(np.uint8)
        return recon, accuracy(pattern, recon)
