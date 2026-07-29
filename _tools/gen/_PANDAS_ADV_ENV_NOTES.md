# ENV NOTES — Pandas/Advance authors (sab facts asli probe se verified, GUESS NAHI)

Probes: `_tools/gen/_pandas_adv_probe.py`, `_pandas_adv_probe2.py`, `_pandas_adv_probe3.py`
(outputs: `_probe_out.txt`, `_probe_out2.txt`, `_probe_out3.txt`).
`AGENT_SPEC.md` + ye file dono LAZMI follow karo.

## Runtime
- Python **3.14.0**, numpy **2.4.2**, pandas **3.0.5**, sqlite3 lib **3.50.4**.
- `runnb.py` har code cell ko ek **shared namespace** me `exec()` karta hai, cwd fresh temp dir.
  Magics (`%%timeit`, `%timeit`) = SyntaxError → **bilkul na likho**, sirf markdown me zikr karo.
- Har notebook total **< 40 second**.

## INSTALLED / MISSING (verified)
| lib | status |
|---|---|
| jinja2 3.1.6 | present (`df.style` object banta hai) |
| **pyarrow** | **MISSING** |
| **numexpr** | **MISSING** |
| **bottleneck** | MISSING |
| **tabulate** | **MISSING** → `to_markdown()` ImportError |
| **tables (pytables)** | MISSING → `to_hdf` ImportError |
| matplotlib/seaborn | MISSING |
| sqlalchemy, scipy, numba, swifter, openpyxl, fastparquet | MISSING |

### Iska matlab (bohat ahem)
- `to_parquet` / `to_feather` / `read_parquet` / `engine="pyarrow"` / `string[pyarrow]` /
  `dtype_backend="pyarrow"` / `pd.ArrowDtype` → **sab fail**. Inhe **`try/except ImportError`** me
  wrap kar ke "pyarrow install ho to ye milta" note print karo. Ye spec me allowed hai.
- `dtype_backend="numpy_nullable"` **kaam karta hai** (`Int64`/`string`) → pyarrow ka substitute demo.
- `to_markdown()` fail → apna chhota `md_table(df)` helper likho (verified pattern):
  ```python
  def md_table(d):
      cols = list(d.columns)
      head = "| " + " | ".join(map(str, cols)) + " |"
      sep  = "|" + "|".join("---" for _ in cols) + "|"
      rows = ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)]
      return "\n".join([head, sep] + rows)
  ```
  `to_markdown` ko sirf `try/except` demo ke tor par dikhao. `to_string()` **kaam karta hai**.
- `pd.eval(..., engine="numexpr")` → ImportError. **`df.eval()` / `df.query()` default engine
  kaam karte hain** (numexpr na ho to python fallback) → "numexpr hota to itna faida" markdown me.
- Persistence ke liye jo **kaam karta hai**: CSV, `to_pickle`/`read_pickle`, `sqlite3` (`to_sql`/`read_sql`), JSON.
  IO benchmark table inhi 3-4 formats par banao + parquet ka try/except note.

