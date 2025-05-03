# backend/models/hybrid.py
import numpy as np

class HybridHopCaHop:
    """HopfieldPI → WeightedMajorityCA → HopfieldPI."""
    def __init__(self, hop: "HopfieldPseudoInverse", ca: "WeightedMajorityCA"):
        self.hop = hop
        self.ca  = ca

    def recall(self, x01):
        # 1) first PI‐Hop
        r1, _ = self.hop.recall(x01)
        # 2) CA on its output
        c1    = self.ca.recall(r1.astype(float) / 255)
        # 3) PI‐Hop again
        r2, _ = self.hop.recall(c1)
        # r2 here is a flat vector of length 28*28, but your endpoint
        # is expecting a 28×28 image, so you need to reshape it:
        side = int(np.sqrt(r2.size))
        return r2.reshape(side, side)
