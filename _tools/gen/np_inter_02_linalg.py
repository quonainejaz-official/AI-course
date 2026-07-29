"""Generator: Numpy/Intermediate/02_LinearAlgebra_Random_aur_Statistics.ipynb
NOTE: code cells ke andar triple-quote docstring MAT likho (outer r-string toot jata hai).
"""
import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

CELLS = []
def M(s): CELLS.append(md(s))
def C(s): CELLS.append(code(s))

M(r"""
# NumPy Intermediate 02 — Linear Algebra, Random aur Statistics

**Level:** Intermediate → Advanced
**Prerequisites:** NB01 (axis mastery), broadcasting ka basic idea, school ka matrix concept

Machine learning asal me **linear algebra + probability** hai. Neural network ka forward
pass ek `X @ W + b` hai. PCA ek SVD hai. Regression ek `solve(A, b)` hai.
Is notebook me hum ye poora toolbox NumPy me seekhenge — theory rattne ke liye nahi,
**code me use karne** ke liye.

## Is notebook me kya seekhenge

**Part A — Linear Algebra**
- vector / matrix / tensor ka farq, `dot` vs `matmul` vs `@` vs `*` ka **poora** farq
- `np.dot` ka 1D/2D/ND behaviour, matmul broadcasting (stacked matrices)
- `inner`, `outer`, `cross`, `kron`, `vdot`, `tensordot`
- transpose, trace, diagonal, `matrix_rank`, determinant
- inverse (aur kab singular), `pinv`, `solve` vs inverse (accuracy + speed), `lstsq`
- eigenvalues (`eig`, `eigh`), **SVD** + low-rank reconstruction, QR, Cholesky
- norms (`ord=1/2/inf/'fro'`, axis-wise), condition number, positive-definite check
- `matrix_power`, identity/permutation matrices, rotation/scaling ka geometric matlab
- Applications: normal equation regression, projection, cosine similarity matrix,
  PCA teaser (SVD se), Markov chain steady state

**Part B — Random & Statistics**
- legacy `np.random.seed` vs **naya `default_rng` Generator API** (aur kyun naya behtar)
- `integers/random/normal/uniform/binomial/poisson/exponential/beta/choice/shuffle/permutation/permuted`
- reproducibility strategy, bit generators
- descriptive stats: mean/median/mode/var/std (`ddof`!)/percentile/quantile/IQR/corrcoef/cov
- weighted mean, z-score aur outlier detection
- sampling: bootstrap, train/test split, stratified idea
- **Monte Carlo**: pi estimation, dice, coin flips, random walk, portfolio simulation
- **Central Limit Theorem** aur **Law of Large Numbers** — numbers/tables se (plot ke baghair)

Phir: gotchas, 4 real-world problems, 4 LeetCode problems, 20+ interview Q&A, exercises, cheat-sheet.
""")

C(r"""
# Setup
import numpy as np

print("NumPy:", np.__version__)
np.set_printoptions(precision=4, suppress=True, linewidth=110)

def info(name, a):
    a = np.asarray(a)
    print(f"{name:<14} shape={str(a.shape):<14} ndim={a.ndim} dtype={a.dtype}")

# Poore notebook me yehi rng use karenge -> natije reproducible
rng = np.random.default_rng(seed=2024)
print("rng ready:", type(rng).__name__, "| bit generator:", type(rng.bit_generator).__name__)
""")

# ============================================================ PART A
M(r"""# PART A — Linear Algebra

## 1. Vector, Matrix, Tensor — naam ka jhagra khatam

| Naam | Math | NumPy | Misal |
|---|---|---|---|
| Scalar | 0D | `np.array(5)`, shape `()` | learning rate |
| Vector | 1D | shape `(n,)` | ek sample ke features |
| Matrix | 2D | shape `(m, n)` | dataset (rows=samples, cols=features) |
| Tensor | 3D+ | shape `(b, h, w, c)` | images ka batch |

### ML convention (yaad rakho)
`X` ki shape `(n_samples, n_features)` hoti hai — **rows = data points**.
Weights `W` ki shape `(n_features, n_outputs)`, to `X @ W` → `(n_samples, n_outputs)`.

### Row vector vs column vector ka trap
NumPy me `(n,)` **na** row hai na column — ye 1D hai aur context ke hisaab se behave karta hai.
- `(n,)` → 1D vector (dot product ke liye best)
- `(1, n)` → row vector (2D)
- `(n, 1)` → column vector (2D)

`a.T` ka **1D array par koi asar nahi hota** — ye sab se aam confusion hai!
""")

