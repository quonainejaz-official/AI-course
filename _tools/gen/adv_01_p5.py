import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code

CELLS = []
A = CELLS.append

A(md("""
---
# LeetCode Problems

Is notebook ke teen problems jaan boojh kar chune gaye hain — teeno **references, identity aur
copying** ke baare me hain, yaani exactly wohi jo hum ne upar seekha:

| # | Problem | Concept jo test hota hai |
|---|---|---|
| 138 | Copy List with Random Pointer | deep copy + `id()` based identity mapping |
| 133 | Clone Graph | reference cycles + visited map (deepcopy ka memo khud banana) |
| 146 | LRU Cache | dict + doubly linked list (cycles!) — cache design |
"""))

A(md("""
### LC 138. Copy List with Random Pointer — Medium

**Link:** https://leetcode.com/problems/copy-list-with-random-pointer/

**Problem (Roman Urdu):** Ek linked list di hai jahan har node ke paas `next` ke ilawa ek
`random` pointer bhi hai jo list ke **kisi bhi** node (ya `None`) ko point kar sakta hai.
Poori list ka **deep copy** banao: naye nodes banao, aur naye nodes ke `random` pointers
**naye** nodes ki taraf ho (purane ki taraf nahi) — structure bilkul same.

**Ye notebook ke topic se kaise juda hai:** Ye asal me `copy.deepcopy` ka `memo` dict
haath se implement karna hai. `old node → new node` mapping wahi "id → copy" idea hai.

**Approach 1 — Hash map (2 passes)**
1. Pass 1: har purane node ke liye naya node banao aur `mapping[old] = new` rakho
   (`Node` hashable hai default identity hash se).
2. Pass 2: `mapping[old].next = mapping.get(old.next)` aur
   `mapping[old].random = mapping.get(old.random)` — `.get` is liye ke `None` safe rahe.

- **Time:** O(n) &nbsp; **Space:** O(n) (mapping)

**Approach 2 — Interleaving (O(1) extra space)**
1. Har original node ke foran baad uska copy ghusa do: `A → A' → B → B' → ...`
2. Ab `A'.random = A.random.next` (kyunki kisi bhi node ka copy uske foran baad hai) — bilkul mapping ke baghair!
3. Do lists ko wapas alag karo (original bhi restore karo).

- **Time:** O(n) &nbsp; **Space:** O(1) extra (output ke ilawa)
"""))

