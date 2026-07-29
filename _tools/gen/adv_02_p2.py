import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code

CELLS = []
A = CELLS.append

A(md("""
---
## 5. `gather` vs `as_completed` vs `wait` vs `TaskGroup`

### Char tools, char maqasid

| Tool | Kab use karo | Results kaise milte | Error hone par |
|---|---|---|---|
| `asyncio.gather(*aws)` | sab ke results **tarteeb se** chahiye | list, **input order me** | pehla error foran raise (baaqi chalte rehte hain!) |
| `gather(..., return_exceptions=True)` | sab ka natija chahiye, error bhi data ki tarah | list jis me exceptions bhi | koi raise nahi |
| `asyncio.as_completed(aws)` | jo pehle khatam ho usay foran process karo (streaming) | jaise jaise mukammal hon | us await par raise |
| `asyncio.wait(tasks, return_when=...)` | "pehla khatam hote hi aage barho", manual control | `(done, pending)` sets | raise nahi karta — tum `task.exception()` dekho |
| `asyncio.TaskGroup()` (3.11+) | **modern default** — structured concurrency | tasks ke `.result()` | **ExceptionGroup**, baaqi tasks **cancel** |

### Rule of thumb (2026 me)
Naya code likh rahe ho → **`TaskGroup`** use karo. Simple "sab ke results do" → `gather`.
Streaming results → `as_completed`. Low-level control → `wait`.
"""))

A(code(r"""
import asyncio, time

async def job(name, delay, fail=False):
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(f"{name} fail ho gaya")
    return f"{name}({delay}s)"

# ---------- 1) gather: order mehfooz ----------
async def demo_gather():
    results = await asyncio.gather(job("slow", 0.06), job("fast", 0.01), job("mid", 0.03))
    return results

print("gather results (input order):", asyncio.run(demo_gather()))

# ---------- 2) gather + error ----------
async def demo_gather_error():
    try:
        await asyncio.gather(job("ok", 0.01), job("bad", 0.02, fail=True), job("ok2", 0.03))
    except ValueError as e:
        return f"pehla error bahar aaya: {e}"

print("\n" + asyncio.run(demo_gather_error()))

# ---------- 3) gather(return_exceptions=True) ----------
async def demo_gather_safe():
    results = await asyncio.gather(
        job("ok", 0.01), job("bad", 0.02, fail=True), job("ok2", 0.03),
        return_exceptions=True,
    )
    return [r if not isinstance(r, Exception) else f"<{type(r).__name__}: {r}>" for r in results]

print("return_exceptions=True ->")
for r in asyncio.run(demo_gather_safe()):
    print("   ", r)
"""))

A(code(r"""
import asyncio, time

async def job(name, delay):
    await asyncio.sleep(delay)
    return name

# ---------- 4) as_completed: jo pehle khatam ho, wo pehle mile ----------
async def demo_as_completed():
    t0 = time.perf_counter()
    order = []
    aws = [job("slow", 0.06), job("fast", 0.01), job("mid", 0.03)]
    for fut in asyncio.as_completed(aws):
        result = await fut
        order.append((result, round(time.perf_counter() - t0, 2)))
        print(f"   mila: {result:<5} @ {order[-1][1]}s  <- foran process kar sakte ho")
    return [o[0] for o in order]

print("as_completed (completion order):")
finish_order = asyncio.run(demo_as_completed())
assert set(finish_order) == {"slow", "fast", "mid"}      # sab aaye
assert finish_order[0] == "fast"                          # sab se tez pehle
print("order:", finish_order)

# ---------- 5) wait: manual control ----------
async def demo_wait():
    tasks = [asyncio.create_task(job(n, d)) for n, d in
             [("slow", 0.08), ("fast", 0.01), ("mid", 0.04)]]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    first = [t.result() for t in done]
    # ab pending ko cancel karo (ya await karo) -- warna 'orphan tasks' rah jaate hain
    for t in pending:
        t.cancel()
    await asyncio.gather(*pending, return_exceptions=True)   # cancellation settle hone do
    return first, len(pending)

first, n_pending = asyncio.run(demo_wait())
print("\nwait(FIRST_COMPLETED) -> pehla mila:", first, "| cancel kiye:", n_pending)
print("NOTE: asyncio.wait ko Tasks do (3.12+ me coroutines allowed nahi).")
"""))

