"""Probe round 2. Run: python _tools/gen/_pandas_probe2.py"""
import io, sys, time, timeit, warnings, tempfile, os, json
import numpy as np
import pandas as pd

def t(label, fn):
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            r = fn()
        cats = sorted({x.category.__name__ for x in w})
        extra = f"   WARN={cats}" if cats else ""
        print(f"[OK ] {label} -> {r!r}"[:300] + extra)
    except Exception as e:
        print(f"[ERR] {label} -> {type(e).__name__}: {e}"[:300])

df = pd.DataFrame({"a": [1, 2, 3], "b": [1.5, 2.5, 3.5], "c": ["x", "y", "z"], "d": [True, False, True]})

print("== numeric_only / mixed dtype aggregations ==")
t("df.mean() mixed", lambda: df.mean().to_dict())
t("df.mean(numeric_only=True)", lambda: df.mean(numeric_only=True).to_dict())
t("df.sum() mixed", lambda: df.sum().to_dict())
t("df.describe() default", lambda: df.describe().columns.tolist())
t("df.corr() mixed", lambda: df.corr().shape)
t("df.corr(numeric_only=True)", lambda: df.corr(numeric_only=True).shape)
t("df.median() mixed", lambda: df.median(numeric_only=True).to_dict())
t("df.max() mixed", lambda: df.max().to_dict())
t("df.groupby('c').mean()", lambda: df.groupby("c").mean().shape)
t("df.groupby('c').agg dict", lambda: df.groupby("c").agg({"a": "sum", "b": "mean"}).shape)
t("groupby.apply(lambda g: g['a'].sum())", lambda: df.groupby("c").apply(lambda g: g["a"].sum()).to_dict())
t("groupby.apply include_groups", lambda: df.groupby("c")[["a"]].apply(lambda g: g["a"].sum()).to_dict())
t("groupby.size", lambda: df.groupby("c").size().to_dict())
t("groupby.transform mean numeric", lambda: df.groupby("d")["a"].transform("mean").tolist())
t("groupby nlargest per group", lambda: df.groupby("d")["a"].nlargest(1).tolist())
t("groupby head(2)", lambda: df.groupby("d").head(2).shape)

print("== datetime units ==")
t("date_range dtype", lambda: pd.date_range("2024-01-01", periods=3).dtype)
t("to_datetime series dtype", lambda: pd.to_datetime(pd.Series(["2024-01-01"])).dtype)
t("Timestamp('now') - ts days", lambda: (pd.Timestamp("2024-01-10") - pd.Timestamp("2024-01-01")).days)
t("dt subtraction / timedelta days", lambda: (pd.to_datetime(pd.Series(["2024-03-01"])) - pd.Timestamp("2024-01-01")).dt.days.tolist())
t("date_range freq ME", lambda: pd.date_range("2024-01-01", periods=3, freq="ME").strftime("%Y-%m-%d").tolist())
t("date_range freq M (old)", lambda: pd.date_range("2024-01-01", periods=2, freq="M").tolist())
t("date_range freq 'D' 60", lambda: len(pd.date_range("2024-01-01", periods=60, freq="D")))
t("read_csv parse_dates dtype", lambda: pd.read_csv(io.StringIO("d\n2024-01-01"), parse_dates=["d"])["d"].dtype)
t("astype datetime64[ns]", lambda: pd.Series(["2024-01-01"]).astype("datetime64[ns]").dtype)

