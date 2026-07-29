import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ============================================================
# 1. TITLE + ROADMAP
# ============================================================
cells.append(md("""
# 01 — Linked List: Complete Guide (Zero se Interview tak)

**Level:** Intermediate
**Series:** DSA in Python — Intermediate

## Is notebook me kya seekhenge (roadmap)

1. Linked List kya hai — memory me asal picture (boxes + arrows)
2. Array vs Linked List — complexity table + memory overhead ka hisaab
3. `Node` class aur **Singly Linked List** (insert head/tail/index, delete, search, `__iter__`, `__str__`)
4. **Doubly Linked List** (prev + next, dono taraf traversal)
5. **Circular Linked List** + **Josephus problem**
6. **Dummy / sentinel node** technique — 90% bugs isi se khatam hote hain
7. **Two-pointer** techniques: middle, nth-from-end, Floyd cycle detection (+ cycle start ka **proof**), intersection
8. **Reverse**: iterative, recursive, k-groups, between positions
9. **Merge**: two sorted, k sorted (heap), poori list ka merge sort
10. **Duplicates** hatana (sorted aur unsorted dono)
11. Palindrome check, Add two numbers, Partition, Copy with random pointer
12. DLL ka **LRU Cache** me asli role
13. Common bugs ki list (jahan har student phasta hai)
14. **19 LeetCode problems** — full solutions + passing asserts
15. Interview Q&A, Practice exercises, Cheat-sheet

## Prerequisites

- Python classes/objects (`__init__`, `self`), `None` ka matlab
- `list`, `dict`, loops, recursion ki basic samajh
- Big-O notation ki thori si jaan-pehchan

> **Golden rule:** Yeh notebook top-se-bottom chalao. Har cell pichle cell ke classes/helpers
> par depend karta hai.
"""))

# ============================================================
# 2. CONCEPT
# ============================================================
cells.append(md("""
## 1. Linked List Kya Hai

**Kya hai:** Linked List ek **linear data structure** hai jisme elements (jinko **node** kehte hain)
memory me **contiguous** (aik saath) nahi hote. Har node do cheezein rakhta hai:

1. **data** — asli value
2. **next** — agle node ka **reference (pointer)**

```
head
 |
 v
+----+----+    +----+----+    +----+------+
| 10 |  o-|--->| 20 |  o-|--->| 30 | None |
+----+----+    +----+----+    +----+------+
```

**Kyun / kahan use hota hai:**

- Jahan **insert/delete beech me** bohat hoti hai (array me shifting karni parti hai, LL me sirf
  pointer badalna hai) — jaise **LRU cache**, **undo/redo**, **music playlist**.
- Jahan size pehle se **maloom nahi** — LL grow karti rehti hai bina "resize + copy" ke.
- **OS / low level:** free memory blocks ki list, process scheduling queue.
- **Foundation:** Stack, Queue, Graph adjacency list, Hash table ki chaining — sab LL par bane hain.

**Ahem baat:** Python ka built-in `list` **linked list NAHI** hai — woh **dynamic array** hai.
`collections.deque` andar se **doubly linked list of blocks** hai. Interview me LL manually likhni parti hai.

**Terminology:**

| Term | Matlab |
|---|---|
| `head` | pehla node (poori list ka handle) |
| `tail` | aakhri node (jiska `next is None`) |
| `node` | ek dabba (data + pointer) |
| traversal | head se shuru kar ke `next` follow karna |
| dangling pointer | aisa reference jo delete ho chuke node ko point kare |

**Interview tip:** Jab bhi koi kahe "insert/delete O(1) chahiye lekin random access nahi chahiye"
→ jawab **linked list**.
"""))

cells.append(md("""
## 2. Array vs Linked List — Poora Muqabla

### Time complexity

| Operation | Array / Python `list` | Singly Linked List |
|---|---|---|
| Index par access (`a[i]`) | **O(1)** | O(n) — chal kar jana parta hai |
| Head par insert | O(n) — sab shift | **O(1)** |
| Tail par insert | O(1) amortized | O(n), ya **O(1)** agar `tail` pointer rakho |
| Beech me insert (node pata hai) | O(n) | **O(1)** |
| Head delete | O(n) | **O(1)** |
| Value se search | O(n) | O(n) |
| Sorted me binary search | **O(log n)** | O(n) — random access nahi |
| Reverse | O(n) | O(n) |

### Memory

| Cheez | Array | Linked List |
|---|---|---|
| Layout | contiguous block | scattered nodes |
| Extra memory | thora slack (capacity > size) | **har node par ek pointer** (8 bytes) + object overhead |
| Cache locality | **bohat achhi** (CPU prefetch) | kharab (pointer chasing = cache miss) |
| Resize ka cost | O(n) copy jab bhar jaye | kabhi nahi |

**Practical reality (yaad rakhna):** Chhoti/medium n par array **aksar tez** hota hai — chahe
theory me LL ka insert O(1) ho — kyunki **cache locality** jeet jati hai. LL ka asli faida
tab hai jab:
- node ka reference pehle se hath me ho (jaise LRU cache), ya
- bohat bari list ke beech me continuously insert/delete ho raha ho.

**Interview tip:** "Array vs Linked List" ka best jawab sirf table nahi — **cache locality** ka
zikr karo, interviewer impress hota hai.
"""))

cells.append(md("""
## 3. `Node` Class

**Kya hai:** Sabse chhota building block. Sirf `data` aur `next`.

**Syntax + gotcha:** `__slots__` use karne se memory bachti hai (per-object `__dict__` nahi banta).
Interview me `__slots__` likhna optional hai, lekin batana plus point hai.
"""))

cells.append(code(r"""
# ---- Node: linked list ka sabse chhota hissa ----
class Node:
    # __slots__: per-instance __dict__ nahi banega -> memory kam, attribute access tez
    __slots__ = ("data", "next")

    def __init__(self, data, next=None):
        self.data = data      # asli value
        self.next = next      # agle node ka reference (default None = list ka end)

    def __repr__(self):
        # debugging ke liye: sirf apna data dikhao, poori chain nahi (warna infinite loop risk)
        return f"Node({self.data!r})"


# Haath se 3 node jorte hain: 10 -> 20 -> 30 -> None
n3 = Node(30)
n2 = Node(20, n3)
n1 = Node(10, n2)
head = n1

print("head        ->", head)
print("head.next   ->", head.next)
print("2nd next    ->", head.next.next)
print("teesre ka next (end) ->", head.next.next.next)

# Manual traversal - LL ka sabse bunyadi loop (yeh muhavra yaad kar lo)
cur = head
out = []
while cur is not None:      # 'is not None' likho, 'while cur:' data=0 par galat ho sakta hai...
    out.append(cur.data)    # ...actually node object hamesha truthy hai, magar habit achhi rakho
    cur = cur.next          # aage barho -- yeh line bhoolna = infinite loop
print("traversal   ->", out)
"""))

cells.append(md("""
### Memory ka hisaab (chhota experiment)

Har node ek Python object hai — us par overhead hota hai. Neeche `sys.getsizeof` se andaza
lagate hain ke 1 int list me store karne ka cost vs node me store karne ka cost.
"""))

cells.append(code(r"""
import sys

# Ek node ka size (with __slots__)
print("Node object size      :", sys.getsizeof(Node(1)), "bytes (+ __slots__ storage)")

# Python list: 1000 ints ke liye array of pointers
lst = list(range(1000))
print("list(1000) ka container:", sys.getsizeof(lst), "bytes (sirf pointer array)")

# 1000 nodes banane ka container cost (int objects alag se, dono me common hain)
total_nodes = 0
cur = None
for i in range(1000):
    cur = Node(i, cur)
    total_nodes += sys.getsizeof(cur)
print("1000 Nodes ka total   :", total_nodes, "bytes")
print()
print("Natija: LL me per-element overhead kaafi zyada hai (object header + pointer).")
print("Isi liye 'memory efficient' kehna aksar GALAT hai - LL sirf structural flexibility deti hai.")
"""))

# ============================================================
# 3. SINGLY LINKED LIST CLASS
# ============================================================
cells.append(md("""
## 4. Singly Linked List Class (poori)

**Kya hai:** Ek wrapper class jo `head`, `tail` aur `_size` maintain karti hai. `tail` rakhne se
`append` O(1) ho jata hai, aur `_size` rakhne se `len()` O(1).

**Design decisions (interview me poocha jata hai):**

| Choice | Faida | Nuqsan |
|---|---|---|
| `tail` pointer rakhna | append O(1) | har delete par tail update karna parta hai (bug risk) |
| `_size` counter | `len()` O(1) | har op me update karna zaroori |
| dummy head | edge cases khatam | ek extra node |

Neeche wali class me sab kuch hai: insert (head/tail/index), delete (value/index), search,
`__len__`, `__iter__`, `__str__`, `from_list`, `to_list`.
"""))

cells.append(code(r"""
class SinglyLinkedList:
    # Ek complete singly linked list: head + tail + size maintain karti hai

    def __init__(self, iterable=None):
        self.head = None      # pehla node
        self.tail = None      # aakhri node (append O(1) ke liye)
        self._size = 0        # len() O(1) ke liye
        if iterable is not None:
            for x in iterable:
                self.append(x)          # tail par ek ek daalte jao

    # ---------- basics ----------
    def __len__(self):
        return self._size               # O(1) kyunki counter maintain kiya

    def is_empty(self):
        return self.head is None

    def __iter__(self):
        # generator: 'for x in ll' kaam karega, list(ll) bhi
        cur = self.head
        while cur is not None:
            yield cur.data
            cur = cur.next

    def nodes(self):
        # data ki jagah node objects dena (internal kaam ke liye)
        cur = self.head
        while cur is not None:
            yield cur
            cur = cur.next

    def __str__(self):
        # 10 -> 20 -> 30 -> None  (readable form)
        return " -> ".join(map(repr, self)) + " -> None" if self.head else "None (empty)"

    def __repr__(self):
        return f"SinglyLinkedList([{', '.join(map(repr, self))}])"

    # ---------- insert ----------
    def insert_head(self, data):            # O(1)
        node = Node(data, self.head)        # naya node purane head ko point kare
        self.head = node                    # head shift
        if self.tail is None:               # list khali thi -> ab tail bhi yehi hai
            self.tail = node
        self._size += 1
        return self

    def append(self, data):                 # tail par -> O(1) (tail pointer ki wajah se)
        node = Node(data)
        if self.tail is None:               # khali list ka special case
            self.head = self.tail = node
        else:
            self.tail.next = node           # purane tail ko naye se jodo
            self.tail = node                # tail update -- bhoolna = tail dangling bug
        self._size += 1
        return self

    insert_tail = append                    # alias (dono naam interview me chalte hain)

    def insert_at(self, index, data):       # O(index)
        if index < 0 or index > self._size:
            raise IndexError(f"index {index} out of range 0..{self._size}")
        if index == 0:
            return self.insert_head(data)
        if index == self._size:
            return self.append(data)
        prev = self.head
        for _ in range(index - 1):          # index-1 tak chalo (us se pehle wala node chahiye)
            prev = prev.next
        prev.next = Node(data, prev.next)   # beech me ghusa do -- O(1) pointer work
        self._size += 1
        return self

    # ---------- read ----------
    def get(self, index):                   # O(index) -- array jaisa O(1) NAHI
        if index < 0 or index >= self._size:
            raise IndexError(index)
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur.data

    def search(self, target):
        # pehla index return karo jahan value mile, warna -1
        for i, x in enumerate(self):
            if x == target:
                return i
        return -1

    def __contains__(self, target):         # 'in' operator ke liye
        return self.search(target) != -1

    # ---------- delete ----------
    def delete_head(self):                  # O(1)
        if self.head is None:
            raise IndexError("empty list se delete")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:               # aakhri element nikal gaya
            self.tail = None                # tail bhi reset -- CLASSIC BUG yahan hota hai
        self._size -= 1
        return data

    def delete_value(self, target):
        # pehla matching node hatao; True/False return
        prev, cur = None, self.head
        while cur is not None:
            if cur.data == target:
                if prev is None:            # head hi target tha
                    self.head = cur.next
                else:
                    prev.next = cur.next    # prev ko cur ke baad wale se jodo
                if cur is self.tail:        # tail delete hua -> tail peeche khisko
                    self.tail = prev
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def delete_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError(index)
        if index == 0:
            return self.delete_head()
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next
        victim = prev.next
        prev.next = victim.next
        if victim is self.tail:
            self.tail = prev
        self._size -= 1
        return victim.data

    def clear(self):
        self.head = self.tail = None
        self._size = 0

    # ---------- helpers (bohat kaam aayenge) ----------
    @classmethod
    def from_list(cls, values):
        return cls(values)

    def to_list(self):
        return list(self)


# ---- Demo ----
ll = SinglyLinkedList.from_list([10, 20, 30])
print("banayi        :", ll)
ll.insert_head(5)
print("insert_head(5):", ll)
ll.append(40)
print("append(40)    :", ll)
ll.insert_at(2, 15)
print("insert_at(2,15):", ll)
print("len           :", len(ll), "| get(3):", ll.get(3), "| search(30):", ll.search(30))
print("25 in ll?     :", 25 in ll, "| 30 in ll?:", 30 in ll)
ll.delete_value(15)
print("delete 15     :", ll)
print("delete_at(0)  :", ll.delete_at(0), "->", ll)
print("to_list       :", ll.to_list())
print("repr          :", repr(ll))
"""))

# ============================================================
# 4. DOUBLY LINKED LIST
# ============================================================
cells.append(md("""
## 5. Doubly Linked List (DLL)

**Kya hai:** Har node ke paas **do** pointer hote hain — `prev` aur `next`.

```
None <-+----+----+     +----+----+     +----+----+-> None
       |prev| 10 |<--->| 20 |    |<--->|    | 30 |
       +----+----+     +----+----+     +----+----+
        head                             tail
```

**Kyun:**

1. **Dono taraf traversal** (forward + backward)
2. Node ka reference hath me ho to us node ko **O(1) me delete** kar sakte ho (SLL me `prev`
   dhoondne ke liye O(n) chalna parta hai) — **yeh LRU cache ki jaan hai**
3. `tail` se peeche chalna aasan (browser back button, undo stack)

**Cost:** har node par ek extra pointer (memory +), aur har operation me **do** pointer update
karne parte hain (bug risk +).

**Gotcha:** DLL me update ka order galat hua to reference kho jata hai. Formula yaad rakho —
pehle naye node ke pointers set karo, phir purane nodes ke.
"""))

