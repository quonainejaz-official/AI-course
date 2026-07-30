import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ============================================================================
# TITLE / ROADMAP
# ============================================================================
cells.append(md(r"""
# 05 — Lists aur Tuples (Python Basics)

**Level:** Beginner → Advanced (interview-ready)

Is notebook me hum Python ke do sabse zyada use hone wale sequence types — **list** aur **tuple** —
ko zero se advance tak cover karenge. Senior-dev-to-junior style: har concept ka **kya/kyun/syntax/example/gotcha/interview tip**.

## Is notebook me kya seekhenge (roadmap)

1. List basics — banane ke tareeqe, heterogeneous elements, nesting
2. Indexing, negative indexing, `IndexError`
3. Slicing `[a:b:c]`, negative step, slice copy
4. Slice assignment (grow/shrink/insert/delete) — in depth
5. `lst[:] = other` vs `lst = other` — in-place vs rebinding (bohat important!)
6. Saare list methods — `append`, `extend`, `insert`, `remove`, `pop`, `clear`, `index`, `count`, `sort`, `reverse`, `copy`
7. `del` statement vs `pop`/`remove`
8. `sort` vs `sorted` — key, reverse, multi-key, stability, dicts/tuples sort karna
9. List comprehensions — filter, nested, flatten, generator vs list, perf
10. 2D lists / matrices — trap `[[0]*3]*3`, transpose, row/col sums
11. Copy semantics — alias vs shallow vs deep copy
12. Unpacking — starred targets, nested, swap, `*args`
13. Membership & complexity — `in` O(n) vs set O(1), full complexity table
14. Other useful built-ins — `min/max`, `zip`, `enumerate`, `itertools`
15. Tuples — immutability, hashability, `namedtuple`, tuple vs list decision table
16. Common Mistakes / Gotchas
17. Real-World Problems (6)
18. LeetCode Problems (6, Easy) — two-pointer pattern
19. Interview Q&A (15)
20. Practice Exercises (8)
21. Summary / Cheat-sheet

## Prerequisites

- Python variables, basic data types (`int`, `str`, `float`, `bool`)
- `for` loops, `if/else`, functions basics
- Pichli notebook: `04_...` (agar cover ho chuki ho) — warna bhi chalega, ye notebook self-contained hai.
"""))

# ============================================================================
# 1. LIST BASICS
# ============================================================================
cells.append(md(r"""
## 1. List Basics

**Kya hai:** `list` Python ka **ordered, mutable** (badla ja sakta hai) collection hai. Elements kisi bhi type ke ho sakte hain.

**Kyun/kahan:** Jab bhi tumhein items ka ek sequence chahiye jo **grow/shrink** ho, ya jisko baad me modify karna ho — list use karo
(agar modify nahi karna to tuple better hai — us par aage aayenge).

**Syntax:** `[]`, `list()`, `list(iterable)`.
"""))

cells.append(code(r"""
# List banane ke kayi tareeqe - sab common hain, interview me bhi poochte hain
lst_literal = [1, 2, 3, 4, 5]                 # seedha literal syntax - sabse common
lst_empty = []                                 # empty list
lst_from_range = list(range(5))                # list() constructor + range() se
lst_from_str = list("abc")                     # string ko characters ki list banate hain
lst_repeat = [0] * 5                           # ek value ko n baar repeat karna
lst_hetero = [1, "two", 3.0, True, None]       # heterogeneous - kisi bhi type ka mix chalta hai
lst_nested = [1, [2, 3], [4, [5, 6]]]          # nested lists - list ke andar list

print("literal:      ", lst_literal)
print("from range:   ", lst_from_range)
print("from string:  ", lst_from_str)
print("repeat [0]*5: ", lst_repeat)
print("hetero:       ", lst_hetero)
print("nested:       ", lst_nested)
print("len(nested):  ", len(lst_nested))          # len() top-level elements ginta hai, andar wale nahi
print("empty truthy? ", bool(lst_empty))           # empty list -> False
print("literal truthy?", bool(lst_literal))        # non-empty -> True
"""))

cells.append(md(r"""
**Output ka matlab:** `len(lst_nested)` = 3 (kyunki top-level par 3 items hain: `1`, `[2,3]`, `[4,[5,6]]`) —
nested elements ko count nahi karta.

**Common mistakes / gotchas:**
- `lst_repeat = [0] * 5` sirf **immutable** elements (int, str) ke liye safe hai. Agar andar mutable object ho
  (jaise `[[0]*3]*3`), sab references **same object** ki taraf point karti hain — ye trap aage detail me dekhenge.
- Empty list `[]` **falsy** hoti hai — `if my_list:` likhna `if len(my_list) > 0:` se zyada Pythonic hai.

**Interview tip:** "Truthiness of empty containers" ek common interview question hai — list, tuple, dict, str,
set sab empty hone par `False` hote hain.
"""))

# ============================================================================
# 2. INDEXING / NEGATIVE INDEXING / IndexError
# ============================================================================
cells.append(md(r"""
## 2. Indexing aur Negative Indexing

**Kya hai:** Har element ka ek position hota hai — `0` se shuru (positive) ya `-1` se end se (negative).

**Kyun:** Kisi bhi element ko O(1) me directly access karne ke liye.

**Syntax:** `lst[i]`
"""))

cells.append(code(r"""
nums = [10, 20, 30, 40, 50]
print(nums[0])    # pehla element -> 10
print(nums[-1])   # aakhri element -> 50 (negative indexing)
print(nums[2])    # teesra element -> 30
print(nums[-2])   # doosra last -> 40

try:
    print(nums[10])   # IndexError - list ki range se bahar
except IndexError as e:
    print("IndexError pakda gaya:", e)
"""))

cells.append(md(r"""
**Common mistakes:** `nums[len(nums)]` bhi `IndexError` dega — last valid index `len(nums)-1` hai, `len(nums)` nahi.

**Interview tip:** Negative index `-1` "last element" ke liye idiomatic hai — `nums[len(nums)-1]` likhna beginner smell hai.
"""))

# ============================================================================
# 3. SLICING
# ============================================================================
cells.append(md(r"""
## 3. Slicing `[start:stop:step]`

**Kya hai:** Ek sath multiple elements nikalna, **naya list** return karta hai (original untouched).

**Syntax:** `lst[start:stop:step]` — `stop` **exclusive** hota hai.
"""))

cells.append(code(r"""
nums = [10, 20, 30, 40, 50, 60]
print(nums[1:4])       # index 1,2,3 (4 exclusive) -> [20,30,40]
print(nums[:3])        # start se index 2 tak -> [10,20,30]
print(nums[3:])        # index 3 se end tak -> [40,50,60]
print(nums[::2])       # har doosra element -> [10,30,50]
print(nums[::-1])      # pura list reverse -> [60,50,40,30,20,10]
print(nums[-3:])       # last 3 elements -> [40,50,60]

# COPY via slice - [:] naya (shallow) list banata hai, alias NAHI
copy_via_slice = nums[:]
copy_via_slice.append(999)
print("original:", nums)
print("copy:    ", copy_via_slice)
print("same object?", nums is copy_via_slice)   # False - alag objects
"""))

cells.append(md(r"""
**Output ka matlab:** `nums[:]` ek naya list object banata hai jiska content same hai — is liye `copy_via_slice`
me append karne se original `nums` **change nahi** hota. Ye "shallow copy" ka sabse simple tareeqa hai.

**Common mistakes:** `nums[3:1]` (start > stop, positive step) empty list deta hai, error nahi. Slicing kabhi
`IndexError` nahi deti — out-of-range indices silently clamp ho jate hain.

**Interview tip:** `nums[::-1]` reverse karne ka sabse fast/idiomatic tareeqa hai (vs `list(reversed(nums))`).
"""))

# ============================================================================
# 4. SLICE ASSIGNMENT (in depth)
# ============================================================================
cells.append(md(r"""
## 4. Slice Assignment — in depth

**Kya hai:** Slice ko sirf read hi nahi, **assign** bhi kar sakte ho — list ka size khud-ba-khud grow/shrink ho jata hai.

**Kyun:** Bulk replace, insert, ya delete karna — bina naya list banaye, in-place.
"""))

