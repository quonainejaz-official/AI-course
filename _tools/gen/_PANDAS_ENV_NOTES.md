# ENV NOTES — Pandas authors (pandas 3.0.5 par PROBE kiye hue asli facts, guess NAHI)

`AGENT_SPEC.md` ke saath ye bhi LAZMI follow karo. Har row `runnb.py` ke asli
environment par test kar ke likhi gayi hai (`_tools/gen/_pandas_probe.py`, `_pandas_probe2.py`).

## Runtime
- Python **3.14.0**, **pandas 3.0.5**, numpy 2.4.2. matplotlib/seaborn NAHI. Network NAHI. `input()` NAHI.
- `runnb.py` har code cell ko **shared namespace** me `exec()` karta hai, cwd = fresh temp dir.
- Koi bhi cell **exception** phenke to `[FAIL]`. **Warning se FAIL nahi hota**, magar phir bhi
  jaan-boojh kar warning wale demo ko `warnings.catch_warnings()` me lapeto (output saaf rehta hai).

## SAB SE BARA CHANGE: default string dtype `str` hai (object NAHI) — PDEP-14
```
pd.DataFrame({"c": ["x","y"]}).dtypes   ->  c    str
pd.Series(["a"]).dtype                 ->  <StringDtype(storage='python', na_value=nan)>
df.info() ki Dtype column me "str" likha aata hai, "object" nahi
```
- Missing value is `str` dtype me **`nan`** hota hai (`pd.NA` nahi): `pd.Series(["a", pd.NA]).tolist()` → `['a', nan]`.
- `astype("string")` alag cheez hai → `StringDtype(na_value=<NA>)` (nullable semantics).
- `astype(object)` se purana `object` dtype milta hai (comparison sikhane ke liye useful).
- **`select_dtypes(include="object")` par `Pandas4Warning`** aata hai (str columns bhi aa jate hain,
  deprecated). Sikhao: `select_dtypes(include="str")`. `include="number"` theek hai.
- `pd.api.types.is_string_dtype(s)` → True; `s.dtype == "str"` → True.
- `.array` on str col → `StringArray`; int col par → `NumpyExtensionArray`; `.values`/`to_numpy()` → object ndarray.

## HATA DIYE GAYE / TOOT GAYE (as-is MAT likho; `try/except AttributeError|TypeError` me dikhao)
| Purana code | Ab kya hota hai | Kya likhna hai |
|---|---|---|
| `df.append(...)` | `AttributeError` | `pd.concat([df, pd.DataFrame([row])], ignore_index=True)` |
| `df.applymap(f)` | `AttributeError` | `df.map(f)` (DataFrame.map) |
| `df.iteritems()` | `AttributeError` | `df.items()` |
| `pd.errors.SettingWithCopyWarning` | `AttributeError` (class hi nahi hai) | `pd.errors.ChainedAssignmentError` (ye ek **Warning** subclass hai) |
| `s.fillna(method="ffill")` | `TypeError: unexpected keyword 'method'` | `s.ffill()` / `s.bfill()` |
| `pd.to_numeric(s, errors="ignore")` | `ValueError: invalid error value` | `errors="coerce"` ya `errors="raise"` |
| `pd.to_datetime(s, errors="ignore")` | `AssertionError` | `errors="coerce"` |
| `pd.to_datetime(s, infer_datetime_format=True)` | `TypeError` | `format="mixed"` ya explicit `format=` |
| `pd.factorize(["a","b"])` (plain list) | `TypeError: factorize requires a Series/Index/...` | `pd.factorize(pd.Series([...]))` ya `np.array([...])` |
| `freq="M"` | `ValueError: 'M' is no longer supported` | `freq="ME"` (month end). `"D"`, `"h"` theek hain |
| `s.astype("int64")` jab NaN ho | `IntCastingNaNError` | `astype("Int64")` (nullable) — **best dtype gotcha demo** |
| `df.mean()` jab str column ho | `TypeError: Cannot perform reduction 'mean' with string dtype` | `df.mean(numeric_only=True)` |
| `df.corr()` jab str column ho | `ValueError: could not convert string to float` | `df.corr(numeric_only=True)` |
| `df.reindex([...], fill_value=0)` jab str col ho | `TypeError: Invalid value '0' for dtype 'str'` | numeric-only frame par demo karo, ya `fill_value=""` |
| duplicate index par `reindex` | `ValueError: cannot reindex on an axis with duplicate labels` | accha gotcha — `try/except` me dikhao |

## Copy-on-Write (pandas 3 default) — VERIFIED behaviour
```python
d = pd.DataFrame({"a":[1,2,3]})
d[d["a"] > 1]["a"] = 99     # -> ChainedAssignmentError WARNING, aur d BILKUL nahi badalta -> [1,2,3]
d["a"][0] = 99              # -> wahi warning, koi asar nahi
d["a"].fillna(0, inplace=True)  # -> wahi warning, koi asar nahi  => "inplace se bacho" ka proof
d.loc[d["a"] > 1, "a"] = 99 # -> SAHI tareeqa -> [1, 99, 99]
```
- Filtered subset par `.loc` se likhna **warning nahi** deta aur original ko **nahi** badalta
  (`sub = d[d["a"]>1]; sub.loc[...] = 99` → sirf `sub` badla).
- Parent ko badalne se pehle liya hua `s = d["a"]` bhi **nahi** badalta (CoW).
- Chained-assignment demo ko `warnings.catch_warnings(); simplefilter("ignore")` me rakho.

