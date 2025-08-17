# Quickstart

A minimal quickstart for developers and reviewers.

## Fast local demo (no heavy ML)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir -r requirements.light.txt
export SKIP_ML=1
python3 app.py
# from another terminal
curl -fsS http://127.0.0.1:5002/api/health
```

## Frontend

```bash
cd frontend
npm ci
npm start
# open http://localhost:3000/
```
