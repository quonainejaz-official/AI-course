# ENV NOTES — Pandas/Intermediate (pandas 3.0.5 par PROBE kiye hue asli facts, guess nahi)

Python 3.14.0, pandas **3.0.5**, numpy 2.4.2. `AGENT_SPEC.md` ke saath ye bhi LAZMI follow karo.

## Kya NAHI hai (import bhi na karo)
- **pyarrow NAHI** → `dtype="string[pyarrow]"` / `dtype_backend="pyarrow"` **ImportError** deta hai.
  `string[pyarrow]` sirf *concept* ke tor par likho, ya `try/except ImportError` me wrap karo.
- **scipy NAHI** → `rolling(win_type="triang"/"gaussian")` **ImportError**. Sirf zikr karo ya try/except.
- **matplotlib/seaborn NAHI** → koi plotting nahi. `statsmodels` bhi nahi (seasonal_decompose ka sirf zikr).
- Network/`input()`/bahar ki file NAHI. Data inline: dict / `io.StringIO` / `pd.date_range` / `default_rng` / `tempfile`.

## pandas 3.0 ke BADLE hue behaviours (probe-verified)

### String dtype (sab se bara farq)
- Default string dtype ab **`str`** hai: `pd.Series(["a"]).dtype` → `<StringDtype(storage='python', na_value=nan)>`,
  `df.dtypes` me `'str'` dikhta hai (`'object'` NAHI). `pd.get_option("future.infer_string")` → `True`.
- Isliye `assert df["s"].dtype == "object"` jaisi assert **FAIL** karegi. `== "str"` use karo ya dtype assert na karo.
- `memory_usage(deep=True)`: object aur str dono **57132** (1000×8-char), `category` → **1189**.
  Yaani category ka memory demo abhi bhi shandaar chalta hai (~48x) — wahi use karo.
- `s.str.contains("a")` me NaN row → **False** (bool dtype), isliye mask seedha filter me chal jata hai.
  Lekin `s.str.len()` → float64 with `nan`. `.str.split("-", expand=True)` ke columns bhi `str` dtype.
- `astype("object")` still allowed (comparison demo ke liye theek).

### groupby
- `groupby.apply(..., include_groups=True)` → **ValueError: include_groups=True is no longer allowed.**
  Default hi grouping columns ko **exclude** karta hai. `include_groups=False` likhna optional/allowed hai.
- `df.groupby("g").mean()` jab koi `str` column ho → **TypeError: dtype 'str' does not support operation 'mean'**.
  → `numeric_only=True` do ya columns select karo. (Acha gotcha, try/except me dikhao.)
- `df.groupby("g").sum()` **chalta hai** aur text columns ko **jod deta (concat)** hai: `{'s': ['pq','rt']}` — "silent text aggregation" gotcha.
- Categorical groupby me **`observed=True` DEFAULT** hai (unused category nahi aati); `observed=False` do to `z: 0` aata hai.
- NaN group: `dropna=True` default → NaN group drop; `dropna=False` se group banta hai.
  NaN group ki wajah se `ngroup()`/`cumcount()` **float** (`nan`) return karte hain.
- `pct_change()` ab **fill karta nahi** (default `fill_method=None` jaisa): `[1,2,nan,4]` → `[nan,1.0,nan,nan]`.
- `group_keys=True` (default) apply me group key index me add karta hai → `[('a',0),('b',2)]`; `False` → `[0,2]`.
- Verified working: `.groups` (values `RangeIndex`), `.ngroups`, `get_group`, iteration, `agg` list/dict/lambda,
  named agg + `pd.NamedAgg`, `describe()`, `nunique/first/last/prod/std/var/median/quantile/idxmax`,
  `size` vs `count` (NaN), `transform`, `filter(dropna=)`, `head/tail/nth([0,1])`, `nlargest`, `rank`,
  `expanding`, `rolling`, `shift/diff`, `sort=False`, `as_index=False`, `pd.Grouper(key=,freq="ME")`,
  grouping by function / dict / array / `level=`, `reset_index(name=...)`, `size().reset_index(name="n")`.

### merge / concat
- **int vs str key merge ab ERROR hai** (silent empty merge NAHI):
  `ValueError: You are trying to merge on int64 and str columns for key 'k'...`
  → "purane pandas me silently khali aata tha, ab error" aisa likho; try/except me dikhao. int vs float chalta hai.
