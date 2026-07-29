"""Probe 3 — sparse fill_value, datetime units, tz, memory tables, misc."""
import io, sqlite3, statistics, sys, time, tracemalloc, warnings, gc
import numpy as np
import pandas as pd

def p(label, fn):
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            v = fn()
            ws = sorted({type(x.message).__name__ for x in w})
        print(f"[OK ] {label} -> {v!r} warns={ws}"[:190])
    except Exception as e:
        print(f"[ERR] {label} -> {type(e).__name__}: {str(e)[:90]}")

rng = np.random.default_rng(0)
arr = np.where(np.arange(20000) % 100 == 0, 1.0, 0.0)
p("dense mem", lambda: int(pd.Series(arr).memory_usage(deep=True)))
p("Sparse[float] nan fill mem", lambda: int(pd.Series(arr).astype("Sparse[float]").memory_usage(deep=True)))
p("SparseDtype fill 0 mem", lambda: int(pd.Series(arr).astype(pd.SparseDtype("float64", 0.0)).memory_usage(deep=True)))
p("sparse density fill0", lambda: pd.Series(arr).astype(pd.SparseDtype("float64", 0.0)).sparse.density)
p("sparse -> dense", lambda: pd.Series(arr).astype(pd.SparseDtype("float64", 0.0)).sparse.to_dense().sum())
p("sparse sum works", lambda: float(pd.Series(arr).astype(pd.SparseDtype("float64",0.0)).sum()))

p("date_range dtype", lambda: str(pd.date_range("2024-01-01", periods=2).dtype))
p("to_datetime dtype", lambda: str(pd.to_datetime(pd.Series(["2024-01-01"])).dtype))
p("to_datetime format", lambda: str(pd.to_datetime(pd.Series(["05/01/2024"]), format="%d/%m/%Y").iloc[0].date()))
p("timedelta dtype", lambda: str((pd.date_range("2024-01-01", periods=2).to_series().diff()).dtype))
p("datetime mem 2 rows", lambda: int(pd.date_range("2024-01-01", periods=1000).to_series().memory_usage(deep=True)))
p("astype datetime64[s]", lambda: str(pd.date_range("2024-01-01", periods=2).astype("datetime64[s]").dtype))
p("tz nonexistent", lambda: pd.Series(pd.to_datetime(["2024-03-10 02:30"])).dt.tz_localize("America/New_York").iloc[0])
p("tz ambiguous", lambda: pd.Series(pd.to_datetime(["2024-11-03 01:30"])).dt.tz_localize("America/New_York", ambiguous=True).iloc[0])
p("tz aware compare naive", lambda: pd.Timestamp("2024-01-01", tz="UTC") > pd.Timestamp("2024-01-01"))
p("NaT propagate", lambda: str(pd.Series([pd.NaT]).dt.year.iloc[0]))

# memory table helper accuracy
n = 50_000
df = pd.DataFrame({
    "id": rng.integers(0, 10**6, n),
    "city": rng.choice(["Lahore","Karachi","Islamabad","Multan"], n),
    "amt": rng.random(n) * 100,
    "flag": rng.choice([True, False], n),
})
p("df mem deep MB", lambda: round(df.memory_usage(deep=True).sum()/1e6, 3))
opt = df.assign(id=lambda d: pd.to_numeric(d["id"], downcast="unsigned"),
                city=lambda d: d["city"].astype("category"),
                amt=lambda d: d["amt"].astype("float32"))
p("opt mem deep MB", lambda: round(opt.memory_usage(deep=True).sum()/1e6, 3))
p("per-col mem", lambda: {k: int(v) for k, v in df.memory_usage(deep=True).items()})
p("opt per-col mem", lambda: {k: int(v) for k, v in opt.memory_usage(deep=True).items()})
p("id downcast dtype", lambda: str(opt["id"].dtype))