cells.append(code(r"""
# 1) SAME LENGTH replace - straightforward
a = [1, 2, 3, 4, 5]
a[1:3] = [20, 30]              # 2 elements ki jagah 2 naye elements
print("same length:", a)

# 2) DIFFERENT LENGTH - GROW (2 elements ki jagah 4 daal diye)
b = [1, 2, 3, 4, 5]
b[1:3] = [20, 30, 40, 50]
print("grow:       ", b)

# 3) DIFFERENT LENGTH - SHRINK (3 elements ki jagah 1 daala)
c = [1, 2, 3, 4, 5]
c[1:4] = [99]
print("shrink:     ", c)

# 4) INSERT without removing - EMPTY slice (koi element remove nahi hota, bas ghusaya)
d = [1, 2, 3]
d[1:1] = [100, 101]            # index 1 par insert, kuch delete nahi
print("insert:     ", d)

# 5) DELETE via empty list assign
e = [1, 2, 3, 4, 5]
e[1:3] = []                     # index 1,2 delete
print("delete:     ", e)
"""))

cells.append(code(r"""
# 6) EXTENDED SLICE (step != 1) - length EXACTLY match honi chahiye
f = [1, 2, 3, 4, 5, 6]
f[::2] = [100, 200, 300]        # 3 positions (0,2,4), 3 values diye - theek
print("extended slice ok:", f)

try:
    g = [1, 2, 3, 4, 5, 6]
    g[::2] = [1, 2]              # sirf 2 values diye, 3 positions hain -> ValueError
except ValueError as e:
    print("ValueError (extended slice length mismatch):", e)
"""))

cells.append(md(r"""
**Output ka matlab:** Normal slice (`step=1`) ka target list **kisi bhi length** ka ho sakta hai (grow/shrink allowed).
Lekin **extended slice** (`step != 1`) ke liye assigned values ki count **exactly** utni honi chahiye jitni slice
me positions hain — warna `ValueError`.

**Common mistakes:** Beginners `lst[2:2] = [x]` aur `lst.insert(2, x)` me confuse hote hain — dono same kaam karte
hain single element ke liye, lekin slice assignment multiple elements ek sath insert kar sakti hai.

**Interview tip:** `lst[a:b] = []` aur `del lst[a:b]` **same effect** dete hain — dono se poocho, dono chalne
chahiye demo me.
"""))

# ============================================================================
# 5. lst[:] = other  vs  lst = other
# ============================================================================
cells.append(md(r"""
## 5. `lst[:] = other` vs `lst = other` — In-place vs Rebinding (BOHAT IMPORTANT)

**Kya hai:** Ye Python ka sabse confuse karne wala concept hai — ek **same object ko modify** karta hai,
doosra **variable ko naye object se re-point** karta ha.

**Kyun important hai:** Agar kisi function ke andar list ko "replace" karna ho aur caller ko bhi dikhna ho,
to `[:] =` use karna hoga — plain `=` sirf local reference badalega.
"""))

cells.append(code(r"""
# Case A: [:] = ... -> IN-PLACE replace, saare aliases update hote hain
original = [1, 2, 3]
alias = original                # alias aur original SAME object
original[:] = [9, 9, 9]         # original object ke andar ka data replace hua
print("Case A - alias after [:] replace:", alias)   # [9,9,9] - alias bhi badla!
print("Case A - same object?", alias is original)    # True - dono ab bhi same object

# Case B: = ... -> REBINDING, sirf 'original2' naye object ki taraf point karta hai
original2 = [1, 2, 3]
alias2 = original2
original2 = [9, 9, 9]           # naya object banaya, sirf original2 usko point karta hai
print("Case B - alias2 after rebind:", alias2)       # [1,2,3] - alias2 purana hi hai
print("Case B - original2:", original2)               # [9,9,9]
print("Case B - same object?", alias2 is original2)   # False - ab alag objects
"""))

cells.append(md(r"""
**Output ka matlab:** `original[:] = [9,9,9]` list ke andar ka data **mutate** karta hai — object ka `id()` same
rehta hai. `original2 = [9,9,9]` variable ko naye object se **rebind** karta hai — purana object jahan `alias2`
abhi bhi point karta hai, waisa hi rehta hai.

**Common mistakes:** Function ke andar `def reset(lst): lst = []` caller ka list **empty nahi karega** (rebind hai,
local scope me). `def reset(lst): lst[:] = []` caller ka list **empty kar dega** (in-place).

**Interview tip:** Ye Python me "pass by object reference" samjhane ka best example hai — interview me
zaroor poocha jata hai "list ko function ke andar reset kaise karo taake caller ko dikhe".
"""))

# ============================================================================
# 6. LIST METHODS
# ============================================================================
cells.append(md(r"""
## 6. List Methods — mukammal tour

Har method: kya karta hai, return value kya hai (bohat se **`None`** return karte hain — in-place mutate),
aur common gotcha.
"""))

cells.append(code(r"""
# append() vs + : append single element end me add karta hai, original ko MUTATE karta hai
lst = [1, 2, 3]
lst.append(4)
print("append:", lst)

# + naya list BANATA hai, original nahi badalta
lst2 = [1, 2, 3] + [4, 5]
print("plus (+):", lst2)

# extend() vs append(list) - CLASSIC CONFUSION
lst3 = [1, 2, 3]
lst3.extend([4, 5])             # extend elements ko ek-ek karke add karta hai
print("extend([4,5]):", lst3)

lst4 = [1, 2, 3]
lst4.append([4, 5])             # append pura [4,5] ko EK single element ki tarah daal deta hai!
print("append([4,5]) - GOTCHA:", lst4)

# extend() ek STRING bhi le sakta hai - string ek iterable hai, characters add hote hain
lst5 = [1, 2, 3]
lst5.extend("ab")
print("extend('ab'):", lst5)
"""))

cells.append(code(r"""
# insert(index, value) - O(n) kyunki index ke baad ke saare elements shift hote hain
lst6 = [10, 20, 30]
lst6.insert(1, 99)
print("insert:", lst6)

# remove(value) - sirf PEHLA match hatata hai, missing par ValueError
lst7 = [1, 2, 3, 2, 1]
lst7.remove(2)
print("remove (first match only):", lst7)
try:
    lst7.remove(100)
except ValueError as e:
    print("remove ValueError:", e)

# pop([index]) - default last element, index bhi de sakte ho; empty par IndexError
lst8 = [1, 2, 3]
popped_last = lst8.pop()        # default -1
popped_first = lst8.pop(0)      # explicit index
print("pop() results:", popped_last, popped_first, "| remaining:", lst8)
try:
    [].pop()
except IndexError as e:
    print("pop empty list IndexError:", e)

# clear() - sab elements hata deta hai, list object wahi rehta hai (empty)
lst9 = [1, 2, 3]
lst9.clear()
print("clear:", lst9)
"""))

cells.append(code(r"""
# index(value, [start], [stop]) - pehla occurrence dhoondta hai, optional start/stop range
lst10 = [5, 3, 8, 3, 9, 3]
print("index of 3 (default):     ", lst10.index(3))         # 1
print("index of 3 (start=2):     ", lst10.index(3, 2))        # 3
print("index of 3 (start=2,stop=4):", lst10.index(3, 2, 4))    # 3
try:
    lst10.index(100)
except ValueError as e:
    print("index() ValueError:", e)

# count(value) - kitni baar value milti hai
print("count of 3:", lst10.count(3))

# sort() - IN-PLACE sort, returns None -> #1 BEGINNER BUG
lst11 = [5, 2, 9, 1]
return_value = lst11.sort()
print("sort() in place:", lst11, "| return value (None!):", return_value)
# GOTCHA: x = lst.sort() likhoge to x hamesha None hoga - lst khud sorted ho jata hai

# reverse() - IN-PLACE, returns None bhi
lst12 = [1, 2, 3]
lst12.reverse()
print("reverse:", lst12)

# copy() - SHALLOW copy, naya top-level list object
lst13 = [1, 2, 3]
lst14 = lst13.copy()
lst14.append(4)
print("copy - original:", lst13, "| copy:", lst14)
"""))