## `describe()` / `info()` ki asli shakal (assert likhte waqt kaam aayega)
- `df.describe(include="all").index` → `['count','unique','top','freq','mean','std','min','25%','50%','75%','max']`
- `df.describe()` default sirf numeric columns leta hai; str col ka describe → `['count','unique','top','freq']`
- `df.describe()` **bool column ko numeric nahi ginta**, magar `df.mean(numeric_only=True)` **bool ko ginta hai** (`d: 0.667`).
- `df.sum()` mixed par chalta hai: str column concatenate ho jata hai (`'xyz'`) — funny gotcha.

## Datetime
- **Default unit `us` hai, `ns` nahi**: `pd.date_range(...).dtype` → `datetime64[us]`,
  `pd.to_datetime(Series).dtype` → `datetime64[us]`, `read_csv(parse_dates=)` → `datetime64[us]`.
  Isliye `assert s.dtype == "datetime64[ns]"` **MAT** likho → `pd.api.types.is_datetime64_any_dtype(s)` use karo.
- `astype("datetime64[ns]")` explicit ho to `ns` milta hai.
- `.dt` accessor verified: `year/month/day/dayofweek/day_name()/quarter/hour/date/normalize()/days_in_month/is_month_end/strftime()`
- `(s - pd.Timestamp("...")).dt.days` verified.
- `to_json` → `read_json` par dates **int64 epoch** ban jati hain + `Pandas4Warning`. Isliye
  JSON round-trip me dates ko pehle `strftime` se string bana lo, ya `Pandas4Warning` suppress karo,
  ya sirf non-date columns ka JSON round-trip dikhao.

## Ye sab VERIFIED chalte hain (be-fikr use karo)
`loc/iloc/at/iat`, `loc` callable, `loc` slice inclusive, `query("a > @lim")`, backtick `` `my col` ``,
`eval`, `where/mask`, `filter(like=/regex=)`, `nlargest/nsmallest(keep=)`, `idxmax/idxmin`,
`between(inclusive=)`, `isin`, `sample(random_state=)`, `sort_values(kind="mergesort", na_position=)`,
`sort_index`, `rank(method=average/min/dense/first, pct=True)`, `set_index(append=)`, `reset_index(names=)`,
`reindex(method="ffill")`, `rename(columns=str.upper)`, `rename_axis`, `add_prefix/add_suffix`,
`insert`, `pop`, `drop(columns=/index=)`, `df.loc[len(df)] = [...]`, `pd.concat(keys=/axis=1/ignore_index=)`,
`duplicated(subset=,keep=)`, `drop_duplicates`, `dropna(axis/how/thresh/subset)`,
`fillna(scalar/dict)`, `ffill(limit=)/bfill`, `interpolate()` + `interpolate(method="time")` (datetime index par),
`isna/notna/isnull`, `replace(scalar/list->list/dict/nested/regex=True)`, `clip`, `round(dict)`, `abs`,
`cut(bins,labels,right,include_lowest,retbins)`, `qcut(duplicates="drop", labels=False)`,
`get_dummies(drop_first=)` → **bool** columns, `str.get_dummies("|")`,
`value_counts(normalize/dropna=False/bins=)`, `unique/nunique(dropna=)`, `mode()`,
`.str` sab: `strip/lower/upper/title/replace(regex=True)/contains(na=False)/startswith/extract/split(expand=True)/len/zfill/pad/cat`,
`map(dict/func, na_action="ignore")`, `apply(axis=1, raw=True)`, `df.map`, `assign(lambda)`, `pipe`,
`groupby(...).mean()/agg(dict)/size()/transform("mean")/apply()/head()/nlargest()`,
`pd.crosstab(normalize=,margins=)`, `pd.pivot_table(margins=)`, `df.pivot`, `pd.melt`,
`corr(numeric_only=True)`, `cumsum`, `T`, `to_frame`, `squeeze`, `equals`, `pd.testing.assert_frame_equal`,
`memory_usage(deep=True)`, `to_numeric(downcast="integer"/"float")`, `astype("category")` + `.cat.codes`,
ordered Categorical `max()`, `pd.array`, `pd.json_normalize`, `to_dict("records")`,
`read_csv(sep/header/names/index_col/usecols/dtype/na_values/parse_dates/nrows/skiprows/encoding/thousands/chunksize)`,
`pd.set_option/get_option/reset_option/option_context`, `hasattr(pd,"read_excel"/"read_parquet"/"read_sql")` → True.

## Assert likhne ke rules
- Aggregations **numpy scalar** deti hain (`np.int64(6)`); `== 6` chalta hai, ya `int(...)` se convert karo.
- `assert s.tolist() == [...]`, `assert df.shape == (r, c)`, `pd.testing.assert_frame_equal(a, b)` use karo.
- NaN ke sath `==` kabhi True nahi (`np.nan == np.nan` → False) → `.isna()` par assert karo.
- `bool(pd.NA)` → `TypeError: boolean value of NA is ambiguous` (accha gotcha cell).
- `memory_usage` ke exact bytes machine-specific → **print karo, assert na karo**
  (`df.memory_usage(deep=True).sum()` sirf print). Shape/dtype par assert theek hai.
- `sample(random_state=0)` deterministic hai magar exact indices par assert se bacho — `.shape` par karo.
- **Timing-based assert NAHI** (`assert fast < slow` mana hai) — sirf print + samjhao.
  `timeit.timeit("...", globals=globals(), number=...)` me `globals=globals()` LAZMI.

## Timing / size
- Notebook total **< ~30 second**. Datasets chhote rakho (60-200 rows). `timeit` ka `number` chhota (100-1000).
- Har notebook ke shuru me: `import numpy as np, pandas as pd` + `print(pd.__version__)`.
- Random data ho to `np.random.default_rng(42)` (seed LAZMI) — magar practice dataset preferably
  hard-coded lists se banao taake outputs deterministic aur explainable rahen.