A(code(r"""
class RNode:
    # LeetCode ka 'Node': val + next + random
    __slots__ = ("val", "next", "random")
    def __init__(self, val, next=None, random=None):
        self.val, self.next, self.random = val, next, random

# ---- test helpers: [(val, random_index_or_None), ...] se list banao / wapas pairs nikalo ----
def build_random_list(pairs):
    nodes = [RNode(v) for v, _ in pairs]
    for i, n in enumerate(nodes):
        n.next = nodes[i + 1] if i + 1 < len(nodes) else None
        ridx = pairs[i][1]
        n.random = nodes[ridx] if ridx is not None else None
    return nodes[0] if nodes else None

def to_pairs(head):
    nodes, cur = [], head
    while cur:
        nodes.append(cur); cur = cur.next
    pos = {id(n): i for i, n in enumerate(nodes)}       # identity -> index
    return [(n.val, pos.get(id(n.random)) if n.random is not None else None) for n in nodes]

def all_nodes(head):
    out, cur = [], head
    while cur:
        out.append(cur); cur = cur.next
    return out

# ---- Approach 1: hash map (deepcopy ka memo haath se) ----
def copyRandomList_map(head):
    if head is None:
        return None
    mapping = {}                                # old node -> new node (yehi 'memo' hai)
    cur = head
    while cur:                                  # pass 1: sirf nodes banao
        mapping[cur] = RNode(cur.val)
        cur = cur.next
    cur = head
    while cur:                                  # pass 2: pointers jodo
        mapping[cur].next = mapping.get(cur.next)      # None safe
        mapping[cur].random = mapping.get(cur.random)
        cur = cur.next
    return mapping[head]

# ---- Approach 2: interleaving, O(1) extra space ----
def copyRandomList_interleave(head):
    if head is None:
        return None
    # step 1: A -> A' -> B -> B' ...
    cur = head
    while cur:
        nxt = cur.next
        cur.next = RNode(cur.val)
        cur.next.next = nxt
        cur = nxt
    # step 2: random pointers -- kisi node ka copy hamesha uske foran baad hai
    cur = head
    while cur:
        if cur.random is not None:
            cur.next.random = cur.random.next
        cur = cur.next.next
    # step 3: alag karo aur original restore karo
    dummy = RNode(0)
    copy_tail, cur = dummy, head
    while cur:
        copy = cur.next
        cur.next = copy.next                    # original bahaal
        copy_tail.next = copy                   # copy list barhao
        copy_tail = copy
        cur = cur.next
    return dummy.next

# ---- TESTS ----
cases = [
    [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)],   # LeetCode ka example 1
    [(1, 1), (2, 1)],                                  # example 2
    [(3, None), (3, 0), (3, None)],                    # example 3
    [],                                                # khaali list
    [(5, 0)],                                          # ek node jo khud ko point karta hai
]

for pairs in cases:
    for fn in (copyRandomList_map, copyRandomList_interleave):
        head = build_random_list(pairs)
        original_nodes = all_nodes(head)
        copied = fn(head)
        # 1) structure bilkul same
        assert to_pairs(copied) == pairs, (fn.__name__, pairs, to_pairs(copied))
        # 2) DEEP copy hai -- koi node share nahi hui
        copy_ids = {id(n) for n in all_nodes(copied)}
        assert copy_ids.isdisjoint({id(n) for n in original_nodes}), "shallow copy!"
        # 3) original bilkul waisa hi bacha (interleave version ke liye ahem)
        assert to_pairs(head) == pairs, "original kharab ho gaya"

print("LC 138: dono approaches ke saare tests pass ✔")
print("example 1 ka copy:", to_pairs(copyRandomList_map(build_random_list(cases[0]))))
"""))

A(md("""
**Output ka matlab:** Teen cheezein sabit hui — (1) structure hu-ba-hu, (2) `id()` sets disjoint
yaani **koi node share nahi** (asli deep copy), (3) interleaving ke baad **original restore** ho gaya.

**Interview follow-up:** *"Interleaving me `random` pointer bina map kaise mila?"* →
Kyunki har node ka copy uske foran baad hai, is liye `old.random.next` hi `new.random` hai.
Yehi trick "invariant se memory bachana" ka classic example hai.
"""))

A(md("""
### LC 133. Clone Graph — Medium

**Link:** https://leetcode.com/problems/clone-graph/

**Problem (Roman Urdu):** Ek connected undirected graph ka node diya hai (`val` + `neighbors` list).
Poore graph ka **deep copy** banao. Graph me **cycles** hain (undirected = har edge dono taraf),
is liye seedha recursion infinite loop me chala jayega.

**Ye topic se kaise juda hai:** Bilkul `deepcopy` ka `memo`! Ek `visited` dict
(`old node → new node`) hi cycle protection deta hai — exactly jaise CPython ka memo.

**Approach (DFS + visited map)**
1. `visited` dict rakho: purana node → naya node.
2. Node par pahunchte hi **pehle** clone banao aur `visited` me daal do (recursion se **pehle** —
   yehi cycle-safety hai, `__deepcopy__` me bhi yehi rule tha).
3. Har neighbour ke liye recursive clone kar ke naye node ke `neighbors` me daalo.
4. BFS version bhi wahi kaam `deque` se karta hai (deep graph par `RecursionError` se bachne ke liye behtar).

- **Time:** O(V + E) — har node aur edge ek dafa
- **Space:** O(V) visited map (+ recursion stack ya BFS queue)
"""))

