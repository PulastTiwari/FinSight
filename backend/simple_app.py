from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/categorize', methods=['POST'])
def categorize():
    return jsonify({
        'category': random.choice(['Travel', 'Utilities', 'Salaries', 'Procurement']),
        'confidence': 0.85,
        'is_anomaly': False
    })

@app.route('/api/analytics')
def analytics():
    return jsonify({
        'category_distribution': {'Travel': 5, 'Utilities': 4, 'Salaries': 3, 'Procurement': 3},
        'average_amounts': {'Travel': 450, 'Utilities': 83, 'Salaries': 3500, 'Procurement': 200},
        'total_transactions': 15,
        'anomaly_count': 2,
        'transactions': [{'date': '2024-01-01', 'description': 'SAMPLE', 'amount': 100, 'category': 'Utilities'}]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
