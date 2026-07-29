"""Probe 2 — freq aliases, warnings, sqlite window fns, timing budget."""
import io, sqlite3, sys, time, warnings, tempfile, os
import numpy as np
import pandas as pd

def p(label, fn):
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            v = fn()
            ws = sorted({type(x.message).__name__ for x in w})
        print(f"[OK ] {label} -> {v!r} warns={ws}"[:200])
    except Exception as e:
        print(f"[ERR] {label} -> {type(e).__name__}: {str(e)[:90]}")

print("sqlite3 lib version:", sqlite3.sqlite_version)

# freq aliases
p("date_range M", lambda: len(pd.date_range("2024-01-01", periods=3, freq="M")))
p("date_range ME", lambda: len(pd.date_range("2024-01-01", periods=3, freq="ME")))
p("resample M", lambda: pd.Series(range(3), index=pd.date_range("2024-01-01", periods=3)).resample("M").sum().shape)
p("resample MS", lambda: pd.Series(range(3), index=pd.date_range("2024-01-01", periods=3)).resample("MS").sum().shape)
p("resample QE", lambda: pd.Series(range(3), index=pd.date_range("2024-01-01", periods=3)).resample("QE").sum().shape)
p("period_range M", lambda: len(pd.period_range("2024-01", periods=3, freq="M")))
p("dt.to_period M", lambda: pd.Series(pd.date_range("2024-01-01", periods=2)).dt.to_period("M").astype(str).tolist())
p("Timestamp - Period arithmetic", lambda: (pd.Period("2024-03", "M") - pd.Period("2024-01", "M")).n)
p("date_range freq 'h'", lambda: len(pd.date_range("2024-01-01", periods=3, freq="h")))
p("date_range freq 'H'", lambda: len(pd.date_range("2024-01-01", periods=3, freq="H")))

# stack / future_stack warnings
d = pd.DataFrame({"a":[1,2],"b":[3,None]}, index=["x","y"])
p("stack default (NaN drop?)", lambda: d.stack().shape)
p("stack future_stack=True", lambda: d.stack(future_stack=True).shape)
p("unstack fill_value", lambda: d.stack().unstack(fill_value=0).shape)

# MultiIndex performance warning
rng = np.random.default_rng(0)
n = 2000
mi = pd.MultiIndex.from_arrays([rng.choice(list("abcdefgh"), n), rng.integers(0,50,n)], names=["l0","l1"])
big = pd.DataFrame({"v": rng.random(n)}, index=mi)
def perfwarn():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = big.loc[("a", slice(None)), :]
        return [type(x.message).__name__ for x in w]
p("unsorted MI slice warns", perfwarn)
p("lexsort_depth unsorted", lambda: big.index._lexsort_depth)
p("lexsort_depth sorted", lambda: big.sort_index().index._lexsort_depth)
def perfwarn2():
    s = big.sort_index()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = s.loc[("a", slice(None)), :]
        return [type(x.message).__name__ for x in w]
p("sorted MI slice warns", perfwarn2)

# misc removals
p("pd.concat copy kw", lambda: pd.concat([d,d], copy=False).shape)
p("Series.view", lambda: hasattr(pd.Series([1]), "view"))
p("swapaxes", lambda: hasattr(d, "swapaxes"))
p("factorize on ndarray", lambda: pd.factorize(np.array(["a","b","a"]))[0].tolist())
p("factorize on Series", lambda: pd.factorize(pd.Series(["a","b","a"]))[0].tolist())
p("groupby apply include_groups kw", lambda: pd.DataFrame({"k":["a"],"v":[1]}).groupby("k").apply(lambda x: len(x), include_groups=False))
p("read_csv dtype_backend numpy_nullable", lambda: pd.read_csv(io.StringIO("a,b\n1,x\n"), dtype_backend="numpy_nullable").dtypes.astype(str).to_dict())
p("convert_dtypes numpy_nullable", lambda: pd.DataFrame({"a":[1]}).convert_dtypes(dtype_backend="numpy_nullable").dtypes.astype(str).to_dict())
p("errors.Pandas4Warning", lambda: pd.errors.Pandas4Warning.__name__)
p("assert_frame_equal check_like", lambda: (pd.testing.assert_frame_equal(d, d[["b","a"]], check_like=True), "ok")[1])
p("assert_frame_equal check_dtype F", lambda: (pd.testing.assert_frame_equal(pd.DataFrame({"a":[1]}), pd.DataFrame({"a":[1.0]}), check_dtype=False), "ok")[1])
p("explode multiple cols", lambda: pd.DataFrame({"a":[[1,2]],"b":[[3,4]]}).explode(["a","b"]).shape)
p("str.split expand", lambda: pd.Series(["a-b"]).str.split("-", expand=True).shape)
p("Sparse memory", lambda: int(pd.Series(np.where(np.arange(5000)%50==0,1.0,0.0)).astype("Sparse[float]").memory_usage(deep=True)))
p("dense memory", lambda: int(pd.Series(np.where(np.arange(5000)%50==0,1.0,0.0)).memory_usage(deep=True)))
p("df.map", lambda: pd.DataFrame({"a":[1]}).map(lambda x: x+1).iloc[0,0])
p("Series.case_when", lambda: pd.Series([1,5]).case_when([(lambda s: s>3, "hi")]).tolist())
p("df.query MI level", lambda: big.sort_index().query("l1 < 5").shape)
p("at on MI", lambda: big.sort_index().at[("a", big.sort_index().loc['a'].index[0]), "v"] is not None)
p("groupby(level).transform", lambda: big.groupby(level=0)["v"].transform("mean").shape)
p("crosstab margins normalize", lambda: pd.crosstab(pd.Series(list("aab")), pd.Series(list("xyx")), margins=True).shape)
p("value_counts on df", lambda: pd.DataFrame({"a":list("aab")}).value_counts().to_dict())
p("nlargest keep=all", lambda: pd.DataFrame({"v":[1,3,3]}).nlargest(2,"v",keep="all").shape)
p("rank method first", lambda: pd.Series([1,1,2]).rank(method="first").tolist())
p("qcut duplicates drop", lambda: pd.qcut(pd.Series([1,1,1,2]), 4, labels=False, duplicates="drop").tolist())
p("pd.cut labels", lambda: pd.cut(pd.Series([1,9]), [0,5,10], labels=["lo","hi"]).astype(str).tolist())
p("IntervalIndex as index lookup", lambda: pd.Series([10,20], index=pd.IntervalIndex.from_breaks([0,5,10])).loc[3])
p("interval get_loc", lambda: pd.IntervalIndex.from_breaks([0,5,10]).get_loc(7))
p("cut on new data via IntervalIndex", lambda: pd.cut(pd.Series([2,8]), pd.IntervalIndex.from_breaks([0,5,10])).astype(str).tolist())

