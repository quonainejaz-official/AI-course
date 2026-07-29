import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code

CELLS = []
A = CELLS.append

A(md("""
# Asyncio, Coroutines aur Async Patterns

**Level:** Advanced &nbsp;|&nbsp; **Folder:** `Python/Advance` &nbsp;|&nbsp; **Python:** 3.14

`asyncio` Python ka wo hissa hai jise log "samajh" lete hain magar "mehsoos" nahi karte.
Is notebook me hum event loop ko *dekhenge*: kaun kab chalta hai, `await` par kya hota hai,
task cancel hone par cleanup kaise hota hai, aur asli production patterns kaise likhte hain.

## Is notebook me kya seekhenge

- **Blocking vs non-blocking**, aur **concurrency vs parallelism** ka asli farq
- **Event loop ka mental model** — single thread, cooperative multitasking
- `async def` / `await`, **coroutine object** (await na karne par kya hota hai)
- `asyncio.run`, **tasks vs coroutines**, `create_task`
- `gather` vs `as_completed` vs `wait` vs **`TaskGroup`** (3.11+)
- **Timeouts:** `asyncio.timeout`, `wait_for`
- **Cancellation** aur `CancelledError` ke sath sahi cleanup (`try/finally`, `shield`)
- **Sequential vs concurrent** timing ka live muqabla
- **Async iterators**, **async generators**, **async context managers**
- **Semaphore / Lock / Event / Queue** — producer-consumer aur worker pool
- **`run_in_executor`**, **`asyncio.to_thread`** — blocking/CPU kaam ka sahi jagah
- `gather(return_exceptions=True)` aur **ExceptionGroup** (`except*`)
- **Pitfalls:** `await` bhool jana, loop ko `time.sleep` se block karna, fire-and-forget tasks
- **Real patterns:** rate-limited fake API fetcher, worker pool, retry with backoff, pipeline
- **LeetCode:** 1834 (Single-Threaded CPU) + async simulation, 1188 (Bounded Blocking Queue) ka async version, 621 (Task Scheduler)

## Prerequisites
Functions, generators, exceptions, decorators ki samajh. Threads ka basic idea (notebook 03 me tafseel).

> **Zaroori note:** Is notebook me **koi network call nahi** — saara I/O `asyncio.sleep()` se
> **simulate** kiya gaya hai. Notebook ke cells me top-level `await` nahi chalta, is liye har demo
> `async def main()` + `asyncio.run(main())` ke pattern se chalta hai (yehi asli scripts ka tareeqa bhi hai).
"""))

A(md("""
---
## 1. Blocking vs Non-blocking — asal masla kya hai

### Kya hai
- **Blocking call**: `time.sleep(2)`, file read, DB query, HTTP request — thread **ruk** jaata hai
  aur us dauran kuch nahi hota, CPU bekaar baitha hai.
- **Non-blocking / async**: "main is I/O ka intezar kar raha hoon, meri jagah koi doosra kaam chalao" —
  event loop us waqt doosre coroutines chalata hai.

### Kyun important hai
Asli web/API code ka 90% waqt **I/O ka intezar** hota hai. Agar 100 requests karni hain aur
har ek 100ms leti hai:
- Blocking: 100 × 100ms = **10 second**
- Async: sab ek sath = **~100ms** (network ki hadd tak)

Ye CPU speed ka masla hi nahi tha — **intezar ko overlap** karne ka masla tha.

### Ahem baat
Async **CPU-bound** kaam tez nahi karta. Number crunching ke liye processes chahiye (notebook 03).
"""))

