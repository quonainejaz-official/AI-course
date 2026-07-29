"""Probe: pandas 3.0.5 advanced-notebook behaviour verify (guess nahi, asli output)."""
import io, json, sqlite3, sys, tempfile, warnings, os
import numpy as np
import pandas as pd

def p(label, fn):
    try:
        v = fn()
        print(f"[OK ] {label} -> {v!r}"[:400])
    except Exception as e:
        print(f"[ERR] {label} -> {type(e).__name__}: {e}"[:400])

print("pandas", pd.__version__, "numpy", np.__version__, "py", sys.version.split()[0])

# ---------- optional libs ----------
for mod in ["pyarrow", "numexpr", "bottleneck", "tabulate", "jinja2", "tables", "numba", "sqlalchemy", "openpyxl", "scipy"]:
    try:
        m = __import__(mod)
        print(f"[LIB] {mod} {getattr(m,'__version__','?')}")
    except Exception as e:
        print(f"[LIB] {mod} MISSING")

# ---------- default dtypes (PDEP-14 str dtype) ----------
s = pd.Series(["a", "b", None])
p("str series dtype", lambda: str(s.dtype))
p("str series dtype type", lambda: type(s.dtype).__name__)
p("infer_string option", lambda: pd.get_option("future.infer_string") if "future.infer_string" in [o for o in dir(pd.options.future)] else "n/a")
p("options.mode keys", lambda: [k for k in dir(pd.options.mode)])
p("astype object", lambda: str(s.astype(object).dtype))
p("astype string", lambda: str(s.astype("string").dtype))
p("StringDtype default storage", lambda: str(pd.StringDtype()))
p("string[pyarrow]", lambda: str(pd.Series(["a"]).astype("string[pyarrow]").dtype))
p("dtype_backend pyarrow", lambda: str(pd.DataFrame({"a":[1]}).convert_dtypes(dtype_backend="pyarrow").dtypes.iloc[0]))
p("memory_usage deep on str", lambda: int(s.memory_usage(deep=True)))
p("object col memory", lambda: int(pd.Series(["aaaa"]*1000, dtype=object).memory_usage(deep=True)))
p("str col memory", lambda: int(pd.Series(["aaaa"]*1000).memory_usage(deep=True)))
p("category memory", lambda: int(pd.Series(["aaaa"]*1000).astype("category").memory_usage(deep=True)))

# ---------- stack/unstack ----------
df = pd.DataFrame({"a":[1,2],"b":[3,4]}, index=["x","y"])
p("stack basic", lambda: df.stack().shape)
p("stack future_stack kw", lambda: df.stack(future_stack=True).shape)
p("stack dropna kw", lambda: df.stack(dropna=False).shape)
mi = pd.MultiIndex.from_product([["A","B"],["p","q"]])
d2 = pd.DataFrame(np.arange(8).reshape(2,4), columns=mi)
p("unstack multi level list", lambda: d2.stack(level=[0,1]).shape)
p("stack level list", lambda: d2.stack(level=[0,1]).index.nlevels)

# ---------- sum(level=) removed ----------
mdf = pd.DataFrame({"v":[1,2,3,4]}, index=pd.MultiIndex.from_product([["a","b"],[1,2]], names=["g","i"]))
p("sum(level=0)", lambda: mdf.sum(level=0).shape)
p("groupby(level=0).sum", lambda: mdf.groupby(level=0).sum().shape)
p("groupby(level='g').sum", lambda: mdf.groupby(level="g").sum().to_dict())

# ---------- Index types ----------
p("Int64Index", lambda: pd.Int64Index([1,2]))
p("pd.Index int dtype", lambda: str(pd.Index([1,2]).dtype))
p("RangeIndex", lambda: repr(pd.RangeIndex(3)))
p("CategoricalIndex", lambda: str(pd.CategoricalIndex(["a","b"]).dtype))
p("IntervalIndex.from_breaks", lambda: repr(pd.IntervalIndex.from_breaks([0,5,10])))
p("PeriodIndex", lambda: repr(pd.period_range("2024-01", periods=2, freq="M")))
p("IntervalIndex get_indexer", lambda: pd.IntervalIndex.from_breaks([0,5,10]).get_indexer([3,7]).tolist())
p("cut retbins categories", lambda: pd.cut(pd.Series([1,6]), bins=[0,5,10]).cat.categories.tolist())

# ---------- CoW / chained assignment ----------
def chained():
    d = pd.DataFrame({"a":[1,2,3]})
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        d["a"][0] = 99
        return (d.loc[0,"a"], [str(x.category.__name__) for x in w])
p("chained assignment", chained)
def chained_err():
    d = pd.DataFrame({"a":[1,2,3]})
    try:
        d[d.a>1]["a"] = 5
        return "no error"
    except Exception as e:
        return type(e).__name__
