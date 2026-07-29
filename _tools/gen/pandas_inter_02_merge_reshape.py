"""Generator: Pandas/Intermediate/02_Merging_Joining_Concat_aur_Reshaping.ipynb"""
import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

CELLS = []
def M(s): CELLS.append(md(s))
def C(s): CELLS.append(code(s))

# ----------------------------------------------------------------- title
M(r"""
# Pandas Intermediate 02 — Merging, Joining, Concat aur Reshaping

**Level:** Intermediate
**Prerequisites:** Pandas Basics (Series/DataFrame banana, indexing, `groupby` ka basic idea)

Real duniya me data kabhi ek clean table me nahi milta — customers alag table me,
orders alag me, aur report ke liye kabhi wide format chahiye kabhi long. Ye notebook
do super-powers sikhata hai: **combining** (concat/merge/join) aur **reshaping**
(melt/pivot/stack).

## Is notebook me kya seekhenge
- `pd.concat` — axis=0/1, `keys=`, `ignore_index`, mismatched columns
- `pd.merge` mastery — `how=inner/left/right/outer/cross`, `on`, `left_on/right_on`,
  index-based merge, `suffixes`, `indicator=True`, `validate=`
- **Duplicate-key cardinality** — one-to-many aur many-to-many blow-up, detect kaise karein
- Key dtype mismatch aur NaN keys ke gotchas
- `df.join` vs `df.merge` — kab konsa use karein
- Reshaping: `melt`, `pivot`, `pivot_table`, `stack`/`unstack`, `wide_to_long`, `explode`
- **Anti-join pattern** (kis customer ne order nahi kiya jaisi queries)
- Gotchas, real-world problems, LeetCode problems, interview Q&A, practice exercises

> **Padhne ka tareeqa:** har code cell chala kar output dekho, phir agla parho.
""")

C(r"""
# Setup — ye cell sab se pehle chalao
import pandas as pd
import numpy as np
import io

print("pandas version:", pd.__version__)
pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)
print("setup done")
""")

# ----------------------------------------------------------------- concat
M(r"""
## 1. `pd.concat` — DataFrames ko "chipkana" (stack karna)

### Kya hai
`pd.concat([df1, df2, ...])` — kai DataFrames/Series ko ek sath jorta hai, **bina kisi
key column ke** (merge ke ulat — merge keys match karta hai, concat sirf "saath rakh deta hai").

### Kyun / kahan use hota hai
- Monthly files ko ek sath jama karna (Jan.csv + Feb.csv + Mar.csv)
- Model predictions ko batches se combine karna
- Do tables ko side-by-side (columns) jorna jab index already aligned ho

### Syntax
```python
pd.concat(objs, axis=0, join="outer", keys=None, ignore_index=False, verify_integrity=False)
```
""")

C(r"""
# axis=0 (default) -> rows ke neeche rows jorta hai (jaise do CSVs ko stack karna)
jan_sales = pd.DataFrame({"city": ["Lahore", "Karachi"], "amount": [1000, 1500]})
feb_sales = pd.DataFrame({"city": ["Lahore", "Karachi"], "amount": [1100, 1400]})

combined = pd.concat([jan_sales, feb_sales])   # index repeat ho jata hai (0,1,0,1)
print(combined)
print("\nindex dekho — 0,1,0,1 repeat hua, ye gotcha hai (aage ignore_index se theek karenge)")
assert len(combined) == 4
""")

C(r"""
# axis=1 -> columns ke saath columns jorta hai (index alignment se)
q1 = pd.DataFrame({"revenue": [1000, 1500]}, index=["Lahore", "Karachi"])
q2 = pd.DataFrame({"cost": [700, 900]}, index=["Lahore", "Karachi"])

side_by_side = pd.concat([q1, q2], axis=1)   # index match hua isliye clean jura
print(side_by_side)

# Agar index match na ho to NaN aata hai — join="outer" (default) sab index rakhta hai
q3 = pd.DataFrame({"tax": [50]}, index=["Lahore"])   # Karachi missing
print("\njoin='outer' (default) — Karachi ke liye tax NaN:")
print(pd.concat([q1, q3], axis=1))

print("\njoin='inner' — sirf common index (Lahore) bachta hai:")
print(pd.concat([q1, q3], axis=1, join="inner"))
""")