cells.append(code(r"""
class DNode:
    __slots__ = ("data", "prev", "next")

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev      # pichla node
        self.next = next      # agla node

    def __repr__(self):
        return f"DNode({self.data!r})"


class DoublyLinkedList:
    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self._size = 0
        if iterable:
            for x in iterable:
                self.append(x)

    def __len__(self):
        return self._size

    def __iter__(self):                    # forward
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next

    def backward(self):                    # reverse traversal -- DLL ka special power
        cur = self.tail
        while cur:
            yield cur.data
            cur = cur.prev

    def __str__(self):
        if not self.head:
            return "None (empty)"
        return "None <-> " + " <-> ".join(map(repr, self)) + " <-> None"

    def append(self, data):                            # O(1)
        node = DNode(data, prev=self.tail)             # naye node ka prev = purana tail
        if self.tail:
            self.tail.next = node                      # purane tail ka next = naya
        else:
            self.head = node                           # list khali thi
        self.tail = node
        self._size += 1
        return self

    def push_front(self, data):                        # O(1)
        node = DNode(data, next=self.head)
        if self.head:
            self.head.prev = node
        else:
            self.tail = node
        self.head = node
        self._size += 1
        return self

    def unlink(self, node):
        # DLL ka MOST IMPORTANT operation: node ka reference hath me hai -> O(1) delete
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next          # node head tha
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev          # node tail tha
        node.prev = node.next = None       # dangling pointers saaf karo (GC friendly)
        self._size -= 1
        return node.data

    def pop_back(self):
        if not self.tail:
            raise IndexError("empty")
        return self.unlink(self.tail)

    def pop_front(self):
        if not self.head:
            raise IndexError("empty")
        return self.unlink(self.head)

    def find(self, target):
        cur = self.head
        while cur:
            if cur.data == target:
                return cur                 # NODE return kar rahe hain (data nahi) -- taake unlink ho sake
            cur = cur.next
        return None


dll = DoublyLinkedList([1, 2, 3, 4])
print("dll          :", dll)
print("forward      :", list(dll))
print("backward     :", list(dll.backward()))
dll.push_front(0)
print("push_front(0):", dll)

mid = dll.find(2)                          # node ka reference mil gaya
dll.unlink(mid)                            # O(1) delete -- SLL me yeh O(n) hota
print("unlink(2)    :", dll)
print("pop_back     :", dll.pop_back(), "| pop_front:", dll.pop_front(), "->", dll)
print("len          :", len(dll))
"""))

# ============================================================
# 5. CIRCULAR LINKED LIST + JOSEPHUS
# ============================================================
cells.append(md("""
## 6. Circular Linked List

**Kya hai:** Aakhri node ka `next` `None` nahi — wapis `head` ko point karta hai. Loop banta hai.

```
   +----+     +----+     +----+
-->| 10 |---->| 20 |---->| 30 |--+
   +----+     +----+     +----+  |
     ^                           |
     +---------------------------+
```

**Kyun / kahan:**

- **Round-robin CPU scheduling** — har process ko turn milta hai, list khatam nahi hoti
- **Multiplayer game turns**, playlist "repeat all"
- **Circular buffer / ring buffer** ka conceptual base

**Sabse bara gotcha:** Traversal ka condition badal jata hai. `while cur:` **infinite loop** hai!
Sahi pattern:

```python
cur = head
while True:
    ...work...
    cur = cur.next
    if cur is head:      # ek chakkar poora ho gaya
        break
```

`do-while` jaisa pattern chahiye — kam az kam ek dafa chalo, phir head par rukk jao.
"""))

cells.append(code(r"""
class CircularLinkedList:
    # Hum sirf 'tail' rakhte hain: tail.next hamesha head hai -> append aur push_front dono O(1)
    def __init__(self, iterable=None):
        self.tail = None
        self._size = 0
        if iterable:
            for x in iterable:
                self.append(x)

    def __len__(self):
        return self._size

    @property
    def head(self):
        return self.tail.next if self.tail else None

    def __iter__(self):
        if self.tail is None:
            return
        cur = self.tail.next          # head se shuru
        while True:
            yield cur.data
            cur = cur.next
            if cur is self.tail.next:  # ek poora chakkar -> ruk jao
                break

    def __str__(self):
        if not self.tail:
            return "None (empty)"
        return " -> ".join(map(repr, self)) + " -> (back to head)"

    def append(self, data):           # tail ke baad, circle barqarar rakhte hue
        node = Node(data)
        if self.tail is None:
            node.next = node          # apne aap ko point kare (single node circle)
            self.tail = node
        else:
            node.next = self.tail.next   # naya node head ko point kare
            self.tail.next = node        # purana tail naye ko
            self.tail = node             # naya tail
        self._size += 1
        return self

    def push_front(self, data):
        # tail ke baad daalo lekin tail ko NA badlo -> naya node head ban jata hai. O(1)
        if self.tail is None:
            return self.append(data)
        self.tail.next = Node(data, self.tail.next)
        self._size += 1
        return self

    def rotate(self, k=1):
        # k dafa tail ko aage barhao = list "ghoom" gayi (round-robin ka core)
        for _ in range(k % max(self._size, 1)):
            self.tail = self.tail.next
        return self


cll = CircularLinkedList([1, 2, 3, 4, 5])
print("circular     :", cll)
print("head         :", cll.head, "| tail:", cll.tail, "| len:", len(cll))
print("tail.next is head?", cll.tail.next is cll.head)
cll.rotate(2)
print("rotate(2)    :", cll)

# 12 baar traverse karke dikhate hain ke list khatam nahi hoti (round robin)
cur = cll.head
seq = []
for _ in range(12):
    seq.append(cur.data)
    cur = cur.next
print("12 turns     :", seq)
"""))

cells.append(md("""
### Josephus Problem (circular list ka classic use)

**Problem:** `n` log ek circle me baithe hain (1..n). Har `k`-va banda circle se bahar
(eliminate) hota jata hai. Aakhir me kaun bacha? (**survivor** ka number batao.)

**Approach (simulation):** Circular linked list banao, `k-1` step chalo, agle node ko
unlink karo, wahin se dobara ginna shuru. Jab ek node bache — wohi survivor.

- **Time:** O(n·k) — simulation
- **Space:** O(n)

**Math shortcut:** `k == 2` ke liye formula hai: `2*L + 1` jahan `n = 2^m + L`.
Aur general recurrence: `J(1)=0`, `J(n) = (J(n-1) + k) % n` (0-indexed) — yeh **O(n) time, O(1) space**.
Dono neeche compare karte hain.
"""))

cells.append(code(r"""
def josephus_simulate(n, k):
    # ---- Circular list ki asli simulation ----
    if n <= 0:
        raise ValueError("n >= 1 hona chahiye")
    # circle banao: 1..n
    head = Node(1)
    cur = head
    for v in range(2, n + 1):
        cur.next = Node(v)
        cur = cur.next
    cur.next = head                     # circle band karo
    prev, cur = cur, head               # prev = tail (delete ke liye prev chahiye)

    while cur.next is not cur:          # jab tak ek se zyada node hain
        for _ in range(k - 1):          # k-1 step aage (k-va banda cur par aayega)
            prev, cur = cur, cur.next
        prev.next = cur.next            # cur ko circle se nikaal do
        cur = prev.next                 # ginti agle bande se dobara shuru
    return cur.data


def josephus_formula(n, k):
    # ---- Recurrence: J(1)=0, J(n) = (J(n-1)+k) % n  (0-indexed), aakhir me +1 ----
    ans = 0
    for m in range(2, n + 1):
        ans = (ans + k) % m
    return ans + 1


print("n=7,  k=3 -> survivor:", josephus_simulate(7, 3), "| formula:", josephus_formula(7, 3))
print("n=5,  k=2 -> survivor:", josephus_simulate(5, 2), "| formula:", josephus_formula(5, 2))
print("n=10, k=4 -> survivor:", josephus_simulate(10, 4), "| formula:", josephus_formula(10, 4))

# dono tareeqe hamesha same jawab dete hain -- verify
for n in range(1, 30):
    for k in range(1, 6):
        assert josephus_simulate(n, k) == josephus_formula(n, k), (n, k)
print("Simulation aur formula 1..29 x 1..5 tak match karte hain")
"""))

# ============================================================
# 6. DUMMY / SENTINEL
# ============================================================
cells.append(md("""
## 7. Dummy (Sentinel) Node Technique — **yeh sab se zyada kaam ki cheez hai**

**Masla:** Jab bhi head delete ya head par insert hota hai, code me `if prev is None:` jaisa
special case likhna parta hai. 80% linked-list bugs isi `if` me hote hain.

**Hal:** Ek **fake node** (dummy/sentinel) banao jo asli head se pehle lage:

```
dummy -> 1 -> 2 -> 3 -> None
```

Ab **har** node ke paas ek `prev` maujood hai — head ka bhi. Aakhir me `return dummy.next`.

**Kab use karo:**
- Nodes delete karte waqt (`remove elements`, `remove duplicates`)
- Do lists merge karte waqt (result banate hue)
- Partition, add-two-numbers, reorder — jahan naya list build ho raha ho

**Yaad rakhne wala muhavra:**

```python
dummy = Node(0)          # ya Node(0, head)
tail  = dummy            # jahan agla node lagana hai
...
tail.next = something
tail = tail.next
...
return dummy.next        # asli head
```

**Interview tip:** Solution me dummy use karte hue zor se kaho "sentinel node se head ka
special case khatam ho jata hai" — yeh seniority ki nishani hai.
"""))

cells.append(code(r"""
# ---- Bina dummy (special cases se bhara) vs dummy ke saath (saaf) ----

def remove_all_naive(head, val):
    # pehle head wale saare matching nodes hatao -- ALAG loop chahiye (yehi takleef hai)
    while head is not None and head.data == val:
        head = head.next
    cur = head
    while cur is not None and cur.next is not None:
        if cur.next.data == val:
            cur.next = cur.next.next        # skip
        else:
            cur = cur.next
    return head


def remove_all_dummy(head, val):
    # ---- dummy ke saath: sirf EK loop, koi special case nahi ----
    dummy = Node(0, head)                   # dummy asli head se pehle
    prev = dummy
    while prev.next is not None:
        if prev.next.data == val:
            prev.next = prev.next.next      # node hata do; prev wahin rehta hai
        else:
            prev = prev.next                # aage barho
    return dummy.next                       # naya head (head badla ho to bhi sahi)


def build(vals):
    # list -> linked list (raw Node chain), poore notebook me kaam aayega
    dummy = Node(0)
    t = dummy
    for v in vals:
        t.next = Node(v)
        t = t.next
    return dummy.next


def dump(head):
    # linked list -> python list
    out = []
    while head:
        out.append(head.data)
        head = head.next
    return out


print("dono functions same jawab dete hain:")
for vals, val in [([7, 7, 1, 7, 2, 7], 7), ([1, 2, 3], 9), ([5, 5, 5], 5), ([], 1)]:
    a = dump(remove_all_naive(build(vals), val))
    b = dump(remove_all_dummy(build(vals), val))
    print(f"  {vals} remove {val} -> naive={a} dummy={b}  {'OK' if a == b else 'MISMATCH'}")
    assert a == b
print("\nCode lines: naive me 2 loop + head special case; dummy me 1 loop. Dummy jeet gaya.")
"""))

# ============================================================
# 7. TWO POINTERS
# ============================================================
cells.append(md("""
## 8. Two-Pointer Techniques (Linked List ka dil)

Array me index arithmetic se kaam ho jata hai (`a[n//2]`). LL me **length pata nahi** aur
**random access nahi** — is liye do pointer chalate hain jo **mukhtalif raftaar** ya
**mukhtalif jagah se** chalte hain.

### Char (4) bunyadi flavours

| Flavour | Setup | Kaam |
|---|---|---|
| **Slow/Fast (1x, 2x)** | dono head par | middle nikalna, cycle detect karna, palindrome |
| **Gap (k ka faasla)** | fast ko k aage bhejo | nth from end, remove nth |
| **Two lists** | dono lists ke head par | merge, intersection |
| **Prev/Cur (ek peeche)** | prev=None, cur=head | reverse, delete |

**Kyun kaam karta hai:** Slow 1 step, fast 2 step → jab fast end par pohnche, slow **aadhe**
raste par hoga. Yeh "ek hi pass me length ka aadha" nikalne ka trick hai (2 pass ki jagah 1 pass).
"""))

cells.append(code(r"""
# ---- 1) MIDDLE nikalna (LC 876 ka core) ----
def middle_node(head):
    # slow 1 step, fast 2 step. even length par slow *doosra* middle par rukta hai.
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def middle_first(head):
    # agar EVEN length me PEHLA middle chahiye ho (split karte waqt zaroori hota hai)
    slow = head
    fast = head.next if head else None       # fast ko ek step aage se shuru karo
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


for vals in ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1], [1, 2]):
    h = build(vals)
    print(f"{vals}: second-middle={middle_node(h).data}, first-middle={middle_first(h).data}")

# ---- 2) Nth node FROM END (gap technique) ----
def nth_from_end(head, n):
    fast = head
    for _ in range(n):                       # fast ko n step aage bhejo
        if fast is None:
            return None                      # n list se bara hai
        fast = fast.next
    slow = head
    while fast is not None:                  # gap 'n' constant rehta hai
        slow, fast = slow.next, fast.next
    return slow                              # fast end par -> slow nth-from-end par


h = build([1, 2, 3, 4, 5])
print()
print("[1..5] 1st from end:", nth_from_end(h, 1).data)
print("[1..5] 3rd from end:", nth_from_end(h, 3).data)
print("[1..5] 5th from end:", nth_from_end(h, 5).data)
print("[1..5] 9th from end:", nth_from_end(h, 9))
"""))

