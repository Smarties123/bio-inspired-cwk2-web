# ===== backend/models/autoencoder.py =====
import numpy as np
import torch, torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from ..utils import accuracy

class FeedforwardAutoencoder(nn.Module):
    """Tiny fully‑connected auto‑encoder for 28×28 images.
    The network is *not* meant to beat SOTA – just to give a differentiable baseline."""
    def __init__(self, input_dim: int = 784, bottleneck: int = 128):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256), nn.ReLU(),
            nn.Linear(256, bottleneck), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(bottleneck, 256), nn.ReLU(),
            nn.Linear(256, input_dim), nn.Sigmoid()
        )

    # ---- required by nn.Module ----
    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        z = self.encoder(x)
        return self.decoder(z)

    # ---- convenience helpers ----
    @torch.no_grad()
    def reconstruct(self, pattern: np.ndarray):
        self.eval()
        x = torch.from_numpy(pattern.astype(np.float32) / 255).flatten().unsqueeze(0)
        recon = self(x).squeeze().mul(255).clamp(0, 255).cpu().numpy().reshape(pattern.shape).astype(np.uint8)
        return recon, accuracy(pattern, recon)

    def train_on(self, patterns: list[np.ndarray], epochs: int = 5, batch_size: int = 32):
        """A very quick on‑start training so the demo works out‑of‑the‑box.
        For a real project you would pre‑train offline and just load the weights."""
        if not patterns:
            return
        X = np.stack([p.flatten() for p in patterns]).astype(np.float32) / 255
        loader = DataLoader(TensorDataset(torch.from_numpy(X)), batch_size=batch_size, shuffle=True)
        opt = torch.optim.Adam(self.parameters(), lr=1e-3)  # ← ASCII minus!
        bce  = nn.BCELoss()
        self.train()
        for _ in range(epochs):
            for (batch,) in loader:
                opt.zero_grad()
                out = self(batch)
                loss = bce(out, batch)
                loss.backward()
                opt.step()