A(md("""
### Output ka matlab
- `gather` ne **input order** me results diye (chahe fast pehle khatam hua).
- `as_completed` ne **completion order** me diye — is liye pehla result ~0.01s par hi mil gaya.
- `wait(FIRST_COMPLETED)` ne pehla mukammal task diya aur baaqi ko humne khud cancel kiya.

### Gotchas
- `gather` error par baaqi tasks ko **cancel nahi** karta (wo chupke chalte rehte hain) —
  yehi `TaskGroup` ki paidaish ki wajah hai.
- `wait` exceptions raise nahi karta; `done` set me se `task.exception()` khud check karo.
- `pending` tasks ko cancel/await karna **lazmi** hai warna "Task was destroyed but it is pending!" warning.

### Interview tip
*"`gather` collects results in input order and propagates the first exception without cancelling
siblings; `TaskGroup` gives structured concurrency: any failure cancels the group and raises an
ExceptionGroup."*
"""))

A(md("""
---
## 6. `TaskGroup` — structured concurrency (modern default, 3.11+)

### Kya hai
```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(job1())
    tg.create_task(job2())
# yahan pahunchne ka matlab: SAB tasks mukammal (ya group fail hua)
```

### Kyun behtar hai `gather` se
1. **Koi orphan task nahi** — block se bahar aane par sab settle ho chuke hote hain.
2. **Error propagation saaf** — ek task fail hua to baaqi **cancel** ho jaate hain
   aur `ExceptionGroup` uthta hai (`except*` se pakro).
3. **Nesting** natural hai — parent group child groups ka zimma leta hai (structured concurrency).

### Gotcha
Group ke andar exception ke baad naya `tg.create_task()` allowed nahi. Aur `except*` syntax naya hai
(`except*` sirf `ExceptionGroup` ke sath).
"""))

A(code(r"""
import asyncio

async def job(name, delay, fail=False):
    try:
        await asyncio.sleep(delay)
        if fail:
            raise ValueError(f"{name} kharab")
        return name
    except asyncio.CancelledError:
        print(f"   [{name}] cancel hua (group ki wajah se)")
        raise

# ---------- 1) sab kaamyab ----------
async def all_ok():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(job("a", 0.02))
        t2 = tg.create_task(job("b", 0.01))
        t3 = tg.create_task(job("c", 0.03))
    # yahan aane ka matlab: teeno mukammal
    return [t1.result(), t2.result(), t3.result()]

print("TaskGroup sab ok:", asyncio.run(all_ok()))

# ---------- 2) ek fail -> baaqi cancel + ExceptionGroup ----------
async def one_fails():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(job("quick", 0.01))
            tg.create_task(job("bad", 0.02, fail=True))
            tg.create_task(job("long", 0.50))       # ye cancel ho jayega
    except* ValueError as eg:                        # except* -> ExceptionGroup ke liye
        return [str(e) for e in eg.exceptions]

print("\nek task fail hua:")
print("pakre gaye errors:", asyncio.run(one_fails()))

# ---------- 3) kai tasks fail -> sab errors ek group me ----------
async def many_fail():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(job("x", 0.01, fail=True))
            tg.create_task(job("y", 0.02, fail=True))
    except* ValueError as eg:
        return len(eg.exceptions), [str(e) for e in eg.exceptions]

n, msgs = asyncio.run(many_fail())
print("\nkai fail ->", n, "errors:", msgs)
print("Dekha? gather sirf PEHLA error deta, TaskGroup ne SAB diye (aur baaqi cancel kiye).")

# ---------- 4) mukhtalif exception types ko alag alag pakarna ----------
async def mixed():
    async def boom_type():
        await asyncio.sleep(0.01); raise TypeError("type wala")
    async def boom_value():
        await asyncio.sleep(0.01); raise ValueError("value wala")
    caught = []
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(boom_type())
            tg.create_task(boom_value())
    except* TypeError as eg:
        caught.append(("TypeError", [str(e) for e in eg.exceptions]))
    except* ValueError as eg:
        caught.append(("ValueError", [str(e) for e in eg.exceptions]))
    return caught

print("\nmixed errors:", asyncio.run(mixed()))
"""))

A(md("""
### Output ka matlab
- Pehle case me teeno tasks mukammal hue.
- Doosre case me `bad` fail hua → `long` ko cancel kiya gaya (uska cancel message print hua) —
  yaani koi task background me lawaris nahi bacha.
- `except*` ne ek hi group me se **saare** matching errors diye, aur mixed case me
  types ke hisaab se alag alag handle hue.

### Interview tip
*"TaskGroup implements structured concurrency: the `async with` block cannot exit until every child
task finishes; a failure cancels siblings and surfaces as an ExceptionGroup handled with `except*`."*
"""))