cells.append(md("""
### 8.1 Floyd's Cycle Detection ("Tortoise and Hare") + cycle-start ka PROOF

**Detect karna:** slow 1x, fast 2x. Agar cycle hai to fast slow ko **pakar lega** (kyunki har
step par faasla 1 kam hota hai, aur circle me faasla wrap ho jata hai). Agar cycle nahi to
fast `None` par pohnch kar loop toot jayega.

**Cycle ka START dhoondna — yahan math zaroori hai:**

Maan lo:
- `L` = head se cycle-start tak ka faasla
- `C` = cycle ki lambai
- `x` = cycle-start se **meeting point** tak ka faasla

Meeting par:
- slow ne chala: `L + x`
- fast ne chala: `2(L + x)`
- fast ne slow se **poore chakkar** zyada kiye: `2(L+x) - (L+x) = L + x = n·C` (kisi integer n ke liye)

→ **`L + x = n·C`** → **`L = n·C - x`**

Iska matlab: agar ek pointer **head** se chale aur doosra **meeting point** se chale, dono
1 step par, to head wala `L` steps me cycle-start par pohnchega, aur meeting-point wala
`n·C - x` steps me... jo bhi `L` ke barabar hai → **dono cycle-start par milenge**. QED.

**Cycle ki LENGTH:** meeting point par ruk kar ek pointer ko ghumao jab tak wapis wahin aaye.

- **Time:** O(n) | **Space:** O(1) — hash-set wale hal (O(n) space) se behtar.
"""))

cells.append(code(r"""
def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:            # 'is' se compare karo (identity), == se NAHI
            return True
    return False


def cycle_start(head):
    # Phase 1: meeting point dhoondo
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            # Phase 2: ek pointer head se, doosra meeting se -> milne ki jagah = cycle start
            p = head
            while p is not slow:
                p, slow = p.next, slow.next
            return p
    return None


def cycle_length(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            n, cur = 1, slow.next
            while cur is not slow:      # ek chakkar gino
                n += 1
                cur = cur.next
            return n
    return 0


def make_cycle(vals, pos):
    # pos = us index par cycle jorna (-1 = koi cycle nahi). Testing helper.
    head = build(vals)
    if pos == -1 or head is None:
        return head
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    nodes[-1].next = nodes[pos]         # tail ko pos par joro
    return head


h1 = make_cycle([3, 2, 0, -4], 1)       # tail -> index 1 (value 2)
h2 = make_cycle([1, 2], 0)
h3 = make_cycle([1, 2, 3, 4], -1)

print("[3,2,0,-4] cycle at 1 -> has_cycle:", has_cycle(h1),
      "| start:", cycle_start(h1).data, "| length:", cycle_length(h1))
print("[1,2] cycle at 0      -> has_cycle:", has_cycle(h2),
      "| start:", cycle_start(h2).data, "| length:", cycle_length(h2))
print("[1,2,3,4] no cycle    -> has_cycle:", has_cycle(h3),
      "| start:", cycle_start(h3), "| length:", cycle_length(h3))

# Hash-set wala tareeqa (simple lekin O(n) space) -- comparison ke liye
def has_cycle_set(head):
    seen = set()
    cur = head
    while cur:
        if id(cur) in seen:      # id() use karo -- Node hashable hai lekin clarity ke liye
            return True
        seen.add(id(cur))
        cur = cur.next
    return False

print("\nset-based check (O(n) space):", has_cycle_set(h1), has_cycle_set(h3))
"""))

cells.append(md("""
### 8.2 Intersection of two lists (Y shape)

Do lists ek node par mil kar aage **shared** ho jati hain. Woh **exact node** (reference)
dhoondna hai — value nahi.

**3 tareeqe:**

1. **Set:** ek list ke saare node `id()` set me daalo, doosri me check karo → O(m+n) time, O(m) space
2. **Length difference:** dono ki length nikalo, lambi wali ko `|m-n|` aage bhejo, phir saath chalo → O(m+n) time, **O(1)** space
3. **Two-pointer switch (sabse elegant):** `a` khatam ho to `a = headB`, `b` khatam ho to `b = headA`.
   Dono ne barabar `m+n` chal liya → agar intersection hai to wahin milenge, warna dono `None` par.

**Interview me #3 likho** — ek loop, koi length calculation nahi.
"""))

cells.append(code(r"""
def get_intersection_switch(headA, headB):
    if not headA or not headB:
        return None
    a, b = headA, headB
    while a is not b:                 # identity compare
        a = a.next if a else headB    # a khatam -> B par switch
        b = b.next if b else headA    # b khatam -> A par switch
    return a                          # ya to common node, ya dono None (koi intersection nahi)


def get_intersection_len(headA, headB):
    def length(h):
        n = 0
        while h:
            n, h = n + 1, h.next
        return n
    la, lb = length(headA), length(headB)
    a, b = headA, headB
    for _ in range(la - lb if la > lb else 0):
        a = a.next
    for _ in range(lb - la if lb > la else 0):
        b = b.next
    while a is not b:
        a, b = a.next, b.next
    return a


# Y shape banao: A = 4->1->[8->4->5], B = 5->6->1->[8->4->5]
shared = build([8, 4, 5])
A = build([4, 1]); A.next.next = shared
B = build([5, 6, 1]); B.next.next.next = shared

for fn in (get_intersection_switch, get_intersection_len):
    node = fn(A, B)
    print(f"{fn.__name__:26s} -> {node.data if node else None}")

# koi intersection nahi wala case
P, Q = build([2, 6, 4]), build([1, 5])
print("no intersection ->", get_intersection_switch(P, Q), get_intersection_len(P, Q))
assert get_intersection_switch(A, B) is shared
assert get_intersection_switch(P, Q) is None
print("asserts pass")
"""))

# ============================================================
# 8. REVERSE
# ============================================================
cells.append(md("""
## 9. Reverse — Char Tareeqe (yeh #1 interview sawaal hai)

### 9.1 Iterative (3 pointer) — **yeh zaroor yaad karo**

```
prev = None,  cur = head
loop:
    nxt  = cur.next     # (1) agla bachao warna kho jayega
    cur.next = prev     # (2) teer ulta kar do
    prev = cur          # (3) prev aage
    cur  = nxt          # (4) cur aage
return prev             # prev naya head hai
```

Order badal dia to list **toot** jayegi — pehle `nxt` bachana **lazmi** hai.

- **Time:** O(n) | **Space:** O(1) ← best

### 9.2 Recursive

Base: khali ya single node → wohi head. Warna: baaki list reverse karao, phir apne aap ko
uske **aakhir me** lagao.

- **Time:** O(n) | **Space:** O(n) — call stack (n=10^5 par Python me `RecursionError`!)

### 9.3 K-groups aur 9.4 Between positions
Neeche code me — dono me **dummy node** ka jadoo dekho.
"""))

cells.append(code(r"""
def reverse_iterative(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next        # (1) agla mehfooz karo
        cur.next = prev       # (2) teer ulta
        prev = cur            # (3)
        cur = nxt             # (4)
    return prev               # naya head


def reverse_recursive(head):
    if head is None or head.next is None:
        return head                       # base: 0 ya 1 node
    new_head = reverse_recursive(head.next)   # baaki reverse ho gaya
    head.next.next = head                 # jo mera agla tha, woh ab mujhe point kare
    head.next = None                      # main naya tail hoon
    return new_head


def reverse_between(head, left, right):
    # 1-indexed: position left..right ko reverse karo (LC 92)
    if head is None or left == right:
        return head
    dummy = Node(0, head)                 # dummy = left==1 ka case khatam
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next                  # prev = reverse hone wale hisse se pehle wala node
    cur = prev.next                       # yeh reverse ke baad TAIL banega
    for _ in range(right - left):
        # "head insertion" trick: cur.next ko utha kar prev ke foran baad daal do
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next


def reverse_k_group(head, k):
    # har k ke group ko reverse karo; aakhri adhoora group waise hi rehne do (LC 25)
    # pehle gino ke k node maujood hain ya nahi
    node, count = head, 0
    while node and count < k:
        node, count = node.next, count + 1
    if count < k:
        return head                       # adhoora group -> chhor do
    # pehle k nodes reverse karo, phir baaki recursively
    prev = reverse_k_group(node, k)       # 'node' = (k+1)-va node
    cur = head
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


print("original       :", dump(build([1, 2, 3, 4, 5])))
print("iterative      :", dump(reverse_iterative(build([1, 2, 3, 4, 5]))))
print("recursive      :", dump(reverse_recursive(build([1, 2, 3, 4, 5]))))
print("between(2,4)   :", dump(reverse_between(build([1, 2, 3, 4, 5]), 2, 4)))
print("between(1,5)   :", dump(reverse_between(build([1, 2, 3, 4, 5]), 1, 5)))
print("k_group(k=2)   :", dump(reverse_k_group(build([1, 2, 3, 4, 5]), 2)))
print("k_group(k=3)   :", dump(reverse_k_group(build([1, 2, 3, 4, 5]), 3)))
print("edge: empty    :", dump(reverse_iterative(build([]))), "| single:", dump(reverse_iterative(build([9]))))

assert dump(reverse_iterative(build([1, 2, 3]))) == [3, 2, 1]
assert dump(reverse_recursive(build([1, 2, 3]))) == [3, 2, 1]
assert dump(reverse_between(build([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5]
assert dump(reverse_k_group(build([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
print("sab reverse asserts pass")
"""))

# ============================================================
# 9. MERGE + SORT
# ============================================================
cells.append(md("""
## 10. Merge aur Sort

### 10.1 Merge two sorted lists
Dono lists par ek-ek pointer, chhoti value ko result me lagao. **Dummy node** se code aadha ho jata hai.
- Time: O(m+n), Space: O(1) (nodes re-link kar rahe hain, naye nahi bana rahe)

### 10.2 Merge k sorted lists — **min-heap**
Heap me har list ka current head daalo (`(value, list_index, node)`). Sabse chhota nikalo,
result me lagao, us list ka agla node heap me daalo.
- Time: **O(N log k)** jahan N = total nodes, k = lists
- Space: O(k)
- *Alternative:* pairwise merge (divide & conquer) — bhi O(N log k)

**Tuple me `list_index` kyun?** Kyunki agar do values barabar hon to Python `Node` objects ko
compare karne ki koshish karega → `TypeError: '<' not supported between Node instances`.
Index tie-breaker ka kaam karta hai. **Yeh classic interview gotcha hai.**

### 10.3 Linked list ko sort karna → **Merge Sort**
- **Quick sort LL par bura hai** (random access nahi, pivot partition mehnga)
- **Merge sort perfect hai**: split (slow/fast se middle), recursively sort, merge
- Time: O(n log n) | Space: O(log n) recursion stack (array merge sort ke O(n) buffer se behtar!)
""" ))

cells.append(code(r"""
import heapq


def merge_two_sorted(a, b):
    dummy = Node(0)                 # sentinel: result ka fake head
    tail = dummy
    while a and b:
        if a.data <= b.data:        # <= use karo taake stable rahe
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b              # jo bachi hui list hai woh chipka do (ek O(1) move)
    return dummy.next


def merge_k_sorted(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            # (value, i, node) -- 'i' tie-breaker, warna Node compare hoga -> TypeError
            heapq.heappush(heap, (node.data, i, node))
    dummy = Node(0)
    tail = dummy
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.data, i, node.next))
    tail.next = None                # zaroori: purani links tor do
    return dummy.next


def sort_list(head):
    # ---- Merge sort on linked list ----
    if head is None or head.next is None:
        return head                          # base case
    # 1) middle par tor do (pehla middle chahiye taake dono hisse non-empty rahen)
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid = slow.next
    slow.next = None                         # link kaato -> do alag lists
    # 2) dono halves sort karo
    left = sort_list(head)
    right = sort_list(mid)
    # 3) merge
    return merge_two_sorted(left, right)


print("merge_two   :", dump(merge_two_sorted(build([1, 3, 5]), build([2, 4, 6]))))
print("merge_two   :", dump(merge_two_sorted(build([]), build([0]))))
lists = [build([1, 4, 5]), build([1, 3, 4]), build([2, 6])]
print("merge_k     :", dump(merge_k_sorted(lists)))
print("merge_k []  :", dump(merge_k_sorted([])))
print("sort_list   :", dump(sort_list(build([4, 2, 1, 3]))))
print("sort_list   :", dump(sort_list(build([-1, 5, 3, 4, 0]))))

assert dump(merge_two_sorted(build([1, 2, 4]), build([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
assert dump(merge_k_sorted([build([1, 4, 5]), build([1, 3, 4]), build([2, 6])])) == [1, 1, 2, 3, 4, 4, 5, 6]
assert dump(sort_list(build([4, 2, 1, 3]))) == [1, 2, 3, 4]
print("merge/sort asserts pass")
"""))

# ============================================================
# 10. DUPLICATES / PALINDROME / ADD / PARTITION
# ============================================================
cells.append(md("""
## 11. Duplicates Hatana

| Case | Tareeqa | Time | Space |
|---|---|---|---|
| **Sorted**, ek copy rakhni hai (LC 83) | `cur.data == cur.next.data` → skip | O(n) | O(1) |
| **Sorted**, duplicates **poore** hatane hain (LC 82) | dummy + prev; group detect kar ke poora group skip | O(n) | O(1) |
| **Unsorted**, ek copy rakhni hai | `set` me seen values | O(n) | O(n) |
| **Unsorted**, O(1) space chahiye | nested loop | O(n²) | O(1) |

**Gotcha (LC 82):** Yahan dummy **lazmi** hai, kyunki head khud bhi duplicate ho sakta hai
(`[1,1,2]` → `[2]`).
""" ))

