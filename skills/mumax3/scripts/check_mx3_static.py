#!/usr/bin/env python3
"""Conservative static warnings for mumax3 .mx3 scripts.

This checker catches common Go/mumax3 boundary mistakes. It does not parse
mumax3 fully and does not prove that a script is semantically correct.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN_STATEMENTS = {
    "package": "mumax3 scripts are not Go packages",
    "import": "Go imports are not available in .mx3 scripts",
    "func": "custom Go function declarations are not supported",
    "type": "Go type declarations are not supported",
    "struct": "Go structs are not supported",
    "interface": "Go interfaces are not supported",
    "go": "goroutines are not supported",
    "chan": "channels are not supported",
    "select": "select statements are not supported",
    "switch": "switch statements are not supported",
    "range": "range loops are not supported",
    "return": "return statements are not supported",
    "break": "break statements are not supported",
    "continue": "continue statements are not supported",
    "defer": "defer is not supported",
    "goto": "goto is not supported",
}

GO_PACKAGE_SELECTORS = [
    "fmt.",
    "math.",
    "os.",
    "strings.",
    "strconv.",
    "filepath.",
    "regexp.",
    "json.",
    "ioutil.",
]

ASSIGN_RE = re.compile(r"(?<![<>=!:+*/%^-])(:=|=)(?!=)")


def strip_strings_and_comments(line: str, in_block_comment: bool) -> tuple[str, bool]:
    out: list[str] = []
    i = 0
    in_string = False
    quote = ""
    while i < len(line):
        ch = line[i]
        nxt = line[i + 1] if i + 1 < len(line) else ""
        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue
        if in_string:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                in_string = False
                quote = ""
            out.append(" ")
            i += 1
            continue
        if ch in ('"', "`"):
            in_string = True
            quote = ch
            out.append(" ")
            i += 1
            continue
        if ch == "/" and nxt == "/":
            break
        if ch == "/" and nxt == "*":
            in_block_comment = True
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out), in_block_comment


def warn(warnings: list[str], path: Path, line_no: int | None, message: str) -> None:
    loc = f"{path}:{line_no}" if line_no is not None else str(path)
    warnings.append(f"{loc}: warning: {message}")


def check_text(path: Path, text: str) -> list[str]:
    warnings: list[str] = []
    clean_lines: list[str] = []
    in_block = False

    for line_no, raw in enumerate(text.splitlines(), start=1):
        clean, in_block = strip_strings_and_comments(raw, in_block)
        clean_lines.append(clean)
        stripped = clean.strip().lstrip("\ufeff")
        if not stripped:
            continue

        first = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\b", stripped)
        if first and first.group(1) in FORBIDDEN_STATEMENTS:
            keyword = first.group(1)
            warn(warnings, path, line_no, f"`{keyword}`: {FORBIDDEN_STATEMENTS[keyword]}")

        for selector in GO_PACKAGE_SELECTORS:
            if selector in clean:
                warn(warnings, path, line_no, f"`{selector}` looks like Go standard library usage; use mumax3 built-ins or Python orchestration")

        if "^" in clean:
            warn(warnings, path, line_no, "`^` is not power in mumax3 scripts; use `pow(x, y)`")

        match = ASSIGN_RE.search(clean)
        if match:
            lhs = clean[: match.start()]
            if "," in lhs:
                warn(warnings, path, line_no, "multiple assignment is suspicious in mumax3 scripts")

    clean_text = "\n".join(clean_lines)
    has_mesh = ("SetGridSize" in clean_text and "SetCellSize" in clean_text) or "SetMesh" in clean_text
    has_output = any(token in clean_text for token in ("Save(", "SaveAs(", "AutoSave(", "TableAutoSave(", "TableSave(", "Snapshot("))

    if not has_mesh:
        warn(warnings, path, None, "missing obvious mesh setup (`SetGridSize` + `SetCellSize`, or `SetMesh`)")
    if not has_output:
        warn(warnings, path, None, "missing obvious output pattern (`Save`, `SaveAs`, `AutoSave`, `TableAutoSave`, or `TableSave`)")

    return warnings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Warn about common mumax3 script anti-patterns.")
    parser.add_argument("paths", nargs="+", help=".mx3 files to check")
    args = parser.parse_args(argv)

    all_warnings: list[str] = []
    exit_code = 0
    for name in args.paths:
        path = Path(name)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"{path}: error: {exc}", file=sys.stderr)
            exit_code = 2
            continue
        all_warnings.extend(check_text(path, text))

    for item in all_warnings:
        print(item)
    if not all_warnings and exit_code == 0:
        print("No static warnings.")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