p("chained assign on filter", chained_err)
p("ChainedAssignmentError exists", lambda: pd.errors.ChainedAssignmentError.__name__)
p("SettingWithCopyWarning exists", lambda: pd.errors.SettingWithCopyWarning.__name__)
p("copy on write option", lambda: pd.get_option("mode.copy_on_write"))
def cow_view():
    d = pd.DataFrame({"a":[1,2,3]})
    v = d["a"]
    d.loc[0,"a"] = 100
    return v.iloc[0]
p("cow: series view after parent write", cow_view)
p("_is_view attr", lambda: pd.DataFrame({"a":[1]})["a"]._is_view)

# ---------- inplace ----------
def inplace_warn():
    d = pd.DataFrame({"a":[1,None,3]})
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        d.fillna(0, inplace=True)
        return [type(x.message).__name__ for x in w]
p("fillna inplace warnings", inplace_warn)
def method_removed():
    d = pd.DataFrame({"a":[1]})
    return hasattr(d, "append"), hasattr(d, "applymap"), hasattr(d, "map"), hasattr(d, "iteritems")
p("removed methods", method_removed)
p("Series.append", lambda: hasattr(pd.Series([1]), "append"))
p("fillna method='ffill'", lambda: pd.Series([1,None]).fillna(method="ffill").tolist())
p("ffill()", lambda: pd.Series([1,None]).ffill().tolist())

# ---------- nullable ----------
p("Int64 + NA", lambda: (pd.Series([1,pd.NA], dtype="Int64") + 1).tolist())
p("boolean NA any", lambda: pd.Series([True,pd.NA], dtype="boolean").any())
p("Int64 mean", lambda: pd.Series([1,pd.NA], dtype="Int64").mean())
p("NA == NA", lambda: repr(pd.NA == pd.NA))
p("Int64 astype int64 with NA", lambda: pd.Series([1,pd.NA],dtype="Int64").astype("int64").tolist())
p("convert_dtypes", lambda: pd.DataFrame({"a":[1,2],"b":["x","y"]}).convert_dtypes().dtypes.astype(str).to_dict())
p("to_numeric downcast", lambda: str(pd.to_numeric(pd.Series([1,2,3]), downcast="unsigned").dtype))
p("Sparse", lambda: str(pd.Series([0,0,1.0], dtype="Sparse[float]").dtype))
p("sparse density", lambda: pd.Series(np.where(np.arange(100)%10==0, 1.0, 0.0)).astype("Sparse[float]").sparse.density)

# ---------- eval/query ----------
dd = pd.DataFrame(np.random.default_rng(0).random((100,3)), columns=list("abc"))
p("df.eval", lambda: float(dd.eval("a + b * c").sum()))
p("df.query", lambda: dd.query("a > 0.5 and b < 0.5").shape)
p("pd.eval engine numexpr", lambda: float(pd.eval("dd.a + dd.b", engine="numexpr").sum()))
p("query local var", lambda: dd.query("a > @thr", local_dict={"thr":0.5}).shape)
p("eval assign", lambda: dd.eval("d = a + b").shape)

# ---------- groupby ----------
g = pd.DataFrame({"k":list("aabbb"),"v":[1,2,3,4,5]})
p("groupby apply include_groups", lambda: g.groupby("k").apply(lambda x: x["v"].sum()).to_dict())
p("groupby apply full frame", lambda: g.groupby("k").apply(lambda x: x.sum(numeric_only=True)).shape)
p("groupby transform", lambda: g.groupby("k")["v"].transform("sum").tolist())
p("groupby rank dense", lambda: g.groupby("k")["v"].rank(method="dense").tolist())
p("groupby cumcount", lambda: g.groupby("k").cumcount().tolist())
p("groupby nth", lambda: g.groupby("k").nth(0).shape)
p("groupby rolling", lambda: g.groupby("k")["v"].rolling(2).mean().shape)
p("groupby expanding", lambda: g.groupby("k")["v"].expanding().sum().shape)
p("groupby observed default", lambda: pd.DataFrame({"c":pd.Categorical(["a"],categories=["a","b"]),"v":[1]}).groupby("c").sum().shape)
p("groupby agg named", lambda: g.groupby("k").agg(total=("v","sum"), n=("v","size")).to_dict())
p("groupby ngroup", lambda: g.groupby("k").ngroup().tolist())
p("groupby pct_change", lambda: g.groupby("k")["v"].pct_change().round(2).tolist())
p("groupby head", lambda: g.groupby("k").head(1).shape)
p("groupby size vs count", lambda: (g.groupby("k").size().to_dict()))
p("groupby qcut per group", lambda: g.groupby("k")["v"].transform(lambda s: pd.qcut(s, 2, labels=False, duplicates="drop")).tolist())

