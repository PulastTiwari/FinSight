import json
from pathlib import Path
import sys
# Ensure backend directory is on sys.path so tests can import app.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import evaluate_rules, save_rules, load_rules


def test_evaluate_contains(tmp_path, monkeypatch):
    rules = [
        {"id": "r1", "enabled": True, "priority": 10, "condition": {"field": "description", "op": "contains", "value": "salary"}, "action": {"type": "set_category", "category": "Salary"}}
    ]
    p = tmp_path / 'rules.json'
    p.write_text(json.dumps(rules))
    monkeypatch.setenv('PYTHONPATH', str(Path(__file__).resolve().parent))
    # monkeypatch load_rules to read from tmp file
    monkeypatch.setattr('app.RULES_PATH', p)
    res = evaluate_rules({'description': 'Monthly SALARY payment', 'amount': 1000})
    assert res['rule_id'] == 'r1'
    assert res['action']['type'] == 'set_category'


def test_evaluate_gt(tmp_path, monkeypatch):
    rules = [
        {"id": "r2", "enabled": True, "priority": 5, "condition": {"field": "amount", "op": "gt", "value": 10000}, "action": {"type": "flag", "flag": "review"}}
    ]
    p = tmp_path / 'rules.json'
    p.write_text(json.dumps(rules))
    monkeypatch.setattr('app.RULES_PATH', p)
    res = evaluate_rules({'description': 'Purchase', 'amount': 25000})
    assert res['rule_id'] == 'r2'
    assert res['action']['type'] == 'flag'