cells.append(md(r"""
**Common mistakes/gotchas (summary):**
- `x = my_list.sort()` → `x` **None** hoga, list khud sort ho gaya. Chahiye to `sorted(my_list)` use karo.
- `append([4,5])` vs `extend([4,5])` — pehla nested list banata hai, doosra flatten karta hai.
- `remove()` **value** se dhoondta hai, `pop()` **index** se — dono confuse hote hain beginners me.
- `insert(0, x)` aur `pop(0)` dono **O(n)** hain (sab elements shift karne padte hain) — queue jaisa use case ho
  to `collections.deque` behtar hai (aage dekhenge).

**Interview tip:** "In-place methods return `None`" — ye ek favourite trick question hai
(`sort`, `reverse`, `append`, `extend`, `insert`, `remove`, `clear` sab `None` return karte hain).
"""))

# ============================================================================
# 7. del STATEMENT
# ============================================================================
cells.append(md(r"""
## 7. `del` Statement — `pop`/`remove` se kaisa alag

**Kya hai:** `del` ek **statement** hai (method nahi), list ke element(s) ya poore variable ko delete kar sakta hai.

**Kyun:** Jab value **wapas nahi chahiye** (sirf hatani hai) — `pop()` value return karta hai, `del` kuch return nahi karta.
"""))

cells.append(code(r"""
lst = [1, 2, 3, 4, 5]
del lst[0]              # single index delete
print("del lst[0]:", lst)

del lst[1:3]            # slice delete
print("del lst[1:3]:", lst)

lst_full = [1, 2, 3]
del lst_full             # variable hi khatam - object bhi reference-free ho jata hai
try:
    print(lst_full)
except NameError as e:
    print("NameError after del lst_full:", e)
"""))

cells.append(md(r"""
**Comparison table:**

| | `pop(i)` | `remove(v)` | `del lst[i]` |
|---|---|---|---|
| Input | index | value | index/slice |
| Return | removed value | `None` | `None` (statement) |
| Missing case | `IndexError` | `ValueError` | `IndexError` |
| Poora variable delete kar sakta? | nahi | nahi | haan (`del lst`) |

**Interview tip:** `del lst` variable ko **unbind** karta hai — agar object ka koi aur reference na ho to
garbage collected ho jata hai. Ye `lst.clear()` se alag hai (jo variable ko rakhta hai, sirf empty karta hai).
"""))

# ============================================================================
# 8. sort() vs sorted()
# ============================================================================
cells.append(md(r"""
## 8. `sort()` vs `sorted()`

**Kya hai:** `list.sort()` **in-place** method hai (list hi ka), `sorted()` **built-in function** hai jo
**kisi bhi iterable** par chalta hai aur **naya list** return karta hai.

**Kyun/kahan:** Agar original order preserve karna ho ya iterable list na ho (jaise `set`, `dict`, `str`) — `sorted()`.
Agar list ko permanently sort karna ho, memory bachani ho — `sort()`.
"""))

cells.append(code(r"""
nums = [5, 2, 9, 1]
new_sorted = sorted(nums)          # NAYA list, original untouched
print("sorted():", new_sorted, "| original still:", nums)

nums.sort()                        # IN-PLACE
print("sort():", nums)

# sorted() KISI BHI iterable par kaam karta hai - list, tuple, set, string
print("sorted string:", sorted("dcba"))
print("sorted tuple: ", sorted((3, 1, 2)))
print("sorted set:   ", sorted({3, 1, 2}))
"""))

cells.append(code(r"""
import operator

words = ["banana", "kiwi", "apple", "fig"]
print("key=len:       ", sorted(words, key=len))                 # length ke hisab se
print("key=str.lower: ", sorted(words, key=str.lower))            # case-insensitive
print("key=last char: ", sorted(words, key=lambda w: w[-1]))      # lambda key
print("reverse=True:  ", sorted(words, key=len, reverse=True))    # descending

# MULTI-KEY sort - tuple key: pehle marks descending, phir naam ascending
students = [("Ali", 85), ("Sara", 90), ("Bilal", 85), ("Ayesha", 90)]
print("multi-key (marks desc, naam asc):", sorted(students, key=lambda s: (-s[1], s[0])))

# operator.itemgetter - faster + readable alternative to lambda for simple field access
print("itemgetter(1): ", sorted(students, key=operator.itemgetter(1)))

# STABILITY - equal keys ka RELATIVE ORDER preserve hota hai (Timsort guarantee)
data = [("a", 2), ("b", 1), ("c", 2), ("d", 1)]
print("stable sort:   ", sorted(data, key=lambda x: x[1]))   # b,d (1) phir a,c (2) - insertion order preserved
"""))

cells.append(code(r"""
# Sorting list of DICTS by a field
people = [{"name": "Ali", "age": 30}, {"name": "Sara", "age": 25}]
print("dicts by age:", sorted(people, key=lambda p: p["age"]))

# Sorting DICT ITEMS by value - top-N pattern
scores = {"Ali": 80, "Sara": 95, "Bilal": 70, "Ayesha": 88}
top2 = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:2]
print("top 2 scorers:", top2)

# TypeError - incomparable types ko sort NAHI kar sakte
try:
    sorted([1, "two", 3])
except TypeError as e:
    print("TypeError (mixed types):", e)

# functools.cmp_to_key - purane C-style comparator (a-b) ko key function me convert karta hai
from functools import cmp_to_key
def compare(a, b):
    return a - b   # negative -> a pehle, positive -> b pehle, 0 -> barabar
print("cmp_to_key:", sorted([3, 1, 2], key=cmp_to_key(compare)))
"""))

cells.append(md(r"""
**Output ka matlab:** `key=` function har element par **ek dafa** apply hota hai (result cache hota hai internally) —
isliye `key=` `cmp=`-style comparator se zyada efficient hai. Stability ka matlab: agar do elements ka key
barabar hai to unka relative order **wahi rahega** jo input me tha.

**Common mistakes:**
- `sorted(my_list)` ke baad `my_list` khud **sort nahi hota** (naya list alag variable me store karna padega).
- `my_list.sort()` `None` return karta hai — `x = my_list.sort()` likh kar `x` use karna bug hai.
- Incomparable types (`int` vs `str`) sort karne par `TypeError` — mixed-type lists sort karne se pehle normalize karo.

**Interview tip:** "Python ka sort algorithm kya hai?" → **Timsort** (merge sort + insertion sort hybrid),
worst case O(n log n), **stable**, best case O(n) (already sorted data par).
"""))

# ============================================================================
# 9. LIST COMPREHENSIONS
# ============================================================================
cells.append(md(r"""
## 9. List Comprehensions

**Kya hai:** Ek line me naya list banane ka concise syntax — loop + condition ko expression me compress karta hai.

**Syntax:** `[expr for item in iterable if condition]`
"""))

cells.append(code(r"""
# Basic comprehension
squares = [x**2 for x in range(6)]
print("basic:", squares)

# with if FILTER
evens = [x for x in range(20) if x % 2 == 0]
print("filter:", evens)

# MULTIPLE if conditions - dono AND ki tarah kaam karte hain
multiples = [x for x in range(50) if x % 2 == 0 if x % 5 == 0]
print("multiple if:", multiples)

# if-else TERNARY in the expression part (note: yahan 'else' zaroori hai, filter wala 'if' alag hai)
labels = ["even" if x % 2 == 0 else "odd" for x in range(6)]
print("ternary expr:", labels)
"""))

cells.append(code(r"""
# NESTED LOOPS in a comprehension - order same hota hai jaise normal nested for loop
pairs = [(x, y) for x in range(3) for y in range(2)]
print("nested loops:", pairs)
# equivalent to:
#   for x in range(3):
#       for y in range(2):
#           pairs.append((x, y))

# comprehension over NESTED LIST - flatten karna
nested = [[1, 2, 3], [4, 5], [6]]
flat = [item for row in nested for item in row]   # bahar wala loop pehle (row), andar wala baad me (item)
print("flatten:", flat)
"""))

cells.append(code(r"""
import time

# Comprehension vs map/filter vs plain loop - readability + chhota perf comparison
N = 20000

start = time.perf_counter()
r1 = [x * 2 for x in range(N)]
t1 = time.perf_counter() - start

start = time.perf_counter()
r2 = list(map(lambda x: x * 2, range(N)))
t2 = time.perf_counter() - start

start = time.perf_counter()
r3 = []
for x in range(N):
    r3.append(x * 2)
t3 = time.perf_counter() - start

print("results match:", r1 == r2 == r3)
print(f"comprehension: {t1:.5f}s | map+lambda: {t2:.5f}s | plain loop: {t3:.5f}s")
# aam tor par: comprehension >= map (map me lambda call overhead hota hai), dono loop se tez hote hain
"""))