C(r"""
# keys= -> hierarchical (MultiIndex) row index banata hai, batch ka pata rehta hai
tagged = pd.concat([jan_sales, feb_sales], keys=["Jan", "Feb"])
print(tagged)
print("\nab har row ka pata hai ke wo kis month se aayi — MultiIndex se access:")
print(tagged.loc["Feb"])

# ignore_index=True -> naya fresh 0..n-1 index, keys ke sath NAHI chalta (dono sath dena error deta hai)
fresh = pd.concat([jan_sales, feb_sales], ignore_index=True)
print("\nignore_index=True se fresh index:")
print(fresh)
""")

M(r"""
### `verify_integrity=True` — overlapping index pakadna

Kabhi kabhi hum galti se same index wale 2 DataFrames concat kar dete hain aur pata
nahi chalta ke row-labels duplicate ho gaye. `verify_integrity=True` isko turant pakar leta hai.

### Common mistake
Mismatched columns (ek df me column A extra hai) -> concat chalta hai magar missing
jagah **NaN** aa jaati hai. Ye error nahi, silent hai — dhyan rakho.
""")

C(r"""
# verify_integrity=True -> overlapping index par ValueError
left_batch = pd.DataFrame({"v": [1, 2]})     # index 0,1
right_batch = pd.DataFrame({"v": [3, 4]})    # index 0,1 (overlap!)

try:
    pd.concat([left_batch, right_batch], verify_integrity=True)
except ValueError as e:
    print("[expected error] verify_integrity=True ->", e)

# Sahi tareeqa: ignore_index ya verify_integrity=False (default)
ok = pd.concat([left_batch, right_batch], ignore_index=True)
print("\nignore_index se theek:\n", ok)
""")

C(r"""
# Mismatched columns -> jo column missing hai wahan NaN aa jata hai (silent, error nahi)
df_a = pd.DataFrame({"name": ["Ali", "Sara"], "city": ["Lahore", "Karachi"]})
df_b = pd.DataFrame({"name": ["Bilal"], "age": [25]})   # 'city' nahi, 'age' extra hai

mixed = pd.concat([df_a, df_b], ignore_index=True)
print(mixed)
print("\ndtypes:\n", mixed.dtypes)
print("\nGotcha: 'city' aur 'age' dono me NaN aaya jahan wo column original df me nahi tha.")
""")

# ----------------------------------------------------------------- merge intro
M(r"""
## 2. `pd.merge` — SQL jaisa JOIN, key columns ke zariye

### Kya hai
`merge` do tables ko ek ya zyada **common key columns** ke zariye jorta hai — bilkul
SQL ka `JOIN`. `concat` sirf "saath rakhta" hai, `merge` **match** kar ke jorta hai.

### Kyun / kahan use hota hai
- `customers` + `orders` (customer_id se) — kis customer ne kya order kiya
- `orders` + `products` (product_id se) — order me product ka naam/price laana
- Do reports ko common key (date, id) se merge karna

### Syntax
```python
pd.merge(left, right, how="inner", on=None, left_on=None, right_on=None,
         left_index=False, right_index=False, suffixes=("_x", "_y"),
         indicator=False, validate=None)
```
""")

M(r"""
### `how=` — sab se ahem parameter (Venn-diagram soch ke sath)

Poori notebook me hum ek hi running example use karenge:

```
customers: cust_id 1,2,3,4     (4 ka koi order nahi)
orders   : cust_id 1,2,2,5     (5 kisi customer ka nahi — orphan order)
```

```
INNER  (sirf jo dono me match ho)
   customers  ∩  orders   ->  sirf 1, 2(x2)               = 3 rows

LEFT   (saare customers + jo match mila)
   customers  (sab)  +  match wale orders                 = 5 rows (3,4 NaN ke sath)

RIGHT  (saare orders + jo match mila)
   orders (sab)  +  match wala customer                   = 4 rows (5 NaN ke sath)

OUTER  (dono taraf ka sab kuch, match ho ya na ho)
   customers ∪ orders (union)                              = 6 rows

CROSS  (har left row x har right row — Cartesian product)
   len(left) * len(right)
```

**Row-count intuition:** `inner <= min(left,right ka overlap)`, `left >= len(left)`,
`right >= len(right)`, `outer >= max(left,right)`, `cross == len(left)*len(right)`.
""")