A(code(r"""
import asyncio, time

# "Network call" ko simulate karne wale do version -- ek blocking, ek async
def fetch_blocking(name, delay):
    time.sleep(delay)                 # BLOCKING: poora thread ruk gaya
    return f"{name}-data"

async def fetch_async(name, delay):
    await asyncio.sleep(delay)        # NON-BLOCKING: loop ko control wapas de diya
    return f"{name}-data"

JOBS = [("api-a", 0.10), ("api-b", 0.10), ("api-c", 0.10), ("api-d", 0.10)]

# --- blocking: ek ke baad ek ---
t0 = time.perf_counter()
blocking_results = [fetch_blocking(n, d) for n, d in JOBS]
blocking_time = time.perf_counter() - t0

# --- async: sab ek sath ---
async def main():
    tasks = [fetch_async(n, d) for n, d in JOBS]
    return await asyncio.gather(*tasks)      # sab ko concurrent chalao

t0 = time.perf_counter()
async_results = asyncio.run(main())
async_time = time.perf_counter() - t0

assert blocking_results == async_results     # natija bilkul same
print("results        :", async_results)
print(f"blocking (4 x 100ms): {blocking_time:.2f}s   <- jama ho gaya")
print(f"async    (4 x 100ms): {async_time:.2f}s   <- overlap ho gaya")
print(f"faida               : ~{blocking_time / async_time:.1f}x")
print("\nNote: total async waqt ~sab se lambe kaam ke barabar hai, sab ka jama nahi.")
"""))

A(md("""
### Output ka matlab
Chaar "API calls" jinme se har ek 100ms leti thi: blocking me ~0.4s, async me ~0.1s.
Async ne kaam tez nahi kiya — **intezar ko overlap** kiya.

### Gotchas
- `time.sleep()` async function ke andar likh do to **poora event loop** ruk jata hai (aage demo hai).
- Agar kaam CPU-bound hai (hashing, image resize, big loops) to async se **zero** faida.

### Interview tip
*"asyncio gives concurrency for I/O-bound work on a single thread by overlapping waits;
it does not give parallelism for CPU-bound work."*
"""))

A(md("""
---
## 2. Concurrency vs Parallelism

### Definitions (interview me exactly ye bolo)
- **Concurrency** = ek waqt me **kai kaam sambhalna** (progress interleaved). Ek chef 3 dishes
  ke beech switch kar raha hai.
- **Parallelism** = ek waqt me **kai kaam chalana** (literally same instant). 3 chefs, 3 dishes.

Python me:

| Approach | Model | Best for | Kitne CPU cores use hote |
|---|---|---|---|
| `asyncio` | concurrency, 1 thread, cooperative | bohat sara I/O wait (network, DB, files) | 1 |
| `threading` | concurrency, kai threads, preemptive (GIL) | blocking I/O + purani libraries | 1 (GIL) |
| `multiprocessing` | **parallelism**, kai processes | CPU-bound (math, parsing, ML) | sab |

### Cooperative vs preemptive
- Threads: OS jab chahe switch kar sakta hai (**preemptive**) → race conditions, locks chahiye.
- asyncio: switch **sirf `await` par** hota hai (**cooperative**) → do lines ke beech koi
  ghus nahi sakta, is liye data races bohat kam. Magar agar tum `await` nahi karte
  (ya blocking call karte ho) to kisi ko chance hi nahi milta.
"""))

A(code(r"""
import asyncio

# Cooperative scheduling ko 'dekho': switch sirf await par hota hai
LOG = []

async def worker(name, steps):
    for i in range(steps):
        LOG.append(f"{name}{i}")
        await asyncio.sleep(0)        # sleep(0) = "meri baari khatam, agla chalao"
    return name

async def main():
    return await asyncio.gather(worker("A", 3), worker("B", 3), worker("C", 3))

names = asyncio.run(main())
print("order:", " ".join(LOG))
print("returns:", names)
print("\nDekha? A0 B0 C0 A1 B1 C1 ... -> har await par baari badal gayi (round-robin jaisa).")

# Ab wohi coroutines BINA await ke andar
LOG.clear()
async def greedy(name, steps):
    for i in range(steps):
        LOG.append(f"{name}{i}")      # koi await nahi -> koi switch nahi
    return name

async def main2():
    return await asyncio.gather(greedy("A", 3), greedy("B", 3), greedy("C", 3))

asyncio.run(main2())
print("\ngreedy order:", " ".join(LOG))
print("Dekha? A ne poora kaam khatam kiya, phir B... (kisi await ke baghair koi switch nahi)")
print("Sabaq: cooperative multitasking me 'yield point' (await) hi asli scheduler hai.")
"""))

