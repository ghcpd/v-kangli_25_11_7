import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def run_cli():
    cmd = ["python", "-m", "kgeb.cli", "--documents", str(ROOT / "documents.txt"), "--entities", str(ROOT / "entities.json"), "--entities-output", str(ROOT / "entities_output.json"), "--relations-output", str(ROOT / "relations_output.json"), "--gold-entities", str(ROOT / "gold_entities.json"), "--gold-relations", str(ROOT / "gold_relations.json"), "--evaluation-output", str(ROOT / "evaluation_report.json")]
    subprocess.check_call(cmd)


def test_run_pipeline(tmp_path):
    # run the CLI to produce outputs
    run_cli()
    # check outputs exist
    assert (ROOT / "entities_output.json").exists()
    assert (ROOT / "relations_output.json").exists()
    assert (ROOT / "evaluation_report.json").exists()

    with open(ROOT / "evaluation_report.json", encoding="utf-8") as f:
        report = json.load(f)

    assert "entity_f1" in report or "entity_f1" in report