C(r"""
# Running example — poore merge section me yehi use hoga
customers = pd.DataFrame({
    "cust_id": [1, 2, 3, 4],
    "name":    ["Ali", "Sara", "Bilal", "Hina"],
})
orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104],
    "cust_id":  [1, 2, 2, 5],          # 5 = orphan order, kisi customer ka nahi
    "amount":   [500, 300, 700, 200],
})
print("customers:\n", customers)
print("\norders:\n", orders)
""")

C(r"""
# how='inner' -> sirf match wale rows (cust_id 1, 2, 2)
inner = pd.merge(customers, orders, on="cust_id", how="inner")
print("INNER:\n", inner)
assert len(inner) == 3

# how='left' -> saare customers, unmatched (3,4) ke liye order columns NaN
left = pd.merge(customers, orders, on="cust_id", how="left")
print("\nLEFT:\n", left)
assert len(left) == 5

# how='right' -> saare orders, unmatched (order 104, cust_id 5) ke liye customer NaN
right = pd.merge(customers, orders, on="cust_id", how="right")
print("\nRIGHT:\n", right)
assert len(right) == 4

# how='outer' -> sab kuch, match ho ya na ho
outer = pd.merge(customers, orders, on="cust_id", how="outer")
print("\nOUTER:\n", outer)
assert len(outer) == 6
""")

C(r"""
# how='cross' -> Cartesian product, koi key nahi chahiye (on= bhi nahi dena)
colors = pd.DataFrame({"color": ["Red", "Blue"]})
sizes = pd.DataFrame({"size": ["S", "M", "L"]})
combo = pd.merge(colors, sizes, how="cross")
print(combo)
print("\nrows =", len(combo), "= len(colors)*len(sizes) =", len(colors) * len(sizes))
assert len(combo) == len(colors) * len(sizes)
""")

M(r"""
## 3. `on` / `left_on` + `right_on` / index-based keys / `suffixes`

### Kya hai
- `on="col"` — dono tables me **same naam** ka key column.
- `left_on=` + `right_on=` — jab dono tables me key column ka **naam alag** ho.
- `left_index=True` / `right_index=True` — jab key **row-index** me ho, column me nahi.
- `suffixes=(a, b)` — dono tables me overlapping (non-key) column names ho to unko
  alag naam dene ke liye (default `('_x', '_y')`).

### Common mistake
`left_on`/`right_on` use karte waqt dono key columns result me **rehte hain** (alag
naam ke sath) — `on=` use karo to sirf ek column bachta hai. Confusion yahi se hoti hai.
""")

C(r"""
# left_on / right_on -> jab key column ka naam alag ho
orders_alt = orders.rename(columns={"cust_id": "customer_id"})   # naam badal diya
merged = pd.merge(customers, orders_alt, left_on="cust_id", right_on="customer_id", how="inner")
print(merged)
print("\nDekho: 'cust_id' aur 'customer_id' DONO columns bache — on= use karte to sirf ek bachta.")
""")

C(r"""
# index-based merge: left_index=True / right_index=True
customers_idx = customers.set_index("cust_id")     # ab cust_id INDEX hai, column nahi
merged_idx = pd.merge(customers_idx, orders, left_index=True, right_on="cust_id", how="inner")
print(merged_idx)
print("\nleft_index=True + right_on= -> ek taraf index, doosri taraf column se match")
""")

C(r"""
# suffixes -> overlapping column names (yahan dono me 'name' hai)
staff = pd.DataFrame({"cust_id": [1, 2], "name": ["Rep-A", "Rep-B"]})   # sales rep ka naam
clash = pd.merge(customers, staff, on="cust_id", suffixes=("_customer", "_rep"))
print(clash)
print("\ncolumns:", list(clash.columns), "-> 'name' clash suffixes se resolve hua")
""")

M(r"""
## 4. `indicator=True` — merge quality check ka sab se aasan tareeqa

### Kya hai
`indicator=True` ek extra column `_merge` bana deta hai jo batata hai har row
`both` (dono me mili), `left_only`, ya `right_only` se aayi.

### Kyun use hota hai
Merge ke baad data-quality check: "kitne customers ke koi orders nahi?",
"kitne orders orphan hain (customer hi nahi milta)?" — ye turant answer deta hai.
""")

