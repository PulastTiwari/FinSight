from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import json
from pathlib import Path

# Optional flag to skip heavy ML imports/training for quick smoke tests
SKIP_ML = os.getenv('SKIP_ML', '0') == '1'

if not SKIP_ML:
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.ensemble import RandomForestClassifier, IsolationForest

app = Flask(__name__)
CORS(app)

# Resolve paths relative to this file so imports/CLI/test-client work from any CWD
BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DATA_PATH = BASE_DIR / 'sample_data.csv'
RULES_PATH = BASE_DIR / 'rules.json'

# Load data and optionally train models on startup (use robust path)
df = pd.read_csv(SAMPLE_DATA_PATH)

if not SKIP_ML:
	# Train categorization model
	vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
	X = vectorizer.fit_transform(df['description'].astype(str))
	y = df['category']
	clf = RandomForestClassifier(n_estimators=50, random_state=42)
	clf.fit(X, y)

	# Train anomaly model
	features = df[['amount']].values
	# Allow runtime configuration of anomaly sensitivity via environment variable
	# ANOMALY_CONTAMINATION is the expected proportion of outliers (float between 0 and 0.5)
	try:
		_cont = float(os.getenv('ANOMALY_CONTAMINATION', '0.2'))
		# clamp sensible values
		if _cont <= 0 or _cont >= 0.5:
			_cont = 0.2
	except Exception:
		_cont = 0.2
	anomaly_model = IsolationForest(contamination=_cont, random_state=42)
	anomaly_model.fit(features)
else:
	# placeholders for smoke tests
	vectorizer = None
	clf = None
	anomaly_model = None


def load_rules():
	if not RULES_PATH.exists():
		return []
	try:
		return json.loads(RULES_PATH.read_text())
	except Exception:
		return []


def save_rules(rules):
	RULES_PATH.write_text(json.dumps(rules, indent=2))


def validate_rule(rule):
	# Minimal validation: required keys
	if not isinstance(rule, dict):
		return False, 'rule must be an object'
	if 'id' not in rule or 'condition' not in rule or 'action' not in rule:
		return False, 'missing required keys (id, condition, action)'
	cond = rule['condition']
	if not isinstance(cond, dict) or 'op' not in cond or 'field' not in cond or 'value' not in cond:
		return False, 'condition must contain op, field, value'
	if cond['op'] not in ('contains', 'equals', 'gt', 'lt'):
		return False, 'unsupported op; allowed: contains, equals, gt, lt'
	return True, None


def evaluate_rules(transaction):
	# transaction: dict with fields like description, amount, vendor
	rules = load_rules()
	# filter enabled and sort by priority desc
	enabled = [r for r in rules if r.get('enabled', True)]
	enabled.sort(key=lambda r: r.get('priority', 0), reverse=True)

	for r in enabled:
		cond = r['condition']
		field = cond['field']
		op = cond['op']
		value = cond['value']
		txn_val = transaction.get(field)
		if txn_val is None:
			continue
		try:
			if op == 'contains':
				if str(value).lower() in str(txn_val).lower():
					return {'rule_id': r['id'], 'action': r['action'], 'provenance': 'rule'}
			elif op == 'equals':
				if str(txn_val).lower() == str(value).lower():
					return {'rule_id': r['id'], 'action': r['action'], 'provenance': 'rule'}
			elif op in ('gt', 'lt'):
				# numeric compare
				try:
					txn_num = float(txn_val)
					val_num = float(value)
				except Exception:
					continue
				if op == 'gt' and txn_num > val_num:
					return {'rule_id': r['id'], 'action': r['action'], 'provenance': 'rule'}
				if op == 'lt' and txn_num < val_num:
					return {'rule_id': r['id'], 'action': r['action'], 'provenance': 'rule'}
		except Exception:
			continue
	return {'rule_id': None, 'action': None, 'provenance': 'none'}


@app.route('/api/health')
def health():
	return jsonify({'status': 'healthy'})


@app.route('/api/rules', methods=['GET'])
def list_rules():
	return jsonify(load_rules())


@app.route('/api/rules', methods=['POST'])
def create_rule():
	rule = request.json
	ok, err = validate_rule(rule)
	if not ok:
		return jsonify({'error': err}), 400
	rules = load_rules()
	# replace if id exists
	existing = [r for r in rules if r.get('id') == rule.get('id')]
	if existing:
		rules = [r for r in rules if r.get('id') != rule.get('id')]
	rules.append(rule)
	save_rules(rules)
	return jsonify({'status': 'saved', 'rule': rule})


@app.route('/api/rules/<rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
	rules = load_rules()
	new_rules = [r for r in rules if str(r.get('id')) != str(rule_id)]
	if len(new_rules) == len(rules):
		return jsonify({'error': 'rule not found'}), 404
	save_rules(new_rules)
	return jsonify({'status': 'deleted', 'rule_id': rule_id})


@app.route('/api/rules/evaluate', methods=['POST'])
def rules_evaluate():
	txn = request.json or {}
	result = evaluate_rules(txn)
	return jsonify(result)


@app.route('/api/categorize', methods=['POST'])
def categorize():
	data = request.json or {}
	description = data.get('description', '')
	amount = float(data.get('amount', 0) or 0)

	# First, apply rules
	rule_result = evaluate_rules({'description': description, 'amount': amount, 'vendor': data.get('vendor')})
	if rule_result.get('rule_id'):
		action = rule_result.get('action') or {}
		if action.get('type') == 'set_category':
			return jsonify({'category': action.get('category'), 'confidence': 1.0, 'is_anomaly': False, 'provenance': 'rule'})
		if action.get('type') == 'flag':
			# return flagged response, but still run ML for category
			pass

	# Fallback to ML classification
	# If ML was skipped at startup, return a lightweight fallback response
	if SKIP_ML or vectorizer is None or clf is None or anomaly_model is None:
		# simple heuristic fallback: short descriptions => Unknown, otherwise use 'Other'
		fallback_category = 'Unknown' if len(description.strip()) == 0 else 'Other'
		# if a rule flagged it, preserve that provenance
		return jsonify({
			'category': fallback_category,
			'confidence': 0.0,
			'is_anomaly': False,
			'provenance': 'fallback'
		})

	# Normal ML path
	desc_vec = vectorizer.transform([description])
	category = clf.predict(desc_vec)[0]
	try:
		confidence = float(max(clf.predict_proba(desc_vec)))
	except Exception:
		confidence = 0.0

	# Anomaly detection
	is_anomaly = anomaly_model.predict([[amount]]) == -1

	return jsonify({
		'category': category,
		'confidence': round(confidence, 3),
		'is_anomaly': bool(is_anomaly),
		'provenance': 'ml'
	})


@app.route('/api/analytics')
def analytics():
	category_counts = df['category'].value_counts().to_dict()
	avg_amounts = df.groupby('category')['amount'].mean().round(2).to_dict()
	# If ML skipped, don't call anomaly_model (it may be None); provide demo-friendly analytics
	if SKIP_ML or anomaly_model is None:
		anomaly_count = 0
		transactions = df.to_dict('records')[:10]
		return jsonify({
			'category_distribution': category_counts,
			'average_amounts': avg_amounts,
			'total_transactions': len(df),
			'anomaly_count': anomaly_count,
			'transactions': transactions,
			'provenance': 'fallback'
		})

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
	app.run(debug=True, port=5002)