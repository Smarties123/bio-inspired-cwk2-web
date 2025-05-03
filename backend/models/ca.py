# backend/models/ca.py
import numpy as np
from ..utils import accuracy

IMG = 28

class WeightedMajorityCA:
    """Retinal-style weighted‐majority cellular automaton."""
    def __init__(self, steps: int = 15, kernel=None, thresh: float = 0.5):
        self.steps = steps
        self.kernel = (kernel if kernel is not None else
                       np.array([[1,2,1],[2,4,2],[1,2,1]], float)/16)
        self.thresh = thresh

    def _step(self, g):
        pad = np.pad(g, 1, mode="wrap")
        out = np.zeros_like(g)
        # vectorized neighborhood sums via convolution-like sliding
        for i in range(IMG):
            for j in range(IMG):
                out[i,j] = (self.kernel * pad[i:i+3,j:j+3]).sum() >= self.thresh
        return out.astype(float)

    def recall(self, x01):
        """Denoise 0–1 vector through repeated CA steps."""
        g = x01.reshape(IMG,IMG)
        for _ in range(self.steps):
            g = self._step(g)
        return g.reshape(-1)

    def run(self, init):
        """Return full frame sequence plus final accuracy against init."""
        x01 = init.astype(float)/255
        frames = [x01]
        g = x01.copy()
        for _ in range(self.steps):
            g = self._step(g)
            frames.append(g)
        final = (g*255).astype(np.uint8)
        return [ (f*255).astype(np.uint8) for f in frames ], accuracy(init, final)
