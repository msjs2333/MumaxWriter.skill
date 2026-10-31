"""Synthetic file/analysis tests; real simulation results are documented separately."""
from __future__ import annotations

import csv
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/"skills/mumax3/scripts"
sys.path.insert(0, str(SCRIPTS))
from analyze_edge_canting import extract, read_profile
sys.path.pop(0)


def ovf(values: list[float]) -> str:
    header = """# OOMMF OVF 2.0
# xnodes: 5
# ynodes: 1
# znodes: 1
# valuedim: 3
# xbase: 1e-9
# xstepsize: 2e-9
# Begin: Data Text
"""
    rows = "".join(f"{mx} 0 {math.sqrt(1-mx*mx)}\n" for mx in values)
    return header+rows+"# End: Data Text\n"


def write_cases(folder: Path) -> None:
    table = ["# t (s)\tmx ()\tmy ()\tmz ()\tcase_index (1)\tD_paper_J_m2 (J/m2)\tA_J_m (J/m)\tK_J_m3 (J/m3)"]
    for index, (d, tilt) in enumerate(((0, 0), (.001, .2), (-.001, -.2))):
        table.append(f"0\t0\t0\t.99\t{index}\t{d}\t1e-11\t4e5")
        (folder/f"m_case_{index}.ovf").write_text(ovf([-tilt, -tilt/2, 0, tilt/2, tilt]), encoding="utf-8")
    (folder/"table.txt").write_text("\n".join(table)+"\n", encoding="utf-8")


class PaperProfileTests(unittest.TestCase):
    def test_extracts_cell_centers_and_uses_recorded_parameters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_cases(root)
            profiles, summaries = extract(root)
            self.assertEqual(len(profiles), 15)
            for point, expected in zip(profiles[:5], [1, 3, 5, 7, 9]):
                self.assertAlmostEqual(point["x_nm"], expected)
            self.assertAlmostEqual(summaries[1]["left_mx"], -.2)
            self.assertAlmostEqual(summaries[2]["right_mx"], -.2)
            self.assertEqual(summaries[1]["center_mz"], 1)
            self.assertAlmostEqual(summaries[1]["edge_scale"], .25)
            self.assertAlmostEqual(summaries[1]["delta_nm"], 5)

    def test_supports_one_pilot_or_a_pilot_and_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_cases(root)
            table = (root/"table.txt").read_text().splitlines()
            for count in (1, 2):
                (root/"table.txt").write_text("\n".join(table[:count+1])+"\n")
                profiles, summaries = extract(root)
                self.assertEqual(len(summaries), count)
                self.assertEqual(len(profiles), 5*count)

    def test_rejects_truncated_or_nonfinite_ovf(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"m.ovf"
            for bad in (ovf([0, 0]), ovf([0]*5).replace("0 0 1.0", "nan 0 1.0"),
                        ovf([0]*5).replace("# End: Data Text", "")):
                path.write_text(bad, encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_profile(path)

    def test_cli_writes_measured_profiles_and_viewable_svg(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_cases(root)
            result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS/"analyze_edge_canting.py"), str(root)],
                                    capture_output=True, encoding="utf-8", timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            with (root/"analysis/profiles.csv").open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 15)
            self.assertEqual(float(rows[-1]["mx"]), -.2)
            svg = ET.parse(root/"analysis/profiles.svg")
            lines = svg.findall(".//{http://www.w3.org/2000/svg}polyline")
            self.assertEqual(len(lines), 6)
            self.assertTrue(all(len(line.attrib["points"].split()) == 5 for line in lines))


if __name__ == "__main__":
    unittest.main()
