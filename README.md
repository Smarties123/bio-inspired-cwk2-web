# Investigating Cellular Automata as Associative Memory Systems

Interactive demo and reference code for our University of Leeds 2025 group project  
**“Bio‑Inspired Associative Memories for Robust Pattern Recall.”**

Live site → **<https://bio-inspired-cwk2-web.vercel.app>**
Backend hosted on → **<https://bio-inspired-cwk2-web.onrender.com/health>**

---

## 🚀 What’s inside?

| Folder | Purpose | Main Tech |
|--------|---------|-----------|
| **`frontend/`** | Vite + React UI with Tailwind CSS & Recharts. | React 18, Vite 5, Tailwind 3 |
| **`backend/`**  | FastAPI micro‑service implementing four bio‑inspired recall models. | FastAPI 0.110, NumPy, scikit‑learn, MiniSom |
| **`research/`** | python notebooks used during experimentation & report writing and contains in depth analysis of Algorithms used. |

### Research notebooks
* `Bio Inspired CWK 2 Final Version - MNIST.ipynb`
* `Bio Inspired CWK 2 Final Version - Larger Images & Colour.ipynb`

---

##  Tech‑stack highlights

* **FastAPI** – typed, lightning‑fast Python API.
* **Vite + React 18** – modern SPA tooling with instant HMR.
* **Tailwind CSS** – utility‑first styling for rapid prototyping.
* **Recharts** – simple D3‑powered charts to visualise accuracy.
* **Deployment** –  
  * Backend: **Render** (free web service, automatic builds).  
  * Frontend: **Vercel** (static build from `frontend/dist`).

---

##   Running locally

> Requires **Node ≥ 18** & **Python ≥ 3.10**.

### 1. Clone

```bash
git clone https://github.com/Smarties123/bio-inspired-cwk2-web.git
cd bio-inspired-cwk2-web
2. Backend
bash
Copy
Edit
# optional: create & activate virtualenv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install server requirements
pip install -r requirements.txt

# start API (defaults to http://localhost:8000)
cd backend
uvicorn main:app --reload
3. Frontend
bash
Copy
Edit
cd ../frontend
npm install
npm run dev           # opens at http://localhost:5173
The React app is hard‑coded to call the API at http://localhost:8000, so keep both processes running in parallel.

📦  requirements.txt (backend)
text
Copy
Edit
# FastAPI server
fastapi==0.110.0
uvicorn==0.27.1

# Array & image processing
numpy==1.26.4
pillow==10.3.0

# Validation
pydantic==2.7.1
python-multipart==0.0.9

# Machine learning
scikit-learn==1.5.0
minisom==2.3.0
(PyTorch / torchvision removed – the project is now pure‑NumPy.)

🤝  Contributors
Angelica P. · Hemant S. – supervised by Prof. Netta Cohen.
University of Leeds · School of Computing · 2025