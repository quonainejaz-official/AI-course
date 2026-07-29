"""Generator: Python/Basics/03_Strings_aur_String_Methods.ipynb"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

cells = []
M = lambda s: cells.append(md(s))   # noqa: E731
C = lambda s: cells.append(code(s))  # noqa: E731

M(r"""
# 03 — Strings aur String Methods

**Level:** Beginner → Intermediate
**Series:** Python Basics (Notebook 3 / 7)

String Python ka sab se zyada istemal hone wala data type hai. Har file, har API response,
har user input, har log line — sab strings hain. Aur interviews me string problems sab se
zyada aate hain (palindrome, anagram, reverse, unique character...).

Is notebook me hum string ko **sequence** ki tarah samjhenge, uske **50+ methods** dekhenge,
Unicode/encoding ki asli haqeeqat samjhenge, aur `+` vs `join()` ki performance ka farq
apni aankhon se dekhenge.

## Is notebook me kya seekhenge

- **Banane ke tareeqe**: quotes, triple quotes, escape sequences, raw strings
- **Sequence** ki tarah string: `len()`, indexing, negative indexing
- **Slicing** poori tafseel se — `[start:stop:step]`, reverse, aur slicing ke gotchas
- **Immutability** — aur uske asli natije (performance!)
- **Methods (categories me)**: case, whitespace/strip, search, replace, split/join,
  padding/align, validation (`is*`), `translate`
- **Unicode**: `ord`/`chr`, code points vs bytes, `encode`/`decode`, normalization
- **Comparison & sorting** — lexicographic order, `casefold` se case-insensitive
- **`str` vs `repr`** — aur kab kaun sa
- **`string` module** aur **`textwrap`**
- **Regex** ka chhota taaruf (poori tafseel Intermediate series me)
- **Performance**: `+` loop me kyun bura hai, `join` kyun behtar
- **4 LeetCode problems**: 344, 125, 242, 387

## Prerequisites

- NB 01 (`print`, `type`, `id`) aur NB 02 (immutability, `==` vs `is`, f-strings, casting)

> **Yaad rakho:** String **immutable** hai. Koi bhi "modify" karne wala method asal me
> **naya string** banata hai. Ye ek jumla is poore notebook ki jaan hai.
""")

M(r"""
---
## 1. String banane ke tareeqe

**Kya hai:** `str` Unicode **code points** ki immutable sequence hai.

| Tareeqa | Misaal | Kab |
|---|---|---|
| Single quotes | `'salam'` | rozana (PEP 8 koi tarjeeh nahi deta) |
| Double quotes | `"salam"` | jab andar apostrophe ho: `"it's"` |
| Triple quotes | `"""kai\nlines"""` | multiline text, docstrings |
| Raw string | `r"C:\new"` | regex, Windows paths |
| Concatenation of literals | `"ab" "cd"` → `"abcd"` | lambi lines torne ke liye |
| `str()` | `str(42)` | doosri type se banana |

**Note:** Python me `char` type nahi hota. `'a'` bhi length-1 ka **string** hai.
""")

C(r"""
# --- Banane ke saare tareeqe ---
s1 = 'single quotes'
s2 = "double quotes"
s3 = """triple quotes
kai lines par
phaila hua"""
s4 = '''ye bhi triple hai'''

print(s1)
print(s2)
print(s3)
print(s4)

print("\n--- Quote ke andar quote ---")
print("It's a beautiful day")          # double ke andar single
print('She said "hello" loudly')       # single ke andar double
print("Mixed: it's a \"test\"")        # escape se
print('''Teeno: it's a "test" ''')     # triple sab le leta hai

print("\n--- Implicit concatenation (adjacent literals) ---")
long_msg = ("Ye ek bohat lambi line hai jo "
            "kai tukron me likhi gayi hai, "
            "aur Python inhe khud jod deta hai.")
print(long_msg)
print("Note: yahan koi '+' nahi hai — sirf adjacent literals.")

print("\n--- char type nahi hota ---")
c = "a"
print(f"'a' ka type: {type(c).__name__}, length: {len(c)}")
print("s[0] bhi string hai:", type("hello"[0]).__name__)
""")

M(r"""
### Escape sequences

