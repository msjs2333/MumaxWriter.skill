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
    "reported_status",
    "derived_status",
    "params_json",
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


def summarize_case(case_dir: Path, root: Path) -> dict[str, Any]:
    params_path = case_dir / "params.json"
    params, error_message = load_params(params_path)
    out_dirs = [path for path in case_dir.glob("*.out") if path.is_dir()]
    stdout_logs = list(case_dir.glob("logs/*stdout*.txt"))
    stderr_logs = list(case_dir.glob("logs/*stderr*.txt"))

    row: dict[str, Any] = {
        "case_id": str(params.get("case_id") or case_dir.name),
        "case_dir": display_path(case_dir, root),
        "reported_status": str(params.get("status", "")),
        "derived_status": "",
        "params_json": "yes" if params_path.exists() else "no",
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
    rows = [summarize_case(case_dir, root) for case_dir in case_dirs]

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
