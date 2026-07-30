import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ============================================================================
# 1. TITLE
# ============================================================================
cells.append(md(r"""
# OOP in Python — 01: Introduction, Classes aur Objects

**Level:** Beginner (Foundation)

Yeh notebook OOP (Object-Oriented Programming) series ka pehla notebook hai. Yahan se
hum bilkul zero se shuru karein ge aur dheere dheere depth barhate jayenge. Yeh series
university syllabus aur job interviews — dono ke liye design ki gayi hai.

## Is notebook me kya seekhenge

- Procedural programming vs OOP — same problem dono tareeqon se solve kar ke farq dekhenge
- OOP ke 4 pillars ka overview (encapsulation, inheritance, polymorphism, abstraction)
- Class kya hoti hai, Object kya hota hai (blueprint analogy)
- `class` syntax aur `__init__` constructor
- `self` asal me hai kya — unbound call se proof
- Instance attributes vs Class attributes, aur mashhoor "shared mutable state" trap
- Runtime par attributes create/read/update/delete karna, `__dict__`, `vars()`, `dir()`
- Instance methods aur class ka namespace
- Multiple objects aur unki independence
- `del`, object lifecycle, `__new__` aur `__del__`
- Default vs parameterized constructor, aur Python me "constructor overloading"
- `__str__` vs `__repr__`
- Objects ko `list` / `dict` me store karna
- Real classes: Student, Book, Car
- 3 LeetCode problems (class-based solutions)
- Interview Q&A, practice exercises aur ek cheat-sheet

## Prerequisites

- Python basics: variables, functions, `if/else`, loops, `list`, `dict`
- Functions ko parameters ke sath likhna aana chahiye

Chalo shuru karte hain!
"""))

# ============================================================================
# 2. PROCEDURAL VS OOP
# ============================================================================
cells.append(md(r"""
## 1. Procedural Programming vs OOP

### Kya hai
- **Procedural programming**: Data (variables/dict/list) aur us par kaam karne wale
  **functions** alag alag hote hain. Har function ko manually data pass karna parta hai.
- **OOP (Object-Oriented Programming)**: Data aur us par kaam karne wale functions
  (methods) ek hi unit — **object** — ke andar bundle ho jate hain.

### Kyun / kahan use hota hai
Jab program chhota ho (ek do functions), procedural style aasan lagti hai. Lekin jaise
hi cheezein badhti hain (multiple accounts, multiple students, multiple cars) — procedural
style me har jagah data explicitly pass karna padta hai, aur bugs ka chance barh jata hai.
OOP is problem ko solve karta hai: **data + behavior ek jagah, object ke andar.**

Neeche hum **bank account** ka SAME problem dono tareeqon se solve karenge, taake farq
apni ankhon se dekh sako.
"""))

cells.append(code(r"""
# ---- PROCEDURAL STYLE ----
# Data (accounts) aur behavior (functions) bilkul alag hain.
# Har function ko "accounts" dictionary explicitly pass karni padti hai.

accounts = {}  # sab accounts yahan store honge: {acc_no: {"owner":..., "balance":...}}

def create_account(accounts, acc_no, owner, balance=0):
    # naya account ek nested dictionary ke tor par bana rahe hain
    accounts[acc_no] = {"owner": owner, "balance": balance}

def deposit(accounts, acc_no, amount):
    # deposit karne ke liye accounts dict + acc_no + amount, teeno chahiye
    accounts[acc_no]["balance"] += amount

def withdraw(accounts, acc_no, amount):
    # withdraw se pehle balance check karna zaroori hai
    if accounts[acc_no]["balance"] >= amount:
        accounts[acc_no]["balance"] -= amount
    else:
        print("Insufficient balance!")

def show_balance(accounts, acc_no):
    info = accounts[acc_no]
    print(f"[Procedural] Account {acc_no} ({info['owner']}) balance: {info['balance']}")

# Ab use karte hain -- har step par 'accounts' dict pass karni pad rahi hai
create_account(accounts, 101, "Ahmed", 5000)
deposit(accounts, 101, 2000)
withdraw(accounts, 101, 1000)
show_balance(accounts, 101)
"""))

cells.append(md(r"""
**Output ka matlab:** Account 101 ka final balance 5000 + 2000 - 1000 = **6000** print hua.

**Dikkat kya hai?** `accounts` dictionary ko har function call me manually pass karna
pad raha hai. Agar bhool gaye to bug. Data (`accounts`) aur behavior (`deposit`,
`withdraw`, ...) ka koi organic connection nahi — sirf convention se jura hua hai.
"""))

cells.append(code(r"""
# ---- OOP STYLE (same problem) ----
# Ab data (attributes) aur behavior (methods) ek hi "BankAccount" object ke andar hain.

class BankAccount:
    def __init__(self, acc_no, owner, balance=0):
        # yeh 3 attributes har object ke apne alag honge
        self.acc_no = acc_no
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # ab 'accounts' dict pass karne ki zaroorat nahi -- 'self' khud object hai
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient balance!")

    def show_balance(self):
        print(f"[OOP] Account {self.acc_no} ({self.owner}) balance: {self.balance}")

# Ab use karte hain -- object khud apna data carry karta hai
acc1 = BankAccount(101, "Ahmed", 5000)
acc1.deposit(2000)
acc1.withdraw(1000)
acc1.show_balance()
"""))

cells.append(md(r"""
### Comparison

| Cheez | Procedural | OOP |
|---|---|---|
| Data + behavior | Alag alag | Bundle (encapsulated) object ke andar |
| Data pass karna | Har function call me manually | `self` khud carry karta hai |
| Naye accounts | Naya dict entry + wahi functions | Bas naya object: `BankAccount(...)` |
| Readability | `withdraw(accounts, 101, 1000)` | `acc1.withdraw(1000)` — zyada natural |
| Scale karna | Mushkil hota jata hai | Objects naturally scale karte hain |

Yeh farq chhote program me itna nazar nahi aata, lekin jab project bada ho jaye
(multiple banks, multiple students, multiple cars...) to OOP ka faida saaf dikhta hai.
"""))

# ============================================================================
# 3. 4 PILLARS OVERVIEW
# ============================================================================
cells.append(md(r"""
## 2. OOP ke 4 Pillars — Overview

Yeh sirf ek **overview** hai — har pillar par ek pura alag notebook aage series me aayega.
Abhi bas itna samajh lo ke yeh chaar cheezein OOP ki jaan hain:

1. **Encapsulation** — Data (attributes) aur behavior (methods) ko ek object ke andar
   bundle karna, aur zaroorat ke mutabiq data ko "chhupana" (private/protected banana)
   taake bahar se galat tarah access na ho. Upar wali `BankAccount` class me `balance`
   ko `deposit`/`withdraw` methods ke zariye control kiya — yeh encapsulation hai.

2. **Inheritance** — Ek class doosri class ki properties/behavior "inherit" (virsay me)
   le sakti hai. Jaise `SavingsAccount` class `BankAccount` se inherit kare aur apna
   interest calculation feature add kare. (Detail agle notebooks me.)

3. **Polymorphism** — "Poly" = kayi, "morph" = shakl. Ek hi method name, alag alag
   classes me alag tarah behave kare. Jaise `show_balance()` har account type ke liye
   thora different tarike se print ho sakta hai.

4. **Abstraction** — Complex implementation ko chhupa kar sirf zaroori interface expose
   karna. Jaise `acc1.deposit(2000)` call karte waqt hume yeh nahi pata hona chahiye ke
   andar balance kaise update hota hai — bas interface use karte hain.

Yeh chaaron pillars is series ke agay ke notebooks me detail se cover honge. Abhi hum
sirf **Classes aur Objects** ki foundation banayenge.
"""))

