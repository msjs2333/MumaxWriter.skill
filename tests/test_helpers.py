from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_release import local_reference_links, missing_local_reference_links


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "mumax3"
CHECKER = SKILL / "scripts" / "check_mx3_static.py"
COLLECTOR = SKILL / "scripts" / "collect_case_status.py"
SYNC = SKILL / "scripts" / "sync_local_skill.py"


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

    def test_analysis_without_comparable_signature_is_unverified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            case = base / "case_a"
            case.mkdir()
            (case / "params.json").write_text(json.dumps({"case_id": "case_a"}), encoding="utf-8")
            (case / "analysis_record.json").write_text(json.dumps({"result": "present"}), encoding="utf-8")
            proc = run(str(COLLECTOR), str(case))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        rows = list(csv.DictReader(proc.stdout.splitlines()))
        self.assertEqual(rows[0]["analysis_status"], "analysis_unverified")
        self.assertNotEqual(rows[0]["analysis_status"], "analysis_fresh")

    def test_optional_json_errors_are_reported_and_signature_mismatch_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            case = base / "case_a"
            case.mkdir()
            (case / "params.json").write_text(
                json.dumps({"case_id": "case_a", "dynamic_signature": "expected"}),
                encoding="utf-8",
            )
            (case / "analysis_record.json").write_text(
                json.dumps({"dynamic_signature": "different"}), encoding="utf-8"
            )
            (case / "manual_review.json").write_text("[]", encoding="utf-8")
            proc = run(str(COLLECTOR), str(case))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        rows = list(csv.DictReader(proc.stdout.splitlines()))
        self.assertEqual(rows[0]["analysis_status"], "analysis_stale")
        self.assertEqual(rows[0]["provenance_state"], "stale")
        self.assertIn("manual_review.json", rows[0]["error_message"])

    def test_invalid_optional_json_is_reported_while_missing_optional_json_is_not(self) -> None:
        for label, content in (("invalid_json", "{"), ("invalid_utf8", b"\xff")):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                case = base / "case_a"
                case.mkdir()
                (case / "params.json").write_text("{}", encoding="utf-8")
                record = case / "analysis_record.json"
                if isinstance(content, bytes):
                    record.write_bytes(content)
                else:
                    record.write_text(content, encoding="utf-8")
                proc = run(str(COLLECTOR), str(case))
                self.assertEqual(proc.returncode, 0, proc.stderr)
                rows = list(csv.DictReader(proc.stdout.splitlines()))
                self.assertIn("analysis_record.json", rows[0]["error_message"])
                self.assertEqual(rows[0]["derived_status"], "needs_review")
                self.assertNotIn("run_record.json", rows[0]["error_message"])

    def test_out_only_root_reports_no_cases_on_stderr_without_csv_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "stage.out").mkdir()
            proc = run(str(COLLECTOR), str(base))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(proc.stderr.strip())
        reader = csv.DictReader(proc.stdout.splitlines())
        self.assertEqual(
            reader.fieldnames,
            [
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
            ],
        )
        rows = list(reader)
        self.assertEqual(rows, [])


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
        links = local_reference_links()
        self.assertTrue(links)
        self.assertEqual(missing_local_reference_links(), [])

if __name__ == "__main__":
    unittest.main()
