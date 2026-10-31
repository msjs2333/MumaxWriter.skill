#!/usr/bin/env python3
"""Analyze the three bundled tutorials using only the Python standard library.

Checks apply to the documented tutorial models, not arbitrary simulations.
No simulation is launched. Failed input/output contracts return a nonzero status.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import math
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_table(path: Path) -> list[dict[str, float]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    require(bool(lines) and lines[0].startswith("#"), "missing MuMax table header")
    names = [part.strip().split(" (")[0] for part in lines[0].lstrip("# ").split("\t")]
    require(len(set(names)) == len(names), "duplicate table column names")
    rows = []
    for number, line in enumerate(lines[1:], 2):
        if not line.strip() or line.startswith("#"):
            continue
        values = [float(v) for v in line.split()]
        require(len(values) == len(names), f"ragged table row {number}")
        require(all(math.isfinite(v) for v in values), f"non-finite table row {number}")
        rows.append(dict(zip(names, values)))
    require(len(rows) >= 3, "need at least three table rows")
    for row in rows:
        require(all(k in row for k in ("t", "mx", "my", "mz")), "missing time/magnetization columns")
        require(sum(row[k]**2 for k in ("mx", "my", "mz")) <= 1.01**2,
                "average normalized magnetization exceeds one")
    return rows


def constant(rows: list[dict[str, float]], key: str) -> float:
    require(all(key in row for row in rows), f"missing column {key}")
    value = rows[0][key]
    require(all(math.isclose(row[key], value, rel_tol=1e-7, abs_tol=1e-30) for row in rows),
            f"{key} must be constant")
    return value


def time_contract(rows: list[dict[str, float]], start: float) -> tuple[float, float]:
    period, duration = constant(rows, "sample_s"), constant(rows, "observe_s")
    require(period > 0 and duration > 0, "sample period and observation duration must be positive")
    require(abs(rows[0]["t"]-start) < period*1e-3, "missing initial time sample")
    require(abs(rows[-1]["t"]-start-duration) < period*1e-3, "incomplete observation window")
    require(all(abs(b["t"]-a["t"]-period) < period*1e-3 for a, b in zip(rows, rows[1:])),
            "time samples are duplicated, missing or irregular")
    return period, duration


def crossing(rows: list[dict[str, float]], xkey: str) -> float:
    for left, right in zip(rows, rows[1:]):
        if left["mx"] * right["mx"] <= 0 and left["mx"] != right["mx"]:
            fraction = -left["mx"] / (right["mx"]-left["mx"])
            return left[xkey] + fraction*(right[xkey]-left[xkey])
    raise ValueError("no mx zero crossing in recorded branch/window")


def hysteresis(rows: list[dict[str, float]]) -> tuple[dict, list[dict]]:
    limit = constant(rows, "field_limit_T")
    step = constant(rows, "field_step_T")
    hk = constant(rows, "anisotropy_field_T")
    transverse = abs(constant(rows, "transverse_T"))
    require(limit > hk > transverse > 0 and step > 0, "invalid near-easy-axis field range")
    intervals = round(2*limit/step)
    require(math.isclose(intervals*step, 2*limit), "field range is not an integer number of steps")
    require(len(rows) == 2*intervals+1, "incomplete hysteresis branch count")
    down, up = rows[:intervals+1], rows[intervals+1:]
    expected = [limit-i*step for i in range(intervals+1)] + [-limit+i*step for i in range(1, intervals+1)]
    for row, field in zip(rows, expected):
        require(abs(row["B_extx"]-field) < step*1e-4, "field order/step mismatch")
    require(all(row["branch"] == -1 for row in down) and all(row["branch"] == 1 for row in up),
            "branch labels do not match the continuation protocol")
    require(down[0]["mx"] > .9 and down[-1]["mx"] < -.9 and up[-1]["mx"] > .9,
            "saturation/reversal missing")
    negative, positive = crossing(down, "B_extx"), crossing(up, "B_extx")
    predicted = hk*(1-(transverse/hk)**(2/3))**1.5
    require(negative < 0 < positive, "loop has the wrong branch switching signs")
    require(max(abs(abs(negative)-predicted), abs(positive-predicted)) <= 2*step,
            "switching field disagrees with the macrospin astroid by more than two field steps")
    curve = [{"branch": r["branch"], "B_x_T": r["B_extx"], "mx": r["mx"]} for r in rows]
    return {"descending_crossing_T": negative, "ascending_crossing_T": positive,
            "analytic_switching_magnitude_T": predicted, "tolerance_T": 2*step,
            "scope": "near-easy-axis, zero-temperature macrospin continuation"}, curve


def sp4(rows: list[dict[str, float]]) -> tuple[dict, list[dict]]:
    period, duration = time_contract(rows, 0)
    require(rows[0]["mx"] > 0 and rows[-1]["mx"] < 0, "SP4 reversal not observed")
    time = crossing(rows, "t")
    recorded = rows[-1]["crossing_time_s"]
    require(time <= recorded <= time+period*1.01, "crossing snapshot time is inconsistent")
    curve = [{"t_s": r["t"], "mx": r["mx"], "my": r["my"], "mz": r["mz"]} for r in rows]
    return {"first_mx_zero_s": time, "snapshot_time_s": recorded, "duration_s": duration,
            "reference_comparison": "not_run", "scope": "SP4 output/reversal checks; not benchmark acceptance"}, curve


def fmr(rows: list[dict[str, float]]) -> tuple[dict, list[dict]]:
    period, duration = time_contract(rows, constant(rows, "pulse_s"))
    bias, damping = constant(rows, "bias_T"), constant(rows, "damping")
    gamma = constant(rows, "gamma_rad_s_T")
    require(bias > 0 and gamma > 0 and 0 <= damping < .1, "invalid small-damping macrospin parameters")
    expected = gamma*bias/(2*math.pi*(1+damping*damping))
    require(expected*duration >= 10 and expected*period <= .1, "need ten cycles and ten samples per expected period")
    require(max(math.hypot(r["mx"], r["my"]) for r in rows) > 1e-6, "no transverse FMR signal")
    count = len(rows)
    require(count <= 10000, "tutorial DFT is limited to 10000 samples; use an FFT for larger data")
    means = [sum(r[k] for r in rows)/count for k in ("mx", "my")]
    samples = [((r["mx"]-means[0])*w, (r["my"]-means[1])*w)
               for i, r in enumerate(rows) for w in [.5-.5*math.cos(2*math.pi*i/(count-1))]]
    spectrum = []
    for index in range(1, count//2+1):
        angle = -2*math.pi*index/count
        phase_step = complex(math.cos(angle), math.sin(angle))
        phase, sx, sy = 1+0j, 0j, 0j
        for x, y in samples:
            sx += x*phase
            sy += y*phase
            phase *= phase_step
        spectrum.append({"frequency_Hz": index/(count*period), "power_arb": (abs(sx)**2+abs(sy)**2)/count**2})
    peak = max(spectrum, key=lambda r:r["power_arb"])["frequency_Hz"]
    tolerance = max(2/duration, .02*expected)
    require(abs(peak-expected) <= tolerance, "FMR peak outside finite-window analytic tolerance")
    return {"peak_Hz": peak, "analytic_Hz": expected, "bin_width_Hz": 1/(count*period),
            "tolerance_Hz": tolerance, "scope": "isotropic macrospin frequency only; not a thin-film dispersion test"}, spectrum


def compare_reference(curve: list[dict], path: Path, tolerance: float) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reference = [{k:float(r[k]) for k in ("t_s", "mx", "my", "mz")} for r in csv.DictReader(handle)]
    require(len(reference) >= 2 and all(math.isfinite(v) for r in reference for v in r.values()),
            "reference CSV needs finite t_s,mx,my,mz samples")
    times = [r["t_s"] for r in reference]
    require(all(b > a for a,b in zip(times,times[1:])), "reference times must increase")
    require(times[0] <= curve[0]["t_s"] and times[-1] >= curve[-1]["t_s"], "reference does not cover the full run")
    error = 0.0
    for row in curve:
        index = max(1, min(bisect.bisect_left(times,row["t_s"]),len(times)-1))
        a,b = reference[index-1],reference[index]
        weight = (row["t_s"]-a["t_s"])/(b["t_s"]-a["t_s"])
        for key in ("mx", "my", "mz"):
            error = max(error,abs(row[key]-(a[key]+weight*(b[key]-a[key]))))
    require(error <= tolerance, f"reference max component error {error:.6g} exceeds {tolerance:g}")
    return {"reference_comparison": "passed_supplied_curve_tolerance", "max_component_error": error,
            "reference_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "reference_tolerance": tolerance}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("hysteresis", "sp4", "fmr"))
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--reference-csv", type=Path, help="SP4 only: independently sourced t_s,mx,my,mz curve")
    parser.add_argument("--tolerance", type=float, default=.03, help="SP4 max absolute normalized component error")
    args = parser.parse_args()
    try:
        require(args.tolerance > 0 and math.isfinite(args.tolerance), "tolerance must be positive and finite")
        require(args.reference_csv is None or args.case == "sp4", "reference CSV is for SP4 only")
        for name in ("m_initial.ovf", "m_final.ovf") + (("m_crossing.ovf",) if args.case == "sp4" else ()):
            with (args.output_dir/name).open("rb") as handle:
                require(handle.read(64).startswith(b"# OOMMF"), f"missing/invalid OVF header: {name}")
        table = args.output_dir/"table.txt"
        metrics, product = {"hysteresis":hysteresis, "sp4":sp4, "fmr":fmr}[args.case](read_table(table))
        if args.reference_csv:
            metrics.update(compare_reference(product,args.reference_csv,args.tolerance))
        metrics["table_sha256"] = hashlib.sha256(table.read_bytes()).hexdigest()
        destination = args.output_dir/"analysis"
        destination.mkdir(exist_ok=True)
        name = "spectrum.csv" if args.case == "fmr" else "curve.csv"
        with (destination/name).open("w",encoding="utf-8",newline="") as handle:
            writer = csv.DictWriter(handle,fieldnames=list(product[0]))
            writer.writeheader()
            writer.writerows(product)
        (destination/"summary.json").write_text(json.dumps(metrics,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(metrics,indent=2))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Tutorial check failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
