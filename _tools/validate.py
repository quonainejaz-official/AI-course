"""
validate.py — saare .ipynb files check karta hai:
  1. valid JSON hai?
  2. required nbformat keys maujood hain?
  3. har cell ka structure theek hai?
  4. kitne cells / markdown / code, aur kya LeetCode mention hai?

Chalane ka tareeqa:  python _tools/validate.py
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

bad: list[str] = []
rows: list[tuple[str, int, int, int, bool]] = []

for nb_path in sorted(ROOT.rglob("*.ipynb")):
    if ".ipynb_checkpoints" in nb_path.parts:
        continue
    rel = nb_path.relative_to(ROOT).as_posix()
    try:
        data = json.loads(nb_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        bad.append(f"{rel}: JSON parse error -> {exc}")
        continue

    for key in ("cells", "metadata", "nbformat", "nbformat_minor"):
        if key not in data:
            bad.append(f"{rel}: missing top-level key '{key}'")

    cells = data.get("cells", [])
    n_md = n_code = 0
    for i, cell in enumerate(cells):
        ct = cell.get("cell_type")
        if ct not in ("markdown", "code"):
            bad.append(f"{rel}: cell {i} bad cell_type {ct!r}")
            continue
        if not isinstance(cell.get("source"), (list, str)):
            bad.append(f"{rel}: cell {i} bad source type")
        if ct == "code":
            n_code += 1
            for key in ("outputs", "execution_count"):
                if key not in cell:
                    bad.append(f"{rel}: code cell {i} missing '{key}'")
        else:
            n_md += 1

    text = nb_path.read_text(encoding="utf-8").lower()
    rows.append((rel, len(cells), n_md, n_code, "leetcode" in text))

print(f"{'notebook':<62} {'cells':>5} {'md':>4} {'code':>5}  leetcode")
print("-" * 92)
for rel, n, n_md, n_code, has_lc in rows:
    print(f"{rel:<62} {n:>5} {n_md:>4} {n_code:>5}  {'yes' if has_lc else '-'}")

print("-" * 92)
print(f"total notebooks: {len(rows)}   total cells: {sum(r[1] for r in rows)}")

if bad:
    print("\nPROBLEMS FOUND:")
    for b in bad:
        print("  -", b)
    sys.exit(1)
print("\nAll notebooks are structurally valid [OK]")

thin = [r for r in rows if r[1] < 45]
if thin:
    print("\nTHIN NOTEBOOKS (<45 cells) - need expansion:")
    for r in thin:
        print(f"  - {r[0]} ({r[1]} cells)")
