import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ============================================================
# 1. TITLE + ROADMAP
# ============================================================
cells.append(md("""
# 01 — Graphs: Traversals, Shortest Paths aur MST

**Level:** Advanced
**Series:** DSA in Python → Advance

Graphs woh topic hai jahan 80% students interview me atak jaate hain — kyunki graph problems
"pehchanna" mushkil hota hai. Asli baat ye hai: **graph algorithms ki tadaad kam hai (~12),
bas unhein achhi tarah se rata nahi, samajhna hai.** Ek dafa BFS/DFS ka template haath me aa gaya,
to 60% graph problems usi ke variations hain.

## Is notebook me kya seekhenge (roadmap)

1. **Terminology** — directed/undirected, weighted, degree, path, cycle, connected vs strongly connected, DAG, tree vs graph
2. **Representations** — adjacency matrix vs adjacency list vs edge list vs implicit grid (memory/time table)
3. **BFS** — queue template, distances, unweighted shortest path, multi-source BFS, 0-1 BFS (deque)
4. **DFS** — recursive + iterative, entry/exit times, path tracking
5. **Connected components** aur **cycle detection** (undirected: parent trick; directed: colors / rec-stack)
6. **Bipartite check** (2-coloring)
7. **Topological sort** — Kahn (BFS) + DFS postorder, cycle detection, lexicographic order
8. **SCC** — Kosaraju aur Tarjan
9. **Bridges aur Articulation Points** (Tarjan low-link) — brief
10. **Dijkstra** (heap) — aur negatives kyun nahi chalte
11. **Bellman-Ford** — negative cycle detection
12. **Floyd-Warshall** — all-pairs
13. **DAG shortest path** via topo order (negative weights bhi OK)
14. **A\\*** ka taaruf (heuristic search)
15. **MST** — Prim (heap) aur Kruskal (union-find)
16. **Grid patterns** — islands, flood fill, rotting oranges, walls & gates
17. **State-space BFS** — word ladder, lock combination
18. **Complexity table** + "kaun sa algorithm kab" decision guide

Phir: **Common Mistakes/Gotchas**, **Real-World Problems**, **LeetCode (19 problems)**,
**Interview Q&A**, **Practice Exercises**, aur **Cheat-sheet**.

## Prerequisites

- Python basics: `list`, `dict`, `set`, tuple unpacking, list comprehension
- `collections.deque`, `heapq` ka basic idea (yahan revise bhi karenge)
- Recursion aur Big-O notation
- Trees ka basic knowledge (graph, tree ka general case hai)

> **Golden rule:** Ye notebook top-se-bottom chalao. Har cell pichle cells ke variables/helpers
> par depend kar sakta hai.
"""))

# ============================================================
# 2. TERMINOLOGY
# ============================================================
cells.append(md("""
## 1. Graph Terminology — Zubaan pehle, code baad me

**Kya hai:** Graph = **G = (V, E)**. `V` = vertices (nodes), `E` = edges (connections).
Bas itni si baat hai — lekin har interview question isi vocabulary me poocha jaata hai,
to zubaan clear honi chahiye.

### Bunyadi istilahat (terms)

| Term | Roman Urdu me matlab |
|---|---|
| **Vertex / Node** | Ek point — city, person, web page, grid cell |
| **Edge** | Do vertices ke darmiyan connection — road, friendship, link |
| **Undirected edge** | Dono taraf chal sakte ho: `u — v` (dosti: agar A, B ka dost hai to B bhi A ka) |
| **Directed edge (arc)** | Sirf ek taraf: `u → v` (Twitter follow, prerequisite course) |
| **Weighted edge** | Edge par cost/distance/time laga hua: `u —(5)— v` |
| **Adjacent / Neighbour** | Do vertices jo edge se jude hain |
| **Degree** (undirected) | Kitni edges vertex ko touch karti hain |
| **In-degree / Out-degree** (directed) | Andar aane wali / bahar jaane wali edges ki tadaad |
| **Path** | Vertices ka aisa sequence jahan consecutive pair edge se jude hon, koi vertex repeat na ho |
| **Walk** | Path jaisa lekin repeat allowed |
| **Cycle** | Path jo wapis apne shuru wale vertex par aa jaye (length ≥ 3 undirected me, ≥ 1 directed me self-loop ke sath) |
| **Simple graph** | Koi self-loop nahi, koi parallel (multi) edge nahi |
| **Connected** (undirected) | Har vertex se har doosre vertex tak koi raasta ho |
| **Connected Component** | Graph ka aisa maximal hissa jo andar se connected ho |
| **Strongly Connected** (directed) | Har `u,v` ke liye `u → v` aur `v → u` dono raaste hon |
| **DAG** | Directed Acyclic Graph — directed, aur koi cycle nahi. Topological sort sirf DAG par |
| **Tree** | Connected undirected graph with **exactly V-1 edges** aur **no cycle** |
| **Forest** | Trees ka collection (disconnected acyclic graph) |
| **Dense vs Sparse** | `E ≈ V²` → dense; `E ≈ V` → sparse. Representation ka faisla isi par |
| **Bipartite** | Vertices ko 2 groups me baant sakein aisay ke har edge groups ke beech ho |

### Tree vs Graph — interview ka favourite

- Tree ek **special graph** hai: connected + acyclic + undirected + `E = V - 1`.
- Tree me **parent** ka concept hota hai, graph me nahi (graph me sirf "visited" set hota hai).
- Tree traversal me `visited` set ki zaroorat nahi (parent ko skip kar do). **Graph me `visited`
  LAZMI hai** warna infinite loop.

**Handshaking Lemma:** undirected graph me `sum(degree) = 2 * E`. (Har edge do degrees deta hai.)

**Interview tip:** Jab bhi problem me "network", "dependency", "connections", "grid",
"transform one word into another", "course prerequisites", "flight routes" jaise lafz aayein —
sochna shuru karo: *ye graph problem hai*.
"""))

cells.append(code('''
# Terminology ko code me dekhte hain — chhota sa social network
from collections import defaultdict

# Undirected graph: dosti ka network (adjacency list ki shakal me)
friends = {
    "Ali":   ["Bilal", "Chand"],
    "Bilal": ["Ali", "Chand"],
    "Chand": ["Ali", "Bilal"],
    "Daud":  ["Erum"],
    "Erum":  ["Daud"],
    "Farhan": [],            # isolated vertex — degree 0
}

V = len(friends)                                  # vertices ki tadaad
E = sum(len(v) for v in friends.values()) // 2    # undirected: har edge 2 dafa gina gaya
print("V =", V, " E =", E)

# Degree har vertex ka
degrees = {u: len(nbrs) for u, nbrs in friends.items()}
print("Degrees:", degrees)

# Handshaking lemma: sum(degree) == 2*E
assert sum(degrees.values()) == 2 * E, "handshaking lemma toot gaya!"
print("Handshaking lemma OK:", sum(degrees.values()), "==", 2 * E)

# Directed graph: course prerequisites (u -> v ka matlab "u ke baad v")
prereq = {
    "Programming": ["DataStructures"],
    "DataStructures": ["Algorithms", "DBMS"],
    "Algorithms": ["ML"],
    "DBMS": [],
    "ML": [],
}
out_deg = {u: len(v) for u, v in prereq.items()}
in_deg = defaultdict(int)
for u in prereq:
    in_deg.setdefault(u, 0)          # sab vertices ko 0 se initialize karo
for u, vs in prereq.items():
    for v in vs:
        in_deg[v] += 1               # har incoming edge count karo

print("Out-degree:", out_deg)
print("In-degree :", dict(in_deg))
# Jis vertex ka in-degree 0 ho, wo "shuruaat" hai (koi prerequisite nahi)
print("Start nodes (in-degree 0):", [u for u, d in in_deg.items() if d == 0])
''' ))

cells.append(code('''
# Tree vs Graph check — practical helper
def is_tree(adj: dict) -> bool:
    """Undirected graph tree hai? => connected AND edges == V-1 AND acyclic.
    Trick: connected + (E == V-1) ho jaye to acyclic apne aap sabit ho jata hai."""
    V = len(adj)
    if V == 0:
        return False
    E = sum(len(x) for x in adj.values()) // 2
    if E != V - 1:                      # pehli shart: exactly V-1 edges
        return False
    # doosri shart: connected? — ek simple DFS se count karo
    start = next(iter(adj))
    seen, stack = {start}, [start]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == V               # sab vertices reach hue?

t = {1: [2, 3], 2: [1], 3: [1, 4], 4: [3]}          # 4 nodes, 3 edges, connected -> tree
g = {1: [2, 3], 2: [1, 3], 3: [1, 2]}               # triangle -> cycle hai, tree nahi
d = {1: [2], 2: [1], 3: [4], 4: [3]}                # 2 components -> forest, tree nahi

assert is_tree(t) is True
assert is_tree(g) is False
assert is_tree(d) is False
print("is_tree(t) =", is_tree(t), "| is_tree(triangle) =", is_tree(g), "| is_tree(forest) =", is_tree(d))
''' ))

# ============================================================
# 3. REPRESENTATIONS
# ============================================================
cells.append(md("""
## 2. Graph Representations — kaun si shakal kab

Ye faisla poori problem ki complexity badal deta hai. Chaar tareeqe hain:

### (a) Adjacency List — **90% interview problems ka default**

```python
adj = {0: [1, 2], 1: [0], 2: [0]}          # dict of lists
adj = [[1, 2], [0], [0]]                    # list of lists (nodes 0..n-1 hon to behtar)
adj = defaultdict(list)                     # missing keys ka jhanjhat khatam
```

### (b) Adjacency Matrix — dense graphs / O(1) edge lookup

```python
mat = [[0]*n for _ in range(n)]
mat[u][v] = 1        # ya weight
```

### (c) Edge List — Kruskal, Bellman-Ford ke liye perfect

```python
edges = [(u, v, w), ...]
```

### (d) Implicit Grid — koi adjacency banane ki zaroorat hi nahi

Grid problems (islands, maze) me "graph" khud grid hai. Neighbours formula se nikaalte hain:
`(r±1, c)` aur `(r, c±1)`. Ye "implicit graph" kehlata hai.

### Comparison table (yaad rakhne wali)

| Operation | Adjacency List | Adjacency Matrix | Edge List |
|---|---|---|---|
| **Memory** | `O(V + E)` | `O(V²)` | `O(E)` |
| Add edge | `O(1)` | `O(1)` | `O(1)` |
| Remove edge | `O(deg(u))` | `O(1)` | `O(E)` |
| Check `u—v` exists? | `O(deg(u))` | **`O(1)`** | `O(E)` |
| Iterate neighbours of `u` | **`O(deg(u))`** | `O(V)` | `O(E)` |
| Iterate all edges | `O(V + E)` | `O(V²)` | **`O(E)`** |
| BFS/DFS total | **`O(V + E)`** | `O(V²)` | pehle convert karo |

### Faisla (decision rule)

- **Sparse graph** (`E << V²`, jo aksar hota hai) → **adjacency list**. BFS/DFS `O(V+E)`.
- **Dense graph** ya `V` chhota (≤ ~500) aur baar baar "edge hai ya nahi" poochna hai → **matrix**.
- **Floyd-Warshall / matrix exponentiation** → matrix lazmi.
- **Kruskal MST / Bellman-Ford** → edge list.
- **Grid / puzzle states** → implicit, koi structure na banao.

**Gotcha:** Adjacency matrix `V = 10⁵` par `10¹⁰` cells maangega — memory blast. Interview me
constraints dekh kar representation choose karo, warna TLE/MLE.
"""))

cells.append(code('''
# Teen representations ke beech conversion — ye utility poore notebook me kaam aayegi
from collections import defaultdict

def edges_to_adj(n: int, edges, directed: bool = False, weighted: bool = False):
    """Edge list -> adjacency list (list-of-lists, nodes 0..n-1).
    weighted=True par neighbours (v, w) tuples hote hain, warna sirf v."""
    adj = [[] for _ in range(n)]
    for e in edges:
        if weighted:
            u, v, w = e
            adj[u].append((v, w))
            if not directed:
                adj[v].append((u, w))
        else:
            u, v = e[0], e[1]
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
    return adj

def edges_to_matrix(n: int, edges, directed: bool = False, weighted: bool = False, no_edge=0):
    """Edge list -> adjacency matrix. no_edge = jab edge na ho to kya rakhein (0 ya inf)."""
    mat = [[no_edge] * n for _ in range(n)]
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if weighted else 1
        mat[u][v] = w
        if not directed:
            mat[v][u] = w
    return mat

def adj_to_edges(adj, directed: bool = False, weighted: bool = False):
    """Adjacency list -> edge list (undirected me har edge sirf ek dafa)."""
    out = []
    for u, nbrs in enumerate(adj):
        for item in nbrs:
            v, w = item if weighted else (item, 1)
            if directed or u < v:            # undirected: duplicate se bachne ke liye u<v
                out.append((u, v, w) if weighted else (u, v))
    return out

E1 = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
A1 = edges_to_adj(5, E1)
M1 = edges_to_matrix(5, E1)

print("Adjacency list:", A1)
print("Adjacency matrix:")
for row in M1:
    print("  ", row)
print("Back to edges:", sorted(adj_to_edges(A1)))

assert A1 == [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3]]
assert M1[0][1] == 1 and M1[1][0] == 1 and M1[0][3] == 0
assert sorted(adj_to_edges(A1)) == sorted(E1)
print("Conversions OK")
''' ))

cells.append(code('''
# Implicit grid graph — neighbours "formula" se, koi adjacency list nahi
GRID = [
    [1, 1, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 1],
]
R, C = len(GRID), len(GRID[0])

# 4-directional moves (up, down, left, right) — ye tuple pattern har grid problem me use hoga
DIRS4 = ((-1, 0), (1, 0), (0, -1), (0, 1))
# 8-directional (diagonals bhi) — kuch problems me chahiye hota hai
DIRS8 = DIRS4 + ((-1, -1), (-1, 1), (1, -1), (1, 1))

def neighbours(r, c, dirs=DIRS4):
    """Grid ke andar rehne wale valid neighbours yield karta hai (bounds check lazmi)."""
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C:      # bounds check — yahan log sab se zyada phaste hain
            yield nr, nc

print("Grid:")
for row in GRID:
    print("  ", row)
print("(0,0) ke 4-dir neighbours:", list(neighbours(0, 0)))
print("(1,1) ke 4-dir neighbours:", list(neighbours(1, 1)))
print("(1,1) ke 8-dir neighbours:", len(list(neighbours(1, 1, DIRS8))), "neighbours")

# Corner cell ke sirf 2 neighbours hote hain, centre cell ke 4
assert len(list(neighbours(0, 0))) == 2
assert len(list(neighbours(1, 1))) == 4
print("Grid neighbour helper OK")
''' ))

# ============================================================
# 4. BFS
# ============================================================
cells.append(md("""
## 3. BFS — Breadth First Search

**Kya hai:** Level-by-level traversal. Source se shuru karo, pehle saare 1-step door wale nodes,
phir 2-step door wale, phir 3-step... Iske liye **queue (FIFO)** use hoti hai.

**Kyun / kahan:**
1. **Unweighted graph ka shortest path** — BFS ki sab se bari superpower. Kyunki BFS level-wise
   phailta hai, jis waqt kisi node ko pehli dafa touch kiya, wahi uska minimum distance hai.
2. Level order traversal (trees), "minimum number of steps/moves" wale saare problems.
3. Connected components, bipartite check, multi-source spread (rotting oranges, walls & gates).

### Template (rat lo — 90% BFS isi shakal me hoti hai)

```python
from collections import deque

def bfs(adj, src):
    dist = {src: 0}                 # visited + distance ek hi dict me (do structures na rakho)
    q = deque([src])
    while q:
        u = q.popleft()             # FIFO — LAZMI popleft, pop() nahi (pop() = DFS ban jayega)
        for v in adj[u]:
            if v not in dist:       # pehli dafa mila => shortest distance mil gaya
                dist[v] = dist[u] + 1
                q.append(v)         # mark-on-push (queue me daalte waqt hi visit mark karo)
    return dist
```

### Sab se bara BFS gotcha: **mark-on-push vs mark-on-pop**

- **Sahi:** node ko `visited` queue me **push karte waqt** mark karo.
- **Ghalat:** pop karte waqt mark karna → same node kai dafa queue me chala jayega →
  exponential blowup / TLE. Ye interview me sab se aam bug hai.

**Time:** `O(V + E)` — har vertex ek dafa pop hota hai, har edge ek dafa (directed) ya do dafa
(undirected) dekhi jaati hai.
**Space:** `O(V)` queue + visited ke liye.

**Interview tip:** "Minimum steps / fewest moves / shortest path in unweighted graph" sunte hi
BFS bolo. Agar weights hon to Dijkstra, agar weights sirf 0/1 hon to **0-1 BFS**.
"""))

cells.append(code('''
from collections import deque

def bfs_dist(adj, src):
    """Standard BFS: source se har node ki minimum edge-count distance."""
    dist = {src: 0}                     # visited ka kaam bhi ye dict karta hai
    q = deque([src])
    order = []                          # visit order (level by level) — sirf dikhane ke liye
    while q:
        u = q.popleft()                 # FIFO
        order.append(u)
        for v in adj[u]:
            if v not in dist:           # mark-on-push: yahin mark kar rahe hain
                dist[v] = dist[u] + 1
                q.append(v)
    return dist, order

#      0 --- 1 --- 3
#      |     |     |
#      2 ----+     4 --- 5
adjA = edges_to_adj(6, [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4), (4, 5)])
dist, order = bfs_dist(adjA, 0)
print("BFS order from 0:", order)
print("Distances       :", dist)

assert dist == {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4}
assert order[0] == 0 and set(order[1:3]) == {1, 2}      # level 1 me 1 aur 2 (order swap ho sakta)
print("BFS distances OK")

# BFS level-by-level (har level ko alag se process karna) — "level size" trick
def bfs_levels(adj, src):
    """Har level ko ek list me collect karta hai. Trick: loop ke shuru me len(q) le lo."""
    levels, q, seen = [], deque([src]), {src}
    while q:
        size = len(q)                   # is waqt queue me sirf current level hai
        cur = []
        for _ in range(size):           # exactly itne hi pop karo
            u = q.popleft()
            cur.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        levels.append(cur)
    return levels

L = bfs_levels(adjA, 0)
print("Levels:", L)
assert [len(x) for x in L] == [1, 2, 1, 1, 1]
print("Level-wise BFS OK")
''' ))

cells.append(code('''
# BFS se actual PATH nikalna (sirf distance nahi) — parent array trick
def bfs_path(adj, src, dst):
    """src se dst tak shortest path (list of nodes). Na mile to []."""
    if src == dst:
        return [src]
    parent = {src: None}                     # parent[v] = v se pehle kaun aaya
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in parent:
                parent[v] = u
                if v == dst:                 # early exit — mil gaya, aage BFS ki zaroorat nahi
                    path = []
                    cur = dst
                    while cur is not None:   # parent chain ko peeche ki taraf chalo
                        path.append(cur)
                        cur = parent[cur]
                    return path[::-1]        # ulta karo (dst..src -> src..dst)
                q.append(v)
    return []

p = bfs_path(adjA, 0, 5)
print("Path 0 -> 5:", p)
assert p[0] == 0 and p[-1] == 5 and len(p) == 5          # distance 4 => 5 nodes
assert bfs_path(adjA, 0, 0) == [0]
adj_disc = edges_to_adj(4, [(0, 1), (2, 3)])
assert bfs_path(adj_disc, 0, 3) == []                    # doosre component me — koi path nahi
print("BFS path reconstruction OK")
''' ))

