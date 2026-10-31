#!/usr/bin/env python3
"""Local release-candidate validation for MumaxWriter.skill.

The checks are intentionally conservative and dependency-light. They do not
prove physical correctness of any mumax3 simulation.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "mumax3"

HELPER_SCRIPTS = [
    SKILL / "scripts" / "check_mx3_static.py",
    SKILL / "scripts" / "render_template.py",
    SKILL / "scripts" / "collect_case_status.py",
    SKILL / "scripts" / "sync_local_skill.py",
    SKILL / "scripts" / "analyze_tutorial.py",
    SKILL / "scripts" / "analyze_edge_canting.py",
    ROOT / "examples" / "expected_outputs" / "parameterize_field_frequency_sweep" / "generate_field_frequency_sweep.py",
]

TEMPLATE_PARAM_MAP = {
    "minimal_relax.mx3.template": ROOT / "examples" / "template_params" / "minimal_relax.params.example.json",
    "thin_film_with_region.mx3.template": ROOT / "examples" / "template_params" / "thin_film_with_region.params.example.json",
    "local_ac_field.mx3.template": ROOT / "examples" / "template_params" / "local_ac_field.params.example.json",
}

# Detect accidentally embedded local home paths without retaining private names.
PRIVATE_PATH = re.compile(r"(?i)(?:[a-z]:[\\/]Users[\\/]|/(?:home|Users)/)[^<>\s`\\/]+[\\/]")

SCAN_SUFFIXES = {".md", ".py", ".mx3", ".template", ".json", ".yaml", ".yml", ".txt"}
MAINTAINED_SCAN_ROOTS = (SKILL, ROOT / "docs", ROOT / "examples", ROOT / "tests")
MAINTAINED_SCAN_FILES = (
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "README.ja.md",
    ROOT / "CHANGELOG.md",
    ROOT / "LICENSE",
)
MAINTAINED_TOP_LEVEL_DIRS = {"skills", "docs", "examples", "tests"}
MAINTAINED_TOP_LEVEL_FILES = {path.name for path in MAINTAINED_SCAN_FILES}



def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run(cmd: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )


def check(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS: {message}")
    else:
        print(f"FAIL: {message}")
        failures.append(message)


def check_skill_metadata(failures: list[str]) -> None:
    path = SKILL / "SKILL.md"
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    has_frontmatter = text.startswith("---\n") and "\n---\n" in text[4:]
    check(has_frontmatter, "SKILL.md has YAML frontmatter fence", failures)
    if not has_frontmatter:
        return
    frontmatter = text.split("---", 2)[1]
    check("name: mumax3" in frontmatter, "SKILL.md frontmatter has name: mumax3", failures)
    check("description:" in frontmatter and ".mx3" in frontmatter, "SKILL.md frontmatter has useful description", failures)


def local_reference_links(skill: Path = SKILL) -> list[str]:
    skill_text = (skill / "SKILL.md").read_text(encoding="utf-8-sig")
    return sorted(set(re.findall(r"references/[A-Za-z0-9_./-]+\.md", skill_text)))


def missing_local_reference_links(skill: Path = SKILL) -> list[str]:
    return [link for link in local_reference_links(skill) if not (skill / link).is_file()]


def check_reference_links(failures: list[str]) -> None:
    links = local_reference_links()
    check(bool(links), "SKILL.md routes to local references", failures)
    for link in missing_local_reference_links():
        check(False, f"SKILL.md reference exists: {link}", failures)


def check_helper_compilation(failures: list[str]) -> None:
    for script in HELPER_SCRIPTS:
        try:
            compile(script.read_text(encoding="utf-8-sig"), str(script), "exec")
        except (OSError, SyntaxError) as exc:
            failures.append(f"{rel(script)} failed syntax compilation: {exc}")
            print(f"FAIL: {rel(script)} compiles")
        else:
            print(f"PASS: {rel(script)} compiles")


def check_templates(failures: list[str]) -> None:
    renderer = SKILL / "scripts" / "render_template.py"
    for template_name, params in TEMPLATE_PARAM_MAP.items():
        template = SKILL / "assets" / "templates" / template_name
        check(template.exists(), f"{rel(template)} exists", failures)
        check(params.exists(), f"{rel(params)} exists", failures)
        if not template.exists() or not params.exists():
            continue
        try:
            data = json.loads(params.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{rel(params)} invalid JSON: {exc}")
            print(f"FAIL: {rel(params)} is valid JSON")
            continue
        check(isinstance(data, dict), f"{rel(params)} is a JSON object", failures)
        proc = run([sys.executable, str(renderer), str(template), "--params", str(params), "--check"])
        if proc.returncode == 0:
            print(f"PASS: {rel(template)} placeholders resolve with {rel(params)}")
        else:
            failures.append(f"{rel(template)} placeholder check failed: {proc.stderr.strip()}")
            print(f"FAIL: {rel(template)} placeholders resolve with {rel(params)}")


def expected_mx3_files() -> list[Path]:
    return sorted([*(ROOT / "examples" / "expected_outputs").rglob("*.mx3"),
                   *(SKILL / "examples").rglob("*.mx3")])


def check_static_warnings(failures: list[str]) -> None:
    scripts = expected_mx3_files()
    check(bool(scripts), "expected-output .mx3 scripts exist", failures)
    if not scripts:
        return
    checker = SKILL / "scripts" / "check_mx3_static.py"
    proc = run([sys.executable, str(checker), *map(str, scripts)])
    if proc.returncode == 0 and "warning:" not in proc.stdout:
        print("PASS: expected-output .mx3 scripts have no static warnings")
    else:
        failures.append("static checker reported warnings or failed")
        print("FAIL: expected-output .mx3 scripts have no static warnings")
        print(proc.stdout)
        print(proc.stderr)


def check_helper_tests(failures: list[str]) -> None:
    proc = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"])
    if proc.returncode == 0:
        print("PASS: helper regression tests")
    else:
        failures.append("helper regression tests failed")
        print("FAIL: helper regression tests")
        print(proc.stdout)
        print(proc.stderr)


def check_mumax_vet(failures: list[str], skipped: list[str]) -> None:
    mumax = shutil.which("mumax3")
    if not mumax:
        message = "mumax3 not found on PATH; mumax3 -vet was not run"
        skipped.append(message)
        print(f"SKIP: {message}")
        return
    for script in expected_mx3_files():
        proc = run([mumax, "-vet", str(script)])
        if proc.returncode == 0:
            print(f"PASS: mumax3 -vet {rel(script)}")
        else:
            failures.append(f"mumax3 -vet failed for {rel(script)}")
            print(f"FAIL: mumax3 -vet {rel(script)}")
            print(proc.stdout)
            print(proc.stderr)


def is_scannable(path: Path) -> bool:
    return path.suffix.lower() in SCAN_SUFFIXES or path.name in {"CHANGELOG.md", "LICENSE"}


def is_maintained_relative(path: Path) -> bool:
    return bool(path.parts) and (
        path.parts[0] in MAINTAINED_TOP_LEVEL_DIRS
        or (len(path.parts) == 1 and path.name in MAINTAINED_TOP_LEVEL_FILES)
    )


def iter_maintained_files() -> tuple[list[Path], str]:
    tracked = run(["git", "ls-files", "-z"])
    if tracked.returncode == 0:
        files: list[Path] = []
        for item in tracked.stdout.split("\0"):
            relative = Path(item)
            path = ROOT / relative
            if item and is_maintained_relative(relative) and path.is_file() and is_scannable(path):
                files.append(path)
        return files, "git-tracked maintained files"

    files: list[Path] = []
    for root in MAINTAINED_SCAN_ROOTS:
        if root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file() and is_scannable(path))
    files.extend(path for path in MAINTAINED_SCAN_FILES if path.is_file() and is_scannable(path))
    return files, "explicit maintained roots (git unavailable)"


def check_sensitive_terms(failures: list[str]) -> None:
    hits: list[str] = []
    files, scope = iter_maintained_files()
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PRIVATE_PATH.search(text):
            hits.append(f"{rel(path)}: literal local home path")
    if hits:
        failures.append("local-path scan found blocked terms")
        print(f"FAIL: local-path scan ({scope})")
        for hit in hits:
            print(f"  {hit}")
    else:
        print(f"PASS: local-path scan ({scope})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a MumaxWriter.skill release candidate.")
    parser.add_argument(
        "--scope",
        choices=("docs", "helpers", "full"),
        default="full",
        help="docs checks metadata, reference links, and local home paths; helpers adds helper checks; full adds templates, static checks, and mumax3 -vet.",
    )
    scope = parser.parse_args().scope
    failures: list[str] = []
    skipped: list[str] = []
    check_skill_metadata(failures)
    check_reference_links(failures)
    check_sensitive_terms(failures)

    if scope in {"helpers", "full"}:
        check_helper_compilation(failures)
        check_helper_tests(failures)

    if scope == "full":
        check_templates(failures)
        check_static_warnings(failures)
        check_mumax_vet(failures, skipped)

    if failures:
        print("\nValidation failed:")
        for item in failures:
            print(f"- {item}")
        return 1
    if skipped:
        print("\nValidation completed with skipped checks (not a full acceptance):")
        for item in skipped:
            print(f"- {item}")
    else:
        print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