C(r"""
checked = pd.merge(customers, orders, on="cust_id", how="outer", indicator=True)
print(checked)
print("\n_merge value_counts:")
print(checked["_merge"].value_counts())

# Data-quality read: kitne customers bina order ke, kitne orders orphan
print("\ncustomers bina order (left_only):", (checked["_merge"] == "left_only").sum())
print("orphan orders (right_only):", (checked["_merge"] == "right_only").sum())
assert checked["_merge"].value_counts().to_dict() == {"both": 3, "left_only": 2, "right_only": 1}
""")

M(r"""
## 5. `validate=` — merge se PEHLE assumption confirm karo

### Kya hai
`validate="one_to_one" | "one_to_many" | "many_to_one" | "many_to_many"` — merge
karne se pehle keys ki uniqueness check karta hai. Ghalat assumption hone par
`MergeError` fori (turant) uthata hai — silent data bugs se bachata hai.

### Interview tip
Production pipelines me `validate=` lagana **best practice** hai — bina iske ek
duplicate key silently row count double/triple kar sakta hai aur kisi ko pata bhi
nahi chalega jab tak downstream numbers ghalat na aayen.
""")

C(r"""
from pandas.errors import MergeError

# customers me cust_id UNIQUE hai, orders me NAHI (cust_id=2 do baar) -> one_to_one FAIL hoga
try:
    pd.merge(customers, orders, on="cust_id", validate="one_to_one")
except MergeError as e:
    print("[expected error] validate='one_to_one' ->", e)

# Sahi validate: customers taraf unique (one), orders taraf duplicate (many) -> one_to_many chalega
ok = pd.merge(customers, orders, on="cust_id", validate="one_to_many", how="inner")
print("\nvalidate='one_to_many' pass ho gaya, rows:", len(ok))
""")

M(r"""
## 6. Duplicate-key cardinality — **many-to-many blow-up trap**

### Kya hai
Agar **dono** tables me key duplicate ho, to merge har combination bana deta hai —
row count **guna** ho jata hai (multiplication, addition nahi). Ye sab se khatarnak
merge bug hai kyunki koi error nahi aata, sirf numbers ghalat ho jate hain.

### Formula
Ek key `k` ke liye: agar left me `k` `n` baar hai aur right me `k` `m` baar hai,
to result me `k` **`n * m`** baar aayega.

### Kaise detect karein PEHLE (merge se pehle hi)
1. `df["key"].duplicated().any()` — kya key unique nahi hai
2. `df["key"].value_counts()` — kitni baar repeat hui
3. `validate=` parameter (upar dekha) — automatic guard
4. Expected len vs actual len compare: `expected = (left_counts * right_counts).sum()`
""")

C(r"""
# Line-items (order ke andar multiple items) aur discount-codes (bug: order_id repeat)
line_items = pd.DataFrame({
    "order_id": [1, 1, 2, 2, 3],
    "item":     ["Pen", "Book", "Bag", "Shoes", "Watch"],
})
discounts = pd.DataFrame({
    "order_id": [1, 1, 2, 3, 3],           # yahan bhi duplicate — real bug scenario
    "code":     ["X10", "X20", "Y5", "Z1", "Z2"],
})

exploded = pd.merge(line_items, discounts, on="order_id", how="inner")
print("line_items rows:", len(line_items), " discounts rows:", len(discounts))
print("merged rows:", len(exploded), "<- explosion! expected ~5 socha tha")
print(exploded)

# Detect BEFORE merging: duplicated() aur value_counts()
print("\nline_items order_id duplicated?", line_items["order_id"].duplicated().any())
print("discounts order_id duplicated?", discounts["order_id"].duplicated().any())

# Expected row count formula se pehle hi andaza laga sakte the
li_counts = line_items["order_id"].value_counts()
dc_counts = discounts["order_id"].value_counts()
expected = (li_counts * dc_counts).dropna().sum()
print("\nformula se expected rows:", int(expected), " actual rows:", len(exploded))
assert int(expected) == len(exploded) == 8
""")

M(r"""
## 7. Key dtype mismatch — pandas 3 me ab **error**, purane pandas me silent bug tha

### Kya hai
Agar merge key ek table me `int64` hai aur doosri me `str`, to **purane pandas** me
silently khali (empty) result aa jata tha — koi warning nahi, bas 0 matches milte
the aur bandey ko pata bhi nahi chalta tha kuch ghalat hai. **pandas 3.0 me ab
seedha `ValueError` aata hai** — bug jaldi pakra jata hai.

### Fix
Merge se pehle dono taraf `astype(str)` (ya dono `int`) kar ke dtype match karo.
""")