cells.append(md(r"""
**Kab comprehension use NAHI karni chahiye:** Jab expression ka result use hi nahi hona (sirf **side effect**
chahiye, jaise printing ya kisi dict me insert karna) — comprehension wahan **anti-pattern** hai, memory bhi
waste hoti hai (ek throwaway list ban jati hai) aur readability bhi kharab hoti hai.
"""))

cells.append(code(r"""
# BAD practice - comprehension sirf side-effect (print) ke liye use karna
throwaway = [print(x) for x in range(3)]   # ye [None, None, None] banata hai - result kabhi use nahi hoga
print("throwaway result (wasteful):", throwaway)

# GOOD - jab sirf side effect chahiye, simple loop use karo
for x in range(3):
    pass   # yahan asal me print(x) ya koi side-effect karte, comprehension nahi
print("plain loop is the right tool for side-effects only")
"""))

cells.append(code(r"""
# LEAKING VARIABLE behaviour - Python 2 me list comprehension ka loop variable
# enclosing scope me LEAK ho jata tha. Python 3 me comprehension ka apna scope hota hai.
x = "before comprehension"
squares_leak_test = [x for x in range(3)]
print("x after comprehension (Py3 - NO leak, comp has own scope):", x)
"""))

cells.append(code(r"""
import sys

# GENERATOR EXPRESSION vs LIST COMPREHENSION - memory difference
list_comp = [x for x in range(10000)]      # () ki jagah [] - pura list memory me banta hai
gen_expr = (x for x in range(10000))       # () - lazy, ek time par ek value

print("list comprehension size (bytes):", sys.getsizeof(list_comp))
print("generator expression size (bytes):", sys.getsizeof(gen_expr))   # bohat chhota - values store nahi hotin

print("sum via generator (consumes it once):", sum(gen_expr))
try:
    next(gen_expr)   # generator ek dafa consume hone ke baad khatam ho jata hai
except StopIteration:
    print("generator exhausted after use - can't reuse")
"""))

cells.append(code(r"""
# NESTED comprehension - matrix banana (row-major, r*3+c pattern)
matrix = [[r * 3 + c for c in range(3)] for r in range(3)]
print("matrix via nested comprehension:")
for row in matrix:
    print(row)
"""))

# ============================================================================
# 10. 2D LISTS / MATRICES
# ============================================================================
cells.append(md(r"""
## 10. 2D Lists / Matrices

**Kya hai:** List ke andar lists — rows ka collection. `grid[r][c]` se access.

**GOTCHA (bohat common bug):** `[[0]*3]*3` teenon rows **SAME inner list object** ki taraf point karti hain!
"""))

cells.append(code(r"""
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("grid[1][2] (row 1, col 2):", grid[1][2])   # 6

print("row-wise iteration:")
for row in grid:
    print(row)

print("index-based iteration:")
for r in range(len(grid)):
    for c in range(len(grid[0])):
        print(grid[r][c], end=" ")
print()
"""))

cells.append(code(r"""
# THE TRAP: [[0]*3]*3 - 3 references to the SAME inner list
trap = [[0] * 3] * 3
trap[0][0] = 99
print("trap - mutation LEAKS to all rows (WRONG):", trap)   # sab rows badal gayi!
print("are rows the same object?", trap[0] is trap[1])       # True - yehi bug ki wajah hai

# CORRECT way - comprehension har row ke liye NAYA object banati hai
correct = [[0] * 3 for _ in range(3)]
correct[0][0] = 99
print("correct - only row 0 changed:", correct)
print("are rows the same object?", correct[0] is correct[1])   # False - alag objects
"""))

cells.append(code(r"""
# Same trap ek list of lists par bhi - * operator SHALLOW repeat karta hai (references copy hoti hain)
row_template = [1, 2]
bad_matrix = [row_template] * 3      # teenon entries same object
bad_matrix[0].append(999)
print("bad_matrix (all rows affected):", bad_matrix)

good_matrix = [row_template.copy() for _ in range(3)]   # copy() se alag objects
good_matrix[0].append(888)
print("good_matrix (only row 0 affected):", good_matrix)
"""))

cells.append(code(r"""
# Row sums, column sums, transpose
sales_data = [[100, 200, 300], [50, 60, 70], [10, 20, 30]]

row_sums = [sum(row) for row in sales_data]
col_sums = [sum(col) for col in zip(*sales_data)]   # zip(*matrix) columns ko group karta hai
print("row sums:", row_sums)
print("col sums:", col_sums)

# Transpose - do tareeqe
transposed_comp = [[sales_data[r][c] for r in range(len(sales_data))] for c in range(len(sales_data[0]))]
transposed_zip = [list(col) for col in zip(*sales_data)]   # zip(*m) - idiomatic transpose trick
print("transpose (comprehension):", transposed_comp)
print("transpose (zip(*m)):      ", transposed_zip)
print("dono same?", transposed_comp == transposed_zip)
"""))

cells.append(md(r"""
**Output ka matlab:** `zip(*matrix)` matrix ki rows ko "unpack" kar ke unhe parallel iterate karta hai — column 0
ke saare elements, phir column 1 ke, waghera. Ye transpose ka **sabse Pythonic** tareeqa hai.

**Interview tip:** `[[0]*3]*3` trap **bohat frequently** interview me poocha jata hai — "is code me bug kya hai"
type question. Hamesha `[[0]*cols for _ in range(rows)]` pattern yaad rakho.
"""))

# ============================================================================
# 11. COPY SEMANTICS
# ============================================================================
cells.append(md(r"""
## 11. Copy Semantics — Alias vs Shallow vs Deep Copy

**Kya hai:**
- **Alias** (`b = a`) — dono naam **same object** ki taraf point karte hain.
- **Shallow copy** — naya top-level object banta hai, lekin **nested/inner objects same reference** rehte hain.
- **Deep copy** — naya object + saare nested objects bhi **recursively naye** ban jate hain.
"""))

cells.append(code(r"""
import copy

original_list = [1, 2, [3, 4]]        # aakhri element ek nested list hai
alias_list = original_list             # ALIAS - same object
shallow1 = original_list.copy()        # SHALLOW copy method
shallow2 = list(original_list)         # SHALLOW via list()
shallow3 = original_list[:]            # SHALLOW via slice
shallow4 = copy.copy(original_list)    # SHALLOW via copy module
deep = copy.deepcopy(original_list)    # DEEP copy - nested bhi naya

print("alias is original?          ", alias_list is original_list)      # True
print("shallow1 is original?       ", shallow1 is original_list)         # False (naya top-level)
print("shallow1[2] is original[2]? ", shallow1[2] is original_list[2])   # True (SAME nested list!)
print("deep[2] is original[2]?     ", deep[2] is original_list[2])       # False (deep me nested bhi naya)
"""))

cells.append(code(r"""
# Ab original ki nested list mutate karte hain aur dekhte hain kya effect hota hai
original_list[2].append(999)

print("original:        ", original_list)
print("shallow1 (nested CHANGED too - shared reference!):", shallow1)
print("deep (unaffected - completely independent):        ", deep)

print("id(original_list):", id(original_list))
print("id(shallow1):     ", id(shallow1), "(different top-level object)")
"""))

cells.append(md(r"""
**Common mistakes:** Log samajhte hain ke `.copy()` / `[:]` "poori tarah independent copy" banati hai — lekin
agar list ke andar mutable objects (list, dict) hain, wo **share** hote hain. Nested mutable data ke liye
`copy.deepcopy()` chahiye.

**Interview tip:** Deep copy **costly** hoti hai (poora object graph traverse karti hai) — sirf tab use karo
jab nested mutable data ko truly independent rakhna zaroori ho. Flat lists (sirf int/str) ke liye shallow copy hi kaafi hai.
"""))

# ============================================================================
# 12. UNPACKING
# ============================================================================
cells.append(md(r"""
## 12. Unpacking

**Kya hai:** List/tuple ke elements ko ek sath multiple variables me "unpack" karna.

**Syntax:** `a, b, c = [1, 2, 3]`, starred `*rest` remaining elements collect karta hai.
"""))