cells.append(code('''
# MULTI-SOURCE BFS — ek se zyada starting points, ek hi baar me
# Idea: saare sources ko shuru me hi queue me daal do (distance 0). Bas.
# Ye "sab se qareeb kaun sa source hai" type problems ka O(V+E) hal hai.
def multi_source_bfs(adj, sources):
    """Har node ki distance = nearest source tak ki distance."""
    dist = {s: 0 for s in sources}          # saare sources ek sath level-0
    q = deque(sources)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

# Chain: 0-1-2-3-4-5-6 ; sources = {0, 6}
chain = edges_to_adj(7, [(i, i + 1) for i in range(6)])
d = multi_source_bfs(chain, [0, 6])
print("Nearest-source distances:", [d[i] for i in range(7)])
assert [d[i] for i in range(7)] == [0, 1, 2, 3, 2, 1, 0]
print("Multi-source BFS OK  (naive tareeqa: har source se alag BFS = O(S*(V+E)) — bekaar)")
''' ))

cells.append(code('''
# 0-1 BFS — jab edge weights sirf 0 ya 1 hon
# Dijkstra ki zaroorat nahi! deque use karo:
#   weight 0 edge -> appendleft (same "level")
#   weight 1 edge -> append     (next "level")
# Isse deque me distances monotonic rehti hain => O(V+E), heap ka log factor gaya.
def zero_one_bfs(n, adj, src):
    """adj[u] = [(v, w), ...] jahan w in {0, 1}."""
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:               # relaxation
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)       # free move — front me
                else:
                    dq.append(v)           # cost 1 — back me
    return dist

# 0 -(1)- 1 -(0)- 2 -(1)- 3 , aur shortcut 0 -(0)- 2
adj01 = edges_to_adj(4, [(0, 1, 1), (1, 2, 0), (2, 3, 1), (0, 2, 0)], weighted=True)
print("0-1 BFS distances:", zero_one_bfs(4, adj01, 0))
# Ghor karo: 0->2 free hai, aur 2->1 bhi free hai (undirected), is liye 1 ka cost bhi 0!
# Seedha edge 0-1 ka cost 1 tha, magar "muft" raasta sasta nikla — yehi 0-1 BFS ka maza hai.
assert zero_one_bfs(4, adj01, 0) == [0, 0, 0, 1]
print("0-1 BFS OK — LC 1368 / 1129 jaise problems ka trick")
''' ))

# ============================================================
# 5. DFS
# ============================================================
cells.append(md("""
## 4. DFS — Depth First Search

**Kya hai:** "Jitna andar ja sakte ho jao, phir wapis aa kar doosri branch." Stack (ya recursion)
use hoti hai.

**Kyun / kahan:**
1. Connected components, cycle detection, topological sort
2. Backtracking (paths enumerate karna, maze solving)
3. Tarjan algorithms — SCC, bridges, articulation points (entry/low times par based)
4. Tree/graph par "subtree ka jawab" nikalna (post-order me combine karna)

### Recursive template

```python
def dfs(u):
    visited.add(u)              # enter
    for v in adj[u]:
        if v not in visited:
            dfs(v)
    # yahan "exit / post-order" ka kaam
```

### Iterative template (recursion limit se bachne ke liye)

```python
stack = [src]
seen = {src}
while stack:
    u = stack.pop()             # LIFO
    for v in adj[u]:
        if v not in seen:
            seen.add(v)
            stack.append(v)
```

### Entry / Exit times (discovery & finish) — Tarjan ki bunyad

DFS chalate waqt ek global timer rakho:
- `tin[u]` = jab u pehli dafa enter hua
- `tout[u]` = jab u ka poora subtree khatam hua

Iske do jadoo:
1. **Ancestor test `O(1)`:** `u` `v` ka ancestor hai ⟺ `tin[u] < tin[v] and tout[v] < tout[u]`
2. **Edge classification:** tree edge / back edge (cycle!) / forward edge / cross edge

### Gotchas

- **Python recursion limit 1000 hai.** `V = 10⁵` wali chain par recursive DFS `RecursionError`
  degi. Hal: `sys.setrecursionlimit(300000)` (thread stack bhi barhana par sakta hai) ya
  **iterative DFS likho**. Interview me ye baat bolna bonus points deta hai.
- **Iterative DFS ka visit order recursive se mukhtalif hota hai** (neighbours ulte order me pop
  hote hain). Agar exact order maangi ho to `reversed(adj[u])` push karo.
- Iterative DFS me agar tumhein **post-order** kaam karna hai to "two-phase" trick use karo:
  `(node, False)` push, pop par `(node, True)` wapis push, phir children.
"""))

cells.append(code('''
import sys

def dfs_recursive(adj, src):
    """Simple recursive DFS — visit order return karta hai."""
    seen, order = set(), []
    def go(u):
        seen.add(u)                        # enter par mark
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                go(v)                      # deeper jao
    go(src)
    return order

def dfs_iterative(adj, src, match_recursive=True):
    """Iterative DFS. match_recursive=True par recursive jaisa hi order deta hai."""
    seen, order, stack = set(), [], [src]
    while stack:
        u = stack.pop()                    # LIFO
        if u in seen:                       # stack me duplicate aa sakta hai -> yahan filter
            continue
        seen.add(u)
        order.append(u)
        nbrs = list(adj[u])
        if match_recursive:
            nbrs = nbrs[::-1]              # ulta push karo taake pehla neighbour pehle pop ho
        for v in nbrs:
            if v not in seen:
                stack.append(v)
    return order

adjB = edges_to_adj(7, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
r_order = dfs_recursive(adjB, 0)
i_order = dfs_iterative(adjB, 0)
print("Recursive DFS:", r_order)
print("Iterative DFS:", i_order)
print("Iterative (no reverse):", dfs_iterative(adjB, 0, match_recursive=False))

assert r_order == i_order == [0, 1, 3, 4, 2, 5, 6]
print("\\nRecursion limit ab:", sys.getrecursionlimit(), "-> bari chain par iterative use karo")
''' ))

cells.append(code('''
# Entry / Exit times + edge classification
def dfs_times(n, adj, directed=False):
    """tin/tout nikalta hai aur edges ko classify karta hai."""
    tin, tout = [-1] * n, [-1] * n
    timer = 0
    state = [0] * n                       # 0=white(untouched) 1=gray(on stack) 2=black(done)
    kinds = []                            # (u, v, kind)

    def go(u, parent):
        nonlocal timer
        state[u] = 1
        tin[u] = timer; timer += 1
        for v in adj[u]:
            if not directed and v == parent:
                continue                   # undirected me parent wapis jana edge nahi ginte
            if state[v] == 0:
                kinds.append((u, v, "tree"))
                go(v, u)
            elif state[v] == 1:
                kinds.append((u, v, "back"))       # BACK EDGE => CYCLE hai!
            else:
                # black: directed graph me forward ya cross
                kinds.append((u, v, "forward" if tin[u] < tin[v] else "cross"))
        state[u] = 2
        tout[u] = timer; timer += 1

    for s in range(n):
        if state[s] == 0:
            go(s, -1)
    return tin, tout, kinds

tin, tout, kinds = dfs_times(4, edges_to_adj(4, [(0, 1), (1, 2), (2, 0), (1, 3)], directed=True), directed=True)
print("tin :", tin)
print("tout:", tout)
for u, v, k in kinds:
    print(f"  edge {u}->{v}: {k}")

def is_ancestor(u, v):
    """O(1) ancestor test — tin/tout nesting se."""
    return tin[u] < tin[v] and tout[v] < tout[u]

assert is_ancestor(0, 3) is True         # 0 -> 1 -> 3
assert is_ancestor(3, 0) is False
assert any(k == "back" for _, _, k in kinds)   # 2->0 back edge => cycle
print("Ancestor test + back edge detection OK")
''' ))

cells.append(code('''
# DFS se SAARE paths (path tracking + backtracking) — LC 797 ka core
def all_paths(adj, src, dst):
    """src se dst tak ke saare simple paths. DAG par safe; cycle wale graph par visited chahiye."""
    res, path = [], [src]
    def go(u):
        if u == dst:
            res.append(path.copy())        # COPY lazmi — warna sab paths same list ban jayenge
            return
        for v in adj[u]:
            path.append(v)                 # choose
            go(v)
            path.pop()                     # un-choose (BACKTRACK) — ye line bhoolna #1 bug hai
    go(src)
    return res

dag = [[1, 2], [3], [3], []]               # 0->1->3, 0->2->3
paths = all_paths(dag, 0, 3)
print("Saare paths 0 -> 3:", paths)
assert sorted(paths) == [[0, 1, 3], [0, 2, 3]]
print("Path tracking OK — 'path.copy()' aur 'path.pop()' dono lazmi")
''' ))

# ============================================================
# 6. COMPONENTS / CYCLES / BIPARTITE
# ============================================================
cells.append(md("""
## 5. Connected Components

**Kya hai:** Graph ke woh alag alag "jazeere" (islands) jinke darmiyan koi edge nahi.

**Template:** Har node par loop chalao; agar `visited` nahi hai to naya component shuru hua —
BFS/DFS chala kar poora component mark kar do. Counter barha do.

```python
count = 0
for s in range(n):
    if s not in seen:
        count += 1
        dfs(s)          # ya bfs(s)
```

**Time:** `O(V + E)` — loop dekhne me `O(V)` hai lekin har node sirf ek dafa traverse hota hai.

**Kahan use hota:** LC 547 (Number of Provinces), LC 200 (Number of Islands), network clustering,
"kitne groups ban rahe hain" wale saare problems. Aur DSU (Union-Find) isi ka doosra hal hai —
NB3 me detail me.
"""))

cells.append(code('''
def count_components(n, adj):
    """Components ki tadaad + har component ki node list."""
    seen, comps = set(), []
    for s in range(n):
        if s in seen:
            continue
        # naya component mila -> BFS se poora nikalo
        comp, q = [], deque([s])
        seen.add(s)
        while q:
            u = q.popleft()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        comps.append(sorted(comp))
    return len(comps), comps

adjC = edges_to_adj(8, [(0, 1), (1, 2), (3, 4), (5, 6)])   # node 7 isolated
cnt, comps = count_components(8, adjC)
print("Components:", cnt)
for i, c in enumerate(comps):
    print(f"  #{i+1}: {c}")
assert cnt == 4
assert comps == [[0, 1, 2], [3, 4], [5, 6], [7]]
print("Connected components OK (isolated node bhi ek component hota hai — ye bhoolna aam bug)")
''' ))

cells.append(md("""
## 6. Cycle Detection — undirected vs directed (do bilkul alag tareeqe!)

Ye interview ka classic trap hai. Dono cases ka logic mukhtalif hai:

### (a) Undirected graph — "parent skip" trick

DFS karte waqt jis node se aaye ho (parent) usay ignore karo. Agar koi **already-visited node**
mil jaye jo parent nahi hai → **cycle**.

```python
def has_cycle(u, parent):
    seen.add(u)
    for v in adj[u]:
        if v == parent: continue        # jahan se aaye wahan wapis dekhna cycle nahi
        if v in seen: return True       # visited + non-parent => CYCLE
        if has_cycle(v, u): return True
    return False
```

**Gotcha:** parallel edges (`u—v` do dafa) hon to ye "parent skip" ghalat jawab de sakta hai.
Us surat me parent ki jagah **edge id** skip karo.

### (b) Directed graph — "3 colors" / recursion-stack trick

Sirf `visited` kaafi nahi! Kyunki directed me ek already-visited node par pohonchna cycle nahi hota
(wo doosri branch se pehle process ho chuka ho sakta hai). Isliye teen halatein rakho:

| Color | Matlab |
|---|---|
| **WHITE (0)** | Abhi tak touch nahi hua |
| **GRAY (1)** | Current DFS path (recursion stack) par hai |
| **BLACK (2)** | Poora process ho gaya, is se koi cycle nahi nikalti |

**GRAY node par edge mil gaya ⟹ back edge ⟹ CYCLE.**

**Alternative:** Kahn's algorithm — agar topological sort me saare `V` nodes na aayein to cycle hai.
(Ye zyada aasan hota hai code karna, LC 207 ka pasandida hal.)

**Time:** dono `O(V + E)`. **Space:** `O(V)`.
"""))

cells.append(code('''
def has_cycle_undirected(n, adj):
    """Undirected cycle detection — parent skip trick (iterative, recursion-safe)."""
    seen = [False] * n
    for s in range(n):
        if seen[s]:
            continue
        stack = [(s, -1)]                   # (node, parent)
        seen[s] = True
        while stack:
            u, p = stack.pop()
            for v in adj[u]:
                if v == p:
                    continue                # parent — ignore
                if seen[v]:
                    return True             # visited + not parent => cycle
                seen[v] = True
                stack.append((v, u))
    return False

tree4 = edges_to_adj(4, [(0, 1), (1, 2), (1, 3)])          # tree -> no cycle
cyc4 = edges_to_adj(4, [(0, 1), (1, 2), (2, 0), (2, 3)])   # triangle -> cycle
assert has_cycle_undirected(4, tree4) is False
assert has_cycle_undirected(4, cyc4) is True
print("Undirected: tree ->", has_cycle_undirected(4, tree4), "| triangle ->", has_cycle_undirected(4, cyc4))


def has_cycle_directed(n, adj):
    """Directed cycle detection — 3 colors (0 white, 1 gray, 2 black)."""
    color = [0] * n
    def go(u):
        color[u] = 1                        # GRAY: current path par
        for v in adj[u]:
            if color[v] == 1:
                return True                 # GRAY par edge => back edge => cycle
            if color[v] == 0 and go(v):
                return True
        color[u] = 2                        # BLACK: done
        return False
    return any(color[s] == 0 and go(s) for s in range(n))

# 0->1->2 ; 0->2  (diamond, koi cycle nahi — lekin sirf 'visited' wala ghalat code isay cycle kehta)
dag_diamond = edges_to_adj(3, [(0, 1), (1, 2), (0, 2)], directed=True)
dcyc = edges_to_adj(3, [(0, 1), (1, 2), (2, 0)], directed=True)
assert has_cycle_directed(3, dag_diamond) is False
assert has_cycle_directed(3, dcyc) is True
print("Directed: diamond ->", has_cycle_directed(3, dag_diamond), "| 0->1->2->0 ->", has_cycle_directed(3, dcyc))
print("\\nSABAK: directed me sirf `visited` set se cycle detect karna GHALAT hai — gray/black chahiye.")
''' ))

cells.append(md("""
## 7. Bipartite Check — 2-Coloring

**Kya hai:** Graph bipartite hai agar vertices ko **do rangon** (0 aur 1) me baant sakein aisay ke
**har edge ke dono sire mukhtalif rang** ke hon.

**Kyun:** "Do teams me baant do", "dushmani ke hisaab se 2 groups", matching problems,
"odd length cycle hai ya nahi" — sab bipartite check hai.

**Theorem (yaad rakho):** Graph bipartite hai **⟺ koi odd-length cycle nahi hai.**

**Tareeqa:** BFS/DFS karte hue rang do. Source ko 0, uske neighbours ko 1, unke neighbours ko 0...
Agar kabhi **same rang** wale do nodes ke beech edge mile → not bipartite.

**Gotcha:** Graph disconnected ho sakta hai → **har component** par alag se check karo.
LC 785 me exactly yehi trap hai.

**Time:** `O(V + E)`, **Space:** `O(V)`.
"""))

cells.append(code('''
def is_bipartite(n, adj):
    """BFS 2-coloring. color[] me -1 = uncolored. Disconnected components handle karta hai."""
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue                        # already colored
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]  # ulta rang (0<->1)
                    q.append(v)
                elif color[v] == color[u]:
                    return False, []         # same rang wali edge => odd cycle => not bipartite
    return True, color

even_cycle = edges_to_adj(4, [(0, 1), (1, 2), (2, 3), (3, 0)])   # C4 -> bipartite
odd_cycle = edges_to_adj(3, [(0, 1), (1, 2), (2, 0)])            # C3 -> nahi
ok, col = is_bipartite(4, even_cycle)
print("C4 bipartite?", ok, "colors:", col)
print("C3 bipartite?", is_bipartite(3, odd_cycle)[0])
assert ok is True and col == [0, 1, 0, 1]
assert is_bipartite(3, odd_cycle)[0] is False
# Disconnected: dono halves bipartite -> poora graph bipartite
assert is_bipartite(6, edges_to_adj(6, [(0, 1), (2, 3), (4, 5)]))[0] is True
print("Bipartite check OK")
''' ))

cells.append(md("""
## 8. Topological Sort — DAG ka linear order

**Kya hai:** DAG ke vertices ka aisa order jahan **har edge `u → v` ke liye `u` pehle aaye**.

**Kyun:** Dependency resolution — course prerequisites, build systems (`make`), package managers
(`pip`, `npm`), task scheduling, spreadsheet formula evaluation, DAG shortest path.

**Bunyadi shart:** Sirf **DAG** par mumkin hai. Cycle ho to topological order **wajood hi nahi
rakhta** — aur isi liye topo sort **cycle detection ka bhi tareeqa** hai.

### Do tareeqe

**(a) Kahn's Algorithm (BFS style) — indegree based**

1. Sab ke in-degree nikalo.
2. Jinka in-degree 0 hai unhein queue me daalo.
3. Pop karo → answer me daalo → uske har neighbour ka in-degree `-1` karo → 0 ho jaye to queue me.
4. Aakhir me `len(answer) < V` ⟹ **cycle hai**.

**(b) DFS + reverse postorder**

DFS karo; jab node ka poora subtree khatam ho (post-order) to usay stack me push karo.
Aakhir me stack ulta karo. Cycle detection ke liye gray/black colors sath rakho.

### Lexicographically smallest topo order

Kahn me `deque` ki jagah **min-heap** use karo → `O((V+E) log V)`. (LC 210 ke follow-up me poocha
jaata hai.)

**Gotcha:** Topological order **unique nahi hota** (aksar). Interview me "koi ek valid order"
maanga jaata hai — apne test me exact list compare karne ki bajaye **validity check** likho.

**Time:** `O(V + E)`, **Space:** `O(V)`.
"""))