# ============================================================================
# 4. CLASS VS OBJECT — BLUEPRINT ANALOGY
# ============================================================================
cells.append(md(r"""
## 3. Class vs Object — Blueprint Analogy

### Kya hai
- **Class** = Blueprint / naqsha (jaise ghar ka design naqsha, ya cookie cutter).
- **Object** = Us blueprint se bana hua **actual cheez** (jaise us naqshe se bana hua
  ghar, ya us cutter se bani hui cookie).

Ek blueprint se **kayi ghar** ban sakte hain — har ghar apni jagah alag hoga (address,
rang, andar ka saman), lekin structure (kamre, darwaze) same design follow karega.
Yehi cheez class aur object ke beech hoti hai.

### Kyun / kahan use hota hai
Jab bhi ek "type" ki kayi cheezein banani hon jo similar structure follow karti hon
(students, cars, books, employees...) — class banate hain, phir us se jitne chahen
utne objects banate hain.
"""))

cells.append(code(r"""
# Blueprint (class): "Dog" jaisi har cheez ka structure define karta hai
class Dog:
    def __init__(self, name, breed):
        self.name = name    # har dog ka apna naam
        self.breed = breed  # har dog ki apni breed

    def bark(self):
        print(f"{self.name} ({self.breed}) keh raha hai: Bhow Bhow!")

# Ab isi ek blueprint se do ALAG objects (actual dogs) bana rahe hain
dog1 = Dog("Tommy", "Bulldog")
dog2 = Dog("Bruno", "Labrador")

dog1.bark()
dog2.bark()

print(type(dog1))         # dono ki class same hai
print(dog1 is dog2)       # lekin dono alag alag objects hain (identity alag)
"""))

cells.append(md(r"""
**Output ka matlab:** `dog1` aur `dog2` dono `Dog` class ke instances (objects) hain —
`type(dog1)` yehi dikha raha hai (`<class '__main__.Dog'>`). Lekin `dog1 is dog2` ->
`False`, kyun ke yeh do bilkul separate memory locations me baithi cheezein hain, sirf
same blueprint follow kar rahi hain.

**Interview tip:** "Class is a blueprint, object is an instance of that blueprint" — yeh
ek-line definition har interview me expect ki jati hai. Ready rakho.
"""))

# ============================================================================
# 5. CLASS SYNTAX + __init__
# ============================================================================
cells.append(md(r"""
## 4. `class` Syntax aur `__init__` Constructor

### Kya hai
`class` keyword se class define hoti hai. `__init__` ek special method hai jise
**constructor** kehte hain — jab bhi naya object banta hai, `__init__` **automatically**
call hoti hai, taake object ko initial state (attributes) mil sake.

### Kyun / kahan use hota hai
Har naye object ko kuch initial data chahiye hota hai (jaise Student ka naam, roll_no).
`__init__` yeh guarantee deta hai ke object "half-banaya hua" (incomplete state) me
kabhi exist nahi karega.

### Syntax
```python
class ClassName:
    def __init__(self, param1, param2):
        self.attr1 = param1
        self.attr2 = param2

    def some_method(self):
        # method body
        ...

obj = ClassName(value1, value2)  # yeh call __init__ ko automatically trigger karta hai
```
"""))

cells.append(code(r"""
# Student class -- is poore notebook me hum isi class ko dheere dheere improve karenge

class Student:
    def __init__(self, name, roll_no, marks=None):
        # __init__ automatically chalta hai jab bhi "Student(...)" call hota hai
        self.name = name              # instance attribute: har student ka apna naam
        self.roll_no = roll_no        # instance attribute: apna roll number
        self.marks = marks if marks is not None else []  # default: khaali list

    def display(self):
        # yeh ek "instance method" hai -- 'self' se object ka data access karta hai
        print(f"Student: {self.name} | Roll No: {self.roll_no} | Marks: {self.marks}")

# Object banate hi __init__ automatically chal gaya
s1 = Student("Ayesha", 1, [85, 90, 78])
s1.display()

# marks na diye to default [] use hoga
s2 = Student("Bilal", 2)
s2.display()
"""))

cells.append(md(r"""
**Output ka matlab:** `s1` ke marks jo diye the wahi print hue. `s2` ke liye marks nahi
diye the, is liye `marks=None` default trigger hua aur andar khaali list `[]` set ho gayi.

### Common mistakes / gotchas
- `__init__` ka naam **exactly** `__init__` hona chahiye (double underscore dono taraf) —
  `_init_` ya `__init` likhne se yeh sirf ek normal method ban jayega, constructor nahi.
- `__init__` **kuch return nahi karta** (na hi `return self` likhna chahiye) — Python
  khud object return kar deta hai.
- Pehla parameter hamesha `self` hona chahiye (naam kuch bhi ho sakta hai technically,
  lekin convention `self` hi hai — isay tabdeel mat karo).

**Interview tip:** `__init__` ko "constructor" kaha jata hai lekin technically yeh
**initializer** hai — asal object creation `__new__` karta hai (aage dekhenge). Yeh
distinction interview me impress karta hai.
"""))

# ============================================================================
# 6. SELF EXPLAINED
# ============================================================================
cells.append(md(r"""
## 5. `self` Asal Me Hai Kya?

### Kya hai
`self` sirf ek convention-based naam hai jo us **object ka reference** hota hai jis par
method call ho raha hai. Jab tum `s1.display()` likhte ho, Python andar hi andar isay
`Student.display(s1)` me convert kar deta hai — `s1` khud-ba-khud `self` ban jata hai.

### Proof: Unbound call
Chalo isay khud prove karte hain — class ke through method ko seedha call kar ke, aur
object ko manually pehle argument ke tor par pass kar ke.
"""))

cells.append(code(r"""
# Normal (bound) call -- Python automatically s1 ko self bana deta hai
s1.display()

# Unbound call -- HUM khud object ko pehle argument ke tor par pass kar rahe hain
# Yeh PROOF hai ke 's1.display()' aur 'Student.display(s1)' bilkul same cheez hain
Student.display(s1)

print(s1.display == Student.display.__get__(s1))  # dono ek hi bound method hain
"""))

cells.append(md(r"""
**Output ka matlab:** Dono lines ka output bilkul same hai — kyun ke `s1.display()`
internally `Student.display(s1)` hi hai. `self` bas woh jagah hai jahan "kis object par
kaam ho raha hai" store hota hai.

### Common mistakes / gotchas
- `self` bhool jana ek method define karte waqt sab se common beginner mistake hai
  (neeche "Common Mistakes" section me dikhayenge).
- `Student.display()` **bina object pass kiye** call karoge to error aayega, kyun ke
  `display` ko pata hi nahi chalega "kis student" ka data print karna hai.

**Interview tip:** "self is not a keyword, it's just a naming convention" — is line ko
yaad rakho. Technically tum `self` ki jagah `this` ya kuch bhi naam use kar sakte ho,
lekin PEP8 convention `self` hi follow karti hai.
"""))

# ============================================================================
# 7. INSTANCE VS CLASS ATTRIBUTES + SHARED STATE TRAP
# ============================================================================
cells.append(md(r"""
## 6. Instance Attributes vs Class Attributes

### Kya hai
- **Instance attribute**: Har object ka apna alag copy hota hai (jaise `self.name`).
- **Class attribute**: Saari instances ke darmiyan **shared** hota hai — class ke level
  par define hota hai, `self.` ke bajaye seedha class body me.

### Kyun / kahan use hota hai
Class attribute tab use hota hai jab koi value saari instances me **common** honi
chahiye — jaise school ka naam (har student same school me hai), ya total objects ka
counter.

### Syntax
```python
class ClassName:
    class_attr = "shared value"   # class attribute -- sab instances share karte hain

    def __init__(self, x):
        self.instance_attr = x    # instance attribute -- har object ka apna
```
"""))

