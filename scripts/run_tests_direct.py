import importlib
import traceback
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

modules = [
    'tests.test_end_to_end',
    'tests.test_atomic_and_multi',
    'tests.test_evaluation'
]

results = {}

for m in modules:
    try:
        mod = importlib.import_module(m)
    except Exception as e:
        results[m] = {'status': 'import_error', 'error': traceback.format_exc()}
        continue
    # discover functions beginning with test_
    tests = [name for name in dir(mod) if name.startswith('test_')]
    results[m] = {'status': 'ok', 'tests': {}}
    for t in tests:
        fn = getattr(mod, t)
        try:
            fn()
            results[m]['tests'][t] = 'passed'
        except Exception as e:
            results[m]['tests'][t] = 'failed'
            results[m]['tests'][t+'_error'] = traceback.format_exc()

import json
out_path = Path(__file__).resolve().parents[1] / 'run_tests_direct_results.json'
with open(out_path, 'w', encoding='utf-8') as fh:
    json.dump(results, fh, indent=2)
print('Wrote results to', out_path)
