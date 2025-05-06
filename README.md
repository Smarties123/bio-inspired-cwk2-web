# Auto-Associative Memory Under Corruption: A Comparative Performance of Advanced Bio-Inspired Architectures

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
| **`research/`** | python notebooks used during experimentation & report writing and contains in depth analysis of Algorithms used. | Google Collab, Matplotlib, skimage and MiniSom

## Step 1: Research notebooks
### All code related to models in report can be found in the research notebook
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

##  Step 2: Running locally (Preview should be available on earlier link)

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

'''


# Statement of Contributions & Attributions

Area	Angelica Patel (sc21asp)	Hemant Smart (sc21hs2)	Mode of collaboration
Project design & research framing	Co‑designed research questions; led literature search on auto‑associative memory	Co‑designed research questions; led comparative‑methods survey	White‑board sessions, Overleaf notes
Model implementation	Implemented SOM‑KNN & LAM+ variants in research/ notebooks; wrote evaluation metrics	Implemented Hopfield‑PI & CA‑Weighted variants; optimised training loops	Pair‑programming in VS Code Live Share
Backend (FastAPI)	Auth & CORS middleware; OpenAPI docs	Core /recall endpoints, weight‑loaders, CI workflow	Code reviews on every PR
Frontend (React + Vite)	Layout, Tailwind styling, Recharts integration, routing	Component state logic, API hooks, deployment to Vercel	Mob‑programming on feature branches
Experiments & figures	MNIST experiments, colour‑image benchmarks, SSIM plots	Runtime profiling, ablation studies, MSE heat‑maps	Shared Colab notebooks; random‑seed lockstep
Report writing	Drafted §1–3 (intro, background, methods); final proofreading	Drafted §4–6 (results, discussion, conclusions); reference management	Joint editing in Overleaf (≈50 : 50 commit split)
Presentation slides	Design & visuals	Speaker notes & timing	Rehearsed together
DevOps & packaging	—	Created Makefile, Dockerfile, GitHub Actions CD	Pair‑review
Testing & QA	PyTest suites, Playwright e2e tests	Front‑end linting, back‑end type‑checks	Alternating reviewer roles

## External code & libraries

Our work stands on the shoulders of open‑source giants; none of these third‑party packages were modified beyond normal configuration and all are licensed for academic use. Full versions are pinned in requirements.txt / package.json.

Python – FastAPI 0.110, Uvicorn 0.27, NumPy 1.26, scikit‑learn 1.5, MiniSom 2.3, Pillow 10.3, pydantic 2.7, python‑multipart 0.0.9
JavaScript – React 18, Vite 5, Tailwind CSS 3, Recharts 2.9
Tooling – GitHub Actions, Render.com, Vercel, Prettier, ESLint, PyTest, Playwright

Icons by Heroicons; fonts via Google Fonts (Inter).