cells.append(code(r"""
class Student:
    school_name = "Bizee Grammar School"  # CLASS attribute -- sab students shared karte hain

    def __init__(self, name, roll_no, marks=None):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks if marks is not None else []

    def display(self):
        # self.school_name likhne se pehle instance me dhoonda jata hai, na mile to class me
        print(f"{self.name} (Roll {self.roll_no}) -> School: {self.school_name}")

s1 = Student("Ayesha", 1)
s2 = Student("Bilal", 2)

s1.display()
s2.display()

# Class attribute ko class ke through change karo -> SABHI instances par asar hoga
Student.school_name = "Bizee Model School"
s1.display()
s2.display()
"""))

cells.append(md(r"""
**Output ka matlab:** Jab humne `Student.school_name` badla (class ke through), dono
`s1` aur `s2` ka school naam change ho gaya — kyun ke yeh attribute unke apne `__dict__`
me nahi, balke **class ke** `__dict__` me hai, aur wahi se shared hota hai.
"""))

cells.append(md(r"""
### Shared-State Trap (Mutable Class Attribute) — Bohat Common Bug!

Yahan asli khatra hai: agar class attribute **mutable** ho (jaise `list` ya `dict`), to
sab instances usi **ek** object ko share karte hain — aur ek instance ka change sab par
asar dalta hai. Yeh ek bohat common real-world bug hai.
"""))

cells.append(code(r"""
# ---- BUGGY VERSION ----
class TeamBuggy:
    members = []  # DANGER: yeh ek SHARED mutable list hai (class attribute)

    def __init__(self, team_name):
        self.team_name = team_name

    def add_member(self, name):
        self.members.append(name)  # yeh 'self.members' likh rahe hain, lekin list SHARED hai

team_a = TeamBuggy("Alpha")
team_b = TeamBuggy("Beta")

team_a.add_member("Ahmed")
team_b.add_member("Sara")

# Expected: team_a sirf 'Ahmed' rakhe, team_b sirf 'Sara' -- lekin dono ke members SAME hain!
print("team_a.members:", team_a.members)
print("team_b.members:", team_b.members)
print("Same list object?", team_a.members is team_b.members)  # True -- yehi bug ki jarh hai
"""))

cells.append(code(r"""
# ---- FIXED VERSION ----
class TeamFixed:
    def __init__(self, team_name):
        self.team_name = team_name
        self.members = []  # FIX: mutable data ko hamesha __init__ ke andar, self. ke sath banao

    def add_member(self, name):
        self.members.append(name)

team_a = TeamFixed("Alpha")
team_b = TeamFixed("Beta")

team_a.add_member("Ahmed")
team_b.add_member("Sara")

print("team_a.members:", team_a.members)   # sirf Ahmed
print("team_b.members:", team_b.members)   # sirf Sara
print("Same list object?", team_a.members is team_b.members)  # ab False
"""))

cells.append(md(r"""
### Common mistakes / gotchas
- **Kabhi bhi mutable default** (list, dict, set) class attribute ke tor par mat banao
  agar tum chahte ho har instance apna alag copy rakhe. Hamesha `__init__` ke andar
  `self.attr = []` likho.
- Immutable class attributes (str, int, tuple) safe hain kyun ke unhe "modify" nahi
  kiya ja sakta — sirf naya value assign hota hai (jo instance-level attribute ban jata
  hai, class-level ko touch nahi karta).
- `self.x = value` likhne se **naya instance attribute** ban jata hai (agar pehle se
  class attribute `x` maujood ho to woh us instance ke liye "shadow"/hide ho jata hai).

**Interview tip:** "Mutable default class attributes are shared across all instances" —
yeh ek classic Python gotcha interview question hai. Isay `__init__` ke sath fix karna
dikhana hamesha impress karta hai.
"""))

# ============================================================================
# 8. RUNTIME ATTRIBUTE CRUD + __dict__ / vars() / dir()
# ============================================================================
cells.append(md(r"""
## 7. Runtime Par Attributes Create / Read / Update / Delete Karna

### Kya hai
Python me attributes **sirf `__init__` tak mehdood nahi** — tum kabhi bhi, kahin bhi
(runtime par) object me naya attribute add kar sakte ho, purana update kar sakte ho, ya
`del` se hata sakte ho.

- `obj.__dict__` — object ke saare instance attributes ek dictionary ki tarah dikhata hai
- `vars(obj)` — `obj.__dict__` jaisa hi hai (thora zyada "proper" tareeqa)
- `dir(obj)` — object ke saare attributes + methods (inherited samet) ki list deta hai
"""))

cells.append(code(r"""
student = Student("Hina", 5)

# CREATE: naya attribute runtime par add kar rahe hain (__init__ me define nahi tha)
student.email = "hina@example.com"
print("Create ke baad:", student.__dict__)

# READ
print("Read email:", student.email)

# UPDATE: maujooda attribute ki value badal rahe hain
student.email = "hina.updated@example.com"
print("Update ke baad:", student.email)

# DELETE
del student.email
print("Delete ke baad __dict__:", student.__dict__)

# ab email access karne ki koshish -> AttributeError (kyun ke hata diya)
try:
    print(student.email)
except AttributeError as e:
    print("Error pakra gaya:", e)
"""))

cells.append(code(r"""
student = Student("Hina", 5)
student.email = "hina@example.com"

print("vars(student):", vars(student))          # __dict__ jaisa hi
print("vars == __dict__ ?", vars(student) is student.__dict__)

# dir() bohat zyada cheezein dikhata hai (methods, dunder methods, sab) -- yahan
# hum sirf woh names dikha rahe hain jo '_' se shuru nahi hote (readable subset)
public_names = [name for name in dir(student) if not name.startswith("_")]
print("dir() ka readable subset:", public_names)
"""))

cells.append(md(r"""
**Output ka matlab:** `__dict__` sirf **instance** attributes dikhata hai (jo `self.x =`
se bane hon). `dir()` bohat zyada cheezein deta hai — instance attributes, class
attributes, aur inherited dunder methods (`__init__`, `__str__`, waghera) sab.

### Common mistakes / gotchas
- `vars(obj)` aur `obj.__dict__` **same dictionary object** return karte hain — is ko
  directly modify karna (`vars(obj)['x'] = 1`) technically kaam karta hai lekin **best
  practice nahi** hai. Hamesha `obj.x = 1` likho.
- `dir()` class attributes bhi dikhata hai, sirf instance attributes nahi — is farq ko
  confuse mat karo `__dict__` ke sath.

**Interview tip:** "How do you check what attributes an object has at runtime?" ->
`vars(obj)` ya `obj.__dict__` ka jawab do (instance ke liye), `dir(obj)` mention karo
poori list (methods samet) ke liye.
"""))

# ============================================================================
# 9. INSTANCE METHODS + CLASS NAMESPACE
# ============================================================================
cells.append(md(r"""
## 8. Instance Methods aur Class ka Namespace

### Kya hai
**Instance methods** woh functions hain jo class ke andar define hote hain aur pehla
parameter `self` lete hain — yeh object ke data par kaam karte hain. Class khud ek
**namespace** hai — uske andar defined saari cheezein (methods, class attributes)
`ClassName.__dict__` me store hoti hain.

Jab tum `obj.method_name` likhte ho, Python attribute lookup is order me karta hai:
1. Pehle `obj.__dict__` me dhoondta hai (instance attributes)
2. Na mile to `type(obj).__dict__` me dhoondta hai (class attributes/methods)
3. Phir parent classes me (inheritance chain — MRO)
"""))

cells.append(code(r"""
class Student:
    school_name = "Bizee Grammar School"

    def __init__(self, name, roll_no, marks=None):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks if marks is not None else []

    def display(self):
        print(f"{self.name} (Roll {self.roll_no}) -> Marks: {self.marks}")

    def add_marks(self, value):
        # instance method: object ke apne 'marks' list ko update karta hai
        self.marks.append(value)

# Class ka namespace -- 'display' aur 'add_marks' yahan dikhengi (methods)
class_level_names = [n for n in Student.__dict__ if not n.startswith("__")]
print("Student class ke apne namespace me:", class_level_names)

s1 = Student("Ayesha", 1)
s1.add_marks(88)
s1.add_marks(92)
s1.display()

# 'add_marks' instance ke __dict__ me NAHI hai -- yeh class ke __dict__ me hai
print("'add_marks' in s1.__dict__?", "add_marks" in s1.__dict__)
print("'add_marks' in Student.__dict__?", "add_marks" in Student.__dict__)
"""))