C(r"""
v1d = np.array([1., 2., 3.])          # 1D — na row na column
row = v1d.reshape(1, -1)              # (1,3) row vector
col = v1d.reshape(-1, 1)              # (3,1) column vector

info("v1d", v1d); info("row", row); info("col", col)
print("\nv1d.T ki shape:", v1d.T.shape, "<- KOI TABDEELI NAHI (1D par transpose bekaar)")
print("row.T ki shape:", row.T.shape, " col.T ki shape:", col.T.shape)

# 1D ko column banane ke teen tareeqe (sab barabar)
assert np.array_equal(v1d[:, None], col)
assert np.array_equal(v1d[:, np.newaxis], col)
assert np.array_equal(np.atleast_2d(v1d).T, col)
print("\nv1d[:, None] == reshape(-1,1) == atleast_2d(v1d).T  ✔")

# Kyun ahem? col @ row ek 3x3 matrix deta hai, row @ col ek 1x1
print("\ncol @ row shape:", (col @ row).shape, " (outer product)")
print("row @ col shape:", (row @ col).shape, " value:", (row @ col)[0, 0], "(inner product)")
""")

M(r"""
## 2. `*` vs `dot` vs `matmul` vs `@` — ye interview ka pakka sawal hai

| Operator | Naam | Kaam |
|---|---|---|
| `A * B` | element-wise (Hadamard) | har position ka apna zarb, **broadcasting** ke sath |
| `np.dot(A, B)` | dot product | 1D: scalar. 2D: matrix multiply. ND: **purana ajeeb rule** |
| `np.matmul(A, B)` / `A @ B` | matrix multiply | ND par **stacked matrices** treat karta hai (broadcast) |
| `np.multiply(A, B)` | == `A * B` | wohi element-wise |
| `np.inner(a, b)` | last axes par sum | 1D par == dot |
| `np.vdot(a, b)` | flatten + conjugate + dot | complex ke liye sahi inner product |

### Matrix multiply ka qanoon
```
(m, k) @ (k, n) -> (m, n)      # andar wale k barabar hone chahiye
```

### `dot` vs `matmul` ka asli farq (2 nuktay)
1. **2D × 2D** par dono bilkul same hain.
2. **3D+** par mukhtalif:
   - `matmul` → aakhri **do** axes ko matrix samajhta hai, baqi axes ko **batch** samajh kar
     broadcast karta hai. (Ye modern aur ML-friendly behaviour hai.)
   - `dot` → `dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])` — sab ke sath sab, output ki
     dimensions phool jati hain. Ziyada tar log ye ghalti se use karte hain.
3. `matmul` **scalar** ke sath kaam nahi karta (`A @ 2` → error), `np.dot(A, 2)` chal jata hai.

### Naseehat
> Matrix multiplication ke liye hamesha **`@`** likho. `np.dot` sirf 1D dot product ke liye.
""")

C(r"""
A = np.array([[1., 2.],
              [3., 4.]])
B = np.array([[5., 6.],
              [7., 8.]])

print("A * B (element-wise):\n", A * B)
print("\nA @ B (matrix multiply):\n", A @ B)
print("\nnp.dot(A,B) == A @ B (2D par same):", np.array_equal(np.dot(A, B), A @ B))
print("np.matmul(A,B) == A @ B:", np.array_equal(np.matmul(A, B), A @ B))

# Manual verification: result[0,0] = row0(A) . col0(B)
print("\nmanual (A@B)[0,0] =", A[0, 0]*B[0, 0] + A[0, 1]*B[1, 0], " numpy:", (A @ B)[0, 0])
assert (A @ B)[0, 0] == 19.

# Shape rule ka error
C34 = np.ones((3, 4))
try:
    _ = A @ C34.T          # (2,2) @ (4,3) -> andar wale 2 aur 4 match nahi
except ValueError as e:
    print("\n[expected error]", str(e)[:100])

# matmul scalar ke sath error deta hai, dot nahi
try:
    _ = A @ 2
except ValueError as e:
    print("[expected error] A @ 2 ->", str(e)[:70])
print("np.dot(A, 2) chal gaya:\n", np.dot(A, 2))
""")

C(r"""
# 1D vectors: dot = inner product = scalar
a = np.array([1., 2., 3.])
b = np.array([4., 5., 6.])
print("np.dot(a,b)   :", np.dot(a, b), "  (1*4 + 2*5 + 3*6 = 32)")
print("a @ b         :", a @ b, " <- 1D par @ bhi inner product deta hai")
print("np.inner(a,b) :", np.inner(a, b))
print("np.vdot(a,b)  :", np.vdot(a, b))
print("(a*b).sum()   :", (a * b).sum(), " <- yehi definition hai")
assert np.dot(a, b) == 32.

# Complex numbers par vdot ka farq (conjugate leta hai)
z1 = np.array([1+2j, 3+4j])
z2 = np.array([5+6j, 7+8j])
print("\ncomplex: np.dot  =", np.dot(z1, z2), "(conjugate NAHI)")
print("complex: np.vdot =", np.vdot(z1, z2), "<- pehla argument conjugate hota hai (sahi inner product)")
print("|z1|^2 vdot se:", np.vdot(z1, z1).real, " == (|z1|**2).sum():", (np.abs(z1)**2).sum())
""")