# merge with categorical / dtype mismatch
a = pd.DataFrame({"k": ["a","b"], "x":[1,2]})
b = pd.DataFrame({"k": ["a","b"], "y":[3,4]})
p("merge str keys", lambda: pd.merge(a,b,on="k").shape)
p("merge cat keys", lambda: pd.merge(a.astype({"k":"category"}), b.astype({"k":"category"}), on="k").dtypes.astype(str).to_dict())
p("merge int vs str key", lambda: pd.merge(pd.DataFrame({"k":[1]}), pd.DataFrame({"k":["1"]}), on="k").shape)
p("merge int64 vs Int64", lambda: pd.merge(pd.DataFrame({"k":[1]}), pd.DataFrame({"k":pd.array([1],dtype='Int64')}), on="k").shape)
p("merge many-to-many size", lambda: pd.merge(pd.DataFrame({"k":[1,1]}), pd.DataFrame({"k":[1,1,1]}), on="k").shape)
p("merge validate 1:1 error", lambda: pd.merge(pd.DataFrame({"k":[1,1]}), pd.DataFrame({"k":[1]}), on="k", validate="one_to_one").shape)

# groupby cython vs lambda timing
g = pd.DataFrame({"g": rng.integers(0, 500, 100_000), "v": rng.random(100_000)})
t0=time.perf_counter(); g.groupby("g")["v"].sum(); t1=time.perf_counter()
g.groupby("g")["v"].agg(lambda s: s.sum()); t2=time.perf_counter()
print(f"[TIME] cython sum {t1-t0:.4f}s vs lambda {t2-t1:.4f}s ratio {(t2-t1)/(t1-t0):.1f}x")

# vectorized vs apply timing on 100k
s = pd.Series(rng.random(100_000))
t0=time.perf_counter(); _=s*2+1; t1=time.perf_counter()
_=s.map(lambda x: x*2+1); t2=time.perf_counter()
print(f"[TIME] vec {t1-t0:.5f}s vs map {t2-t1:.5f}s ratio {(t2-t1)/max(t1-t0,1e-9):.0f}x")

# tracemalloc
tracemalloc.start()
tmp = pd.DataFrame({"a": rng.random(100_000)})
cur, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"[OK ] tracemalloc cur={cur/1e6:.2f}MB peak={peak/1e6:.2f}MB")

# statistics for z-test
p("NormalDist cdf", lambda: round(statistics.NormalDist().cdf(1.96), 4))
p("statistics fmean", lambda: statistics.fmean([1,2,3]))

# to_markdown fallback helper
def md_table(d):
    cols = list(d.columns)
    head = "| " + " | ".join(str(c) for c in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    rows = ["| " + " | ".join(str(v) for v in r) + " |" for r in d.itertuples(index=False)]
    return "\n".join([head, sep] + rows)
p("custom md table", lambda: md_table(a).replace("\n", " ~ "))
p("to_markdown try", lambda: a.to_markdown())

# sqlite verification workflow sample
con = sqlite3.connect(":memory:")
emp = pd.DataFrame({"id":[1,2,3,4],"dept":["a","a","b","b"],"sal":[100,200,300,400]})
emp.to_sql("emp", con, index=False, if_exists="replace")
sql = pd.read_sql("select dept, max(sal) as top from emp group by dept order by dept", con)
pdres = emp.groupby("dept", as_index=False)["sal"].max().rename(columns={"sal":"top"}).sort_values("dept").reset_index(drop=True)
p("sql vs pandas frame equal", lambda: (pd.testing.assert_frame_equal(sql, pdres, check_dtype=False), "ok")[1])
p("sql dtypes", lambda: sql.dtypes.astype(str).to_dict())
p("pd dtypes", lambda: pdres.dtypes.astype(str).to_dict())
con.close()

# is_monotonic lookup speed
idx_sorted = pd.Series(range(200_000), index=np.arange(200_000))
p("monotonic", lambda: idx_sorted.index.is_monotonic_increasing)
p("get_loc", lambda: idx_sorted.index.get_loc(150_000))
p("get_indexer", lambda: idx_sorted.index.get_indexer([1,2]).tolist())

p("show_versions lines", lambda: len(__import__("io").StringIO().getvalue()) if False else "skip")
p("gc collect", lambda: isinstance(gc.collect(), int))
print("PROBE3 DONE")
