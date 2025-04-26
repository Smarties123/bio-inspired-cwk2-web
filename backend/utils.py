import io, base64
from typing import Tuple
import numpy as np
from PIL import Image

# NOTE: replaced all non‑ASCII hyphens with normal '-' to avoid SyntaxError

def b64_to_array(b64: str) -> np.ndarray:
    """Decode base64 PNG → bool array (H,W)"""
    png_bytes = base64.b64decode(b64.split(",", 1)[-1])
    img = Image.open(io.BytesIO(png_bytes))
    return (np.array(img.convert("L")) > 127).astype(np.float32)

def array_to_b64(arr: np.ndarray) -> str:
    arr = (arr * 255).astype(np.uint8)
    img = Image.fromarray(arr, mode="L")
    buff = io.BytesIO()
    img.save(buff, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buff.getvalue()).decode()

def add_noise(arr: np.ndarray, noise_pct: float) -> np.ndarray:
    """Flip given percentage of pixels"""
    noisy = arr.copy()
    n_flip = int(noise_pct / 100 * arr.size)
    idx = np.random.choice(arr.size, n_flip, replace=False)
    flat = noisy.flatten()
    flat[idx] = 1 - flat[idx]
    return flat.reshape(arr.shape)

def accuracy(orig: np.ndarray, recon: np.ndarray) -> float:
    return (orig == recon).mean() * 100