cells.append(code('''
import heapq

def topo_kahn(n, adj):
    """Kahn's algorithm. Return (order, is_dag). Cycle par order adhoora hoga."""
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1                    # in-degree count
    q = deque(i for i in range(n) if indeg[i] == 0)   # sab "free" nodes
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1                    # u nikal gaya => v ki ek dependency kam
            if indeg[v] == 0:
                q.append(v)
    return order, len(order) == n            # len < n => cycle

def topo_dfs(n, adj):
    """DFS postorder + reverse. (order, is_dag)."""
    color = [0] * n
    out = []
    ok = True
    def go(u):
        nonlocal ok
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1:
                ok = False                   # back edge => cycle
            elif color[v] == 0:
                go(v)
        color[u] = 2
        out.append(u)                        # POST-order me push
    for s in range(n):
        if color[s] == 0:
            go(s)
    return out[::-1], ok                     # reverse postorder = topological order

def topo_lexicographic(n, adj):
    """Lexicographically smallest topological order — heap se."""
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    h = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(h)
    order = []
    while h:
        u = heapq.heappop(h)                 # sab available me se SAB SE CHHOTA
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    return order, len(order) == n

def is_valid_topo(n, adj, order):
    """Validity checker — kyunki topo order unique nahi hota."""
    if sorted(order) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u in range(n) for v in adj[u])

# 5 -> 2 -> 3 -> 1 ; 4 -> 0 , 4 -> 1 , 5 -> 0
D = edges_to_adj(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)], directed=True)
k_order, k_ok = topo_kahn(6, D)
d_order, d_ok = topo_dfs(6, D)
l_order, _ = topo_lexicographic(6, D)
print("Kahn      :", k_order, "DAG?", k_ok)
print("DFS       :", d_order, "DAG?", d_ok)
print("Lexicographic smallest:", l_order)

assert k_ok and d_ok
assert is_valid_topo(6, D, k_order) and is_valid_topo(6, D, d_order) and is_valid_topo(6, D, l_order)
assert l_order == [4, 5, 0, 2, 3, 1]

# Cycle wale graph par
C = edges_to_adj(3, [(0, 1), (1, 2), (2, 0)], directed=True)
assert topo_kahn(3, C)[1] is False and topo_dfs(3, C)[1] is False
print("\\nCycle wale graph par: Kahn DAG? ->", topo_kahn(3, C)[1], "(topo sort mumkin nahi)")
''' ))

# ============================================================
# 7. SCC + BRIDGES
# ============================================================
cells.append(md("""
## 9. Strongly Connected Components (SCC) — Kosaraju aur Tarjan

**Kya hai:** Directed graph me SCC = vertices ka aisa maximal group jahan **har node se har node
tak** raasta ho.

**Kyun:** SCC ko ek node maan kar "condense" kar do to graph **DAG** ban jaata hai
(**condensation graph**). Uske baad topological sort, DP — sab kuch mumkin. Use cases: deadlock
detection, 2-SAT, "kaun se accounts ek dusre ko promote kar rahe hain" (link farms), compiler
optimizations.

### (a) Kosaraju's Algorithm — 2 DFS pass (samajhna aasan)

1. Original graph par DFS karo, **finish order** (postorder) record karo.
2. Graph ko **reverse** karo (saari edges ulti).
3. Reverse graph par finish-order ke **ulte** hisaab se DFS karo — har DFS tree = ek SCC.

**Kyun kaam karta hai (intuition):** Reverse graph ke SCCs same hote hain, lekin condensation DAG
ulta ho jaata hai — is liye "sink" component pehle process hota hai aur DFS us se bahar nahi
nikal sakta.

### (b) Tarjan's Algorithm — 1 DFS pass (efficient, lekin low-link samajhna parta hai)

- `disc[u]` = discovery time, `low[u]` = u ke subtree se (ek back edge ke through) pohonchne wala
  sab se chhota discovery time.
- Stack par "abhi tak kisi SCC me assign nahi hue" nodes rakho.
- Agar `low[u] == disc[u]` → `u` apni SCC ka **root** hai → stack se `u` tak pop kar do.

**Time:** dono `O(V + E)`. Tarjan constant factor behtar (1 pass), Kosaraju likhna aasan.

**Interview tip:** Agar poocha jaye "SCC" to Kosaraju bolo (explain karna aasan), aur mention karo
ke Tarjan single-pass hai. Practical LeetCode me SCC kam aata hai (LC 1192 critical connections
undirected bridges hai) — lekin senior interviews me poocha jaata hai.
"""))

cells.append(code('''
def kosaraju(n, adj):
    """SCCs (list of lists). 2-pass DFS, iterative (recursion-safe)."""
    # Pass 1: finish order nikalo (iterative postorder)
    seen = [False] * n
    finish = []
    for s in range(n):
        if seen[s]:
            continue
        stack = [(s, iter(adj[s]))]
        seen[s] = True
        while stack:
            u, it = stack[-1]
            advanced = False
            for v in it:                       # generator jahan chhora tha wahin se chalega
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, iter(adj[v])))
                    advanced = True
                    break
            if not advanced:
                finish.append(u)               # poora subtree done -> postorder
                stack.pop()

    # Reverse graph banao
    radj = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)

    # Pass 2: reverse graph par, finish order ke ULTE hisaab se
    comp = [-1] * n
    sccs = []
    for s in reversed(finish):
        if comp[s] != -1:
            continue
        cid = len(sccs)
        cur, st = [], [s]
        comp[s] = cid
        while st:
            u = st.pop()
            cur.append(u)
            for v in radj[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    st.append(v)
        sccs.append(sorted(cur))
    return sccs, comp

# 0->1->2->0 (SCC), 2->3, 3->4->5->3 (SCC), 6 alone
E_scc = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3)]
adjS = edges_to_adj(7, E_scc, directed=True)
sccs, comp = kosaraju(7, adjS)
print("SCCs (Kosaraju):", sorted(sccs))
assert sorted(sccs) == [[0, 1, 2], [3, 4, 5], [6]]
print("Kosaraju OK — 3 SCCs")

# Condensation graph: SCC ko ek node maan kar DAG banao
cond = set()
for u in range(7):
    for v in adjS[u]:
        if comp[u] != comp[v]:
            cond.add((comp[u], comp[v]))
print("Condensation DAG edges:", sorted(cond), "-> ye ab DAG hai (acyclic)")
''' ))

cells.append(code('''
def tarjan_scc(n, adj):
    """Tarjan's SCC — single DFS pass, iterative version."""
    disc = [-1] * n            # discovery time
    low = [0] * n              # low-link value
    on_stack = [False] * n
    stack = []                 # current SCC candidates
    sccs = []
    timer = 0

    for root in range(n):
        if disc[root] != -1:
            continue
        # iterative DFS: frame = (node, neighbour_index)
        work = [(root, 0)]
        while work:
            u, i = work[-1]
            if i == 0:                          # pehli dafa u par aaye
                disc[u] = low[u] = timer; timer += 1
                stack.append(u); on_stack[u] = True
            recursed = False
            while i < len(adj[u]):
                v = adj[u][i]
                i += 1
                work[-1] = (u, i)
                if disc[v] == -1:
                    work.append((v, 0))         # "recurse"
                    recursed = True
                    break
                elif on_stack[v]:
                    low[u] = min(low[u], disc[v])   # back edge -> low update
            if recursed:
                continue
            # u done: parent ka low update karo
            work.pop()
            if work:
                p = work[-1][0]
                low[p] = min(low[p], low[u])
            if low[u] == disc[u]:               # u SCC ka root hai
                cur = []
                while True:
                    w = stack.pop(); on_stack[w] = False
                    cur.append(w)
                    if w == u:
                        break
                sccs.append(sorted(cur))
    return sccs

t_sccs = tarjan_scc(7, adjS)
print("SCCs (Tarjan)  :", sorted(t_sccs))
assert sorted(t_sccs) == sorted(sccs), "Tarjan aur Kosaraju ka jawab same hona chahiye"
print("Tarjan == Kosaraju  ✔")
''' ))

cells.append(md("""
## 10. Bridges aur Articulation Points (brief)

**Undirected graph** ke "critical" hisse:

- **Bridge (cut edge):** wo edge jise hatane par components barh jaayein.
  → Network ka woh cable jiske katne se network toot jaye. (LC 1192 Critical Connections)
- **Articulation Point (cut vertex):** wo vertex jise hatane par components barh jaayein.
  → Woh router jiske band hone se network toot jaye.

**Tarjan low-link condition:**
- Edge `(u, v)` bridge hai ⟺ `low[v] > disc[u]` (v ke subtree se u ya us se upar koi back edge nahi)
- Vertex `u` articulation point hai ⟺
  - `u` root hai aur uske **2 ya zyada** DFS children hain, **ya**
  - `u` root nahi aur kisi child `v` ke liye `low[v] >= disc[u]`

**Note ka farq:** bridge me `>` (strictly), articulation point me `>=`. Ye ek chhota sa farq
interview me poocha jaata hai.

**Time:** `O(V + E)`.
"""))

cells.append(code('''
def bridges_and_articulation(n, adj):
    """Tarjan low-link se bridges aur articulation points (recursive, chhote graph ke liye)."""
    disc = [-1] * n
    low = [0] * n
    bridges, arts = [], set()
    timer = 0

    def go(u, parent):
        nonlocal timer
        disc[u] = low[u] = timer; timer += 1
        children = 0
        for v in adj[u]:
            if v == parent:
                continue                        # parent ko skip (single edge assumption)
            if disc[v] != -1:
                low[u] = min(low[u], disc[v])   # back edge
            else:
                children += 1
                go(v, u)
                low[u] = min(low[u], low[v])    # child ka low uthao
                if low[v] > disc[u]:
                    bridges.append(tuple(sorted((u, v))))   # STRICT > => bridge
                if parent != -1 and low[v] >= disc[u]:
                    arts.add(u)                             # >= => articulation point
        if parent == -1 and children > 1:
            arts.add(u)                          # root: 2+ children => cut vertex
    for s in range(n):
        if disc[s] == -1:
            go(s, -1)
    return sorted(bridges), sorted(arts)

#  0-1-2 triangle (koi bridge nahi), phir 2-3 bridge, 3-4 bridge
Eb = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]
br, ap = bridges_and_articulation(5, edges_to_adj(5, Eb))
print("Bridges           :", br)
print("Articulation points:", ap)
assert br == [(2, 3), (3, 4)]
assert ap == [2, 3]
print("Triangle ke andar koi bridge nahi (cycle me har edge ka alternative raasta hai) ✔")
''' ))

# ============================================================
# 8. SHORTEST PATHS
# ============================================================
cells.append(md("""
## 11. Dijkstra's Algorithm — non-negative weighted shortest path

**Kya hai:** Ek source se saare nodes tak **minimum total weight** ka raasta. Greedy: har baar
"sab se qareeb, abhi tak finalize na hua" node uthao aur uske neighbours relax karo.

**Implementation (lazy deletion wala, Python me standard):**

```python
import heapq
dist = [inf]*n; dist[src] = 0
pq = [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]: continue       # STALE entry — ye line performance ke liye lazmi
    for v, w in adj[u]:
        nd = d + w
        if nd < dist[v]:
            dist[v] = nd
            heapq.heappush(pq, (nd, v))
```

**Time:** `O((V + E) log V)` binary heap ke sath. `O(V²)` simple array version (dense graph par
behtar). **Space:** `O(V + E)`.

### Negative weights kyun NAHI chalte

Dijkstra ki bunyadi assumption: **jab node pop hua, uska distance final hai.** Ye is liye sahi hai
ke aage ka har edge distance ko sirf **barha** sakta hai. Negative edge is assumption ko tor deta hai.

Misaal: `A→B = 1`, `A→C = 5`, `C→B = -10`.
Dijkstra pehle `B` ko `1` par finalize kar dega, jabke asli shortest `A→C→B = -5` hai. Ghalat jawab.

**Hal:** Bellman-Ford (negative edges OK) ya Johnson's algorithm (reweighting).

### Gotchas

- `visited` set optional hai (stale check `d > dist[u]` kaafi hai), lekin **`d > dist[u]` skip
  bhoolna** = TLE.
- Heap me tuple `(dist, node)` daalo — `dist` pehle, warna sorting node par hogi.
- Node non-integer ho (string) to `dist` dict use karo aur tie-break ka khayal rakho.
- Sirf ek target chahiye? `u == target` par pop hote hi `return` — early exit.
"""))

cells.append(code('''
import heapq
INF = float("inf")

def dijkstra(n, adj, src, target=None):
    """adj[u] = [(v, w), ...] with w >= 0. Returns (dist, parent)."""
    dist = [INF] * n
    parent = [-1] * n
    dist[src] = 0
    pq = [(0, src)]                        # (distance, node) — distance PEHLE
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                       # stale/purani entry — skip (bohat zaroori)
        if target is not None and u == target:
            break                          # early exit — sirf ek target chahiye tha
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:               # relaxation
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent

def rebuild_path(parent, src, dst):
    """parent array se path nikalo."""
    if src == dst:
        return [src]
    path, cur = [], dst
    while cur != -1:
        path.append(cur)
        if cur == src:
            return path[::-1]
        cur = parent[cur]
    return []                              # reachable nahi

#      (4)      (8)
#   0 ----- 1 ----- 2
#   | (1)   | (2)   | (1)
#   3 ----- 4 ----- 5
Ew = [(0, 1, 4), (1, 2, 8), (0, 3, 1), (1, 4, 2), (2, 5, 1), (3, 4, 5), (4, 5, 3)]
adjW = edges_to_adj(6, Ew, weighted=True)
dist, par = dijkstra(6, adjW, 0)
print("Dijkstra distances from 0:", dist)
print("Path 0 -> 5:", rebuild_path(par, 0, 5))
assert dist == [0, 4, 10, 1, 6, 9]     # note: 2 tak ka behtar raasta 0-3-4-5-2 = 10 (0-1-2 = 12 nahi)
assert rebuild_path(par, 0, 5) == [0, 3, 4, 5]

# Negative edge par Dijkstra ka GHALAT jawab — demo
neg = edges_to_adj(3, [(0, 1, 1), (0, 2, 5), (2, 1, -10)], directed=True, weighted=True)
d_wrong, _ = dijkstra(3, neg, 0)
print("\\nNegative edge ke sath Dijkstra:", d_wrong, "<- node 1 ka jawab", d_wrong[1], "diya")
print("Asli shortest 0->2->1 =", 5 + (-10), "=> Dijkstra GHALAT hai. Bellman-Ford use karo.")
''' ))

cells.append(md("""
## 12. Bellman-Ford — negative weights aur negative cycle detection

**Kya hai:** `V-1` dafa **saari edges** relax karo. Har pass me shortest paths ki "ek extra edge"
tak ki information phail jaati hai.

**Kyun `V-1` passes?** Kisi bhi simple shortest path me maximum `V-1` edges ho sakti hain.

**Negative cycle detection:** `V-1` passes ke baad **ek aur** pass karo. Agar koi distance abhi bhi
kam ho rahi hai → **negative cycle** hai (shortest path define hi nahi hota, cycle ghum kar
infinitely kam kar sakte ho).

**Time:** `O(V · E)` — Dijkstra se slow. **Space:** `O(V)`.

### Kab use karein

| Halat | Algorithm |
|---|---|
| Non-negative weights | **Dijkstra** (tez) |
| Negative weights, no negative cycle | **Bellman-Ford** |
| Negative cycle detect karna hai | **Bellman-Ford** |
| DAG (negative bhi OK) | **Topo order DP** — sab se tez, `O(V+E)` |
| All-pairs, chhota V | **Floyd-Warshall** |
| Exactly `k` edges tak ki limit | **Bellman-Ford ka k-pass version** (LC 787!) |

**Optimization:** agar koi pass me kuch bhi na badle → early break. (SPFA queue-based version bhi
hota hai lekin worst case wahi rehta hai.)

**LC 787 (Cheapest Flights Within K Stops)** Bellman-Ford ke `k+1` passes ka perfect misaal hai —
lekin **layer copy** lazmi hai (warna ek hi pass me multiple hops ho jaate hain).
"""))

cells.append(code('''
def bellman_ford(n, edges, src):
    """edges = [(u, v, w)] directed. Returns (dist, has_negative_cycle)."""
    dist = [INF] * n
    dist[src] = 0
    for i in range(n - 1):                 # V-1 passes
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                          # early exit optimization
    # extra pass: abhi bhi improve ho raha hai? => negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return dist, True
    return dist, False

# Negative edge, lekin negative cycle nahi
E_neg = [(0, 1, 4), (0, 2, 5), (1, 3, 3), (2, 1, -10), (3, 4, 2)]
d, neg_cycle = bellman_ford(5, E_neg, 0)
print("Bellman-Ford:", d, "| negative cycle?", neg_cycle)
assert d == [0, -5, 5, -2, 0]
assert neg_cycle is False

# Negative cycle: 1 -> 2 -> 1 with total -1
E_nc = [(0, 1, 1), (1, 2, 2), (2, 1, -4)]
d2, nc2 = bellman_ford(3, E_nc, 0)
print("Negative cycle wala graph -> detected?", nc2)
assert nc2 is True
print("Bellman-Ford OK — Dijkstra se O(VE) slow hai, lekin negatives handle karta hai")
''' ))

cells.append(code('''
def floyd_warshall(n, edges, directed=True):
    """All-pairs shortest path. O(V^3). Chhote dense graphs ke liye best (V <= ~400)."""
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0                        # apne aap tak 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)          # parallel edges: minimum lo
        if not directed:
            d[v][u] = min(d[v][u], w)
    # TEEN nested loops — k SAB SE BAHAR hona LAZMI hai (ye #1 bug hai)
    for k in range(n):                     # k = "intermediate" node jise ab allow kar rahe hain
        for i in range(n):
            if d[i][k] == INF:
                continue                   # chhota optimization
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d

Efw = [(0, 1, 3), (1, 2, 1), (2, 0, 2), (0, 3, 7), (2, 3, 1)]
FW = floyd_warshall(4, Efw)
print("All-pairs shortest paths:")
for row in FW:
    print("  ", ["inf" if x == INF else x for x in row])
assert FW[0][3] == 5          # 0->1->2->3 = 3+1+1 = 5 (direct 7 se behtar)
assert FW[1][0] == 3          # 1->2->0 = 1+2
assert FW[3][0] == INF        # 3 se kahin nahi ja sakte
# Negative cycle check: koi d[i][i] < 0 ho jaye
print("Koi negative cycle?", any(FW[i][i] < 0 for i in range(4)))
print("Floyd-Warshall OK — yaad rakho: k ka loop SAB SE BAHAR")
''' ))

cells.append(code('''
# DAG SHORTEST PATH — topological order me ek pass. Negative weights bhi bilkul OK!
# Kyun kaam karta hai: topo order me jab u process kar rahe ho, uski dist final ho chuki hai.
def dag_shortest_path(n, adj, src):
    """adj[u] = [(v, w)] DAG. O(V+E) — Dijkstra se bhi tez, negatives allowed."""
    # topo order nikalo (weights ignore kar ke)
    plain = [[v for v, _ in adj[u]] for u in range(n)]
    order, ok = topo_kahn(n, plain)
    assert ok, "DAG nahi hai!"
    dist = [INF] * n
    dist[src] = 0
    for u in order:                        # topo order me ek hi pass
        if dist[u] == INF:
            continue                       # unreachable — aage relax ka faida nahi
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist

# 0->1(5), 0->2(3), 1->3(-2), 2->1(2), 2->3(6)
adj_dag = edges_to_adj(4, [(0, 1, 5), (0, 2, 3), (1, 3, -2), (2, 1, 2), (2, 3, 6)],
                       directed=True, weighted=True)
dd = dag_shortest_path(4, adj_dag, 0)
print("DAG shortest path (negative edge ke sath):", dd)
assert dd == [0, 5, 3, 3]      # 0->1=5 (0->2->1=5 bhi) ; 0->1->3 = 5-2 = 3
print("DAG me O(V+E) — Dijkstra ki bhi zaroorat nahi. LONGEST path ke liye min ko max kar do!")
''' ))

