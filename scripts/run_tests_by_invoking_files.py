import subprocess
from pathlib import Path
import json

repo = Path(__file__).resolve().parents[1]
python_exec = 'D:/package/venv310/Scripts/python.exe'

files = [
    repo / 'tests' / 'test_end_to_end.py',
    repo / 'tests' / 'test_atomic_and_multi.py',
    repo / 'tests' / 'test_evaluation.py'
]

results = {}
for f in files:
    try:
        p = subprocess.run([python_exec, str(f)], capture_output=True, text=True, check=False)
        results[str(f)] = {
            'returncode': p.returncode,
            'stdout': p.stdout,
            'stderr': p.stderr
        }
    except Exception as e:
        results[str(f)] = { 'error': str(e) }

out = repo / 'run_tests_file_invocation_results.json'
with open(out, 'w', encoding='utf-8') as fh:
    json.dump(results, fh, indent=2)
print('Wrote', out)
