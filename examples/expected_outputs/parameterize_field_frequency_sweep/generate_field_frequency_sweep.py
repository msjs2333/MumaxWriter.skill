#!/usr/bin/env python3
"""Generate a small mumax3 field/frequency sweep.

The script writes case folders and metadata only. Running mumax3 and analyzing
OVF/table output should be handled by a separate execution or analysis step.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("runs/field_frequency_sweep")
FIELDS_MT = [-5.0, 0.0, 5.0]
FREQUENCIES_GHZ = [5.0, 10.0]

BASE_PARAMS = {
    "geometry": {"length_m": 768e-9, "width_m": 192e-9, "thickness_m": 2e-9},
    "mesh": {"nx": 256, "ny": 64, "nz": 1},
    "material": {"Msat_A_per_m": 800e3, "Aex_J_per_m": 13e-12, "alpha": 0.01},
    "excitation": {"amplitude_T": 1e-3, "source_x_cells": 8},
    "dynamics": {"run_time_s": 2e-9, "table_period_s": 5e-12, "snapshot_period_s": 20e-12},
}


def field_tag(value_mt: float) -> str:
    sign = "p" if value_mt >= 0 else "m"
    return f"{sign}{abs(value_mt):03.0f}mT"


def freq_tag(value_ghz: float) -> str:
    return f"{value_ghz:03.0f}GHz"


def render_relax(params: dict) -> str:
    field_t = params["field_T"]
    return f"""// Relaxation stage for {params["case_id"]}.
OutputFormat = OVF2_TEXT

nx := 256
ny := 64
nz := 1
Lx := 768e-9
Ly := 192e-9
Lz := 2e-9
SetGridSize(nx, ny, nz)
SetCellSize(Lx/nx, Ly/ny, Lz/nz)
SetGeom(Rect(Lx, Ly))

Msat = 800e3
Aex = 13e-12
alpha = 0.01

B0 := {field_t:.12g}
B_ext = Vector(B0, 0, 0)
m = Uniform(1, 0, 0)

TableAdd(m)
TableAdd(B_ext)
TableAdd(E_total)
TableAdd(MaxAngle)
TableAutoSave(5e-12)

Relax()
SaveAs(m, "m_relaxed.ovf")
SaveAs(B_eff, "B_eff_relaxed.ovf")
TableSave()
"""


def render_dynamics(params: dict) -> str:
    field_t = params["field_T"]
    frequency_hz = params["frequency_Hz"]
    return f"""// Dynamics stage for {params["case_id"]}.
OutputFormat = OVF2_TEXT

nx := 256
ny := 64
nz := 1
Lx := 768e-9
Ly := 192e-9
Lz := 2e-9
SetGridSize(nx, ny, nz)
SetCellSize(Lx/nx, Ly/ny, Lz/nz)
SetGeom(Rect(Lx, Ly))

Msat = 800e3
Aex = 13e-12
alpha = 0.01

B0 := {field_t:.12g}
h0 := 1e-3
f := {frequency_hz:.12g}
B_ext = Vector(B0, 0, 0)
m.LoadFile("relax.out/m_relaxed.ovf")

source := NewVectorMask(nx, ny, nz)
for i:=0; i<8; i++{{
    for j:=0; j<ny; j++{{
        source.SetVector(i, j, 0, Vector(0, 1, 0))
    }}
}}
B_ext.Add(source, h0*sin(2*pi*f*t))

TableAdd(m)
TableAdd(B_ext)
TableAdd(E_total)
TableAutoSave(5e-12)
AutoSave(m, 20e-12)

Run(2e-9)
SaveAs(m, "m_dynamic_final.ovf")
TableSave()
"""


def main() -> None:
    for index, field_mt in enumerate(FIELDS_MT, start=1):
        for frequency_ghz in FREQUENCIES_GHZ:
            case_id = f"case_{index:04d}_field_{field_tag(field_mt)}_freq_{freq_tag(frequency_ghz)}"
            case_dir = ROOT / case_id
            (case_dir / "logs").mkdir(parents=True, exist_ok=True)
            params = {
                "case_id": case_id,
                **BASE_PARAMS,
                "field_mT": field_mt,
                "field_T": field_mt * 1e-3,
                "frequency_GHz": frequency_ghz,
                "frequency_Hz": frequency_ghz * 1e9,
                "scripts": {"relax": "relax.mx3", "dynamics": "dynamics.mx3"},
                "expected_output_directories": ["relax.out", "dynamics.out"],
                "logs": {"stdout": "logs/mumax3.stdout.txt", "stderr": "logs/mumax3.stderr.txt"},
            }
            (case_dir / "params.json").write_text(json.dumps(params, indent=2) + "\n", encoding="utf-8")
            (case_dir / "relax.mx3").write_text(render_relax(params), encoding="utf-8")
            (case_dir / "dynamics.mx3").write_text(render_dynamics(params), encoding="utf-8")


if __name__ == "__main__":
    main()