cells.append(md("""
## 13. A\\* Search ka taaruf (heuristic search)

**Kya hai:** Dijkstra ka "smart" version. Dijkstra sab taraf barabar phailta hai; A\\* ek
**heuristic** `h(n)` (target tak ka *andaza*) use karta hai taake target ki taraf pehle jaye.

**Formula:** priority = `f(n) = g(n) + h(n)`
- `g(n)` = source se n tak ki asli cost (jo ab tak mili)
- `h(n)` = n se target tak ka **andaza** (estimate)

**Shartein (bohat zaroori):**
- **Admissible:** `h(n)` kabhi asli cost se **zyada** na ho (over-estimate na kare) → optimal answer.
- **Consistent/monotone:** `h(u) <= w(u,v) + h(v)` → koi node dobara expand nahi hota.

**Aam heuristics (grid par):**
- 4-directional movement → **Manhattan distance** `|dr| + |dc|`
- 8-directional → **Chebyshev** `max(|dr|, |dc|)`
- Free movement → **Euclidean**
- `h(n) = 0` → A\\* bilkul **Dijkstra ban jaata hai** (special case)

**Kahan:** game pathfinding, robotics, puzzle solving (8-puzzle), maps/navigation.

**Interview me:** A\\* aksar sirf "concept" level par poocha jaata hai — "Dijkstra ko kaise tez
karoge agar target ek hi ho?" ka jawab A\\* hai.
"""))

cells.append(code('''
# A* on a grid — Manhattan heuristic
def astar_grid(grid, start, goal):
    """0 = chalne layak, 1 = deewar. 4-directional. Returns (cost, expanded_nodes)."""
    R, C = len(grid), len(grid[0])
    def h(p):                                   # Manhattan distance — admissible for 4-dir
        return abs(p[0] - goal[0]) + abs(p[1] - goal[1])
    g = {start: 0}
    pq = [(h(start), 0, start)]                 # (f, g, node)
    expanded = 0
    while pq:
        f, gu, u = heapq.heappop(pq)
        if gu > g.get(u, INF):
            continue                            # stale
        expanded += 1
        if u == goal:
            return gu, expanded
        r, c = u
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                ng = gu + 1
                if ng < g.get((nr, nc), INF):
                    g[(nr, nc)] = ng
                    heapq.heappush(pq, (ng + h((nr, nc)), ng, (nr, nc)))
    return -1, expanded

maze = [
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
cost_a, exp_a = astar_grid(maze, (0, 0), (4, 4))
print(f"A*: cost={cost_a}, nodes expanded={exp_a}")

# Wahi cheez h=0 ke sath (yaani Dijkstra/BFS) — zyada nodes expand honge
def dijkstra_grid(grid, start, goal):
    R, C = len(grid), len(grid[0])
    g = {start: 0}; pq = [(0, start)]; expanded = 0
    while pq:
        gu, u = heapq.heappop(pq)
        if gu > g.get(u, INF):
            continue
        expanded += 1
        if u == goal:
            return gu, expanded
        r, c = u
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and gu + 1 < g.get((nr, nc), INF):
                g[(nr, nc)] = gu + 1
                heapq.heappush(pq, (gu + 1, (nr, nc)))
    return -1, expanded

cost_d, exp_d = dijkstra_grid(maze, (0, 0), (4, 4))
print(f"Dijkstra (h=0): cost={cost_d}, nodes expanded={exp_d}")
assert cost_a == cost_d == 8, "dono ka COST same hona chahiye (A* admissible hai)"
print("Cost same, lekin A* aam tor par kam nodes explore karta hai (heuristic guide karti hai)")
''' ))

# ============================================================
# 9. MST
# ============================================================
cells.append(md("""
## 14. Minimum Spanning Tree (MST) — Prim aur Kruskal

**Kya hai:** Connected undirected weighted graph ka aisa **spanning tree** (saare `V` vertices,
`V-1` edges, koi cycle nahi) jiska **total weight minimum** ho.

**Kyun:** "Sab shehron ko kam se kam cable/road se jorna", cluster analysis, network design,
approximation algorithms (TSP), image segmentation.

**Ahem facts:**
- MST me exactly `V-1` edges hoti hain.
- Graph disconnected ho to MST nahi banta — **Minimum Spanning Forest** banta hai.
- Weights unique hon to MST **unique** hota hai; duplicate weights par kai MST ho sakte hain
  (lekin total weight same).
- **Cut property:** kisi bhi cut ka minimum-weight edge kisi MST me hota hai.
- **Cycle property:** kisi bhi cycle ka maximum-weight edge kisi MST me **nahi** hota.

### Prim's Algorithm (vertex-based, Dijkstra jaisa)

Ek vertex se shuru karo; har baar wo **sab se sasti edge** uthao jo "tree ke andar" se "tree ke
bahar" jaati ho. Heap se `O(E log V)`.

### Kruskal's Algorithm (edge-based, DSU ke sath)

Saari edges **weight ke hisaab se sort** karo; har edge lo — agar wo cycle na banaye (yaani dono
sire mukhtalif components me hon, **Union-Find** se check) to MST me daal do.
`O(E log E)` (sorting dominate karti hai).

### Kaun sa kab

| Halat | Behtar |
|---|---|
| Sparse graph (`E ≈ V`) | Kruskal (sorting sasti) |
| Dense graph (`E ≈ V²`) | Prim (heap/array) |
| Edges already sorted / stream me | Kruskal |
| Adjacency list already maujood | Prim |
| DSU pehle se likha hua | Kruskal (code chhota) |

**Gotcha (Prim):** heap me "sab se sasti bahar jaane wali edge" rakho — aur pop karte waqt
`if v in in_mst: continue` check LAZMI, warna galat/duplicate edges aa jaayengi.

**Interview tip:** Kruskal ke sath DSU (union by rank + path compression) likh dena strong signal
hai. DSU ki poori detail NB3 me hai.
"""))

cells.append(code('''
def prim_mst(n, adj):
    """Prim's MST. adj[u] = [(v, w)]. Returns (total_weight, mst_edges)."""
    if n == 0:
        return 0, []
    in_mst = [False] * n
    total, mst = 0, []
    pq = [(0, 0, -1)]                       # (weight, node, parent)
    while pq:
        w, u, p = heapq.heappop(pq)
        if in_mst[u]:
            continue                        # ye check LAZMI hai (stale entries)
        in_mst[u] = True
        total += w
        if p != -1:
            mst.append(tuple(sorted((p, u))) + (w,))
        for v, wt in adj[u]:
            if not in_mst[v]:
                heapq.heappush(pq, (wt, v, u))
    if not all(in_mst):
        return -1, []                       # graph disconnected -> MST mumkin nahi
    return total, sorted(mst)

class DSU:
    """Union-Find with union-by-size + path compression. (NB3 me full detail.)"""
    def __init__(self, n):
        self.p = list(range(n))             # parent
        self.sz = [1] * n                   # component size
        self.count = n                      # kitne components bache hain
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]   # path halving — tree flat rehta hai
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                    # already same set => cycle banegi
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra                 # chhota bara ke neeche
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        self.count -= 1
        return True

def kruskal_mst(n, edges):
    """edges = [(u, v, w)]. Returns (total_weight, mst_edges)."""
    dsu = DSU(n)
    total, mst = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):   # weight ke hisaab se sort
        if dsu.union(u, v):                             # cycle nahi banti -> le lo
            total += w
            mst.append(tuple(sorted((u, v))) + (w,))
            if len(mst) == n - 1:
                break                                   # V-1 edges mil gayin -> done
    if len(mst) != n - 1:
        return -1, []                                   # disconnected
    return total, sorted(mst)

E_mst = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2), (2, 4, 5)]
adjM = edges_to_adj(5, E_mst, weighted=True)
pw, pe = prim_mst(5, adjM)
kw, ke = kruskal_mst(5, E_mst)
print("Prim   : weight =", pw, "edges =", pe)
print("Kruskal: weight =", kw, "edges =", ke)
assert pw == kw == 8, "dono ka total weight same hona chahiye"
assert len(pe) == len(ke) == 4                     # V-1 = 4 edges
# Disconnected graph par
assert prim_mst(4, edges_to_adj(4, [(0, 1, 1)], weighted=True))[0] == -1
assert kruskal_mst(4, [(0, 1, 1)])[0] == -1
print("MST OK — Prim aur Kruskal ka total weight hamesha barabar (MST unique na ho tab bhi)")
''' ))

# ============================================================
# 10. GRID PATTERNS
# ============================================================
cells.append(md("""
## 15. Grid Patterns — implicit graph par BFS/DFS

Grid problems interview me sab se zyada aate hain. Chaar core patterns:

| Pattern | Problem | Tareeqa |
|---|---|---|
| **Count components** | Number of Islands (LC 200) | Har unvisited land cell par DFS/BFS, counter++ |
| **Flood fill** | Flood Fill (LC 733), Surrounded Regions (LC 130) | Ek seed se poora connected region badal do |
| **Multi-source spread** | Rotting Oranges (LC 994), 01 Matrix (LC 542), Walls & Gates (LC 286) | Saare sources queue me, level = time |
| **Shortest path in maze** | LC 1091, 1293 | Plain BFS (unweighted) ya 0-1 BFS |

### Grid ke universal tips

1. **Bounds check pehle, value check baad me:** `if 0 <= nr < R and 0 <= nc < C and grid[nr][nc]==1`
   — Python me `and` short-circuits karta hai, is liye order ghalat hone par `IndexError`.
   (Warning: Python me negative index legal hai! `grid[-1]` crash nahi karega — **silent bug**.
   Isi liye `0 <= nr` check bhoolna khatarnaak hai.)
2. **Visited ke liye extra matrix banane ki zaroorat nahi** — grid ko **in-place mark** kar do
   (`grid[r][c] = 0` ya `'#'`). Ye space `O(1)` extra bacha deta hai. (Interview me poocho:
   "kya main input modify kar sakta hoon?")
3. **BFS vs DFS in grid:** DFS recursion `1000x1000` grid par stack overflow de sakti hai →
   BFS ya iterative DFS safe hai.
4. **Direction tuple** ko ek dafa define karo (`DIRS4`) — code saaf rehta hai.
5. **"Time / minimum steps" = BFS. "Region / area / count" = DFS ya BFS, dono theek.**
"""))

cells.append(code('''
def num_islands(grid):
    """LC 200 core: 1 = land, 0 = water. In-place marking (no visited matrix)."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    g = [row[:] for row in grid]              # copy (caller ka data kharab na karein)
    count = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] != 1:
                continue
            count += 1
            # iterative BFS se poora island doobo do
            q = deque([(r, c)])
            g[r][c] = 0                        # mark-on-push
            while q:
                cr, cc = q.popleft()
                for dr, dc in DIRS4:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < R and 0 <= nc < C and g[nr][nc] == 1:
                        g[nr][nc] = 0
                        q.append((nr, nc))
    return count

iso = [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1],
]
print("Islands:", num_islands(iso))
assert num_islands(iso) == 3
assert num_islands([[0, 0], [0, 0]]) == 0
assert num_islands([[1]]) == 1
print("Islands (component counting) OK")


def flood_fill(image, sr, sc, new_color):
    """LC 733: (sr,sc) se connected same-color region ko new_color kar do."""
    R, C = len(image), len(image[0])
    img = [row[:] for row in image]
    old = img[sr][sc]
    if old == new_color:
        return img                             # infinite loop se bachao — ye check LAZMI
    st = [(sr, sc)]
    img[sr][sc] = new_color
    while st:
        r, c = st.pop()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and img[nr][nc] == old:
                img[nr][nc] = new_color
                st.append((nr, nc))
    return img

img0 = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
print("Flood fill:", flood_fill(img0, 1, 1, 2))
assert flood_fill(img0, 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
assert flood_fill(img0, 1, 1, 1) == img0        # same color -> koi tabdeeli nahi, hang bhi nahi
print("Flood fill OK (same-color guard bhoolna = infinite loop)")
''' ))

cells.append(code('''
def rotting_oranges(grid):
    """LC 994: 0 empty, 1 fresh, 2 rotten. Har minute rotten apne 4 neighbours ko rot kar deta hai.
    Multi-source BFS — level = minute. -1 agar koi fresh reh jaye."""
    R, C = len(grid), len(grid[0])
    g = [row[:] for row in grid]
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] == 2:
                q.append((r, c))              # SAARE rotten ek sath level-0 sources
            elif g[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:                        # fresh khatam ho gaye to ruk jao
        for _ in range(len(q)):               # ek poora level = ek minute
            r, c = q.popleft()
            for dr, dc in DIRS4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and g[nr][nc] == 1:
                    g[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes

assert rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1    # bottom-left kabhi nahi sarega
assert rotting_oranges([[0, 2]]) == 0                              # koi fresh nahi -> 0 minute
print("Rotting oranges OK — 'while q and fresh' se off-by-one minute ka bug bachta hai")


def walls_and_gates(rooms, INF_VAL=2**31 - 1):
    """LC 286: -1 = wall, 0 = gate, INF = empty room.
    Har empty room me nearest gate ki distance bhar do. Multi-source BFS."""
    R, C = len(rooms), len(rooms[0])
    g = [row[:] for row in rooms]
    q = deque((r, c) for r in range(R) for c in range(C) if g[r][c] == 0)
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] == INF_VAL:
                g[nr][nc] = g[r][c] + 1
                q.append((nr, nc))
    return g

I = 2**31 - 1
rooms = [[I, -1, 0, I], [I, I, I, -1], [I, -1, I, -1], [0, -1, I, I]]
out = walls_and_gates(rooms)
for row in out:
    print("  ", row)
assert out == [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
print("Walls & gates OK — naive tareeqa (har room se BFS) O((RC)^2) hota, ye O(RC) hai")
''' ))

cells.append(md("""
## 16. State-Space BFS — jab "graph" diya hi na ho

**Kya hai:** Sab se powerful graph idea. Kabhi kabhi problem me koi nodes/edges nahi hote —
lekin **states** hote hain:

- **Node** = ek "state" (ek word, ek lock combination, ek board configuration, ek `(pos, mask)` pair)
- **Edge** = ek "legal move" jo ek state se doosri state par le jaye
- **Answer** = shortest number of moves ⟹ **BFS**

Misaal:
| Problem | State | Move |
|---|---|---|
| LC 127 Word Ladder | ek word | ek harf badal do |
| LC 752 Open the Lock | 4-digit string | ek wheel ±1 |
| LC 773 Sliding Puzzle | board string | blank ko swap karo |
| LC 864 Shortest Path All Keys | `(r, c, key_bitmask)` | ek qadam chalo |
| Water jug puzzle | `(jug1, jug2)` | fill/empty/pour |

**Do zaroori tricks:**

1. **State ko hashable banao** — `str`, `tuple`, ya `int` bitmask. `list` set me nahi jaa sakta.
2. **Neighbour generation smart karo.** Word Ladder me har word ko har doosre word se compare karna
   `O(N² · L)` hai. Behtar: **wildcard pattern bucket** banao (`h*t` → `[hot, hit]`) →
   `O(N · L · 26)`.
3. **Bidirectional BFS** — dono taraf (start aur end) se BFS chalao, jahan mile wahan jawab.
   Branching factor `b`, depth `d` → `O(b^d)` se `O(b^(d/2))`. Word Ladder / Open the Lock par
   dramatic speedup.
"""))

cells.append(code('''
def open_lock(deadends, target):
    """LC 752 core: '0000' se target tak, deadends ko chhoo bhi nahi sakte. Har move: ek wheel +-1."""
    dead = set(deadends)
    start = "0000"
    if start in dead:
        return -1
    if start == target:
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        s, steps = q.popleft()
        for i in range(4):                       # kaun sa wheel
            d = int(s[i])
            for nd in ((d + 1) % 10, (d - 1) % 10):   # modulo se wrap (9->0, 0->9)
                nxt = s[:i] + str(nd) + s[i + 1:]
                if nxt in seen or nxt in dead:
                    continue
                if nxt == target:
                    return steps + 1
                seen.add(nxt)                    # mark-on-push
                q.append((nxt, steps + 1))
    return -1

assert open_lock(["0201", "0101", "0102", "1212", "2002"], "0202") == 6
assert open_lock(["8888"], "0009") == 1
assert open_lock(["0000"], "8888") == -1
print("Open the Lock (state-space BFS) OK — state = 4-char string, move = wheel +-1")


def word_ladder(begin, end, word_list):
    """LC 127 core: begin -> end, har step me ek harf badle, har intermediate word list me ho.
    Wildcard bucket + bidirectional BFS."""
    words = set(word_list)
    if end not in words:
        return 0
    L = len(begin)
    # wildcard buckets: "h*t" -> ["hot", "hit"] — neighbour lookup O(L) ho jaata hai
    buckets = defaultdict(list)
    for w in words | {begin}:
        for i in range(L):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)

    def nbrs(w):
        for i in range(L):
            for x in buckets[w[:i] + "*" + w[i + 1:]]:
                if x != w:
                    yield x

    # bidirectional BFS: dono frontiers ko barhao, chhote wale ko pehle
    front, back = {begin}, {end}
    seen = {begin, end}
    steps = 1
    while front and back:
        if len(front) > len(back):
            front, back = back, front            # hamesha chhoti frontier expand karo
        nxt = set()
        for w in front:
            for x in nbrs(w):
                if x in back:
                    return steps + 1             # dono taraf mil gaye
                if x not in seen:
                    seen.add(x)
                    nxt.add(x)
        front = nxt
        steps += 1
    return 0

assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
assert word_ladder("a", "c", ["a", "b", "c"]) == 2
print("Word Ladder OK — bucket + bidirectional BFS = O(N*L*26) ke bajaye bohat kam kaam")
''' ))