A(code(r"""
from collections import deque

class GNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
    def __repr__(self):
        return f"GNode({self.val})"

# ---- helpers: adjacency list (1-indexed jaise LeetCode) se graph banao ----
def build_graph(adj):
    if not adj:
        return None
    nodes = {i + 1: GNode(i + 1) for i in range(len(adj))}
    for i, nbrs in enumerate(adj, start=1):
        nodes[i].neighbors = [nodes[j] for j in nbrs]
    return nodes[1]

def to_adj(node):
    # graph ko wapas adjacency list me: {val: sorted neighbour vals}
    if node is None:
        return {}
    seen, q, out = {node.val}, deque([node]), {}
    while q:
        cur = q.popleft()
        out[cur.val] = sorted(n.val for n in cur.neighbors)
        for n in cur.neighbors:
            if n.val not in seen:
                seen.add(n.val); q.append(n)
    return out

def collect_ids(node):
    if node is None:
        return set()
    seen, q, ids = {id(node)}, deque([node]), set()
    while q:
        cur = q.popleft(); ids.add(id(cur))
        for n in cur.neighbors:
            if id(n) not in seen:
                seen.add(id(n)); q.append(n)
    return ids

# ---- Approach 1: DFS + visited (recursive) ----
def cloneGraph_dfs(node, visited=None):
    if node is None:
        return None
    visited = {} if visited is None else visited
    if node in visited:                     # pehle se clone ho chuka -> wohi do (cycle-safe)
        return visited[node]
    clone = GNode(node.val)
    visited[node] = clone                   # LAZMI: recursion se PEHLE register karo
    for nbr in node.neighbors:
        clone.neighbors.append(cloneGraph_dfs(nbr, visited))
    return clone

# ---- Approach 2: BFS (bare/deep graphs ke liye, koi recursion limit nahi) ----
def cloneGraph_bfs(node):
    if node is None:
        return None
    visited = {node: GNode(node.val)}
    q = deque([node])
    while q:
        cur = q.popleft()
        for nbr in cur.neighbors:
            if nbr not in visited:
                visited[nbr] = GNode(nbr.val)
                q.append(nbr)
            visited[cur].neighbors.append(visited[nbr])
    return visited[node]

# ---- TESTS ----
graphs = [
    [[2, 4], [1, 3], [2, 4], [1, 3]],      # LeetCode example 1 (square, cycles)
    [[]],                                   # ek akela node
    [[2], [1]],                             # do nodes
    [[2, 3], [1], [1]],                     # star
]

for adj in graphs:
    expected = to_adj(build_graph(adj))
    for fn in (cloneGraph_dfs, cloneGraph_bfs):
        original = build_graph(adj)
        clone = fn(original)
        assert to_adj(clone) == expected, (fn.__name__, adj)
        # deep copy proof: koi node share nahi
        assert collect_ids(clone).isdisjoint(collect_ids(original)), "shallow clone!"
        # original bilkul bacha rehna chahiye
        assert to_adj(original) == expected

assert cloneGraph_dfs(None) is None and cloneGraph_bfs(None) is None   # khaali graph
print("LC 133: DFS + BFS dono pass ✔")
print("example 1 ka clone adjacency:", to_adj(cloneGraph_bfs(build_graph(graphs[0]))))

# self-loop bhi handle hota hai (node khud ka neighbour)
selfy = GNode(1); selfy.neighbors = [selfy]
c = cloneGraph_bfs(selfy)
assert c is not selfy and c.neighbors[0] is c        # clone bhi khud ko point kare
print("self-loop graph bhi theek clone hua ✔")
"""))

A(md("""
**Output ka matlab:** Adjacency dono me barabar, `id()` sets disjoint (poora naya graph),
original mehfooz, aur self-loop bhi structure ke sath copy hua — matlab hamara "memo" theek kaam kar raha hai.

**Interview follow-up:** *"`visited[node] = clone` recursion se pehle kyun?"* →
Warna cycle par wapas usi node par aa kar infinite recursion ho jaayegi.
Bilkul yehi wajah hai ke `__deepcopy__` me `memo[id(self)] = new` sab se pehle likhte hain.
"""))