C(r"""
# Mixed shapes: 2D @ 1D aur 1D @ 2D (yahan dhyan se)
M2 = np.array([[1., 2., 3.],
               [4., 5., 6.]])          # (2,3)
v = np.array([1., 1., 1.])              # (3,)

print("M2 @ v  ->", M2 @ v, " shape:", (M2 @ v).shape, "<- (2,3)@(3,) = (2,) row sums")
u = np.array([1., 1.])                  # (2,)
print("u @ M2  ->", u @ M2, " shape:", (u @ M2).shape, "<- (2,)@(2,3) = (3,) col sums")

# Rule: 1D array right side par ho to usay column samjha jata hai (baad me axis hata di jati hai),
# left side par ho to row samjha jata hai. Result se wo dimension gayab ho jati hai.
assert (M2 @ v).tolist() == [6., 15.]
assert (u @ M2).tolist() == [5., 7., 9.]

# Neural network ka ek layer — X @ W + b (ML ka sab se aam expression)
X = rng.normal(size=(4, 3))             # 4 samples, 3 features
W = rng.normal(size=(3, 2))             # 3 features -> 2 outputs
bias = np.array([0.5, -0.5])
out = X @ W + bias                      # bias broadcast ho gaya (4,2) par
print("\nX@W + b shape:", out.shape, "(4 samples, 2 outputs)")
assert out.shape == (4, 2)
""")

C(r"""
# ND par matmul vs dot ka asli farq — STACKED (batched) matrices
batch_A = rng.normal(size=(5, 2, 3))     # 5 matrices, har ek (2,3)
batch_B = rng.normal(size=(5, 3, 4))     # 5 matrices, har ek (3,4)

mm = np.matmul(batch_A, batch_B)         # batch-wise: (5,2,3)@(5,3,4) -> (5,2,4)
print("matmul shape:", mm.shape, "<- 5 alag alag matrix multiplications")
assert mm.shape == (5, 2, 4)
assert np.allclose(mm[2], batch_A[2] @ batch_B[2])     # har batch element alag

dd = np.dot(batch_A, batch_B)            # purana rule: dimensions phool gayi!
print("dot shape   :", dd.shape, "<- (5,2,5,4) — ye ziyada tar GALAT hota hai")
assert dd.shape == (5, 2, 5, 4)

# matmul broadcasting: ek matrix ko poore batch par lagao
shared_W = rng.normal(size=(3, 4))       # (3,4) -> broadcast to (5,3,4)
print("\nbroadcast matmul:", np.matmul(batch_A, shared_W).shape, "<- (5,2,4)")
print("Transformers/CNN me batch matmul bilkul aise hota hai (torch.matmul same rules).")
""")

C(r"""
# outer / cross / kron / tensordot
a = np.array([1., 2., 3.])
b = np.array([4., 5.])

print("outer(a,b) shape", np.outer(a, b).shape, ":\n", np.outer(a, b))
print("\nouter == a[:,None] * b[None,:] ?", np.allclose(np.outer(a, b), a[:, None] * b[None, :]))

# cross product — sirf 3D (ya 2D) vectors ke liye, perpendicular vector deta hai
x, y = np.array([1., 0., 0.]), np.array([0., 1., 0.])
print("\ncross(x,y) =", np.cross(x, y), "<- z-axis (right hand rule)")
assert np.allclose(np.cross(x, y), [0., 0., 1.])
print("cross ke dono se dot = 0 (perpendicular):", np.dot(np.cross(x, y), x))

# kron — Kronecker product (block structure banata hai)
print("\nkron([1,2],[1,1]) =", np.kron([1, 2], [1, 1]))
print("kron(I2, [[1,2],[3,4]]) shape:", np.kron(np.eye(2), np.array([[1, 2], [3, 4]])).shape)

# tensordot — apni marzi ke axes par contraction
P = rng.normal(size=(2, 3, 4))
Q = rng.normal(size=(4, 5))
td = np.tensordot(P, Q, axes=([2], [0]))     # P ka axis2 aur Q ka axis0 contract
print("\ntensordot shape:", td.shape, "(2,3,5) — matmul jaisa hi natija")
assert np.allclose(td, P @ Q)
print("tensordot(axes=0) = outer product, axes=1 = matmul jaisa, axes=2 = double contraction")
""")