cells.append(code(r"""
# Basic unpacking
a, b, c = [1, 2, 3]
print("basic:", a, b, c)

# Starred target - remaining elements ek list me
first, *rest = [1, 2, 3, 4, 5]
print("first, *rest:", first, rest)

*init, last = [1, 2, 3, 4, 5]
print("*init, last:", init, last)

first2, *mid, last2 = [1, 2, 3, 4, 5]
print("first, *mid, last:", first2, mid, last2)

# Nested unpacking
(x1, x2), y = [(1, 2), 3]
print("nested:", x1, x2, y)
"""))

cells.append(code(r"""
# Swapping - tuple packing/unpacking ke zariye, temp variable ki zaroorat nahi
p, q = 10, 20
p, q = q, p
print("swapped:", p, q)

# Unpacking in FUNCTION CALLS
def add3(a, b, c):
    return a + b + c

args = [1, 2, 3]
print("f(*args):", add3(*args))

# * in list LITERALS - merge karna
combined = [*[1, 2], *[3, 4], 5]
print("merged with *:", combined)

# Too many / too few values -> ValueError
try:
    a1, b1 = [1, 2, 3]
except ValueError as e:
    print("too many values ValueError:", e)

try:
    a2, b2, c2 = [1, 2]
except ValueError as e:
    print("too few values ValueError:", e)

# Ignoring values with underscore _ (convention, not special syntax)
_, keep, _ = [1, 2, 3]
print("keep (ignored 1st/3rd with _):", keep)
"""))

cells.append(md(r"""
**Interview tip:** Starred unpacking (`*rest`) sirf **ek dafa** ek assignment me use ho sakta hai — do jagah
`*` lagana `SyntaxError` deta hai. Ye Python 3-only feature hai (PEP 3132).
"""))

# ============================================================================
# 13. MEMBERSHIP & COMPLEXITY
# ============================================================================
cells.append(md(r"""
## 13. Membership (`in`) aur Complexity

**Kya hai:** `x in lst` list ko **linearly scan** karta hai — O(n). `x in some_set` ya `x in some_dict`
hashing use karta hai — average O(1).
"""))

cells.append(code(r"""
import time

big_list = list(range(20000))
big_set = set(big_list)
target = 19999   # worst case - end me hai, poora list scan hoga

start = time.perf_counter()
for _ in range(200):
    _ = target in big_list
t_list = time.perf_counter() - start

start = time.perf_counter()
for _ in range(200):
    _ = target in big_set
t_set = time.perf_counter() - start

print(f"list 'in' time: {t_list:.5f}s")
print(f"set  'in' time: {t_set:.5f}s")
print("set 'in' aam tor par list se kaafi tez hota hai bade data par (O(1) vs O(n))")
"""))

cells.append(md(r"""
### List Operations — Complexity Table

| Operation | Complexity | Note |
|---|---|---|
| `lst[i]` (index) | O(1) | direct memory access |
| `lst.append(x)` | O(1) amortized | end me space usually available |
| `lst.insert(0, x)` | O(n) | baaki sab elements shift karte hain |
| `lst.pop()` | O(1) | last element |
| `lst.pop(0)` | O(n) | baaki sab elements shift karte hain |
| `lst.remove(x)` | O(n) | pehle dhoondhna padta hai |
| `x in lst` | O(n) | linear scan |
| `len(lst)` | O(1) | size cached hoti hai |
| `lst.sort()` | O(n log n) | Timsort |
| `lst[a:b]` (slice) | O(k) | k = slice ki length |

**`collections.deque`** — agar dono ends se frequently insert/delete karna ho (queue-like use case),
`deque` use karo — `appendleft`/`popleft` O(1) hote hain (list ke O(n) ke muqable).
"""))

cells.append(code(r"""
from collections import deque

dq = deque([1, 2, 3])
dq.appendleft(0)     # O(1) - list ke insert(0, ...) ki tarah O(n) NAHI
dq.append(4)         # O(1)
print("deque:", dq)
dq.popleft()          # O(1)
print("after popleft:", dq)
"""))

# ============================================================================
# 14. OTHER USEFUL BUILT-INS
# ============================================================================
cells.append(md(r"""
## 14. Other Useful Built-ins on Sequences

`min/max` (with `key`), `sum`, `any/all`, `enumerate`, `zip`, `reversed`, aur `itertools` teasers.
"""))

cells.append(code(r"""
nums = [5, -2, 9, 3, -8]

print("min:", min(nums), "| max:", max(nums))
print("min by abs value (key=):", min(nums, key=abs))
print("sum:", sum(nums))
print("any negative?", any(n < 0 for n in nums))
print("all positive?", all(n > 0 for n in nums))
print("sorted:", sorted(nums))
print("reversed (as list):", list(reversed(nums)))

for i, v in enumerate(nums, start=1):     # start=1 se index 1 se ginti
    print(f"  #{i}: {v}")

names = ["Ali", "Sara"]
ages = [30, 25]
print("zip:", list(zip(names, ages)))     # parallel iteration, shortest input tak

print("list repeat via *:", [1, 2] * 3)   # list.__mul__
"""))

cells.append(code(r"""
from itertools import chain, islice, accumulate

print("chain (flatten multiple iterables):", list(chain([1, 2], [3, 4])))
print("islice (lazy slice on any iterable):", list(islice(range(100), 5)))
print("accumulate (running totals):", list(accumulate([1, 2, 3, 4])))
"""))

# ============================================================================
# 15. TUPLES
# ============================================================================
cells.append(md(r"""
## 15. Tuples

**Kya hai:** `tuple` bhi ordered collection hai lekin **immutable** — ek dafa banne ke baad content change
nahi ho sakta.

**Kyun/kahan:** Fixed data (jaise coordinates, RGB values), dict keys/set members (hashable chahiye),
function se multiple values return karna, ya jab data accidentally mutate na ho ye guarantee chahiye.
"""))

cells.append(code(r"""
t1 = (1, 2, 3)             # parentheses ke sath
t2 = 1, 2, 3                # parentheses OPTIONAL - ye bhi "packing" hai
t3 = tuple([1, 2, 3])       # list se convert
t_empty = ()                 # empty tuple

single = (5,)                 # SINGLE-ELEMENT tuple - trailing comma ZAROORI hai
not_tuple = (5)                # ye sirf int 5 hai - parentheses yahan grouping hain, tuple nahi!

print("t1:", t1, type(t1))
print("t2 (no parens):", t2, type(t2))
print("t3 (from list):", t3, type(t3))
print("t_empty:", t_empty, type(t_empty))
print("single (5,):", single, type(single))         # <class 'tuple'>
print("not_tuple (5):", not_tuple, type(not_tuple))   # <class 'int'> - GOTCHA!
"""))

cells.append(code(r"""
# IMMUTABILITY - element assign karne par TypeError
tup = (1, 2, 3)
try:
    tup[0] = 99
except TypeError as e:
    print("TypeError (tuple immutable):", e)

# LEKIN agar tuple ke andar MUTABLE object ho (jaise list), wo khud change ho sakta hai
tup_with_list = ([1, 2], [3, 4])
tup_with_list[0].append(99)     # tuple ka slot 0 wahi list object hai - us list ko mutate kiya, tuple ko nahi
print("tuple containing mutable list:", tup_with_list)
"""))

cells.append(code(r"""
# + aur * NAYE tuples banate hain (concat / repeat)
tA = (1, 2) + (3, 4)
tB = (1, 2) * 3
print("concat (+):", tA)
print("repeat (*):", tB)

# Tuple methods - SIRF do hain: count() aur index() (list ke muqable bohat kam, immutable hone ki wajah se)
t = (1, 2, 3, 2, 1)
print("count(2):", t.count(2))
print("index(2):", t.index(2))
try:
    t.index(100)
except ValueError as e:
    print("index() ValueError:", e)

# Indexing/slicing - list jaisa hi
t_seq = (10, 20, 30, 40, 50)
print("t_seq[0]:", t_seq[0], "| t_seq[-1]:", t_seq[-1], "| t_seq[1:3]:", t_seq[1:3], "| reversed:", t_seq[::-1])
"""))