- **NaN keys merge me match KARTE hain** (same dtype): `{'k':[1.0,nan],...}` → NaN ↔ NaN join ho gaya (SQL se ulta!). Ye zaroor dikhao.
- `validate="one_to_one"` duplicate keys par `MergeError` (message me "Duplicates in left/right").
- `verify_integrity=True` overlapping index par `ValueError: Indexes have overlapping values`.
- Verified: `how=inner/left/right/outer/cross`, `indicator=True` (`{'both':4,'left_only':2,'right_only':1}`),
  `suffixes`, `left_index`+`right_on`, anti-join `.query("_merge=='left_only'")`, `merge_asof(by=, tolerance=, direction=)`,
  `merge_ordered(fill_method="ffill", left_by=)`, `combine_first`, `update` (inplace hi hai), `compare(keep_shape,keep_equal)`,
  `concat(keys=, ignore_index=, join="inner", axis=1)`, `df.join(lsuffix/rsuffix)`, `isin` semi-join.

### reshaping
- `stack(dropna=...)` → **ValueError** ("dropna must be unspecified as the new implementation..."). `dropna` MAT do.
  `future_stack=True` pass karna chalta hai magar likhne ki zaroorat nahi — plain `.stack()` naya behaviour hai.
- `pivot()` ke arguments **keyword-only**: `pivot(index=, columns=, values=)`. Duplicate index+columns → `ValueError: Index contains duplicate entries, cannot reshape`.
- `pd.get_dummies(...)` default dtype **bool** (`dtype=int` do agar 0/1 chahiye). `from_dummies` chalta hai.
- Verified: `melt`, `wide_to_long(sep=)`, `explode`, `unstack(fill_value=)`, `swaplevel().sort_index()`,
  `xs(level=)`, `pd.IndexSlice`, `json_normalize(record_path=, meta=, sep=)`, `crosstab(values=,aggfunc=,margins=,normalize=)`,
  `pivot_table(margins=,fill_value=,dropna=,observed=,aggfunc=[..])` (multi-aggfunc columns `('sum','v')`), `.T`.
- `applymap` **GONE** → `DataFrame.map` use karo.

### time series
- Purani freq strings **ERROR**: `"M"` → "'M' is no longer supported for offsets. Please use 'ME' instead.",
  `"H"` → "Did you mean h?". Sirf naye codes use karo: `D B W ME MS QE QS YE YS h min s ms`.
- `tshift` **GONE** (AttributeError) → `shift(freq=...)` use karo. `Series.first("2D")`/`.last()` bhi **GONE** → `.loc[:...]`/`truncate` use karo.
  (groupby ka `.first()`/`.last()` bilkul zinda hai.)
- `to_datetime(errors="ignore")` **hata diya gaya** (AssertionError deta hai) → sirf `raise`/`coerce`.
- `format="mixed"`, `dayfirst=`, `unit="s"` verified. `2024-03-10 02:30` America/New_York → nonexistent `ValueError`
  (`nonexistent="shift_forward"` se fix), ambiguous ke liye `ambiguous=True`.
- tz-aware − tz-naive → `TypeError`. Non-monotonic DatetimeIndex par partial slicing → `KeyError`  (sort_index zaroori).
- Verified: partial string indexing `s["2024-03"]` / `s["2024-01":"2024-02"]`, `asfreq` vs `resample`,
  `resample(label=,closed=,origin=)`, `.ohlc()`, `agg({"v":["sum","mean"]})`, `ffill/bfill/interpolate`,
  `interpolate(method="time")`, `groupby(...).resample(...)`, `rolling("2D", on="t")`, `rolling(closed="left")`,
  `rolling(min_periods=,center=)`, `rolling.apply(raw=True)`, `expanding`, `ewm(span=/alpha=,adjust=)`,
  `rolling.corr/cov`, `between_time/at_time`, `truncate`, `bdate_range`, `pd.offsets.CustomBusinessDay(holidays=[...])`,
  `pandas.tseries.holiday.USFederalHolidayCalendar` (2024 me 11 holidays), `dt.isocalendar()` cols `['year','week','day']`,
  `dt.day_name()`, `dt.to_period("W")` → `'2024-01-01/2024-01-07'`, `dt.floor/ceil/round/normalize`,
  `period_range + 1`, `to_timestamp(how="end")`, `Timedelta.total_seconds()`,
  session-ization `diff().gt(Timedelta("30min")).cumsum()` → `[0,0,1]`.