C(r"""
customers_int = customers.copy()                        # cust_id int64 hai
orders_str = orders.copy()
orders_str["cust_id"] = orders_str["cust_id"].astype(str)  # cust_id ko str bana diya (bug simulate)

try:
    pd.merge(customers_int, orders_str, on="cust_id")
except ValueError as e:
    print("[expected error] dtype mismatch ->", e)
    print("(purane pandas me ye silently KHALI result deta tha — ab error hai, behtar!)")

# Fix: dtype match karo (dono ko str, ya dono ko int)
fixed = pd.merge(customers_int, orders_str.assign(cust_id=orders_str["cust_id"].astype(int)), on="cust_id")
print("\nfix ke baad rows:", len(fixed))

# int vs FLOAT chalta hai (koi error nahi) — sirf int vs str error deta hai
orders_float = orders.copy()
orders_float["cust_id"] = orders_float["cust_id"].astype(float)
ok_float = pd.merge(customers_int, orders_float, on="cust_id")
print("int vs float merge chalta hai, rows:", len(ok_float))
""")

M(r"""
## 8. NaN keys — SQL se ULTA behaviour (zaroor yaad rakho)

### Kya hai
SQL me `NULL = NULL` **kabhi True nahi** hota — is liye SQL joins me NULL keys kabhi
match nahi hotay. **Pandas merge me ULTA hai**: agar dono taraf key `NaN` ho (same
dtype ke sath), to wo **match kar jate hain**!

### Interview tip
Ye ek famous "gotcha" hai. Agar tumhare data me missing keys hain aur tum SQL wala
zehni model use kar rahe ho, to unexpected extra matched rows mil sakte hain.
""")

C(r"""
left_nan = pd.DataFrame({"k": [1.0, np.nan, 3.0], "lv": ["L1", "L2", "L3"]})
right_nan = pd.DataFrame({"k": [1.0, np.nan, 4.0], "rv": ["R1", "R2", "R3"]})

joined = pd.merge(left_nan, right_nan, on="k", how="inner")
print(joined)
print("\nNaN wali row bhi match ho gayi (L2-R2) — SQL me aisa NAHI hota, SQL me NULL kabhi match nahi karta!")
assert joined.shape[0] == 2   # k=1.0 match, aur k=NaN bhi match
""")

# ----------------------------------------------------------------- join vs merge
M(r"""
## 9. `df.join` — index-based shortcut, `merge` ka chhota bhai

### Kya hai
`df.join(other)` = `merge` ka convenient version jab dono ka key **index** ho.
Default `how='left'`. Column-name clash ke liye `lsuffix`/`rsuffix` chahiye
(merge me `suffixes` automatic hai, join me lazmi dena parta hai agar clash ho).

### Kab `join` use karo, kab `merge`
- Dono tables **index se** jorne hain, koi extra column-matching nahi -> `join` (chhota syntax)
- Column-based matching, ya complex `how=`/`validate=` chahiye -> `merge`
""")

C(r"""
left_j = pd.DataFrame({"score": [90, 80]}, index=["Ali", "Sara"])
right_j = pd.DataFrame({"score": [5, 9], "grade": ["A", "B"]}, index=["Ali", "Bilal"])

try:
    left_j.join(right_j)          # 'score' dono me hai -> clash, lsuffix/rsuffix lazmi
except ValueError as e:
    print("[expected error] column clash bina suffix ke ->", e)

joined = left_j.join(right_j, lsuffix="_math", rsuffix="_science", how="outer")
print("\njoin(how='outer') with suffixes:\n", joined)

# join == merge(left_index=True, right_index=True) ka shortcut hai
same_as_merge = pd.merge(left_j, right_j, left_index=True, right_index=True,
                          suffixes=("_math", "_science"), how="outer")
print("\njoin aur merge(left_index/right_index) same natija dete hain:", joined.equals(same_as_merge))
""")

# ----------------------------------------------------------------- reshaping: long vs wide
M(r"""
## 10. Reshaping — Long vs Wide, aur "tidy data"

### Kya hai
- **Wide format**: har category apna column hai (e.g. `Q1, Q2, Q3, Q4` columns).
  Insaan ke padhne ke liye acha, code ke liye bura.
- **Long (tidy) format**: har row **ek observation**, columns = `id, variable, value`.
  Groupby/merge/plotting ke liye ye format best hai.

### Tidy data ke 3 usool (Hadley Wickham)
1. Har **variable** apna column
2. Har **observation** apni row
3. Har **observation-type** apni table

`melt` wide->long banata hai, `pivot`/`pivot_table` long->wide banata hai.
""")

