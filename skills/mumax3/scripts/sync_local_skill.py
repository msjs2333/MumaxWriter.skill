#!/usr/bin/env python3
"""Safely synchronize the maintained mumax3 skill into a local Codex install."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path


IGNORED_NAMES = {"__pycache__", ".pytest_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def default_source() -> Path:
    return Path(__file__).resolve().parents[1]


def default_target() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "skills" / "mumax3"


def include(path: Path) -> bool:
    return not any(part in IGNORED_NAMES for part in path.parts) and path.suffix not in IGNORED_SUFFIXES


def file_manifest(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not root.exists():
        return result
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if not include(relative):
            continue
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        result[relative.as_posix()] = digest.hexdigest()
    return result


def validate_paths(source: Path, target: Path) -> None:
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"{source}: source does not contain SKILL.md")
    resolved_target = target.resolve()
    if resolved_target.name.lower() != "mumax3" or resolved_target.parent.name.lower() != "skills":
        raise SystemExit(f"{target}: target must be an exact .../skills/mumax3 directory")
    if source.resolve() == resolved_target:
        raise SystemExit("source and target must be different directories")


def changes(source_manifest: dict[str, str], target_manifest: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    added = sorted(source_manifest.keys() - target_manifest.keys())
    removed = sorted(target_manifest.keys() - source_manifest.keys())
    changed = sorted(
        name
        for name in source_manifest.keys() & target_manifest.keys()
        if source_manifest[name] != target_manifest[name]
    )
    return added, changed, removed


def print_plan(source: Path, target: Path, added: list[str], changed: list[str], removed: list[str]) -> None:
    print(f"Source: {source}")
    print(f"Target: {target}")
    for label, names in (("ADD", added), ("CHANGE", changed), ("REMOVE", removed)):
        for name in names:
            print(f"{label}: {name}")
    print(f"Summary: add={len(added)} change={len(changed)} remove={len(removed)}")


def copy_source(source: Path, staging: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name in IGNORED_NAMES or Path(name).suffix in IGNORED_SUFFIXES
        }

    shutil.copytree(source, staging, ignore=ignore)


def apply_sync(source: Path, target: Path, backup_root: Path) -> Path | None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup: Path | None = None
    if target.exists():
        backup = backup_root / f"mumax3-{timestamp}"
        backup.parent.mkdir(parents=True, exist_ok=True)
        if backup.exists():
            raise SystemExit(f"{backup}: backup path already exists")
        shutil.copytree(target, backup)

    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.parent / f".mumax3-sync-{uuid.uuid4().hex}"
    try:
        copy_source(source, staging)
        if target.exists():
            shutil.rmtree(target)
        staging.replace(target)
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        if backup and backup.exists() and not target.exists():
            shutil.copytree(backup, target)
        raise

    source_manifest = file_manifest(source)
    target_manifest = file_manifest(target)
    if source_manifest != target_manifest:
        if backup and backup.exists():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(backup, target)
        raise SystemExit("post-sync hash verification failed; restored backup")
    return backup


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=default_source(), help="maintained mumax3 skill source")
    parser.add_argument("--target", type=Path, default=default_target(), help="local .../skills/mumax3 target")
    parser.add_argument("--backup-root", type=Path, help="backup directory; defaults beside the target skill")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="show changes without writing (default)")
    mode.add_argument("--apply", action="store_true", help="create a backup and apply the exact synchronization")
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    source = args.source.resolve()
    target = args.target.resolve()
    validate_paths(source, target)
    source_manifest = file_manifest(source)
    target_manifest = file_manifest(target)
    added, changed, removed = changes(source_manifest, target_manifest)
    print_plan(source, target, added, changed, removed)
    if not (added or changed or removed):
        print("Already synchronized.")
        return 0
    if not args.apply:
        print("Dry run only. Re-run with --apply to synchronize.")
        return 0
    backup_root = (args.backup_root or target.parent / ".mumax3-backups").resolve()
    backup = apply_sync(source, target, backup_root)
    print(f"Backup: {backup if backup else 'none (target did not exist)'}")
    print("Synchronization complete and hashes verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