## pandas 3.0 me jo BADAL/HAT gaya (verified)
| cheez | pandas 3.0.5 me natija |
|---|---|
| default string dtype | `pd.Series(["a"]).dtype` → **`str`** (class `StringDtype`), object NAHI |
| str col memory | python-backed `str` ka `memory_usage(deep=True)` object ke **barabar** (50k rows city: 2.80 MB); `category` → 0.05 MB (~56x) |
| `df.append` / `Series.append` / `applymap` / `iteritems` | **hat gaye** (`hasattr` → False). `DataFrame.map` maujood |
| `df.sum(level=0)` | `TypeError` → `df.groupby(level=0).sum()` |
| `df.sortlevel()` | gone. `df.index.sortlevel(0)` maujood; `df.sort_index(level=)` use karo |
| `index.is_lexsorted()` | gone. `df.index._lexsort_depth` (private) → unsorted 0, sorted 2 |
| `pd.Int64Index` | `AttributeError` → `pd.Index([...], dtype="int64")` |
| `fillna(method="ffill")` | `TypeError` → `.ffill()` |
| `stack(dropna=...)` | `ValueError` (new impl). `stack()` **NaN drop nahi karta** ab |
| `stack(future_stack=True)` | chalta hai, no warning (no-op — naya behaviour default hai) |
| `pd.concat(..., copy=False)` | `Pandas4Warning` → `copy=` kwarg **na do** |
| `pd.errors.SettingWithCopyWarning` | `AttributeError` (gone). `pd.errors.ChainedAssignmentError` maujood |
| freq aliases | `"M"`/`"H"`/`"Q"`/`"Y"` → **ValueError**. `"ME"`, `"MS"`, `"QE"`, `"YE"`, `"h"`, `"D"`, `"W"` use karo |
| datetime default unit | `date_range`/`to_datetime` → **`datetime64[us]`** (ns nahi!), diff → `timedelta64[us]` |
| `pd.array([1,2])` | dtype **`Int64`** (nullable by default) |
| `pd.factorize(["a","b"])` (plain list) | `TypeError` → Series/Index/ndarray do |
| `get_dummies` | dtype **`bool`** |
| groupby `observed` | default **True** (unused categories nahi aate) |
| `groupby.apply` | grouping column by default pass nahi hoti; `include_groups=False` kwarg maujood |
| `df.at[("a",1), "v"]` (MultiIndex tuple) | `ValueError` → `.loc` use karo |
| `Series.view`, `df.swapaxes` | gone |
| `read_sql(parse_dates=)` | `datetime64[us]` |
| sqlite text column read back | dtype `str` |

## Copy-on-Write (default ON: `pd.get_option("mode.copy_on_write")` → True)
- `d["a"][0] = 99` → value **update NAHI hoti** aur `ChainedAssignmentError` **warning** (exception nahi)
  emit hoti hai. Demo `warnings.catch_warnings(record=True)` me lo aur original value print karo.
- `d[d.a>1]["a"] = 5` → **koi error nahi, chup-chaap no-op** (yeh sab se khatarnak). Zaroor dikhao.
- `v = d["a"]; d.loc[0,"a"] = 100` → `v` **purani value** rakhta hai (lazy copy).
- `fillna(..., inplace=True)` par koi warning nahi aati — magar spec ke mutabiq **reassignment sikhao**.

## Verified-working APIs (bila jhijhak use karo)
MultiIndex: `from_tuples/from_arrays/from_product`, `set_index`, `.loc[("a",1)]`, `.loc["a"]`,
`pd.IndexSlice`, `xs(level=, axis=, drop_level=)`, `.loc[[("a",1),("b",2)]]`, `droplevel`,
`swaplevel`, `reorder_levels`, `rename_axis`, `index.set_names`, `sort_index(level=, ascending=[..])`,
`reindex(mi, fill_value=)`, `align(join=)`, `combine_first`, `update`, `where/mask`,
`groupby(level=)`, `agg(axis=1)`, `index.codes/levels/nlevels/get_level_values`,
`index.is_monotonic_increasing`, `index._lexsort_depth`, `stack([0,1])`, `unstack(fill_value=)`,
`pivot_table(margins=True)`, `wide_to_long`, `melt`, `crosstab(margins=)`, `explode` (multi-col bhi),
`json_normalize(record_path=, meta=)`, `IntervalIndex.from_breaks/get_indexer/get_loc`,
`pd.cut(bins=IntervalIndex)`, `qcut(duplicates="drop")`, `CategoricalIndex`, `period_range`.

Perf/dtypes: `to_numeric(downcast="unsigned"→uint32)`, `astype("category")`, `convert_dtypes()`,
`convert_dtypes(dtype_backend="numpy_nullable")`, `read_csv(dtype_backend="numpy_nullable")`,
`memory_usage(deep=True)`, `info(buf=io.StringIO(), memory_usage="deep")`, `tracemalloc`,
`pd.SparseDtype("float64", 0.0)`, `Sparse` accessors (`.sparse.density`, `.sparse.to_dense()`),
`read_csv(dtype=..., usecols=..., low_memory=..., chunksize=...)`, `to_pickle`, `to_sql`,
`read_sql(..., chunksize=)`, `read_sql_query(params=)`, `merge(validate=, indicator=)`,
`merge_asof`, `nlargest(keep="all")`, `df.map`, `Series.case_when`, `np.select`, `np.where`.

