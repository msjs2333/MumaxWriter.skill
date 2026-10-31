#!/usr/bin/env python3
"""Extract and plot the bundled paper example's 1D OVF profiles.

Uses only the standard library. Reports observables, not a reproduction score.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

from analyze_tutorial import read_table, require


def read_profile(path: Path) -> list[dict[str, float]]:
    """Read one rectangular OVF2 text vector field with ny=nz=1."""
    header, vectors = {}, []
    in_data = False
    completed = False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if stripped.lower() == "# begin: data text":
            in_data = True
        elif stripped.lower() == "# end: data text":
            in_data = False
            completed = True
        elif in_data and stripped and not stripped.startswith("#"):
            values = [float(v) for v in stripped.split()]
            require(len(values) == 3 and all(math.isfinite(v) for v in values), "invalid OVF vector")
            vectors.append(values)
        elif stripped.startswith("#") and ":" in stripped:
            key, value = stripped[1:].split(":", 1)
            header[key.strip().lower()] = value.strip()
    require(completed, "expected an OVF text data block; use OutputFormat = OVF2_TEXT")
    nx = int(header["xnodes"])
    require(nx >= 3 and int(header["ynodes"]) == int(header["znodes"]) == 1,
            "this example reader expects a 1D x profile (ny=nz=1)")
    require(int(header["valuedim"]) == 3 and len(vectors) == nx, "incomplete OVF vector field")
    base, step = float(header["xbase"]), float(header["xstepsize"])
    require(math.isfinite(base) and math.isfinite(step) and step > 0, "invalid OVF coordinates")
    return [{"x_nm": (base+i*step)*1e9, "mx": v[0], "my": v[1], "mz": v[2]}
            for i, v in enumerate(vectors)]


def extract(output: Path) -> tuple[list[dict], list[dict]]:
    profiles, summaries, seen = [], [], set()
    for row in read_table(output/"table.txt", min_rows=1):
        index = int(row["case_index"])
        require(index == row["case_index"] and index >= 0 and index not in seen, "invalid/duplicate case index")
        seen.add(index)
        curve = read_profile(output/f"m_case_{index}.ovf")
        d, a, k = row["D_paper_J_m2"], row["A_J_m"], row["K_J_m3"]
        require(a > 0 and k > 0, "the edge-canting model needs positive A and K_eff")
        profiles.extend({"case_index": index, "D_paper_mJ_m2": d*1e3, **point} for point in curve)
        middle = curve[(len(curve)-1)//2:len(curve)//2+1]
        summaries.append({"case_index": index, "D_paper_mJ_m2": d*1e3,
                          "left_mx": curve[0]["mx"], "right_mx": curve[-1]["mx"],
                          "center_mx": sum(r["mx"] for r in middle)/len(middle),
                          "center_mz": sum(r["mz"] for r in middle)/len(middle),
                          "edge_scale": abs(d)/(2*math.sqrt(a*k)),
                          "delta_nm": math.sqrt(a/k)*1e9})
    return profiles, summaries


def plot_svg(profiles: list[dict], summaries: list[dict]) -> str:
    """A dependency-free plot of the simulated cell-center profiles."""
    left, right = min(r["x_nm"] for r in profiles), max(r["x_nm"] for r in profiles)
    colors = ("#555555", "#0072b2", "#d55e00", "#009e73")
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="470" viewBox="0 0 900 470">',
           '<rect width="900" height="470" fill="white"/>',
           '<g font-family="sans-serif" font-size="14" fill="#222">',
           '<text x="60" y="25" font-size="18">DMI edge canting — simulated cell-center profiles</text>']
    for panel, component in enumerate(("mx", "mz")):
        x0, y0, width, height = 60+430*panel, 70, 360, 300
        svg.append(f'<text x="{x0}" y="55">{component}</text>')
        for tick in (-1, -.5, 0, .5, 1):
            y = y0+(1-tick)*height/2
            svg.append(f'<path d="M{x0},{y}h{width}" stroke="#ddd"/>')
            svg.append(f'<text x="{x0-35}" y="{y+5}">{tick:g}</text>')
        for fraction in (0, .5, 1):
            x = x0+fraction*width
            svg.append(f'<text x="{x-12}" y="395">{left+(right-left)*fraction:.1f}</text>')
        svg.append(f'<text x="{x0+140}" y="420">x (nm)</text>')
        for number, summary in enumerate(summaries):
            curve = [r for r in profiles if r["case_index"] == summary["case_index"]]
            points = " ".join(f'{x0+(r["x_nm"]-left)/(right-left)*width:.2f},{y0+(1-r[component])*height/2:.2f}' for r in curve)
            svg.append(f'<polyline points="{points}" fill="none" stroke="{colors[number%len(colors)]}" stroke-width="2"/>')
    for number, summary in enumerate(summaries):
        x = 60+210*number
        svg.append(f'<text x="{x}" y="452" fill="{colors[number%len(colors)]}">D = {summary["D_paper_mJ_m2"]:g} mJ/m²</text>')
    return "\n".join(svg+["</g></svg>"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    try:
        profiles, summaries = extract(args.output_dir)
        destination = args.output_dir/"analysis"
        destination.mkdir(exist_ok=True)
        with (destination/"profiles.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(profiles[0]))
            writer.writeheader()
            writer.writerows(profiles)
        (destination/"profiles.svg").write_text(plot_svg(profiles, summaries), encoding="utf-8")
        print("D_paper(mJ/m2)  left_mx   right_mx  center_mz  continuum_edge_scale")
        for row in summaries:
            print(f'{row["D_paper_mJ_m2"]:13g}  {row["left_mx"]:8.5f}  {row["right_mx"]:8.5f}  {row["center_mz"]:9.6f}  {row["edge_scale"]:.5f}')
        print(f'Spatial scale sqrt(A/K_eff): {summaries[0]["delta_nm"]:.3f} nm')
        print(f"Wrote {destination/'profiles.csv'} and profiles.svg")
        print("Compare the trend and shape; cell centers are inside the continuum boundary.")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Cannot analyze edge profile: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