cells.append(md(r"""
**Output ka matlab:** `add_marks` method **class** ke namespace me rehta hai, har
instance ke `__dict__` me nahi — warna har object apna separate copy of the function
rakhta, jo memory waste hoti. Sab instances **wahi ek** method share karte hain, sirf
`self` ke through pata chalta hai kis object par chalana hai.

**Interview tip:** "Methods live on the class, not on the instance" — is se Python ki
memory efficiency samajh aati hai (1000 students banao, `add_marks` function sirf
**ek baar** memory me hoga, har object me nahi).
"""))

# ============================================================================
# 10. MULTIPLE OBJECTS INDEPENDENCE
# ============================================================================
cells.append(md(r"""
## 9. Multiple Objects aur Unki Independence

### Kya hai
Har object apna **alag instance state** rakhta hai. Ek object ka data change karne se
doosre object par koi asar nahi padta (jab tak woh mutable class attribute na ho, jo
humne upar dekha).
"""))

cells.append(code(r"""
s1 = Student("Ayesha", 1)
s2 = Student("Bilal", 2)

s1.add_marks(90)
s1.add_marks(85)

s2.add_marks(70)

# s1 aur s2 ke marks bilkul independent hain
print("s1 marks:", s1.marks)
print("s2 marks:", s2.marks)

assert s1.marks == [90, 85]
assert s2.marks == [70]
assert s1.marks != s2.marks
print("\nProof: dono objects ka 'marks' apna alag list hai (independent state)")
print("s1.marks is s2.marks ->", s1.marks is s2.marks)
"""))

cells.append(md(r"""
**Interview tip:** "Each object has its own copy of instance attributes, but shares
class attributes and methods" — yeh ek line pura is section ka essence hai.
"""))

# ============================================================================
# 11. DEL, OBJECT LIFECYCLE, __new__, __del__
# ============================================================================
cells.append(md(r"""
## 10. `del`, Object Lifecycle, `__new__` aur `__del__`

### Kya hai
Object ki poori zindagi (lifecycle) teen phases me hoti hai:
1. **Creation**: `__new__` call hota hai — yeh **memory allocate** karta hai aur
   khaali (raw) object return karta hai.
2. **Initialization**: `__new__` ke turant baad `__init__` call hota hai — yeh object ko
   values se initialize karta hai.
3. **Destruction**: Jab object ka koi reference baaki nahi bachta (reference count 0 ho
   jata hai), CPython usay garbage collect kar deta hai aur `__del__` call hota hai.

`del obj` khud object ko delete **nahi** karta — yeh sirf `obj` naam (reference) ko
hata deta hai. Agar woh **aakhri** reference thi, to object garbage collect ho jata hai
aur `__del__` chal jata hai.

### Syntax
```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)   # asal memory allocation
        return instance

    def __init__(self, ...):
        ...   # initialization

    def __del__(self):
        ...   # cleanup jab object destroy ho raha ho
```
"""))

cells.append(code(r"""
class Resource:
    def __new__(cls, *args, **kwargs):
        # __new__ pehle chalta hai -- yeh object ka memory allocate karta hai
        print("[1] __new__ chal raha hai -> memory allocate ho rahi hai")
        instance = super().__new__(cls)
        return instance

    def __init__(self, name):
        # __new__ ke baad __init__ chalta hai -- yeh object ko initialize karta hai
        print(f"[2] __init__ chal raha hai -> '{name}' initialize ho raha hai")
        self.name = name

    def __del__(self):
        # jab object ka koi reference nahi bachta, yeh cleanup ke waqt chalta hai
        print(f"[3] __del__ chal raha hai -> '{self.name}' object destroy ho raha hai")

r = Resource("TempConnection")
print("Object ban gaya, ab hum 'del r' karte hain:")
del r   # yeh 'r' naam hata deta hai -- kyun ke yeh aakhri reference thi, __del__ chal jata hai
print("del ke baad 'r' variable ab exist nahi karta")
"""))

cells.append(md(r"""
**Output ka matlab:** Order dekho — `__new__` -> `__init__` -> (kaam) -> `del r` ke baad
`__del__`. Yeh object ki poori lifecycle hai.

### Common mistakes / gotchas
- `__del__` par **bharosa mat karo** critical cleanup (jaise file close karna, database
  connection band karna) ke liye — CPython me refcounting se yeh usually turant chal
  jata hai, lekin **doosre Python implementations** (PyPy waghera) me timing guaranteed
  nahi hoti. Critical cleanup ke liye `with` statement / context managers use karo.
- `del obj` sirf reference hataata hai — agar object ka koi aur reference (list, dict,
  doosra variable) maujood hai, to `__del__` turant **nahi** chalega.
- `__new__` bohat kam khud likhna padta hai — zyada tar normal classes me sirf
  `__init__` hi kaafi hota hai. `__new__` zyada tar immutable types (`str`, `tuple`) ke
  subclassing ya metaclasses me use hota hai.

**Interview tip:** "`__new__` creates the object, `__init__` initializes it" — is farq
ko clearly explain kar sako to yeh mid-level+ interview me achha impression deta hai.
"""))

# ============================================================================
# 12. DEFAULT VS PARAMETERIZED CONSTRUCTOR + CLASSMETHOD FACTORIES
# ============================================================================
cells.append(md(r"""
## 11. Default vs Parameterized Constructor, aur "Constructor Overloading"

### Kya hai
- **Default constructor**: Jab `__init__` ko koi bhi extra arguments na diye jayein
  (ya sab ke default values ho).
- **Parameterized constructor**: Jab `__init__` explicit values leta hai.

### Kyun / kahan use hota hai
Java/C++ me class ke **multiple `__init__`-jaise constructors** (overloading) ban sakte
hain. **Python ismein alag hai** — Python me ek class ka sirf **ek** `__init__` ho sakta
hai. Iska Pythonic solution do tareeqon se hota hai:
1. **Default arguments** — `def __init__(self, name, marks=None)`
2. **`@classmethod` factory methods** — alternate "constructors" jo `cls(...)` call
   karke object banate hain, alag alag input formats ke liye.
"""))

cells.append(code(r"""
class Student:
    school_name = "Bizee Grammar School"

    def __init__(self, name, roll_no, marks=None):
        # Default constructor jaisa istemal: Student() bhi chal sakta hai (sab defaults)
        # Parameterized: Student("Ali", 3, [90, 85])
        self.name = name
        self.roll_no = roll_no
        self.marks = marks if marks is not None else []

    def add_marks(self, value):
        self.marks.append(value)

    @classmethod
    def from_string(cls, csv_line):
        # yeh ek "alternate constructor" hai -- CSV jaisi string se Student banata hai
        # e.g. "Bilal,3,90-85-77"
        name, roll_no, marks_str = csv_line.split(",")
        marks = [int(m) for m in marks_str.split("-")] if marks_str else []
        return cls(name, int(roll_no), marks)  # cls(...) == Student(...) yahan

    @classmethod
    def new_blank(cls, name):
        # ek aur factory -- sirf naam se student banao, roll_no baad me set hoga
        return cls(name, roll_no=0)

    def display(self):
        print(f"{self.name} (Roll {self.roll_no}) -> Marks: {self.marks}")

# 1) "default-ish" constructor -- marks nahi diye
s1 = Student("Sara", 4)

# 2) parameterized constructor -- sab kuch explicit
s2 = Student("Ali", 3, [90, 85])

# 3) classmethod factory -- CSV string se banaya
s3 = Student.from_string("Bilal,7,90-85-77")

# 4) classmethod factory -- sirf naam se banaya
s4 = Student.new_blank("Zara")

for s in (s1, s2, s3, s4):
    s.display()

assert s3.name == "Bilal" and s3.roll_no == 7 and s3.marks == [90, 85, 77]
assert s4.roll_no == 0
print("\nSab factory methods ne sahi objects banaye -- asserts pass!")
"""))

