# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
# from torchvision import datasets, transforms

from backend.utils import b64_to_array, array_to_b64
from backend.models.ca import WeightedMajorityCA
from backend.models.hopfield_pi import HopfieldPseudoInverse
from backend.models.som_knn import SOMKNN
from backend.models.hybrid import HybridHopCaHop
from backend.utils import add_noise

from pathlib import Path



app = FastAPI(title="Bio-Inspired Recall API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ImageReq(BaseModel):
    image: str
    noise: float = 0.0

class ReconResp(BaseModel):
    reconstructed: str
    accuracy: float

class CAResp(ReconResp):
    frames: list[str]
    
class DualImageReq(BaseModel):
    noisy: str   # base64 string
    init:  str   # base64 string


# load 10 MNIST test samples into memory
def _load_samples():
    """Load the 10 NP‑arrays we exported; no torch required."""
    data = np.load(Path(__file__).parent / "assets" / "mnist10.npz")
    # data.files == ['0','1',...,'9']
    return [data[str(i)] for i in range(10)]

_samples = _load_samples()
_patterns = np.stack([s.flatten()/255 for s in _samples], axis=0)

# instantiate each model once
ca_model   = WeightedMajorityCA(steps=15)
hop_model  = HopfieldPseudoInverse(_patterns)
som_model  = SOMKNN(_patterns)
hyb_model  = HybridHopCaHop(hop_model, ca_model)

# endpoints
@app.post("/run_ca", response_model=CAResp)
def run_ca(req: ImageReq):
    init = b64_to_array(req.image)
    noisy = init.copy()
    # salt‐pepper
    idx = np.random.choice(init.size, int(req.noise/100*init.size), replace=False)
    flat = noisy.flatten(); flat[idx] = 255-flat[idx]; noisy = flat.reshape(init.shape)
    frames, acc = ca_model.run(noisy)
    return {
        "reconstructed": array_to_b64(frames[-1]),
        "accuracy": acc,
        "frames": [array_to_b64(f) for f in frames]
    }

@app.post("/run_hopfield", response_model=ReconResp)
def run_hopfield(req: DualImageReq):
    noisy_arr = b64_to_array(req.noisy)
    init_arr  = b64_to_array(req.init)

    recon_flat, acc = hop_model.recall(noisy_arr.flatten() / 255)
    recon_img = recon_flat.reshape(init_arr.shape)

    return {
        "reconstructed": array_to_b64(recon_img),
        "accuracy": acc
    }

@app.post("/run_som", response_model=ReconResp)
def run_som(req: DualImageReq):
    noisy_arr = b64_to_array(req.noisy)
    init_arr  = b64_to_array(req.init)

    recon_flat, acc = som_model.recall(noisy_arr.flatten() / 255)
    recon_img = recon_flat.reshape(init_arr.shape)

    return {
        "reconstructed": array_to_b64(recon_img),
        "accuracy": acc
    }

@app.post("/run_hybrid", response_model=ReconResp)
def run_hybrid(req: ImageReq):
    init = b64_to_array(req.image)
    noisy = init.copy()
    idx = np.random.choice(init.size, int(req.noise/100*init.size), replace=False)
    flat = noisy.flatten(); flat[idx] = 255-flat[idx]; noisy = flat.reshape(init.shape)
    recon = hyb_model.recall(noisy.flatten()/255)
    # compute accuracy manually
    from backend.utils import accuracy
    acc = accuracy(init, recon)
    return {"reconstructed": array_to_b64(recon), "accuracy": acc}

@app.get("/sample_digits")
def sample_digits():
    return { str(i): array_to_b64(arr) for i,arr in enumerate(_samples) }


from backend.utils import add_noise, array_to_b64, b64_to_array

@app.post("/generate_noise", response_model=ReconResp)
def generate_noise(req: ImageReq):
    init  = b64_to_array(req.image)
    noisy = add_noise(init, req.noise)     # just salt & pepper
    return { "reconstructed": array_to_b64(noisy),
             "accuracy": 0.0 }