# sqlite window functions + verification workflow
con = sqlite3.connect(":memory:")
df = pd.DataFrame({"id":[1,2,3,4],"dept":["a","a","b","b"],"sal":[100,200,300,400]})
df.to_sql("emp", con, index=False, if_exists="replace")
p("sqlite RANK OVER", lambda: pd.read_sql("select id, rank() over (partition by dept order by sal desc) r from emp", con).shape)
p("sqlite ROW_NUMBER", lambda: pd.read_sql("select row_number() over (order by sal) r from emp", con)["r"].tolist())
p("sqlite CTE", lambda: pd.read_sql("with x as (select * from emp) select count(*) c from x", con)["c"].tolist())
p("sqlite FULL OUTER JOIN", lambda: pd.read_sql("select * from emp a full outer join emp b on a.id=b.id", con).shape)
p("sqlite dtypes back", lambda: pd.read_sql("select * from emp", con).dtypes.astype(str).to_dict())
p("sqlite date fn", lambda: pd.read_sql("select date('2024-01-05','+1 day') d", con)["d"].tolist())
p("read_sql parse_dates", lambda: pd.read_sql("select '2024-01-05' as d from emp limit 1", con, parse_dates=["d"]).dtypes.astype(str).to_dict())
p("sqlite ROUND/COALESCE", lambda: pd.read_sql("select coalesce(null,1) a, round(1.2345,2) b", con).to_dict("records"))

# timing budget checks
t0=time.perf_counter()
big2 = pd.DataFrame({"a": rng.random(200_000), "g": rng.integers(0,100,200_000)})
_ = big2.groupby("g")["a"].mean()
print(f"[TIME] 200k groupby -> {time.perf_counter()-t0:.3f}s")
t0=time.perf_counter()
_ = big2.head(20000).apply(lambda r: r.a*2, axis=1)
print(f"[TIME] 20k apply axis=1 -> {time.perf_counter()-t0:.3f}s")
t0=time.perf_counter()
_ = [r for r in big2.head(20000).itertuples()]
print(f"[TIME] 20k itertuples -> {time.perf_counter()-t0:.3f}s")
t0=time.perf_counter()
_ = sum(1 for _ in big2.head(5000).iterrows())
print(f"[TIME] 5k iterrows -> {time.perf_counter()-t0:.3f}s")
t0=time.perf_counter()
tmpd=tempfile.mkdtemp(); pth=os.path.join(tmpd,"b.csv")
big2.to_csv(pth, index=False); _=pd.read_csv(pth)
print(f"[TIME] 200k csv roundtrip -> {time.perf_counter()-t0:.3f}s")
t0=time.perf_counter()
_ = pd.Series(rng.choice(["alpha","beta","gamma"], 100_000)).str.upper()
print(f"[TIME] 100k str.upper -> {time.perf_counter()-t0:.3f}s")
t0=time.perf_counter()
d0=pd.DataFrame()
for i in range(300):
    d0 = pd.concat([d0, pd.DataFrame({"a":[i]})], ignore_index=True)
print(f"[TIME] 300 concat loop -> {time.perf_counter()-t0:.3f}s")
print("PROBE2 DONE")
