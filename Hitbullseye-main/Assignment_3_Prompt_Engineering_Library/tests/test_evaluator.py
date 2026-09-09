"""
Unit tests for Assignment 3 Prompt Evaluator
"""
import pytest
import os
import json
from evaluate import load_json, evaluate_case, GOLDEN_SET_PATH

def test_golden_set_structure():
    assert os.path.exists(GOLDEN_SET_PATH)
    data = load_json(GOLDEN_SET_PATH)
    assert len(data) == 50
    for item in data:
        assert "id" in item
        assert "user_input" in item
        assert "expected_output" in item
        assert "acceptance_criteria" in item
        assert "is_out_of_scope" in item
        assert "is_hostile" in item

def test_evaluator_format_checking():
    item = {
        "id": "TEST-01",
        "category": "Billing",
        "user_input": "Test query",
        "expected_output": "Expected response",
        "acceptance_criteria": ["criteria1"],
        "is_out_of_scope": False,
        "is_hostile": False
    }
    
    # Valid JSON for v1.3
    valid_json_resp = json.dumps({"category": "Billing", "is_boundary_violation": False, "customer_message": "Hello"})
    res = evaluate_case("v1.3", item, valid_json_resp)
    assert res["format_pass"] is True

    # Invalid JSON for v1.3
    invalid_json_resp = "Here is your response: Hello!"
    res_invalid = evaluate_case("v1.3", item, invalid_json_resp)
    assert res_invalid["format_pass"] is False
