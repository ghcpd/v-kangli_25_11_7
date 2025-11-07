import os
import json
from pathlib import Path
import tempfile
from threading import Thread

from extractors import save_json, parse_documents_dir, extract_all


def test_atomic_write_and_concurrent(tmp_path):
    path = tmp_path / 'out.json'
    data1 = {'a': 1}
    data2 = {'b': 2}

    def write1():
        save_json(data1, str(path))
    def write2():
        save_json(data2, str(path))

    t1 = Thread(target=write1)
    t2 = Thread(target=write2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Both writes succeed; file must contain one of the two writes
    with open(path, 'r', encoding='utf-8') as f:
        out = json.load(f)
    assert out == data1 or out == data2


def test_parse_documents_dir(tmp_path, monkeypatch):
    # create two doc files
    f1 = tmp_path / 'd1.txt'
    f2 = tmp_path / 'd2.txt'
    f1.write_text('John Doe, age 32, works at OpenAI as a Researcher.')
    f2.write_text('Project Alpha started on 2023-01-15, ends on 2023-06-30.')
    lines = parse_documents_dir(str(tmp_path))
    out = extract_all(lines)
    assert 'Person' in out['entities']
    assert 'Project' in out['entities']


if __name__ == '__main__':
    import tempfile
    from pathlib import Path
    td = Path(tempfile.mkdtemp())
    print('Running test_atomic_write_and_concurrent with tmp_path', td)
    test_atomic_write_and_concurrent(td)
    print('Running test_parse_documents_dir with tmp_path', td)
    test_parse_documents_dir(td, None)
    print('Tests ran successfully')
