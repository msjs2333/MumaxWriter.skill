#!/usr/bin/env python3
"""Render simple {{placeholder}} mumax3 templates.

This helper performs deterministic text substitution only. It does not validate
mumax3 physics or prove that the rendered script is semantically correct.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


def load_json_mapping(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"{path}: error: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a JSON object")
    return data


def parse_set_value(item: str) -> tuple[str, str]:
    if "=" not in item:
        raise argparse.ArgumentTypeError("expected KEY=VALUE")
    key, value = item.split("=", 1)
    if not PLACEHOLDER_RE.fullmatch("{{" + key + "}}"):
        raise argparse.ArgumentTypeError(f"invalid placeholder name: {key!r}")
    return key, value


def value_to_text(value: Any, key: str) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float, str)):
        return str(value)
    raise SystemExit(f"{key}: unsupported value type {type(value).__name__}; use a string, number, or boolean")


def render(template: str, values: dict[str, Any]) -> tuple[str, list[str]]:
    missing: list[str] = []

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            missing.append(key)
            return match.group(0)
        return value_to_text(values[key], key)

    return PLACEHOLDER_RE.sub(replace, template), sorted(set(missing))


def find_placeholders(template: str) -> list[str]:
    return sorted(set(PLACEHOLDER_RE.findall(template)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a mumax3 {{placeholder}} template.")
    parser.add_argument("template", type=Path, help="input .mx3.template file")
    parser.add_argument("-p", "--params", type=Path, help="JSON object with placeholder values")
    parser.add_argument("-s", "--set", action="append", default=[], type=parse_set_value, metavar="KEY=VALUE", help="override or add one placeholder value")
    parser.add_argument("-o", "--output", type=Path, help="output .mx3 path; stdout is used when omitted")
    parser.add_argument("--list", action="store_true", help="list placeholders and exit")
    parser.add_argument("--check", action="store_true", help="fail if placeholders are missing, but do not write output")
    parser.add_argument("--force", action="store_true", help="overwrite an existing output file")
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    try:
        template = args.template.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{args.template}: error: {exc}", file=sys.stderr)
        return 2

    if args.list:
        for name in find_placeholders(template):
            print(name)
        return 0

    values: dict[str, Any] = {}
    if args.params:
        values.update(load_json_mapping(args.params))
    values.update(dict(args.set))

    rendered, missing = render(template, values)
    if missing:
        print("missing placeholder values: " + ", ".join(missing), file=sys.stderr)
        return 1

    if args.check:
        print("Template placeholders are fully resolved.")
        return 0

    if args.output:
        if args.output.exists() and not args.force:
            print(f"{args.output}: already exists; use --force to overwrite", file=sys.stderr)
            return 1
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