print("== misc api ==")
t("factorize Series", lambda: [x.tolist() if hasattr(x, 'tolist') else x for x in pd.factorize(pd.Series(["b", "a", "b"]))])
t("factorize np.array", lambda: pd.factorize(np.array(["b", "a"]))[0].tolist())
t("between inclusive", lambda: df["a"].between(1, 3, inclusive="neither").tolist())
t("crosstab normalize", lambda: pd.crosstab(df["c"], df["d"], normalize=True).values.sum())
t("crosstab margins", lambda: pd.crosstab(df["c"], df["d"], margins=True).shape)
t("pivot_table margins", lambda: pd.pivot_table(df, values="a", index="c", aggfunc="sum", margins=True).shape)
t("value_counts dropna=False str NaN", lambda: pd.Series(["a", None]).value_counts(dropna=False).to_dict())
t("value_counts normalize", lambda: pd.Series(["a", "a", "b"]).value_counts(normalize=True).to_dict())
t("nunique dropna=False", lambda: pd.Series(["a", None]).nunique(dropna=False))
t("cut retbins", lambda: pd.cut(pd.Series([1, 5]), bins=2, retbins=True)[1].tolist())
t("qcut duplicates drop", lambda: pd.qcut(pd.Series([1, 1, 1, 2]), 4, duplicates="drop", labels=False).tolist())
t("loc callable", lambda: df.loc[lambda d: d["a"] > 1].shape)
t("reset_index names", lambda: df.set_index("c").reset_index(names="letter").columns.tolist())
t("drop columns=", lambda: df.drop(columns=["a"]).columns.tolist())
t("drop index=", lambda: df.drop(index=[0]).shape)
t("concat axis=1", lambda: pd.concat([df["a"], df["b"]], axis=1).shape)
t("concat keys", lambda: pd.concat([df, df], keys=["p", "q"]).index.nlevels)
t("pd.array([1,2])", lambda: pd.array([1, 2]).dtype)
t("Series.values int", lambda: type(pd.Series([1, 2]).values).__name__)
t("to_numeric '1,200'", lambda: pd.to_numeric(pd.Series(["1,200"]), errors="coerce").tolist())
t("astype Int64 from float w/ nan", lambda: pd.Series([1.0, np.nan]).astype("Int64").tolist())
t("astype int from float w/ nan", lambda: pd.Series([1.0, np.nan]).astype("int64").tolist())
t("Int64 + int", lambda: (pd.Series([1, None], dtype="Int64") + 1).tolist())
t("str col + str", lambda: (df["c"] + "!").tolist())
t("str.len", lambda: pd.Series(["abc"]).str.len().tolist())
t("str col sum error?", lambda: df["c"].sum())
t("df.dtypes value counts", lambda: df.dtypes.astype(str).tolist())
t("dtype comparison == 'str'", lambda: df["c"].dtype == "str")
t("isinstance str dtype", lambda: pd.api.types.is_string_dtype(df["c"]))
t("info memory deep", lambda: (df.info(buf=io.StringIO(), memory_usage="deep"), "ok")[1])
t("assert_frame_equal", lambda: (pd.testing.assert_frame_equal(df, df.copy()), "ok")[1])
t("df.equals", lambda: df.equals(df.copy()))
t("to_json/read_json dates", lambda: pd.read_json(io.StringIO(pd.DataFrame({"d": pd.date_range('2024-01-01', periods=2)}).to_json(orient="records")), orient="records")["d"].dtype)
t("Series.to_frame", lambda: df["a"].to_frame().shape)
t("df.T", lambda: df.T.shape)
t("np.where 3 args on str", lambda: pd.Series(np.where(df["a"] > 1, "big", "small")).dtype)
t("df.insert", lambda: (lambda d: (d.insert(0, "z", 0), d.columns.tolist())[1])(df.copy()))
t("df.pop", lambda: (lambda d: (d.pop("a").tolist(), d.columns.tolist()))(df.copy()))
t("df.iloc[-1]", lambda: df.iloc[-1].to_dict())
t("df.iloc[0:2, 0:2]", lambda: df.iloc[0:2, 0:2].shape)
t("df.loc[0:1] inclusive", lambda: df.loc[0:1].shape)
def _atset():
    d = df.copy()
    d.at[0, "a"] = 0
    return d["a"].tolist()
