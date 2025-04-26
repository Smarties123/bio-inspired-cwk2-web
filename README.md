# Bio‑Inspired Pattern Recall Demo

## Prerequisites
- **Python 3.9+** & **Node 18+**

## Setup (Backend)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload  # server at http://localhost:8000