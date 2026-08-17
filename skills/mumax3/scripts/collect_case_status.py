#!/usr/bin/env python3
"""Collect conservative status information from mumax3 case folders.

The script reports files, logs, and metadata that are present on disk. It does
not claim that a simulation is physically correct or numerically converged.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


FIELDNAMES = [
    "case_id",
    "case_dir",
    "result_dir",
    "reported_status",
    "derived_status",
    "params_json",
    "manifest_json",
    "config_signature",
    "input_sha256",
    "dynamic_signature",
    "analysis_status",
    "manual_review_status",
    "provenance_state",
    "mx3_count",
    "out_dir_count",
    "ovf_count",
    "table_count",
    "stdout_log_count",
    "stderr_log_count",
    "stderr_nonempty",
    "error_message",
]


def load_params(path: Path) -> tuple[dict[str, Any], str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, ""
    except json.JSONDecodeError as exc:
        return {}, f"invalid params.json: {exc}"
    except OSError as exc:
        return {}, f"cannot read params.json: {exc}"
    if not isinstance(data, dict):
        return {}, "params.json is not a JSON object"
    return data, ""


def load_optional_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def first_value(data: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = data.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def find_manifest(case_dir: Path, root: Path) -> Path | None:
    for path in (
        case_dir / "manifest.json",
        case_dir / "case_manifest.json",
        root / "manifest.json",
        root / "case_manifest.json",
    ):
        if path.exists():
            return path
    return None


def find_case_dirs(root: Path, recursive: bool) -> list[Path]:
    if (root / "params.json").exists() or list(root.glob("*.mx3")):
        return [root]
    candidates = root.rglob("*") if recursive else root.iterdir()
    case_dirs: list[Path] = []
    for path in candidates:
        if not path.is_dir():
            continue
        if (path / "params.json").exists() or list(path.glob("*.mx3")):
            case_dirs.append(path)
    return sorted(set(case_dirs))


def count_nonempty(paths: list[Path]) -> int:
    count = 0
    for path in paths:
        try:
            if path.stat().st_size > 0:
                count += 1
        except OSError:
            continue
    return count


def derive_status(row: dict[str, Any]) -> str:
    if row["error_message"] or row["stderr_nonempty"]:
        return "needs_review"
    if row["provenance_state"] == "stale":
        return "stale"
    if row["manual_review_status"] not in {"", "review_pending"}:
        return "review_recorded"
    if row["analysis_status"] == "analysis_fresh":
        return "analysis_present"
    if row["ovf_count"] or row["table_count"]:
        return "outputs_present"
    if row["out_dir_count"]:
        return "output_dirs_present"
    if row["mx3_count"]:
        return "prepared"
    return "unknown"


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve().parent))
    except ValueError:
        return str(path)


def summarize_case(case_dir: Path, root: Path, result_root: Path | None = None) -> dict[str, Any]:
    params_path = case_dir / "params.json"
    params, error_message = load_params(params_path)
    try:
        relative_case = case_dir.resolve().relative_to(root.resolve())
    except ValueError:
        relative_case = Path(case_dir.name)
    result_dir = result_root / relative_case if result_root else case_dir
    manifest_path = find_manifest(case_dir, root)
    manifest = load_optional_json(manifest_path) if manifest_path else {}
    run_record = load_optional_json(case_dir / "run_record.json")
    analysis_record = load_optional_json(result_dir / "analysis_record.json")
    manual_review = load_optional_json(result_dir / "manual_review.json")

    config_signature = first_value(
        params,
        ("configuration_signature", "config_signature", "case_signature", "stage2_signature", "stage3_signature"),
    )
    input_sha256 = first_value(
        params,
        ("checkpoint_sha256", "static_input_sha256", "input_sha256", "h0_sha256"),
    )
    dynamic_signature = first_value(params, ("dynamic_signature", "stage3_signature"))
    analysis_signature = first_value(analysis_record, ("analysis_signature", "signature"))
    analysis_dynamic = first_value(analysis_record, ("dynamic_signature", "stage3_signature"))
    review_dynamic = first_value(manual_review, ("dynamic_signature", "stage3_signature"))
    review_analysis = first_value(manual_review, ("analysis_signature",))

    stale = False
    if dynamic_signature and analysis_dynamic and dynamic_signature != analysis_dynamic:
        stale = True
    if dynamic_signature and review_dynamic and dynamic_signature != review_dynamic:
        stale = True
    if analysis_signature and review_analysis and analysis_signature != review_analysis:
        stale = True

    if stale:
        provenance_state = "stale"
    elif config_signature or input_sha256 or dynamic_signature or manifest:
        provenance_state = "recorded"
    elif list(case_dir.glob("*.out/*.ovf")) or list(case_dir.glob("*.out/table.txt")):
        provenance_state = "unverified_outputs"
    else:
        provenance_state = "unrecorded"

    if analysis_record:
        analysis_status = "analysis_fresh" if not stale else "analysis_stale"
    else:
        analysis_status = ""
    manual_review_status = first_value(manual_review, ("status", "classification")) or (
        "review_pending" if analysis_record else ""
    )
    out_dirs = [path for path in case_dir.glob("*.out") if path.is_dir()]
    stdout_logs = list(case_dir.glob("logs/*stdout*.txt"))
    stderr_logs = list(case_dir.glob("logs/*stderr*.txt"))

    row: dict[str, Any] = {
        "case_id": str(params.get("case_id") or case_dir.name),
        "case_dir": display_path(case_dir, root),
        "result_dir": str(result_dir),
        "reported_status": first_value(run_record, ("status",)) or str(params.get("status", "")),
        "derived_status": "",
        "params_json": "yes" if params_path.exists() else "no",
        "manifest_json": str(manifest_path) if manifest_path else "",
        "config_signature": config_signature,
        "input_sha256": input_sha256,
        "dynamic_signature": dynamic_signature,
        "analysis_status": analysis_status,
        "manual_review_status": manual_review_status,
        "provenance_state": provenance_state,
        "mx3_count": len(list(case_dir.glob("*.mx3"))),
        "out_dir_count": len(out_dirs),
        "ovf_count": len(list(case_dir.glob("*.out/*.ovf"))),
        "table_count": len(list(case_dir.glob("*.out/table.txt"))),
        "stdout_log_count": len(stdout_logs),
        "stderr_log_count": len(stderr_logs),
        "stderr_nonempty": count_nonempty(stderr_logs),
        "error_message": error_message or str(params.get("error_message", "")),
    }
    row["derived_status"] = derive_status(row)
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect conservative mumax3 case status rows.")
    parser.add_argument("root", type=Path, help="case directory or directory containing case directories")
    parser.add_argument("--recursive", action="store_true", help="scan nested directories for cases")
    parser.add_argument("--result-root", type=Path, help="parallel result root containing analysis and manual-review records")
    parser.add_argument("--csv", type=Path, help="write a CSV summary")
    parser.add_argument("--json", type=Path, help="write a JSON summary")
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    root = args.root
    if not root.exists():
        print(f"{root}: does not exist", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"{root}: expected a directory", file=sys.stderr)
        return 2

    case_dirs = find_case_dirs(root, args.recursive)
    rows = [summarize_case(case_dir, root, args.result_root) for case_dir in case_dirs]

    if args.csv:
        write_csv(args.csv, rows)
        print(f"Wrote {args.csv}")
    if args.json:
        write_json(args.json, rows)
        print(f"Wrote {args.json}")
    if not args.csv and not args.json:
        writer = csv.DictWriter(sys.stdout, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
