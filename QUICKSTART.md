Quickstart — Fast demo (SKIP_ML)

This project supports a fast demo mode that skips heavy ML training and uses a lightweight dependency set. Use this for local demos, CI, and quick onboarding.

Backend (fast):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.light.txt
SKIP_ML=1 python3 app.py
```

Frontend:

```bash
cd ../frontend
npm install
npm start
```

Docker quickstart (backend-only, fast):

```bash
# build with default fast install
docker build -f Dockerfile.backend -t finsight-backend .
# run with memory limits suitable for 8GB host
docker run -d --name finsight-backend -e SKIP_ML=1 -p 5002:5002 --memory=1.5g --memory-swap=2g finsight-backend
```

To run full ML mode (may require more memory & scikit-learn):

```bash
# Local: install full requirements
pip install -r requirements.txt
# or Docker: build with full deps
docker build --build-arg USE_LIGHT=0 -f Dockerfile.backend -t finsight-backend-full .
```

## Runtime configuration (anomaly sensitivity)

The backend supports a small set of environment variables to control demo vs. ML mode and anomaly sensitivity. One useful tuning knob is `ANOMALY_CONTAMINATION` which adjusts the IsolationForest expected proportion of outliers.

- ANOMALY_CONTAMINATION (float): controls IsolationForest contamination (expected proportion of outliers).
  - Default: `0.2` (20%)
  - Valid range: (0, 0.5). Values outside this range will fall back to the default.

Examples:

```bash
# fast demo with custom anomaly sensitivity
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.light.txt
export SKIP_ML=1
export ANOMALY_CONTAMINATION=0.05
python3 app.py
```

Docker example (pass env into compose or docker run):

```bash
ANOMALY_CONTAMINATION=0.05 docker-compose up --build
```
