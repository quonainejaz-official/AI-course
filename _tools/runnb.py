"""
runnb.py — notebook ke saare code cells ko upar se neeche chala kar dekhta hai ke koi error to nahi.

Chalane ka tareeqa:
    python _tools/runnb.py "Python/Basics/01_Python_Introduction_aur_Setup.ipynb"
    python _tools/runnb.py "Python/Basics"        # folder = us folder ke saare notebooks
    python _tools/runnb.py                        # sab kuch

Har notebook alag process me nahi, magar alag namespace + temp working dir me chalta hai,
taake file likhne wale examples repo ko ganda na karein.
"""

from __future__ import annotations

import io
import json
import os
import pathlib
import sys
import tempfile
import traceback
from contextlib import redirect_stdout, redirect_stderr

ROOT = pathlib.Path(__file__).resolve().parents[1]


def cells_source(nb_path: pathlib.Path) -> list[tuple[int, str]]:
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    out = []
    for i, cell in enumerate(data.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        src = cell["source"]
        if isinstance(src, list):
            src = "".join(src)
        out.append((i, src))
    return out


def run_notebook(nb_path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    ns: dict = {"__name__": "__main__"}
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp(prefix="nbrun_")
    os.chdir(tmp)
    try:
        for idx, src in cells_source(nb_path):
            buf_out, buf_err = io.StringIO(), io.StringIO()
            try:
                with redirect_stdout(buf_out), redirect_stderr(buf_err):
                    exec(compile(src, f"{nb_path.name}#cell{idx}", "exec"), ns)
            except SystemExit:
                pass
            except BaseException:  # noqa: BLE001
                tb = traceback.format_exc(limit=3).strip().splitlines()
                errors.append(f"cell {idx}: {tb[-1]}")
    finally:
        os.chdir(cwd)
    return errors


def targets(arg: str | None) -> list[pathlib.Path]:
    if not arg:
        base = ROOT
    else:
        base = (ROOT / arg) if not pathlib.Path(arg).is_absolute() else pathlib.Path(arg)
    if base.is_file():
        return [base]
    return [p for p in sorted(base.rglob("*.ipynb")) if ".ipynb_checkpoints" not in p.parts]


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    nbs = targets(arg)
    if not nbs:
        print("koi notebook nahi mila:", arg)
        return 1
    total_fail = 0
    for nb in nbs:
        rel = nb.relative_to(ROOT).as_posix() if str(nb).startswith(str(ROOT)) else str(nb)
        errs = run_notebook(nb)
        if errs:
            total_fail += 1
            print(f"[FAIL] {rel}")
            for e in errs[:12]:
                print("        ", e)
        else:
            print(f"[pass] {rel}")
    print(f"\n{len(nbs) - total_fail}/{len(nbs)} notebooks ran clean")
    return 1 if total_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