cells.append(code(r"""
def dedup_sorted_keep_one(head):
    # [1,1,2,3,3] -> [1,2,3]
    cur = head
    while cur and cur.next:
        if cur.data == cur.next.data:
            cur.next = cur.next.next      # duplicate skip; cur wahin rehta hai (aur bhi ho sakte hain)
        else:
            cur = cur.next
    return head


def dedup_sorted_remove_all(head):
    # [1,2,3,3,4,4,5] -> [1,2,5]   (duplicate wali saari values ghayab)
    dummy = Node(0, head)
    prev = dummy                          # prev = aakhri "confirmed unique" node
    cur = head
    while cur:
        # group ka size check karo
        if cur.next and cur.next.data == cur.data:
            val = cur.data
            while cur and cur.data == val:    # poora group aage skip
                cur = cur.next
            prev.next = cur                   # prev ko group ke baad wale se joro
        else:
            prev = cur                        # unique tha -> prev aage
            cur = cur.next
    return dummy.next


def dedup_unsorted_set(head):
    # unsorted: seen set (O(n) space)
    if not head:
        return head
    seen = {head.data}
    cur = head
    while cur.next:
        if cur.next.data in seen:
            cur.next = cur.next.next
        else:
            seen.add(cur.next.data)
            cur = cur.next
    return head


def dedup_unsorted_no_space(head):
    # O(1) space, O(n^2) time -- "follow up: bina buffer?" ka jawab
    cur = head
    while cur:
        runner = cur
        while runner.next:
            if runner.next.data == cur.data:
                runner.next = runner.next.next
            else:
                runner = runner.next
        cur = cur.next
    return head


print("keep_one   [1,1,2,3,3]      ->", dump(dedup_sorted_keep_one(build([1, 1, 2, 3, 3]))))
print("remove_all [1,2,3,3,4,4,5]  ->", dump(dedup_sorted_remove_all(build([1, 2, 3, 3, 4, 4, 5]))))
print("remove_all [1,1,1,2,3]      ->", dump(dedup_sorted_remove_all(build([1, 1, 1, 2, 3]))))
print("remove_all [1,1]            ->", dump(dedup_sorted_remove_all(build([1, 1]))))
print("unsorted set  [3,1,3,2,1]   ->", dump(dedup_unsorted_set(build([3, 1, 3, 2, 1]))))
print("unsorted O(1) [3,1,3,2,1]   ->", dump(dedup_unsorted_no_space(build([3, 1, 3, 2, 1]))))
"""))

cells.append(md("""
## 12. Palindrome Check (O(1) space)

**Steps:** (1) middle nikalo slow/fast se, (2) doosra half **reverse** karo,
(3) dono halves compare karo, (4) *achhi practice:* list ko **wapis restore** kar do.

- Time: O(n) | Space: **O(1)**
- Simple tareeqa: values `list` me daal kar `vals == vals[::-1]` → O(n) space (interview me
  pehle yeh batao, phir optimal karo)

**Gotcha:** Odd length me middle node koi farq nahi daalta — comparison us se pehle ruk jata hai.
""" ))

cells.append(code(r"""
def is_palindrome_simple(head):
    vals = dump(head)                 # O(n) space
    return vals == vals[::-1]


def is_palindrome(head):
    if head is None or head.next is None:
        return True
    # 1) pehla middle dhoondo
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    # 2) second half reverse karo
    second = reverse_iterative(slow.next)
    slow.next = None
    # 3) compare
    p, q, ok = head, second, True
    while q:                          # second half chhota ya barabar hota hai
        if p.data != q.data:
            ok = False
            break
        p, q = p.next, q.next
    # 4) list restore (input ko kharab na chhoro -- senior habit)
    slow.next = reverse_iterative(second)
    return ok


for vals in ([1, 2, 2, 1], [1, 2], [1], [], [1, 2, 3, 2, 1], [1, 2, 3]):
    h = build(vals)
    r = is_palindrome(h)
    print(f"{str(vals):16s} palindrome? {r}   (restore ke baad list: {dump(h)})")
    assert r == is_palindrome_simple(build(vals))
print("palindrome asserts pass")
"""))

cells.append(md("""
## 13. Add Two Numbers (linked list me digits)

Digits **reverse order** me hote hain (`342` → `2->4->3`), is liye head se hi add karna
seedha hai — **carry** aage le jao.

**Muhavra:**
```python
total = (a.data if a else 0) + (b.data if b else 0) + carry
carry, digit = divmod(total, 10)
```
Loop condition `while a or b or carry` — **carry ko bhoolna sabse common bug hai**
(`[9,9] + [1]` → `[0,0,1]`).
""" ))

cells.append(code(r"""
def add_two_numbers(l1, l2):
    dummy = Node(0)
    tail = dummy
    carry = 0
    while l1 or l2 or carry:               # carry bhi condition me -- yeh yaad rakho
        total = (l1.data if l1 else 0) + (l2.data if l2 else 0) + carry
        carry, digit = divmod(total, 10)   # divmod = (quotient, remainder) ek hi call me
        tail.next = Node(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next


print("342 + 465 = 807 ->", dump(add_two_numbers(build([2, 4, 3]), build([5, 6, 4]))))
print("0 + 0           ->", dump(add_two_numbers(build([0]), build([0]))))
print("9999999 + 9999  ->", dump(add_two_numbers(build([9]*7), build([9]*4))))
assert dump(add_two_numbers(build([2, 4, 3]), build([5, 6, 4]))) == [7, 0, 8]
assert dump(add_two_numbers(build([9, 9]), build([1]))) == [0, 0, 1]
print("add asserts pass")
"""))

cells.append(md("""
## 14. Partition List

`x` diya hai: saare nodes jo `< x` hain woh **pehle**, baqi baad me — aur **relative order**
barqarar rahe (stable).

**Trick:** **Do dummy lists** banao (`less` aur `greater_equal`), ek pass me nodes baant do,
aakhir me jor do. Yeh "two-bucket" pattern quicksort partition aur stable sort me bhi aata hai.

- Time: O(n) | Space: O(1)
""" ))

cells.append(code(r"""
def partition(head, x):
    less_d, ge_d = Node(0), Node(0)         # do dummy heads
    less, ge = less_d, ge_d
    while head:
        if head.data < x:
            less.next = head
            less = less.next
        else:
            ge.next = head
            ge = ge.next
        head = head.next
    ge.next = None                          # ZAROORI: warna purani link se cycle ban sakta hai
    less.next = ge_d.next                   # do buckets jor do
    return less_d.next


print("[1,4,3,2,5,2] x=3 ->", dump(partition(build([1, 4, 3, 2, 5, 2]), 3)))
print("[2,1] x=2         ->", dump(partition(build([2, 1]), 2)))
print("[] x=0            ->", dump(partition(build([]), 0)))
assert dump(partition(build([1, 4, 3, 2, 5, 2]), 3)) == [1, 2, 2, 4, 3, 5]
print("partition assert pass")
"""))

cells.append(md("""
## 15. Copy List with Random Pointer (deep copy)

Har node ke paas `next` ke ilawa ek `random` pointer bhi hai jo **kisi bhi** node (ya `None`)
ko point kar sakta hai. Poori list ka **deep copy** banao.

**Masla:** Jab naya node banate ho to uska `random` kis naye node ko point kare? Purana random
target ka **naya version** to abhi bana bhi nahi.

**Hal 1 — HashMap (old node → new node), 2 pass:** O(n) time, O(n) space. Aasan, likhne layaq.

**Hal 2 — Interleaving (O(1) extra space), 3 pass:**
1. Har original node ke **foran baad** uski copy daal do: `A->A'->B->B'->C->C'`
2. `A'.random = A.random.next` (kyunki `A.random.next` hi us node ki copy hai) — genius step
3. Do lists ko alag (unweave) kar do

Interview me #1 likho, #2 ka zikr karo → strong signal.
""" ))

cells.append(code(r"""
class RNode:
    # next + random pointer wala node (LC 138)
    __slots__ = ("val", "next", "random")

    def __init__(self, val, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_map(head):
    # ---- Hal 1: hashmap old->new ----
    if not head:
        return None
    mapping = {}
    cur = head
    while cur:                                  # pass 1: sab nodes ki copy (bina pointers)
        mapping[cur] = RNode(cur.val)
        cur = cur.next
    cur = head
    while cur:                                  # pass 2: pointers set karo (map se)
        mapping[cur].next = mapping.get(cur.next)      # .get -> None safe
        mapping[cur].random = mapping.get(cur.random)
        cur = cur.next
    return mapping[head]


def copy_random_interleave(head):
    # ---- Hal 2: O(1) extra space, 3 pass ----
    if not head:
        return None
    cur = head
    while cur:                                  # pass 1: A->A'->B->B'
        cur.next = RNode(cur.val, cur.next)
        cur = cur.next.next
    cur = head
    while cur:                                  # pass 2: random assign
        if cur.random:
            cur.next.random = cur.random.next   # random target ki copy = target.next
        cur = cur.next.next
    new_head = head.next
    cur = head
    while cur:                                  # pass 3: unweave (dono lists alag)
        copy = cur.next
        cur.next = copy.next
        copy.next = copy.next.next if copy.next else None
        cur = cur.next
    return new_head


def build_random(vals, random_idx):
    # helper: values + random indices (None allowed) se RNode list banao
    nodes = [RNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    for i, ri in enumerate(random_idx):
        nodes[i].random = nodes[ri] if ri is not None else None
    return nodes[0] if nodes else None


def dump_random(head):
    # (val, random ka val) ki list -- comparison ke liye
    out, cur = [], head
    while cur:
        out.append((cur.val, cur.random.val if cur.random else None))
        cur = cur.next
    return out


vals, ridx = [7, 13, 11, 10, 1], [None, 0, 4, 2, 0]
for fn in (copy_random_map, copy_random_interleave):
    orig = build_random(vals, ridx)
    cp = fn(orig)
    print(f"{fn.__name__:24s} ->", dump_random(cp))
    assert dump_random(cp) == dump_random(build_random(vals, ridx))
    # deep copy hone ka saboot: koi bhi node shared nahi
    a, b = cp, build_random(vals, ridx)
    assert a is not b
print("copy-random asserts pass (dono tareeqe identical structure dete hain)")
"""))

# ============================================================
# 11. LRU CACHE
# ============================================================
cells.append(md("""
## 16. DLL ka Asli Real-World Role: **LRU Cache**

**Requirement:** `get` aur `put` dono **O(1)** me. Capacity bhar jaye to **Least Recently Used**
item nikal do.

**Kyun DLL + HashMap?**

| Zaroorat | Kaun poori karta hai |
|---|---|
| key se O(1) me node dhoondna | **HashMap** (`dict[key] = node`) |
| node ko O(1) me apni jagah se nikaalna | **DLL** (`prev` maloom hai → `unlink` O(1)) |
| "sab se purana" O(1) me milna | DLL ka **tail** (ya head, order ki marzi) |
| "abhi use hua" ko front par lana | DLL me unlink + push_front, dono O(1) |

**SLL se yeh kaam nahi ho sakta** — SLL me node ka `prev` dhoondne ke liye O(n) chalna parta hai.
**Yeh interview me poocha jane wala #1 "DLL kyun?" ka jawab hai.**

**Note:** Python me `collections.OrderedDict` (ya `dict` + `move_to_end`) andar se yehi
DLL+hashmap hi hai — is liye `OrderedDict.move_to_end()` O(1) hai.

Neeche **sentinel head+tail** wala clean implementation (dummy nodes se koi `if None` check nahi).
""" ))

cells.append(code(r"""
class LRUCache:
    # DLL + dict. head ke paas = sab se naya, tail ke paas = sab se purana.
    class _N:
        __slots__ = ("key", "val", "prev", "next")

        def __init__(self, key=None, val=None):
            self.key, self.val = key, val
            self.prev = self.next = None

    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                       # key -> node
        # do sentinel nodes: h <-> t (khali cache). Isse insert/remove me koi None check nahi
        self.h, self.t = self._N(), self._N()
        self.h.next, self.t.prev = self.t, self.h

    def _remove(self, node):                # O(1) -- DLL ka jadoo
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):             # head sentinel ke foran baad
        node.next = self.h.next
        node.prev = self.h
        self.h.next.prev = node
        self.h.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)                  # apni jagah se nikaalo...
        self._add_front(node)               # ...aur front par lagao (recently used)
        return node.val

    def put(self, key, val):
        if key in self.map:
            node = self.map[key]
            node.val = val
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) >= self.cap:
            lru = self.t.prev               # tail sentinel se pehla = least recently used
            self._remove(lru)
            del self.map[lru.key]           # map se bhi hatao -- warna memory leak
        node = self._N(key, val)
        self.map[key] = node
        self._add_front(node)

    def state(self):
        # MRU se LRU tak keys (debugging/teaching ke liye)
        out, cur = [], self.h.next
        while cur is not self.t:
            out.append(cur.key)
            cur = cur.next
        return out


c = LRUCache(2)
c.put(1, 1); print("put(1,1)  order(MRU->LRU):", c.state())
c.put(2, 2); print("put(2,2)  order:", c.state())
print("get(1) ->", c.get(1), " order:", c.state())
c.put(3, 3); print("put(3,3)  order:", c.state(), "(2 evict ho gaya)")
print("get(2) ->", c.get(2), "(-1 = nahi mila)")
c.put(4, 4); print("put(4,4)  order:", c.state())
print("get(1) ->", c.get(1), "| get(3) ->", c.get(3), "| get(4) ->", c.get(4))

assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
print("LRU asserts pass")

# Python ka built-in bhi wahi kaam karta hai (comparison)
from collections import OrderedDict
od = OrderedDict([(1, 'a'), (2, 'b'), (3, 'c')])
od.move_to_end(1)                       # O(1) -- kyunki andar DLL hai
print("\nOrderedDict move_to_end(1) ->", list(od.keys()))
print("popitem(last=False) [LRU]  ->", od.popitem(last=False))
"""))