cells.append(code(r"""
# Packing/unpacking + returning MULTIPLE VALUES from a function - tuple ka sabse common real use
def min_max(values):
    return min(values), max(values)   # PACKING - implicitly ek tuple return ho raha hai

lo, hi = min_max([3, 1, 4, 1, 5])      # UNPACKING
print("min:", lo, "| max:", hi)

# Tuple COMPARISON - lexicographic (element by element, list jaisi)
print("(1,2,3) < (1,2,4)?", (1, 2, 3) < (1, 2, 4))     # True - 3rd element compare hua
print("(1,2)   < (1,2,3)?", (1, 2) < (1, 2, 3))          # True - shorter jo prefix match kare, chhota hai
print("('a',)  < ('b',)?", ("a",) < ("b",))                # True - string comparison jaisa
"""))

cells.append(code(r"""
# HASHABILITY - tuple dict keys ya set members ban sakta hai (list NAHI ban sakti)
locations = {(0, 0): "origin", (1, 1): "corner"}
print("dict with tuple keys:", locations[(0, 0)])

coord_set = {(1, 2), (3, 4), (1, 2)}   # duplicate automatically drop
print("set of tuples:", coord_set)

# LEKIN agar tuple ke andar UNHASHABLE object ho (list), tuple khud unhashable ban jata hai
try:
    bad_key = {([1, 2],): "x"}      # tuple containing a list -> TypeError
except TypeError as e:
    print("TypeError (tuple containing list is unhashable):", e)
"""))

cells.append(code(r"""
# namedtuple - readable, field-named tuples (immutable + memory efficient)
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print("namedtuple access:", p.x, p.y, "| by index:", p[0], p[1])
print("repr:", p)

# typing.NamedTuple - class-based syntax, type hints ke sath (modern alternative)
from typing import NamedTuple

class PointT(NamedTuple):
    x: int
    y: int

p2 = PointT(3, 4)
print("typing.NamedTuple:", p2.x, p2.y, p2)
"""))

cells.append(code(r"""
import sys, time

# Memory: tuple usually list se thodi kam memory leti hai (fixed size, no over-allocation)
lst_ = [1, 2, 3, 4, 5]
tup_ = (1, 2, 3, 4, 5)
print("list size (bytes):", sys.getsizeof(lst_))
print("tuple size (bytes):", sys.getsizeof(tup_))

# Creation speed - tuple literals aam tor par thodi tezi se bante hain (list ki growth logic nahi)
N = 100000
start = time.perf_counter()
for _ in range(N):
    x = [1, 2, 3]
t_list_create = time.perf_counter() - start

start = time.perf_counter()
for _ in range(N):
    x = (1, 2, 3)
t_tuple_create = time.perf_counter() - start
print(f"list create: {t_list_create:.5f}s | tuple create: {t_tuple_create:.5f}s")
"""))

cells.append(md(r"""
### Tuple vs List — Decision Table

| Criteria | List | Tuple |
|---|---|---|
| Mutable? | Haan | Nahi |
| Hashable (dict key/set member)? | Nahi | Haan (agar andar sab hashable ho) |
| Memory | Thodi zyada | Thodi kam |
| Use case | Data jo grow/shrink/modify ho | Fixed record (coords, RGB), function se multiple return |
| Methods | Bohat saare | Sirf `count`, `index` |
| Semantic signal | "ye badlega" | "ye fixed hai, safe hai" |

**Interview tip:** "Tuple immutable hai to fast/hashable kyun hota hai?" — kyunki content fix hone ki
guarantee ki wajah se Python **hash value cache/compute** kar sakta hai reliably, aur memory allocation
bhi upfront exact size ki hoti hai (list extra capacity rakhti hai future growth ke liye).
"""))

# ============================================================================
# COMMON MISTAKES / GOTCHAS (dedicated section)
# ============================================================================
cells.append(md(r"""
## Common Mistakes / Gotchas — Recap + Ek Aur Classic

Upar jitne bhi gotchas dekhe (mutable default `[x]*n`, `append` vs `extend`, `sort()` returns `None`,
`[[0]*3]*3` trap, shallow vs deep copy, single-element tuple comma) — un sab ka ek aur bohat famous cousin
hai: **mutable default argument**.
"""))

cells.append(code(r"""
# GOTCHA: mutable default argument - default list SIRF EK BAAR banti hai (function definition time par),
# aur function calls ke beech SHARE hoti hai!
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print("call 1:", add_item("apple"))
print("call 2:", add_item("banana"))   # basket khali NAHI hai - purani state persist ho gayi!

# FIX: default None rakho, andar naya list banao
def add_item_correct(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print("fixed call 1:", add_item_correct("apple"))
print("fixed call 2:", add_item_correct("banana"))   # har call apni fresh list leti hai
"""))

# ============================================================================
# REAL-WORLD PROBLEMS
# ============================================================================
cells.append(md(r"""
## Real-World Problems

6 realistic problems jo lists/tuples ke concepts ko combine karte hain.
"""))

cells.append(md(r"""
### 1. Student Marks Report — top-N multi-key sort + averages
"""))

cells.append(code(r"""
students_data = [
    {"name": "Ali", "marks": [80, 90, 70]},
    {"name": "Sara", "marks": [95, 85, 90]},
    {"name": "Bilal", "marks": [70, 75, 65]},
    {"name": "Ayesha", "marks": [95, 80, 85]},
]

for s in students_data:
    s["average"] = sum(s["marks"]) / len(s["marks"])   # har student ka average nikalo

# Rank: average descending, tie-break naam ascending (multi-key sort via tuple key)
ranked = sorted(students_data, key=lambda s: (-s["average"], s["name"]))

print("Rank Report:")
for rank, s in enumerate(ranked, start=1):
    print(f"  {rank}. {s['name']:8s} avg={s['average']:.2f}")
"""))

cells.append(md(r"""
### 2. Shopping Cart Total + Discount
"""))

cells.append(code(r"""
# cart: list of tuples (name, price, qty)
cart = [("Pen", 10, 5), ("Notebook", 50, 2), ("Bag", 500, 1)]

subtotal = sum(price * qty for _, price, qty in cart)   # unpacking tuple in comprehension
discount = 0.10 if subtotal > 500 else 0.0
total = subtotal * (1 - discount)

print(f"Subtotal: {subtotal} | Discount: {discount * 100:.0f}% | Total: {total:.2f}")
"""))

cells.append(md(r"""
### 3. CSV-ish Rows → Sorted Table (f-string alignment)
"""))

cells.append(code(r"""
rows = [
    "Ali,30,Lahore",
    "Sara,25,Karachi",
    "Bilal,35,Islamabad",
]

parsed = [r.split(",") for r in rows]                        # split -> list of lists
parsed_sorted = sorted(parsed, key=lambda r: int(r[1]))        # age (string) -> int -> sort

print(f"{'Name':10s}{'Age':5s}{'City':12s}")
for name, age, city in parsed_sorted:
    print(f"{name:10s}{age:5s}{city:12s}")
"""))

cells.append(md(r"""
### 4. Matrix Operations — Sales Grid Transpose + Totals
"""))

cells.append(code(r"""
# rows = regions, cols = months
sales_grid = [[120, 340, 210], [90, 150, 200], [300, 100, 50]]

region_totals = [sum(r) for r in sales_grid]
month_totals = [sum(c) for c in zip(*sales_grid)]
transposed = [list(c) for c in zip(*sales_grid)]

print("region totals:", region_totals)
print("month totals: ", month_totals)
print("transposed (months as rows):", transposed)
"""))

cells.append(md(r"""
### 5. Deduplicate While Preserving Order + Frequency Ranking
"""))

cells.append(code(r"""
words_list = ["apple", "banana", "apple", "cherry", "banana", "apple", "date"]

# Dedup preserving FIRST-seen order
seen = set()
deduped = []
for w in words_list:
    if w not in seen:
        seen.add(w)
        deduped.append(w)
print("deduped (order preserved):", deduped)

# Frequency ranking
from collections import Counter
freq = Counter(words_list)
freq_ranked = sorted(freq.items(), key=lambda kv: -kv[1])
print("frequency ranking (most common first):", freq_ranked)
"""))

cells.append(md(r"""
### 6. Seating Grid Problem (2D list use case)
"""))