M(r"""
## 3. Matrix ki bunyadi properties

| Cheez | Function | Matlab |
|---|---|---|
| Transpose | `A.T`, `np.transpose(A, axes)` | rows ↔ columns (**view** hai, copy nahi) |
| Trace | `np.trace(A)` | diagonal ka jama (= eigenvalues ka jama) |
| Diagonal | `np.diag(A)` / `np.diag(v)` | nikalna / banana (dono kaam ek function!) |
| Rank | `np.linalg.matrix_rank(A)` | independent rows/columns ki tadaad |
| Determinant | `np.linalg.det(A)` | volume scaling factor; **0 = singular** |
| Inverse | `np.linalg.inv(A)` | `A @ A_inv = I`; sirf square + non-singular |
| Pseudo-inverse | `np.linalg.pinv(A)` | hamesha maujood (SVD se), non-square bhi |

### Rank ka intuition
Rank = "asli information ki tadaad". Agar ek column doosre ka multiple hai to wo koi nayi
information nahi de raha → rank kam ho jata hai (**multicollinearity** — regression me bara masla).

### det = 0 ka matlab
Matrix space ko "flatten" kar deta hai (volume 0) → information zaya → inverse namumkin.
""")

C(r"""
A = np.array([[4., 7., 2.],
              [3., 6., 1.],
              [2., 5., 3.]])

print("A:\n", A)
print("\nA.T:\n", A.T, "\nA.T ek view hai? ", A.T.base is A)
print("\ntrace     :", np.trace(A), " (4+6+3)")
print("diag nikalo:", np.diag(A))
print("diag banao (vector se matrix):\n", np.diag([1., 2., 3.]))
print("\nrank      :", np.linalg.matrix_rank(A))
print("det       :", round(float(np.linalg.det(A)), 6))

# Rank deficient matrix — teesra column pehle ka 2 guna
B = np.array([[1., 2., 2.],
              [3., 1., 6.],
              [5., 0., 10.]])
print("\nB (col2 = 2*col0) ka rank:", np.linalg.matrix_rank(B), "<- 3 nahi, 2! (dependent column)")
print("B ka det:", round(float(np.linalg.det(B)), 12), "<- ~0 => singular")
assert np.linalg.matrix_rank(B) == 2

# k-th diagonal aur triangular helpers
print("\nupper diagonal (k=1):", np.diag(A, k=1))
print("triu (upper triangle):\n", np.triu(A))
print("tril (lower triangle):\n", np.tril(A))
print("identity:", np.eye(2).tolist(), " zeros_like ok:", np.zeros_like(A).shape)
""")

C(r"""
# Inverse, singular matrix, pseudo-inverse
A = np.array([[4., 7.],
              [2., 6.]])
Ainv = np.linalg.inv(A)
print("A_inv:\n", Ainv)
print("\nA @ A_inv (I hona chahiye):\n", A @ Ainv)
print("allclose to I:", np.allclose(A @ Ainv, np.eye(2)))
# GOTCHA: exact barabari check MAT karo — floating point me chhoti error rehti hai
print("exact equal?", np.array_equal(A @ Ainv, np.eye(2)), "<- False! allclose use karo")

# Singular matrix -> LinAlgError (production code me try/except lazmi)
S = np.array([[1., 2.],
              [2., 4.]])            # row2 = 2*row1
try:
    np.linalg.inv(S)
except np.linalg.LinAlgError as e:
    print("\n[expected error] inv(singular) ->", e)

# pinv hamesha kaam karta hai (Moore-Penrose pseudo-inverse, SVD par bana)
Sp = np.linalg.pinv(S)
print("\npinv(S):\n", Sp)
print("S @ pinv(S) @ S == S ?", np.allclose(S @ Sp @ S, S), "<- pinv ki guarantee")

# pinv non-square par bhi chalta hai (least-squares ka core)
R = rng.normal(size=(5, 3))
print("\nnon-square (5,3) ka pinv shape:", np.linalg.pinv(R).shape, "(3,5)")
print("pinv(R) @ R == I3 ?", np.allclose(np.linalg.pinv(R) @ R, np.eye(3)))
""")

M(r"""
## 4. `solve` vs `inv` — system of equations ka sahi tareeqa

### Masla
`Ax = b` hal karna hai. Do tareeqe:
```python
x = np.linalg.inv(A) @ b     # BURA tareeqa
x = np.linalg.solve(A, b)    # ACHA tareeqa
```

### `solve` kyun behtar hai (interview me ye teen nuktay bolo)
1. **Accuracy** — `inv` pehle poora inverse compute karta hai (extra rounding errors),
   `solve` LU decomposition se direct hal nikalta hai.
2. **Speed** — `solve` ~2-3x tez (inverse ke n³ kaam ka bara hissa bekaar hai).
3. **Stability** — ill-conditioned matrices par `inv` ka jawab bohat kharab ho sakta hai.

### Rule
> "Never invert a matrix if you only need to solve a system." — numerical computing ka
> pehla sabaq. Sirf tab `inv` chahiye jab wo inverse **khud** matlub ho (rare).

### Non-square / inconsistent system?
`solve` sirf square + non-singular par chalta hai. Warna **`lstsq`** (least squares) use karo —
wo `||Ax - b||²` minimize karta hai (regression ka core).
""")