# ============================================================
# 12. COMMON BUGS
# ============================================================
cells.append(md("""
## 17. Common Bugs / Gotchas (yahan har student phasta hai)

| # | Bug | Nateeja | Fix |
|---|---|---|---|
| 1 | `cur.next = prev` se pehle `nxt = cur.next` bhoolna | baqi list kho gayi | pehle `nxt` bachao |
| 2 | Loop me `cur = cur.next` bhoolna | **infinite loop** / hang | har loop me pointer aage barhao |
| 3 | `while cur.next:` jab `cur` `None` ho sakta hai | `AttributeError: 'NoneType' has no 'next'` | `while cur and cur.next:` |
| 4 | Head delete karte waqt special case | galat output ya crash | **dummy node** |
| 5 | Tail delete par `self.tail` update na karna | `tail` dangling node par → append toot gaya | delete me `if victim is self.tail: self.tail = prev` |
| 6 | Node compare `==` se karna (`cycle`/`intersection` me) | galat True/False | **`is`** use karo (identity) |
| 7 | Partition/merge me aakhri `tail.next = None` na karna | **cycle** ban gaya, `dump()` hang | end par `None` set karo |
| 8 | Recursion se n=10⁵ par reverse | `RecursionError` | iterative likho |
| 9 | Heap me `(value, node)` push karna | `TypeError: '<' not supported between Node` | tie-breaker index daalo |
| 10 | `_size` counter update bhoolna | `len()` jhoot bolne laga | ek hi jagah se update karo |
| 11 | `k` rotate/group me `k > n` handle na karna | index error / galat jawab | `k %= n` |
| 12 | Deleted node ke `prev/next` saaf na karna (DLL) | GC nahi ho paya / dangling | `node.prev = node.next = None` |

**Sabse zaroori teaching point:** LL ke bugs **silently galat** nahi hote — woh **hang** ya
**crash** karte hain. Is liye har solution ko chhote edge cases par test karo:
`[]`, `[1]`, `[1,2]`, aur "head hi target hai" wala case.
""" ))

cells.append(code(r"""
# ---- Bug 3 aur Bug 2 ko live dekhte hain (safe try/except me) ----

def buggy_length(head):
    n = 0
    cur = head
    while cur.next:              # BUG: cur None ho sakta hai (khali list)
        n += 1
        cur = cur.next
    return n

try:
    print(buggy_length(build([])))
except AttributeError as e:
    print("Bug 3 (khali list):", type(e).__name__, "-", e)

def fixed_length(head):
    n, cur = 0, head
    while cur is not None:       # sahi condition
        n, cur = n + 1, cur.next
    return n

print("fixed_length([]) =", fixed_length(build([])), "| fixed_length([1,2,3]) =", fixed_length(build([1, 2, 3])))

# ---- Bug 7: tail.next = None na karne se cycle ban jata hai ----
a = build([1, 2, 3])
b = build([4, 5])
a.next.next.next = b             # jor diya
b.next.next = a                  # GALTI: wapis a par -> cycle!
print("\ncycle ban gaya? ->", has_cycle(a), " (dump() infinite loop karta, is liye chalaya nahi)")

# ---- Bug 6: == vs is ----
x, y = Node(5), Node(5)
print("\nx == y ?", x == y, "(default __eq__ = identity, is liye False)")
print("x is y ?", x is y)
print("Sabaq: cycle/intersection me hamesha 'is' likho -- agar kisi ne __eq__ define kar dia to == dhoka de sakta hai")
"""))

# ============================================================
# 13. REAL WORLD PROBLEMS
# ============================================================
cells.append(md("""
## 18. Real-World Problems (linked list se hal)

1. **Music player playlist** — next/prev track, "repeat all" (circular DLL)
2. **Browser history** — back/forward (DLL)
3. **Text editor undo/redo** — do stacks ya DLL
4. **Round-robin task scheduler** — circular list
5. **Sparse polynomial** — sirf non-zero terms store karo (memory bachat)
6. **Version chain / blockchain-ish log** — har entry pichle ka reference

Har ek ka chalta hua code neeche.
""" ))

cells.append(code(r"""
# ---- 1) Music Player: circular DLL playlist ----
class Playlist:
    class _T:
        __slots__ = ("title", "prev", "next")
        def __init__(self, title):
            self.title = title
            self.prev = self.next = None

    def __init__(self, titles=()):
        self.cur = None
        self._n = 0
        for t in titles:
            self.add(t)

    def add(self, title):
        node = self._T(title)
        if self.cur is None:
            node.prev = node.next = node        # single node circle
            self.cur = node
        else:
            last = self.cur.prev                # circle me cur ka prev = aakhri track
            last.next = node
            node.prev = last
            node.next = self.cur
            self.cur.prev = node
        self._n += 1
        return self

    def next_track(self):
        self.cur = self.cur.next                # "repeat all" khud ba khud kaam karta hai
        return self.cur.title

    def prev_track(self):
        self.cur = self.cur.prev
        return self.cur.title

    def now_playing(self):
        return self.cur.title


pl = Playlist(["Afreen", "Sayonee", "Neend", "Bandeya"])
print("now playing :", pl.now_playing())
print("next x3     :", [pl.next_track() for _ in range(3)])
print("next (wrap) :", pl.next_track(), "<- circle wapis shuru par")
print("prev x2     :", [pl.prev_track() for _ in range(2)])
"""))

cells.append(code(r"""
# ---- 2) Browser History (DLL) ----
class BrowserHistory:
    def __init__(self, homepage):
        self.cur = DNode(homepage)              # pehle banayi hui DNode class reuse

    def visit(self, url):
        node = DNode(url, prev=self.cur)
        self.cur.next = node                    # forward history mit jati hai (real browser jaisa)
        self.cur = node
        return self

    def back(self, steps=1):
        while steps and self.cur.prev:
            self.cur = self.cur.prev
            steps -= 1
        return self.cur.data

    def forward(self, steps=1):
        while steps and self.cur.next:
            self.cur = self.cur.next
            steps -= 1
        return self.cur.data


bh = BrowserHistory("bizee.com")
bh.visit("bizee.com/pricing").visit("bizee.com/blog").visit("bizee.com/blog/dsa")
print("current      :", bh.cur.data)
print("back(2)      :", bh.back(2))
print("forward(1)   :", bh.forward(1))
print("back(10)     :", bh.back(10), "(homepage se aage peeche nahi ja sakte)")
bh.visit("bizee.com/new")
print("visit ke baad forward(1):", bh.forward(1), "(purani forward history khatam)")


# ---- 3) Undo/Redo (do stacks, jo andar se LL bhi ho sakte hain) ----
class Editor:
    def __init__(self):
        self.text = ""
        self._undo = []      # (action) stack
        self._redo = []

    def type(self, s):
        self._undo.append(self.text)   # purani halat save
        self._redo.clear()             # naya action -> redo chain toot gaya
        self.text += s
        return self

    def undo(self):
        if self._undo:
            self._redo.append(self.text)
            self.text = self._undo.pop()
        return self.text

    def redo(self):
        if self._redo:
            self._undo.append(self.text)
            self.text = self._redo.pop()
        return self.text


ed = Editor().type("Salam ").type("Duniya").type("!")
print("\ntext        :", repr(ed.text))
print("undo        :", repr(ed.undo()))
print("undo        :", repr(ed.undo()))
print("redo        :", repr(ed.redo()))
"""))

cells.append(code(r"""
# ---- 4) Round-robin scheduler ----
def round_robin(tasks, quantum, total_time):
    # tasks: {name: burst_time}. Circular list se turn-by-turn CPU dete hain.
    cl = CircularLinkedList([[name, bt] for name, bt in tasks.items()])
    log, t = [], 0
    cur = cl.tail                          # tail se shuru -> cur.next = head
    remaining = len(tasks)
    while remaining and t < total_time:
        cur = cur.next
        name, bt = cur.data
        if bt <= 0:
            continue                       # yeh task khatam ho chuka, skip
        run = min(quantum, bt)
        cur.data[1] -= run
        t += run
        log.append(f"t={t - run}-{t}: {name} (baqi {cur.data[1]})")
        if cur.data[1] == 0:
            remaining -= 1
    return log


for line in round_robin({"A": 5, "B": 3, "C": 4}, quantum=2, total_time=100):
    print(line)


# ---- 5) Sparse polynomial: 5x^100 + 3x^2 + 7 ----
def poly_from_terms(terms):
    # terms: [(coeff, power)] descending power. Sirf non-zero terms -> memory bachat
    return build(terms)                    # Node ka data ek tuple

def poly_str(head):
    parts = []
    while head:
        c, p = head.data
        parts.append(f"{c}x^{p}" if p else f"{c}")
        head = head.next
    return " + ".join(parts)

def poly_eval(head, x):
    total = 0
    while head:
        c, p = head.data
        total += c * (x ** p)
        head = head.next
    return total

poly = poly_from_terms([(5, 3), (3, 2), (7, 0)])
print("\npolynomial :", poly_str(poly))
print("x=2 par    :", poly_eval(poly, 2), "(5*8 + 3*4 + 7 = 59)")
print("Dense array me x^3 ke liye 4 slots chahiye; x^100 hota to 101 slots -- LL me sirf 3 nodes.")
"""))

# ============================================================
# 14. LEETCODE SECTION
# ============================================================
cells.append(md("""
# 19. LeetCode Problems (19 problems)

LeetCode par node class ka naam **`ListNode`** hota hai aur field **`val`** (humari `Node` me
`data` tha). Neeche wale cell me exactly LeetCode wali class + helpers bana rahe hain, taake
solutions **copy-paste ready** hon.

| LC | Title | Difficulty | Pattern |
|---|---|---|---|
| 206 | Reverse Linked List | Easy | 3-pointer reverse |
| 21 | Merge Two Sorted Lists | Easy | dummy + two pointers |
| 141 | Linked List Cycle | Easy | Floyd |
| 142 | Linked List Cycle II | Medium | Floyd + math |
| 876 | Middle of the Linked List | Easy | slow/fast |
| 19 | Remove Nth Node From End of List | Medium | gap + dummy |
| 234 | Palindrome Linked List | Easy | middle + reverse |
| 160 | Intersection of Two Linked Lists | Easy | pointer switch |
| 143 | Reorder List | Medium | middle + reverse + merge |
| 2 | Add Two Numbers | Medium | carry |
| 83 | Remove Duplicates from Sorted List | Easy | skip |
| 82 | Remove Duplicates from Sorted List II | Medium | dummy + group skip |
| 92 | Reverse Linked List II | Medium | dummy + head-insert |
| 148 | Sort List | Medium | merge sort |
| 61 | Rotate List | Medium | k %= n + split |
| 138 | Copy List with Random Pointer | Medium | hashmap / interleave |
| 24 | Swap Nodes in Pairs | Medium | dummy + local swap |
| 23 | Merge k Sorted Lists | Hard | min-heap |
| 707 | Design Linked List | Medium | full implementation |
""" ))

cells.append(code(r"""
# ---- LeetCode style node + helpers (LC section me yehi use honge) ----
class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def to_ll(vals):
    # python list -> ListNode chain
    dummy = ListNode()
    t = dummy
    for v in vals:
        t.next = ListNode(v)
        t = t.next
    return dummy.next


def to_py(head, limit=10000):
    # ListNode chain -> python list (limit = cycle se bachne ke liye safety)
    out = []
    while head and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out


def ll_cycle(vals, pos):
    # pos par cycle jorne wala helper (-1 = no cycle)
    head = to_ll(vals)
    if pos == -1 or head is None:
        return head
    nodes, cur = [], head
    while cur:
        nodes.append(cur)
        cur = cur.next
    nodes[-1].next = nodes[pos]
    return head


print("to_ll/to_py test :", to_py(to_ll([1, 2, 3])))
print("helpers ready")
"""))

cells.append(md("""
### LC 206. Reverse Linked List — Easy
https://leetcode.com/problems/reverse-linked-list/

**Problem (Roman Urdu):** Ek singly linked list ka head diya hai. Poori list **ulti** kar do
aur naya head return karo.

**Approach (iterative, 3 pointer):**
1. `prev = None`, `cur = head`
2. Har step: `nxt` bachao → `cur.next = prev` (teer ulta) → `prev = cur` → `cur = nxt`
3. Jab `cur is None`, `prev` naya head hai

**Recursive:** `head.next` se aage reverse karao, phir `head.next.next = head`, `head.next = None`.

**Time:** O(n) — ek pass
**Space:** O(1) iterative | O(n) recursive (call stack)
""" ))

cells.append(code(r"""
def reverseList(head):
    # --- Iterative: interview me yehi likho (O(1) space) ---
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next   # tuple assignment: RHS pehle evaluate
    return prev


def reverseList_rec(head):
    # --- Recursive version ---
    if not head or not head.next:
        return head
    new_head = reverseList_rec(head.next)
    head.next.next = head       # agla node mujhe point kare
    head.next = None            # main tail
    return new_head


assert to_py(reverseList(to_ll([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
assert to_py(reverseList(to_ll([1, 2]))) == [2, 1]
assert to_py(reverseList(to_ll([]))) == []
assert to_py(reverseList_rec(to_ll([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
assert to_py(reverseList_rec(to_ll([7]))) == [7]
print("[1,2,3,4,5] ->", to_py(reverseList(to_ll([1, 2, 3, 4, 5]))))
print("LC 206 sab asserts pass")
"""))

cells.append(md("""
### LC 21. Merge Two Sorted Lists — Easy
https://leetcode.com/problems/merge-two-sorted-lists/

**Problem (Roman Urdu):** Do **sorted** linked lists diye hain. Unhein mila kar ek sorted list
banao — **naye nodes na banao**, purane nodes ko dobara link karo.

**Approach:** Dummy node banao. Jab tak dono lists me nodes hain, chhote wale node ko result ke
`tail` par lagao aur us list ka pointer aage barhao. Aakhir me jo list bachi hai woh
`tail.next = a or b` se chipka do (O(1)).

**Time:** O(m + n)
**Space:** O(1) (dummy ke ilawa kuch nahi)
""" ))

cells.append(code(r"""
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:          # <= se stability barqarar
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2              # bachi hui poori list ek dafa me
    return dummy.next


assert to_py(mergeTwoLists(to_ll([1, 2, 4]), to_ll([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
assert to_py(mergeTwoLists(to_ll([]), to_ll([]))) == []
assert to_py(mergeTwoLists(to_ll([]), to_ll([0]))) == [0]
assert to_py(mergeTwoLists(to_ll([5]), to_ll([1, 2, 3]))) == [1, 2, 3, 5]
print("[1,2,4] + [1,3,4] ->", to_py(mergeTwoLists(to_ll([1, 2, 4]), to_ll([1, 3, 4]))))
print("LC 21 asserts pass")
"""))

