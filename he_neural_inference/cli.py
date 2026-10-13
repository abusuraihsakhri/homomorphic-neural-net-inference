"""
Command-Line Interface for HE-NeuralInference: Polynomial Activation Encrypted Medical Classifier Agent.
"""
import argparse
import csv
import json
import math
import math
import os
import sys
from .models import FrontierPayload
from .agents import HENeuralInferenceCoordinator

coordinator = HENeuralInferenceCoordinator()


def finite_float(value):
    try:
        result = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected a finite number") from exc
    if not math.isfinite(result):
        raise argparse.ArgumentTypeError("Expected a finite number")
    return result


def safe_csv_row(row):
    """Escape spreadsheet expressions while preserving ordinary signed numbers."""
    def protect(value):
        if not isinstance(value, str):
            return value
        trimmed = value.lstrip()
        if trimmed.startswith(("+", "-")):
            try:
                if math.isfinite(float(trimmed)):
                    return value
            except ValueError:
                pass
        if trimmed.startswith(("=", "+", "-", "@")):
            return "'" + value
        return value

    return {key: protect(value) for key, value in row.items()}


def parse_csv_bool(value):
    """Parse boolean text explicitly instead of bool("False")."""
    normalized = str(value if value is not None else "").strip().lower()
    if normalized in ("", "false", "0", "no", "n", "f"):
        return False
    if normalized in ("true", "1", "yes", "y", "t"):
        return True
    raise ValueError(f"Invalid is_critical_flag value: {value!r}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="homomorphic-neural-net-inference", description="HE-NeuralInference: Polynomial Activation Encrypted Medical Classifier Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Audit
    p_audit = subparsers.add_parser("audit", help="Run single task evaluation")
    p_audit.add_argument("--task-id", default="TASK-2026-001")
    p_audit.add_argument("--target", default="TARGET-GEN-01")
    p_audit.add_argument("--primary", type=finite_float, default=29.4)
    p_audit.add_argument("--secondary", type=finite_float, default=15.1)
    p_audit.add_argument("--critical", action="store_true")
    p_audit.add_argument("--status", default="DISCORDANT")

    # Chat
    p_chat = subparsers.add_parser("chat", help="System configuration query")
    p_chat.add_argument("query", nargs="+")

    # Batch
    p_batch = subparsers.add_parser("batch", help="Batch process CSV records")
    p_batch.add_argument("-i", "--input", required=True)
    p_batch.add_argument("-o", "--output", default="results.csv")

    # Serve
    p_serve = subparsers.add_parser("serve", help="Launch FastAPI REST server")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)

    if args.command == "audit":
        payload = FrontierPayload(
            task_id=args.task_id,
            target_identifier=args.target,
            primary_metric=args.primary,
            secondary_metric=args.secondary,
            status_descriptor=args.status,
            is_critical_flag=args.critical,
        )
        dossier = coordinator.process(payload)
        print("=" * 80)
        print(f"  HE-NEURALINFERENCE: POLYNOMIAL ACTIVATION ENCRYPTED MEDICAL CLASSIFIER AGENT")
        print("  Mode: Threshold-rule demonstration; no homomorphic encryption or neural-network inference")
        print(f"  Task: {dossier['task_id']} | Status: [{dossier['overall_status']}] | Total Alerts: {dossier['total_alerts']}")
        print("=" * 80)
        for a in dossier["alerts"]:
            print(f"\n  [{a['status']}] from {a['origin_agent']}:")
            print(f"  Summary: {a['summary']}")
            print(f"  Details: {a['technical_details']}")
            print(f"  Action:  {a['actionable_remediation']}")
        print("\n" + "=" * 80)
        return 0

    if args.command == "chat":
        ans = coordinator.query_supervisory_chat(" ".join(args.query))
        print(f"\n[HENeuralInferenceCoordinator]:\n{ans}\n")
        return 0

    if args.command == "batch":
        if not os.path.isfile(args.input):
            print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
            return 1
        with open(args.input, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
        if any(None in row for row in rows):
            print("Error: CSV row contains more fields than the header.", file=sys.stderr)
            return 1

        required = {"task_id", "target_identifier", "primary_metric"}
        if not required.issubset(fieldnames):
            print(f"Error: Missing CSV columns: {', '.join(sorted(required - set(fieldnames)))}", file=sys.stderr)
            return 1
        out_fields = list(dict.fromkeys(fieldnames + ["overall_status", "total_alerts", "critical_count", "consensus_summary"]))
        out_rows = []
        for row_num, r in enumerate(rows, 2):
            try:
                payload = FrontierPayload(
                    task_id=r.get("task_id", ""),
                    target_identifier=r.get("target_identifier", ""),
                    primary_metric=float(r.get("primary_metric", "")),
                    secondary_metric=float(r.get("secondary_metric") or 0.0),
                    status_descriptor=r.get("status_descriptor") or "NOMINAL",
                    is_critical_flag=parse_csv_bool(r.get("is_critical_flag")),
                )
                dossier = coordinator.process(payload)
            except (ValueError, TypeError) as exc:
                print(f"Error in CSV row {row_num}: {exc}", file=sys.stderr)
                return 1
            row_dict = dict(r)
            row_dict["overall_status"] = dossier["overall_status"]
            row_dict["total_alerts"] = dossier["total_alerts"]
            row_dict["critical_count"] = dossier["critical_count"]
            row_dict["consensus_summary"] = dossier["consensus_summary"]
            out_rows.append(row_dict)

        if any(name.lstrip().startswith(("=", "+", "-", "@")) for name in fieldnames):
            print("Error: CSV column names must not be spreadsheet formulas.", file=sys.stderr)
            return 1
        with open(args.output, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=out_fields)
            writer.writeheader()
            writer.writerows(safe_csv_row(row) for row in out_rows)
        print(f"Processed {len(out_rows)} records -> {args.output}")
        return 0

    if args.command == "serve":
        try:
            import uvicorn
            from .server import create_app
            app = create_app()
            if app is None:
                print("FastAPI is not installed. Install the server extra.", file=sys.stderr)
                return 1
            print(f"Starting legacy rule API on http://{args.host}:{args.port}")
            uvicorn.run(app, host=args.host, port=args.port)
        except ImportError:
            print("FastAPI / uvicorn not installed. Run 'pip install fastapi uvicorn'")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