### categoricals
- `pd.concat` par **different categories → dtype `str` ban jata hai** (category kho jati hai!) — ye gotcha zaroor dikhao.
  Same categories dono taraf → `CategoricalDtype` bach jata hai. `pd.api.types.union_categoricals` bhi verified.
- Nayi value assign → `TypeError: Cannot setitem on a Categorical with a new category (zzz), set the categories first`.
- Verified: `astype("category")`, `.cat.categories/codes/add_categories/remove_categories/rename_categories/reorder_categories/as_ordered`,
  ordered comparison, `sort_values` category order se, `cut`/`qcut(labels=,duplicates="drop")`, `cut(labels=False)`,
  category merge keys.

### CoW / misc
- Chained assignment `d["a"][0] = 99` → value **badalti NAHI**, `ChainedAssignmentError` **warning** milti hai
  (`pd.errors.ChainedAssignmentError` maujood hai). Demo ke liye `warnings.catch_warnings(record=True)` use karo
  aur print karo ke value unchanged rahi — yehi CoW ka sabaq hai. Sahi tareeqa: `.loc[0, "a"] = 99`.
- Verified: `query` (backtick + `@var`), `eval`, `pipe`, `assign` chaining, `iterrows`, `read_csv(io.StringIO(...))`,
  `read_csv(chunksize=)`, `rank(method="dense")`, `nlargest(keep="all")`, `drop_duplicates(keep=)`,
  `duplicated(subset=,keep=False)`, `sort_values(kind="stable")`, `info(buf=io.StringIO())`, `convert_dtypes()` → `Int64`,
  `pd.testing.assert_frame_equal`, `np.where`, `where/mask`, `clip`, `MultiIndex.from_product`.

## Timing / assert rules
- Timing sirf `time.perf_counter()` se **print** karo; `assert fast < slow` **NAHI** (machine par badalta hai).
- Har notebook total **< ~30 sec**. Data size chhota (200–500 rows) rakho.
- LeetCode asserts deterministic. Float compare me `round()` ya `np.isclose`/`assert_frame_equal(check_dtype=False)`.
- `assert_frame_equal` me pandas 3 ke dtypes (`str`, `Int64`) ka dhyan → `check_dtype=False` safe hai.

## LeetCode — exact number + title + slug (verified list, inhi ko use karo)
| # | Exact Title | Diff | slug |
|---|---|---|---|
| 596 | Classes More Than 5 Students | Easy | classes-more-than-5-students |
| 511 | Game Play Analysis I | Easy | game-play-analysis-i |
| 1050 | Actors and Directors Who Cooperated At Least Three Times | Easy | actors-and-directors-who-cooperated-at-least-three-times |
| 1741 | Find Total Time Spent by Each Employee | Easy | find-total-time-spent-by-each-employee |
| 2668 | Find Latest Salaries | Easy | find-latest-salaries |
| 2887 | Fill Missing Data | Easy | fill-missing-data |
| 2888 | Reshape Data: Concatenate | Easy | reshape-data-concatenate |
| 2889 | Reshape Data: Pivot | Easy | reshape-data-pivot |
| 2890 | Reshape Data: Melt | Easy | reshape-data-melt |
| 2891 | Method Chaining | Easy | method-chaining |
| 570 | Managers with at Least 5 Direct Reports | Medium | managers-with-at-least-5-direct-reports |
| 1378 | Replace Employee ID With The Unique Identifier | Easy | replace-employee-id-with-the-unique-identifier |
| 1607 | Sellers With No Sales | Easy | sellers-with-no-sales |
| 1141 | User Activity for the Past 30 Days I | Easy | user-activity-for-the-past-30-days-i |
| 1084 | Sales Analysis III | Easy | sales-analysis-iii |
| 550 | Game Play Analysis IV | Medium | game-play-analysis-iv |
| 1729 | Find Followers Count | Easy | find-followers-count |
| 197 | Rising Temperature | Easy | rising-temperature |
| 176 | Second Highest Salary | Medium | second-highest-salary |
| 178 | Rank Scores | Medium | rank-scores |
| 180 | Consecutive Numbers | Medium | consecutive-numbers |
| 184 | Department Highest Salary | Medium | department-highest-salary |
| 185 | Department Top Three Salaries | Hard | department-top-three-salaries |

Link format: `https://leetcode.com/problems/<slug>/`