# ============================================================
# 11. COMPLEXITY + DECISION GUIDE
# ============================================================
cells.append(md("""
## 17. Complexity Table (sab kuch ek jagah)

| Algorithm | Time | Space | Kaam |
|---|---|---|---|
| BFS | `O(V + E)` | `O(V)` | Unweighted shortest path, levels, multi-source |
| DFS | `O(V + E)` | `O(V)` | Components, cycles, topo, backtracking |
| 0-1 BFS (deque) | `O(V + E)` | `O(V)` | Weights sirf {0,1} |
| Connected components | `O(V + E)` | `O(V)` | Islands, provinces |
| Cycle detection | `O(V + E)` | `O(V)` | DAG validation |
| Topological sort (Kahn/DFS) | `O(V + E)` | `O(V)` | Dependency order |
| Topological sort (lexicographic) | `O((V+E) log V)` | `O(V)` | Smallest order |
| Bipartite check | `O(V + E)` | `O(V)` | 2-coloring |
| Kosaraju / Tarjan SCC | `O(V + E)` | `O(V)` | Strongly connected components |
| Bridges / Articulation points | `O(V + E)` | `O(V)` | Critical connections |
| **Dijkstra** (binary heap) | `O((V + E) log V)` | `O(V + E)` | Non-negative weights, 1 source |
| Dijkstra (array, dense) | `O(V²)` | `O(V²)` | Dense graph |
| **Bellman-Ford** | `O(V · E)` | `O(V)` | Negative weights, negative cycle |
| Bellman-Ford (k edges) | `O(k · E)` | `O(V)` | LC 787 style |
| **Floyd-Warshall** | `O(V³)` | `O(V²)` | All-pairs, `V ≤ ~400` |
| DAG shortest/longest path | `O(V + E)` | `O(V)` | DAG (negatives OK) |
| A\\* | `O(E log V)` worst | `O(V)` | Single target + good heuristic |
| **Prim** (heap) | `O(E log V)` | `O(V + E)` | MST, dense graph |
| **Kruskal** (DSU) | `O(E log E)` | `O(V + E)` | MST, sparse graph |
| Grid BFS/DFS | `O(R · C)` | `O(R · C)` | Islands, maze, spread |

## 18. "Kaun sa algorithm kab" — Decision Guide

```
Problem me kya poocha gaya hai?
│
├─ "Kya reach ho sakta hai?" / "Kitne groups?" / "Cycle hai?"
│      → BFS ya DFS  (O(V+E))
│
├─ "MINIMUM number of steps/moves" (har edge ka cost same/1)
│      → BFS. Multiple starting points? → Multi-source BFS
│      → Sirf ek target aur good heuristic? → A*
│      → Weights sirf 0 aur 1? → 0-1 BFS (deque)
│
├─ "MINIMUM total cost/distance/time" (weights mukhtalif)
│      ├─ saare weights >= 0 ......... → DIJKSTRA
│      ├─ koi weight negative ....... → BELLMAN-FORD
│      ├─ graph DAG hai ............. → TOPO ORDER DP (O(V+E), negatives OK)
│      ├─ HAR pair ka jawab chahiye, V chhota → FLOYD-WARSHALL
│      └─ "at most K edges/stops" ... → BELLMAN-FORD k passes (layer copy!)
│
├─ "Dependency order" / "kya schedule mumkin hai?"
│      → TOPOLOGICAL SORT (Kahn aasan hai). Smallest order chahiye? → heap
│
├─ "Sab ko jorne ki kam se kam cost"
│      → MST: Kruskal (sparse/edge list) ya Prim (dense/adj list)
│
├─ "Do groups me baant do" / "odd cycle hai?"
│      → BIPARTITE (2-coloring BFS)
│
├─ "Critical edge/node — hatane par network toot jaye"
│      → BRIDGES / ARTICULATION POINTS (Tarjan low-link)
│
├─ "Mutually reachable groups" (directed)
│      → SCC (Kosaraju/Tarjan) + condensation DAG
│
├─ "Kitne raaste hain?" / "sab raaste list karo"
│      → DAG par DP (counting) ya DFS backtracking (enumeration)
│
└─ Graph diya hi nahi, sirf "states aur moves"
       → STATE-SPACE BFS (state ko hashable banao) [+ bidirectional]
```

### Constraints se hint

| Constraint | Kya karna hai |
|---|---|
| `V ≤ 20` | Bitmask DP / brute force allowed (`2^V`) |
| `V ≤ 400` | `O(V³)` Floyd-Warshall theek |
| `V ≤ 1000`, dense | `O(V²)` matrix chalega |
| `V, E ≤ 10⁵` | `O(V + E)` ya `O(E log V)` lazmi. Matrix na banao (memory) |
| `V ≤ 10⁵` chain shape | Recursive DFS **nahi** — iterative karo (`RecursionError`) |
| Grid `1000 × 1000` | BFS theek (`10⁶`), recursive DFS risky |
"""))

# ============================================================
# 12. GOTCHAS
# ============================================================
cells.append(md("""
## 19. Common Mistakes / Gotchas — "yahan log phaste hain"

Ye list interview me bachaayegi. Har point asli galti hai jo log dohraate hain.
"""))

cells.append(code('''
# GOTCHA 1: mark-on-pop (pop par visited mark karna) => duplicate queue entries
def bfs_wrong(adj, src):
    """GHALAT: visited pop par mark ho raha hai."""
    q, seen, pushes = deque([src]), set(), 0
    while q:
        u = q.popleft()
        if u in seen:
            continue
        seen.add(u)                  # <-- pop par mark (der ho gayi)
        for v in adj[u]:
            q.append(v)              # koi check nahi -> duplicates
            pushes += 1
    return pushes

def bfs_right(adj, src):
    """SAHI: push par mark."""
    q, seen, pushes = deque([src]), {src}, 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)          # <-- push par mark
                q.append(v)
                pushes += 1
    return pushes

k5 = edges_to_adj(5, [(i, j) for i in range(5) for j in range(i + 1, 5)])   # complete graph K5
print("Ghalat BFS pushes:", bfs_wrong(k5, 0), " | Sahi BFS pushes:", bfs_right(k5, 0))
assert bfs_wrong(k5, 0) > bfs_right(k5, 0)
print("=> Dense graph par mark-on-pop bohat zyada kaam karta hai (bare inputs par TLE)\\n")

# GOTCHA 2: Python me negative index legal hai -> bounds check bhoolna SILENT bug deta hai
grid_g = [[1, 2], [3, 4]]
print("grid_g[-1][0] =", grid_g[-1][0], "<- crash nahi hua! (wrap around ho gaya)")
print("=> Isi liye 'if 0 <= nr < R and 0 <= nc < C' me '0 <=' hissa lazmi hai\\n")

# GOTCHA 3: directed cycle detection me sirf `visited` set = ghalat jawab
def cycle_wrong(n, adj):
    """GHALAT: sirf visited set. Diamond ko cycle keh dega."""
    seen = set()
    def go(u):
        if u in seen:
            return True              # <-- ghalat: visited hona cycle nahi hota
        seen.add(u)
        return any(go(v) for v in adj[u])
    return go(0)

diamond = edges_to_adj(4, [(0, 1), (0, 2), (1, 3), (2, 3)], directed=True)
print("Diamond (0->1->3, 0->2->3), koi cycle nahi.")
print("  Ghalat code:", cycle_wrong(4, diamond), " | Sahi code:", has_cycle_directed(4, diamond))
assert cycle_wrong(4, diamond) is True and has_cycle_directed(4, diamond) is False
print("=> Directed me gray/black (rec-stack) chahiye\\n")
''' ))

cells.append(code('''
# GOTCHA 4: mutable default argument — classic Python trap graph code me
def collect_bad(node, acc=[]):        # <-- acc list SIRF EK DAFA banti hai (function definition par)
    acc.append(node)
    return acc

print("collect_bad(1):", collect_bad(1))
print("collect_bad(2):", collect_bad(2), "<- pichla data bacha hua hai! BUG")

def collect_good(node, acc=None):
    acc = [] if acc is None else acc   # SAHI pattern
    acc.append(node)
    return acc
print("collect_good(1):", collect_good(1), "collect_good(2):", collect_good(2))
assert collect_good(1) == [1] and collect_good(2) == [2]

# GOTCHA 5: Dijkstra me stale-entry skip bhool jana
def dijkstra_no_skip(n, adj, src):
    """Skip check ke baghair — pops ki tadaad count karte hain."""
    dist = [INF] * n; dist[src] = 0
    pq = [(0, src)]; pops = 0
    while pq:
        d, u = heapq.heappop(pq); pops += 1
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist, pops

def dijkstra_with_skip(n, adj, src):
    dist = [INF] * n; dist[src] = 0
    pq = [(0, src)]; pops = 0
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        pops += 1
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist, pops

d1, p1 = dijkstra_no_skip(6, adjW, 0)
d2, p2 = dijkstra_with_skip(6, adjW, 0)
assert d1 == d2, "jawab to same aata hai..."
print(f"\\nDijkstra pops: bina skip = {p1}, skip ke sath = {p2}  (jawab same, kaam kam)")

# GOTCHA 6: defaultdict par iterate karte waqt missing key access = dict ka size badal jata hai
dd = defaultdict(list)
dd[1].append(2)
try:
    for k in dd:
        _ = dd[3]                      # <-- naya key ban gaya -> RuntimeError
except RuntimeError as e:
    print("RuntimeError:", e, "\\n=> defaultdict ko loop me touch na karo; .get(k, []) use karo")

# GOTCHA 7: graph ke nodes 1-indexed hon (LC me aksar) — size n+1 lo
n_nodes = 4
adj_1based = [[] for _ in range(n_nodes + 1)]     # index 0 waste, 1..4 use
for u, v in [(1, 2), (2, 3), (3, 4)]:
    adj_1based[u].append(v); adj_1based[v].append(u)
print("1-indexed adj:", adj_1based, "<- 'n+1' bhoolna = IndexError")
''' ))

# ============================================================
# 13. REAL WORLD
# ============================================================
cells.append(md("""
## 20. Real-World Problems

Ab wo problems jo asli software me aati hain — graph theory ki asli value yahan dikhti hai.
"""))

cells.append(code('''
# REAL-WORLD 1: Build system / package dependency resolver
# "npm install" ya "make" jo karta hai: topological sort + cycle detection
def resolve_build_order(deps: dict):
    """deps[pkg] = [wo packages jo pkg se PEHLE build hone chahiye].
    Returns (order, error_message)."""
    pkgs = sorted(set(deps) | {d for v in deps.values() for d in v})
    idx = {p: i for i, p in enumerate(pkgs)}
    n = len(pkgs)
    adj = [[] for _ in range(n)]
    for p, needs in deps.items():
        for d in needs:
            adj[idx[d]].append(idx[p])           # d -> p (d pehle)
    order, ok = topo_lexicographic(n, adj)       # deterministic order ke liye lexicographic
    if not ok:
        return [], "CIRCULAR DEPENDENCY! Build mumkin nahi."
    return [pkgs[i] for i in order], None

project = {
    "app":      ["ui", "api"],
    "ui":       ["utils"],
    "api":      ["db", "utils"],
    "db":       ["utils"],
    "utils":    [],
}
order, err = resolve_build_order(project)
print("Build order:", " -> ".join(order))
assert err is None
assert order.index("utils") < order.index("db") < order.index("api") < order.index("app")

broken = {"a": ["b"], "b": ["c"], "c": ["a"]}
_, err2 = resolve_build_order(broken)
print("Circular project:", err2)
assert err2 is not None
''' ))

cells.append(code('''
# REAL-WORLD 2: Flight route planner — sasta ticket vs kam stops
# Do mukhtalif objectives = do mukhtalif algorithms
FLIGHTS = [
    ("KHI", "LHE", 8000), ("KHI", "ISB", 12000), ("LHE", "ISB", 5000),
    ("ISB", "DXB", 40000), ("LHE", "DXB", 48000), ("DXB", "LHR", 90000),
    ("KHI", "DXB", 55000), ("ISB", "LHR", 145000),
]
cities = sorted({c for f in FLIGHTS for c in f[:2]})
ci = {c: i for i, c in enumerate(cities)}
n_c = len(cities)
adj_f = edges_to_adj(n_c, [(ci[a], ci[b], w) for a, b, w in FLIGHTS], directed=True, weighted=True)

# (a) Sab se sasta raasta -> Dijkstra
dist_f, par_f = dijkstra(n_c, adj_f, ci["KHI"])
path_f = [cities[i] for i in rebuild_path(par_f, ci["KHI"], ci["LHR"])]
print(f"Sab se sasta KHI->LHR: {' -> '.join(path_f)} = Rs {dist_f[ci['LHR']]:,}")

# (b) Kam se kam stops -> BFS (cost ignore)
adj_plain = [[v for v, _ in adj_f[u]] for u in range(n_c)]
hops = bfs_path(adj_plain, ci["KHI"], ci["LHR"])
print(f"Kam se kam flights : {' -> '.join(cities[i] for i in hops)} = {len(hops)-1} flights")

assert dist_f[ci["LHR"]] == 12000 + 40000 + 90000          # KHI-ISB-DXB-LHR = 142,000
assert len(hops) - 1 == 2                                   # KHI-DXB-LHR ya KHI-ISB-LHR
print("\\nSABAK: 'sasta' aur 'chhota' do alag problems hain — Dijkstra vs BFS")
''' ))

cells.append(code('''
# REAL-WORLD 3: Deadlock detection in a database / OS
# "Wait-for graph": T1 -> T2 ka matlab "T1, T2 ka lock chhorne ka intezar kar raha hai"
# Cycle => DEADLOCK. Rollback ke liye cycle ka koi ek transaction chuno.
def find_deadlock_cycle(txns: dict):
    """txns[t] = [wo transactions jinka t intezar kar raha hai]. Cycle return karta hai ya []."""
    color = {t: 0 for t in txns}
    stack, cycle = [], []
    def go(u):
        color[u] = 1
        stack.append(u)
        for v in txns.get(u, []):
            if color.get(v, 0) == 1:              # gray -> cycle mil gayi
                cycle.extend(stack[stack.index(v):] + [v])
                return True
            if color.get(v, 0) == 0 and go(v):
                return True
        color[u] = 2
        stack.pop()
        return False
    for t in txns:
        if color[t] == 0 and go(t):
            return cycle
    return []

waiting = {"T1": ["T2"], "T2": ["T3"], "T3": ["T1"], "T4": ["T1"]}
cyc = find_deadlock_cycle(waiting)
print("Wait-for graph:", waiting)
print("DEADLOCK cycle:", " -> ".join(cyc) if cyc else "koi deadlock nahi")
assert cyc and cyc[0] == cyc[-1] and len(cyc) == 4

safe = {"T1": ["T2"], "T2": ["T3"], "T3": [], "T4": ["T3"]}
assert find_deadlock_cycle(safe) == []
print("Safe schedule:", find_deadlock_cycle(safe) or "koi deadlock nahi")
print("=> Asli DB engine (MySQL InnoDB) exactly yehi karta hai, phir chhoti transaction rollback")
''' ))

cells.append(code('''
# REAL-WORLD 4: Social network — "kitne degree door hai?" + mutual friends + friend suggestions
NETWORK = {
    "ali": {"bilal", "chand"},
    "bilal": {"ali", "daud"},
    "chand": {"ali", "daud", "erum"},
    "daud": {"bilal", "chand", "farhan"},
    "erum": {"chand"},
    "farhan": {"daud"},
    "gul": set(),
}

def degrees_of_separation(net, a, b):
    """BFS — 'six degrees of separation' ka asli implementation."""
    if a == b:
        return 0
    dist, q = {a: 0}, deque([a])
    while q:
        u = q.popleft()
        for v in net[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                if v == b:
                    return dist[v]
                q.append(v)
    return -1                                # connected nahi

def suggest_friends(net, person, top=3):
    """Friend-of-friend jo abhi dost nahi — mutual count ke hisaab se rank."""
    mine = net[person]
    scores = defaultdict(int)
    for f in mine:
        for fof in net[f]:
            if fof != person and fof not in mine:
                scores[fof] += 1             # ek aur mutual friend
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:top]

print("ali <-> farhan:", degrees_of_separation(NETWORK, "ali", "farhan"), "degrees")
print("ali <-> gul   :", degrees_of_separation(NETWORK, "ali", "gul"), "(-1 = disconnected)")
print("ali ke liye suggestions:", suggest_friends(NETWORK, "ali"))

assert degrees_of_separation(NETWORK, "ali", "farhan") == 3     # ali-chand-daud-farhan
assert degrees_of_separation(NETWORK, "ali", "gul") == -1
assert suggest_friends(NETWORK, "ali")[0] == ("daud", 2)        # bilal aur chand dono se
print("Social graph utilities OK")
''' ))

cells.append(code('''
# REAL-WORLD 5: Network design — kam se kam cable se saare offices join karo (MST)
OFFICES = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta", "Multan"]
oi = {c: i for i, c in enumerate(OFFICES)}
# (city_a, city_b, laying cost in lakh rupees)
CABLE = [
    ("Karachi", "Lahore", 120), ("Karachi", "Quetta", 70), ("Karachi", "Multan", 90),
    ("Lahore", "Islamabad", 30), ("Lahore", "Multan", 35), ("Islamabad", "Peshawar", 20),
    ("Quetta", "Multan", 60), ("Lahore", "Peshawar", 45), ("Quetta", "Peshawar", 200),
]
edges_c = [(oi[a], oi[b], w) for a, b, w in CABLE]
total, chosen = kruskal_mst(len(OFFICES), edges_c)
print(f"Kam se kam total cost: Rs {total} lakh   ({len(chosen)} cables for {len(OFFICES)} offices)")
for u, v, w in chosen:
    print(f"   {OFFICES[u]:<11} <-> {OFFICES[v]:<11}  {w} lakh")

# Saari cables lagane ki cost se compare karo
print(f"\\nSaari {len(CABLE)} cables lagane ki cost: Rs {sum(w for _,_,w in CABLE)} lakh")
assert len(chosen) == len(OFFICES) - 1
assert total == 20 + 30 + 35 + 60 + 70        # verified minimum = 215 lakh
print(f"MST ne {sum(w for _,_,w in CABLE) - total} lakh bachaye — aur network phir bhi connected hai")

# Bonus: kaun si cable "critical" hai (bridge)? Us cable ke katne se network toot jayega
mst_adj = edges_to_adj(len(OFFICES), [(u, v) for u, v, _ in chosen])
br, _ = bridges_and_articulation(len(OFFICES), mst_adj)
print("MST ki saari edges bridges hain (tree me har edge critical):", len(br) == len(chosen))
assert len(br) == len(chosen)
''' ))

# ============================================================
# 14. LEETCODE
# ============================================================
cells.append(md("""
# 21. LeetCode Problems (Graphs)

19 problems — traversal se le kar shortest path aur MST tak. Har problem me:
short bayan → approach → complexity → code with passing asserts.

**Padhne ka tareeqa:** pehle heading + bayan padho, notebook band kar ke **khud try karo**,
phir solution dekho. Sirf solution padhne se interview me kuch nahi hota.
"""))

# ---- LC 200 ----
cells.append(md("""
### LC 200. Number of Islands — Medium

https://leetcode.com/problems/number-of-islands/

**Bayan:** `m x n` grid me `'1'` = zameen, `'0'` = paani. Islands ki tadaad ginao. Island = 4-directional
(horizontally/vertically) connected zameen ka group.

**Approach:** Ye classic **connected components on implicit grid** hai.
1. Har cell par loop chalao.
2. Jahan `'1'` mile aur wo visited na ho → **naya island mila**, counter `+1`.
3. Us cell se BFS/DFS chala kar poore island ko "doobo do" (`'0'` kar do) — taake dobara na ginein.

In-place marking se `visited` matrix ki zaroorat nahi (`O(1)` extra space, recursion/queue ke ilawa).

**Time:** `O(m · n)` — har cell max 2 dafa touch hota hai (loop + BFS).
**Space:** `O(min(m, n))` BFS queue (worst case diagonal frontier) / `O(m·n)` DFS recursion worst case.
"""))

