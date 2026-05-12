#!/usr/bin/env python3
"""Local release-candidate validation for MumaxWriter.skill.

The checks are intentionally conservative and dependency-light. They do not
prove physical correctness of any mumax3 simulation.
"""

from __future__ import annotations

import json
import py_compile
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
]

TEMPLATE_PARAM_MAP = {
    "minimal_relax.mx3.template": ROOT / "examples" / "template_params" / "minimal_relax.params.example.json",
    "thin_film_with_region.mx3.template": ROOT / "examples" / "template_params" / "thin_film_with_region.params.example.json",
    "local_ac_field.mx3.template": ROOT / "examples" / "template_params" / "local_ac_field.params.example.json",
}

SENSITIVE_TERMS = [
    "ROG-ZG16-MSJS",
    "CodexSandboxOffline",
    "notes_CDW",
    "SWlens",
    "domain_wall_scripts_analysis",
    "parameter_sweep_planning_tasklist",
]

SCAN_SUFFIXES = {".md", ".py", ".mx3", ".template", ".json", ".yaml", ".yml", ".txt"}
EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", "runs", "results", "external_reference_cache"}
EXCLUDED_FILES = {
    Path("tests") / "validate_release.py",
    Path("docs") / "research" / "mumax3_script_language_and_api.md",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run(cmd: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


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


def check_helper_compilation(failures: list[str]) -> None:
    for script in HELPER_SCRIPTS:
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"{rel(script)} failed py_compile: {exc.msg}")
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
    return sorted((ROOT / "examples" / "expected_outputs").rglob("*.mx3"))


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


def check_mumax_vet(failures: list[str]) -> None:
    mumax = shutil.which("mumax3")
    if not mumax:
        print("SKIP: mumax3 not found on PATH; skipping mumax3 -vet")
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


def iter_scannable_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if relative in EXCLUDED_FILES:
            continue
        if any(part in EXCLUDED_DIR_NAMES for part in relative.parts):
            continue
        if path.suffix in SCAN_SUFFIXES or path.name in {"CHANGELOG.md", "LICENSE"}:
            files.append(path)
    return files


def check_sensitive_terms(failures: list[str]) -> None:
    hits: list[str] = []
    for path in iter_scannable_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for term in SENSITIVE_TERMS:
            if term in text:
                hits.append(f"{rel(path)}: {term}")
    if hits:
        failures.append("sensitive-term scan found blocked terms")
        print("FAIL: sensitive-term scan")
        for hit in hits:
            print(f"  {hit}")
    else:
        print("PASS: sensitive-term scan")


def main() -> int:
    failures: list[str] = []
    check_skill_metadata(failures)
    check_helper_compilation(failures)
    check_templates(failures)
    check_static_warnings(failures)
    check_mumax_vet(failures)
    check_sensitive_terms(failures)

    if failures:
        print("\nValidation failed:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