t("df.at set", _atset)
t("style hidden", lambda: True)
t("read_csv usecols+dtype+index_col", lambda: pd.read_csv(io.StringIO("i,a,b\n1,2,3"), usecols=["i", "a"], dtype={"a": "Int64"}, index_col="i").dtypes.astype(str).to_dict())
t("read_csv names+header=None+skiprows", lambda: pd.read_csv(io.StringIO("junk\n1,2"), header=None, names=["x", "y"], skiprows=1).shape)
t("read_csv nrows", lambda: pd.read_csv(io.StringIO("a\n1\n2\n3"), nrows=2).shape)
t("read_csv sep=';'", lambda: pd.read_csv(io.StringIO("a;b\n1;2"), sep=";").shape)
t("read_csv encoding", lambda: pd.read_csv(io.StringIO("a\n1"), encoding="utf-8").shape)
t("read_csv chunksize", lambda: sum(len(c) for c in pd.read_csv(io.StringIO("a\n1\n2\n3"), chunksize=2)))
t("clipboard/excel readers exist", lambda: (hasattr(pd, "read_excel"), hasattr(pd, "read_parquet"), hasattr(pd, "read_sql")))
t("tempfile csv roundtrip", lambda: (lambda p: (df.to_csv(p, index=False), pd.read_csv(p).shape)[1])(os.path.join(tempfile.mkdtemp(), "x.csv")))
t("df.to_dict('records')", lambda: df.to_dict("records")[0])
t("pd.json_normalize", lambda: pd.json_normalize([{"a": {"b": 1}}]).columns.tolist())
t("df.memory_usage index", lambda: df.memory_usage().index.tolist())
t("downcast float", lambda: pd.to_numeric(pd.Series([1.0, 2.0]), downcast="float").dtype)
t("category codes", lambda: pd.Series(["a", "b"], dtype="category").cat.codes.tolist())
t("category ordered compare", lambda: pd.Series(pd.Categorical(["lo", "hi"], categories=["lo", "hi"], ordered=True)).max())
t("timeit with globals", lambda: round(timeit.timeit("df['a'].sum()", globals=globals(), number=100), 5))
t("iterrows timing loop 3 rows", lambda: sum(r["a"] for _, r in df.iterrows()))
t("df.apply raw", lambda: df[["a", "b"]].apply(np.sum, axis=1, raw=True).tolist())
t("Series.map with Series arg", lambda: pd.Series(["a"]).map(pd.Series({"a": 1})).tolist())
t("df.rename func", lambda: df.rename(columns=str.upper).columns.tolist())
t("df.rename index dict", lambda: df.rename(index={0: "first"}).index.tolist())
t("df.reindex columns", lambda: df.reindex(columns=["a", "zz"]).columns.tolist())
t("df.reindex fill_value", lambda: df.reindex([0, 9], fill_value=0)["a"].tolist())
t("dup index loc", lambda: pd.Series([1, 2], index=["a", "a"]).loc["a"].tolist())
t("dup index reindex err", lambda: pd.Series([1, 2], index=["a", "a"]).reindex(["a"]))
t("df.duplicated().sum()", lambda: int(pd.DataFrame({"a": [1, 1]}).duplicated().sum()))
t("isna on str dtype col with None", lambda: pd.DataFrame({"c": ["a", None]}).isna().sum().to_dict())
t("dropna subset", lambda: pd.DataFrame({"a": [1, None], "b": [1, 2]}).dropna(subset=["a"]).shape)
t("fillna dict", lambda: pd.DataFrame({"a": [1, None], "b": [None, 2]}).fillna({"a": 0, "b": -1}).values.tolist())
t("fillna mode()[0]", lambda: pd.Series(["a", None, "a"]).fillna(pd.Series(["a", None, "a"]).mode()[0]).tolist())
t("ffill/bfill methods", lambda: (pd.Series([1, None]).ffill().tolist(), pd.Series([None, 1]).bfill().tolist()))
t("df.interpolate on df", lambda: pd.DataFrame({"a": [1.0, None, 3.0]}).interpolate().values.ravel().tolist())
t("replace list->list", lambda: pd.Series([1, 2]).replace([1, 2], [10, 20]).tolist())
t("replace with nan then downcast warn", lambda: pd.Series([1, 2]).replace(2, np.nan).tolist())
t("clip lower/upper both", lambda: pd.Series([-5, 5, 50]).clip(0, 10).tolist())
t("round dict", lambda: pd.DataFrame({"a": [1.234]}).round({"a": 2}).values.tolist())
t("abs", lambda: pd.Series([-1]).abs().tolist())
t("rank pct", lambda: pd.Series([1, 2]).rank(pct=True).tolist())
t("sort_index ascending False", lambda: df.sort_index(ascending=False).index.tolist())
t("df.sample frac", lambda: df.sample(frac=0.5, random_state=1).shape)
t("df.squeeze scalar", lambda: pd.DataFrame({"a": [1]}).squeeze())
t("df.nlargest keep", lambda: df.nlargest(2, "a", keep="last").index.tolist())
t("idxmin on str", lambda: df["c"].idxmin())
t("df.eval assign", lambda: df.eval("e = a + b").columns.tolist())
t("df.query engine", lambda: df.query("a > 1 and c == 'y'").shape)
t("df.query backtick col", lambda: pd.DataFrame({"my col": [1, 2]}).query("`my col` > 1").shape)
t("mask/where other df", lambda: df[["a"]].where(df[["a"]] > 1, other=0).values.ravel().tolist())
t("pd.concat ignore_index new row", lambda: pd.concat([df, pd.DataFrame([{"a": 9, "b": 9.9, "c": "w", "d": False}])], ignore_index=True).shape)
t("pd.concat dtype preserved", lambda: pd.concat([df, pd.DataFrame([{"a": 9, "b": 9.9, "c": "w", "d": False}])], ignore_index=True).dtypes.astype(str).to_dict())
def _addrow():
    d = df.copy()
    d.loc[len(d)] = [9, 9.9, "w", False]
    return d.shape
