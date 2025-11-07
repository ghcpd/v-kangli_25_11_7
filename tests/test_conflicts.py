from kgeb.evaluator import detect_entity_conflicts


def test_detect_conflicts():
    preds = {
        "Person": [
            {"name": "Alex Doe", "age": 30, "position": "Engineer"},
            {"name": "Alex Doe", "age": 31, "position": "Engineer"},
            {"name": "Sam Smith", "age": 40}
        ],
        "Company": [
            {"name": "Acme"}
        ]
    }
    conflicts = detect_entity_conflicts(preds)
    assert "Person" in conflicts
    assert "Alex Doe" in conflicts["Person"]
