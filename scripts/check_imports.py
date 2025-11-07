from pathlib import Path
import importlib, traceback, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
modules = ['tests.test_end_to_end','tests.test_atomic_and_multi','tests.test_evaluation']
res={}
for m in modules:
    try:
        importlib.import_module(m)
        res[m]='imported'
    except Exception as e:
        res[m]={'error':traceback.format_exc()}

import json
p=Path(__file__).resolve().parents[1]/'check_imports_results.json'
with open(p,'w',encoding='utf-8') as f:
    json.dump(res,f,indent=2)
print('Wrote',p)
