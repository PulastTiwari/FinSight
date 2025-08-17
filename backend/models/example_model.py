"""Simple model contract used by the Flask app and tests.
Provides train/predict/save/load functions using scikit-learn.
"""

def _ensure_sklearn():
    try:
        import sklearn  # noqa: F401
    except Exception as e:
        raise ImportError("scikit-learn is required for example_model. Set SKIP_ML=1 to skip ML or install scikit-learn.") from e


def train(df):
    """Train a TF-IDF + RandomForest pipeline.

    Args:
        df: pandas.DataFrame with columns ['description', 'amount', 'category']

    Returns:
        fitted pipeline
    """
    _ensure_sklearn()
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import make_pipeline

    X_text = df['description'].fillna('')
    pipeline = make_pipeline(TfidfVectorizer(max_features=1024), RandomForestClassifier(n_estimators=50))
    pipeline.fit(X_text, df['category'])
    return pipeline


def predict(model, descriptions):
    """Predict categories for a list/series of descriptions.

    Args:
        model: trained pipeline
        descriptions: iterable of strings

    Returns:
        numpy array of predicted labels
    """
    _ensure_sklearn()
    return model.predict(descriptions)


def save(model, path):
    _ensure_sklearn()
    import joblib
    joblib.dump(model, path)


def load(path):
    _ensure_sklearn()
    import joblib
    return joblib.load(path)