# ---------- merge / IO ----------
p("merge validate", lambda: pd.merge(g, g, on="k", validate="many_to_many").shape)
p("merge indicator", lambda: pd.merge(g, g.head(2), on="k", how="left", indicator=True)["_merge"].value_counts().to_dict())
p("merge_asof", lambda: pd.merge_asof(pd.DataFrame({"t":[1,5],"a":[1,2]}), pd.DataFrame({"t":[0,4],"b":[9,8]}), on="t").to_dict("list"))
p("join on index", lambda: g.set_index("k").join(g.set_index("k"), rsuffix="_r").shape)
p("compare", lambda: pd.DataFrame({"a":[1,2]}).compare(pd.DataFrame({"a":[1,3]})).shape)

tmpd = tempfile.mkdtemp()
csvp = os.path.join(tmpd, "t.csv")
g.to_csv(csvp, index=False)
p("read_csv dtype dict", lambda: pd.read_csv(csvp, dtype={"v":"int32"}).dtypes.astype(str).to_dict())
p("read_csv engine pyarrow", lambda: pd.read_csv(csvp, engine="pyarrow").shape)
p("read_csv low_memory", lambda: pd.read_csv(csvp, low_memory=False).shape)
p("read_csv chunksize", lambda: sum(len(c) for c in pd.read_csv(csvp, chunksize=2)))
p("to_parquet", lambda: (g.to_parquet(os.path.join(tmpd,"t.parquet")), "ok")[1])
p("to_feather", lambda: (g.to_feather(os.path.join(tmpd,"t.f")), "ok")[1])
p("to_pickle", lambda: (g.to_pickle(os.path.join(tmpd,"t.pkl")), pd.read_pickle(os.path.join(tmpd,"t.pkl")).shape)[1])
p("to_hdf", lambda: (g.to_hdf(os.path.join(tmpd,"t.h5"), key="k"), "ok")[1])
p("to_markdown", lambda: g.head(2).to_markdown())
p("to_string", lambda: g.head(1).to_string())
p("style", lambda: type(g.style).__name__)

con = sqlite3.connect(":memory:")
p("to_sql sqlite3", lambda: g.to_sql("t", con, index=False, if_exists="replace"))
p("read_sql sqlite3", lambda: pd.read_sql("select * from t", con).shape)
p("read_sql chunksize", lambda: sum(len(c) for c in pd.read_sql("select * from t", con, chunksize=2)))
p("read_sql_query params", lambda: pd.read_sql_query("select * from t where v > ?", con, params=(2,)).shape)

# ---------- reshaping ----------
p("wide_to_long", lambda: pd.wide_to_long(pd.DataFrame({"id":[1],"x_2020":[1],"x_2021":[2]}), ["x"], i="id", j="yr", sep="_").shape)
p("melt", lambda: g.melt(id_vars="k").shape)
p("pivot_table margins", lambda: g.pivot_table(index="k", values="v", aggfunc="sum", margins=True).to_dict())
p("pivot", lambda: pd.DataFrame({"i":[1,1],"c":["a","b"],"v":[1,2]}).pivot(index="i", columns="c", values="v").shape)
p("crosstab", lambda: pd.crosstab(g.k, g.v).shape)
p("explode", lambda: pd.DataFrame({"a":[[1,2],[3]]}).explode("a").shape)
p("json_normalize", lambda: pd.json_normalize([{"a":1,"b":{"c":2}}]).columns.tolist())
p("json_normalize record_path", lambda: pd.json_normalize([{"id":1,"items":[{"p":"x"}]}], record_path="items", meta="id").shape)

# ---------- multiindex ----------
mi2 = pd.MultiIndex.from_product([list("ab"), [1,2]], names=["l0","l1"])
mdf2 = pd.DataFrame({"v":range(4)}, index=mi2)
p("loc tuple", lambda: mdf2.loc[("a",1),"v"])
p("loc partial", lambda: mdf2.loc["a"].shape)
p("IndexSlice", lambda: mdf2.loc[pd.IndexSlice[:,1],:].shape)
p("xs", lambda: mdf2.xs(1, level="l1").shape)
p("loc list of tuples", lambda: mdf2.loc[[("a",1),("b",2)]].shape)
p("sortlevel", lambda: mdf2.sortlevel(0)[0].shape)
p("index.sortlevel", lambda: mdf2.index.sortlevel(0)[0].nlevels)
p("lexsort_depth", lambda: mdf2.index._lexsort_depth)
p("is_lexsorted attr", lambda: hasattr(mdf2.index, "is_lexsorted"))
p("PerformanceWarning cls", lambda: pd.errors.PerformanceWarning.__name__)
p("get_level_values", lambda: mdf2.index.get_level_values(0).tolist())
p("droplevel", lambda: mdf2.droplevel(0).shape)
p("swaplevel", lambda: mdf2.swaplevel().index.names)
p("reorder_levels", lambda: mdf2.reorder_levels([1,0]).index.names)
p("rename_axis", lambda: mdf2.rename_axis(["A","B"]).index.names)
p("set_names", lambda: mdf2.index.set_names(["x","y"]).names)
p("reindex fill_value", lambda: mdf2.reindex(pd.MultiIndex.from_tuples([("a",1),("z",9)]), fill_value=0).shape)
p("align", lambda: [x.shape for x in mdf2.align(mdf2.iloc[:2], join="outer")])
p("combine_first", lambda: mdf2.combine_first(mdf2).shape)
p("update", lambda: (mdf2.copy().update(mdf2), "ok")[1])
p("mask/where", lambda: mdf2.where(mdf2.v>1).shape)
p("memory_usage index", lambda: int(mdf2.memory_usage(deep=True).sum()))
p("mi codes/levels", lambda: (mi2.codes[0].tolist(), [list(l) for l in mi2.levels]))
p("agg axis=1", lambda: pd.DataFrame({"a":[1],"b":[2]}).agg("sum", axis=1).tolist())
p("df.T with mi", lambda: mdf2.T.shape)

