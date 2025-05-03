# # backend/create_static_mnist.py
# from torchvision import datasets, transforms
# import numpy as np
# from pathlib import Path

# def save_static_digits():
#     tf = transforms.ToTensor()
#     ds = datasets.MNIST(root="./data", train=False, download=True, transform=tf)
#     picked = {}
#     for img, label in ds:
#         if label not in picked:
#             arr = (img.squeeze(0).numpy() * 255).astype(np.uint8)
#             picked[label] = arr
#         if len(picked) == 10:
#             break

#     out = {str(k): v for k, v in picked.items()}
#     path = Path(__file__).parent / "assets"
#     path.mkdir(parents=True, exist_ok=True)
#     np.savez_compressed(path / "mnist10.npz", **out)
#     print(f"Saved static MNIST digits to {path / 'mnist10.npz'}")

# save_static_digits()
