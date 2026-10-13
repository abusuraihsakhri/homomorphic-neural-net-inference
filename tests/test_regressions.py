"""Regression coverage for integrity, CSV parsing, API validation and metrics."""
import csv

from agents.base import AuditTrail
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from agents.metrics import GLOBAL_METRICS
from cli import main as primary_cli
from he_neural_inference.cli import main as legacy_cli


def test_hmac_detects_modified_signed_fields():
    audit = AuditTrail(secret_key="test-only-key")
    audit.log("worker", "system", "completed", {"result": "NOMINAL"})
    assert audit.verify_integrity()
    audit.logs[0]["actor"] = "modified"
    assert not audit.verify_integrity()


def test_hmac_detects_modified_chain_and_published_logs_are_copies():
    audit = AuditTrail(secret_key="test-only-key")
    audit.log("worker", "system", "first", {"value": 1})
    audit.log("worker", "system", "second", {"value": 2})
    snapshot = audit.get_trail()
    snapshot[0]["actor"] = "external-modification"
    assert audit.verify_integrity()
    audit.logs[1]["prev_hash"] = "modified"
    assert not audit.verify_integrity()


def test_false_boolean_csv_stays_false_in_both_clis(tmp_path):
    inp = tmp_path / "input.csv"
    inp.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "T1,SYNTHETIC,10,4,False,NOMINAL\n"
        "T2,SYNTHETIC,10,4,True,NOMINAL\n",
        encoding="utf-8",
    )
    for cli_fn, field in ((primary_cli, "overall_urgency"), (legacy_cli, "overall_status")):
        out = tmp_path / (field + ".csv")
        assert cli_fn(["batch", "-i", str(inp), "-o", str(out)]) == 0
        with out.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        assert rows[0][field] in ("ROUTINE", "NOMINAL_OPTIMAL")
        assert rows[1][field] in ("CRITICAL_STAT_PANIC", "CRITICAL_INTERVENTION_REQUIRED")


def test_bad_csv_boolean_does_not_produce_output(tmp_path):
    inp = tmp_path / "bad.csv"
    inp.write_text(
        "task_id,target_identifier,primary_metric,is_critical_flag\n"
        "T1,SYNTHETIC,10,not-a-bool\n", encoding="utf-8"
    )
    out = tmp_path / "out.csv"
    assert primary_cli(["batch", "-i", str(inp), "-o", str(out)]) == 1
    assert not out.exists()


def test_metrics_track_processing_not_unique_dossiers():
    old = GLOBAL_METRICS.tasks_total
    sup = SystemSupervisor()
    payload = SystemTaskPayload(task_id="SYNTHETIC", target_identifier="KEY-01", primary_metric=1)
    sup.process_task(payload)
    sup.process_task(payload)
    assert GLOBAL_METRICS.tasks_total == old + 2


def test_api_rejects_nested_identifiers_and_nonfinite_numbers():
    from fastapi.testclient import TestClient
    from agents.api import app
    client = TestClient(app)
    base = {"task_id": "T1", "target_identifier": "SYNTHETIC",
            "primary_metric": 5, "secondary_metric": 1, "status_descriptor": "NOMINAL"}
    rejected = client.post("/api/audit", json={**base, "attributes": {"contact": "name@example.com"}})
    assert rejected.status_code == 400
    rejected = client.post("/api/audit", json={**base, "primary_metric": "Infinity"})
    assert rejected.status_code == 422
    accepted = client.post("/api/audit", json=base)
    assert accepted.status_code == 200
    assert accepted.json()["overall_urgency"] == "ROUTINE"


def test_export_escapes_spreadsheet_formulas(tmp_path):
    inp = tmp_path / "formulas.csv"
    inp.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "=1+2,SYNTHETIC,5,0,False,NOMINAL\n", encoding="utf-8"
    )
    out = tmp_path / "result.csv"
    assert primary_cli(["batch", "-i", str(inp), "-o", str(out)]) == 0
    with out.open(newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))
    assert row["task_id"] == "'=1+2"

def test_negative_numeric_values_remain_reimportable(tmp_path):
    inp = tmp_path / "numbers.csv"
    inp.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "T1,SYNTHETIC,-3,-2,False,NOMINAL\n", encoding="utf-8"
    )
    for cli_fn in (primary_cli, legacy_cli):
        first = tmp_path / (cli_fn.__module__.replace(".", "_") + ".csv")
        second = tmp_path / (cli_fn.__module__.replace(".", "_") + "_second.csv")
        assert cli_fn(["batch", "-i", str(inp), "-o", str(first)]) == 0
        with first.open(newline="", encoding="utf-8") as handle:
            row = next(csv.DictReader(handle))
        assert row["primary_metric"] == "-3"
        assert row["secondary_metric"] == "-2"
        assert cli_fn(["batch", "-i", str(first), "-o", str(second)]) == 0

def test_legacy_coordinator_rejects_nonfinite_metrics():
    from he_neural_inference.models import FrontierPayload
    from he_neural_inference.agents import HENeuralInferenceCoordinator
    from pytest import raises
    payload = FrontierPayload("T", "SYNTHETIC", float("nan"), 1, "NOMINAL")
    with raises(ValueError, match="finite"):
        HENeuralInferenceCoordinator().process(payload)


def test_simulation_rejects_zero_iterations():
    from simulator import run_simulation
    from pytest import raises
    with raises(ValueError, match="positive"):
        run_simulation(0)
