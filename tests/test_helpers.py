from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "mumax3"
CHECKER = SKILL / "scripts" / "check_mx3_static.py"
COLLECTOR = SKILL / "scripts" / "collect_case_status.py"
SYNC = SKILL / "scripts" / "sync_local_skill.py"


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )


class StaticCheckerTests(unittest.TestCase):
    def test_lowercase_template_and_b1_are_accepted(self) -> None:
        script = """\
setgridsize({{nx}}, 8, 1)
setcellsize(2e-9, 2e-9, 2e-9)
b1 := rect(10e-9, 10e-9)
defregion(1, b1)
Ku1.setregion(1, 1.5e5)
DisableZhangLiTorque = true
FixedLayerPosition = FIXEDLAYER_TOP
sotMask := LoadFile("sot_mask.ovf")
B_ext.Add(sotMask, 1e-3*sin(2*pi*1e9*t))
run(1e-9)
B_ext.RemoveExtraTerms()
saveas(m, "m_final.ovf")
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "case.mx3.template"
            path.write_text(script, encoding="utf-8")
            proc = run(str(CHECKER), str(path))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("warning:", proc.stdout)

    def test_protected_identifiers_still_warn(self) -> None:
        script = """\
SetGridSize(8, 8, 1)
SetCellSize(2e-9, 2e-9, 2e-9)
mu0 := 1
SaveAs(m, "m.ovf")
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "case.mx3"
            path.write_text(script, encoding="utf-8")
            proc = run(str(CHECKER), str(path))
        self.assertIn("`mu0` is a mumax3 built-in identifier", proc.stdout)

    def test_loop_table_column_and_euler_without_fixdt_warn(self) -> None:
        script = """\
SetGridSize(8, 8, 1)
SetCellSize(2e-9, 2e-9, 2e-9)
SetSolver(1)
for i := 0; i < 2; i++ {
    TableAddVar(i, "i", "")
}
SaveAs(m, "m.ovf")
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "case.mx3"
            path.write_text(script, encoding="utf-8")
            proc = run(str(CHECKER), str(path))
        self.assertIn("`TableAddVar` adds table columns", proc.stdout)
        self.assertIn("requires an explicit `FixDt = ...`", proc.stdout)


class StatusCollectorTests(unittest.TestCase):
    def test_reports_fresh_analysis_and_manual_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            run_root = base / "runs"
            result_root = base / "results"
            case = run_root / "case_a"
            result = result_root / "case_a"
            (case / "stage.out").mkdir(parents=True)
            result.mkdir(parents=True)
            (case / "stage.out" / "m000001.ovf").write_bytes(b"ovf")
            (case / "params.json").write_text(
                json.dumps(
                    {
                        "case_id": "case_a",
                        "configuration_signature": "cfg",
                        "checkpoint_sha256": "input",
                        "dynamic_signature": "dyn",
                    }
                ),
                encoding="utf-8",
            )
            (run_root / "manifest.json").write_text("{}", encoding="utf-8")
            (result / "analysis_record.json").write_text(
                json.dumps({"analysis_signature": "ana", "dynamic_signature": "dyn"}),
                encoding="utf-8",
            )
            (result / "manual_review.json").write_text(
                json.dumps({"status": "retained", "dynamic_signature": "dyn", "analysis_signature": "ana"}),
                encoding="utf-8",
            )
            proc = run(
                str(COLLECTOR),
                str(run_root),
                "--result-root",
                str(result_root),
                "--recursive",
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        rows = list(csv.DictReader(proc.stdout.splitlines()))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["analysis_status"], "analysis_fresh")
        self.assertEqual(rows[0]["manual_review_status"], "retained")
        self.assertEqual(rows[0]["provenance_state"], "recorded")


class SyncSkillTests(unittest.TestCase):
    def test_dry_run_then_exact_apply_with_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "source" / "mumax3"
            target = base / "install" / "skills" / "mumax3"
            backup_root = base / "backups"
            source.mkdir(parents=True)
            target.mkdir(parents=True)
            (source / "SKILL.md").write_text("---\nname: mumax3\n---\n", encoding="utf-8")
            (source / "new.txt").write_text("new\n", encoding="utf-8")
            (target / "SKILL.md").write_text("old\n", encoding="utf-8")
            (target / "project_model.md").write_text("stale\n", encoding="utf-8")

            dry = run(str(SYNC), "--source", str(source), "--target", str(target), "--dry-run")
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertTrue((target / "project_model.md").exists())
            self.assertIn("REMOVE: project_model.md", dry.stdout)

            applied = run(
                str(SYNC),
                "--source",
                str(source),
                "--target",
                str(target),
                "--backup-root",
                str(backup_root),
                "--apply",
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertFalse((target / "project_model.md").exists())
            self.assertEqual((target / "new.txt").read_text(encoding="utf-8"), "new\n")
            backups = list(backup_root.glob("mumax3-*"))
            self.assertEqual(len(backups), 1)
            self.assertTrue((backups[0] / "project_model.md").exists())


class ReferenceContractTests(unittest.TestCase):
    def test_skill_reference_links_exist(self) -> None:
        text = normalized_text(SKILL / "SKILL.md")
        links = sorted(set(re.findall(r"references/[A-Za-z0-9_./-]+\.md", text)))
        self.assertTrue(links)
        for link in links:
            with self.subTest(link=link):
                self.assertTrue((SKILL / link).is_file())

    def test_four_safety_invariants_are_explicit(self) -> None:
        text = normalized_text(SKILL / "SKILL.md")
        required = (
            "**Single writer:**",
            "**SHA256 lineage:**",
            "**All-vector decision gates:**",
            "**Manual/automatic separation:**",
            "`mx`",
            "`my`",
            "`mz`",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_workflow_and_output_contracts_are_routed(self) -> None:
        workflow = normalized_text(SKILL / "references" / "project_workflows.md")
        output = normalized_text(SKILL / "references" / "output_and_reproducibility.md")
        workflow_fragments = (
            "## State Safety Primitives",
            "`execution_state`",
            "## Decision Contracts And Ancestor Gates",
            "`monitor_handoff.json`",
            "`cancelled_by_user`",
            "A GPU lease is capacity scheduling",
        )
        output_fragments = (
            "## Output Directory Contract",
            "`execution_succeeded_reconciliation_required`",
            "## Timeline And Completion Contract",
            "repository-relative path",
            "## Output And Sampling Profiles",
            "## Analysis Products And Plot Profiles",
            "## Retention And Safe Release",
            "every destructive release candidate",
            "must be hashed again at apply time",
            "matching terminal journal declares release",
            "tombstone exists",
            "immutable tombstone",
        )
        for fragment in workflow_fragments:
            with self.subTest(document="workflow", fragment=fragment):
                self.assertIn(fragment, workflow)
        for fragment in output_fragments:
            with self.subTest(document="output", fragment=fragment):
                self.assertIn(fragment, output)

    def test_generic_skill_excludes_project_specific_literals(self) -> None:
        blocked = (
            "E:\\CDW",
            "D:\\Project\\MumaxWriter.skill",
            "C:\\Users\\msjs2",
            "field_switchable_ellipse_ku_dw_lens",
            "dmi2p4_f050",
            "bimeron_homotopy_diagnostic",
            "3335.681",
        )
        for path in sorted(SKILL.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".yaml", ".yml", ".template"}:
                continue
            text = normalized_text(path)
            for literal in blocked:
                with self.subTest(path=path.relative_to(SKILL), literal=literal):
                    self.assertNotIn(literal, text)


if __name__ == "__main__":
    unittest.main()