C(r"""
# 3 samikaran, 3 unknowns:  2x + y - z = 8 ;  -3x - y + 2z = -11 ;  -2x + y + 2z = -3
A = np.array([[ 2.,  1., -1.],
              [-3., -1.,  2.],
              [-2.,  1.,  2.]])
b = np.array([8., -11., -3.])

x_solve = np.linalg.solve(A, b)
x_inv   = np.linalg.inv(A) @ b
print("solve   :", x_solve)
print("inv @ b :", x_inv)
print("expected: [2, 3, -1]")
assert np.allclose(x_solve, [2., 3., -1.])
print("\nresidual ||Ax - b|| (solve):", np.linalg.norm(A @ x_solve - b))
print("residual ||Ax - b|| (inv)  :", np.linalg.norm(A @ x_inv - b))

# Speed comparison
import timeit
n = 200
Abig = rng.normal(size=(n, n)) + n * np.eye(n)      # diagonal dominant => well conditioned
bbig = rng.normal(size=n)
t_solve = timeit.timeit("np.linalg.solve(Abig, bbig)", globals=globals(), number=30)
t_inv   = timeit.timeit("np.linalg.inv(Abig) @ bbig", globals=globals(), number=30)
print(f"\nsolve : {t_solve:.4f}s   inv@b : {t_inv:.4f}s   -> solve ~{t_inv/max(t_solve,1e-9):.1f}x tez")
""")

C(r"""
# Ill-conditioned matrix par inv ka accuracy masla (condition number ka asar)
H = np.array([[1., 1/2, 1/3],                  # Hilbert matrix — famous ill-conditioned
              [1/2, 1/3, 1/4],
              [1/3, 1/4, 1/5]])
x_true = np.array([1., 1., 1.])
b = H @ x_true

x_s = np.linalg.solve(H, b)
x_i = np.linalg.inv(H) @ b
print("condition number:", f"{np.linalg.cond(H):.1f}", "<- bara = khatarnaak")
print("solve error :", f"{np.abs(x_s - x_true).max():.3e}")
print("inv   error :", f"{np.abs(x_i - x_true).max():.3e}", "<- aam tor par ziyada")

# Condition number ka matlab: input me 1 unit error -> output me cond(A) guna error
print("\ncond(I) =", np.linalg.cond(np.eye(3)), "(perfect)")
print("cond(singular) =", f"{np.linalg.cond(np.array([[1., 2.], [2., 4.]])):.2e}", "(infinity ke qareeb)")
print("\nRule of thumb: cond(A) ~ 1e{k} => aakhri ~k digits par bharosa na karo.")
""")

C(r"""
# lstsq — overdetermined system (samikaran ziyada, unknowns kam) = LINEAR REGRESSION
# y = 3x + 5 par thora noise
x_data = np.linspace(0, 10, 20)
y_data = 3 * x_data + 5 + rng.normal(0, 0.5, 20)

# Design matrix: [x, 1] taake slope aur intercept dono nikal aayein
Xd = np.column_stack([x_data, np.ones_like(x_data)])
coef, residuals, rank, sv = np.linalg.lstsq(Xd, y_data, rcond=None)
slope, intercept = coef
print(f"fit: y = {slope:.3f}x + {intercept:.3f}   (asli: y = 3x + 5)")
print("rank:", rank, " singular values:", np.round(sv, 3))
print("residual sum of squares:", np.round(residuals, 4))
assert abs(slope - 3) < 0.2 and abs(intercept - 5) < 0.6

# Wohi kaam normal equation se: w = (X'X)^-1 X'y  -> solve se (inv se nahi!)
w_normal = np.linalg.solve(Xd.T @ Xd, Xd.T @ y_data)
print("\nnormal equation se:", np.round(w_normal, 4), " lstsq se:", np.round(coef, 4))
assert np.allclose(w_normal, coef, atol=1e-8)
print("Dono barabar. Magar lstsq numerically ziyada stable hai (SVD par bana hai).")
""")