t("df.loc[len(df)] = row", _addrow)

print("== chained assignment / CoW details ==")
d = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
t("ChainedAssignmentError is Warning subclass", lambda: issubclass(pd.errors.ChainedAssignmentError, Warning))
def chained():
    dd = pd.DataFrame({"a": [1, 2, 3]})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dd["a"][0] = 99
    return dd["a"].tolist()
t("dd['a'][0]=99", chained)
def proper():
    dd = pd.DataFrame({"a": [1, 2, 3]})
    dd.loc[dd["a"] > 1, "a"] = 99
    return dd["a"].tolist()
t("proper .loc assign", proper)
def viewcheck():
    dd = pd.DataFrame({"a": [1, 2, 3]})
    s = dd["a"]
    dd.loc[0, "a"] = 100
    return s.tolist()
t("series view after parent modify", viewcheck)
t("np.shares_memory", lambda: np.shares_memory(d["a"].to_numpy(), d["a"].to_numpy()))

print("== warnings audit for common teaching patterns ==")
for label, fn in [
    ("select_dtypes(object)", lambda: df.select_dtypes(include="object")),
    ("df.astype(str)", lambda: df.astype(str).dtypes.tolist()),
    ("series.astype(object)", lambda: pd.Series(["a"]).astype(object).dtype),
    ("groupby.apply full", lambda: df.groupby("d").apply(lambda g: g["a"].mean())),
    ("df.replace downcast", lambda: pd.Series([1.0, 2.0]).replace(2.0, 1)),
    ("bfill/ffill axis=1", lambda: pd.DataFrame({"a": [1.0, None]}).ffill(axis=1)),
    ("df.fillna(0) on str col", lambda: pd.DataFrame({"c": ["a", None]}).fillna("missing")),
    ("pd.concat empty", lambda: pd.concat([pd.DataFrame(), df])),
    ("df.sum(axis=1) mixed", lambda: df[["a", "b"]].sum(axis=1)),
    ("str.contains no na", lambda: pd.Series(["a", None]).str.contains("a")),
]:
    t(label, fn)
print("done")