# ---------- window / ts ----------
ts = pd.Series(range(10), index=pd.date_range("2024-01-01", periods=10, freq="D"))
p("rolling mean", lambda: ts.rolling(3).mean().dropna().shape)
p("rolling window '3D'", lambda: ts.rolling("3D").sum().shape)
p("resample", lambda: ts.resample("W").sum().shape)
p("resample ME", lambda: ts.resample("ME").sum().shape)
p("ewm", lambda: ts.ewm(span=3).mean().shape)
p("shift freq", lambda: ts.shift(1, freq="D").index[0])
p("tz_localize", lambda: ts.tz_localize("UTC").tz_convert("Asia/Karachi").index[0])
p("PeriodIndex asfreq", lambda: pd.period_range("2024-01", periods=2, freq="M").asfreq("D").astype(str).tolist())
p("dt.day_name", lambda: ts.index.day_name()[:2].tolist())
p("offsets BDay", lambda: (pd.Timestamp("2024-01-05") + pd.tseries.offsets.BDay(1)).date())

# ---------- misc perf ----------
p("itertuples", lambda: next(iter(g.itertuples(index=False)))._asdict())
p("iterrows", lambda: next(iter(g.iterrows()))[0])
p("np.select", lambda: np.select([g.v<3,g.v<5],["lo","mid"],default="hi").tolist())
p("at vs loc", lambda: g.at[0,"v"])
p("index.is_unique", lambda: g.index.is_unique)
p("index.is_monotonic_increasing", lambda: g.index.is_monotonic_increasing)
p("nlargest", lambda: g.nlargest(2,"v").shape)
p("drop_duplicates subset keep", lambda: g.drop_duplicates(subset="k", keep="last").shape)
p("str accessor", lambda: pd.Series(["ab","cd"]).str.upper().tolist())
p("str dtype .str", lambda: str(pd.Series(["ab"]).str.len().dtype))
p("assert_frame_equal", lambda: (pd.testing.assert_frame_equal(g,g), "ok")[1])
p("show_versions", lambda: type(pd.show_versions).__name__)
p("options display", lambda: pd.get_option("display.max_rows"))
p("infer_objects", lambda: str(pd.Series([1,2],dtype=object).infer_objects().dtype))
p("pd.array", lambda: str(pd.array([1,2]).dtype))
p("factorize", lambda: [x.tolist() if hasattr(x,'tolist') else list(x) for x in pd.factorize(["a","b","a"])])
p("get_dummies dtype", lambda: pd.get_dummies(pd.Series(["a","b"])).dtypes.astype(str).to_dict())
p("cat codes memory", lambda: str(pd.Series(["a"]*5).astype("category").cat.codes.dtype))
p("corr", lambda: dd.corr().shape)
p("rank pct", lambda: g["v"].rank(pct=True).round(2).tolist())
p("nunique dropna", lambda: g.nunique().to_dict())
p("value_counts normalize", lambda: g.k.value_counts(normalize=True).to_dict())
p("select_dtypes", lambda: g.select_dtypes("number").columns.tolist())
p("pipe", lambda: g.pipe(lambda d: d.shape))
p("assign multi", lambda: g.assign(a=lambda d: d.v*2, b=lambda d: d.a+1).shape)
p("filter regex", lambda: g.filter(regex="^v$").shape)
p("empty df ops", lambda: pd.DataFrame({"a":[]}).groupby("a").size().shape)
p("all-NaN mean", lambda: pd.Series([np.nan]).mean())
p("df.info deep", lambda: (pd.DataFrame({"a":[1]}).info(buf=io.StringIO(), memory_usage="deep"), "ok")[1])
print("PROBE DONE")