cells.append(md("""
### LC 141. Linked List Cycle — Easy
https://leetcode.com/problems/linked-list-cycle/

**Problem (Roman Urdu):** Batao ke list me **cycle** hai ya nahi (koi node dobara aata hai).

**Approach 1 (hash set):** Har visited node `set` me daalo — dobara mila to cycle. O(n) space.
**Approach 2 (Floyd, optimal):** slow 1x, fast 2x. Milein to cycle, fast `None` par pohnche to nahi.

**Kyun milte hain?** Cycle ke andar dono ghoom rahe hain aur faasla har step 1 kam hota hai →
kabhi 0 hoga.

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:            # identity check
            return True
    return False


assert hasCycle(ll_cycle([3, 2, 0, -4], 1)) is True
assert hasCycle(ll_cycle([1, 2], 0)) is True
assert hasCycle(ll_cycle([1], -1)) is False
assert hasCycle(ll_cycle([], -1)) is False
assert hasCycle(ll_cycle([1], 0)) is True       # self-loop
print("cycle at 1 ->", hasCycle(ll_cycle([3, 2, 0, -4], 1)))
print("no cycle   ->", hasCycle(ll_cycle([1, 2, 3], -1)))
print("LC 141 asserts pass")
"""))

cells.append(md("""
### LC 142. Linked List Cycle II — Medium
https://leetcode.com/problems/linked-list-cycle-ii/

**Problem (Roman Urdu):** Cycle ka **shuru hone wala node** return karo (cycle na ho to `None`).

**Approach (Floyd 2-phase):**
1. **Phase 1:** slow/fast se meeting point dhoondo.
2. **Phase 2:** ek pointer `head` se, doosra meeting point se — dono **1 step** chalein.
   Jahan milein wohi cycle start hai.

**Proof (yaad karne layaq):** `L` = head→start, `C` = cycle length, `x` = start→meeting.
slow ne `L+x` chala, fast ne `2(L+x)`; farq `L+x` poore chakkaron ka multiple hona chahiye →
`L + x = nC` → `L = nC − x`. Yani meeting se `L` step chalne par bhi exactly start par pohnchte hain.

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                    # Phase 1 done
            p = head
            while p is not slow:            # Phase 2
                p, slow = p.next, slow.next
            return p
    return None


n = detectCycle(ll_cycle([3, 2, 0, -4], 1))
assert n is not None and n.val == 2
n = detectCycle(ll_cycle([1, 2], 0))
assert n is not None and n.val == 1
assert detectCycle(ll_cycle([1], -1)) is None
assert detectCycle(ll_cycle([1, 2, 3, 4, 5], 4)).val == 5
print("[3,2,0,-4] pos=1 -> cycle start value:", detectCycle(ll_cycle([3, 2, 0, -4], 1)).val)
print("LC 142 asserts pass")
"""))

cells.append(md("""
### LC 876. Middle of the Linked List — Easy
https://leetcode.com/problems/middle-of-the-linked-list/

**Problem (Roman Urdu):** Beech wala node return karo. Agar do middle hon (even length) to
**doosra** wala.

**Approach:** slow 1x, fast 2x. `while fast and fast.next` → fast end par, slow middle par.
(Agar **pehla** middle chahiye ho to `fast = head.next` se shuru karo — split karte waqt yeh version chahiye hota hai.)

**Time:** O(n), ek pass | **Space:** O(1)
**Brute force:** pehle length gino (O(n)), phir `n//2` step chalo — 2 pass, wohi complexity.
""" ))

cells.append(code(r"""
def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow


assert to_py(middleNode(to_ll([1, 2, 3, 4, 5]))) == [3, 4, 5]
assert to_py(middleNode(to_ll([1, 2, 3, 4, 5, 6]))) == [4, 5, 6]
assert to_py(middleNode(to_ll([1]))) == [1]
print("[1..5] middle se aage:", to_py(middleNode(to_ll([1, 2, 3, 4, 5]))))
print("[1..6] middle se aage:", to_py(middleNode(to_ll([1, 2, 3, 4, 5, 6]))))
print("LC 876 asserts pass")
"""))

cells.append(md("""
### LC 19. Remove Nth Node From End of List — Medium
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

**Problem (Roman Urdu):** End se `n`-va node hata do (1-indexed) aur head return karo.

**Approach (ek pass, gap technique):**
1. `dummy` lagao (kyunki head khud delete ho sakta hai — `[1], n=1`)
2. `fast` ko `n` step aage bhejo
3. Dono ko saath chalao jab tak `fast` aakhri node par ho → tab `slow` **delete hone wale se pehle** hoga
4. `slow.next = slow.next.next`

**Time:** O(n) — ek pass | **Space:** O(1)
""" ))

cells.append(code(r"""
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)          # dummy = head delete ka case handle
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next               # gap = n
    while fast.next:                   # fast aakhri node par rukega
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next         # victim skip
    return dummy.next


assert to_py(removeNthFromEnd(to_ll([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
assert to_py(removeNthFromEnd(to_ll([1]), 1)) == []
assert to_py(removeNthFromEnd(to_ll([1, 2]), 1)) == [1]
assert to_py(removeNthFromEnd(to_ll([1, 2]), 2)) == [2]     # head delete
print("[1..5] n=2 ->", to_py(removeNthFromEnd(to_ll([1, 2, 3, 4, 5]), 2)))
print("[1,2]  n=2 ->", to_py(removeNthFromEnd(to_ll([1, 2]), 2)), "(head hata)")
print("LC 19 asserts pass")
"""))

cells.append(md("""
### LC 234. Palindrome Linked List — Easy
https://leetcode.com/problems/palindrome-linked-list/

**Problem (Roman Urdu):** Batao ke list palindrome hai ya nahi.

**Approach 1 (aasan):** values array me daal kar `arr == arr[::-1]` → O(n) time, **O(n) space**
**Approach 2 (optimal, follow-up ka jawab):** middle nikalo → doosra half reverse karo →
compare karo → (achhi practice) list restore kar do.

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def isPalindrome_array(head):
    a = to_py(head)
    return a == a[::-1]


def isPalindrome(head):
    if not head or not head.next:
        return True
    # pehla middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = reverseList(slow.next)       # LC 206 ka function reuse
    slow.next = None
    p, q, ok = head, second, True
    while q:
        if p.val != q.val:
            ok = False
            break
        p, q = p.next, q.next
    slow.next = reverseList(second)       # restore
    return ok


for vals in ([1, 2, 2, 1], [1, 2], [1], [1, 2, 3, 2, 1], [1, 0, 1], [1, 2, 3]):
    assert isPalindrome(to_ll(vals)) == isPalindrome_array(to_ll(vals)), vals
    print(f"{str(vals):14s} -> {isPalindrome(to_ll(vals))}")
print("LC 234 asserts pass")
"""))

cells.append(md("""
### LC 160. Intersection of Two Linked Lists — Easy
https://leetcode.com/problems/intersection-of-two-linked-lists/

**Problem (Roman Urdu):** Do lists kisi node par mil kar shared ho jati hain. Woh **node**
return karo (value nahi — exact node reference). Mile nahi to `None`.

**Approach (pointer switch — sabse elegant):**
`a` A se chale, `b` B se. `a` khatam ho to `a = headB`; `b` khatam ho to `b = headA`.
Dono barabar `m + n` steps chalte hain → agar intersection hai to wahin milenge, warna dono
`None` par ek saath pohnchenge (loop khatam).

**Time:** O(m + n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def getIntersectionNode(headA, headB):
    if not headA or not headB:
        return None
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a


# test 1: intersection at value 8
shared = to_ll([8, 4, 5])
A = to_ll([4, 1]); A.next.next = shared
B = to_ll([5, 6, 1]); B.next.next.next = shared
got = getIntersectionNode(A, B)
assert got is shared and got.val == 8

# test 2: koi intersection nahi
assert getIntersectionNode(to_ll([2, 6, 4]), to_ll([1, 5])) is None

# test 3: pehla node hi intersection
s2 = to_ll([2, 4])
assert getIntersectionNode(s2, s2) is s2

print("intersection node value:", got.val)
print("LC 160 asserts pass")
"""))

cells.append(md("""
### LC 143. Reorder List — Medium
https://leetcode.com/problems/reorder-list/

**Problem (Roman Urdu):** `L0 → L1 → … → Ln` ko is tarteeb me lao:
`L0 → Ln → L1 → Ln-1 → L2 → …` (pehla, aakhri, doosra, doosra-aakhri...). In-place karna hai.

**Approach = teen chhote problems ka jorr (yeh pattern yaad rakho):**
1. **Middle** dhoondo (slow/fast)
2. Doosra half **reverse** karo
3. Dono halves ko **alternate** merge karo

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def reorderList(head):
    if not head or not head.next:
        return head
    # 1) pehla middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    # 2) second half reverse + link kaato
    second = reverseList(slow.next)
    slow.next = None
    # 3) alternate merge
    first = head
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1        # n1 None bhi ho sakta hai -> theek hai
        first, second = n1, n2
    return head


assert to_py(reorderList(to_ll([1, 2, 3, 4]))) == [1, 4, 2, 3]
assert to_py(reorderList(to_ll([1, 2, 3, 4, 5]))) == [1, 5, 2, 4, 3]
assert to_py(reorderList(to_ll([1]))) == [1]
assert to_py(reorderList(to_ll([1, 2]))) == [1, 2]
print("[1,2,3,4]   ->", to_py(reorderList(to_ll([1, 2, 3, 4]))))
print("[1,2,3,4,5] ->", to_py(reorderList(to_ll([1, 2, 3, 4, 5]))))
print("LC 143 asserts pass")
"""))

cells.append(md("""
### LC 2. Add Two Numbers — Medium
https://leetcode.com/problems/add-two-numbers/

**Problem (Roman Urdu):** Do non-negative numbers linked lists me diye hain, digits **reverse
order** me (`342` → `2→4→3`). Unka sum bhi isi format me return karo.

**Approach:** School wali addition. `dummy` + `carry`. Loop condition
`while l1 or l2 or carry` — **carry ko condition me rakhna zaroori hai** warna `[9,9]+[1]`
galat aayega.

`divmod(total, 10)` se ek hi line me `(carry, digit)` mil jate hain.

**Time:** O(max(m, n)) | **Space:** O(max(m, n)) — output list
""" ))

cells.append(code(r"""
def addTwoNumbers(l1, l2):
    dummy = ListNode()
    tail = dummy
    carry = 0
    while l1 or l2 or carry:
        total = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next


assert to_py(addTwoNumbers(to_ll([2, 4, 3]), to_ll([5, 6, 4]))) == [7, 0, 8]
assert to_py(addTwoNumbers(to_ll([0]), to_ll([0]))) == [0]
assert to_py(addTwoNumbers(to_ll([9, 9, 9, 9, 9, 9, 9]), to_ll([9, 9, 9, 9]))) == [8, 9, 9, 9, 0, 0, 0, 1]
assert to_py(addTwoNumbers(to_ll([9, 9]), to_ll([1]))) == [0, 0, 1]
print("342+465 ->", to_py(addTwoNumbers(to_ll([2, 4, 3]), to_ll([5, 6, 4]))))
print("LC 2 asserts pass")
"""))

cells.append(md("""
### LC 83. Remove Duplicates from Sorted List — Easy
https://leetcode.com/problems/remove-duplicates-from-sorted-list/

**Problem (Roman Urdu):** **Sorted** list se duplicates hatao — har value ki **sirf ek** copy rahe.

**Approach:** Ek pointer `cur`. Agar `cur.val == cur.next.val` to `cur.next` skip kar do
(`cur` **wahin rehta hai**, kyunki aur bhi duplicates ho sakte hain). Warna `cur` aage.

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def deleteDuplicates(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next     # skip; cur ko aage NA barhao
        else:
            cur = cur.next
    return head


assert to_py(deleteDuplicates(to_ll([1, 1, 2]))) == [1, 2]
assert to_py(deleteDuplicates(to_ll([1, 1, 2, 3, 3]))) == [1, 2, 3]
assert to_py(deleteDuplicates(to_ll([1, 1, 1]))) == [1]
assert to_py(deleteDuplicates(to_ll([]))) == []
print("[1,1,2,3,3] ->", to_py(deleteDuplicates(to_ll([1, 1, 2, 3, 3]))))
print("LC 83 asserts pass")
"""))

cells.append(md("""
### LC 82. Remove Duplicates from Sorted List II — Medium
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/

**Problem (Roman Urdu):** Sorted list se **jis value ka duplicate hai woh poori value hi** hata do
— sirf woh values bachein jo exactly **ek** dafa aayi hain. `[1,2,3,3,4,4,5]` → `[1,2,5]`.

**Approach (dummy lazmi hai):**
- `prev = dummy` (aakhri confirmed-unique node)
- Har `cur` par dekho: agar `cur.next` ki value same hai → poora group aage skip karo aur
  `prev.next = cur` (group ke baad wala) set karo. Warna `prev = cur`.
- Head bhi duplicate ho sakta hai (`[1,1,2]` → `[2]`), is liye **dummy zaroori**.

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def deleteDuplicatesII(head):
    dummy = ListNode(0, head)
    prev = dummy
    cur = head
    while cur:
        if cur.next and cur.next.val == cur.val:
            val = cur.val
            while cur and cur.val == val:   # poora duplicate group skip
                cur = cur.next
            prev.next = cur                 # prev ko group ke baad joro
        else:
            prev = cur                      # unique -> keep
            cur = cur.next
    return dummy.next


assert to_py(deleteDuplicatesII(to_ll([1, 2, 3, 3, 4, 4, 5]))) == [1, 2, 5]
assert to_py(deleteDuplicatesII(to_ll([1, 1, 1, 2, 3]))) == [2, 3]
assert to_py(deleteDuplicatesII(to_ll([1, 1]))) == []
assert to_py(deleteDuplicatesII(to_ll([1, 2]))) == [1, 2]
print("[1,2,3,3,4,4,5] ->", to_py(deleteDuplicatesII(to_ll([1, 2, 3, 3, 4, 4, 5]))))
print("[1,1,1,2,3]     ->", to_py(deleteDuplicatesII(to_ll([1, 1, 1, 2, 3]))))
print("LC 82 asserts pass")
"""))

