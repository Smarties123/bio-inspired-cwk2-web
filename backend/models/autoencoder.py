import torch, torch.nn as nn
from ..utils import accuracy

class FeedforwardAutoencoder(nn.Module):
    def __init__(self, input_dim=256, bottleneck=64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128), nn.ReLU(),
            nn.Linear(128, bottleneck), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(bottleneck, 128), nn.ReLU(),
            nn.Linear(128, input_dim), nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

    def reconstruct(self, pattern):
        self.eval()
        x = torch.from_numpy(pattern.flatten()).float().unsqueeze(0)
        with torch.no_grad():
            recon = self.forward(x).squeeze().reshape(pattern.shape).numpy()
        bin_recon = (recon > 0.5).astype(np.float32)
        return bin_recon, accuracy(pattern, bin_recon)