M(r"""
## 5. Eigenvalues aur Eigenvectors

### Kya hai
```
A v = λ v
```
`v` (eigenvector) wo khaas direction hai jise matrix **ghumata nahi**, sirf **kheenchta**
(scale karta) hai. `λ` (eigenvalue) batata hai kitna kheencha.

### Kahan use hota hai
- **PCA** — covariance matrix ke eigenvectors = principal components
- **Markov chains** — λ=1 ka eigenvector = steady state distribution
- **PageRank** — dominant eigenvector
- Stability analysis, spectral clustering, graph Laplacians

### `eig` vs `eigh` (ahem farq)
| | `np.linalg.eig` | `np.linalg.eigh` |
|---|---|---|
| Input | koi bhi square matrix | **symmetric/Hermitian** matrix |
| Output | **complex** ho sakta hai, unsorted | hamesha **real**, **ascending sorted** |
| Speed | slow | ~2-3x tez |

Covariance/correlation matrices hamesha symmetric hoti hain → **`eigh` use karo**.

### Gotchas
1. `eig` ke eigenvectors **columns** me hote hain (`w[:, i]`), rows me nahi!
2. Eigenvector ka sign/scale unique nahi — `-v` bhi bilkul sahi eigenvector hai.
3. `eig` real matrix par bhi complex de sakta hai (rotation matrices!).
""")

C(r"""
# eig ka bunyadi demo
A = np.array([[4., 1.],
              [2., 3.]])
vals, vecs = np.linalg.eig(A)
print("eigenvalues :", vals)
print("eigenvectors (COLUMNS me):\n", vecs)

# Definition verify: A v = lambda v
for i in range(len(vals)):
    v = vecs[:, i]                       # i-th eigenvector = i-th COLUMN
    print(f"\nA @ v{i} =", np.round(A @ v, 6), "   lambda*v{0} =".format(i), np.round(vals[i] * v, 6))
    assert np.allclose(A @ v, vals[i] * v)

# Do mazedar identities
print("\nsum(eigenvalues) =", round(float(vals.sum()), 6), " == trace(A) =", np.trace(A))
print("prod(eigenvalues) =", round(float(np.prod(vals)), 6), " == det(A) =", round(float(np.linalg.det(A)), 6))
assert np.isclose(vals.sum(), np.trace(A))
assert np.isclose(np.prod(vals), np.linalg.det(A))
""")

C(r"""
# eigh — symmetric matrix ke liye (PCA ka rasta)
X = rng.normal(size=(100, 3)) @ np.array([[2., 0.5, 0.], [0., 1., 0.3], [0., 0., 0.7]])
cov = np.cov(X, rowvar=False)              # (3,3) symmetric
print("cov symmetric?", np.allclose(cov, cov.T))

w, V = np.linalg.eigh(cov)                 # ascending order me
print("\neigh eigenvalues (ascending):", np.round(w, 4))
order = np.argsort(-w)                     # PCA ke liye descending chahiye
w, V = w[order], V[:, order]
print("descending:", np.round(w, 4))
print("explained variance ratio:", np.round(w / w.sum(), 4))

# Eigenvectors orthonormal hote hain (symmetric matrix par) -> V.T @ V = I
print("\nV.T @ V == I ?", np.allclose(V.T @ V, np.eye(3)))
# Reconstruction: A = V diag(w) V.T  (spectral decomposition)
assert np.allclose(V @ np.diag(w) @ V.T, cov)
print("spectral decomposition verified: cov == V @ diag(w) @ V.T ✔")

# eig complex de sakta hai — rotation matrix par
theta = np.pi / 4
Rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
print("\nrotation matrix ke eigenvalues:", np.linalg.eigval:=np.linalg.eigvals(Rot), "<- COMPLEX!")
""")

M(r"""
## 6. SVD — sab se taqatwar decomposition

### Kya hai
**Har** matrix (square ho ya na ho, singular ho ya na ho) ko tor sakte hain:
```
A = U @ diag(S) @ Vt        # A: (m,n),  U: (m,m),  S: (min(m,n),),  Vt: (n,n)
```
- `U`, `Vt` orthonormal (rotations)
- `S` = **singular values**, descending order me, sab non-negative (stretching)

Yaani har linear transformation = **rotate → stretch → rotate**.

### Kahan use hota hai (ML me har jagah)
- **PCA** (covariance ke eigen ki jagah data par direct SVD — numerically behtar)
- **Low-rank approximation** / image compression
- **Recommender systems** (matrix factorization)
- **Pseudo-inverse** aur `lstsq` isi par bane hain
- Noise removal, LSA (topic modeling), rank/condition number nikalna

### Eckart–Young theorem
Top-k singular values rakh kar baqi 0 kar do → **best possible rank-k approximation**
(Frobenius norm me). Ye compression ki riyazi guarantee hai.

### Gotchas
1. `np.linalg.svd` **`Vt` (already transposed)** deta hai — `V` nahi. `V = Vt.T`.
2. `full_matrices=False` (economy SVD) use karo — bara memory bachta hai.
3. `S` ek **1D array** hai, matrix nahi — `np.diag(S)` khud lagana parta hai.
""")

