"""CPU-only regressions; synthetic signals are not physical benchmark evidence."""
from __future__ import annotations

import copy
import csv
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "examples/expected_outputs/parameterize_field_frequency_sweep/generate_field_frequency_sweep.py"


def module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


sweep = module(GENERATOR)
analysis = module(ROOT / "skills/mumax3/scripts/analyze_tutorial.py")


class ParameterizationTests(unittest.TestCase):
    def test_recorded_parameters_drive_both_rendered_stages(self):
        values = {"case_id":"changed", "field_T":.017, "frequency_Hz":7.25e9,
                  **copy.deepcopy(sweep.BASE_PARAMS)}
        values.update(geometry={"length_m":1.2e-6, "width_m":240e-9, "thickness_m":6e-9},
                      mesh={"nx":80,"ny":40,"nz":3},
                      material={"Msat_A_per_m":620e3,"Aex_J_per_m":9e-12,"alpha":.025},
                      excitation={"amplitude_T":.0025,"source_x_cells":6},
                      dynamics={"run_time_s":3e-9,"table_period_s":8e-12,"snapshot_period_s":32e-12})
        for render in (sweep.render_relax,sweep.render_dynamics):
            result = render(values)
            for token in ("nx := 80", "ny := 40", "nz := 3", "Lx := 1.2e-06",
                          "Ly := 2.4e-07", "Lz := 6e-09", "Msat = 620000", "Aex = 9e-12",
                          "alpha = 0.025", "B0 := 0.017", "TableAutoSave(8e-12)"):
                self.assertIn(token,result)
        dynamic = sweep.render_dynamics(values)
        for token in ("h0 := 0.0025", "f := 7250000000", "i<6", "k<nz",
                      "SetVector(i, j, k", "AutoSave(m, 3.2e-11)", "Run(3e-09)"):
            self.assertIn(token,dynamic)

    def test_six_cases_and_tracked_representative_match_their_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/"cases"
            result = subprocess.run([sys.executable,"-X","utf8",str(GENERATOR),"--output",str(out)],capture_output=True,encoding="utf-8")
            self.assertEqual(result.returncode,0,result.stderr)
            cases = sorted(out.iterdir())
            self.assertEqual(len(cases),6)
            self.assertEqual(len({p.name for p in cases}),6)
            pairs = set()
            for case in cases:
                params = json.loads((case/"params.json").read_text())
                pairs.add((params["field_mT"],params["frequency_GHz"]))
                self.assertEqual(params["field_T"],params["field_mT"]*1e-3)
                self.assertEqual(params["frequency_Hz"],params["frequency_GHz"]*1e9)
                for stage in ("relax","dynamics"):
                    self.assertEqual((case/f"{stage}.mx3").read_text(),getattr(sweep,f"render_{stage}")(params))
            self.assertEqual(pairs,{(h,f) for h in (-5,0,5) for f in (5,10)})
            representative = GENERATOR.parent/"case_0001_field_m005mT_freq_005GHz"
            for stage in ("relax","dynamics"):
                self.assertEqual((out/representative.name/f"{stage}.mx3").read_text(),(representative/f"{stage}.mx3").read_text())
            sentinel=cases[0]/"relax.mx3"
            sentinel.write_text("existing simulation")
            (cases[0]/"logs").rmdir()
            again = subprocess.run([sys.executable,"-X","utf8",str(GENERATOR),"--output",str(out)],capture_output=True,encoding="utf-8")
            self.assertNotEqual(again.returncode,0)
            self.assertEqual(sentinel.read_text(),"existing simulation")


class AnalysisTests(unittest.TestCase):
    def fmr_rows(self, factor=1):
        gamma, bias, alpha, dt, count = 1.7595e11,.1,.01,20e-12,1001
        frequency=gamma*bias/(2*math.pi*(1+alpha**2))*factor
        rows=[]
        for i in range(count):
            amplitude=.01*math.exp(-i*dt/6e-9)
            rows.append({"t":50e-12+i*dt,"mx":amplitude*math.cos(2*math.pi*frequency*i*dt),
                         "my":amplitude*math.sin(2*math.pi*frequency*i*dt),"mz":math.sqrt(1-amplitude**2),
                         "pulse_s":50e-12,"sample_s":dt,"observe_s":(count-1)*dt,
                         "bias_T":bias,"damping":alpha,"gamma_rad_s_T":gamma})
        return rows

    def test_fmr_recovers_synthetic_frequency_and_rejects_wrong_frequency(self):
        metrics,spectrum=analysis.fmr(self.fmr_rows())
        self.assertLess(abs(metrics["peak_Hz"]-metrics["analytic_Hz"]),metrics["bin_width_Hz"])
        self.assertEqual(len(spectrum),500)
        with self.assertRaisesRegex(ValueError,"peak outside"):
            analysis.fmr(self.fmr_rows(1.5))

    def test_fmr_rejects_truncation_missing_sample_and_no_signal(self):
        rows=self.fmr_rows()
        for bad in (rows[:-1],rows[:20]+rows[21:]):
            with self.assertRaises(ValueError): analysis.fmr(bad)
        for row in rows:row["mx"]=row["my"]=0
        with self.assertRaisesRegex(ValueError,"no transverse"):analysis.fmr(rows)

    def test_sp4_crossing_and_independent_reference_comparison(self):
        rows=[{"t":i*1e-12,"mx":.8-i*.8,"my":.1,"mz":0,"sample_s":1e-12,
               "observe_s":2e-12,"crossing_time_s":1e-12 if i else -1} for i in range(3)]
        metrics,curve=analysis.sp4(rows)
        self.assertEqual(metrics["first_mx_zero_s"],1e-12)
        self.assertEqual(metrics["reference_comparison"],"not_run")
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"synthetic.csv"
            with path.open("w",newline="") as handle:
                writer=csv.DictWriter(handle,fieldnames=list(curve[0]));writer.writeheader();writer.writerows(curve)
            self.assertEqual(analysis.compare_reference(curve,path,.01)["max_component_error"],0)
            wrong=copy.deepcopy(curve);wrong[1]["mx"]+=.1
            with self.assertRaisesRegex(ValueError,"exceeds"):analysis.compare_reference(wrong,path,.01)
        rows[-1]["crossing_time_s"]=2.5e-12
        with self.assertRaisesRegex(ValueError,"snapshot"):analysis.sp4(rows)

    def test_hysteresis_checks_branch_history_and_switching(self):
        fields=[.2-i*.005 for i in range(81)]+[-.2+i*.005 for i in range(1,81)]
        rows=[]
        for i,field in enumerate(fields):
            down=i<81
            mx=(1 if field>-.118 else -1) if down else (-1 if field<.118 else 1)
            rows.append({"B_extx":field,"mx":mx,"branch":-1 if down else 1,
                         "field_limit_T":.2,"field_step_T":.005,"transverse_T":.001,"anisotropy_field_T":.125})
        metrics,_=analysis.hysteresis(rows)
        self.assertLess(metrics["descending_crossing_T"],0)
        with self.assertRaises(ValueError):analysis.hysteresis(rows[:-1])
        rows[100]["branch"]=-1
        with self.assertRaisesRegex(ValueError,"branch labels"):analysis.hysteresis(rows)

    def test_native_table_rejects_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"table.txt"
            for content in ("# t (s)\tmx ()\tmy ()\tmz ()\n0 nan 0 0\n",
                            "# t (s)\tmx ()\tmy ()\tmz ()\n0 1 0\n"):
                p.write_text(content)
                with self.assertRaises(ValueError):analysis.read_table(p)


if __name__ == "__main__":
    unittest.main()
