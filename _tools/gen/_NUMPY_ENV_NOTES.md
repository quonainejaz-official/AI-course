# ENV NOTES — NumPy authors (asli machine par probe kiye hue facts, guess NAHI)

`AGENT_SPEC.md` ke saath ye bhi LAZMI follow karo. Ye sab `runnb.py` ke asli
environment par test kar ke likha gaya hai.

## Runtime
- Python **3.14.0**, **numpy 2.4.2**, pandas 3.0.x. matplotlib/seaborn NAHI. Network NAHI. `input()` NAHI.
- `runnb.py` har code cell ko **shared namespace** me `exec()` karta hai, cwd = fresh temp dir.
- Koi bhi cell exception phenke to `[FAIL]`. Warnings se FAIL nahi hota (magar demo me `np.errstate` use karna behtar).

## NumPy 2.x me jo cheezein TOOT gayi hain (verified) — inhe as-is MAT likho
| Purani cheez | Ab kya hota hai | Kya likhna hai |
|---|---|---|
| `np.in1d(a, b)` | `AttributeError` (numpy 2 me hata diya gaya) | sirf `np.isin()` use karo; `in1d` ka zikr "removed in NumPy 2.0" ke tor par karo (call na karo, ya `try/except AttributeError`) |
| `arr.ptp()` (method) | `AttributeError` | `np.ptp(arr)` function form |
| `np.row_stack` | `DeprecationWarning` | `np.vstack` |
| `np.NaN`, `np.Inf`, `np.float_`, `np.int0`, `np.unicode_` | `AttributeError` (removed) | `np.nan`, `np.inf`, `np.float64`, `np.str_` |
| `np.int8(200)` | `OverflowError: Python integer 200 out of bounds for int8` | overflow demo ke liye `np.array([127], np.int8) + np.int8(1)` (→ `-128`) ya `np.array([300]).astype(np.int8)` (→ `44`); scalar-constructor wala case `try/except OverflowError` me |
| `np.array(obj, copy=False)` | `ValueError: Unable to avoid copy...` | `np.asarray(obj)` use karo. `copy=False` ka naya matlab "never copy" hai — ye **behtareen gotcha cell** hai, `try/except ValueError` me dikhao |
| `np.trapz` | renamed | `np.trapezoid` |
| `np.matrix(...)` | `PendingDeprecationWarning` | sirf zikr karo ke "matrix subclass use na karo"; call karni ho to warnings suppress karke ya bilkul na karo |

## Warning wale operations — `np.errstate` me lapeto (verified chalta hai)
```python
with np.errstate(divide="ignore", invalid="ignore"):
    print(np.array([1.0, 0.0]) / 0)      # [inf nan]
with np.errstate(over="ignore"):
    print(np.array([127], np.int8) + np.int8(1))   # [-128]
```

## Ye sab VERIFIED chalte hain (be-fikr use karo)
`np.isin`, `np.ptp`, `np.take(..., mode='clip')`, `np.put`, `np.ix_`, `np.moveaxis`,
`np.select`, `np.piecewise`, `np.bincount`, `np.histogram`, `np.unravel_index`,
`np.add.reduce`, `np.add.outer`, `np.vectorize`, `np.frompyfunc`, `np.pad`,
`np.diag`, `np.diagflat`, `np.tri`, `np.resize`, `arr.resize(...)` (returns None),
`np.fromiter(..., dtype=..., count=...)`, `np.fromfunction`, `np.meshgrid`,
`np.logspace`, `np.empty`, `np.array_split`, `np.insert/append/delete`, `np.rot90`,
`np.may_share_memory`, `.base`, `arr.flags`, `arr.strides`, `arr.flat`,
`np.finfo(np.float64).eps`, `np.iinfo(np.int8).min/max`, `np.isclose(..., equal_nan=True)`,
`np.allclose`, `np.argsort(kind='stable')`, `np.sort(axis=None)`, `np.median/quantile/percentile`,
`np.count_nonzero(axis=...)`, `np.nanmean/nansum/...`, `np.datetime64`, `np.char.upper`,
`np.strings.upper`, `np.lib.stride_tricks.sliding_window_view`, `np.einsum`,
`np.set_printoptions` / `np.get_printoptions` / `np.printoptions` (context manager),
`np.random.default_rng(...)` (`.integers/.random/.normal/.choice/.shuffle/.permutation`),
legacy `np.random.seed(0)` + `np.random.rand(...)`.

## Genuine TypeError/ValueError demos (try/except me dikhao — accha teaching material)
- `np.arange(5).reshape(2, 3)` → `ValueError: cannot reshape array of size 5 into shape (2,3)`
- `np.array([True]) - np.array([False])` → `TypeError: numpy boolean subtract ... use ^`
- integer array me float in-place: `a = np.arange(3); a += 0.5` → `UFuncTypeError` (Cannot cast ... 'same_kind') — **dtype trap ka best example**
- broadcasting shape error: `np.ones((3,4)) + np.ones((3,5))` → `ValueError: operands could not be broadcast together`

## Print/repr ki shakal (numpy 2 scalars) — assert ke waqt dhyan
- Aggregations **numpy scalar** dete hain aur repr aisa hota hai: `np.int64(4)`, `np.float64(1.0)`, `np.True_`.
- Isliye assert me `== value` likho (kaam karta hai) ya `bool(...)`/`float(...)` se convert karo.
  `assert np.array_equal(a, b)` aur `assert np.allclose(a, b)` use karo — element-wise `==` par
  seedha `assert` (multi-element) `ValueError: truth value of an array is ambiguous` dega
  (ye bhi ek zaroori gotcha cell hai).

## Reproducibility
- Har random cheez me **seed** do: `rng = np.random.default_rng(42)`. Asserts random values par
  depend karein to seed fix ho aur value usi machine par verified ho (script chala kar dekh lo).
- **Timing-based assert NAHI** (`assert fast < slow` mana hai) — sirf print karo aur samjhao.
- `timeit` me cell ke variables chahiye to `globals=globals()` LAZMI.

## Performance/memory numbers
- `sys.getsizeof(np.arange(3))` → `136` (machine-specific, assert na karo, print karo).
- `arr.nbytes` deterministic hai (assert kar sakte ho).
- Notebook total run time **< ~10 second** rakho: timeit ke `number=` chhota (1000-10000), arrays chhote (<= 1e6 elements).