M(r"""
## 11. `melt` — wide se long

### Syntax
```python
df.melt(id_vars=[...], value_vars=[...], var_name="...", value_name="...")
```
`id_vars` = jo columns waise hi rahenge (identifier), `value_vars` = jo columns
"unpivot" karne hain (default: id_vars ke ilawa sab).
""")

C(r"""
sales_wide = pd.DataFrame({
    "city": ["Lahore", "Karachi", "Islamabad"],
    "Q1": [100, 80, 60],
    "Q2": [120, 90, 70],
    "Q3": [110, 95, 65],
    "Q4": [130, 100, 90],
})
print("WIDE format:\n", sales_wide)

sales_long = sales_wide.melt(id_vars="city", var_name="quarter", value_name="amount")
print("\nLONG (tidy) format:\n", sales_long)
print("\nrows: wide =", len(sales_wide), " long =", len(sales_long), "(3 cities * 4 quarters = 12)")
assert len(sales_long) == 12
""")

M(r"""
## 12. `pivot` vs `pivot_table` — long se wide

### Kya hai
- `pivot(index=, columns=, values=)` — **saari args keyword-only hain pandas 3 me**.
  Sirf reshape karta hai, **koi aggregation nahi**. Agar `(index, columns)` combo
  duplicate ho to `ValueError: Index contains duplicate entries, cannot reshape`.
- `pivot_table(index=, columns=, values=, aggfunc=)` — duplicates ko **aggregate**
  (default `mean`) kar deta hai, is liye fail nahi hota.

### Kab konsa
Guarantee hai ke (index,columns) combo unique hai -> `pivot`. Duplicate ho sakte
hain aur summary chahiye (sum/mean/count) -> `pivot_table`.
""")

C(r"""
back_to_wide = sales_long.pivot(index="city", columns="quarter", values="amount")
print("pivot() se wapis wide:\n", back_to_wide)

# Duplicate index+columns combo -> ValueError
dup_long = pd.DataFrame({
    "city": ["Lahore", "Lahore"], "quarter": ["Q1", "Q1"], "amount": [100, 999],
})
try:
    dup_long.pivot(index="city", columns="quarter", values="amount")
except ValueError as e:
    print("\n[expected error] duplicate (index,columns) ->", e)

# pivot_table isko aggregate kar ke fix kar deta hai (default aggfunc='mean')
fixed_table = dup_long.pivot_table(index="city", columns="quarter", values="amount", aggfunc="mean")
print("\npivot_table (aggfunc='mean') se fix:\n", fixed_table)
print("(100+999)/2 =", (100 + 999) / 2)
""")

C(r"""
# pivot_table real use: monthly sales matrix with sum + margins (grand totals)
txns = pd.DataFrame({
    "region": ["North", "North", "South", "South", "North"],
    "month":  ["Jan", "Feb", "Jan", "Feb", "Jan"],
    "sales":  [100, 150, 80, 90, 50],
})
matrix = txns.pivot_table(index="region", columns="month", values="sales",
                           aggfunc="sum", fill_value=0, margins=True, margins_name="Total")
print(matrix)
print("\nmargins=True se row/column totals bhi mil gaye — reporting ke liye bohat kaam ka.")
""")

M(r"""
## 13. `stack` / `unstack` — columns <-> MultiIndex rows

### Kya hai
- `stack()` — columns ko row-index ke andar "andar" kar deta hai (wide -> long-ish, MultiIndex).
- `unstack()` — index level ko wapis column bana deta hai (ulta operation).

### Gotcha (pandas 3 verified)
`stack(dropna=...)` ab **allowed nahi** — `ValueError` deta hai (naya implementation
by-default NaN rows nahi hataata jaise purana karta tha). Sirf plain `.stack()` likho.
""")

