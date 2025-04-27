Quick-start
1 . Clone (or download) the repo
bash
Copy
Edit
git clone https://github.com/<your-org>/bio-inspired-app.git
cd bio-inspired-app            # project root
<details> <summary><strong>Folder layout recap</strong></summary>
css
Copy
Edit
bio-inspired-app
├─ backend/          ← FastAPI + models + utils
│  ├─ models/
│  │   ├─ automaton.py
│  │   ├─ hopfield.py
│  │   └─ autoencoder.py
│  ├─ main.py
│  └─ requirements.txt
└─ frontend/         ← React + Vite + Tailwind
   ├─ src/…
   ├─ package.json
   └─ vite.config.js
</details>
2 . Prerequisites

What	Version	Windows install	macOS / Linux install
Python	3.10 or 3.11 (⚠️ not 3.12)	https://python.org/downloads/ (“Add to PATH”)	brew install python@3.11 / apt install python3.11
Node.js	18 +	https://nodejs.org (LTS)	brew install node / apt install nodejs
Microsoft VC++ Runtime (Windows only)	2015-2022	https://aka.ms/vs/17/release/vc_redist.x64.exe	—
3 . Backend (FastAPI + NumPy/Torch)
bash
Copy
Edit
# from project root
cd backend

# create & activate a venv (Windows PowerShell)
py -3.11 -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process  # first time only
.\.venv\Scripts\activate

# macOS/Linux
# python3.11 -m venv .venv
# source .venv/bin/activate

# upgrade installer and pull deps
python -m pip install --upgrade pip
pip install -r requirements.txt       # fastapi, numpy, torch, ...

# (optional) if NumPy/PyTorch wheels fail to import:
# pip install --force-reinstall --no-cache-dir numpy torch pydantic-core
Tip: confirm the compiled libraries exist:
dir .venv\Lib\site-packages\numpy\core\*.pyd

Launch the API
bash
Copy
Edit
# still inside venv & project root
cd ..
uvicorn backend.main:app --reload
Docs at http://localhost:8000/docs

4 . Frontend (React + Vite)
bash
Copy
Edit
cd frontend
npm install          # installs React, Vite, Tailwind, Axios, Recharts
npm run dev          # dev server on http://localhost:5173
If you run Uvicorn on a different port, update frontend/src/api.js:

js
Copy
Edit
const api = axios.create({ baseURL: "http://localhost:9000" });
5 . Play
Open http://localhost:5173 in your browser.

Choose a digit → set noise level → click one of the model buttons.

View Original | Noisy | Reconstructed and the accuracy bar.

🛠 Common errors & fixes

Error	Cause	Fix
ModuleNotFoundError: torch._prims_common	Installed PyTorch on Python 3.12	Use Python 3.10/3.11 or pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu
No module named 'numpy.core._multiarray_umath'	Corrupt / wrong-arch NumPy wheel	pip install --force-reinstall --no-cache-dir numpy==1.26.4 + install VC++ redist
ImportError: attempted relative import with no known parent package	Running Uvicorn from inside backend/	Run from project root: uvicorn backend.main:app --reload
Fancy hyphen ÔÇô characters cause SyntaxError	Copied text from Word/Slack	Replace with ASCII - (Ctrl+H in VS Code)
🔄 Training your own patterns
The demo ships with tiny inline digit bit-maps.
To train real MNIST for Hopfield/Autoencoder:

python
Copy
Edit
from sklearn.datasets import load_digits
digits = load_digits()
patterns = (digits.images > 4).astype(float)   # threshold to binary

from backend.models.hopfield import HopfieldNetwork
hop = HopfieldNetwork()
hop.train(patterns)
# np.save("hop_weights.npy", hop.W)

# For the autoencoder
from backend.models.autoencoder import FeedforwardAutoencoder
model = FeedforwardAutoencoder()
# ... PyTorch training ...
# torch.save(model.state_dict(), "ae.pt")
Load the weights in backend/main.py.

Happy hacking! 🎉