cells.append(code('''
def numIslands(grid):
    """LC 200 — BFS, in-place marking. grid me '1'/'0' characters hote hain."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] != "1":
                continue
            count += 1                                # naya island
            q = deque([(r, c)])
            grid[r][c] = "0"                          # mark-on-push (doobo diya)
            while q:
                cr, cc = q.popleft()
                for dr, dc in DIRS4:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"
                        q.append((nr, nc))
    return count

g1 = [list("11110"), list("11010"), list("11000"), list("00000")]
g2 = [list("11000"), list("11000"), list("00100"), list("00011")]
assert numIslands(g1) == 1
assert numIslands(g2) == 3
assert numIslands([list("0")]) == 0
assert numIslands([]) == 0
assert numIslands([list("101"), list("010"), list("101")]) == 5   # checkerboard
print("LC 200 pass")
''' ))

# ---- LC 133 ----
cells.append(md("""
### LC 133. Clone Graph — Medium

https://leetcode.com/problems/clone-graph/

**Bayan:** Connected undirected graph ka reference node diya hai. Uska **deep copy** banao — naye
nodes, naye neighbour lists, lekin structure bilkul same.

**Approach:** Sab se bara challenge **cycles** hain — naive recursion infinite loop me chali jayegi.
Hal: ek **`old_node -> new_node` dict** rakho jo "visited + mapping" dono ka kaam kare.

1. `node` par aao. Agar `node` dict me hai → clone pehle se ban chuka hai, wahi return karo.
2. Warna naya node banao aur **pehle dict me daalo** (recursion se pehle! — warna cycle par loop).
3. Phir har neighbour par recurse karke `clone.neighbors` bharo.

BFS version bhi bilkul same logic se chalta hai (recursion limit se safe).

**Time:** `O(V + E)` — har node/edge ek dafa.
**Space:** `O(V)` mapping + `O(V)` recursion/queue.

**Interview tip:** "Pehle map me daalo, phir recurse karo" — ye order bataana hi asli jawab hai.
Yehi pattern LC 138 (Copy List with Random Pointer) aur deep-copy ke har sawal me chalta hai.
"""))

cells.append(code('''
class Node:
    """LeetCode ka diya hua Node — testing ke liye khud bana rahe hain."""
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node):
    """LC 133 — DFS + old->new mapping."""
    if node is None:
        return None
    old_to_new = {}
    def dfs(cur):
        if cur in old_to_new:
            return old_to_new[cur]                 # already cloned -> cycle safe
        copy = Node(cur.val)
        old_to_new[cur] = copy                     # RECURSE SE PEHLE map me daalo (ahem!)
        for nb in cur.neighbors:
            copy.neighbors.append(dfs(nb))
        return copy
    return dfs(node)

def cloneGraph_bfs(node):
    """Wahi kaam BFS se — recursion limit ka masla nahi."""
    if node is None:
        return None
    mapping = {node: Node(node.val)}
    q = deque([node])
    while q:
        cur = q.popleft()
        for nb in cur.neighbors:
            if nb not in mapping:
                mapping[nb] = Node(nb.val)
                q.append(nb)
            mapping[cur].neighbors.append(mapping[nb])
    return mapping[node]

def build_graph(adj_list):
    """1-indexed adjacency list se Node graph banao."""
    nodes = {i + 1: Node(i + 1) for i in range(len(adj_list))}
    for i, nbrs in enumerate(adj_list, start=1):
        nodes[i].neighbors = [nodes[j] for j in nbrs]
    return nodes.get(1)

def serialize(node):
    """Node graph ko adjacency list me wapis (comparison ke liye)."""
    if node is None:
        return []
    seen, q = {node.val: node}, deque([node])
    while q:
        u = q.popleft()
        for nb in u.neighbors:
            if nb.val not in seen:
                seen[nb.val] = nb
                q.append(nb)
    return [sorted(nb.val for nb in seen[v].neighbors) for v in sorted(seen)]

original = [[2, 4], [1, 3], [2, 4], [1, 3]]
root = build_graph(original)
for cloner in (cloneGraph, cloneGraph_bfs):
    cl = cloner(root)
    assert serialize(cl) == original, cloner.__name__
    assert cl is not root                    # naya object hona chahiye
    assert cl.neighbors[0] is not root.neighbors[0]   # neighbours bhi naye
assert cloneGraph(None) is None
assert serialize(cloneGraph(build_graph([[]]))) == [[]]      # single node, no edges
print("LC 133 pass (deep copy verified — koi shared object nahi)")
''' ))

# ---- LC 207 ----
cells.append(md("""
### LC 207. Course Schedule — Medium

https://leetcode.com/problems/course-schedule/

**Bayan:** `numCourses` courses (`0..n-1`) aur `prerequisites[i] = [a, b]` ka matlab
"`a` lene se pehle `b` lena parega". Kya saare courses complete kar sakte ho? (`True/False`)

**Approach:** Sawal asal me ye hai: **kya ye directed graph DAG hai (koi cycle nahi)?**
Do tareeqe:

1. **Kahn's (BFS):** in-degree 0 wale courses queue me daalo, process karte jao. Aakhir me
   `processed == numCourses` ho to DAG hai. **Ye zyada aasan aur iterative hai — yehi likho.**
2. **DFS 3-color:** GRAY node par edge mile to cycle.

**Edge direction ka trap:** `[a, b]` = "b pehle" → edge `b → a` banao. Ulta karne par bhi cycle
detection ka jawab same aata hai (cycle dono taraf cycle hoti hai), lekin LC 210 me order ghalat aayega.
Aadat sahi rakho.

**Time:** `O(V + E)` **Space:** `O(V + E)`.
"""))

cells.append(code('''
def canFinish(numCourses, prerequisites):
    """LC 207 — Kahn's algorithm (indegree BFS)."""
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for a, b in prerequisites:
        adj[b].append(a)                       # b pehle, phir a  =>  b -> a
        indeg[a] += 1
    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return done == numCourses                  # sab process hue? => DAG

def canFinish_dfs(numCourses, prerequisites):
    """Wahi kaam DFS 3-color se."""
    adj = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        adj[b].append(a)
    color = [0] * numCourses
    def go(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1 or (color[v] == 0 and go(v)):
                return True
            # color[v] == 2 => already safe, kuch nahi karna
        color[u] = 2
        return False
    return not any(color[i] == 0 and go(i) for i in range(numCourses))

for f in (canFinish, canFinish_dfs):
    assert f(2, [[1, 0]]) is True, f.__name__               # 0 phir 1 -> theek
    assert f(2, [[1, 0], [0, 1]]) is False, f.__name__      # aapas me depend -> cycle
    assert f(1, []) is True, f.__name__
    assert f(5, [[1, 0], [2, 1], [3, 2], [4, 3]]) is True, f.__name__   # chain
    assert f(3, [[0, 1], [1, 2], [2, 0]]) is False, f.__name__          # triangle cycle
print("LC 207 pass (dono tareeqe)")
''' ))

# ---- LC 210 ----
cells.append(md("""
### LC 210. Course Schedule II — Medium

https://leetcode.com/problems/course-schedule-ii/

**Bayan:** LC 207 jaisa, lekin ab **koi ek valid order** return karo. Mumkin na ho to `[]`.

**Approach:** Bilkul topological sort. Kahn's me processed nodes ko ek list me daalte jao.
Aakhir me `len(order) != numCourses` → cycle → `[]` return.

**Note:** jawab **unique nahi** hota. Grader "koi bhi valid order" accept karta hai — is liye apne
test me exact list compare mat karo, **validity check** likho (jo neeche `valid_order()` karta hai).

**Follow-up (poocha jaata hai):** *lexicographically smallest* order chahiye to `deque` ki jagah
**min-heap** → `O((V+E) log V)`.

**Time:** `O(V + E)` **Space:** `O(V + E)`.
"""))

cells.append(code('''
def findOrder(numCourses, prerequisites):
    """LC 210 — Kahn's, order collect karte hue."""
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == numCourses else []

def findOrder_smallest(numCourses, prerequisites):
    """Follow-up: lexicographically smallest valid order — heap se."""
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    h = [i for i in range(numCourses) if indeg[i] == 0]
    heapq.heapify(h)
    order = []
    while h:
        u = heapq.heappop(h)
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    return order if len(order) == numCourses else []

def valid_order(n, prereqs, order):
    """Validity checker — kyunki topo order unique nahi hota."""
    if sorted(order) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(order)}
    return all(pos[b] < pos[a] for a, b in prereqs)      # b hamesha a se pehle

P = [[1, 0], [2, 0], [3, 1], [3, 2]]
o = findOrder(4, P)
print("Koi valid order:", o)
print("Lexicographically smallest:", findOrder_smallest(4, P))
assert valid_order(4, P, o)
assert findOrder_smallest(4, P) == [0, 1, 2, 3]
assert findOrder(2, [[1, 0]]) == [0, 1]
assert findOrder(1, []) == [0]
assert findOrder(2, [[0, 1], [1, 0]]) == []               # cycle -> mumkin nahi
print("LC 210 pass")
''' ))

# ---- LC 547 ----
cells.append(md("""
### LC 547. Number of Provinces — Medium

https://leetcode.com/problems/number-of-provinces/

**Bayan:** `n x n` matrix `isConnected` jahan `isConnected[i][j] == 1` ka matlab city `i` aur `j`
directly juri hain. **Province** = directly ya indirectly juray cities ka group. Provinces ginao.

**Approach:** Ye **connected components on adjacency matrix** hai. Do hal:

1. **DFS/BFS:** har unvisited city par traversal chalao, counter `+1`. Matrix hone ki wajah se
   neighbours dekhna `O(n)` hai → total `O(n²)`.
2. **Union-Find (DSU):** har `i < j` par agar `isConnected[i][j]` ho to `union(i, j)`.
   Aakhir me `dsu.count` = provinces. Ye interview me zyada "impressive" hota hai.

**Time:** `O(n²)` (matrix padhna hi `O(n²)` hai — is se behtar mumkin nahi).
**Space:** DFS `O(n)`, DSU `O(n)`.
"""))

cells.append(code('''
def findCircleNum(isConnected):
    """LC 547 — DFS on adjacency matrix."""
    n = len(isConnected)
    seen = [False] * n
    provinces = 0
    for s in range(n):
        if seen[s]:
            continue
        provinces += 1
        st = [s]
        seen[s] = True
        while st:
            u = st.pop()
            for v in range(n):                       # matrix -> har neighbour check O(n)
                if isConnected[u][v] and not seen[v]:
                    seen[v] = True
                    st.append(v)
    return provinces

def findCircleNum_dsu(isConnected):
    """LC 547 — Union-Find version (DSU class upar define ki hui)."""
    n = len(isConnected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):                    # sirf upper triangle (symmetric matrix)
            if isConnected[i][j]:
                dsu.union(i, j)
    return dsu.count

M1 = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
M2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
for f in (findCircleNum, findCircleNum_dsu):
    assert f(M1) == 2, f.__name__
    assert f(M2) == 3, f.__name__
    assert f([[1]]) == 1, f.__name__
    assert f([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 1, f.__name__
print("LC 547 pass (DFS aur DSU dono)")
''' ))

# ---- LC 417 ----
cells.append(md("""
### LC 417. Pacific Atlantic Water Flow — Medium

https://leetcode.com/problems/pacific-atlantic-water-flow/

**Bayan:** `heights` grid. Pacific ocean top+left edges par, Atlantic bottom+right par. Paani cell se
neighbour par sirf tab bahta hai jab neighbour ki height **`<=`** current ho. Wo saare cells batao
jahan se paani **dono** oceans tak pohonch sake.

**Approach — REVERSE THINKING (ye is problem ka asli sabak hai):**

Naive: har cell se BFS kar ke dekho dono oceans tak pohonchta hai? → `O((m·n)²)`. Bohat slow.

Smart: **ulta socho.** Ocean se andar ki taraf chalo — "paani upar ki taraf kahan tak charh sakta hai".
1. Pacific edges (row 0, col 0) se DFS/BFS shuru karo, sirf **`height[next] >= height[cur]`** wale
   neighbours par jao (kyunki ulta chal rahe hain). `pac` set bharo.
2. Wahi Atlantic edges (last row, last col) se → `atl` set.
3. Jawab = `pac ∩ atl`.

**Time:** `O(m · n)` — har cell har traversal me max ek dafa.
**Space:** `O(m · n)` do sets ke liye.

**Interview tip:** "Multi-source + reverse direction" ye combo LC 130, 1020, 934 me bhi kaam aata hai.
"""))

cells.append(code('''
def pacificAtlantic(heights):
    """LC 417 — ocean se andar ki taraf (reverse) BFS, dono sets ka intersection."""
    if not heights or not heights[0]:
        return []
    R, C = len(heights), len(heights[0])

    def flow_from(starts):
        """starts se andar chalo, condition: agla cell current se OONCHA ya barabar."""
        seen = set(starts)
        q = deque(starts)
        while q:
            r, c = q.popleft()
            for dr, dc in DIRS4:
                nr, nc = r + dr, c + dc
                if (0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):   # ULTA condition
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return seen

    pacific = [(0, c) for c in range(C)] + [(r, 0) for r in range(R)]
    atlantic = [(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)]
    return sorted(flow_from(pacific) & flow_from(atlantic))

H = [[1, 2, 2, 3, 5],
     [3, 2, 3, 4, 4],
     [2, 4, 5, 3, 1],
     [6, 7, 1, 4, 5],
     [5, 1, 1, 2, 4]]
res = pacificAtlantic(H)
print("Dono oceans tak:", res)
expected = sorted([(0, 4), (1, 3), (1, 4), (2, 2), (3, 0), (3, 1), (4, 0)])
assert res == expected
assert pacificAtlantic([[1]]) == [(0, 0)]                 # 1x1: dono oceans touch karte hain
assert pacificAtlantic([[2, 1], [1, 2]]) == [(0, 0), (0, 1), (1, 0), (1, 1)]
print("LC 417 pass — 'reverse thinking' se O((mn)^2) -> O(mn)")
''' ))

# ============================================================
# LEETCODE SECTION
# ============================================================
cells.append(md("""
---

# 🎯 LeetCode Problems — Graphs

18 problems, aasan se mushkil tak. Har problem ka **bayan → approach → complexity → code + asserts**.

**Padhne ka tareeqa:** pehle bayan padho, notebook band kar ke **khud 15 minute try karo**,
phir solution dekho. Sirf solution parh lena "seekhna" nahi hai.

| # | Title | Difficulty | Core idea |
|---|---|---|---|
| 200 | Number of Islands | Medium | grid DFS/BFS flood fill |
| 130 | Surrounded Regions | Medium | border se reverse DFS |
| 417 | Pacific Atlantic Water Flow | Medium | do multi-source reverse BFS |
| 994 | Rotting Oranges | Medium | multi-source BFS levels |
| 542 | 01 Matrix | Medium | multi-source BFS |
| 1091 | Shortest Path in Binary Matrix | Medium | 8-direction BFS |
| 133 | Clone Graph | Medium | DFS/BFS + visited map |
| 547 | Number of Provinces | Medium | components (DSU/DFS) |
| 684 | Redundant Connection | Medium | union-find cycle |
| 721 | Accounts Merge | Medium | DSU on strings |
| 785 | Is Graph Bipartite? | Medium | 2-coloring BFS |
| 207 | Course Schedule | Medium | cycle detect in digraph |
| 210 | Course Schedule II | Medium | topological order |
| 802 | Find Eventual Safe States | Medium | reverse topo / colors |
| 743 | Network Delay Time | Medium | Dijkstra |
| 787 | Cheapest Flights Within K Stops | Medium | Bellman-Ford (k rounds) |
| 127 | Word Ladder | Hard | BFS on state space |
| 752 | Open the Lock | Medium | BFS on state space |
"""))

cells.append(md("""
### LC 200. Number of Islands — Medium

🔗 https://leetcode.com/problems/number-of-islands/

**Bayan:** `'1'` (zameen) aur `'0'` (paani) ka grid diya hai. Kitne **islands** hain?
Island = 4-direction se juri hui zameen ka group.

**Approach:**
1. Har cell par loop chalao. Jahan `'1'` mile aur wo visited na ho → ek naya island mila, counter `+1`.
2. Wahan se **DFS/BFS** chala kar us poore island ki saari zameen `'0'` bana do (ya visited mark karo)
   — taake dobara count na ho.
3. Grid **implicit graph** hai: node = cell, edge = 4 padosi.

**Do variants:**
- **In-place sinking** (grid modify karo) — `O(1)` extra space, magar input kharab hota hai.
- **visited set** — input safe, `O(R*C)` extra space. Interview me pooch lo kaunsa chahiye.

**Gotcha:** Recursive DFS bare grid (1000x1000 sab `'1'`) par **RecursionError** de sakta hai →
iterative stack ya BFS use karo. Ye interview me bonus point hai.

**Time:** `O(R*C)` — har cell ek dafa. **Space:** `O(R*C)` worst case (stack/queue).
"""))

cells.append(code(r'''
def numIslands(grid):
    """LC 200 — iterative DFS (stack), grid ko sink karte hue. RecursionError-safe."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    count = 0
    for i in range(R):
        for j in range(C):
            if grid[i][j] != "1":
                continue
            count += 1                       # naya island mila
            stack = [(i, j)]
            grid[i][j] = "0"                 # push karte waqt hi mark karo (duplicate se bachao)
            while stack:
                r, c = stack.pop()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"   # sink — warna stack me kai dafa aa jayega
                        stack.append((nr, nc))
    return count

g1 = [list("11110"), list("11010"), list("11000"), list("00000")]
g2 = [list("11000"), list("11000"), list("00100"), list("00011")]
assert numIslands([r[:] for r in g1]) == 1
assert numIslands([r[:] for r in g2]) == 3
assert numIslands([list("000")]) == 0
assert numIslands([]) == 0
assert numIslands([list("1")]) == 1
print("LC 200 OK — islands:", 1, 3, 0)
''' ))

cells.append(md("""
### LC 130. Surrounded Regions — Medium

🔗 https://leetcode.com/problems/surrounded-regions/

**Bayan:** `'X'` aur `'O'` ka board. Har aisa `'O'` region jo **charon taraf se `'X'` se ghira** ho,
usay `'X'` me badal do. Border ko touch karne wale `'O'` bache rehte hain.

**Approach (ULTA sochо — yehi trick hai):**
"Ghire hue" region dhoondna mushkil hai. Iske bajaye **jo ghire hue NAHI hain** unko dhoondo:

1. **Border** ke saare `'O'` se DFS/BFS chalao → jo bhi `'O'` mila usay temporary `'#'` mark karo
   (ye "safe/escape kar sakta hai" wale hain).
2. Phir poore board par loop: `'O'` bacha hua = ghira hua → `'X'`. `'#'` = safe → wapas `'O'`.

**Kyun kaam karta hai:** Region ya to border tak pohanchta hai (safe) ya nahi (ghira hua). Border se
reverse reachability check karna direct check se bohat sasta hai.

**Yehi pattern:** LC 1020 (Number of Enclaves), LC 1254 (Closed Islands) — sab border-se-reverse-flood.

**Time:** `O(R*C)`. **Space:** `O(R*C)` stack ke liye.
"""))

