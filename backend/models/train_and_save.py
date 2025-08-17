"""Train an example model on backend/sample_data.csv and save to backend/models/model.joblib
This script is safe to run when scikit-learn is installed. It exits with a helpful message if SKIP_ML is set.
"""
import os
import sys

if os.getenv('SKIP_ML', '0') == '1':
    print('SKIP_ML=1 set; skipping training (use SKIP_ML=0 to train).')
    sys.exit(0)

import pandas as pd
from example_model import train, save

ROOT = os.path.dirname(os.path.dirname(__file__))
SAMPLE = os.path.join(ROOT, 'sample_data.csv')
OUT = os.path.join(ROOT, 'models', 'model.joblib')

if not os.path.exists(SAMPLE):
    print(f"Missing sample data at {SAMPLE}; please provide sample_data.csv to train a model.")
    sys.exit(1)

os.makedirs(os.path.dirname(OUT), exist_ok=True)

df = pd.read_csv(SAMPLE)
model = train(df)
save(model, OUT)
print(f"Model trained and saved to {OUT}")
