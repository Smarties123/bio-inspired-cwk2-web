from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from torchvision import datasets, transforms

from backend.utils import b64_to_array, array_to_b64, add_noise
from backend.models.automation import CellularAutomaton
from backend.models.hopfield import HopfieldNetwork
from backend.models.autoencoder import FeedforwardAutoencoder

app = FastAPI(title="Bio‑Inspired Recall API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- request/response schemas -----
class ImageReq(BaseModel):
    image: str  # base64 PNG
    noise: float = 0.0  # 0–100

class ReconResp(BaseModel):
    reconstructed: str
    accuracy: float

class CAResp(ReconResp):
    frames: list[str]

# ----- instantiate models and *pre‑train* on 10 MNIST digits -----
ca  = CellularAutomaton(steps=15)
hop = HopfieldNetwork()
ae  = FeedforwardAutoencoder()


def _load_mnist_samples():
    tf = transforms.ToTensor()
    ds = datasets.MNIST(root="/tmp", train=False, download=True, transform=tf)
    picked: dict[int, np.ndarray] = {}
    for img, label in ds:
        if label not in picked:
            arr = (img.squeeze(0).numpy() * 255).astype("uint8")  # 28×28
            picked[label] = arr
        if len(picked) == 10:
            break
    return picked

_samples_dict = _load_mnist_samples()
_samples       = list(_samples_dict.values())

# --- train Hopfield & AE so the demo has something to recall ---
hop.train(_samples)
ae.train_on(_samples, epochs=15)

# --- expose sample images to the frontend ---
mnist_samples_b64 = {str(k): array_to_b64(v) for k, v in _samples_dict.items()}

# ---------------------- API ----------------------
@app.post("/generate_noise", response_model=ReconResp)
def generate_noise(req: ImageReq):
    arr   = b64_to_array(req.image)
    noisy = add_noise(arr, req.noise)
    return {"reconstructed": array_to_b64(noisy), "accuracy": 0}

@app.post("/run_ca", response_model=CAResp)
def run_ca(req: ImageReq):
    init   = b64_to_array(req.image)
    noisy  = add_noise(init, req.noise)
    frames, acc = ca.run(noisy)
    return {
        "reconstructed": array_to_b64(frames[-1]),
        "accuracy": acc,
        "frames": [array_to_b64(f) for f in frames],
    }

@app.post("/run_hopfield", response_model=ReconResp)
def run_hopfield(req: ImageReq):
    init  = b64_to_array(req.image)
    noisy = add_noise(init, req.noise)
    recon, acc = hop.recall(noisy)
    return {"reconstructed": array_to_b64(recon), "accuracy": acc}

@app.post("/run_ffn", response_model=ReconResp)
def run_ffn(req: ImageReq):
    init  = b64_to_array(req.image)
    noisy = add_noise(init, req.noise)
    recon, acc = ae.reconstruct(noisy)
    return {"reconstructed": array_to_b64(recon), "accuracy": acc}

@app.get("/sample_digits")
def get_samples():
    return mnist_samples_b64