C(r"""
A = np.array([[3., 1., 1.],
              [-1., 3., 1.]])                  # (2,3) non-square

U, S, Vt = np.linalg.svd(A, full_matrices=False)
print("U shape:", U.shape, " S:", np.round(S, 4), " Vt shape:", Vt.shape)
print("\nreconstruction A == U @ diag(S) @ Vt ?", np.allclose(U @ np.diag(S) @ Vt, A))
print("U orthonormal (U.T@U=I)?", np.allclose(U.T @ U, np.eye(U.shape[1])))
print("singular values descending?", bool(np.all(np.diff(S) <= 0)))

# SVD se rank, condition number aur norms
print("\nrank (non-zero singular values):", int((S > 1e-10).sum()), " == matrix_rank:", np.linalg.matrix_rank(A))
print("cond = S.max()/S.min() =", round(float(S.max()/S.min()), 4), " == np.linalg.cond:", round(float(np.linalg.cond(A)), 4))
print("2-norm (spectral) = S.max() =", round(float(S.max()), 4), " == norm(A, 2):", round(float(np.linalg.norm(A, 2)), 4))
print("Frobenius = sqrt(sum(S^2)) =", round(float(np.sqrt((S**2).sum())), 4), " == norm(A,'fro'):", round(float(np.linalg.norm(A, 'fro')), 4))
""")

C(r"""
# Low-rank approximation demo — "image compression" ka core idea
# Ek 12x12 matrix banate hain jiska asli rank sirf 3 hai + halka noise
rank_true = 3
L = rng.normal(size=(12, rank_true))
R = rng.normal(size=(rank_true, 12))
M0 = L @ R + rng.normal(0, 0.05, size=(12, 12))

U, S, Vt = np.linalg.svd(M0)
print("singular values:", np.round(S, 3))
print("energy ratio (S^2 ka hissa):", np.round(np.cumsum(S**2) / (S**2).sum(), 4)[:6])

def low_rank(k):
    # sirf top-k components se dobara banao
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

print("\n k | relative error ||M-Mk||_F / ||M||_F | storage (numbers)")
den = np.linalg.norm(M0, 'fro')
for k in [1, 2, 3, 4, 6, 12]:
    err = np.linalg.norm(M0 - low_rank(k), 'fro') / den
    storage = k * (12 + 12 + 1)
    print(f"{k:2d} | {err:34.5f} | {storage:5d}  (asal: {M0.size})")

# k=3 par error bohat gir jata hai kyunke asli rank 3 tha
assert np.linalg.norm(M0 - low_rank(3), 'fro') / den < 0.1
assert np.allclose(low_rank(12), M0)
print("\nk=3 par error <10% — SVD ne chhupa hua rank pakar liya ✔")
""")

C(r"""
# QR aur Cholesky (mukhtasar)
A = np.array([[12., -51., 4.],
              [6., 167., -68.],
              [-4., 24., -41.]])
Q, R = np.linalg.qr(A)
print("QR: Q orthonormal?", np.allclose(Q.T @ Q, np.eye(3)), " R upper triangular?",
      np.allclose(R, np.triu(R)))
print("A == Q @ R ?", np.allclose(Q @ R, A))
print("\nQR ka use: least squares (lstsq ka aik implementation), Gram-Schmidt,")
print("aur eigenvalue algorithms (QR iteration).")

# Cholesky — sirf symmetric POSITIVE DEFINITE matrices par: A = L @ L.T
P = np.array([[4., 2., 1.],
              [2., 5., 3.],
              [1., 3., 6.]])
L = np.linalg.cholesky(P)
print("\nL (lower triangular):\n", np.round(L, 4))
print("L @ L.T == P ?", np.allclose(L @ L.T, P))
print("Cholesky ~2x tez hai LU se — Gaussian sampling aur GP/Kalman filters me use hota hai.")

# Positive definite check ke do tareeqe
def is_pos_def_eig(M):
    return bool(np.all(np.linalg.eigvalsh(M) > 0))          # saare eigenvalues > 0

def is_pos_def_chol(M):
    # Cholesky ka chalna hi positive-definite ka proof hai (aur ye tez tareeqa hai)
    try:
        np.linalg.cholesky(M)
        return True
    except np.linalg.LinAlgError:
        return False

bad = np.array([[1., 2.], [2., 1.]])                         # eigenvalues: 3, -1
print("\nP positive definite?", is_pos_def_eig(P), is_pos_def_chol(P))
print("bad positive definite?", is_pos_def_eig(bad), is_pos_def_chol(bad))
assert is_pos_def_chol(P) and not is_pos_def_chol(bad)
""")