C(r"""
wide2 = pd.DataFrame({"Q1": [100, 80], "Q2": [120, 90]}, index=["Lahore", "Karachi"])
print("wide:\n", wide2)

stacked = wide2.stack()             # columns -> inner index level, MultiIndex Series
print("\nstacked (MultiIndex Series):\n", stacked)
print("type:", type(stacked).__name__, " index:", stacked.index.names)

unstacked = stacked.unstack()       # wapis original wide shape
print("\nunstack() se wapis:\n", unstacked)
assert unstacked.equals(wide2)

# stack(dropna=...) ab error deta hai — naya behaviour hai, purana param mat do
try:
    wide2.stack(dropna=False)
except (ValueError, TypeError) as e:
    print("\n[expected error] stack(dropna=...) ->", e)
    print("(pandas 3 me naya stack by-default NaN rows nahi hataata, param dena hi mat)")
""")

C(r"""
# unstack(fill_value=) -> jab kisi combination ka data hi na ho to NaN ki jagah value
multi = pd.Series(
    [10, 20, 30],
    index=pd.MultiIndex.from_tuples([("A", "x"), ("A", "y"), ("B", "x")], names=["grp", "sub"]),
)
print("original MultiIndex series:\n", multi)

un_default = multi.unstack()
print("\nunstack() default (B,y missing -> NaN):\n", un_default)

un_filled = multi.unstack(fill_value=0)
print("\nunstack(fill_value=0):\n", un_filled)
""")

M(r"""
## 14. `wide_to_long` aur `explode`

### `wide_to_long`
Jab columns me stub + suffix pattern ho (jaise `score1970`, `score1980`), to
`pd.wide_to_long(df, stubnames=[...], i=..., j=..., sep=...)` unhe long format me
todta hai — `melt` se zyada structured jab pattern regular ho.

### `explode`
Jab ek column me **list** ho (jaise `["Python","SQL"]`), to `explode` har list-item
ki alag row bana deta hai.
""")

C(r"""
wide_pattern = pd.DataFrame({
    "id": [1, 2],
    "score2019": [70, 80], "score2020": [75, 85],
})
long_pattern = pd.wide_to_long(wide_pattern, stubnames="score", i="id", j="year", sep="")
print(long_pattern.reset_index())
print("\nstubname='score' + sep='' se 'score2019'/'score2020' -> score,year columns bane")
""")

C(r"""
skills = pd.DataFrame({
    "name": ["Ali", "Sara"],
    "skills": [["Python", "SQL"], ["Excel"]],
})
print("before explode:\n", skills)

exploded_skills = skills.explode("skills", ignore_index=True)
print("\nafter explode (har skill apni row):\n", exploded_skills)
assert len(exploded_skills) == 3
""")

# ----------------------------------------------------------------- anti-join
M(r"""
## 15. Anti-join pattern — "jinka match NAHI mila"

### Kya hai
SQL me `LEFT JOIN ... WHERE right.key IS NULL` se wo rows milti hain jinka match
nahi mila (e.g. "customers jinhone koi order nahi kiya"). Pandas me isko
`indicator=True` + `.query("_merge=='left_only'")` se karte hain.

### Semi-join
Sirf "match hua ya nahi" batana hai (columns nahi chahiye) to `isin()` kaafi hai —
faster aur saada, poora merge karne ki zaroorat nahi.
""")

C(r"""
# Anti-join: kis customer ne koi order NAHI kiya
merged_flag = pd.merge(customers, orders, on="cust_id", how="left", indicator=True)
no_orders = merged_flag.query("_merge == 'left_only'")[["cust_id", "name"]]
print("Customers bina order ke (anti-join):\n", no_orders)
assert no_orders["name"].tolist() == ["Bilal", "Hina"]

# Semi-join (halka tareeqa): sirf filter karna hai, poora merge nahi chahiye
has_order_mask = customers["cust_id"].isin(orders["cust_id"])
print("\nSemi-join (isin) — jinke orders HAIN:\n", customers[has_order_mask])
print("\nAnti-join (isin ulta) — jinke orders NAHI:\n", customers[~has_order_mask])
""")