cells.append(md(r"""
**Output ka matlab:** `Student.from_string(...)` aur `Student.new_blank(...)` dono
`Student` ke **naye objects** hi bana rahe hain, bas alag input format se — yehi
"Pythonic constructor overloading" hai.

### Common mistakes / gotchas
- Python me `def __init__` do dafa likhna **error nahi** dega, lekin doosri definition
  pehli ko **overwrite** kar degi (Java jaisi overloading nahi hoti). Isliye classmethods
  ka tareeqa use karo.
- `@classmethod` ka pehla parameter `cls` hota hai (class khud), `self` (instance) nahi.
- Mutable default argument (`marks=[]`) likhna **wahi shared-state trap** hai jo humne
  upar dekha — isliye `marks=None` likh kar andar `if marks is not None else []` karte
  hain.

**Interview tip:** "Python doesn't support method/constructor overloading like Java —
we simulate it using default arguments and `@classmethod` factory methods." Yeh answer
bohat common interview question ka perfect jawab hai.
"""))

# ============================================================================
# 13. __str__ VS __repr__
# ============================================================================
cells.append(md(r"""
## 12. `__str__` vs `__repr__`

### Kya hai
- `__str__` — **user-friendly** readable string (jab `print(obj)` ya `str(obj)` chalao).
- `__repr__` — **developer-friendly** unambiguous string (jab sirf `obj` type karo REPL
  me, ya `repr(obj)` call karo). Ideally aisi honi chahiye ke usay `eval()` kar ke wapas
  object recreate ho sake.

### Kyun / kahan use hota hai
Agar `__str__` define na ho, Python `__repr__` ko fallback ke tor par use karta hai. Agar
dono na hon, default `<__main__.Student object at 0x...>` jaisa ugly output aata hai.
"""))

cells.append(code(r"""
class Student:
    def __init__(self, name, roll_no, marks=None):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks if marks is not None else []

    def __str__(self):
        # print(student) ya str(student) call hone par yeh chalega -- readable
        return f"Student({self.name}, Roll {self.roll_no})"

    def __repr__(self):
        # repr(student) ya sirf 'student' likhne par yeh chalega -- unambiguous/debug-friendly
        return f"Student(name={self.name!r}, roll_no={self.roll_no!r}, marks={self.marks!r})"

s1 = Student("Ayesha", 1, [90, 85])

print(s1)          # __str__ use hota hai
print(str(s1))     # __str__ explicitly
print(repr(s1))    # __repr__ explicitly

print([s1])        # list ke andar print karne par __repr__ use hota hai, __str__ nahi!
"""))

cells.append(md(r"""
**Output ka matlab:** `print(s1)` -> `__str__` (readable). Lekin `print([s1])` (list ke
andar) -> `__repr__` use hua, kyun ke containers (`list`, `dict`) apne elements ko print
karte waqt hamesha `repr()` use karte hain, `str()` nahi.

### Common mistakes / gotchas
- Sirf `__repr__` define karo aur `__str__` na karo — koi masla nahi, Python `__repr__`
  ko hi fallback ke tor par use kar lega `print()` ke liye.
- `__repr__` me `!r` format specifier use karna best practice hai — strings ko quotes
  ke sath dikhata hai (`name='Ayesha'` na ke `name=Ayesha`), jo debug karte waqt clearer
  hota hai.

**Interview tip:** "`__repr__` is for developers/debugging, `__str__` is for end users.
If only one is defined, prefer `__repr__` because Python falls back to it." Yeh line
ready rakho.
"""))

# ============================================================================
# 14. STORING OBJECTS IN LIST / DICT
# ============================================================================
cells.append(md(r"""
## 13. Objects ko `list` / `dict` me Store Karna

### Kya hai / Kyun
Real applications me hume **kayi objects** ek sath manage karne hote hain — jaise
"saare students ki class list". Objects ko `list` me daal kar loop kar sakte hain, ya
`dict` me kisi unique key (jaise `roll_no`) ke against store kar ke fast lookup kar
sakte hain.
"""))

cells.append(code(r"""
class Student:
    def __init__(self, name, roll_no, marks=None):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks if marks is not None else []

    def __repr__(self):
        return f"Student({self.name!r}, roll_no={self.roll_no})"

# ---- List me store karna ----
students_list = [
    Student("Ayesha", 1, [90, 85]),
    Student("Bilal", 2, [70, 75]),
    Student("Sara", 3, [95, 92]),
]

print("Poori list:", students_list)   # __repr__ use hoga

for s in students_list:
    avg = sum(s.marks) / len(s.marks)
    print(f"{s.name}: average marks = {avg:.2f}")

# ---- Dict me store karna (roll_no -> object, fast lookup ke liye) ----
students_by_roll = {s.roll_no: s for s in students_list}

# ab O(1) me kisi bhi roll_no se student mil sakta hai (list me O(n) lagta)
lookup = students_by_roll[2]
print("\nRoll 2 ka student:", lookup)

assert students_by_roll[1].name == "Ayesha"
assert len(students_by_roll) == 3
print("Asserts pass!")
"""))

cells.append(md(r"""
**Output ka matlab:** `dict` me store karne se `roll_no` ke zariye direct O(1) lookup
mil gaya, jab ke `list` me dhoondne ke liye O(n) loop lagta. Yeh pattern real projects
me bohat common hai (jaise database records ko ID ke against cache karna).

**Interview tip:** "Store objects in a dict keyed by their unique identifier when you
need O(1) lookups; use a list when order matters or you'll always iterate everything."
"""))

# ============================================================================
# 15. REAL EXAMPLES: BOOK, CAR
# ============================================================================
cells.append(md(r"""
## 14. Real Examples — Book aur Car Classes

Ab tak humne `Student` class ko dheere dheere improve kiya. Chalo do aur real-world
classes banate hain taake pattern pukhta ho jaye.
"""))

cells.append(code(r"""
class Book:
    def __init__(self, title, author, pages, price):
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.is_issued = False   # library me hai ya issue ho chuki hai

    def issue(self):
        if self.is_issued:
            print(f"'{self.title}' pehle se hi issue hai!")
        else:
            self.is_issued = True
            print(f"'{self.title}' issue kar di gayi.")

    def return_book(self):
        self.is_issued = False
        print(f"'{self.title}' wapas aa gayi.")

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"'{self.title}' by {self.author} ({self.pages}p, Rs.{self.price}) [{status}]"

book1 = Book("Python Crash Course", "Eric Matthes", 560, 2500)
print(book1)
book1.issue()
book1.issue()      # dobara issue karne ki koshish -> already-issued message
book1.return_book()
print(book1)
"""))

cells.append(code(r"""
class Car:
    # class attribute: total kitni cars bani hain, sab objects share karte hain
    total_cars_made = 0

    def __init__(self, brand, model, year, fuel_level=0):
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel_level = fuel_level   # percentage: 0 to 100
        Car.total_cars_made += 1       # har naye object par class-level counter barhta hai

    def refuel(self, amount):
        self.fuel_level = min(100, self.fuel_level + amount)  # 100% se zyada nahi ho sakta

    def drive(self, distance_km):
        fuel_needed = distance_km // 10  # har 10km ke liye 1% fuel (simple simulation)
        if fuel_needed > self.fuel_level:
            print(f"{self.brand} {self.model}: itna fuel nahi hai is safar ke liye!")
        else:
            self.fuel_level -= fuel_needed
            print(f"{self.brand} {self.model} ne {distance_km}km chala. Fuel left: {self.fuel_level}%")

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} (Fuel: {self.fuel_level}%)"

car1 = Car("Toyota", "Corolla", 2022, fuel_level=50)
car2 = Car("Honda", "Civic", 2023, fuel_level=20)

car1.refuel(30)
car1.drive(400)
car2.drive(400)   # kam fuel hai, warning aayegi

print(car1)
print(car2)
print("Total cars made so far:", Car.total_cars_made)  # class attribute -- shared counter

assert Car.total_cars_made == 2
"""))