cells.append(code(r"""
rows_n, cols_n = 3, 4
seats = [["Empty" for _ in range(cols_n)] for _ in range(rows_n)]   # safe 2D init (no shared-reference trap)

bookings = [(0, 0), (1, 2), (2, 3)]
for r, c in bookings:
    seats[r][c] = "Booked"

print("Seating chart:")
for row in seats:
    print(row)

available = sum(row.count("Empty") for row in seats)
print("Available seats:", available)
"""))

# ============================================================================
# LEETCODE
# ============================================================================
cells.append(md(r"""
## LeetCode Problems (Easy)

In sab problems ka common thread: **two-pointer pattern** (ek slow, ek fast pointer, in-place array modification).
"""))

cells.append(md(r"""
### LC 26. Remove Duplicates from Sorted Array — Easy
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

**Bayan:** Ek sorted array `nums` diya hai — duplicates ko in-place remove karo, taake har unique element
sirf ek dafa aaye, aur unique elements ki count `k` return karo (array ka pehla `k` hissa unique, sorted hona chahiye).

**Approach:** Two-pointer — `slow` next unique position track karta hai, `fast` har element scan karta hai.
Jab `nums[fast] != nums[slow]` (naya unique element mila), `slow` aage badhao aur `nums[fast]` ko wahan copy karo.

**Time:** O(n) — ek pass. **Space:** O(1) — in-place, no extra array.
"""))

cells.append(code(r"""
def remove_duplicates(nums):
    # two-pointer: slow index jahan next unique element jayega
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1   # k = unique elements ki count

nums1 = [1, 1, 2]
k1 = remove_duplicates(nums1)
assert k1 == 2
assert nums1[:k1] == [1, 2]

nums2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k2 = remove_duplicates(nums2)
assert k2 == 5
assert nums2[:k2] == [0, 1, 2, 3, 4]

print("LC 26 passed:", nums1[:k1], nums2[:k2])
"""))

cells.append(md(r"""
### LC 27. Remove Element — Easy
https://leetcode.com/problems/remove-element/

**Bayan:** Array `nums` aur ek `val` diya hai — `val` ke saare occurrences in-place remove karo aur naya
length `k` return karo (order matter nahi karta).

**Approach:** Two-pointer — `slow` next "keep" position, `fast` scan karta hai. Jab `nums[fast] != val`,
usko `slow` position par copy karo aur `slow` badhao.

**Time:** O(n). **Space:** O(1).
"""))

cells.append(code(r"""
def remove_element(nums, val):
    # slow = agle "valid" element ki position, fast = scanning pointer
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow

nums3 = [3, 2, 2, 3]
k3 = remove_element(nums3, 3)
assert k3 == 2
assert sorted(nums3[:k3]) == [2, 2]

nums4 = [0, 1, 2, 2, 3, 0, 4, 2]
k4 = remove_element(nums4, 2)
assert k4 == 5
assert sorted(nums4[:k4]) == [0, 0, 1, 3, 4]

print("LC 27 passed")
"""))

cells.append(md(r"""
### LC 88. Merge Sorted Array — Easy
https://leetcode.com/problems/merge-sorted-array/

**Bayan:** `nums1` (length `m+n`, pehle `m` elements valid) aur `nums2` (length `n`) dono sorted hain —
`nums2` ko `nums1` me merge karo taake `nums1` sorted ho jaye, in-place.

**Approach (optimal):** **Backwards two-pointer** — end se fill karo (`i=m-1`, `j=n-1`, `k=m+n-1`) taake
`nums1` ke valid elements overwrite hone se pehle hi use ho jayen. Naive approach: slice-assign + `sort()`
(simpler, lekin O((m+n) log(m+n))).

**Time:** optimal O(m+n), naive O((m+n) log(m+n)). **Space:** O(1) optimal (in-place, no sort needed).
"""))

cells.append(code(r"""
def merge_naive(nums1, m, nums2, n):
    # simple: nums2 ko tail me copy karo, phir poora sort kar do
    nums1[m:m + n] = nums2[:n]
    nums1.sort()
    return nums1

def merge_two_pointer(nums1, m, nums2, n):
    # backwards two-pointer - end se fill karo taake overwrite na ho
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    return nums1

a1 = [1, 2, 3, 0, 0, 0]
merge_two_pointer(a1, 3, [2, 5, 6], 3)
assert a1 == [1, 2, 2, 3, 5, 6]

a2 = [1, 2, 3, 0, 0, 0]
merge_naive(a2, 3, [2, 5, 6], 3)
assert a2 == [1, 2, 2, 3, 5, 6]

a3 = [0]
merge_two_pointer(a3, 0, [1], 1)
assert a3 == [1]

print("LC 88 passed")
"""))

cells.append(md(r"""
### LC 283. Move Zeroes — Easy
https://leetcode.com/problems/move-zeroes/

**Bayan:** Array `nums` me saare zeroes end me le jao, non-zero elements ka relative order preserve karte
hue — in-place, extra array nahi.

**Approach:** Two-pointer — `slow` next non-zero slot track karta hai, `fast` scan karta hai. Jab
non-zero mile, `slow` aur `fast` ko swap karo.

**Time:** O(n). **Space:** O(1).
"""))

cells.append(code(r"""
def move_zeroes(nums):
    slow = 0   # next non-zero ki position
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]   # swap karo (in-place, no temp list)
            slow += 1
    return nums

b1 = [0, 1, 0, 3, 12]
move_zeroes(b1)
assert b1 == [1, 3, 12, 0, 0]

b2 = [0]
move_zeroes(b2)
assert b2 == [0]

print("LC 283 passed")
"""))

cells.append(md(r"""
### LC 1480. Running Sum of 1d Array — Easy
https://leetcode.com/problems/running-sum-of-1d-array/

**Bayan:** Array `nums` ka running sum return karo — `runningSum[i] = sum(nums[0..i])`.

**Approach:** In-place prefix sum — har index par pichle index ki value add karo. `itertools.accumulate`
bhi yehi kaam ek built-in ke zariye karta hai (naya list return karta hai).

**Time:** O(n). **Space:** O(1) in-place version, O(n) accumulate version (naya list return karta hai).
"""))

cells.append(code(r"""
from itertools import accumulate

def running_sum_inplace(nums):
    # prefix sum - har element me pichla accumulated total add karo
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]
    return nums

def running_sum_accumulate(nums):
    return list(accumulate(nums))   # built-in - same result, naya list

c1 = [1, 2, 3, 4]
assert running_sum_inplace(c1[:]) == [1, 3, 6, 10]      # c1[:] copy pass ki taake original safe rahe
assert running_sum_accumulate([1, 2, 3, 4]) == [1, 3, 6, 10]
assert running_sum_inplace([1, 1, 1, 1, 1]) == [1, 2, 3, 4, 5]

print("LC 1480 passed")
"""))

cells.append(md(r"""
### LC 1929. Concatenation of Array — Easy
https://leetcode.com/problems/concatenation-of-array/

**Bayan:** Array `nums` (length n) ka ek naya array `ans` (length 2n) banao jahan `ans[i] = ans[i+n] = nums[i]`.

**Approach:** `nums + nums` sabse simple (Python `+` naya list concat karta hai). Manual loop se bhi
same result index-by-index bana sakte hain.

**Time:** O(n) dono. **Space:** O(n) (output array khud hi O(n) extra hai — requirement ka hissa hai).
"""))

cells.append(code(r"""
def get_concatenation_builtin(nums):
    return nums + nums   # + operator naya concatenated list banata hai

def get_concatenation_manual(nums):
    n = len(nums)
    ans = [0] * (2 * n)
    for i in range(n):
        ans[i] = nums[i]
        ans[i + n] = nums[i]
    return ans

d1 = [1, 2, 1]
assert get_concatenation_builtin(d1) == [1, 2, 1, 1, 2, 1]
assert get_concatenation_manual(d1) == [1, 2, 1, 1, 2, 1]

print("LC 1929 passed")
"""))

cells.append(md(r"""
**Common thread across all 6:** Sab me **two-pointer / index-tracking** pattern hai — ek pointer "write position"
track karta hai, doosra "scan/read position". Ye pattern array-in-place-modification questions ka backbone hai —
interview me isko pehchan lo to naya problem bhi jaldi solve ho jata hai.
"""))