# ----------------------------------------------------------------- gotchas
M(r"""
## 16. Common Mistakes / Gotchas — recap

1. **`concat` axis=0 ke baad duplicate index** — `ignore_index=True` ya `keys=` bhool na jao.
2. **`merge` se columns clash** hone par `suffixes` default `_x/_y` deta hai jo confusing
   hota hai — apne meaningful suffixes do.
3. **Duplicate keys = silent row explosion** — `validate=` ya `duplicated()` check kiye
   baghair production merge kabhi mat karo.
4. **int vs str key** ab `ValueError` deta hai (accha hai, purane pandas me silent empty
   result aata tha) — dtype hamesha match karo.
5. **NaN keys match kar jate hain** merge me — SQL ka zehn lagaya to surprise milega.
6. **`pivot` duplicate combo par fail** hota hai — `pivot_table` (aggregation) use karo.
7. **`stack(dropna=...)`** pandas 3 me error deta hai — param hi mat do.
8. **`how='left'` ka matlab "left table sab kuch"** hai, na ke "left column preserve" —
   log confuse karte hain.
9. `merge` vs `join`: `join` **index-based** hai, `merge` column ya index dono se ho sakta.
""")

# ----------------------------------------------------------------- real world
M(r"""
## 17. Real-World Problems

Ab 5 realistic problems — jaisa office me rozana milte hain.
""")

C(r"""
# Problem 1: orders + customers + products -> ek full report banao (3-way merge)
customers_full = pd.DataFrame({"cust_id": [1, 2, 3], "cust_name": ["Ali", "Sara", "Bilal"]})
products = pd.DataFrame({"prod_id": [10, 20], "prod_name": ["Laptop", "Mouse"], "price": [1000, 20]})
orders_full = pd.DataFrame({
    "order_id": [1, 2, 3],
    "cust_id": [1, 2, 1],
    "prod_id": [10, 20, 20],
    "qty": [1, 2, 3],
})

report = (orders_full
          .merge(customers_full, on="cust_id", how="left")
          .merge(products, on="prod_id", how="left"))
report["total"] = report["qty"] * report["price"]
print(report[["order_id", "cust_name", "prod_name", "qty", "total"]])
assert report["total"].tolist() == [1000, 40, 60]
""")

C(r"""
# Problem 2: monthly sales matrix (pivot_table) region x month report ke liye
tx = pd.DataFrame({
    "region": ["North", "South", "North", "South", "North", "South"],
    "month":  ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar"],
    "sales":  [200, 150, 220, 160, 250, 170],
})
sales_matrix = tx.pivot_table(index="region", columns="month", values="sales", aggfunc="sum")
sales_matrix = sales_matrix[["Jan", "Feb", "Mar"]]   # column order fix
print(sales_matrix)
assert sales_matrix.loc["North", "Feb"] == 220
""")

C(r"""
# Problem 3: dimension table patch — purani (kuch missing) vs nayi (kuch update) info combine
dim_old = pd.DataFrame({"sku": ["A", "B", "C"], "category": ["Elec", None, "Home"]}).set_index("sku")
dim_new = pd.DataFrame({"sku": ["B", "C"], "category": ["Elec", "Home-Decor"]}).set_index("sku")

patched = dim_old.combine_first(dim_new)     # missing (NaN) values dim_new se bharo
print("combine_first (missing bharo, existing preserve):\n", patched)

updated = dim_old.copy()
updated.update(dim_new)                       # matching (non-NaN) values OVERWRITE ho jate hain, INPLACE
print("\nupdate() (overwrite matching, inplace) natija:\n", updated)
""")

C(r"""
# Problem 4: fan-out detect karo merge ke baad (expected vs actual row count)
expected_rows = len(orders_full)     # hum expect kar rahe hain 1 order = 1 row (one-to-one/many-to-one)
after_merge = orders_full.merge(customers_full, on="cust_id", how="left")
print("expected rows:", expected_rows, " actual rows:", len(after_merge))
if len(after_merge) != expected_rows:
    print("WARNING: fan-out hua — customers_full me duplicate cust_id check karo!")
else:
    print("OK — koi fan-out nahi, merge safe hai.")
assert len(after_merge) == expected_rows
""")

C(r"""
# Problem 5: sellers/customers jinka koi bhi sale/order nahi (anti-join, LC 1607 jaisa idea)
sellers = pd.DataFrame({"seller_id": [1, 2, 3], "seller_name": ["S1", "S2", "S3"]})
sale_orders = pd.DataFrame({"order_id": [1, 2], "seller_id": [1, 1]})   # 2,3 ne kabhi becha nahi

no_sales = sellers.merge(sale_orders, on="seller_id", how="left", indicator=True) \
                   .query("_merge == 'left_only'")[["seller_name"]]
print("Sellers with no sales:\n", no_sales)
assert no_sales["seller_name"].tolist() == ["S2", "S3"]
""")
