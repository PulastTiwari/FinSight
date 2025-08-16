from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, IsolationForest

app = Flask(__name__)
CORS(app)

# Load and train models on startup
df = pd.read_csv('sample_data.csv')

# Train categorization model
vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
X = vectorizer.fit_transform(df['description'])
y = df['category']
clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X, y)

# Train anomaly model
features = df[['amount']].values
anomaly_model = IsolationForest(contamination=0.2, random_state=42)
anomaly_model.fit(features)

@app.route('/api/health')
def health():
	return jsonify({'status': 'healthy'})

@app.route('/api/categorize', methods=['POST'])
def categorize():
	data = request.json
	description = data.get('description', '')
	amount = float(data.get('amount', 0))
    
	# Categorize
	desc_vec = vectorizer.transform([description])
	category = clf.predict(desc_vec)[0]
	confidence = max(clf.predict_proba(desc_vec))
    
	# Anomaly detection
	is_anomaly = anomaly_model.predict([[amount]]) == -1
    
	return jsonify({
		'category': category,
		'confidence': round(confidence, 3),
		'is_anomaly': bool(is_anomaly)
	})

@app.route('/api/analytics')
def analytics():
	category_counts = df['category'].value_counts().to_dict()
	avg_amounts = df.groupby('category')['amount'].mean().round(2).to_dict()
    
	anomalies = anomaly_model.predict(df[['amount']].values)
	anomaly_count = sum(1 for x in anomalies if x == -1)
    
	return jsonify({
		'category_distribution': category_counts,
		'average_amounts': avg_amounts,
		'total_transactions': len(df),
		'anomaly_count': anomaly_count,
		'transactions': df.to_dict('records')[:10]
	})

if __name__ == '__main__':
	app.run(debug=True, port=5000)