**Sparse gotcha (verified, zaroor sikhao):** 0-heavy data par `astype("Sparse[float]")` ka default
`fill_value=nan` hai → memory **barh** jati hai (160KB → 240KB). Sahi tareeqa:
`astype(pd.SparseDtype("float64", 0.0))` → **2.5KB**.

Window/analytics: `groupby().rank(method=)/cumcount()/shift()/cumsum()/cummax()/transform()/
rolling()/expanding()/nth()/head()/tail()/ngroup()/pct_change()/size()`, `rolling("3D")`,
`ewm(span=)`, `resample("ME"/"W"/"MS")`, `shift(freq="D")`, `tz_localize/tz_convert`,
`dt.day_name()`, `pd.tseries.offsets.BDay`, `Period` arithmetic, `rank(pct=True)`.

Testing: `pd.testing.assert_frame_equal(..., check_dtype=False, check_like=True)`, `assert_series_equal`.
Stdlib: `statistics.NormalDist().cdf()` (z-test ke liye), `statistics.fmean`, `logging`, `unittest`,
`tempfile`, `sqlite3`, `gc`, `tracemalloc`, `time.perf_counter`, `timeit` (`globals=globals()` LAZMI).

## sqlite3 (NB3/NB4 ke SQL-vs-pandas verification ke liye) — sab verified
- Window functions **support hain** (`RANK() OVER (PARTITION BY ... ORDER BY ...)`, `ROW_NUMBER`,
  `DENSE_RANK`, `LAG`, `LEAD`, `SUM() OVER`), `WITH` CTE, `FULL OUTER JOIN`, `COALESCE`, `ROUND`,
  `date('2024-01-05','+1 day')`, `strftime`.
- `df.to_sql("t", con, index=False, if_exists="replace")` + `pd.read_sql(sql, con)` sqlite3
  DBAPI connection ke sath theek chalta hai (sqlalchemy ki zaroorat nahi).
- SQL vs pandas match karte waqt: dono taraf `sort_values(...).reset_index(drop=True)` karo aur
  `assert_frame_equal(..., check_dtype=False)` use karo (sqlite int/float/str dtypes thoda alag).

## Timing budget (asli maapa gaya — inse zyada NA karo)
| kaam | waqt |
|---|---|
| 200k rows groupby mean | 0.03s |
| 100k vectorized vs `.map(lambda)` | 0.003s vs 0.094s (~37x) |
| groupby cython `sum` vs `agg(lambda)` (100k, 500 groups) | 0.011s vs 0.100s (~9x) |
| **20k rows `apply(axis=1)`** | **1.56s** → apply demos **<= 20k rows** |
| **5k rows `iterrows`** | **0.98s** → iterrows demos **<= 3k rows** |
| **200k×2 CSV write+read** | **7.0s** → CSV IO demos **<= 60k rows** |
| 100k `.str.upper()` | 0.26s |
| 300-iteration `pd.concat` loop | 0.51s |
- **Timing par assert MAT karo** (`assert fast < slow` NAHI) — sirf print + "aam tor par X tez hai".
- Dataset size cap: **<= 200k cells** per DataFrame.

## Style (spec se, dohra raha hoon)
- Roman Urdu + English mix, senior→junior tone. Har concept: Kya hai → Kyun → Syntax → Example →
  Output ka matlab → Gotchas → Interview tip. Har ahem line par comment.
- `md()`/`code()` ke triple-quoted string ka content **column 0** se; backslash ho to `r"""..."""`.
- Har notebook **60+ cells**. Data hamesha inline (`default_rng(seed)`, `io.StringIO`, `tempfile`, `sqlite3`).
- LeetCode section LAZMI: `### LC <num>. <Exact Title> — <Difficulty>` + link + Roman-Urdu bayan +
  approach + complexity + code with **chalte asserts** (deterministic).