A(md("""
---
## 7. Timeouts — `asyncio.timeout` aur `wait_for`

### Do tareeqe
```python
# 1) Modern (3.11+): context manager -- kai statements ko ek sath timeout do
async with asyncio.timeout(2.0):
    await step_one()
    await step_two()          # 2 second POORE block ke liye hai

# 2) Purana / per-call: wait_for
result = await asyncio.wait_for(step_one(), timeout=2.0)
```

### Ahem
- Dono **`TimeoutError`** raise karte hain (3.11+ me `asyncio.TimeoutError` = builtin `TimeoutError`).
- Timeout andar ke task ko **cancel** karta hai — is liye cleanup `try/finally` me likho.
- `asyncio.timeout_at(loop.time() + 5)` absolute deadline ke liye.
- **Har network/external call par timeout lagao** — warna hang forever ka risk.
"""))

A(code(r"""
import asyncio, time

async def slow_api(delay, name="api"):
    try:
        await asyncio.sleep(delay)
        return f"{name} ka data"
    finally:
        # cancellation par bhi ye chalta hai -> resource cleanup ki sahi jagah
        pass

# ---------- 1) wait_for ----------
async def demo_wait_for():
    out = []
    out.append(await asyncio.wait_for(slow_api(0.02), timeout=0.20))     # waqt par
    try:
        await asyncio.wait_for(slow_api(1.0), timeout=0.05)              # der ho gayi
    except TimeoutError:
        out.append("TimeoutError (wait_for) -> underlying task cancel ho gaya")
    return out

for line in asyncio.run(demo_wait_for()):
    print("wait_for:", line)

# ---------- 2) asyncio.timeout: poore block par ----------
async def demo_timeout_block():
    out = []
    async with asyncio.timeout(0.30):            # teen step mila kar 0.3s me hone chahiye
        out.append(await slow_api(0.05, "step1"))
        out.append(await slow_api(0.05, "step2"))
        out.append(await slow_api(0.05, "step3"))
    return out

print("\ntimeout block ke andar:", asyncio.run(demo_timeout_block()))

async def demo_timeout_exceeded():
    try:
        async with asyncio.timeout(0.06):
            await slow_api(0.02, "a")
            await slow_api(0.02, "b")
            await slow_api(0.50, "c")            # yahan budget khatam
    except TimeoutError:
        return "block ka total budget khatam -> TimeoutError"

print("timeout exceeded  :", asyncio.run(demo_timeout_exceeded()))

# ---------- 3) timeout ke sath fallback (asli service pattern) ----------
async def fetch_with_fallback(delay, budget=0.05):
    try:
        async with asyncio.timeout(budget):
            return await slow_api(delay, "primary")
    except TimeoutError:
        return "cached/fallback value"

async def main():
    return [await fetch_with_fallback(0.01), await fetch_with_fallback(1.0)]

print("\nfallback pattern:", asyncio.run(main()))

# ---------- 4) deadline extend karna (rare, magar useful) ----------
async def demo_reschedule():
    async with asyncio.timeout(0.05) as cm:
        await asyncio.sleep(0.02)
        cm.reschedule(asyncio.get_running_loop().time() + 0.20)   # deadline barha di
        await asyncio.sleep(0.10)
        return "extended deadline ke sath mukammal"

print("reschedule      :", asyncio.run(demo_reschedule()))
"""))

A(md("""
### Output ka matlab
`wait_for` ne ek call par timeout lagaya; `asyncio.timeout` ne **poore block** par budget lagaya
(teen steps ka jama waqt). Fallback pattern ne timeout ko error ki jagah **degraded response** bana diya.

### Gotchas
- `wait_for` andar wale coroutine ko cancel karta hai — agar wo cancellation ko `except CancelledError: pass`
  se nigal le to timeout "kaam nahi karta" lagta hai. **CancelledError ko kabhi chup-chaap na nigalo.**
- `asyncio.timeout` sirf `async with` me chalta hai (sync code me nahi).
- Timeout ka matlab "kaam ruk gaya" nahi — sirf "hum ne intezar chhor diya". Server par kaam
  ho sakta hai chal raha ho (idempotency ka khayal rakho).

### Interview tip
*"Use `asyncio.timeout` for a deadline over a block and `wait_for` for a single awaitable;
both cancel the inner operation and raise `TimeoutError`."*
"""))

A(md("""
---
## 8. Cancellation aur `CancelledError` ke sath cleanup

### Kya hai
`task.cancel()` andar chalne wale coroutine ke **agle `await` point** par `CancelledError`
"inject" karta hai. Ye ek **BaseException** hai (3.8+) — yaani `except Exception` se **nahi** pakri jaati
(jaan boojh kar, taake galti se na dabai jaye).

### Sahi cleanup ka tareeqa
```python
try:
    await long_work()
except asyncio.CancelledError:
    ...             # apna cleanup
    raise           # <-- LAZMI: dobara raise karo
finally:
    release()       # cancellation aur normal exit dono par chalta hai
```

### `shield`
`asyncio.shield(aw)` us awaitable ko bahar ki cancellation se bachata hai
(e.g. "payment commit ho hi jaye chahe client chala jaye") — magar sambhal kar,
kyunki tumhara wait cancel ho jata hai aur kaam background me chalta rehta hai.
"""))