# ============================================================================
# 16. COMMON MISTAKES / GOTCHAS (consolidated section)
# ============================================================================
cells.append(md(r"""
## 15. Common Mistakes / Gotchas (Consolidated)

Upar humne gotchas concept-wise dekhe. Yahan do sab se common mistakes ko live demo
karte hain jo beginners bohat karte hain.
"""))

cells.append(code(r"""
# MISTAKE 1: method define karte waqt 'self' bhool jana

class BrokenCounter:
    def __init__(self):
        self.count = 0

    def increment():          # 'self' bhool gaye!
        pass                   # (galat -- yeh ab bhi "count" access nahi kar sakta)

c = BrokenCounter()
try:
    c.increment()   # Python 'c' ko automatically pehla argument banata hai -> extra arg error
except TypeError as e:
    print("Error pakra gaya (self bhoolne ki wajah se):", e)
"""))

cells.append(code(r"""
# MISTAKE 2: mutable default argument function/method me (class attribute wali trap
# se related, lekin yeh __init__ ke PARAMETER par hoti hai)

class ShoppingCartBuggy:
    def __init__(self, items=[]):   # DANGER: default list SIRF EK BAAR banti hai (function def time par)
        self.items = items

    def add_item(self, item):
        self.items.append(item)

cart1 = ShoppingCartBuggy()
cart1.add_item("Laptop")

cart2 = ShoppingCartBuggy()   # naya cart -- lekin default 'items=[]' wahi PURANI list hai!
print("cart2 ka items (expected []):", cart2.items)   # bug: 'Laptop' yahan bhi aa jayega!

# FIX: hamesha None default use karo
class ShoppingCartFixed:
    def __init__(self, items=None):
        self.items = items if items is not None else []   # har object apni nayi list banata hai

    def add_item(self, item):
        self.items.append(item)

cart3 = ShoppingCartFixed()
cart3.add_item("Phone")
cart4 = ShoppingCartFixed()
print("cart4 ka items (fixed, expected []):", cart4.items)

assert cart2.items == ["Laptop"]     # buggy behavior proof
assert cart4.items == []             # fixed behavior proof
"""))

cells.append(md(r"""
### Aur gotchas jo yaad rakhne wale hain
- Class attribute vs instance attribute ka naam **same** rakhna confusion paida karta
  hai — `self.x = x` likhne se instance-level `x` ban jata hai jo class-level `x` ko
  "shadow" kar deta hai (chupa deta hai), delete karna par wapis class wala nazar aata hai.
- `self` ko method ke andar reassign karna (`self = something_else`) kabhi mat karo —
  yeh sirf local variable badal dega, object ko nahi.
- Object comparison: `obj1 == obj2` by default `obj1 is obj2` jaisa hi behave karta hai
  (identity check) jab tak `__eq__` define na ho — yeh agla notebook (dunder methods) me
  detail se cover hoga.
"""))

# ============================================================================
# 17. REAL-WORLD PROBLEMS
# ============================================================================
cells.append(md(r"""
## 16. Real-World Problems (Practice with Solutions)

Chaar realistic problems, jinke commented solutions neeche hain.
"""))

cells.append(md(r"""
### Problem 1: Library Book Tracker

Ek chhoti library system banao jahan books track ho sakein — kitni copies available
hain, issue/return ka hisaab.
"""))

cells.append(code(r"""
class LibraryBook:
    def __init__(self, title, total_copies):
        self.title = title
        self.total_copies = total_copies
        self.issued_copies = 0   # kitni copies is waqt issue hain

    @property
    def available_copies(self):
        # yeh ek computed value hai -- humesha total - issued
        return self.total_copies - self.issued_copies

    def issue_copy(self):
        if self.available_copies > 0:
            self.issued_copies += 1
            print(f"'{self.title}' ki ek copy issue hui. Available: {self.available_copies}")
        else:
            print(f"'{self.title}' ki koi copy available nahi hai!")

    def return_copy(self):
        if self.issued_copies > 0:
            self.issued_copies -= 1
            print(f"'{self.title}' ki ek copy wapas aayi. Available: {self.available_copies}")

book = LibraryBook("Clean Code", total_copies=2)
book.issue_copy()
book.issue_copy()
book.issue_copy()   # ab koi copy available nahi
book.return_copy()

assert book.available_copies == 1
assert book.issued_copies == 1
print("\nSab asserts pass!")
"""))

cells.append(md(r"""
### Problem 2: Bank Account with Validation

Bank account jo negative balance ya invalid amounts na hone de.
"""))

cells.append(code(r"""
class SafeBankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount positive hona chahiye!")
            return
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdraw amount positive hona chahiye!")
            return
        if amount > self.balance:
            print("Insufficient funds!")
            return
        self.balance -= amount

acc = SafeBankAccount("Nadia", 1000)
acc.deposit(500)
acc.withdraw(200)
acc.withdraw(-50)     # invalid -> reject
acc.deposit(0)        # invalid -> reject
acc.withdraw(5000)     # insufficient -> reject

print("Final balance:", acc.balance)
assert acc.balance == 1300
"""))

cells.append(md(r"""
### Problem 3: Simple Inventory Management

Store ke products ka stock track karo, low-stock warning ke sath.
"""))

cells.append(code(r"""
class Product:
    LOW_STOCK_THRESHOLD = 5   # class attribute -- sab products ke liye same rule

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def sell(self, units):
        if units > self.quantity:
            print(f"'{self.name}': itni quantity stock me nahi hai!")
            return
        self.quantity -= units
        print(f"{units} '{self.name}' beche gaye. Baaki stock: {self.quantity}")
        if self.quantity < Product.LOW_STOCK_THRESHOLD:
            print(f"  WARNING: '{self.name}' ka stock kam ho raha hai ({self.quantity} bache)!")

    def restock(self, units):
        self.quantity += units

inventory = [
    Product("Notebook", 50, 20),
    Product("Pen", 10, 100),
]

inventory[0].sell(17)   # stock 20 -> 3, low stock warning ayegi
inventory[1].sell(30)   # stock 100 -> 70, koi warning nahi

assert inventory[0].quantity == 3
assert inventory[1].quantity == 70
"""))

cells.append(md(r"""
### Problem 4: Employee Payroll Calculator

Employees ka basic salary + bonus/deductions se net pay calculate karo.
"""))

cells.append(code(r"""
class Employee:
    def __init__(self, name, basic_salary):
        self.name = name
        self.basic_salary = basic_salary
        self.bonus = 0
        self.deductions = 0

    def add_bonus(self, amount):
        self.bonus += amount

    def add_deduction(self, amount):
        self.deductions += amount

    def net_pay(self):
        # method jo real-time calculation karta hai -- state store nahi karta
        return self.basic_salary + self.bonus - self.deductions

    def __str__(self):
        return f"{self.name}: Net Pay = Rs.{self.net_pay()}"

emp = Employee("Usman", basic_salary=50000)
emp.add_bonus(5000)
emp.add_deduction(2000)
print(emp)

assert emp.net_pay() == 53000
"""))

# ============================================================================
# 18. LEETCODE PROBLEMS
# ============================================================================
cells.append(md(r"""
## 17. LeetCode Problems (Class-based Solutions)

OOP theme ke sath teen LeetCode problems solve karte hain — LeetCode khud bhi `class
Solution` ka structure expect karta hai, is liye yeh dono world (OOP practice +
interview prep) ek sath cover ho rahe hain.
"""))