A(md("""
### Output ka matlab
Pehle case me output `A0 B0 C0 A1 B1 C1 ...` tha — kyunki har `await asyncio.sleep(0)` par
coroutine ne control chhora. Doosre case me koi `await` nahi tha, is liye har coroutine
apna poora kaam ek hi baar me kar gaya.

### Interview tip
*"asyncio is cooperative: a coroutine runs until it awaits. Between two statements without an
`await`, nothing else can interleave — that's why asyncio code rarely needs locks for pure
in-memory state, but a single blocking call freezes everything."*
"""))

A(md("""
---
## 3. Event Loop ka Mental Model

### Kya hai
Event loop ek **while loop** hai jo ye karta hai:

```text
while there is work:
    1. "ready" queue se agla callback/coroutine chalao (jab tak wo await na kare)
    2. jo coroutines I/O ka intezar kar rahe hain, unke sockets/timers OS se poocho (select/epoll/IOCP)
    3. jo tayyar ho gaye unhe ready queue me daal do
    4. timers (sleep) check karo, waqt aa gaya to unhe ready karo
```

### Ahem nukaat
- **Ek thread**, ek waqt me **ek** coroutine chal raha hota hai.
- `await` ka matlab: "meri state sambhaal lo, main ruk raha hoon, jab ye future tayyar ho to mujhe wapas chalao".
- Coroutine ek **suspendable function** hai (generator ki tarah), aur `Task` us coroutine ka
  "scheduler wala wrapper" hai jo loop me register hota hai.
- Loop me **koi bhi** blocking cheez (CPU loop, `time.sleep`, sync DB call) sab kuch rok deti hai.
"""))

A(code(r"""
import asyncio, inspect

async def demo(x):
    await asyncio.sleep(0)
    return x * 2

# 1) 'async def' call karne se function CHALTA NAHI -- coroutine object banta hai
coro = demo(5)
print("type          :", type(coro).__name__)
print("iscoroutine?  :", inspect.iscoroutine(coro))
print("chal gaya?    : nahi -- sirf object bana hai (koi output nahi aaya)")
coro.close()          # await nahi karna to close kar do warna 'never awaited' warning aati hai

# 2) Chalane ke 3 tareeqe
print("\nasyncio.run se:", asyncio.run(demo(5)))

async def main():
    r1 = await demo(1)                              # seedha await
    t = asyncio.create_task(demo(2))                 # task banao (foran schedule)
    r2 = await t
    r3 = await asyncio.gather(demo(3), demo(4))      # kai ek sath
    # loop ke andar se loop ki info
    loop = asyncio.get_running_loop()
    return r1, r2, r3, type(loop).__name__

print("andar se       :", asyncio.run(main()))

# 3) Loop ke baahar loop ki cheezein maangna -> error
try:
    asyncio.get_running_loop()
except RuntimeError as e:
    print("\nbaahar get_running_loop() ->", type(e).__name__, ":", e)

# 4) asyncio.run ke andar dobara asyncio.run -> error (nested loops allowed nahi)
async def nested():
    return asyncio.run(demo(1))      # GALAT
try:
    asyncio.run(nested())
except RuntimeError as e:
    print("nested asyncio.run   ->", type(e).__name__, ":", str(e)[:60])
print("\nJupyter/IPython me loop pehle se chal raha hota hai -> wahan cell me seedha 'await' likho,")
print("ya nest_asyncio use karo. Scripts me hamesha ek hi asyncio.run(main()) entry point rakho.")
"""))

A(md("""
### Output ka matlab
- `demo(5)` ne function chalaya **nahi** — sirf coroutine object banaya. Async code "lazy" hai.
- `asyncio.run()` ne naya loop banaya, coroutine chalaya, aur loop band kar diya.
- Nested `asyncio.run` ne `RuntimeError` diya — ek thread me ek waqt me ek hi loop.

### Gotchas
1. Coroutine ko `await` na karo to kaam hota hi nahi (silent bug!) — Python `RuntimeWarning` deta hai.
2. `asyncio.run()` ko library code me na chalao — sirf application ke entry point par.
3. Jupyter me loop already chal raha hota hai (is notebook ke cells `exec` se chalte hain,
   is liye yahan `asyncio.run` theek kaam karta hai).

### Interview tip
*"A coroutine is a suspendable function object; the event loop is a single-threaded scheduler that
resumes coroutines when their awaited futures (timers, sockets) become ready. A Task wraps a
coroutine and schedules it on the loop."*
"""))