cells.append(code(r'''
def solve_surrounded(board):
    """LC 130 — border se reverse flood fill. Board in-place badalta hai."""
    if not board or not board[0]:
        return board
    R, C = len(board), len(board[0])

    def escape(r, c):
        """Border-connected 'O' region ko '#' mark karo (iterative)."""
        if board[r][c] != "O":
            return
        st = [(r, c)]
        board[r][c] = "#"
        while st:
            x, y = st.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < R and 0 <= ny < C and board[nx][ny] == "O":
                    board[nx][ny] = "#"
                    st.append((nx, ny))

    for i in range(R):                       # left + right columns
        escape(i, 0); escape(i, C - 1)
    for j in range(C):                       # top + bottom rows
        escape(0, j); escape(R - 1, j)

    for i in range(R):
        for j in range(C):
            if board[i][j] == "O":
                board[i][j] = "X"            # border tak nahi pohancha => ghira hua
            elif board[i][j] == "#":
                board[i][j] = "O"            # safe tha => restore
    return board

b = [list("XXXX"), list("XOOX"), list("XXOX"), list("XOXX")]
out = solve_surrounded(b)
got = ["".join(r) for r in out]
print("LC 130 result:", got)
assert got == ["XXXX", "XXXX", "XXXX", "XOXX"]
assert ["".join(r) for r in solve_surrounded([list("X")])] == ["X"]
assert ["".join(r) for r in solve_surrounded([list("OOO"), list("OOO")])] == ["OOO", "OOO"]
print("LC 130 OK — border wala 'O' (row 3) bacha, andar wale sab 'X' ho gaye")
''' ))

cells.append(md("""
### LC 417. Pacific Atlantic Water Flow — Medium

🔗 https://leetcode.com/problems/pacific-atlantic-water-flow/

**Bayan:** Heights ka grid. Paani cell se **barabar ya neechay** (`<=`) wale padosi me beh sakta hai.
Pacific = top + left border, Atlantic = bottom + right border.
Un saare cells ki list do jahan se paani **dono** samudron tak pohanch sake.

**Approach (phir reverse!):**
Har cell se aage simulate karna `O((RC)^2)` ho jayega. Iske bajaye **samudr se ulta upar** chalo:

1. Pacific border cells se multi-source DFS/BFS — sirf us padosi par jao jiski height **`>=`** current
   (yaani paani wahan se yahan aa sakta tha). Jo reach hua = `pac` set.
2. Wahi Atlantic border se → `atl` set.
3. Jawab = `pac ∩ atl`.

**Yaad rakho:** forward me condition `next <= cur`, reverse me **`next >= cur`** ho jaati hai.
Yehi ek line 90% logon ka bug hai.

**Time:** `O(R*C)`. **Space:** `O(R*C)`.
"""))

cells.append(code(r'''
def pacificAtlantic(heights):
    """LC 417 — do reverse BFS (samudr se pahar ki taraf)."""
    if not heights or not heights[0]:
        return []
    R, C = len(heights), len(heights[0])

    def reach(starts):
        seen = set(starts)
        dq = deque(starts)
        while dq:
            r, c = dq.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                # REVERSE flow: upar (ya barabar) ki taraf jao
                if (0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):
                    seen.add((nr, nc))
                    dq.append((nr, nc))
        return seen

    pac = reach([(0, c) for c in range(C)] + [(r, 0) for r in range(R)])
    atl = reach([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)])
    return sorted(pac & atl)                 # dono tak pohanchne wale

H = [[1, 2, 2, 3, 5],
     [3, 2, 3, 4, 4],
     [2, 4, 5, 3, 1],
     [6, 7, 1, 4, 5],
     [5, 1, 1, 2, 4]]
res = pacificAtlantic(H)
print("LC 417 cells:", res)
assert res == sorted([(0, 4), (1, 3), (1, 4), (2, 2), (3, 0), (3, 1), (4, 0)])
assert pacificAtlantic([[1]]) == [(0, 0)]           # single cell dono borders par hai
assert pacificAtlantic([]) == []
print("LC 417 OK — reverse me condition '>=' hoti hai, ye yaad rakho")
''' ))

cells.append(md("""
### LC 994. Rotting Oranges — Medium

🔗 https://leetcode.com/problems/rotting-oranges/

**Bayan:** `0` = khali, `1` = taza orange, `2` = sara hua. Har minute me sara hua orange apne
4 padosiyon ko sara deta hai. Kitne minute me **sab** sar jayenge? Agar koi taza bach jaye → `-1`.

**Approach — classic multi-source BFS:**
1. Saare `2` ko queue me daalo (ye "level 0" hain), `fresh` count kar lo.
2. Level-by-level BFS: har level = 1 minute. Har naye sarne wale par `fresh -= 1`.
3. Aakhir me `fresh > 0` ⟹ `-1` (wo orange kisi sare hue tak juda nahi tha), warna minutes.

**Kyun multi-source:** saare sare hue oranges **ek hi waqt** me phailte hain — BFS ko ek fake super-source
se shuru karna equivalent hai. Har source se alag BFS chalana ghalat **aur** slow hai.

**Edge cases:**
- Shuru me `fresh == 0` → jawab `0` (chahe koi `2` ho ya na ho). Bohat log yahan `-1` de dete hain.
- Grid me sirf `0` → `0`.

**Time:** `O(R*C)`. **Space:** `O(R*C)`.
"""))

cells.append(code(r'''
def orangesRotting(grid):
    """LC 994 — multi-source level BFS."""
    R, C = len(grid), len(grid[0])
    dq = deque()
    fresh = 0
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 2:
                dq.append((i, j))            # saare rotten ek hi saath = level 0
            elif grid[i][j] == 1:
                fresh += 1
    if fresh == 0:
        return 0                             # EDGE CASE: kuch sarna hi nahi hai
    minutes = 0
    while dq and fresh:
        minutes += 1                         # naya minute shuru
        for _ in range(len(dq)):             # SIRF is level ke nodes (snapshot size)
            r, c = dq.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2         # sara diya
                    fresh -= 1
                    dq.append((nr, nc))
    return minutes if fresh == 0 else -1     # bacha hua fresh => reachable nahi tha

assert orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1   # neeche-baayen wala akela hai
assert orangesRotting([[0, 2]]) == 0
assert orangesRotting([[0]]) == 0
assert orangesRotting([[1]]) == -1                                # koi rotten hi nahi
print("LC 994 OK — 4 minutes, -1, 0, 0, -1")
''' ))

cells.append(md("""
### LC 542. 01 Matrix — Medium

🔗 https://leetcode.com/problems/01-matrix/

**Bayan:** 0/1 matrix. Har cell ke liye **nazdeek tareen `0`** ka distance batao.

**Approach:** Har `1` se BFS chalana `O((RC)^2)` — bekaar. **Ulta karo:**
saare `0` ko sources bana kar **ek multi-source BFS** chalao. Jo cell jab pehli dafa visit hua,
wohi uska minimum distance hai (BFS ki guarantee).

**Alternative (DP, 2 pass):** left-top se ek pass, right-bottom se doosra pass —
`O(R*C)` time, `O(1)` extra space. Interview me multi-source BFS batao, phir "DP se bhi ho sakta hai"
kehna bonus hai.

**Time:** `O(R*C)` dono me. **Space:** BFS `O(R*C)`, DP `O(1)` extra.
"""))

cells.append(code(r'''
def updateMatrix(mat):
    """LC 542 — multi-source BFS: saare 0 ek saath sources."""
    R, C = len(mat), len(mat[0])
    dist = [[-1] * C for _ in range(R)]
    dq = deque()
    for i in range(R):
        for j in range(C):
            if mat[i][j] == 0:
                dist[i][j] = 0
                dq.append((i, j))            # sab zeros level 0 par
    while dq:
        r, c = dq.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                dq.append((nr, nc))
    return dist

def updateMatrix_dp(mat):
    """Wahi jawab, 2-pass DP se — O(1) extra space (jawab usi array me)."""
    R, C = len(mat), len(mat[0])
    BIG = 10**9
    d = [[0 if v == 0 else BIG for v in row] for row in mat]
    for i in range(R):                       # pass 1: upar + baayen se
        for j in range(C):
            if i: d[i][j] = min(d[i][j], d[i-1][j] + 1)
            if j: d[i][j] = min(d[i][j], d[i][j-1] + 1)
    for i in range(R - 1, -1, -1):           # pass 2: neeche + daayen se
        for j in range(C - 1, -1, -1):
            if i + 1 < R: d[i][j] = min(d[i][j], d[i+1][j] + 1)
            if j + 1 < C: d[i][j] = min(d[i][j], d[i][j+1] + 1)
    return d

M = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
print("LC 542 BFS:", updateMatrix(M))
assert updateMatrix(M) == [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
assert updateMatrix(M) == updateMatrix_dp(M), "BFS aur DP ka jawab same hona chahiye"
assert updateMatrix([[0, 1, 1]]) == [[0, 1, 2]]
print("LC 542 OK — BFS == DP ✔")
''' ))

cells.append(md("""
### LC 1091. Shortest Path in Binary Matrix — Medium

🔗 https://leetcode.com/problems/shortest-path-in-binary-matrix/

**Bayan:** `n x n` binary grid. `(0,0)` se `(n-1,n-1)` tak **8-direction** clear path (saare cells `0`)
ki sab se chhoti **length** (cells ki ginti) batao, warna `-1`.

**Approach:** Unweighted shortest path ⟹ **BFS**. Sirf 2 baatein khaas:
1. **8 directions** (diagonals bhi) — `DIRS8`.
2. Start aur end dono `0` hone chahiye, warna foran `-1`.
3. Jawab **cells ki ginti** hai (edges nahi) → start ka distance `1` rakho, `0` nahi.

**Gotcha:** `1x1` grid `[[0]]` ka jawab `1` hai. Aur mark karte waqt **enqueue par** karo,
dequeue par nahi — warna same cell kai dafa queue me aa jayega (TLE).

**Time:** `O(n²)`. **Space:** `O(n²)`.
"""))

cells.append(code(r'''
def shortestPathBinaryMatrix(grid):
    """LC 1091 — 8-direction BFS, distance = cells ki ginti."""
    n = len(grid)
    if grid[0][0] or grid[n-1][n-1]:
        return -1                            # shuru ya aakhir blocked
    dq = deque([(0, 0, 1)])                  # (r, c, cells_so_far) — start = 1
    grid[0][0] = 1                           # visited mark (grid ko reuse kiya)
    while dq:
        r, c, d = dq.popleft()
        if r == n - 1 and c == n - 1:
            return d                         # BFS => pehla hit hi shortest
        for dr, dc in DIRS8:                 # 8 padosi (diagonal allowed)
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1             # ENQUEUE par mark — duplicate se bachao
                dq.append((nr, nc, d + 1))
    return -1

assert shortestPathBinaryMatrix([[0, 1], [1, 0]]) == 2          # diagonal se
assert shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
assert shortestPathBinaryMatrix([[1, 0, 0], [1, 1, 0], [1, 1, 0]]) == -1
assert shortestPathBinaryMatrix([[0]]) == 1                     # EDGE CASE
print("LC 1091 OK — 2, 4, -1, 1")
''' ))

# ---- LC 994 ----
cells.append(md("""
### LC 994. Rotting Oranges — Medium

https://leetcode.com/problems/rotting-oranges/

**Bayan:** Grid me `0` = khaali, `1` = taza orange, `2` = sara hua. Har minute me har sara hua orange
apne 4 neighbours ko sara deta hai. Kitne minute me saare oranges sar jayenge? Koi taza reh jaye to `-1`.

**Approach:** **Multi-source BFS jahan level = time.**
1. Saare `2` cells ek sath queue me daalo (level 0), aur `fresh` count karo.
2. Level-by-level BFS: har poora level = **1 minute**. `len(q)` ka trick use karo.
3. `fresh == 0` par ruk jao; loop khatam hone par `fresh > 0` ho to `-1`.

**Ahem gotcha (off-by-one):** loop ki condition `while q and fresh` rakho.
Agar sirf `while q` likho to aakhri level ke baad ek extra minute count ho jayega
(aakhri level ke oranges kisi ko nahi saraate). Aur agar shuru me hi koi fresh na ho → `0`.

**Time:** `O(m · n)` **Space:** `O(m · n)` queue.
"""))

cells.append(code('''
def orangesRotting(grid):
    """LC 994 — multi-source BFS, level = minute."""
    R, C = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r, c))                # saare rotten = level 0 sources
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:                          # 'and fresh' se off-by-one bachta hai
        for _ in range(len(q)):                 # ek poora level = 1 minute
            r, c = q.popleft()
            for dr, dc in DIRS4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes

assert orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert orangesRotting([[0, 2]]) == 0                # koi fresh nahi -> 0 minute
assert orangesRotting([[0]]) == 0                   # khaali grid
assert orangesRotting([[1]]) == -1                  # taza hai lekin koi rotten nahi
assert orangesRotting([[2, 1, 1, 1, 1]]) == 4
print("LC 994 pass")
''' ))

# ---- LC 542 ----
cells.append(md("""
### LC 542. 01 Matrix — Medium

https://leetcode.com/problems/01-matrix/

**Bayan:** Binary matrix diya hai. Har cell ke liye sab se qareeb `0` ki distance (4-directional) batao.

**Approach:** Ye **LC 994 ka bhai** hai — bas sources `0` cells hain.
1. Saare `0` cells queue me (distance 0), unhein `dist = 0` do.
2. Baqi ko `-1` (unvisited) mark karo.
3. BFS: `dist[neighbour] = dist[cur] + 1`.

**Naive:** har `1` se BFS chalao → `O((m·n)²)`. **Multi-source ek hi pass me `O(m·n)`.**

**Alternative — 2-pass DP (`O(1)` extra space):**
- Pass 1: top-left se bottom-right → `dp[r][c] = min(dp[r][c], dp[r-1][c]+1, dp[r][c-1]+1)`
- Pass 2: bottom-right se top-left → `dp[r][c] = min(dp[r][c], dp[r+1][c]+1, dp[r][c+1]+1)`

Dono passes se chaar directions cover ho jaati hain. Interview me ye alternative bataana strong signal hai.

**Time:** `O(m · n)` dono tareeqe. **Space:** BFS `O(m·n)`, DP `O(1)` extra.
"""))

cells.append(code('''
def updateMatrix(mat):
    """LC 542 — multi-source BFS."""
    R, C = len(mat), len(mat[0])
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if mat[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))               # saare 0 -> sources
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist

def updateMatrix_dp(mat):
    """LC 542 — 2-pass DP version (O(1) extra space)."""
    R, C = len(mat), len(mat[0])
    BIG = 10 ** 9
    dp = [[0 if mat[r][c] == 0 else BIG for c in range(C)] for r in range(R)]
    for r in range(R):                          # pass 1: upar-baayein se
        for c in range(C):
            if r > 0:
                dp[r][c] = min(dp[r][c], dp[r - 1][c] + 1)
            if c > 0:
                dp[r][c] = min(dp[r][c], dp[r][c - 1] + 1)
    for r in range(R - 1, -1, -1):              # pass 2: neeche-daayein se
        for c in range(C - 1, -1, -1):
            if r + 1 < R:
                dp[r][c] = min(dp[r][c], dp[r + 1][c] + 1)
            if c + 1 < C:
                dp[r][c] = min(dp[r][c], dp[r][c + 1] + 1)
    return dp

m1 = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
m2 = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
for f in (updateMatrix, updateMatrix_dp):
    assert f([r[:] for r in m1]) == [[0, 0, 0], [0, 1, 0], [0, 0, 0]], f.__name__
    assert f([r[:] for r in m2]) == [[0, 0, 0], [0, 1, 0], [1, 2, 1]], f.__name__
    assert f([[0]]) == [[0]], f.__name__
    assert f([[0, 1, 1, 1, 1]]) == [[0, 1, 2, 3, 4]], f.__name__
print("LC 542 pass (BFS aur 2-pass DP dono ka jawab same)")
''' ))

# ---- LC 127 ----
cells.append(md("""
### LC 127. Word Ladder — Hard

https://leetcode.com/problems/word-ladder/

**Bayan:** `beginWord`, `endWord`, aur `wordList`. Har transformation me **exactly ek harf** badal
sakte ho, aur har intermediate word `wordList` me hona chahiye. Sab se chhoti sequence ki **length**
batao (words ki tadaad, moves nahi). Mumkin na ho to `0`.

**Approach:** **State-space BFS.** State = ek word, edge = ek harf ka farq.

Teen levels ki optimization:
1. **Naive neighbours:** har word ko har doosre word se compare → `O(N² · L)`. Bara N par slow.
2. **Wildcard buckets:** `hot` → patterns `*ot`, `h*t`, `ho*`. Same bucket wale words neighbours hain.
   Build `O(N · L)`, lookup `O(L)`.
3. **Bidirectional BFS:** dono taraf (begin aur end) se BFS chalao, hamesha **chhoti frontier**
   expand karo. Branching `b`, depth `d` → `O(b^d)` se `O(2·b^(d/2))`. Ye Hard ko Medium bana deta hai.

**Edge cases:** `endWord` list me na ho → foran `0`. `beginWord` list me hona zaroori **nahi**.

**Time:** `O(N · L²)` bucket version se (`L` = word length, har word ke `L` patterns, har pattern `L` chars).
**Space:** `O(N · L²)` buckets ke liye.
"""))

cells.append(code('''
def ladderLength(beginWord, endWord, wordList):
    """LC 127 — wildcard buckets + bidirectional BFS."""
    words = set(wordList)
    if endWord not in words:
        return 0                                    # end reachable hi nahi
    if beginWord == endWord:
        return 1
    L = len(beginWord)
    buckets = defaultdict(set)
    for w in words | {beginWord}:
        for i in range(L):
            buckets[w[:i] + "*" + w[i + 1:]].add(w)

    def nbrs(w):
        for i in range(L):
            for x in buckets[w[:i] + "*" + w[i + 1:]]:
                if x != w:
                    yield x

    front, back = {beginWord}, {endWord}
    seen = {beginWord, endWord}
    length = 1
    while front and back:
        if len(front) > len(back):
            front, back = back, front               # hamesha chhoti side expand karo
        nxt = set()
        for w in front:
            for x in nbrs(w):
                if x in back:
                    return length + 1               # dono frontiers mil gaye
                if x not in seen:
                    seen.add(x)
                    nxt.add(x)
        front = nxt
        length += 1
    return 0

def ladderLength_simple(beginWord, endWord, wordList):
    """Simple one-directional BFS — samajhne ke liye (26 * L neighbour generation)."""
    words = set(wordList)
    if endWord not in words:
        return 0
    q = deque([(beginWord, 1)])
    seen = {beginWord}
    while q:
        w, d = q.popleft()
        if w == endWord:
            return d
        for i in range(len(w)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nxt = w[:i] + ch + w[i + 1:]
                if nxt in words and nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, d + 1))
    return 0

WL = ["hot", "dot", "dog", "lot", "log", "cog"]
for f in (ladderLength, ladderLength_simple):
    assert f("hit", "cog", WL) == 5, f.__name__          # hit->hot->dot->dog->cog
    assert f("hit", "cog", WL[:-1]) == 0, f.__name__     # cog list me nahi
    assert f("a", "c", ["a", "b", "c"]) == 2, f.__name__
    assert f("hot", "dog", ["hot", "dog"]) == 0, f.__name__   # 'hot'->'dog' me 2 harf farq
print("LC 127 pass (bidirectional aur simple BFS dono)")
''' ))