cells.append(md(r"""
### LC 1929. Concatenation of Array — Easy
https://leetcode.com/problems/concatenation-of-array/

**Bayan:** Ek array `nums` (length `n`) diya hai. Ek naya array `ans` (length `2n`)
banao jahan:
- `ans[i] = nums[i]` for `0 <= i < n`
- `ans[i + n] = nums[i]` for `0 <= i < n`

Yani `nums` ko apne aap ke sath jorna hai (concatenate).

**Approach:**
- **Brute force**: naya array banao, do loops (ya ek loop, dono index fill karo).
- **Optimal**: Python me `nums + nums` seedha concatenation kar deta hai — O(n) me.

**Time complexity:** O(n) dono approaches me (output khud O(n) size ka hai).
**Space complexity:** O(n) for the output array.

Neeche hum LeetCode ke expected `class Solution` format ke sath **class-wrapper style**
bhi dikha rahe hain (object-oriented tareeqe se ek "converter" object banana).
"""))

cells.append(code(r"""
# ---- Brute-force style (dono index manually fill karna) ----
class SolutionBruteForce:
    def getConcatenation(self, nums: list[int]) -> list[int]:
        n = len(nums)
        ans = [0] * (2 * n)   # pehle se size fix kar lena efficient hai
        for i in range(n):
            ans[i] = nums[i]        # pehla hissa
            ans[i + n] = nums[i]    # dusra hissa (concatenation)
        return ans


# ---- Optimal (LeetCode standard "class Solution" format) ----
class Solution:
    def getConcatenation(self, nums: list[int]) -> list[int]:
        return nums + nums   # Python list concatenation -- ek line me kaam


# ---- Class-wrapper style (OOP theme ke mutabiq: ek object jo array ko "wrap" karta hai) ----
class ArrayConcatenator:
    def __init__(self, nums: list[int]):
        self.nums = nums   # object apna data khud carry karta hai

    def concatenate(self) -> list[int]:
        return self.nums + self.nums


# ---- Test cases ----
assert SolutionBruteForce().getConcatenation([1, 2, 1]) == [1, 2, 1, 1, 2, 1]
assert Solution().getConcatenation([1, 2, 1]) == [1, 2, 1, 1, 2, 1]
assert Solution().getConcatenation([1, 3, 2, 1]) == [1, 3, 2, 1, 1, 3, 2, 1]

converter = ArrayConcatenator([1, 2, 1])
assert converter.concatenate() == [1, 2, 1, 1, 2, 1]

print("LC 1929: sab asserts pass!")
"""))

cells.append(md(r"""
### LC 2469. Convert the Temperature — Easy
https://leetcode.com/problems/convert-the-temperature/

**Bayan:** Ek `celsius` (float) diya hai. Ek array `[kelvin, fahrenheit]` return karo,
jahan:
- `Kelvin = Celsius + 273.15`
- `Fahrenheit = Celsius * 1.8 + 32.00`

Answer 10^-5 tak accurate hona chahiye.

**Approach:** Seedha formula apply karo, `round(value, 5)` se precision handle karo.

**Time complexity:** O(1) — sirf arithmetic.
**Space complexity:** O(1).

Is problem ko hum poori tarah **class-based** solve kar rahe hain (theme ke mutabiq) —
ek `TemperatureConverter` object banate hain jo apna `celsius` value carry karta hai.
"""))

cells.append(code(r"""
class TemperatureConverter:
    def __init__(self, celsius: float):
        self.celsius = celsius   # object apna input value store karta hai

    def convert(self) -> list[float]:
        kelvin = round(self.celsius + 273.15, 5)     # Kelvin formula
        fahrenheit = round(self.celsius * 1.8 + 32.00, 5)  # Fahrenheit formula
        return [kelvin, fahrenheit]


# ---- Test cases (LeetCode ke official examples) ----
assert TemperatureConverter(36.50).convert() == [309.65, 97.7]
assert TemperatureConverter(122.11).convert() == [395.26, 251.798]

print("LC 2469: sab asserts pass!")
print("Example:", TemperatureConverter(36.50).convert())
"""))

cells.append(md(r"""
### LC 1656. Design an Ordered Stream — Easy
https://leetcode.com/problems/design-an-ordered-stream/

**Bayan:** `n` values ka ek stream hai, id `1` se `n` tak. `OrderedStream` class banao:
- `OrderedStream(int n)` — stream initialize karo `n` values ke liye.
- `insert(int idKey, String value)` — id `idKey` par `value` store karo, aur woh saari
  **consecutive** values return karo jo pointer se shuru ho kar milti hain (chunk),
  phir pointer ko aage badhao.

Yeh problem khud OOP hai — bilkul `class`-based design expect karta hai.

**Approach:**
- Ek array `stream` banao size `n+1` ka (1-indexed, index 0 unused).
- Ek `pointer` rakho jo batata hai "agla kaunsa id chahiye tha".
- `insert` par: value store karo, phir jab tak `pointer` par value maujood hai, usay
  result me daalo aur `pointer` aage badhao.

**Time complexity:** Har `insert` call worst case O(n) lag sakta hai, lekin **total**
(saari calls milakar) O(n) hi hota hai — har id sirf ek dafa "consume" hota hai
(amortized O(1) per call).
**Space complexity:** O(n) for the internal stream array.
"""))

cells.append(code(r"""
class OrderedStream:
    def __init__(self, n: int):
        self.stream = [None] * (n + 1)   # 1-indexed; index 0 kabhi use nahi hoga
        self.ptr = 1                      # agla id jo hume "expect" hai

    def insert(self, idKey: int, value: str) -> list[str]:
        self.stream[idKey] = value   # is id par value store karo

        result = []
        # jab tak pointer par value maujood hai, usay result me daalo aur aage barho
        while self.ptr < len(self.stream) and self.stream[self.ptr] is not None:
            result.append(self.stream[self.ptr])
            self.ptr += 1
        return result


# ---- Test case (LeetCode ka official example) ----
os_stream = OrderedStream(5)
r1 = os_stream.insert(3, "ccccc")
r2 = os_stream.insert(1, "aaaaa")
r3 = os_stream.insert(2, "bbbbb")
r4 = os_stream.insert(5, "eeeee")
r5 = os_stream.insert(4, "ddddd")

assert r1 == []
assert r2 == ["aaaaa"]
assert r3 == ["bbbbb", "ccccc"]
assert r4 == []
assert r5 == ["ddddd", "eeeee"]

print("LC 1656: sab asserts pass!")
print("Results:", r1, r2, r3, r4, r5)
"""))