Backslash `\` ke baad khaas maani:

| Escape | Matlab |
|---|---|
| `\n` | newline |
| `\t` | tab |
| `\r` | carriage return |
| `\\` | literal backslash |
| `\'` `\"` | quote |
| `\0` | null character |
| `\b` | backspace |
| `\uXXXX` | 4-digit Unicode (`\u0645`) |
| `\UXXXXXXXX` | 8-digit Unicode |
| `\xXX` | 2-digit hex byte |
| `\N{NAME}` | Unicode naam se (`\N{GREEK SMALL LETTER PI}`) |
| `\` + newline | line continuation (koi newline insert nahi) |

**Raw string** `r"..."` me escape **kaam nahi karta** — sab literal rehta hai.
Regex aur Windows paths ke liye lazmi.

**Gotcha:** raw string **backslash par khatam nahi** ho sakti — `r"C:\"` SyntaxError hai.
""")

C(r"""
# --- Escape sequences ---
print("Newline  -> Line1\nLine2")
print("Tab      -> Col1\tCol2\tCol3")
print("Backslash-> C:\\Users\\name")
print("Quote    -> \"quoted\" aur \'single\'")
print("Unicode  -> \u0645 \u06CC\u06BA (Urdu letters), \u03C0 (pi)")
print("By name  -> \N{GREEK SMALL LETTER PI} \N{DEGREE SIGN} \N{RUPEE SIGN}")
print("Hex byte -> \x41\x42\x43 (ASCII 65,66,67)")
print("Bell/back-> 'ab\bc' =", repr("ab\bc"), "(\\b backspace hai)")

print("\n--- Line continuation (backslash + newline) ---")
one_line = "ye ek \
hi line hai"
print(one_line, "| length:", len(one_line))

print("\n--- Raw strings ---")
print("normal :", "C:\name\test")        # \n aur \t escape ban gaye — BUG!
print("raw    :", r"C:\name\test")       # sahi path
print("repr normal:", repr("C:\name"))
print("repr raw   :", repr(r"C:\name"))

print("\n--- Regex ke liye raw lazmi hai ---")
import re
print("r'\\d+' se match:", re.findall(r"\d+", "order 42, qty 7"))
print("bina raw likhna parta: '\\\\d+' — aankhon ko takleef hoti hai")

print("\n--- Raw string backslash par khatam nahi ho sakti ---")
try:
    compile(r'x = r"C:\"', "<demo>", "exec")
except SyntaxError as e:
    print("SyntaxError:", e.msg)
print("Hal: 'C:' + chr(92)  ya  r'C:' '\\\\'  ->", "C:" + chr(92))
""")

M(r"""
---
## 2. String ek SEQUENCE hai

`str` bhi `list`/`tuple` ki tarah **sequence** hai, is liye ye sab chalta hai:
`len()`, `s[i]`, `s[a:b]`, `in`, `for ch in s`, `min()`, `max()`, `sorted()`, `reversed()`.

**Indexing:**
```
 s  =  P    y    t    h    o    n
 +ve   0    1    2    3    4    5
 -ve  -6   -5   -4   -3   -2   -1
```
`s[-1]` aakhri character — ye Python ka bohat kaam ka idiom hai.

**Gotcha:** ghalat index par **`IndexError`** aata hai (slicing par nahi aata — aage dekho).
""")

C(r"""
# --- len aur indexing ---
s = "Python"
print(f"s = {s!r}, len = {len(s)}")

print("\n--- Positive indexing ---")
for i in range(len(s)):
    print(f"  s[{i}] = {s[i]!r}")

print("--- Negative indexing (aakhir se) ---")
for i in range(-1, -len(s) - 1, -1):
    print(f"  s[{i}] = {s[i]!r}")

print("\n--- Aam idioms ---")
print("pehla char  s[0]  :", s[0])
print("aakhri char s[-1] :", s[-1], "  <- len(s)-1 likhne ki zaroorat nahi")
print("doosra-aakhri s[-2]:", s[-2])

print("\n--- IndexError ---")
try:
    print(s[10])
except IndexError as e:
    print("s[10] -> IndexError:", e)
try:
    print(s[-10])
except IndexError as e:
    print("s[-10] -> IndexError:", e)

print("\n--- Sequence ke doosre operations ---")
print("'y' in s        ->", "y" in s)
print("min(s)          ->", min(s), "(sab se chhota code point)")
print("max(s)          ->", max(s))
print("sorted(s)       ->", sorted(s), "<- LIST deta hai, string nahi")
print("''.join(sorted(s)) ->", "".join(sorted(s)))
print("list(reversed(s))  ->", list(reversed(s)))
print("''.join(reversed(s)) ->", "".join(reversed(s)))
""")

M(r"""
---
## 3. Slicing — `s[start:stop:step]`

**Qanoon:**
- `start` **shamil** hai, `stop` **shamil nahi** (half-open interval) — yani `s[1:4]` me index 1,2,3.
- `start` default `0` (ya `-1` agar step negative ho), `stop` default "aakhir tak", `step` default `1`.
- **Slicing kabhi `IndexError` nahi deta** — hadd se bahar ho to chup chaap clip kar deta hai.
- Slice hamesha **naya** string deta hai.

**Yaad rakhne wale idioms:**

