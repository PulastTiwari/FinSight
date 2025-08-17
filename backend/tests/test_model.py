import os
import sys
import pathlib
import pytest
import pandas as pd

# Ensure repo root is on sys.path so package imports resolve when running tests from backend/
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Skip ML tests in SKIP_ML mode for CI/demo compatibility
skip_ml = os.getenv('SKIP_ML', '0') == '1'

from backend.models.example_model import train, predict, save, load

@pytest.mark.skipif(skip_ml, reason='SKIP_ML=1 set; skipping ML-dependent tests')
def test_train_predict_save_load(tmp_path):

    data = pd.DataFrame([
        {'description': 'MONTHLY SALARY PAYMENT', 'amount': 3500, 'category': 'income'},
        {'description': 'ELECTRIC BILL - CO', 'amount': 150, 'category': 'utilities'},
        {'description': 'UBER RIDE', 'amount': 25.5, 'category': 'travel'}
    ])

    model = train(data)
    preds = predict(model, data['description'])
    assert len(preds) == 3

    out = tmp_path / 'model.joblib'
    save(model, str(out))
    loaded = load(str(out))
    preds2 = predict(loaded, data['description'])
    assert list(preds) == list(preds2)