cells.append(md("""
### LC 92. Reverse Linked List II — Medium
https://leetcode.com/problems/reverse-linked-list-ii/

**Problem (Roman Urdu):** Position `left` se `right` tak (1-indexed) ka hissa reverse karo,
baqi list waise hi rahe. **Ek pass** me karo.

**Approach (head-insertion trick):**
1. `dummy` lagao, `prev` ko `left-1` position par le jao
2. `cur = prev.next` (yeh reverse ke baad **tail** banega)
3. `right-left` dafa: `cur.next` wale node ko utha kar `prev` ke **foran baad** daal do

```
prev -> [1] -> 2 -> 3 -> 4     (cur = 1)
prev -> 2 -> [1] -> 3 -> 4     (2 uthaya)
prev -> 3 -> 2 -> [1] -> 4     (3 uthaya)
```

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def reverseBetween(head, left, right):
    if not head or left == right:
        return head
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next          # reverse hone wale hisse se pehle wala node
    cur = prev.next               # yeh baad me tail banega
    for _ in range(right - left):
        nxt = cur.next            # utha do
        cur.next = nxt.next       # chain jor do
        nxt.next = prev.next      # prev ke baad wale se joro
        prev.next = nxt           # prev ke foran baad set karo
    return dummy.next


assert to_py(reverseBetween(to_ll([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5]
assert to_py(reverseBetween(to_ll([5]), 1, 1)) == [5]
assert to_py(reverseBetween(to_ll([1, 2, 3, 4, 5]), 1, 5)) == [5, 4, 3, 2, 1]
assert to_py(reverseBetween(to_ll([3, 5]), 1, 2)) == [5, 3]
print("[1..5] left=2 right=4 ->", to_py(reverseBetween(to_ll([1, 2, 3, 4, 5]), 2, 4)))
print("LC 92 asserts pass")
"""))

cells.append(md("""
### LC 148. Sort List — Medium
https://leetcode.com/problems/sort-list/

**Problem (Roman Urdu):** Linked list ko **O(n log n)** time aur (follow-up) **O(1)** space me
sort karo.

**Approach — Merge Sort (LL ke liye best):**
1. **Split:** slow/fast se pehla middle dhoondo, wahan link kaat do
2. **Sort:** dono halves recursively
3. **Merge:** LC 21 ka merge

**Quick sort kyun nahi?** LL me random access nahi → pivot ke around partition mehnga, aur
worst case O(n²).

**Time:** O(n log n)
**Space:** O(log n) recursion stack (top-down). Bottom-up karo to **O(1)** — asli follow-up jawab.
""" ))

cells.append(code(r"""
def sortList(head):
    # ---- Top-down merge sort: O(n log n) time, O(log n) stack ----
    if not head or not head.next:
        return head
    slow, fast = head, head.next            # pehla middle (dono halves non-empty rahenge)
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid = slow.next
    slow.next = None                        # link kaato
    return mergeTwoLists(sortList(head), sortList(mid))


def sortList_bottom_up(head):
    # ---- Bottom-up: O(1) extra space (recursion nahi) -- follow-up ka asli jawab ----
    if not head or not head.next:
        return head

    def split(node, n):
        # n nodes ke baad list tor do, baqi ka head return karo
        for _ in range(n - 1):
            if not node:
                break
            node = node.next
        if not node:
            return None
        rest = node.next
        node.next = None
        return rest

    length = 0
    cur = head
    while cur:
        length, cur = length + 1, cur.next

    dummy = ListNode(0, head)
    size = 1
    while size < length:                    # 1, 2, 4, 8 ... size ke blocks merge karte jao
        cur, tail = dummy.next, dummy
        while cur:
            left = cur
            right = split(left, size)
            cur = split(right, size)        # agli round ka shuru
            tail.next = mergeTwoLists(left, right)
            while tail.next:                # tail ko merged hisse ke end par le jao
                tail = tail.next
        size *= 2
    return dummy.next


for vals in ([4, 2, 1, 3], [-1, 5, 3, 4, 0], [], [1], [2, 1], [5, 4, 3, 2, 1]):
    a = to_py(sortList(to_ll(vals)))
    b = to_py(sortList_bottom_up(to_ll(vals)))
    assert a == sorted(vals) == b, (vals, a, b)
    print(f"{str(vals):18s} -> {a}")
print("LC 148 asserts pass (top-down aur bottom-up dono)")
"""))

cells.append(md("""
### LC 61. Rotate List — Medium
https://leetcode.com/problems/rotate-list/

**Problem (Roman Urdu):** List ko **right** ki taraf `k` jagah rotate karo.
`[1,2,3,4,5], k=2` → `[4,5,1,2,3]`.

**Approach:**
1. Length `n` gino aur `tail` bhi le lo
2. `k %= n` — **yeh line bhoolna sabse common bug hai** (`k` bohat bara ho sakta hai, e.g. 2·10⁹)
3. `k == 0` → jaisi hai waisi return karo
4. Naya tail = `(n - k - 1)`-va node → `new_head = new_tail.next`, `new_tail.next = None`,
   `old_tail.next = old_head` (circle bana kar tor diya)

**Time:** O(n) | **Space:** O(1)
""" ))

cells.append(code(r"""
def rotateRight(head, k):
    if not head or not head.next or k == 0:
        return head
    # length + tail
    n, tail = 1, head
    while tail.next:
        n, tail = n + 1, tail.next
    k %= n                              # ZAROORI: k bohat bara ho sakta hai
    if k == 0:
        return head
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None                # naya end
    tail.next = head                    # purana tail purane head se juda
    return new_head


assert to_py(rotateRight(to_ll([1, 2, 3, 4, 5]), 2)) == [4, 5, 1, 2, 3]
assert to_py(rotateRight(to_ll([0, 1, 2]), 4)) == [2, 0, 1]      # k > n
assert to_py(rotateRight(to_ll([1, 2]), 2)) == [1, 2]            # k == n -> same
assert to_py(rotateRight(to_ll([]), 3)) == []
assert to_py(rotateRight(to_ll([1]), 99)) == [1]
print("[1..5] k=2 ->", to_py(rotateRight(to_ll([1, 2, 3, 4, 5]), 2)))
print("[0,1,2] k=4 ->", to_py(rotateRight(to_ll([0, 1, 2]), 4)), "(k %= n ki ahmiyat)")
print("LC 61 asserts pass")
"""))

cells.append(md("""
### LC 138. Copy List with Random Pointer — Medium
https://leetcode.com/problems/copy-list-with-random-pointer/

**Problem (Roman Urdu):** Har node ke paas `next` aur `random` (kisi bhi node ya `None`) hai.
Poori list ka **deep copy** banao — naye nodes, aur `random` bhi naye nodes ko point karein.

**Approach 1 — HashMap (`old → new`), 2 pass:** O(n) time, O(n) space. Likhna aasan.
**Approach 2 — Interleave, 3 pass, O(1) extra space:**
`A→A'→B→B'→C→C'` bana lo, phir `A'.random = A.random.next` (kyunki kisi node ki copy
uske foran baad hai), phir unweave.

**Time:** O(n) dono | **Space:** O(n) vs **O(1)**
""" ))

cells.append(code(r"""
class RandNode:
    __slots__ = ("val", "next", "random")

    def __init__(self, x, next=None, random=None):
        self.val = x
        self.next = next
        self.random = random


def copyRandomList(head):
    # ---- Approach 1: hashmap ----
    if not head:
        return None
    old_to_new = {}
    cur = head
    while cur:
        old_to_new[cur] = RandNode(cur.val)
        cur = cur.next
    cur = head
    while cur:
        old_to_new[cur].next = old_to_new.get(cur.next)
        old_to_new[cur].random = old_to_new.get(cur.random)
        cur = cur.next
    return old_to_new[head]


def copyRandomList_O1(head):
    # ---- Approach 2: interleave (O(1) extra space) ----
    if not head:
        return None
    cur = head
    while cur:                                   # A -> A' -> B -> B'
        cur.next = RandNode(cur.val, cur.next)
        cur = cur.next.next
    cur = head
    while cur:                                   # random pointers
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    new_head = head.next
    cur = head
    while cur:                                   # unweave
        copy = cur.next
        cur.next = copy.next
        copy.next = cur.next.next if cur.next else None
        cur = cur.next
    return new_head


def make_rand(vals, rnd):
    nodes = [RandNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    for i, r in enumerate(rnd):
        nodes[i].random = nodes[r] if r is not None else None
    return nodes[0] if nodes else None


def show_rand(head):
    out = []
    while head:
        out.append([head.val, head.random.val if head.random else None])
        head = head.next
    return out


vals, rnd = [7, 13, 11, 10, 1], [None, 0, 4, 2, 0]
expected = show_rand(make_rand(vals, rnd))
for fn in (copyRandomList, copyRandomList_O1):
    orig = make_rand(vals, rnd)
    cp = fn(orig)
    assert show_rand(cp) == expected
    # deep copy verify: copy ka koi bhi node RandNode ka NAYA object hona chahiye
    assert cp is not orig
    print(f"{fn.__name__:22s} ->", show_rand(cp))
assert copyRandomList(None) is None and copyRandomList_O1(None) is None
print("expected              ->", expected)
print("LC 138 asserts pass")
"""))

cells.append(md("""
### LC 24. Swap Nodes in Pairs — Medium
https://leetcode.com/problems/swap-nodes-in-pairs/

**Problem (Roman Urdu):** Har **jori** (pair) ko aapas me swap karo — **values badalna allowed
nahi**, sirf nodes ke links badlo. `[1,2,3,4]` → `[2,1,4,3]`. Odd length me aakhri node waise hi.

**Approach (dummy + 3 pointers):**
```
prev -> a -> b -> rest
banao: prev -> b -> a -> rest
```
Yani: `a.next = b.next`, `b.next = a`, `prev.next = b`, phir `prev = a`.

**Time:** O(n) | **Space:** O(1) (recursive version O(n) stack)
""" ))

cells.append(code(r"""
def swapPairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:      # kam az kam 2 node bache hon
        a = prev.next
        b = a.next
        a.next = b.next                      # a ko b ke baad wale se joro
        b.next = a                            # b pehle, a baad me
        prev.next = b                         # prev ko naye pehle (b) se joro
        prev = a                              # a ab is pair ka aakhir hai
    return dummy.next


def swapPairs_rec(head):
    if not head or not head.next:
        return head
    second = head.next
    head.next = swapPairs_rec(second.next)   # baqi list swap karao
    second.next = head
    return second


for vals in ([1, 2, 3, 4], [], [1], [1, 2, 3], [1, 2, 3, 4, 5, 6]):
    a = to_py(swapPairs(to_ll(vals)))
    b = to_py(swapPairs_rec(to_ll(vals)))
    assert a == b
    print(f"{str(vals):20s} -> {a}")
assert to_py(swapPairs(to_ll([1, 2, 3, 4]))) == [2, 1, 4, 3]
assert to_py(swapPairs(to_ll([1, 2, 3]))) == [2, 1, 3]
print("LC 24 asserts pass")
"""))

cells.append(md("""
### LC 23. Merge k Sorted Lists — Hard
https://leetcode.com/problems/merge-k-sorted-lists/

**Problem (Roman Urdu):** `k` sorted linked lists ka array diya hai. Sab ko mila kar ek sorted
list banao.

**Approach 1 — Min-heap:** har list ka current head heap me. Sabse chhota nikaalo, result me
lagao, us list ka agla node push karo.
- **Time:** O(N log k) | **Space:** O(k)
- **Gotcha:** heap me `(val, i, node)` push karo. Sirf `(val, node)` par barabar values aane par
  `TypeError: '<' not supported between instances of 'ListNode'` aayega.

**Approach 2 — Divide & Conquer (pairwise merge):** lists ko jori-jori merge karte jao
(k → k/2 → k/4 …).
- **Time:** O(N log k) | **Space:** O(1) — **heap se behtar space**

**Naive:** ek ek kar ke merge → O(N·k). Interview me pehle yeh batao, phir optimize karo.
""" ))

cells.append(code(r"""
import heapq


def mergeKLists_heap(lists):
    h = []
    for i, node in enumerate(lists):
        if node:
            h.append((node.val, i, node))       # 'i' = tie-breaker
    heapq.heapify(h)                            # O(k)
    dummy = ListNode()
    tail = dummy
    while h:
        _, i, node = heapq.heappop(h)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    tail.next = None                            # purani links tor do
    return dummy.next


def mergeKLists_dc(lists):
    # ---- Divide & conquer: pairwise merge, O(1) space ----
    if not lists:
        return None
    step = 1
    n = len(lists)
    lists = list(lists)
    while step < n:
        for i in range(0, n - step, step * 2):
            lists[i] = mergeTwoLists(lists[i], lists[i + step])
        step *= 2
    return lists[0]


data = [[1, 4, 5], [1, 3, 4], [2, 6]]
r1 = to_py(mergeKLists_heap([to_ll(x) for x in data]))
r2 = to_py(mergeKLists_dc([to_ll(x) for x in data]))
assert r1 == r2 == [1, 1, 2, 3, 4, 4, 5, 6]
print("heap ->", r1)
print("D&C  ->", r2)
assert mergeKLists_heap([]) is None and mergeKLists_dc([]) is None
assert to_py(mergeKLists_heap([to_ll([])])) == []
assert to_py(mergeKLists_dc([to_ll([]), to_ll([1])])) == [1]

# gotcha ko live dekho: bina tie-breaker crash hota hai
try:
    bad = [(1, ListNode(1)), (1, ListNode(2))]
    heapq.heapify(bad)
    heapq.heappush(bad, (1, ListNode(3)))
    heapq.heappop(bad); heapq.heappop(bad)
except TypeError as e:
    print("\nGotcha (bina index):", type(e).__name__, "-", e)
print("LC 23 asserts pass")
"""))