| Slice | Matlab |
|---|---|
| `s[:]` | poori copy |
| `s[::-1]` | **reverse** (sab se mashhoor trick) |
| `s[:n]` | pehle `n` characters |
| `s[n:]` | `n` ke baad sab |
| `s[-n:]` | aakhri `n` characters |
| `s[:-n]` | aakhri `n` chhor kar |
| `s[::2]` | har doosra character |
| `s[1::2]` | odd positions |

**Kyun `stop` shamil nahi?** Do faide: `len(s[a:b]) == b - a`, aur `s[:i] + s[i:] == s`
(koi overlap ya gap nahi).
""")

C(r"""
# --- Slicing ka poora tour ---
s = "Python Programming"
print(f"s = {s!r}  (len = {len(s)})\n")

slices = [
    ("s[0:6]",     s[0:6],     "index 0 se 5 tak (6 shamil NAHI)"),
    ("s[:6]",      s[:6],      "start default 0"),
    ("s[7:]",      s[7:],      "stop default = aakhir"),
    ("s[:]",       s[:],       "poori copy"),
    ("s[-11:]",    s[-11:],    "aakhri 11"),
    ("s[:-12]",    s[:-12],    "aakhri 12 chhor kar"),
    ("s[7:14]",    s[7:14],    "beech ka hissa"),
    ("s[::2]",     s[::2],     "har doosra char"),
    ("s[1::2]",    s[1::2],    "index 1 se, har doosra"),
    ("s[::3]",     s[::3],     "har teesra"),
    ("s[::-1]",    s[::-1],    "REVERSE"),
    ("s[::-2]",    s[::-2],    "reverse, har doosra"),
    ("s[-1:0:-1]", s[-1:0:-1], "reverse magar s[0] chhor kar"),
]
print(f"{'slice':<12} {'natija':<22} matlab")
print("-" * 64)
for expr, val, why in slices:
    print(f"{expr:<12} {val!r:<22} {why}")

print("\n--- Do khoobsurat qanoon ---")
print("len(s[3:9]) == 9-3 ->", len(s[3:9]) == 9 - 3)
i = 6
print(f"s[:{i}] + s[{i}:] == s ->", s[:i] + s[i:] == s, "(koi gap/overlap nahi)")
""")

C(r"""
# --- Slicing ke GOTCHAS ---
s = "Python"

print("--- 1. Out-of-range slice error NAHI deta (indexing deta hai) ---")
print("s[0:100]  ->", repr(s[0:100]), "(chup chaap clip)")
print("s[100:]   ->", repr(s[100:]), "(khali string, koi error nahi)")
print("s[-100:]  ->", repr(s[-100:]))
try:
    s[100]
except IndexError as e:
    print("magar s[100] -> IndexError:", e)

print("\n--- 2. Ulti tarteeb -> khali string (step positive ke sath) ---")
print("s[4:1]    ->", repr(s[4:1]), "(start > stop, step +1 -> khali)")
print("s[4:1:-1] ->", repr(s[4:1:-1]), "(negative step ke sath sahi chalta hai)")

print("\n--- 3. step = 0 -> ValueError ---")
try:
    s[::0]
except ValueError as e:
    print("s[::0] -> ValueError:", e)

print("\n--- 4. Negative step ke sath defaults ULTE ho jate hain ---")
print("s[::-1]     ->", repr(s[::-1]), "(start=aakhir, stop=shuru se pehle)")
print("s[:3:-1]    ->", repr(s[:3:-1]), "(aakhir se index 4 tak)")
print("s[3::-1]    ->", repr(s[3::-1]), "(index 3 se shuru tak, ulta)")

print("\n--- 5. slice() object bhi banaya ja sakta hai ---")
first_three = slice(0, 3)
last_two = slice(-2, None)
every_other = slice(None, None, 2)
print("slice(0,3)         ->", s[first_three])
print("slice(-2, None)    ->", s[last_two])
print("slice(None,None,2) ->", s[every_other])
print("Faida: slice ko variable me rakh kar dobara use kar sakte ho")

print("\n--- 6. Slice assignment string par NAHI chalti (immutable) ---")
try:
    s[0:2] = "XY"
except TypeError as e:
    print("TypeError:", e)
print("list par chalti hai:", end=" ")
lst = list("Python")
lst[0:2] = "XY"
print("".join(lst))
""")

M(r"""
---
## 4. Concatenation, repetition aur immutability

| Operator | Kaam | Misaal |
|---|---|---|
| `+` | jodna | `"a" + "b"` → `"ab"` |
| `*` | dohrana | `"ab" * 3` → `"ababab"` |
| `+=` | jod kar rebind | naya object banta hai |