A(md("""
### LC 146. LRU Cache — Medium

**Link:** https://leetcode.com/problems/lru-cache/

**Problem (Roman Urdu):** Ek cache banao jis me `get(key)` aur `put(key, value)` **O(1)** me ho.
Capacity full ho jaye to sab se **purana istemal hone wala** (least recently used) item nikaal do.
`get` aur `put` dono item ko "recently used" bana dete hain.

**Ye topic se kaise juda hai:** Ye asli production cache design hai — aur andar
**doubly linked list** hai, yaani har node me `prev`/`next` = **reference cycles** ki bharmaar.
Isi liye GC (section 11) aur weakref (section 13) ki baat cache ke sath aati hai.

**Approach 1 — dict + doubly linked list (classic, "interview answer")**
- `dict`: key → node (O(1) lookup)
- DLL: order (head = most recent, tail = least recent). Dummy `head`/`tail` sentinels rakho
  taake edge cases (khaali list, aakhri node) me `if` na likhna paren.
- `get`: node dhoondo → DLL se nikaal kar head ke paas lagao
- `put`: maujood ho to update + move; warna add; capacity cross ho to `tail.prev` (LRU) hatao

**Approach 2 — `collections.OrderedDict`** (ya plain `dict`, jo 3.7+ me insertion-ordered hai)
`move_to_end()` aur `popitem(last=False)` se wohi kaam 10 lines me.

- **Time:** dono me `get`/`put` **O(1)** amortized
- **Space:** O(capacity)
"""))

A(code(r"""
from collections import OrderedDict

# ================= Approach 1: dict + doubly linked list =================
class _DNode:
    __slots__ = ("key", "val", "prev", "next")      # slots -> kam memory (section 14)
    def __init__(self, key=None, val=None):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}                               # key -> _DNode
        # sentinels: head.next = most recent, tail.prev = least recent
        self.head, self.tail = _DNode(), _DNode()
        self.head.next, self.tail.prev = self.tail, self.head

    # --- DLL helpers ---
    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev
        node.prev = node.next = None                # references saaf (cycle na chhore)

    def _push_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    # --- public API ---
    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node); self._push_front(node)   # "recently used" bana do
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:                         # update + move to front
            node.val = value
            self._unlink(node); self._push_front(node)
            return
        if len(self.map) >= self.cap:                # evict LRU (tail se pehla asli node)
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]
        node = _DNode(key, value)
        self.map[key] = node
        self._push_front(node)

    def keys_mru_first(self):                        # sirf testing/debug ke liye
        out, cur = [], self.head.next
        while cur is not self.tail:
            out.append(cur.key); cur = cur.next
        return out

# ================= Approach 2: OrderedDict =================
class LRUCacheOrdered:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key)                     # most-recent ban gaya
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)              # sab se purana nikaalo
"""))

A(code(r"""
# ---- TESTS (dono implementations par ek jaise) ----
for cls in (LRUCache, LRUCacheOrdered):
    # LeetCode ka official example
    c = cls(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1                # 1 recently used
    c.put(3, 3)                         # capacity full -> key 2 evict
    assert c.get(2) == -1, cls.__name__
    c.put(4, 4)                         # key 1 evict (kyunki 3,1 me 1 purana)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

    # capacity 1 ka edge case
    c1 = cls(1)
    c1.put(1, 10); assert c1.get(1) == 10
    c1.put(2, 20); assert c1.get(1) == -1 and c1.get(2) == 20

    # update se value badle magar naya slot na bane
    c2 = cls(2)
    c2.put(1, 1); c2.put(1, 100); c2.put(2, 2)
    assert c2.get(1) == 100 and c2.get(2) == 2

    # get bhi recency update kare
    c3 = cls(2)
    c3.put(1, 1); c3.put(2, 2)
    c3.get(1)                           # 1 fresh ho gaya
    c3.put(3, 3)                        # -> 2 evict hona chahiye
    assert c3.get(2) == -1 and c3.get(1) == 1

print("LC 146: dono implementations ke saare tests pass ✔")

# order ka andar se muayana (sirf DLL version me available)
c = LRUCache(3)
for k in (1, 2, 3):
    c.put(k, k * 10)
c.get(1)
print("MRU -> LRU order:", c.keys_mru_first(), "(1 ko chhoone se wo aage aa gaya)")

# --- interview follow-up: kya functools.lru_cache kaafi nahi? ---
from functools import lru_cache
@lru_cache(maxsize=2)
def slow_square(n):
    return n * n
slow_square(2); slow_square(3); slow_square(2); slow_square(4)
print("\nfunctools.lru_cache stats:", slow_square.cache_info())
print("Farq: lru_cache FUNCTION results cache karta hai (arguments = key).")
print("      LC 146 wala manual cache mutable key/value store hai jahan tum evict/inspect kar sakte ho.")
"""))