# ---- LC 752 ----
cells.append(md("""
### LC 752. Open the Lock — Medium

https://leetcode.com/problems/open-the-lock/

**Bayan:** 4 wheels wala lock, har wheel `0-9` (circular: `9` ke baad `0`). Shuru me `"0000"`.
Ek move = ek wheel ko ek qadam ghumana. `deadends` par pohonchte hi lock jam ho jaata hai.
`target` tak minimum moves batao, mumkin na ho to `-1`.

**Approach:** State-space BFS. State = 4-char string (10,000 mumkin states).
- Neighbours: har `i` (4 wheels) × 2 directions = **8 neighbours** per state.
- `(d + 1) % 10` aur `(d - 1) % 10` — modulo se circular wrap khud handle ho jaata hai.
- `deadends` ko `set` banao (`in` check `O(1)`), aur `visited` me pehle se daal do — ya check karo.

**Edge cases (yahan log phaste hain):**
- `"0000"` khud deadend ho → `-1` (BFS shuru hi nahi ho sakta)
- `target == "0000"` → `0`

**Time:** `O(10⁴ · 8 · 4)` = states × neighbours × string ops → practically constant, `O(N·A^N)` general.
**Space:** `O(10⁴)`.

**Optimization:** bidirectional BFS yahan bhi ~2x tez hai (branching factor 8, depth ~14).
"""))

cells.append(code('''
def openLock(deadends, target):
    """LC 752 — BFS on 4-digit state space."""
    dead = set(deadends)
    if "0000" in dead:
        return -1                                # shuruaat hi band
    if target == "0000":
        return 0
    seen = {"0000"}
    q = deque([("0000", 0)])
    while q:
        s, steps = q.popleft()
        for i in range(4):                       # kaun sa wheel ghumana hai
            d = int(s[i])
            for nd in ((d + 1) % 10, (d - 1) % 10):    # circular wrap
                nxt = s[:i] + str(nd) + s[i + 1:]
                if nxt in seen or nxt in dead:
                    continue
                if nxt == target:
                    return steps + 1
                seen.add(nxt)                    # mark-on-push
                q.append((nxt, steps + 1))
    return -1

assert openLock(["0201", "0101", "0102", "1212", "2002"], "0202") == 6
assert openLock(["8888"], "0009") == 1
assert openLock(["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888") == -1
assert openLock(["0000"], "8888") == -1          # start deadend
assert openLock([], "0000") == 0                 # already open
assert openLock([], "1111") == 4                 # 4 wheels, ek ek qadam
print("LC 752 pass")
''' ))

# ---- LC 743 ----
cells.append(md("""
### LC 743. Network Delay Time — Medium

https://leetcode.com/problems/network-delay-time/

**Bayan:** `n` nodes (1-indexed), `times[i] = [u, v, w]` = `u` se `v` tak signal `w` waqt me jaata hai.
Node `k` se signal bhejo — **saare** nodes tak pohonchne me kitna waqt lagega? Koi node reachable
na ho to `-1`.

**Approach:** Ye Dijkstra ka **seedha** application hai. Jawab = `max(dist)`.

Kyun max? Kyunki signal parallel me phailta hai — jo node sab se der me milta hai, wahi total waqt hai.

**Steps:**
1. Adjacency list banao (1-indexed! `n+1` size lo).
2. `k` se Dijkstra.
3. `max(dist[1..n])`. Koi `INF` ho → `-1`.

**Time:** `O(E log V)` **Space:** `O(V + E)`.

**Note:** weights positive hain (`1 <= w <= 100`) → Dijkstra safe. Bellman-Ford bhi chalega
(`O(V·E)`, slow), aur `n <= 100` hone ki wajah se Floyd-Warshall (`O(n³) = 10⁶`) bhi accept ho jayega.
"""))

cells.append(code('''
def networkDelayTime(times, n, k):
    """LC 743 — Dijkstra, jawab = max distance."""
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))                    # DIRECTED
    dist = {k: 0}
    pq = [(0, k)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, INF):
            continue                             # stale
        for v, w in adj[u]:
            if d + w < dist.get(v, INF):
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    if len(dist) != n:
        return -1                                # koi node reach nahi hua
    return max(dist.values())

assert networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
assert networkDelayTime([[1, 2, 1]], 2, 1) == 1
assert networkDelayTime([[1, 2, 1]], 2, 2) == -1     # 2 se 1 tak koi edge nahi
assert networkDelayTime([], 1, 1) == 0               # single node
assert networkDelayTime([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1) == 3   # 1->2->3 = 3 < direct 4
print("LC 743 pass — 'sab tak pohonchne ka waqt' = max(shortest distances)")
''' ))

# ---- LC 787 ----
cells.append(md("""
### LC 787. Cheapest Flights Within K Stops — Medium

https://leetcode.com/problems/cheapest-flights-within-k-stops/

**Bayan:** `n` cities, `flights[i] = [from, to, price]`. `src` se `dst` tak sab se sasta ticket batao
**lekin at most `k` stops** (yaani **`k+1` flights**) ke sath. Mumkin na ho to `-1`.

**Approach:** Ye "constrained shortest path" hai — plain Dijkstra **kaafi nahi** (Dijkstra sirf cost
minimize karta hai, hops ki fikar nahi karta; sasta raasta zyada hops le sakta hai).

**Behtareen hal — Bellman-Ford ke `k+1` passes:**
```
for i in range(k+1):            # at most k+1 edges
    nd = dist.copy()            # <-- LAYER COPY: ye line asli jaadu hai
    for u, v, w in flights:
        if dist[u] + w < nd[v]: nd[v] = dist[u] + w
    dist = nd
```

**`dist.copy()` kyun LAZMI hai?** Agar same array par update karte rahe to ek hi pass me
`src → a → b` do hops ho jaayenge (kyunki `a` ki nayi value usi pass me use ho jayegi) —
aur hop limit toot jayegi. Copy se har pass **exactly ek extra edge** allow karta hai.

**Alternative:** Dijkstra with state `(cost, node, stops)` — lekin `visited` ki jagah
`best_stops[node]` track karna parta hai (ek node par kam cost/zyada stops **aur** zyada cost/kam stops
dono useful ho sakte hain).

**Time:** `O(k · E)` **Space:** `O(n)`.
"""))

cells.append(code('''
def findCheapestPrice(n, flights, src, dst, k):
    """LC 787 — Bellman-Ford with k+1 relaxation rounds (layer copy)."""
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):                        # at most k stops = k+1 flights
        nd = dist[:]                              # LAYER COPY — bina iske hop limit toot jayegi
        for u, v, w in flights:
            if dist[u] != INF and dist[u] + w < nd[v]:
                nd[v] = dist[u] + w
        if nd == dist:
            break                                 # kuch nahi badla -> aage bhi nahi badlega
        dist = nd
    return -1 if dist[dst] == INF else dist[dst]

def findCheapestPrice_dijkstra(n, flights, src, dst, k):
    """Wahi kaam modified Dijkstra se — state (cost, node, stops_used)."""
    adj = defaultdict(list)
    for u, v, w in flights:
        adj[u].append((v, w))
    best_stops = [INF] * n                        # kisi node par ab tak ka SAB SE KAM stops
    pq = [(0, src, 0)]
    while pq:
        cost, u, stops = heapq.heappop(pq)
        if u == dst:
            return cost                           # heap se pehla pop = sab se sasta valid
        if stops > k or stops >= best_stops[u]:
            continue                              # ya limit paar, ya isse behtar (kam stops) mil chuka
        best_stops[u] = stops
        for v, w in adj[u]:
            heapq.heappush(pq, (cost + w, v, stops + 1))
    return -1

F1 = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
F2 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
for f in (findCheapestPrice, findCheapestPrice_dijkstra):
    assert f(4, F1, 0, 3, 1) == 700, f.__name__      # 0->1->3 (1 stop)
    assert f(3, F2, 0, 2, 1) == 200, f.__name__      # 0->1->2 (1 stop, sasta)
    assert f(3, F2, 0, 2, 0) == 500, f.__name__      # 0 stops -> majboori me direct
    assert f(2, [], 0, 1, 5) == -1, f.__name__       # koi flight nahi
    assert f(2, [[0, 1, 10]], 0, 0, 0) == 0, f.__name__   # src == dst
print("LC 787 pass — 'dist.copy()' bhoolna is problem ka #1 bug hai")
''' ))

# ---- LC 684 ----
cells.append(md("""
### LC 684. Redundant Connection — Medium

https://leetcode.com/problems/redundant-connection/

**Bayan:** Ek tree (n nodes, n-1 edges) me ek **extra** edge add kar di gayi — ab `n` edges hain aur
exactly ek cycle ban gayi. Wo edge return karo jise hataane se dobara tree ban jaye. Kai jawab hon
to **input me sab se aakhir wala** return karo.

**Approach — Union-Find (perfect fit):**

Edges ko **order me** process karo. Har edge `(u, v)` par:
- `find(u) != find(v)` → alag components the → `union` kar do (ye edge tree ka hissa hai)
- `find(u) == find(v)` → **pehle se connected the** → ye edge cycle banati hai → **yahi jawab hai**

Kyunki hum order me chal rahe hain, jo pehli aisi edge milegi wo "aakhri added" wali hi hogi
(problem guarantee karta hai ke sirf ek cycle hai).

**Alternative (DFS):** har edge add karne se pehle DFS se check karo ke `u` se `v` tak raasta hai —
`O(n²)`. DSU `O(n · α(n)) ≈ O(n)` hai.

**Time:** `O(n · α(n))` ≈ `O(n)` **Space:** `O(n)`.
"""))

cells.append(code('''
def findRedundantConnection(edges):
    """LC 684 — DSU. Pehli edge jo do already-connected nodes ko jorti hai."""
    n = len(edges)
    dsu = DSU(n + 1)                              # nodes 1-indexed -> n+1 size
    for u, v in edges:
        if not dsu.union(u, v):                   # union False = already same set = cycle
            return [u, v]
    return []

def findRedundantConnection_dfs(edges):
    """DFS version — har edge se pehle 'path already hai?' check."""
    adj = defaultdict(set)
    for u, v in edges:
        # kya u se v tak pehle se raasta hai? (is edge ko add karne se pehle)
        seen, st = {u}, [u]
        found = False
        while st and not found:
            x = st.pop()
            if x == v:
                found = True
                break
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        if found:
            return [u, v]
        adj[u].add(v)
        adj[v].add(u)
    return []

for f in (findRedundantConnection, findRedundantConnection_dfs):
    assert f([[1, 2], [1, 3], [2, 3]]) == [2, 3], f.__name__
    assert f([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4], f.__name__
    assert f([[1, 2], [2, 1]]) == [2, 1], f.__name__          # parallel edge
print("LC 684 pass — DSU ka textbook use case")
''' ))

# ---- LC 721 ----
cells.append(md("""
### LC 721. Accounts Merge — Medium

https://leetcode.com/problems/accounts-merge/

**Bayan:** `accounts[i] = [name, email1, email2, ...]`. Do accounts **same person** ke hain agar
unme **koi ek email common** ho (naam same hona kaafi nahi — do mukhtalif log ka naam same ho sakta hai).
Merge kar ke return karo: `[name, ...sorted unique emails]`.

**Approach — Union-Find on emails:**

1. Har email ko ek "node" samjho. Ek account ke **saare emails ko aapas me union** kar do
   (pehle email ko representative bana lo).
2. `email -> name` map bhi bana lo (naam kisi bhi email se mil jayega).
3. Aakhir me `find(email)` ke hisaab se emails ko group karo.
4. Har group: `[name] + sorted(emails)`.

**DFS alternative:** emails ka graph banao (ek account ke emails aapas me connected), phir connected
components nikaalo. Bilkul same complexity, lekin DSU zyada saaf hai.

**Gotcha:** `name` ko union me shamil **na** karo — sirf emails. Warna do different log jinke naam
same hain merge ho jaayenge.

**Time:** `O(N · L · α + N·L·log(N·L))` — sorting dominate karti hai (`N·L` = total emails).
**Space:** `O(N · L)`.
"""))

cells.append(code('''
def accountsMerge(accounts):
    """LC 721 — DSU on email strings (dict-based parent)."""
    parent = {}
    owner = {}                                    # email -> name

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]         # path halving
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for acc in accounts:
        name, emails = acc[0], acc[1:]
        if not emails:
            continue
        first = emails[0]
        find(first)
        for e in emails:
            owner[e] = name                       # naam sirf lookup ke liye, union me NAHI
            union(first, e)                       # ek account ke saare emails ek group

    groups = defaultdict(list)
    for e in owner:
        groups[find(e)].append(e)

    return sorted([owner[root]] + sorted(es) for root, es in groups.items())

A = [["John", "johnsmith@mail.com", "john_newyork@mail.com"],
     ["John", "johnsmith@mail.com", "john00@mail.com"],
     ["Mary", "mary@mail.com"],
     ["John", "johnnybravo@mail.com"]]
res = accountsMerge(A)
for r in res:
    print("  ", r)
expected = sorted([
    ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
    ["John", "johnnybravo@mail.com"],
    ["Mary", "mary@mail.com"],
])
assert res == expected
# Same naam lekin koi common email nahi -> merge NAHI hona chahiye
B = [["Alex", "a@x.com"], ["Alex", "b@x.com"]]
assert accountsMerge(B) == [["Alex", "a@x.com"], ["Alex", "b@x.com"]]
print("LC 721 pass — naam same hona merge ki wajah NAHI hai")
''' ))

# ---- LC 802 ----
cells.append(md("""
### LC 802. Find Eventual Safe States — Medium

https://leetcode.com/problems/find-eventual-safe-states/

**Bayan:** Directed graph. Node **safe** hai agar us se shuru kar ke **har** mumkin raasta kisi
terminal node (out-degree 0) par khatam ho — yaani kabhi cycle me na phanse. Saare safe nodes sorted
return karo.

**Approach 1 — DFS 3-color (seedha):**
- Node safe hai ⟺ uske **saare** outgoing neighbours safe hain.
- GRAY node par pohonch gaye → cycle → **unsafe**.
- Terminal node (no neighbours) → trivially safe.

**Approach 2 — Reverse graph + Kahn (zyada elegant):**
- Graph **reverse** karo, aur original ka **out-degree** ko indegree ki tarah use karo.
- `out_degree == 0` wale nodes queue me (terminal = safe).
- Pop karo, reverse edges ke through predecessors ka out-degree `-1` karo; `0` ho jaye to wo bhi safe.
- Ye "peeling from the leaves" hai — jo bache wo cycle ya cycle-tak-pohonchne wale hain.

**Time:** `O(V + E)` dono. **Space:** `O(V + E)`.

**Interview tip:** Ye "reverse topological peeling" pattern LC 210, 310 (Min Height Trees), 2115 me
bhi milta hai — seekh lo.
"""))

cells.append(code('''
def eventualSafeNodes(graph):
    """LC 802 — DFS 3-color. color: 0 unknown, 1 in-progress(gray), 2 safe, 3 unsafe."""
    n = len(graph)
    color = [0] * n
    def safe(u):
        if color[u] in (2, 3):
            return color[u] == 2                  # memoized
        color[u] = 1                              # gray: is raaste par hain
        for v in graph[u]:
            if color[v] == 1 or not safe(v):      # gray mila (cycle) ya child unsafe
                color[u] = 3
                return False
        color[u] = 2
        return True
    return [u for u in range(n) if safe(u)]

def eventualSafeNodes_kahn(graph):
    """LC 802 — reverse graph + Kahn on out-degree (leaves se peel karo)."""
    n = len(graph)
    rev = [[] for _ in range(n)]
    outdeg = [0] * n
    for u in range(n):
        outdeg[u] = len(graph[u])
        for v in graph[u]:
            rev[v].append(u)                      # reverse edge
    q = deque(u for u in range(n) if outdeg[u] == 0)   # terminal nodes = safe
    safe_set = set(q)
    while q:
        u = q.popleft()
        for p in rev[u]:                          # p -> u tha
            outdeg[p] -= 1
            if outdeg[p] == 0:                    # p ke SAARE raaste safe nodes par jaate hain
                safe_set.add(p)
                q.append(p)
    return sorted(safe_set)

G1 = [[1, 2], [2, 3], [5], [0], [5], [], []]
G2 = [[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]
for f in (eventualSafeNodes, eventualSafeNodes_kahn):
    assert f(G1) == [2, 4, 5, 6], f.__name__
    assert f(G2) == [4], f.__name__
    assert f([[]]) == [0], f.__name__                     # akela terminal node
    assert f([[1], [0]]) == [], f.__name__                # 2-cycle -> koi safe nahi
print("LC 802 pass (DFS aur reverse-Kahn dono)")
''' ))

# ---- LC 785 ----
cells.append(md("""
### LC 785. Is Graph Bipartite? — Medium

https://leetcode.com/problems/is-graph-bipartite/

**Bayan:** Undirected graph (adjacency list). Kya vertices ko do sets `A` aur `B` me baant sakte ho
aisay ke **har edge ka ek sira `A` me aur doosra `B` me** ho?

**Approach:** **2-coloring** BFS/DFS.
1. Har uncolored node par shuru karo (**graph disconnected ho sakta hai — ye is problem ka trap hai**).
2. Source ko rang `0`, uske neighbours ko `1`, unke ko `0`...
3. Kabhi bhi neighbour ka rang **current jaisa** mila → `False`.

**Theorem:** bipartite ⟺ koi **odd-length cycle** nahi.

**Time:** `O(V + E)` **Space:** `O(V)`.

**Union-Find se bhi ho sakta hai:** har node `u` ke saare neighbours ko aapas me union karo;
agar `find(u) == find(neighbour)` ho jaye → not bipartite.
"""))

cells.append(code('''
def isBipartite(graph):
    """LC 785 — BFS 2-coloring, disconnected components handle karta hai."""
    n = len(graph)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue                              # already colored (kisi aur component me)
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]       # ulta rang
                    q.append(v)
                elif color[v] == color[u]:
                    return False                  # same rang wali edge => odd cycle
    return True

def isBipartite_dsu(graph):
    """DSU version: node ke saare neighbours ek hi set me hone chahiye, aur node unse alag."""
    n = len(graph)
    dsu = DSU(n)
    for u in range(n):
        for v in graph[u]:
            if dsu.find(u) == dsu.find(v):
                return False                      # u aur v ek hi side par aa gaye
            dsu.union(graph[u][0], v)             # u ke saare neighbours ek side
    return True

for f in (isBipartite, isBipartite_dsu):
    assert f([[1, 3], [0, 2], [1, 3], [0, 2]]) is True, f.__name__     # C4
    assert f([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]) is False, f.__name__
    assert f([[]]) is True, f.__name__                                  # single node
    assert f([[1], [0], [3], [2]]) is True, f.__name__                  # 2 disconnected edges
    assert f([[1, 2], [0, 2], [0, 1]]) is False, f.__name__             # triangle
print("LC 785 pass — disconnected components ka loop bhoolna #1 bug hai")
''' ))

# @@APPEND@@

save(r"DSA in Python/Advance/01_Graphs_Traversals_ShortestPaths_aur_MST.ipynb", cells)