cells.append(md("""
### LC 707. Design Linked List — Medium
https://leetcode.com/problems/design-linked-list/

**Problem (Roman Urdu):** Poori linked list class design karo in operations ke saath:
`get(index)`, `addAtHead(val)`, `addAtTail(val)`, `addAtIndex(index, val)`, `deleteAtIndex(index)`.
Invalid index par `get` → `-1`, `addAtIndex` (index > length) → kuch na karo.

**Approach:** **Sentinel head** + `size` counter rakho:
- Sentinel se `addAtHead` aur `deleteAtIndex(0)` ke special cases khatam
- `size` se bounds check O(1)
- `addAtTail` ke liye `tail` pointer rakh lo (O(1)) — warna O(n)

**Time:** `get`/`addAtIndex`/`deleteAtIndex` → O(index); `addAtHead`/`addAtTail` → O(1)
**Space:** O(n)
""" ))

cells.append(code(r"""
class MyLinkedList:
    def __init__(self):
        self.sent = ListNode(0)      # sentinel: asli head sent.next hai
        self.tail = self.sent        # tail pointer -> addAtTail O(1)
        self.size = 0

    def _node_before(self, index):
        # index-va node se PEHLE wala node (sentinel se ginte hue)
        cur = self.sent
        for _ in range(index):
            cur = cur.next
        return cur

    def get(self, index):
        if index < 0 or index >= self.size:
            return -1                        # invalid -> -1
        return self._node_before(index).next.val

    def addAtHead(self, val):
        self.addAtIndex(0, val)

    def addAtTail(self, val):
        node = ListNode(val)
        self.tail.next = node
        self.tail = node
        self.size += 1

    def addAtIndex(self, index, val):
        if index > self.size or index < 0:
            return                            # ignore (problem ki requirement)
        if index == self.size:
            return self.addAtTail(val)
        prev = self._node_before(index)
        prev.next = ListNode(val, prev.next)
        self.size += 1

    def deleteAtIndex(self, index):
        if index < 0 or index >= self.size:
            return
        prev = self._node_before(index)
        victim = prev.next
        prev.next = victim.next
        if victim is self.tail:               # tail delete hua -> tail peeche
            self.tail = prev
        self.size -= 1

    def to_list(self):
        return to_py(self.sent.next)


ml = MyLinkedList()
ml.addAtHead(1)
ml.addAtTail(3)
ml.addAtIndex(1, 2)          # 1 -> 2 -> 3
print("list      :", ml.to_list())
print("get(1)    :", ml.get(1))
ml.deleteAtIndex(1)          # 1 -> 3
print("after del :", ml.to_list())
print("get(1)    :", ml.get(1))
print("get(9)    :", ml.get(9), "(invalid)")
ml.addAtIndex(9, 100)        # ignore hona chahiye
print("ignore ke baad:", ml.to_list())
ml.addAtTail(7); ml.addAtHead(0)
print("final     :", ml.to_list())

assert ml.to_list() == [0, 1, 3, 7]
assert ml.get(0) == 0 and ml.get(3) == 7 and ml.get(4) == -1
ml.deleteAtIndex(3)          # tail delete -> tail pointer update hona chahiye
ml.addAtTail(9)              # agar tail galat hota to yeh galat jagah lagta
assert ml.to_list() == [0, 1, 3, 9], ml.to_list()
print("LC 707 asserts pass (tail pointer bhi sahi update hua)")
"""))

# ============================================================
# 15. INTERVIEW Q&A
# ============================================================
cells.append(md("""
## 20. Interview Questions & Answers

**Q1. Linked list array se behtar kab hai?**
Jab beech me insert/delete zyada ho aur node ka reference pehle se hath me ho (LRU cache), ya size
bohat badalta ho. Random access chahiye ho to array.

**Q2. Array actually kab bhi tez hota hai chahe complexity kharab ho?**
**Cache locality** ki wajah se. Array contiguous hai → CPU prefetch karta hai. LL me pointer
chasing = cache miss. Chhoti n par array aksar jeet jata hai.

**Q3. Python ka `list` linked list hai?**
Nahi — **dynamic array** (over-allocation + amortized O(1) append). `collections.deque`
andar se doubly-linked list of fixed-size blocks hai — is liye dono taraf se O(1) push/pop.

**Q4. Singly vs Doubly — trade-off?**
DLL: backward traversal + node ka reference hote hue **O(1) delete**. Cost: per-node extra
pointer + har op me 2 pointer update (zyada bugs).

**Q5. Cycle detect karne ke tareeqe?**
(a) hash set of visited nodes — O(n) time, O(n) space.
(b) **Floyd's tortoise-hare** — O(n) time, **O(1) space**. (c) Nodes ko mark karna (list mutate
karni pare, aksar allowed nahi).

**Q6. Floyd me cycle start kaise milta hai?**
`L + x = nC` (proof section 8.1 me). Meeting ke baad ek pointer head se, doosra meeting se —
1-1 step chalein, jahan milein wohi start.

**Q7. Fast pointer 3 step chale to?**
Cycle detect **phir bhi** hoga (modular arithmetic se guarantee), lekin `L = nC − x` wala saaf
relation toot jata hai → cycle start ka simple 2-phase trick kaam nahi karega. 2x standard hai.

**Q8. Dummy node kyun?**
Head ke special cases (head delete, head par insert, khali result list) khatam. Code me
`if prev is None` wale branch nahi likhne parte → bugs kam.

**Q9. Linked list ke liye best sorting algorithm?**
**Merge sort.** Split O(1) pointer work se hota hai, merge sequential access se; O(n log n)
guaranteed aur array ke O(n) buffer ki zaroorat nahi. Quick sort par random access na hone
se pivot partition mehnga.

**Q10. LL me binary search kar sakte ho?**
Practically nahi (middle nikalne me O(n) lagta hai → O(n log n), linear scan se bura).
**Skip list** isi masle ka hal hai — multi-level LL jo O(log n) search deti hai.

**Q11. Middle nikalne ka one-pass tareeqa?**
slow/fast. `while fast and fast.next` → even length me **doosra** middle; agar
`fast = head.next` se shuru karo to **pehla** middle (split ke liye zaroori).

**Q12. Reverse iterative vs recursive — kaun behtar?**
Iterative — O(1) space. Recursive O(n) stack, aur Python me default recursion limit ~1000 hai,
n = 10⁵ par `RecursionError`.

**Q13. Aik hi node ka reference diya hai (head nahi) — usay delete karo?**
Agar woh tail nahi: `node.val = node.next.val; node.next = node.next.next` (agle node ki value
copy kar ke usay hata do). Tail ho to yeh trick kaam nahi karti.

**Q14. `k` sorted lists merge — heap vs D&C?**
Dono O(N log k). Heap O(k) space leta hai aur streaming input ke liye behtar. D&C O(1) extra
space leta hai (in-place merges) aur cache-friendly hai.

**Q15. LRU cache me DLL kyun, SLL nahi?**
`get` par node ko front par lana hai → usay apni jagah se **O(1)** me nikaalna parega. SLL me
`prev` nahi maloom → O(n).

**Q16. Skip list kya hai?**
Probabilistic multi-level linked list — average O(log n) search/insert/delete. Redis (sorted sets)
me use hoti hai, balanced tree ka simple alternative.

**Q17. `is` vs `==` LL me?**
Cycle/intersection **identity** ka masla hai → `is`. Values compare karni hon → `==`.
Agar kisi ne `__eq__` override kar diya to `==` dhoka de sakta hai.

**Q18. Memory leak LL me kaise?**
Deleted nodes ke `prev/next` clear na karo to reference cycles ban jate hain. Python ka GC
cycles handle karta hai, lekin C++ me yeh asli leak hai. Achhi practice: `node.prev = node.next = None`.

**Q19. LL ko O(1) me reverse kar sakte hain?**
Nahi (har node ka pointer badalna parega → O(n)). Trick: ek flag rakh lo aur "logical direction"
DLL me flip kar do — traversal ka direction badal jata hai bina links chhoone.

**Q20. Real product me linked list kahan dekhi?**
`OrderedDict`/LRU cache, Redis lists (quicklist), OS ka free-list allocator, Linux kernel ki
`list_head`, undo stack, adjacency list of graph, hash table chaining.
""" ))

# ============================================================
# 16. PRACTICE
# ============================================================
cells.append(md("""
## 21. Practice Exercises (khud karo)

1. **`SinglyLinkedList.reverse()` method likho** (in-place, iterative). *Hint:* `head` aur `tail`
   dono swap karna na bhoolna.
2. **`odd_even_list(head)`** — odd positions ke nodes pehle, even baad me (LC 328).
   *Hint:* do pointers `odd`, `even` + `even_head` save karo.
3. **`split_in_half(head)`** — do lists return karo (odd length me pehli lambi ho).
   *Hint:* pehla middle + `slow.next = None`.
4. **`is_circular(head)`** — batao ke list circular hai (tail → head) ya sirf koi cycle hai.
   *Hint:* Floyd se start dhoondo aur dekho `start is head`?
5. **`flatten_multilevel(head)`** — har node ka ek `child` list bhi hai; poori list ko flat karo
   (LC 430). *Hint:* stack ya recursion.
6. **`add_two_numbers_forward(l1, l2)`** — digits **forward** order me hain (LC 445).
   *Hint:* reverse karo, ya stack use karo.
7. **`remove_zero_sum_sublists(head)`** — jo consecutive sublists ka sum 0 ho, hata do (LC 1171).
   *Hint:* prefix sum + hashmap of `prefix -> node`.
8. **`sort_dll(head)`** — DLL ko merge sort se sort karo, `prev` pointers bhi sahi rakho.
9. **`josephus_kill_order(n, k)`** — sirf survivor nahi, **poori elimination order** return karo.
10. **`LFUCache`** — LRU se aage: least *frequently* used. *Hint:* frequency → DLL ka dict.

*(Har ek ko chhote inputs par test karo: `[]`, `[1]`, `[1,2]`.)*
""" ))

cells.append(code(r"""
# ---- Exercise 1 aur 2 ka model solution (baqi khud karo) ----

def sll_reverse(self):
    # SinglyLinkedList par in-place reverse (head/tail swap ke saath)
    prev, cur = None, self.head
    self.tail = self.head              # purana head naya tail banega
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    self.head = prev
    return self

SinglyLinkedList.reverse = sll_reverse   # monkey-patch (teaching ke liye)

ll2 = SinglyLinkedList.from_list([1, 2, 3, 4])
print("pehle  :", ll2)
ll2.reverse()
print("baad me:", ll2)
ll2.append(99)                            # tail sahi hai to yeh aakhir me lagega
print("append :", ll2)
assert ll2.to_list() == [4, 3, 2, 1, 99]


def odd_even_list(head):
    # LC 328: odd positions pehle, even baad me (1-indexed positions)
    if not head or not head.next:
        return head
    odd, even = head, head.next
    even_head = even                      # even chain ka head bachao
    while even and even.next:
        odd.next = even.next              # odd chain agla odd
        odd = odd.next
        even.next = odd.next              # even chain agla even
        even = even.next
    odd.next = even_head                  # odd ke end par even chain joro
    return head


print("\nodd_even [1,2,3,4,5] ->", to_py(odd_even_list(to_ll([1, 2, 3, 4, 5]))))
print("odd_even [2,1,3,5,6,4,7] ->", to_py(odd_even_list(to_ll([2, 1, 3, 5, 6, 4, 7]))))
assert to_py(odd_even_list(to_ll([1, 2, 3, 4, 5]))) == [1, 3, 5, 2, 4]
print("model solutions pass")
"""))

# ============================================================
# 17. CHEAT SHEET
# ============================================================
cells.append(md("""
## 22. Summary / Cheat-sheet

### Muhavray (idioms) — yeh 5 yaad kar lo, 80% problems ho jayengi

```python
# 1) Traverse
cur = head
while cur:
    ...
    cur = cur.next

# 2) Reverse (3-pointer)
prev, cur = None, head
while cur:
    nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
return prev

# 3) Dummy + tail (naya list banate waqt)
dummy = ListNode(); tail = dummy
...
tail.next = node; tail = tail.next
return dummy.next

# 4) Slow / Fast (middle, cycle)
slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next

# 5) Gap n (nth from end)
fast = head
for _ in range(n): fast = fast.next
while fast: slow, fast = slow.next, fast.next
```

### Complexity table

| Operation | SLL | DLL | Array |
|---|---|---|---|
| access by index | O(n) | O(n) | **O(1)** |
| insert/delete head | **O(1)** | **O(1)** | O(n) |
| insert/delete tail | O(1)* | **O(1)** | O(1) amortized |
| delete given node | O(n) | **O(1)** | O(n) |
| search | O(n) | O(n) | O(n) |
| reverse | O(n) | O(n) | O(n) |
| sort | O(n log n) merge sort | same | O(n log n) |

\\* `tail` pointer ho to O(1)

### Pattern → Technique map

| Problem me yeh dikhe | Technique |
|---|---|
| "middle", "half" | slow/fast |
| "cycle", "loop" | Floyd |
| "nth from end", "remove nth" | gap pointer |
| "reverse ... part / groups" | dummy + head-insertion |
| "merge sorted" | dummy + two pointers |
| "k lists / k largest" | min-heap |
| "sort a linked list" | merge sort |
| "palindrome" | middle + reverse half |
| "reorder / zigzag" | middle + reverse + merge |
| "head delete ho sakta hai" | **dummy node** |
| "O(1) get + O(1) evict" | DLL + hashmap (LRU) |
| "intersection of two lists" | pointer switch |

### Aakhri naseehat

1. Solution likhne se pehle **kaghaz par teer bana lo** — 3 nodes ka diagram kaafi hai.
2. Har code ko `[]`, `[1]`, `[1,2]`, aur "head hi target" par test karo.
3. `tail.next = None` bhoolna = infinite loop. Sab se mehnga bug.
4. Recursion Python me n=10⁵ par toot jayegi — iterative default rakho.
5. Interview me bolte raho: "yahan dummy lagata hoon takay head ka special case na aaye."
""" ))

save(r"DSA in Python/Intermediate/01_LinkedList_Complete.ipynb", cells)
save(r"DSA in Python/Intermediate/01_LinkedList_Complete.ipynb", cells)
