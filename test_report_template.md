# KGEB Test Report Template

## Test Execution Summary

**Date:** [Date]
**Method:** [Method Name]
**Version:** [Version]
**Environment:** [OS, Python Version, etc.]

---

## 1. Entity Extraction Results

### Overall Metrics

| Metric | Value |
|--------|-------|
| Entity F1 Score | [Value] |
| Entity Precision | [Value] |
| Entity Recall | [Value] |
| Schema Compliance | [Value]% |

### Per-Entity-Type Results

| Entity Type | Count | Precision | Recall | F1 | Schema Compliance |
|------------|-------|-----------|--------|----|-------------------|
| Person | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Company | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Project | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Department | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Position | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Technology | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Location | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Team | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Product | [Count] | [Value] | [Value] | [Value] | [Value]% |
| Client | [Count] | [Value] | [Value] | [Value] | [Value]% |

### Sample Extracted Entities

```json
{
  "Person": [
    {
      "name": "[Example]",
      "age": [Example],
      "position": "[Example]",
      "department": "[Example]"
    }
  ]
}
```

---

## 2. Relation Extraction Results

### Overall Metrics

| Metric | Value |
|--------|-------|
| Relation F1 Score | [Value] |
| Relation Precision | [Value] |
| Relation Recall | [Value] |
| Schema Compliance | [Value]% |
| Logical Consistency | [Value]% |

### Per-Relation-Type Results

| Relation Type | Count | Precision | Recall | F1 | Schema Compliance | Logical Consistency |
|---------------|-------|-----------|--------|----|-------------------|---------------------|
| BelongsTo | [Count] | [Value] | [Value] | [Value] | [Value]% | [Value]% |
| WorksAt | [Count] | [Value] | [Value] | [Value] | [Value]% | [Value]% |
| ManagesProject | [Count] | [Value] | [Value] | [Value] | [Value]% | [Value]% |
| ... | ... | ... | ... | ... | ... | ... |

### Sample Extracted Relations

```json
{
  "WorksAt": [
    {
      "person": "[Example]",
      "company": "[Example]"
    }
  ]
}
```

---

## 3. Test Execution Details

### Unit Tests

| Test Suite | Tests Run | Passed | Failed | Skipped |
|------------|-----------|--------|--------|---------|
| Entity Extraction | [Count] | [Count] | [Count] | [Count] |
| Relation Extraction | [Count] | [Count] | [Count] | [Count] |
| Evaluator | [Count] | [Count] | [Count] | [Count] |
| Collaboration | [Count] | [Count] | [Count] | [Count] |

### Integration Tests

| Test Type | Status | Details |
|-----------|--------|---------|
| Full Pipeline | [Pass/Fail] | [Details] |
| Multi-Document | [Pass/Fail] | [Details] |
| Persistence | [Pass/Fail] | [Details] |
| Concurrency | [Pass/Fail] | [Details] |

---

## 4. Performance Metrics

| Metric | Value |
|--------|-------|
| Total Processing Time | [Time] |
| Entity Extraction Time | [Time] |
| Relation Extraction Time | [Time] |
| Evaluation Time | [Time] |
| Memory Usage (Peak) | [Memory] |

---

## 5. Issues and Observations

### Known Issues

1. [Issue Description]
   - Impact: [High/Medium/Low]
   - Status: [Open/Resolved]

### Observations

- [Observation 1]
- [Observation 2]

---

## 6. Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

---

## 7. Conclusion

[Summary of test results and overall assessment]

---

## Appendix

### Test Environment Details

- OS: [OS Version]
- Python: [Python Version]
- Dependencies: [List of key dependencies and versions]

### Test Data

- Documents: [Number of documents processed]
- Total Text Length: [Characters/Lines]

### Output Files

- `entities_output.json`: [File size, entity count]
- `relations_output.json`: [File size, relation count]
- `evaluation_report.json`: [File size]