M(r"""
## 7. Norms — "lambai" napne ke mukhtalif tareeqe

`np.linalg.norm(x, ord=None, axis=None, keepdims=False)`

### Vector norms
| `ord` | Naam | Formula | Use |
|---|---|---|---|
| `1` | L1 / Manhattan | `sum(|x|)` | Lasso regularization, sparsity |
| `2` (default) | L2 / Euclidean | `sqrt(sum(x²))` | distance, Ridge regularization |
| `np.inf` | max norm | `max(|x|)` | worst-case error |
| `0` | (norm nahi) | non-zero ki ginti | sparsity count |

### Matrix norms
| `ord` | Matlab |
|---|---|
| `'fro'` | Frobenius: `sqrt(sum(A²))` — sab elements ka RMS (default agar `ord=None`) |
| `2` | spectral norm = sab se bara singular value |
| `1` | max **column** ka absolute sum |
| `np.inf` | max **row** ka absolute sum |
| `'nuc'` | nuclear = singular values ka jama (low-rank regularization) |

### Sab se kaam ki cheez: `axis`
`np.linalg.norm(X, axis=1)` → **har row** ka norm (n samples ke length ek sath).
Ye normalization aur distance computation me rozana lagta hai.
""")

C(r"""
v = np.array([3., -4., 0., 12.])
print("L1  :", np.linalg.norm(v, 1), " (3+4+0+12)")
print("L2  :", np.linalg.norm(v), "   (sqrt(9+16+0+144)=13)")
print("Linf:", np.linalg.norm(v, np.inf), " (max abs)")
print("L0-ish (non-zero count):", np.linalg.norm(v, 0))
assert np.linalg.norm(v) == 13.0

Am = np.array([[1., -2.], [-3., 4.]])
print("\nFrobenius :", round(float(np.linalg.norm(Am, 'fro')), 4), " == sqrt(1+4+9+16)")
print("spectral 2:", round(float(np.linalg.norm(Am, 2)), 4), " (max singular value)")
print("ord=1  (max col sum):", np.linalg.norm(Am, 1))
print("ord=inf(max row sum):", np.linalg.norm(Am, np.inf))
print("nuclear:", round(float(np.linalg.norm(Am, 'nuc')), 4))

# axis ka asli faida: per-row norms + unit vectors banana
X = np.array([[3., 4.],
              [1., 0.],
              [5., 12.]])
row_norms = np.linalg.norm(X, axis=1, keepdims=True)      # (3,1) keepdims!
print("\nper-row norms:", row_norms.ravel())
X_unit = X / row_norms                                    # L2 normalization
print("normalized rows ka norm:", np.linalg.norm(X_unit, axis=1))
assert np.allclose(np.linalg.norm(X_unit, axis=1), 1.0)
""")

C(r"""
# matrix_power, identity, permutation matrix aur geometry
print("A^3 (matrix power, A@A@A):\n", np.linalg.matrix_power(np.array([[1., 1.], [0., 1.]]), 3))
print("\nA^0 = identity:\n", np.linalg.matrix_power(np.array([[2., 3.], [4., 5.]]), 0))
print("A^-1 == inv(A) ?", np.allclose(np.linalg.matrix_power(np.array([[4., 7.], [2., 6.]]), -1),
                                     np.linalg.inv(np.array([[4., 7.], [2., 6.]]))))

# Permutation matrix — rows ki tarteeb badalta hai
P = np.eye(3)[[2, 0, 1]]                    # identity ki rows rearrange
print("\npermutation matrix:\n", P)
data = np.array([[1., 1.], [2., 2.], [3., 3.]])
print("P @ data (rows reorder):\n", P @ data)
assert (P @ data)[0].tolist() == [3., 3.]

# GEOMETRY: rotation aur scaling
def rotation(deg):
    t = np.radians(deg)
    return np.array([[np.cos(t), -np.sin(t)],
                     [np.sin(t),  np.cos(t)]])

point = np.array([1., 0.])
print("\n(1,0) ko 90 degree ghumao ->", np.round(rotation(90) @ point, 10), "(0,1 hona chahiye)")
print("(1,0) ko 180 degree      ->", np.round(rotation(180) @ point, 10))
assert np.allclose(rotation(90) @ point, [0., 1.])

# Rotation matrix ki khasoosiyat: det=1, inverse == transpose (orthogonal)
Rz = rotation(37)
print("\ndet(rotation) =", round(float(np.linalg.det(Rz)), 10), "(hamesha 1 — area barqarar)")
print("R.T == R^-1 ?", np.allclose(Rz.T, np.linalg.inv(Rz)), "<- orthogonal matrix")

scale = np.diag([2., 0.5])                  # x ko double, y ko half
print("\nscaling matrix ka det:", np.linalg.det(scale), "<- area 1x rehta (2 * 0.5)")
print("combined (rotate phir scale):\n", np.round(scale @ rotation(90), 6))
print("\nYAAD RAKHO: matrix zarb me tarteeb ahem hai — scale@rot != rot@scale")
assert not np.allclose(scale @ rotation(37), rotation(37) @ scale)
""")