**Immutability ka asli natija — performance:**
Loop me `s += x` karna **O(n²)** hai, kyunki har baar poora naya string copy hota hai.
`"".join(list_of_parts)` **O(n)** hai. Bare data par ye farq seconds vs milliseconds ka hota hai.

> **Interview me ye zaroor poocha jata hai:** "Loop me string banane ka behtar tareeqa kya hai?"
> Jawab: parts ko list me jama karo, aakhir me ek baar `join`.
""")

C(r"""
# --- Concatenation aur repetition ---
print('"Py" + "thon"   =', "Py" + "thon")
print('"ab" * 3        =', "ab" * 3)
print('3 * "ab"        =', 3 * "ab", "(dono taraf chalta hai)")
print('"ab" * 0        =', repr("ab" * 0), "(khali)")
print('"ab" * -1       =', repr("ab" * -1), "(negative bhi khali)")
print('"-" * 30        =', "-" * 30, "<- separator line ka idiom")

print("\n--- Number se jodne par TypeError ---")
try:
    "Age: " + 25
except TypeError as e:
    print("TypeError:", e)
print("Hal:", "Age: " + str(25), "| ya f-string:", f"Age: {25}")

print("\n--- Immutability: har 'tabdeeli' naya object ---")
s = "hello"
print(f"shuru      : {s!r}  id={id(s)}")
s += " world"
print(f"after +=   : {s!r}  id={id(s)}  <- id BADAL gaya (naya object)")
s = s.upper()
print(f"after upper: {s!r}  id={id(s)}")

t = "abc"
print(f"\nt.upper() ne t ko badla? t = {t!r} -> {t.upper()!r}, magar t abhi bhi {t!r}")
print("SABAQ: string methods ka natija PAKARNA parta hai: t = t.upper()")
""")

C(r"""
# --- '+' loop vs join: asli performance ka farq ---
import time

N = 20_000

# Tareeqa 1: += loop -> O(n^2), har baar naya string copy
t0 = time.perf_counter()
out = ""
for i in range(N):
    out += "x"
t_plus = time.perf_counter() - t0

# Tareeqa 2: list me jama karo, aakhir me join -> O(n)
t0 = time.perf_counter()
parts = []
for i in range(N):
    parts.append("x")
joined = "".join(parts)
t_join = time.perf_counter() - t0

# Tareeqa 3: generator + join (sab se saaf)
t0 = time.perf_counter()
gen_joined = "".join("x" for _ in range(N))
t_gen = time.perf_counter() - t0

# Tareeqa 4: repetition operator (jab mumkin ho, sab se tez)
t0 = time.perf_counter()
repeated = "x" * N
t_rep = time.perf_counter() - t0

assert out == joined == gen_joined == repeated       # natija bilkul same
print(f"N = {N:,} characters | teeno ka natija ek jaisa: {out == joined == repeated}\n")
results = sorted([("+= loop  ", t_plus), ("list+join", t_join),
                  ("gen+join ", t_gen), ("'x' * N  ", t_rep)], key=lambda r: r[1])
fastest = results[0][1]
for label, sec in results:
    print(f"  {label} {sec * 1000:8.2f} ms   ({sec / fastest:6.1f}x)")

print("\nNote: CPython me += ke liye ek chhupa optimization hai (refcount 1 ho to in-place),")
print("is liye farq theoretical O(n^2) se kam nazar aata hai. Magar join hamesha SAFE choice hai —")
print("doosre implementations (PyPy, Jython) me ye optimization nahi hoti.")
""")

C(r"""
# --- Iteration ke tareeqe ---
s = "Python"

print("1. Seedha character par loop:")
print("  ", " ".join(ch for ch in s))

print("\n2. enumerate() — index + character (Pythonic tareeqa):")
for i, ch in enumerate(s):
    print(f"   {i}: {ch}", end="  ")
print()

print("\n3. enumerate(start=1) — 1 se ginti:")
for i, ch in enumerate(s, start=1):
    print(f"   {i}:{ch}", end="")
print()

print("\n4. range(len(s)) — kaam karta hai magar GHAIR-Pythonic:")
for i in range(len(s)):
    print(f"   {s[i]}", end="")
print("   <- enumerate behtar hai")

print("\n5. zip() se do strings sath sath:")
for a, b in zip("abc", "xyz"):
    print(f"   {a}-{b}", end="  ")
print()

print("\n6. zip(s, s[1:]) — consecutive pairs (sliding window):")
for a, b in zip(s, s[1:]):
    print(f"   {a}{b}", end="")
print()

print("\n7. reversed() se ulta:")
print("  ", "".join(reversed(s)))
""")

# CHUNK_MARKER

save(r"Python/Basics/03_Strings_aur_String_Methods.ipynb", cells)