# ============================================================================
# INTERVIEW Q&A
# ============================================================================
cells.append(md(r"""
## Interview Questions & Answers

1. **List aur tuple me basic farq?**
   List mutable hai, tuple immutable. List ke methods zyada hain, tuple hashable hai (dict key/set member ban sakta hai).

2. **`sort()` aur `sorted()` me farq?**
   `sort()` list ka in-place method hai, `None` return karta hai. `sorted()` built-in function hai, kisi bhi
   iterable par chalta hai, naya list return karta hai.

3. **`append()` aur `extend()` me farq?**
   `append(x)` `x` ko ek single element ki tarah end me daalta hai (nested ho sakta hai). `extend(iterable)`
   iterable ke elements ko ek-ek karke add karta hai (flatten).

4. **`[[0]*3]*3` me kya bug hai?**
   Teenon rows same inner list object ki taraf point karti hain — ek row mutate karne se sab badalti hain.
   Fix: `[[0]*3 for _ in range(3)]`.

5. **Shallow copy aur deep copy me farq?**
   Shallow copy naya top-level object banati hai lekin nested mutable objects same reference share karte hain.
   Deep copy poore object graph ko recursively copy karti hai.

6. **List ke andar `(5)` aur `(5,)` me farq?**
   `(5)` sirf int `5` hai (parentheses grouping). `(5,)` ek single-element tuple hai — trailing comma zaroori.

7. **Tuple immutable hone ke bawajood usme mutable object kaise change ho sakta hai?**
   Tuple sirf apne **slots ke references** ko immutable rakhta hai — agar slot ek mutable object (list) point
   karta hai, wo object khud mutate ho sakta hai (tuple ka reference wahi rehta hai).

8. **`lst[:] = other` aur `lst = other` me farq?**
   Pehla existing object ko in-place modify karta hai (saare aliases update hote hain). Doosra sirf variable
   ko naye object se rebind karta hai (aliases purane object par hi rehte hain).

9. **List me membership check (`in`) ki complexity kya hai, aur set/dict se kaise behtar/kamzor hai?**
   List me O(n) (linear scan). Set/dict me average O(1) (hashing) — lekin set ordering guarantee nahi karta,
   aur elements hashable hone chahiye.

10. **`del`, `pop()`, aur `remove()` me farq?**
    `del lst[i]` statement hai, kuch return nahi karta, index/slice/poora variable delete kar sakta hai.
    `pop(i)` value return karta hai (index se). `remove(v)` value se dhoondh kar pehla match hatata hai.

11. **List comprehension vs generator expression?**
    Comprehension `[]` poori list memory me bana deta hai. Generator `()` lazy hota hai, ek time par ek value —
    bade data ya one-time iteration ke liye memory-efficient.

12. **Mutable default argument gotcha kya hai?**
    `def f(x, lst=[])` — default list function definition time par **ek dafa** banti hai aur calls ke beech
    share hoti hai. Fix: `lst=None` phir andar `if lst is None: lst = []`.

13. **Tuple dict key kyun ban sakta hai lekin list nahi?**
    Dict keys **hashable** honi chahiye. Tuple immutable hai (agar andar sab elements bhi hashable hon) —
    is liye hash value consistent rehta hai. List mutable hai, is liye unhashable.

14. **`zip(*matrix)` kya karta hai?**
    Matrix (list of lists/rows) ko unpack kar ke columns ko parallel group karta hai — matrix transpose
    karne ka idiomatic tareeqa.

15. **Python me sort algorithm kaunsa hai, aur stable kyun important hai?**
    **Timsort** — merge sort + insertion sort hybrid, worst case O(n log n), **stable** (equal keys ka
    relative order preserve karta hai) — ye multi-pass sorting (pehle secondary key, phir primary key) ke
    liye zaroori hota hai.
"""))

# ============================================================================
# PRACTICE EXERCISES
# ============================================================================
cells.append(md(r"""
## Practice Exercises (khud karo)

1. Ek list `[5, 3, 8, 1, 9, 2]` di gayi hai. `sorted()` use kar ke descending order me sort karo bina
   original list ko modify kiye.
   *Hint:* `reverse=True` parameter.

2. Ek 2D list (3x3 matrix) banao jisme har cell apni `row*10 + col` value store kare, comprehension se.
   *Hint:* nested comprehension `[[... for c in range(3)] for r in range(3)]`.

3. Ek list `[1, 2, 2, 3, 3, 3, 4]` di gayi hai — ek dict banao jisme har unique value ki count ho, phir
   sabse zyada frequent value print karo.
   *Hint:* `collections.Counter` ya manual dict + loop.

4. Do lists `names = ["a","b","c"]` aur `scores = [90, 75, 88]` di gayi hain — `zip` use kar ke ek list of
   tuples banao aur score ke hisab se descending sort karo.
   *Hint:* `zip()` + `sorted(key=lambda t: -t[1])`.

5. Ek function likho jo list ko in-place reverse kare **bina** `.reverse()` method ya slicing use kiye
   (two-pointer swap se).
   *Hint:* `left, right = 0, len(lst)-1` phir swap karte hue aage badho.

6. `[[1,2],[3,4]]` ka deepcopy banao, phir copy ke andar wali list mutate karo aur verify karo original
   affected nahi hua.
   *Hint:* `copy.deepcopy` + `id()` check.

7. Ek tuple `(1, 2, 3)` ko list me convert karo, ek element modify karo, wapas tuple me convert karo.
   *Hint:* `list(t)`, modify, `tuple(...)`.

8. `namedtuple` use kar ke ek `Employee` type banao jisme `name`, `age`, `salary` fields hon — 3 employees
   ki list banao aur salary ke hisab se sort karo.
   *Hint:* `namedtuple("Employee", ["name","age","salary"])`, `sorted(key=lambda e: e.salary)`.
"""))

# ============================================================================
# SUMMARY / CHEAT-SHEET
# ============================================================================
cells.append(md(r"""
## Summary / Cheat-Sheet

**List basics**
- Creation: `[]`, `list()`, `list(range(n))`, `list("abc")`, `[x]*n`
- Mutable, ordered, heterogeneous elements allowed, nesting allowed.

**Indexing/slicing**
- `lst[i]` O(1), negative index from end, `IndexError` on out-of-range.
- `lst[a:b:c]` — new list, `stop` exclusive, no `IndexError` ever.
- Slice assignment: same-length replace, grow, shrink, insert (`lst[i:i]=`), delete (`lst[a:b]=[]`).
  Extended slice (`step!=1`) length must match exactly → `ValueError` otherwise.

**Critical distinction**
- `lst[:] = other` → in-place mutate (aliases see it). `lst = other` → rebind (aliases don't).

**Methods (mutating, return `None`)**: `append`, `extend`, `insert`, `remove`, `pop` (returns value),
`clear`, `sort`, `reverse`. **Non-mutating**: `index`, `count`, `copy`.

**`sort()` vs `sorted()`**: in-place/None vs new-list/any-iterable. `key=`, `reverse=`, stable (Timsort).

**Comprehensions**: `[expr for x in it if cond]`; nested loops flatten order matches nested `for`;
generator `()` for memory-lazy iteration; avoid for side-effects only.

**2D lists**: `[[0]*c for _ in range(r)]` — never `[[0]*c]*r` (shared reference trap). `zip(*m)` = transpose.

**Copy**: alias (`b=a`) shares everything; shallow (`copy()`/`[:]`/`list()`) shares nested mutables;
`copy.deepcopy` fully independent (costly).

**Unpacking**: `a,b,c=lst`; `first,*rest=lst`; swap `a,b=b,a`; `f(*args)`; `[*a,*b]`.

**Complexity**: index/append/len O(1); insert(0)/pop(0)/remove/`in` O(n); sort O(n log n).
Need fast both-ends ops → `collections.deque`.

**Tuples**: immutable, `(x,)` for single-element, hashable (if contents hashable) → dict key/set member,
only `count`/`index` methods, `namedtuple`/`typing.NamedTuple` for named fields, slightly less memory
than list.

**Tuple vs list**: fixed/hashable data → tuple; data that changes → list.

**LeetCode pattern learned**: two-pointer in-place array modification (LC 26, 27, 88, 283) + prefix-sum
and concatenation tricks (LC 1480, 1929).
"""))

save(r"Python/Basics/05_Lists_and_Tuples.ipynb", cells)