A(md("""
**Output ka matlab:** Dono implementations bilkul same behave karti hain.
`keys_mru_first()` se nazar aaya ke `get(1)` ne key 1 ko aage laa diya.

**Interview follow-ups:**
- *"Kyun doubly linked list, singly nahi?"* → Kisi bhi node ko O(1) me nikaalna hai;
  singly list me uska `prev` dhoondne ke liye O(n) traverse karna parta.
- *"`dict` (3.7+) insertion-ordered hai, phir DLL ki zaroorat kya?"* → Interview me DLL wala
  jawab expected hai (aur `move_to_end` jaisi API plain dict me nahi hai). Production me
  `OrderedDict`/`lru_cache` use karo.
- *"Thread-safe kaise banaoge?"* → `threading.Lock` `get`/`put` ke around
  (dekho notebook 03), ya per-shard locks.
- *"Memory leak ka khatra?"* → DLL cycles banata hai; `_unlink` me `prev`/`next` ko `None`
  karna aur bounded capacity rakhna zaroori hai. Unbounded cache = leak.
"""))

A(md("""
---
# Interview Questions & Answers

**Q1. Python me variable kya hai — dabba ya label?**
Label. Names heap objects ki taraf **references** hain. `a = b` object copy nahi karta,
sirf ek aur naam usi object par bind karta hai.

**Q2. Python pass-by-value hai ya pass-by-reference?**
Dono nahi — **call by object reference (sharing)**. Object mutate karo to caller ko dikhega,
parameter rebind karo to nahi.

**Q3. `is` aur `==` me farq?**
`is` identity (same object, `id()` barabar), `==` value (`__eq__`). `is` sirf `None`/singletons/sentinels ke liye.

**Q4. `sys.getrefcount(x)` expected se 1 zyada kyun deta hai?**
Function call ka argument khud ek temporary reference banata hai.

**Q5. Immortal objects kya hain?**
PEP 683 (3.12+): `None`, `True`, `False`, chhote ints/strings ka refcount fixed bara constant
rakh diya gaya hai taake unke counters par contention/locking na ho — is liye unka refcount
ajeeb bara nazar aata hai.

**Q6. CPython memory kaise manage karta hai?**
Primary: **reference counting** (refcount 0 → foran free). Sath me **cycle collector**
(generational, 3.13+ incremental) un containers ke liye jo cycles bana lete hain.
Allocator level par `pymalloc` arenas/pools/blocks use karta hai aur chhote objects ke liye free lists.

**Q7. Reference cycle kya hai aur kyun masla hai?**
`a.peer = b; b.peer = a` — dono ka refcount kabhi 0 nahi hota, is liye refcounting free nahi kar sakti.
`gc` module cycles detect kar ke free karta hai; ya design me `weakref` use kar ke cycle banao hi na.

**Q8. `gc.disable()` kab theek hai?**
Jab tum yaqeen se jaanti ho ke cycles nahi banenge (short-lived request handlers, batch scripts)
aur GC pauses measurable dard de rahe hon. Warna memory growth ka risk hai.

**Q9. Shallow vs deep copy?**
Shallow: naya container, andar wale objects shared. Deep: recursively sab naya, `memo` dict ke sath
(cycles safe + shared structure mehfooz). Deepcopy slow hai.

**Q10. `deepcopy` cycle par crash kyun nahi karta?**
`memo` dict me `id(obj) → copy` rakhta hai; dobara wohi object aane par nayi copy nahi banata,
memo wali de deta hai.

**Q11. Mutable default argument ka masla aur fix?**
Default `def` chalne par **ek dafa** evaluate ho kar `__defaults__` me store hota hai —
har call me wohi object. Fix: `def f(x=None): x = [] if x is None else x`.

**Q12. `__slots__` kya karta hai aur kab use karein?**
Per-instance `__dict__` hata kar fixed C-array slots deta hai: kam memory, thora tez attribute
access, dynamic attributes band. Sirf tab jab hazaaron/lakhon instances hon.
Subclass me `__slots__ = ()` likhna na bhoolo, aur weakref chahiye to `__weakref__` add karo.

**Q13. `sys.getsizeof` list ke liye chhota number kyun deta hai?**
Wo sirf container (pointer array + header) ginta hai, andar wale objects nahi.
Deep size ke liye `id()`-based `seen` set ke sath recursion, ya `tracemalloc`.

**Q14. `weakref` kab use karte hain?**
Caches/identity maps (`WeakValueDictionary`), parent back-references (cycle avoid),
observers/callbacks (`WeakMethod`), per-object metadata (`WeakKeyDictionary`).

**Q15. `__del__` kyun avoid karna chahiye?**
Non-deterministic timing, exceptions nigal jaate hain, resurrection mumkin,
shutdown par globals gaayab. Behtar: context manager (`with`) ya `weakref.finalize`.

**Q16. String concatenation loop me kyun slow hai?**
`str` immutable — har `+=` (aam tor par) nayi string + poora copy → O(n²).
`"".join(pieces)` ek allocation me O(n).

**Q17. `list` vs `tuple` internals?**
`list`: mutable, over-allocated pointer array (amortized O(1) append), `__hash__ = None`.
`tuple`: immutable, exact size, hashable (agar andar sab hashable ho), interpreter isay
cache/reuse kar sakta hai, thora kam memory.

**Q18. String interning kya hai, `sys.intern` kab?**
Compile-time identifier-jaisi strings ek hi object share karti hain. `sys.intern` un cases me
faida deta hai jahan bohat si duplicate runtime strings hon (log/CSV parsing) —
memory kam aur dict lookups tez (pointer compare fast path). Interned strings process bhar zinda rehti hain.

**Q19. `LOAD_FAST` vs `LOAD_GLOBAL`?**
Locals array-index se uthte hain (tez), globals/builtins dictionary lookup se.
Hot loop me globals/methods ko local naam me bind karna ek jaana-pehchana micro-optimization hai.

**Q20. Constant folding kya hai?**
Compiler literal expressions ka natija pehle hi nikaal leta hai (`24*60*60` → `86400`),
aur literal membership sets ko `frozenset` constant bana deta hai. `dis` / `co_consts` se dekho.
"""))

