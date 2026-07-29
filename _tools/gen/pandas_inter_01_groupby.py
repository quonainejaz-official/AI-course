"""Generator: Pandas/Intermediate/01_Grouping_Aggregation_aur_Pivot_Tables.ipynb"""
import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

CELLS = []

CELLS += [
md("""
# 01 — Grouping, Aggregation aur Pivot Tables (Pandas Intermediate)

**Level:** Intermediate | **Requirement:** pandas 3.x, numpy

Ye notebook pandas ka sab se zyada "interview + real job" wala hissa hai: **split-apply-combine**.
Excel me jo kaam Pivot Table karta hai, pandas me wo `groupby` / `pivot_table` / `crosstab` karte hain —
magar 100x zyada powerful aur programmable.

## Is notebook me kya seekhenge

- **Split-Apply-Combine** ka concept (text diagram ke sath)
- `groupby` object asal me kya hota hai (lazy hai, kuch compute nahi karta) — `.groups`, `.ngroups`, `get_group()`, iteration
- **Grouping ke saare tareeqe**: column, multiple columns, Series/array, index level, function, dict/mapping, `pd.Grouper`
- `sort=False` (performance), `dropna=False` (NaN groups), `observed` (categoricals), `as_index=False` vs `reset_index()`
- **Aggregation**: single func, list of funcs, dict per column, lambda, **named aggregation**, custom funcs, `describe()` per group
- Built-in fast aggs: sum/mean/median/min/max/count/size/nunique/first/last/std/var/prod/quantile/idxmax
- **`count` vs `size`** ka farq (NaN wali kahani) — classic interview question
- **`transform`** (same-shape output): group mean fill, z-score, percent of total, rank, cumcount, cumsum, `ngroup`
- **`filter`** (poore group ko rakhna ya hatana), **`apply`** (kab zaroori, kyun slow, `group_keys`)
- Group ke andar window ops: `shift`, `diff`, `pct_change`, `rolling`, `expanding`, `head`/`tail`/`nth`
- **Top-N per group — 3 tareeqe** + timing comparison
- MultiIndex results, `unstack()` se pivot, **`pivot_table`** (margins/fill_value/aggfunc), **`crosstab`** (normalize)
- Business questions: revenue per region per month, AOV, conversion by channel, category share, best product per store, outlier flag
- Common mistakes, **LeetCode problems**, Interview Q&A, Practice exercises, Cheat-sheet

## Prerequisites
Pandas Basics: Series/DataFrame banana, `loc`/`iloc`, boolean filtering, `sort_values`, NaN ka basic idea.
"""),
code("""
# Setup — sirf pandas aur numpy (matplotlib is env me NAHI hai, plotting nahi karenge)
import time                      # timing comparisons ke liye
import numpy as np
import pandas as pd

# Display thora control — taake output readable rahe
pd.set_option("display.width", 110)          # console width
pd.set_option("display.max_columns", 25)     # columns chhupne na paayein

print("pandas:", pd.__version__)   # is notebook ko pandas 3.x par likha gaya hai
print("numpy :", np.__version__)
"""),
md("""
## 1. Split-Apply-Combine — poora concept

Har group-wise analysis 3 steps me hoti hai:

1. **Split** — data ko kisi key (ya keys) ke hisab se tukdon me baant do.
2. **Apply** — har tukde par koi kaam karo (sum, mean, custom function...).
3. **Combine** — natije ko wapas ek DataFrame/Series me jod do.

```text
        RAW DATA                      SPLIT (by region)            APPLY (sum)      COMBINE
 region   amount
 ------   ------                   North: 1200, 800  ---------->    2000
  North    1200                                                                    region  amount
  South    1500      groupby       South: 1500, 600  ---------->    2100   -->      North    2000
  North     800      -------->                                                      South    2100
  South     600                    East : 950        ---------->     950            East      950
  East      950
```

**Yaad rakho:** tumhein sirf "Apply" step likhna hota hai. Split aur Combine pandas khud karta hai.
Interview me agar poochein "groupby kaise kaam karta hai?" — yehi 3 lafz bolo: split, apply, combine.
"""),
code("""
# Hamara main dataset — chhota hai taake har output aankh se verify ho sake.
# Jaan boojh kar 2 "gande" points daale hain:
#   - index 9 par amount = NaN  (count vs size ka farq dikhane ke liye)
#   - index 17 par region = None (NaN group dikhane ke liye)
orders = pd.DataFrame({
    "order_id": range(1, 19),
    "region": ["North", "North", "South", "South", "East", "East", "West", "West",
               "North", "South", "East", "West", "North", "South", "East", "West",
               "North", None],
    "channel": ["Web", "Store", "Web", "Partner", "Web", "Store", "Web", "Partner",
                "Web", "Web", "Partner", "Store", "Store", "Web", "Web", "Web",
                "Partner", "Web"],
    "rep": ["Ali", "Sara", "Ali", "Bilal", "Sara", "Ali", "Bilal", "Sara",
            "Ali", "Sara", "Bilal", "Ali", "Sara", "Bilal", "Ali", "Sara",
            "Bilal", "Ali"],
    "amount": [1200.0, 800.0, 1500.0, 600.0, 950.0, 1100.0, 2000.0, 450.0,
               1300.0, np.nan, 700.0, 1650.0, 500.0, 1900.0, 1250.0, 300.0,
               875.0, 1000.0],
    "units": [3, 2, 5, 1, 2, 4, 6, 1, 3, 2, 2, 5, 1, 7, 3, 1, 2, 2],
    "order_date": pd.to_datetime([
        "2024-01-05", "2024-01-11", "2024-01-19", "2024-01-27",
        "2024-02-02", "2024-02-08", "2024-02-14", "2024-02-20",
        "2024-02-26", "2024-03-03", "2024-03-07", "2024-03-12",
        "2024-03-15", "2024-03-19", "2024-03-22", "2024-03-25",
        "2024-03-28", "2024-03-30"]),
})

print(orders.head(6))
print("\\nshape:", orders.shape)
print("\\ndtypes:\\n", orders.dtypes)   # NOTE: pandas 3 me text columns ka dtype 'str' hai, 'object' nahi
"""),
md("""
## 2. `groupby` object — ye LAZY hota hai

**Kya hai:** `df.groupby("col")` ek `DataFrameGroupBy` object deta hai — ye **abhi kuch compute nahi karta**.
Ye sirf plan banata hai ("kaun row kis group me jayegi"). Compute tab hota hai jab tum aggregation maangte ho.

**Kyun important:** interview me poocha jata hai "groupby turant kaam karta hai?" — jawab: **nahi, lazy hai**.
Isi wajah se `df.groupby("a")` print karne par tumhein data nahi, object ka repr milta hai.
""" ),
code("""
g = orders.groupby("region")     # sirf plan bana — koi calculation nahi hui

print("type:", type(g))                  # DataFrameGroupBy
print("ngroups:", g.ngroups)             # kitne groups bane (NaN group by default count nahi hota)
print("\\n.groups (dict: key -> row labels):")
for key, idx in g.groups.items():        # .groups ek mapping hai: group key -> index labels
    print(f"  {key!r:>8} -> {list(idx)}")

# NOTE: region me ek None tha (index 17) — wo group me NAHI aaya, kyunki dropna=True default hai
print("\\nkul rows:", len(orders), "| groups me rows:", sum(len(i) for i in g.groups.values()))
"""),
code("""
# get_group() — ek group ka poora DataFrame nikalo
south = g.get_group("South")
print("South group:\\n", south[["order_id", "region", "amount"]])

# Iteration — (key, sub_dataframe) tuples milte hain. Debugging ke liye behtareen.
print("\\n--- iteration ---")
for key, sub in g:
    print(f"{key:>6}: rows={len(sub):>2}, amount_sum={sub['amount'].sum():>8.1f}")

# Gotcha: multiple columns par group karo to key ek TUPLE hoti hai
for key, sub in orders.groupby(["region", "channel"]):
    print("tuple key example:", key, "-> rows:", len(sub))
    break   # sirf pehla dikhaya
"""),
md("""
## 3. Grouping ke tareeqe (7 tareeqe)

`groupby()` ko tum ye sab de sakte ho:

| Tareeqa | Syntax | Kab use karein |
|---|---|---|
| Single column | `df.groupby("region")` | sab se aam |
| Multiple columns | `df.groupby(["region","channel"])` | 2-level breakdown → MultiIndex result |
| Series / array | `df.groupby(arr)` | key data ke bahar se aa rahi ho |
| Index level | `df.groupby(level="region")` | key index me ho |
| Function | `df.groupby(len)` | index par calculation se key bane |
| dict / mapping | `df.groupby({"a":"X"})` | manual bucketing (region → zone) |
| `pd.Grouper` | `pd.Grouper(key="order_date", freq="ME")` | time-based grouping (monthly, weekly) |
"""),
code("""
# (a) Single column
print("(a) single column:\\n", orders.groupby("region")["amount"].sum(), sep="")

# (b) Multiple columns -> MultiIndex (region, channel)
multi = orders.groupby(["region", "channel"])["amount"].sum()
print("\\n(b) multiple columns (pehli 6 rows):\\n", multi.head(6), sep="")
print("index nlevels:", multi.index.nlevels)   # 2 levels

# (c) Series/array se grouping — data ke bahar ki key
# Yahan ek derived key bana rahe hain: amount 1000 se bara ya chhota
size_key = np.where(orders["amount"] >= 1000, "big", "small")   # numpy array
print("\\n(c) array se grouping:\\n", orders.groupby(size_key)["order_id"].count(), sep="")
"""),
code("""
# (d) Index level par grouping — pehle region ko index banate hain
by_idx = orders.set_index("region")
print("(d) level ke naam se:\\n", by_idx.groupby(level="region")["amount"].sum(), sep="")

# (e) Function se grouping — function ko INDEX ki har value milti hai
# Yahan region ke pehle harf par group kar rahe hain (N, S, E, W)
# Pehle region ki NaN row hata di, warna function ko None milega aur None[0] crash karega
by_idx2 = orders.dropna(subset=["region"]).set_index("region")
print("\\n(e) function (pehla harf):\\n",
      by_idx2.groupby(lambda label: label[0])["amount"].sum(), sep="")

# (f) dict / mapping — business bucketing (region -> zone)
zone_map = {"North": "Upper", "South": "Lower", "East": "Upper", "West": "Lower"}
print("\\n(f) dict mapping (zone):\\n",
      by_idx2.groupby(zone_map)["amount"].sum(), sep="")
"""),
code("""
# (g) pd.Grouper — time based grouping. freq="ME" = Month End.
# pandas 3 me freq codes: D B W ME MS QE QS YE YS h min s  (purana "M"/"H" ERROR deta hai!)
monthly = orders.groupby(pd.Grouper(key="order_date", freq="ME"))["amount"].sum()
print("(g) monthly (ME = month end labels):\\n", monthly, sep="")

# Purane freq codes ab error dete hain — ye pandas 3 ka bara change hai
try:
    orders.groupby(pd.Grouper(key="order_date", freq="M"))["amount"].sum()
except Exception as e:
    print("\\n'M' ka natija ->", type(e).__name__, ":", str(e)[:90])
"""),
]
CELLS += [
md("""
## 4. Zaroori groupby flags: `sort`, `dropna`, `observed`, `as_index`

Ye 4 flags 90% "arey ye output aisa kyun hai?" wale sawalon ka jawab hain.

- **`sort=True`** (default) — group keys sorted order me aati hain. `sort=False` **tez** hota hai (bare data par farq dikhta hai)
  aur groups **first-appearance** order me aate hain.
- **`dropna=True`** (default) — key me NaN wali rows **poori tarah gayab** ho jati hain. `dropna=False` unka apna NaN group banata hai.
  **Ye silent data loss ka sab se aam sabab hai.**
- **`observed=True`** (pandas 3 me default) — Categorical keys par sirf **mojood** categories aati hain. `observed=False` un-used
  categories ko bhi zero ke sath dikhata hai.
- **`as_index=True`** (default) — group keys result ka **index** bante hain. `as_index=False` unhein normal columns rakhta hai
  (yani flat table — merge/plot ke liye behtar).
"""),
code("""
# sort=True vs sort=False — order ka farq
print("sort=True  (default, alphabetical):")
print(orders.groupby("region", sort=True)["amount"].sum())

print("\\nsort=False (first appearance order — North, South, East, West):")
print(orders.groupby("region", sort=False)["amount"].sum())
"""),
code("""
# dropna — SILENT DATA LOSS ka demo. index 17 ki region None thi.
d_true = orders.groupby("region", dropna=True)["amount"].sum()
d_false = orders.groupby("region", dropna=False)["amount"].sum()

print("dropna=True  -> groups:", d_true.shape[0], "| kul amount:", d_true.sum())
print("dropna=False -> groups:", d_false.shape[0], "| kul amount:", d_false.sum())
print("\\ndropna=False ka natija (dekho aakhir me NaN group):")
print(d_false)

# Verify: 1000.0 wali row (order_id 18) dropna=True me GAYAB hai
print("\\ngayab hua amount:", d_false.sum() - d_true.sum(), "<- ye order_id 18 hai")
"""),
code("""
# observed — Categorical ke sath. Ek category ('Central') jaan boojh kar khali rakhi hai.
cat_regions = pd.Categorical(
    orders["region"],
    categories=["North", "South", "East", "West", "Central"],   # Central kisi row me nahi
)
tmp = orders.assign(region_cat=cat_regions)

obs_true = tmp.groupby("region_cat", observed=True)["amount"].sum()
obs_false = tmp.groupby("region_cat", observed=False)["amount"].sum()

print("observed=True (pandas 3 default) — sirf mojood categories:\\n", obs_true, sep="")
print("\\nobserved=False — un-used 'Central' bhi 0.0 ke sath aa gaya:\\n", obs_false, sep="")
"""),
code("""
# as_index=False -> flat table (keys column rehte hain). Ye merge ke liye ideal hai.
nested = orders.groupby(["region", "channel"])["amount"].sum()
flat = orders.groupby(["region", "channel"], as_index=False)["amount"].sum()

print("as_index=True  -> Series with MultiIndex, nlevels =", nested.index.nlevels)
print("as_index=False -> DataFrame, columns =", list(flat.columns))
print("\\nflat table (pehli 5):\\n", flat.head(5), sep="")

# Wahi kaam reset_index() se bhi hota hai — dono barabar hain
same = nested.reset_index()
print("\\nreset_index() ka natija barabar hai?", flat.equals(same))
"""),
md("""
## 5. Aggregation — single, list, dict, named

Aggregation = har group ko **ek value** me sikorna.

Char shakal:

1. **Single** — `g["amount"].sum()`
2. **List** — `g["amount"].agg(["sum", "mean"])` → har func ka apna column
3. **Dict** — `g.agg({"amount": "sum", "units": "mean"})` → har column ka apna func
4. **Named aggregation** (BEST) — `g.agg(total=("amount", "sum"), n=("order_id", "count"))`
   → saaf column names, koi MultiIndex column nahi. **Production me yehi use karo.**
"""),
code("""
g = orders.groupby("region")

# 1) Single aggregation -> Series
print("1) single:\\n", g["amount"].sum(), sep="")

# 2) List of functions -> DataFrame (columns = func names)
print("\\n2) list of funcs:\\n", g["amount"].agg(["sum", "mean", "count", "max"]), sep="")
"""),
code("""
# 3) Dict — har column ka alag func
print("3) dict per column:")
print(g.agg({"amount": "sum", "units": "mean", "order_id": "count"}))

# Dict + list -> MultiIndex columns ban jate hain (jo phir dukh deta hai)
multi_cols = g.agg({"amount": ["sum", "mean"], "units": "max"})
print("\\ndict + list -> MultiIndex columns:")
print(multi_cols)
print("\\ncolumns:", multi_cols.columns.tolist())    # tuples! ('amount','sum') ...
"""),
code("""
# 4) NAMED AGGREGATION — saaf, flat, production-ready. Format: naya_naam=(column, func)
summary = orders.groupby("region").agg(
    total_revenue=("amount", "sum"),
    avg_order=("amount", "mean"),
    n_orders=("order_id", "count"),
    total_units=("units", "sum"),
    unique_reps=("rep", "nunique"),
    biggest=("amount", "max"),
)
print(summary)
print("\\ncolumns flat hain:", summary.columns.tolist())

# AOV (Average Order Value) — business metric, derived column
summary["aov"] = (summary["total_revenue"] / summary["n_orders"]).round(2)
print("\\nAOV ke sath:\\n", summary[["total_revenue", "n_orders", "aov"]], sep="")
"""),
code("""
# Custom functions — lambda ya named func, dono chalte hain
def spread(s):
    \"\"\"Max - min: group ke andar amount ka phailaav.\"\"\"
    return s.max() - s.min()

res = orders.groupby("region")["amount"].agg([
    "mean",
    spread,                                  # named function -> column name = 'spread'
    ("range_pct", lambda s: (s.max() - s.min()) / s.max() * 100),   # (naam, func) tuple
])
print(res.round(2))

# Named aggregation ke sath custom func
print("\\nnamed + custom:")
print(orders.groupby("region").agg(
    spread=("amount", spread),
    p90=("amount", lambda s: s.quantile(0.90)),
).round(2))
"""),
]
CELLS += [
md("""
## 6. `count` vs `size` — classic interview question

- **`size()`** = group me **rows** kitni hain (NaN bhi ginta hai). Hamesha ek Series deta hai.
- **`count()`** = group me **non-NaN values** kitni hain (per column).

Yani: `size() - count() = us column me NaN ki tadaad`.

Hamare data me `amount` ki index 9 (South) par NaN hai — isi liye South ka count 1 kam hoga.
"""),
code("""
g = orders.groupby("region")

cmp = pd.DataFrame({
    "size": g.size(),                    # saari rows
    "count_amount": g["amount"].count(),  # sirf non-NaN amount
    "count_units": g["units"].count(),    # units me koi NaN nahi
})
cmp["missing_amount"] = cmp["size"] - cmp["count_amount"]
print(cmp)

print("\\nSouth me amount ka ek NaN hai -> size=4 magar count=3")
print("\\ng.count() poore DataFrame par (har column ka apna count):")
print(g.count())
"""),
md("""
## 7. Built-in aggregations ki poori list

Ye sab **C/Cython me likhe hue** hain — `apply(lambda ...)` se **kai guna tez**. Jab bhi mumkin ho yehi use karo.

| Function | Kaam |
|---|---|
| `sum` `mean` `median` `min` `max` `prod` | numeric summary |
| `count` `size` `nunique` | ginti |
| `std` `var` `sem` | phailaav (spread) |
| `first` `last` `nth(n)` | position se value |
| `idxmax` `idxmin` | max/min value ka **index label** |
| `quantile(q)` | percentile |
| `any` `all` | boolean |
| `cumsum` `cumcount` `cumprod` `cummax` | running (same-shape) |
"""),
code("""
g = orders.groupby("region")

builtins_demo = pd.DataFrame({
    "sum": g["amount"].sum(),
    "mean": g["amount"].mean().round(1),
    "median": g["amount"].median(),
    "std": g["amount"].std().round(1),
    "min": g["amount"].min(),
    "max": g["amount"].max(),
    "nunique_rep": g["rep"].nunique(),
    "q75": g["amount"].quantile(0.75),
})
print(builtins_demo)
"""),
code("""
# idxmax — sab se bara order kis row par hai? (label deta hai, value nahi)
idx_of_max = orders.groupby("region")["amount"].idxmax()
print("har region me max amount ka index label:\\n", idx_of_max, sep="")

# Us label se poori row nikalo -> "best order per region"
print("\\nun rows ki tafseel:")
print(orders.loc[idx_of_max, ["region", "rep", "channel", "amount"]])

# first / last / nth
print("\\nfirst amount per region:\\n", orders.groupby("region")["amount"].first(), sep="")
print("\\nnth(1) = doosri row per region:\\n", orders.groupby("region")["amount"].nth(1), sep="")
"""),
code("""
# describe() per group — quick EDA. Output me MultiIndex columns aate hain.
desc = orders.groupby("region")["amount"].describe()
print(desc.round(1))

# Sirf kuch stats chahiye to normal column selection kaam karta hai
print("\\nsirf count/mean/max:\\n", desc[["count", "mean", "max"]].round(1), sep="")
"""),
md("""
## 8. `transform` — same shape wapas (SUPER important)

Farq samajh lo:

| Method | Output ka size | Use case |
|---|---|---|
| `agg` | **ek row per group** (chhota) | summary table |
| `transform` | **original ke barabar** (same shape) | naya column banana |
| `filter` | rows ka subset | poore group rakhna/hatana |
| `apply` | kuch bhi | jab baqi kuch kaam na kare |

`transform` group ki value ko **wapas har row par broadcast** kar deta hai. Isi liye ye
"group mean se fill karo", "z-score nikalo", "percent of total" jaise kaam ke liye perfect hai.

```text
 agg:                          transform:
  region  amount               region  amount  region_mean
  North     2000  (1 row)       North    1200      1093.75   <- same rows
  South     2100                North     800      1093.75
                                South    1500      1333.33
```
"""),
code("""
# transform ka bunyadi demo — group mean ko har row par lagao
orders_t = orders.copy()
orders_t["region_mean"] = orders_t.groupby("region")["amount"].transform("mean")

print(orders_t[["region", "amount", "region_mean"]].head(8).round(1))
print("\\nshape wahi hai?", orders_t.shape[0] == orders.shape[0])

# NOTE: jis row ki region NaN thi, uska region_mean bhi NaN hoga
print("\\nregion NaN wali row:\\n", orders_t.loc[[17], ["region", "amount", "region_mean"]], sep="")
"""),
code("""
# USE CASE 1 — missing value ko GROUP ke mean se fill karna (poore column ke mean se behtar)
filled = orders.copy()
grp_mean = filled.groupby("region")["amount"].transform("mean")
filled["amount_filled"] = filled["amount"].fillna(grp_mean)

# South ka NaN (index 9) ab South ke mean se bhar gaya
print(filled.loc[[8, 9, 10], ["region", "amount", "amount_filled"]].round(1))
print("\\nglobal mean hota to:", round(orders['amount'].mean(), 1),
      "| South ka mean:", round(orders[orders.region == 'South']['amount'].mean(), 1))
print("-> group-wise fill zyada honest hai")
"""),
code("""
# USE CASE 2 — group ke andar z-score (outlier detection)
z = orders.copy()
gb = z.groupby("region")["amount"]
z["z_score"] = ((z["amount"] - gb.transform("mean")) / gb.transform("std")).round(2)

# USE CASE 3 — percent of group total (share)
z["pct_of_region"] = (z["amount"] / gb.transform("sum") * 100).round(1)

print(z[["region", "amount", "z_score", "pct_of_region"]].head(10))

# Har region ka pct_of_region 100 tak jama hona chahiye — verify
print("\\nverify (har region ~100%):")
print(z.groupby("region")["pct_of_region"].sum())
"""),
code("""
# USE CASE 4 — rank, cumcount, cumsum, ngroup (group ke andar)
r = orders.sort_values(["region", "order_date"]).copy()

r["rank_in_region"] = r.groupby("region")["amount"].rank(ascending=False, method="dense")
r["order_seq"] = r.groupby("region").cumcount() + 1          # 0-based -> 1-based
r["running_total"] = r.groupby("region")["amount"].cumsum()
r["group_id"] = r.groupby("region").ngroup()                 # har group ko number

print(r[["region", "order_date", "amount", "rank_in_region",
         "order_seq", "running_total", "group_id"]].head(9))
"""),
]
# <<APPEND>>

save(r"Pandas/Intermediate/01_Grouping_Aggregation_aur_Pivot_Tables.ipynb", CELLS)
