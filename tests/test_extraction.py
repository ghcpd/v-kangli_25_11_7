import json
import subprocess


def run_extraction():
    subprocess.run(['python', 'kgeb/extract.py', '--docs', 'documents.txt', '--entities', 'entities.json', '--out', 'entities_output.json'], check=True)


def test_entities_exist():
    run_extraction()
    with open('entities_output.json','r',encoding='utf-8') as f:
        data = json.load(f)
    assert 'Person' in data
    assert 'Company' in data
    print('Basic extraction smoke test passed')

if __name__ == '__main__':
    test_entities_exist()
