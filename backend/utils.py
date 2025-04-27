# ===== backend/utils.py (unchanged except for a helper) =====
import io, base64
from typing import Tuple
import numpy as np
from PIL import Image


def b64_to_array(b64: str) -> np.ndarray:
    """Decode base‑64 PNG → uint8 array (H, W) with pixel values 0–255."""
    png_bytes = base64.b64decode(b64.split(",", 1)[-1])
    img = Image.open(io.BytesIO(png_bytes)).convert("L")          # grayscale
    return np.array(img, dtype=np.uint8)


def array_to_b64(arr: np.ndarray) -> str:
    """uint8 image (0‑255) → data‑URI PNG (base‑64)"""
    img = Image.fromarray(arr.astype(np.uint8), mode="L")
    buff = io.BytesIO()
    img.save(buff, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buff.getvalue()).decode()


def add_noise(arr: np.ndarray, noise_pct: float) -> np.ndarray:
    """Flip the polarity of the requested % of pixels (simple salt/pepper)."""
    noisy = arr.copy()
    n_flip = int(noise_pct / 100 * arr.size)
    idx = np.random.choice(arr.size, n_flip, replace=False)
    flat = noisy.reshape(-1)
    flat[idx] = 255 - flat[idx]                                 # invert
    return flat.reshape(arr.shape)


def accuracy(orig: np.ndarray, recon: np.ndarray) -> float:
    return (orig == recon).mean() * 100