A(md("""
---
# Practice Exercises (khud karo)

1. **Refcount detective** — ek function likho `ref_report(obj)` jo `sys.getrefcount` aur
   `gc.get_referrers` use kar ke bataye kitne aur kaun references pakre hue hain.
   *Hint:* `gc.get_referrers` ka output bara hota hai — sirf `type()` names print karo.

2. **Freeze karo** — `deep_freeze(obj)` likho jo nested `dict`/`list` ko recursively
   `MappingProxyType`/`tuple` me badal de (immutable snapshot).
   *Hint:* `types.MappingProxyType`, aur recursion + `seen` set cycles ke liye.

3. **Copy-on-write config** — ek class banao jo shared defaults par baithi ho magar pehli
   write par apna deep copy bana le.
   *Hint:* `__setitem__` me flag check karo, `copy.deepcopy` ek dafa.

4. **Leak hunter** — ek function jo dane par bataye ke di gayi class ke kitne instances zinda hain.
   *Hint:* `gc.get_objects()` par `isinstance` filter, ya class me `WeakSet` registry.

5. **`__slots__` benchmark** — ek script jo `N` badal kar (1k, 10k, 100k) dict-class vs
   slots-class vs `NamedTuple` vs `dataclass(slots=True)` ki memory aur build time compare kare.
   *Hint:* `tracemalloc` + `time.perf_counter`, results ek table me print karo.

6. **Interning ka faida napo** — 100k duplicate strings ke sath aur bina `sys.intern`
   memory measure karo. Kitne percent bacha?
   *Hint:* Strings runtime par banao (`"user_" + str(i % 50)`) warna compiler intern kar dega.

7. **Apna `deepcopy`** — `my_deepcopy(obj, memo=None)` likho jo `dict`/`list`/`tuple`/`set`
   aur custom objects handle kare, cycles safe ho, aur `copy.deepcopy` se compare karo.
   *Hint:* pehle `memo[id(obj)] = new` rakho, phir bharo.

8. **Bytecode quiz** — `x in {1,2,3}` vs `x in [1,2,3]` vs `x in (1,2,3)` ka `dis` compare karo
   aur `timeit` se speed. Kaun jeeta aur kyun?

9. **LC 138 variant** — same problem magar `random` pointer ke sath ek `parent` pointer bhi ho.
   Kya tumhara mapping approach change hoga? (Nahi — kyun? likho.)

10. **LRU + TTL** — LC 146 wale cache me `ttl_seconds` add karo (expire ho jaye to `get` par -1).
    *Hint:* node me `expires_at` rakho, `time.monotonic()` use karo, lazy expiry par evict karo.
"""))

