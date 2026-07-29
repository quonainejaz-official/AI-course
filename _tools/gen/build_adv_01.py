"""Notebook 01 build karta hai (parts p1..p5 ko jor kar)."""
import pathlib
import sys

GEN = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(GEN.parent))          # _tools  -> nbgen
sys.path.insert(0, str(GEN))                 # _tools/gen -> parts

from nbgen import save  # noqa: E402

import adv_01_p1, adv_01_p2, adv_01_p3, adv_01_p4, adv_01_p5  # noqa: E402

cells = (adv_01_p1.CELLS + adv_01_p2.CELLS + adv_01_p3.CELLS
         + adv_01_p4.CELLS + adv_01_p5.CELLS)

save("Python/Advance/01_Memory_Model_References_GC_aur_Performance_Internals.ipynb", cells)

n_md = sum(1 for c in cells if c["cell_type"] == "markdown")
print(f"markdown: {n_md}  code: {len(cells) - n_md}")