A(code(r"""
import asyncio

EVENTS = []

async def worker(name):
    EVENTS.append(f"{name}:start")
    try:
        while True:
            await asyncio.sleep(0.01)          # cancellation yahan inject hoti hai
            EVENTS.append(f"{name}:tick")
    except asyncio.CancelledError:
        EVENTS.append(f"{name}:cancelled")     # cleanup ki jagah
        raise                                   # LAZMI: dobara raise
    finally:
        EVENTS.append(f"{name}:cleanup")        # hamesha chalta hai

async def demo_cancel():
    t = asyncio.create_task(worker("w1"))
    await asyncio.sleep(0.035)                  # thora chalne do
    t.cancel("client chala gaya")               # cancel karo (message optional)
    try:
        await t                                 # cancellation ka intezar
    except asyncio.CancelledError:
        EVENTS.append("main:cancel confirm")
    return t.cancelled()

was_cancelled = asyncio.run(demo_cancel())
print("task.cancelled():", was_cancelled)
print("events:", EVENTS)
assert "w1:cleanup" in EVENTS and "w1:cancelled" in EVENTS

# ---- BURI aadat: CancelledError ko nigal jana ----
EVENTS.clear()
async def stubborn():
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        EVENTS.append("cancel ignore kiya")     # BAD: raise nahi kiya
        return "main to chalta rahunga"         # cancellation 'fail' ho gayi

async def demo_stubborn():
    t = asyncio.create_task(stubborn())
    await asyncio.sleep(0.01)
    t.cancel()
    result = await t                            # exception nahi -- normal result!
    return result, t.cancelled()

res, cancelled = asyncio.run(demo_stubborn())
print("\nstubborn task ->", res, "| cancelled?", cancelled)
print("Sabaq: CancelledError nigalne se timeouts/shutdown TOOT jaate hain. Cleanup karo, phir raise karo.")
"""))

A(code(r"""
import asyncio

# ---- shield: critical kaam ko cancellation se bachana ----
LOG = []

async def critical_commit():
    LOG.append("commit start")
    await asyncio.sleep(0.05)
    LOG.append("commit done")           # ye har haal me hona chahiye
    return "committed"

async def demo_shield():
    inner = asyncio.create_task(critical_commit())
    try:
        # 0.02s me hamara intezar cancel ho jayega, magar kaam nahi
        await asyncio.wait_for(asyncio.shield(inner), timeout=0.02)
    except TimeoutError:
        LOG.append("wait cancel hua (magar commit chal raha hai)")
    result = await inner                # shielded task ab bhi zinda hai
    return result

print("shield result:", asyncio.run(demo_shield()))
print("log:", LOG)

# ---- graceful shutdown pattern: sab tasks ko theek se band karo ----
async def service(name, stop_event):
    count = 0
    try:
        while not stop_event.is_set():
            await asyncio.sleep(0.01)
            count += 1
        return f"{name} ne {count} ticks ke baad safai se band kiya"
    finally:
        pass

async def graceful_main():
    stop = asyncio.Event()
    tasks = [asyncio.create_task(service(f"svc{i}", stop)) for i in range(3)]
    await asyncio.sleep(0.05)
    stop.set()                          # sab ko "band ho jao" ka signal (cancel se behtar)
    return await asyncio.gather(*tasks)

print("\ngraceful shutdown:")
for line in asyncio.run(graceful_main()):
    print("  ", line)

# ---- current task ko cancel-safe banana ----
async def cancel_aware():
    task = asyncio.current_task()
    print("\ncurrent task ka naam:", task.get_name())
    print("cancelling?", task.cancelling())        # 3.11+: kitni dafa cancel request hui
    return "ok"

asyncio.run(cancel_aware())
"""))

A(md("""
### Output ka matlab
- `worker` cancel hone par bhi `finally` chala → resource leak nahi hua.
- `stubborn` ne `CancelledError` nigal liya → `task.cancelled()` **False**, cancellation nakaam.
  Yehi wo bug hai jis se `wait_for`/shutdown "kaam nahi karta".
- `shield` ne commit ko bachaya jab ke bahar wala wait timeout ho gaya.
- `Event` based shutdown cancellation se saaf hai — kaam beech me nahi kata.

### Interview tip
*"`CancelledError` derives from BaseException; catch it only to clean up and always re-raise.
Prefer cooperative shutdown via an Event, and use `shield` only for genuinely critical work."*
"""))
