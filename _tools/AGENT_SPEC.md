# Notebook Authoring Spec (sab authors ke liye lazmi)

ROOT = `c:\Users\Quonain\MyFiles\Artificial-Intelligence`

Tumhara kaam: `ROOT/<FOLDER>` ke andar Jupyter notebooks (`.ipynb`) banana — poore teaching content ke sath.
Target learner: Pakistani student jo interview prep + university syllabus ke liye zero se advance tak seekhna chahta hai.

## 1. Notebooks kaise banayein (JSON haath se NAHI likhni)

`ROOT/_tools/nbgen.py` helper use karo. Apni generator script(s) yahan rakho: `ROOT/_tools/gen/<kuch_naam>.py`

```python
import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

save(r"<FOLDER>/01_topic_ka_naam.ipynb", [
    md("""# Title ..."""),
    code("""print("hello")"""),
])
```

Phir chalao: `python _tools/gen/<kuch_naam>.py`

Rules:
- Ek script me 1 notebook (behtar) — script ~600-900 lines tak theek hai. Bohat lambi single script se bachna.
- `md()` / `code()` andar `textwrap.dedent` lagta hai: triple-quoted string ka content **column 0** se shuru karo warna indentation bigar jayegi.
- Markdown ke andar `\n` newlines normal likho. Code me backslash wale strings ke liye raw strings (`r"""..."""`) use karo.

## 2. Zubaan aur teaching style

- Explanation **Roman Urdu + English mix** me (jaise senior dev junior ko samjhata hai). Technical terms English me.
- Code ke andar comments bhi Roman Urdu/English mix — har ahem line par comment.
- Har concept ka pattern:
  1. **Kya hai** 2. **Kyun / kahan use hota hai** 3. **Syntax** 4. **Chalta hua example**
  5. **Output ka matlab** 6. **Common mistakes / gotchas** 7. **Interview tip**
- Minor se minor detail bhi cover karo — edge cases, gotchas, "yahan log phaste hain" wali baatein.

## 3. Har notebook ka structure

1. **Title cell** — topic, level, "Is notebook me kya seekhenge" bullet roadmap, prerequisites.
2. **Concept sections** — markdown explanation + code cell(s). Aage barhte hue difficulty.
3. **Common Mistakes / Gotchas** section.
4. **Real-World Problems** — 3-6 realistic problems, commented solutions.
5. **LeetCode Problems** section (LAZMI, har notebook me). Har problem ke liye:
   - Heading: `### LC <number>. <Exact Problem Title> — <Easy|Medium|Hard>`
   - Link: `https://leetcode.com/problems/<slug>/`
   - Problem ka short bayan Roman Urdu me
   - Approach / intuition step-by-step
   - **Time & Space complexity**
   - Code cell: function + inline comments + `assert` test cases jo chal kar pass hon
   - Jahan faida ho: brute force vs optimal dono
6. **Interview Questions & Answers** — 10-20 real interview Q&A (crisp answers).
7. **Practice Exercises (khud karo)** — 5-10 tasks with hints.
8. **Summary / Cheat-sheet** cell — quick revision table ya bullets.

## 4. Code rules (bohat zaroori)

- Har code cell **error ke baghair** chalna chahiye. Jo cell jaan boojh kar error dikhata hai use `try/except` me wrap kar ke `print` karo.
- `input()` **bilkul nahi**. Internet/network access **nahi**. Bahar ki data files par depend **nahi** — data inline banao (`list`, `dict`, `io.StringIO`, `tempfile`).
- `matplotlib` / `seaborn` install **nahi** hain → plotting code na likho.
- Available: Python 3.14, numpy 2.4, pandas 3.0 (stdlib sab kuch).
- Notebook top-to-bottom chalta hai: variable pehle define, phir use.
- Windows machine hai — file examples me `tempfile` use karo.
- Heavy compute na karo (har notebook total < ~30 second me chal jaye).

## 5. Verify (submit se pehle LAZMI)

```
cd "c:\Users\Quonain\MyFiles\Artificial-Intelligence"
python _tools/runnb.py "<FOLDER>"     # sab [pass] hona chahiye
python _tools/validate.py             # JSON/structure check
```
Fail hone par theek karo aur dobara chalao. Jab tak apne folder ke saare notebooks `[pass]` na hon, kaam mukammal nahi.
(validate.py dusre authors ki files bhi dikhata hai — sirf apni parwah karo.)

## 6. Boundaries

- Sirf apne `<FOLDER>` me aur `ROOT/_tools/gen/` me likho.
- Dusre topic folders ya `_tools/*.py` (nbgen/validate/runnb) ko **touch na karo**.
- File names exactly wahi rakho jo tumhein diye gaye hain.

## 7. Quality bar

- Har notebook **substantial**: kam az kam 40-70 cells, asli depth, chalte hue examples.
- Shallow / one-liner notebooks reject.
- Aakhir me short report do: kitne notebooks, kitne cells, kitne LeetCode problems cover hue.