A(md("""
---
## 4. Coroutines vs Tasks — sab se zyada confusion yahan hai

### Farq
| | Coroutine | Task |
|---|---|---|
| Banta kaise hai | `foo()` (async def call) | `asyncio.create_task(foo())` |
| Kab chalna shuru hota hai | **jab tum `await` karo** | **foran** (agli `await` par loop chala dega) |
| Concurrency | akela `await` = sequential | kai tasks = concurrent |
| Cancel/inspect | nahi | `task.cancel()`, `task.done()`, `task.result()` |

### Sunehri rule
> `await one_thing()` = **sequential**.
> Concurrency chahiye to **pehle sab tasks banao**, phir await karo (ya `gather`/`TaskGroup` use karo).
"""))

A(code(r"""
import asyncio, time

async def job(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done"

# GALAT: har await mukammal hone ka intezar -> sequential
async def sequential():
    t0 = time.perf_counter()
    r1 = await job("a", 0.1)
    r2 = await job("b", 0.1)
    r3 = await job("c", 0.1)
    return [r1, r2, r3], time.perf_counter() - t0

# SAHI: pehle tasks banao (foran schedule ho gaye), phir intezar karo
async def concurrent_tasks():
    t0 = time.perf_counter()
    t1 = asyncio.create_task(job("a", 0.1))
    t2 = asyncio.create_task(job("b", 0.1))
    t3 = asyncio.create_task(job("c", 0.1))
    results = [await t1, await t2, await t3]        # ye sab pehle se chal rahe the
    return results, time.perf_counter() - t0

# SAB SE SAAF: gather (khud tasks bana deta hai)
async def with_gather():
    t0 = time.perf_counter()
    results = await asyncio.gather(job("a", 0.1), job("b", 0.1), job("c", 0.1))
    return results, time.perf_counter() - t0

for label, fn in [("sequential awaits", sequential),
                  ("create_task x3   ", concurrent_tasks),
                  ("gather           ", with_gather)]:
    res, el = asyncio.run(fn())
    print(f"{label}: {el:.2f}s  {res}")

# Task ki inspection
async def inspect_task():
    t = asyncio.create_task(job("x", 0.05))
    print("\nbanane ke foran baad -> done?", t.done(), "| cancelled?", t.cancelled())
    await asyncio.sleep(0)          # loop ko ek chance do
    print("ek tick baad         -> done?", t.done())
    result = await t
    print("await ke baad        -> done?", t.done(), "| result:", t.result())
    print("naam                 :", t.get_name())
    return result

asyncio.run(inspect_task())
"""))

A(md("""
### Output ka matlab
`sequential` ~0.3s, `create_task` aur `gather` ~0.1s. Teeno ka natija same hai —
farq sirf ye hai ke kaam **kab shuru** hua.

### Gotchas
- `asyncio.create_task()` ko chalne ke liye loop chahiye — module top-level par call na karo.
- Task ka **reference sambhaalo**! Warna GC task ko beech me utha sakta hai
  ("fire and forget" ka masla — aage pitfalls me demo hai).
- `await task` do dafa karna theek hai (wohi result milta hai), magar coroutine ko do dafa
  await karna `RuntimeError` deta hai.

### Interview tip
*"Awaiting a coroutine runs it sequentially; wrapping coroutines in Tasks (or using
`gather`/`TaskGroup`) schedules them immediately so their waits overlap."*
"""))

A(code(r"""
import asyncio

# Coroutine ko do dafa await karne ki koshish -> RuntimeError
async def demo():
    return 1

async def main():
    coro = demo()
    print("pehla await :", await coro)
    try:
        await coro                     # coroutine ek dafa chal kar khatam ho jaata hai
    except RuntimeError as e:
        print("doosra await:", type(e).__name__, ":", e)

    # Task ko jitna chaho await karo -- result cached hai
    t = asyncio.create_task(demo())
    print("task await 1:", await t)
    print("task await 2:", await t, "<- wohi result, dobara nahi chala")

asyncio.run(main())
"""))