# ============================================================================
# 19. INTERVIEW Q&A
# ============================================================================
cells.append(md(r"""
## 18. Interview Questions & Answers

**Q1. Class aur object me farq kya hai?**
Class ek blueprint/template hai; object us blueprint se banaya gaya actual instance hai
jiska apna memory aur state hota hai.

**Q2. `__init__` constructor hai ya initializer?**
Technically **initializer** hai. Asal object creation `__new__` karta hai; `__init__`
sirf us object ko values se initialize karta hai.

**Q3. `self` kya hai, aur kya yeh keyword hai?**
`self` us object ka reference hai jis par method call ho raha hai. Yeh keyword nahi,
sirf ek strong convention hai — `obj.method()` internally `Class.method(obj)` hota hai.

**Q4. Instance attribute aur class attribute me farq?**
Instance attribute (`self.x`) har object ka apna hota hai. Class attribute (class body
me directly) sab instances ke darmiyan shared hota hai.

**Q5. Mutable default class attribute (jaise `list`) khatarnak kyun hai?**
Kyun ke woh sab instances ke darmiyan **shared** hota hai — ek instance ka change sab
par asar dalta hai. Fix: mutable data hamesha `__init__` ke andar `self.x = []` se banao.

**Q6. `__dict__`, `vars()`, aur `dir()` me farq?**
`obj.__dict__` aur `vars(obj)` sirf instance attributes ki dictionary dete hain (same
cheez). `dir(obj)` bohat zyada cheezein deta hai — instance + class attributes + saare
inherited methods/dunders ki poori list.

**Q7. `__str__` aur `__repr__` me farq?**
`__str__` end-user ke liye readable representation deta hai (`print(obj)`). `__repr__`
developer/debugging ke liye unambiguous representation deta hai (`repr(obj)`, ya list
ke andar print hote waqt). Agar sirf ek define karni ho, `__repr__` prefer karo (Python
usay fallback ke tor par bhi use karta hai).

**Q8. Python "constructor overloading" support karta hai?**
Nahi, Java/C++ jaisi direct overloading nahi hoti (do `__init__` likhne se dusra pehli
ko overwrite kar deta hai). Iski jagah default arguments aur `@classmethod` factory
methods use hote hain.

**Q9. `@classmethod` factory kyun use karte hain?**
Jab ek hi class ko alag alag input formats se banana ho (jaise CSV string se, ya
dictionary se) — har format ke liye ek alag, readable naam wala classmethod banate hain
(`from_string`, `from_dict`, waghera) jo `cls(...)` call kar ke object return karta hai.

**Q10. `__new__` aur `__init__` ka order kya hai, aur farq?**
`__new__` pehle chalta hai — yeh object ka memory allocate karta hai aur usay return
karta hai. Uske baad Python automatically `__init__` call karta hai us object par, taake
attributes set ho sakein. `__new__` static-ish hota hai (`cls` leta hai), `__init__`
instance method hai (`self` leta hai).

**Q11. `__del__` par cleanup ke liye bharosa karna theek hai?**
Nahi — CPython me refcounting se yeh usually turant chalta hai, lekin timing
**guaranteed** nahi hoti (khaas kar cycles ya doosre Python implementations me). Critical
resources (files, connections) ke liye context managers (`with` statement) use karo.

**Q12. `del obj` object ko delete karta hai?**
Nahi — `del obj` sirf `obj` naam (reference) ko hataata hai. Agar yeh **aakhri**
reference thi to object garbage-collected hota hai aur `__del__` chalta hai; warna
object memory me baaki references ke sath zinda rehta hai.

**Q13. Ek class ke methods kahan store hote hain — har instance me ya class me?**
Class ke `__dict__` me — sab instances **wahi ek** method object share karte hain.
Isi liye 1000 objects banane se method ki 1000 copies nahi bantin, memory efficient hai.

**Q14. Do objects `obj1 == obj2` compare karne par True kab denge?**
Default behavior me `==` identity check (`is`) jaisa hota hai — jab tak class me
`__eq__` define na ho. Do alag objects same attribute values ke sath bhi by default
`False` denge jab tak `__eq__` override na ho (agla notebook ka topic).

**Q15. Instance method ke andar `self.attr` likhne se kya hota hai agar `attr` class
attribute ke tor par pehle se maujood ho?**
Yeh us instance ke liye ek **naya instance attribute** bana deta hai jo class attribute
ko "shadow" (chupa) kar deta hai us specific instance ke liye — class attribute khud
tabdeel nahi hota, aur baaki instances par asar nahi hota.

**Q16. `vars(obj)['x'] = 5` likhna safe hai?**
Yeh technically kaam kar jata hai (`__dict__` ko directly modify kar deta hai), lekin
best practice nahi hai — hamesha `obj.x = 5` likho, readability aur consistency ke liye.
"""))

# ============================================================================
# 20. PRACTICE EXERCISES
# ============================================================================
cells.append(md(r"""
## 19. Practice Exercises (Khud Karo)

Neeche diye gaye tasks khud, is notebook ki style follow karte hue, solve karo. Hints
diye gaye hain.

1. **Rectangle class**: `Rectangle(width, height)` banao jisme `area()` aur `perimeter()`
   methods hon. *(Hint: dono simple formulas hain, `self.width * self.height`.)*

2. **Counter with class attribute**: `Counter` class banao jisme har naye object par
   ek class-level `total_created` counter barhta ho (jaise `Car.total_cars_made`).
   *(Hint: `__init__` ke andar `ClassName.total_created += 1` likho.)*

3. **Shared-state bug dhoondo**: Ek `Playlist` class banao jisme `songs = []` **class**
   attribute ke tor par ho (bug jaan boojh kar). Do playlists banao, dikhao ke bug
   hota hai, phir fix karo. *(Hint: is notebook ka "Team" example dekho.)*

4. **`__str__`/`__repr__` likho**: `Movie(title, year, rating)` class banao jisme
   `__str__` readable string de aur `__repr__` debug-friendly string de. Dono ka farq
   `print(movie)` aur list ke andar print kar ke dikhao.

5. **Classmethod factory**: `Temperature` class banao jisme `from_fahrenheit(cls, f)`
   naam ka classmethod ho jo Fahrenheit ko Celsius me convert kar ke object banaye.
   *(Hint: `celsius = (f - 32) / 1.8`.)*

6. **Runtime attribute practice**: Ek `Person` object banao, runtime par `nickname`
   attribute add karo, `vars()` se dikhao, phir `del` kar ke `AttributeError` catch karo.

7. **Dictionary of objects**: 5 `Product` objects (naam + price) ek `dict` me store karo
   (`name -> Product`), phir sab se mehnga product `max()` + lambda se dhoondo.
   *(Hint: `max(products.values(), key=lambda p: p.price)`.)*

8. **`__del__` order dikhao**: Ek class banao jisme `__new__`, `__init__`, aur `__del__`
   teeno print statements ke sath hon, aur do objects bana kar unka lifecycle order dikhao.

9. **LeetCode practice**: LC 1929, 2469, ya 1656 ka apna khud ka alternate implementation
   likho (jaise 1656 me `dict` use kar ke, list ke bajaye) aur time complexity compare
   karo.

10. **Mini system**: `Library` class banao jo andar `Book` objects ki `list` rakhe, aur
    `find_by_title(title)` method ho jo linear search kare. *(Hint: list comprehension
    ya loop + `if book.title == title`.)*
"""))

# ============================================================================
# 21. SUMMARY / CHEAT-SHEET
# ============================================================================
cells.append(md(r"""
## 20. Summary / Cheat-Sheet

| Concept | Ek-line Yaad Dahani |
|---|---|
| Class vs Object | Class = blueprint, Object = us se bana instance |
| `__init__` | Automatically object banate waqt chalta hai; initialize karta hai (constructor nahi, initializer) |
| `self` | Us object ka reference jis par method call hua; convention hai, keyword nahi |
| Instance attribute | `self.x = ...`, har object ka apna alag copy |
| Class attribute | Class body me direct, sab instances me shared |
| Shared-state trap | Mutable class attribute (list/dict) sab instances me shared hota hai — fix: `__init__` me banao |
| `__dict__` / `vars()` | Instance ke attributes ki dictionary |
| `dir()` | Instance + class + inherited sab kuch ki poori list |
| Methods ka location | Class ke `__dict__` me hote hain, instance ke nahi (memory efficient) |
| `del obj` | Sirf reference hataata hai; object tab destroy hota hai jab koi reference na bache |
| `__new__` | Object create karta hai (memory allocate) |
| `__del__` | Object destroy hote waqt chalta hai (cleanup ke liye guarantee nahi) |
| Constructor overloading | Python me nahi hoti — default args ya `@classmethod` factories use karo |
| `__str__` | `print(obj)` ke liye readable string |
| `__repr__` | `repr(obj)` / debugging ke liye unambiguous string; fallback bhi hai |
| Objects in list/dict | List = order + iterate; Dict = fast lookup by key |

### Is notebook ke baad agla kadam
Agle notebook me hum **Encapsulation** deep dive karenge: `_protected`, `__private`
(name mangling), `@property`, getters/setters ka Pythonic tareeqa.
"""))

save(r"OOP in Python/Basics/01_OOP_Introduction_Classes_and_Objects.ipynb", cells)
