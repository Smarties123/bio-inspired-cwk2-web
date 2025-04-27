import numpy as np
from ..utils import accuracy

class CellularAutomaton:
    """Simple totalistic CA: a cell becomes 1 (black / 255) if ≥ 5 neighbours (incl. itself) are 1."""
    def __init__(self, steps: int = 10):
        self.steps = steps

    def _step(self, grid: np.ndarray) -> np.ndarray:
        # Expect values 0 / 255 (uint8). Convert to 0/1 for counting.
        bin_grid = (grid > 128).astype(np.uint8)
        padded = np.pad(bin_grid, 1, mode="wrap")
        neigh_sum = sum(np.roll(np.roll(padded, i, 0), j, 1)[1:-1, 1:-1]
                         for i in (-1, 0, 1) for j in (-1, 0, 1))
        nxt = (neigh_sum >= 5).astype(np.uint8) * 255
        return nxt

    def run(self, init: np.ndarray):
        frames = [init]
        g = init.copy()
        for _ in range(self.steps):
            g = self._step(g)
            frames.append(g)
        return frames, accuracy(init, g)