A(md("""
---
# Summary / Cheat-sheet

## Mental model (ek line me)
> Python me **names** heap **objects** ki taraf **references** hain. Assignment naam bind karta hai,
> kabhi object copy nahi karta. Behaviour ka farq **mutability** se aata hai, "value vs reference" se nahi.

## Quick reference

| Cheez | Yaad rakhne wali baat |
|---|---|
| `a = b` | reference copy, object copy nahi |
| `a is b` | same object? (`id` barabar) — sirf singletons/sentinels ke liye |
| `sys.getrefcount(x)` | jawab me **+1** (argument bhi reference) |
| Immortal objects | `None`/`True`/chhote ints ka refcount ajeeb bara — normal |
| Small int cache | `-5..256` pre-created |
| String interning | compile-time literals shared; runtime strings ke liye `sys.intern` |
| Mutation vs rebinding | `x.append()` sab ko dikhta; `x = ...` sirf local |
| Mutable default | `def f(a=[])` → shared state; `None` sentinel use karo |
| `copy.copy` | naya container, andar shared |
| `copy.deepcopy` | recursively naya + `memo` (cycle safe, structure preserve) |
| `__copy__`/`__deepcopy__` | resources ko copy hone se bachane ke liye; `memo[id(self)]` pehle |
| Refcounting | 0 par foran free, deterministic, cycles hal nahi karta |
| `gc` | cycle collector, generational/incremental, sirf containers track |
| `__del__` | non-deterministic + exceptions nigal jaate hain → `with` / `weakref.finalize` |
| `weakref` | refcount nahi barhata → cache/observer/parent-pointer |
| `__slots__` | `__dict__` khatam: memory kam, access tez, dynamic attrs band |
| `getsizeof` | shallow! deep size ke liye recursion + `seen`, ya `tracemalloc` |
| `list` | pointers + over-allocation → append amortized O(1) |
| `array`/`numpy` | raw values contiguous → kai guna kam memory |
| `deque` | dono sire par O(1); indexing O(n) |
| `+=` on str in loop | O(n²) → `"".join(pieces)` ya `io.StringIO` |
| `LOAD_FAST` vs `LOAD_GLOBAL` | locals array-index, globals dict lookup |
| Constant folding | literals compile-time par hal; `in {literal set}` → `frozenset` constant |

## Memory optimization playbook (tarteeb se)
1. Kya data structure sahi hai? (`list of dicts` → `dataclass(slots=True)` / columnar arrays)
2. Sab kuch memory me kyun? → **generators / streaming**
3. Duplicate strings bohat hain? → `sys.intern`
4. Lakhs objects? → `__slots__` / `NamedTuple` / `array` / `numpy`
5. Cache leak kar raha hai? → bounded LRU ya `WeakValueDictionary`
6. Numbers ki bari list? → `array`/`numpy` (pointer + boxing khatam)
7. Measure karo: `tracemalloc` (kahan allocate hua), recursive `deep_size`, `gc.get_objects()`

## LeetCode recap
| # | Title | Core idea | Time | Space |
|---|---|---|---|---|
| 138 | Copy List with Random Pointer | old→new map (memo), ya interleaving | O(n) | O(n) / O(1) |
| 133 | Clone Graph | DFS/BFS + visited map (cycle safe) | O(V+E) | O(V) |
| 146 | LRU Cache | dict + doubly linked list (ya OrderedDict) | O(1) | O(capacity) |

**Agla notebook:** `02_Asyncio_Coroutines_aur_Async_Patterns.ipynb` — event loop, tasks,
aur concurrency ke asli patterns.
"""))
