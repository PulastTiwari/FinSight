# backend/models

Place custom ML model code and related utilities here.

Suggested layout:

- models/
  - my_model.py # contains train(), predict(), save(), load() functions
  - utils.py # helper functions for preprocessing

Patterns:

- Keep model code independent from Flask app logic.
- Expose simple function signatures:
  - train(df: pd.DataFrame) -> model
  - predict(model, X: np.ndarray) -> np.ndarray
  - save(model, path: str)
  - load(path: str) -> model

When adding a new model, add tests under `backend/tests/` and document usage in `backend/README.md`.

## Minimal training and persistence example

Below is a compact blueprint you can adapt for a TF-IDF + RandomForest classifier used by the Flask app.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import joblib

def train(df):
    # df expected to have ['description', 'amount', 'category']
    X_text = df['description'].fillna('')
    pipeline = make_pipeline(TfidfVectorizer(max_features=1024), RandomForestClassifier(n_estimators=50))
    pipeline.fit(X_text, df['category'])
    return pipeline

def predict(model, descriptions):
    return model.predict(descriptions)

def save(model, path):
    joblib.dump(model, path)

def load(path):
    return joblib.load(path)
```

Notes:

- Keep preprocessing consistent between `train()` and `predict()` by including transformers (TF-IDF) in the same pipeline as the estimator.
- Prefer `joblib` for model persistence (works well with scikit-learn objects).
- For production, separate feature engineering and store the fitted transformers alongside the model artifact.

## Tests

- Add unit tests under `backend/tests/` that exercise `train()` and `predict()` using a small synthetic dataframe. Use `ANOMALY_CONTAMINATION` via environment variables to keep anomaly-related tests deterministic.
