# Temporary harness: gen script ke cells ko chala kar dekhta hai (save nahi karta)
import io, pathlib, sys, traceback
from contextlib import redirect_stdout
src = pathlib.Path("_tools/gen/pandas_basics_01.py").read_text(encoding="utf-8")
ns = {}
exec(compile(src, "gen01", "exec"), ns)
cells = ns["cells"]
print("total cells:", len(cells))
code_cells = [c for c in cells if c["cell_type"] == "code"]
print("code cells :", len(code_cells))
env = {"__name__": "__main__"}
fails = 0
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    s = "".join(c["source"])
    try:
        with redirect_stdout(io.StringIO()):
            exec(compile(s, f"cell{i}", "exec"), env)
    except BaseException:
        fails += 1
        print(f"[FAIL] cell {i}: {traceback.format_exc(limit=2).strip().splitlines()[-1]}")
print("fails:", fails)
