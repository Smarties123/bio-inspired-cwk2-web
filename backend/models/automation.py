import numpy as np
from ..utils import accuracy

class CellularAutomaton:
    """Simple totalistic CA: cell becomes 1 if >= 5 neighbours incl. itself are 1"""
    def __init__(self, steps: int = 10):
        self.steps = steps

    def _step(self, grid):
        padded = np.pad(grid, 1, mode="wrap")
        neigh_sum = sum(np.roll(np.roll(padded, i, 0), j, 1)[1:-1,1:-1]
                        for i in (-1,0,1) for j in (-1,0,1))
        return (neigh_sum >= 5).astype(np.float32)

    def run(self, init):
        frames = [init]
        g = init.copy()
        for _ in range(self.steps):
            g = self._step(g)
            frames.append(g)
        return frames, accuracy(init, g)