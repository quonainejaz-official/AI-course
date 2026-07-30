import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ---------------------------------------------------------------------------
# 1. TITLE
# ---------------------------------------------------------------------------
cells.append(md(r"""
# 02 — Encapsulation, Access Modifiers aur Properties

**Level:** Beginner → Advanced (interview prep + university syllabus)

Ye notebook OOP series ka doosra notebook hai. Pehle notebook me humne classes, objects,
`__init__`, methods waghera dekhe the. Ab hum seekhenge ke apna data kaise **surakshit
(protect)** karte hain aur users ko kaise force karte hain ke woh sirf "sahi tareeqe" se
object ke andar ka data change karein.

## Is notebook me kya seekhenge (roadmap)

1. Encapsulation kya hai aur kyun zaroori hai
2. Public / protected (`_x`) / private (`__x`) naming conventions
3. Name mangling — proof ke Python me "private" asal me kya hota hai
4. Philosophy: "we are all consenting adults" — Python private ko force nahi karta
5. Classic Java-style getter/setter aur woh Pythonic kyun nahi
6. `@property` — getter, `@x.setter`, `@x.deleter`
7. Computed / derived properties (area, full_name, age-from-dob)
8. Read-only properties
9. `property()` function ka purana style
10. Backwards-compatible refactor — plain attribute se property tak, bina user code today
11. Data validation patterns + custom exceptions
12. Class-level constants
13. `__slots__` — memory saving aur typo-protection, gotchas ke sath
14. Information hiding vs abstraction — farq
15. Common mistakes / gotchas
16. Real-world problems (BankAccount, Temperature, User password hashing, Rectangle)
17. LeetCode problems (encapsulation/validation ke angle se)
18. Interview Q&A
19. Practice exercises
20. Summary / cheat-sheet

## Prerequisites

- Notebook 01 (classes, objects, `__init__`, instance/class methods) pehle se pata hona chahiye.
- Basic Python: functions, exceptions (`try/except`), dictionaries.
"""))

# ---------------------------------------------------------------------------
# 2. ENCAPSULATION — KYA HAI, KYUN
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 1. Encapsulation — Kya hai aur Kyun chahiye

**Kya hai:** Encapsulation ek OOP principle hai jisme hum object ka internal data (attributes)
aur us data par kaam karne wale methods ko ek unit (class) me bundle karte hain, aur bahar
ki duniya se us data ko **direct, uncontrolled access** se bachate hain.

**Kyun chahiye:**
- Data ko invalid state me jaane se rokna hai (jaise negative balance, negative age).
- Internal implementation ko chupana hai taake baad me badal saken bina bahar ka code tode.
- "Contract" define karna hai — object ke sath sirf defined methods/properties ke zariye
  interact karo, seedha internals se chher-chhaar mat karo.

**Kahan use hota hai:** Har jagah — banking systems, user accounts, game state, ORMs,
libraries jo apna internal state control karna chahti hain.

Neeche ek "bad design" dekhte hain jahan encapsulation bilkul nahi hai — bug turant nazar aata hai.
"""))

cells.append(code(r"""
# BAD DESIGN: koi encapsulation nahi -> balance seedha public attribute hai
class BankAccountBad:
    def __init__(self, balance):
        self.balance = balance  # kisi bhi validation ke bagair public attribute

acc = BankAccountBad(1000)
acc.balance = -5000  # koi rok-tok nahi - negative balance ban gaya, real bug!
print("Bad design ka balance:", acc.balance)  # -5000 -> ye ghalat hai magar Python ne allow kar diya
assert acc.balance == -5000  # proof ke Python ne kuch nahi roka
"""))

# ---------------------------------------------------------------------------
# 3. NAMING CONVENTIONS
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 2. Public / Protected (`_x`) / Private (`__x`) — Naming Conventions

**Kya hai:** Python me access control **keywords se nahi**, balke **naming conventions** se
hota hai:

| Prefix        | Naam         | Matlab                                                        |
|---------------|--------------|----------------------------------------------------------------|
| `name`        | Public       | Kahin se bhi access karo, koi restriction nahi                |
| `_name`       | Protected    | "Sirf internal use ke liye" — convention hai, force nahi hota  |
| `__name`      | Private      | Name-mangling hoti hai (`_ClassName__name`) — thoda mushkil banate hain access karna |

**Syntax:** Bas attribute/method ke naam ke shuru me underscore laga do — koi special keyword nahi.

**Kyun use hota hai:** Doosre developers (aur khud aap 6 mahine baad) ko batane ke liye ke
"ye attribute internal implementation detail hai, isse bahar se mat chhero."
"""))

cells.append(code(r"""
class Demo:
    def __init__(self):
        self.public_var = "sab kahin se dekh/badal sakte hain"          # public
        self._protected_var = "convention: 'internal use', phir bhi accessible"  # protected
        self.__private_var = "name-mangled, seedha access mushkil hai"          # private

d = Demo()
print(d.public_var)        # normal access - koi masla nahi
print(d._protected_var)    # convention violate karke bhi access ho gaya - Python nahi rokta
# d.__private_var seedha nahi chalega - agla cell me dekhenge
"""))

# ---------------------------------------------------------------------------
# 4. NAME MANGLING PROOF
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 3. Name Mangling — Proof

**Kya hai:** Jab class ke andar `self.__x` likhte hain, Python compile time par usay
`self._ClassName__x` me convert kar deta hai. Isay **name mangling** kehte hain.

**Kyun:** Taake subclasses accidentally parent class ki "private" cheezein overwrite na kar den
(name clash avoid karne ke liye), na ke security ke liye.

Chalo `__dict__` khol kar dekhte hain ke asal me naam kya bana.
"""))

cells.append(code(r"""
class Demo2:
    def __init__(self):
        self.__secret = 42  # Python isay andar hi andar '_Demo2__secret' bana dega

d2 = Demo2()
print(d2.__dict__)  # dekho: key '_Demo2__secret' hai, '__secret' nahi

try:
    print(d2.__secret)  # ye fail hoga - is naam ka attribute exist hi nahi karta (mangled ho chuka hai)
except AttributeError as e:
    print("AttributeError pakड़ liya:", e)

# lekin mangled naam se access ho jata hai - proof ke ye 'real' private nahi, sirf naam badla hai
print("Mangled naam se access:", d2._Demo2__secret)
assert d2._Demo2__secret == 42
"""))

# ---------------------------------------------------------------------------
# 5. PHILOSOPHY
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 4. Philosophy: Python me "Private" Real Nahi Hota

Java/C++ jaisi languages me `private` keyword compiler-level enforce hota hai — bahar se
bilkul access nahi ho sakta. **Python aisa nahi karta.**

Python ki philosophy: *"We are all consenting adults here"* — matlab, hum sab jaante hain ke
kya sahi hai kya ghalat, aur language humein zabardasti nahi rokegi. `__x` sirf ek **strong
hint** hai ("please isay bahar se mat chhuo"), enforcement nahi.

Isi liye humne upar dekha ke `_Demo2__secret` likh kar hum "private" attribute ko phir bhi
access/modify kar sakte hain. Yehi baat Real-World Problems section me BankAccount example me
bhi dikhayenge (validation bypass karna possible hai, agar koi jaan boojh kar mangled naam use kare).

**Interview tip:** Agar interviewer pooche "Does Python have true private variables?" — jawab hai
**NO**, sirf naming convention + name mangling hai jo accidental access rokta hai, malicious/
intentional access nahi.
"""))

# ---------------------------------------------------------------------------
# 6. CLASSIC GETTER/SETTER
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 5. Classic Getter/Setter (Java-style) — Aur Ye Pythonic Kyun Nahi

**Kya hai:** Java/C++ me tradition hai ke har private field ke liye `getX()` aur `setX(value)`
methods likhte hain.

**Syntax (Python me bhi likh sakte ho, lekin...):**
"""))

cells.append(code(r"""
class Employee:
    def __init__(self, salary):
        self.__salary = salary

    def get_salary(self):          # classic getter
        return self.__salary

    def set_salary(self, value):   # classic setter
        if value < 0:
            raise ValueError("salary negative nahi ho sakti")
        self.__salary = value

e = Employee(50000)
print(e.get_salary())
e.set_salary(60000)
print(e.get_salary())
try:
    e.set_salary(-100)
except ValueError as ex:
    print("ValueError:", ex)
"""))

cells.append(md(r"""
**Ye Pythonic kyun nahi:**
- Caller ko `e.salary` jaisi natural attribute syntax nahi milti, `e.get_salary()` likhna
  padta hai — verbose aur "un-Pythonic".
- Agar kal aap plain attribute se property me switch karna chahein, syntax badal jayega
  aur sara calling code todna padega.
- Python ka jawab: **`@property`** — jisse method attribute jaisa dikhta hai, lekin validation
  bhi kar sakta hai. Agla section me dekhte hain.
"""))

# ---------------------------------------------------------------------------
# 7. @property BASIC GETTER
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 6. `@property` — Getter

**Kya hai:** `@property` decorator ek method ko "computed attribute" bana deta hai — call
karte waqt parenthesis `()` nahi lagane padte.

**Syntax:**
```python
class C:
    @property
    def x(self):
        return self.__x
```

**Kahan use hota hai:** Jab chahte ho ke attribute jaisa access ho (`obj.x`), lekin peeche
logic/validation/computation chal rahi ho.
"""))

cells.append(code(r"""
class Circle:
    def __init__(self, radius):
        self.__radius = radius

    @property
    def radius(self):     # ab 'radius' ek property hai, method nahi lagta bahar se
        return self.__radius

c = Circle(5)
print(c.radius)          # note: c.radius, NOT c.radius() - parenthesis nahi
assert c.radius == 5
"""))

# ---------------------------------------------------------------------------
# 8. SETTER WITH VALIDATION
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 7. `@x.setter` — Validation ke Sath

**Kya hai:** `@property` ke sath `@<name>.setter` decorator laga kar hum assignment
(`obj.x = value`) ko bhi intercept kar sakte hain aur validation laga sakte hain.

**Syntax:**
```python
@x.setter
def x(self, value):
    # validation
    self.__x = value
```

**Gotcha:** Setter ke andar `self.<same_property_name> = value` mat likhna — isse infinite
recursion ho jayegi (ye hum Common Mistakes section me dikhayenge). Hamesha mangled/private
attribute (`self.__x`) me store karo.
"""))

cells.append(code(r"""
class Circle2:
    def __init__(self, radius):
        self.radius = radius  # yahan constructor me hi setter call ho raha hai (validation ke sath)

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("radius positive hona chahiye")
        self.__radius = value

c2 = Circle2(3)
print(c2.radius)
c2.radius = 10           # normal attribute syntax, lekin peeche validation chal rahi hai
print(c2.radius)
try:
    c2.radius = -1        # validation fail hoga
except ValueError as e:
    print("ValueError:", e)
assert c2.radius == 10
"""))

# ---------------------------------------------------------------------------
# 9. DELETER
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 8. `@x.deleter`

**Kya hai:** `del obj.x` chalane par custom logic run karne ke liye `@<name>.deleter`
decorator use hota hai.

**Kahan use hota hai:** Cleanup logic, logging, ya attribute reset karna jab `del` call ho.
"""))

cells.append(code(r"""
class Circle3:
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("radius positive hona chahiye")
        self.__radius = value

    @radius.deleter
    def radius(self):
        print("Radius delete ho raha hai...")   # cleanup / logging yahan kar sakte hain
        del self.__radius

c3 = Circle3(4)
del c3.radius   # deleter call hoga
try:
    print(c3.radius)   # ab attribute exist nahi karta
except AttributeError as e:
    print("AttributeError:", e)
"""))

# ---------------------------------------------------------------------------
# 10. COMPUTED / DERIVED PROPERTIES
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 9. Computed / Derived Properties

**Kya hai:** Property hamesha `self.__x` return nahi karti — ye kisi bhi expression/computation
ka result bhi return kar sakti hai, jo har baar access hone par (re)calculate hota hai.

**Examples neeche:** circle ka `area`, person ka `full_name`, aur ek fixed reference date se
`age` (note: hum `date.today()` use **nahi** karenge, warna asserts future me fail ho jayenge —
hamesha fixed date use karo jab deterministic output chahiye).
"""))

cells.append(code(r"""
class CircleFull:
    PI = 3.14159  # constant neeche class-level constants section me detail me dekhenge

    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):                              # computed property - har call par calculate hoti hai
        return round(CircleFull.PI * self.radius ** 2, 2)

    @property
    def circumference(self):
        return round(2 * CircleFull.PI * self.radius, 2)

cf = CircleFull(10)
print("Area:", cf.area, "| Circumference:", cf.circumference)
assert cf.area == 314.16
assert cf.circumference == 62.83
"""))

cells.append(code(r"""
class Person:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):                          # do attributes ko combine kar ke derive kiya
        return f"{self.first} {self.last}"

p = Person("Ayesha", "Khan")
print(p.full_name)
assert p.full_name == "Ayesha Khan"

p.first = "Sana"       # first badalne se full_name automatically update ho jata hai
print(p.full_name)
assert p.full_name == "Sana Khan"
"""))

cells.append(code(r"""
from datetime import date

class PersonAge:
    # FIXED reference date - deterministic output ke liye asal 'aaj ki date' NAHI use kar rahe
    _FIXED_TODAY = date(2026, 1, 1)

    def __init__(self, name, dob):
        self.name = name
        self.dob = dob   # date object

    @property
    def age(self):
        ref = PersonAge._FIXED_TODAY
        years = ref.year - self.dob.year
        # agar birthday abhi is saal nahi aaya (month/day fixed date se aage hai) to ek saal ghatao
        if (ref.month, ref.day) < (self.dob.month, self.dob.day):
            years -= 1
        return years

pa = PersonAge("Bilal", date(2000, 5, 15))
print("Age (fixed reference 2026-01-01):", pa.age)
assert pa.age == 25   # 2000-05-15 se 2026-01-01 tak - birthday abhi nahi aaya is saal, is liye 25
"""))

# ---------------------------------------------------------------------------
# 11. READ-ONLY PROPERTY
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 10. Read-Only Property

**Kya hai:** Agar sirf `@property` (getter) define karo aur `@x.setter` bilkul na likho, to
`obj.x = value` karne par Python khud `AttributeError` de dega — bina extra code likhe
read-only attribute mil jata hai.

**Kahan use hota hai:** IDs, timestamps, computed values jo kabhi bhi bahar se set nahi hone
chahiye.
"""))

cells.append(code(r"""
class Employee2:
    def __init__(self, emp_id, name):
        self.__emp_id = emp_id     # ye kabhi change nahi hona chahiye
        self.name = name

    @property
    def emp_id(self):
        return self.__emp_id
    # NOTE: setter define nahi kiya - is liye 'emp_id' automatically read-only ban gaya

emp = Employee2("E101", "Sara")
print(emp.emp_id)
try:
    emp.emp_id = "E999"     # setter nahi hai, is liye ye fail hoga
except AttributeError as e:
    print("AttributeError:", e)
assert emp.emp_id == "E101"
"""))

# ---------------------------------------------------------------------------
# 12. property() FUNCTION FORM
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 11. `property()` Function Form (Purana Style)

**Kya hai:** `@property` decorator ke aane se pehle (aur aaj bhi valid hai) `property()`
built-in function directly use hoti thi — getter, setter, deleter, aur docstring pass karke.

**Syntax:**
```python
x = property(fget, fset, fdel, "docstring")
```

Dono style **functionally same** hain — `@property` sirf syntactic sugar hai.
"""))

cells.append(code(r"""
class Square:
    def __init__(self, side):
        self.__side = side

    def get_side(self):
        return self.__side

    def set_side(self, value):
        if value <= 0:
            raise ValueError("side positive hona chahiye")
        self.__side = value

    def del_side(self):
        del self.__side

    # purana style - decorator ke bagair, seedha property() function call kar ke
    side = property(get_side, set_side, del_side, "Square ka side length")

sq = Square(5)
print(sq.side)
sq.side = 8
print(sq.side)
print("Docstring:", Square.side.__doc__)
assert sq.side == 8
"""))

# ---------------------------------------------------------------------------
# 13. BACKWARDS-COMPATIBLE REFACTOR
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 12. Backwards-Compatible Refactor: Plain Attribute → Property

**Kya hai:** Ye `@property` ka sabse bada practical faida hai — agar aapne pehle plain
attribute (`self.width`) expose kiya tha aur bahut sara user code `obj.width = 20` likh chuka
hai, to aap **bina us code ko tode** property me switch kar sakte ho, kyunki syntax bilkul
same rehta hai (`obj.width`), sirf peeche validation add ho jati hai.
"""))

cells.append(code(r"""
# V1: shuru me simple class, width plain public attribute hai
class RectangleV1:
    def __init__(self, width):
        self.width = width

r1 = RectangleV1(10)
r1.width = 20              # purana user code - direct assignment, koi validation nahi
print("V1 width:", r1.width)

# V2: ab humein validation chahiye (width kabhi negative na ho), LEKIN user code todna nahi
class RectangleV2:
    def __init__(self, width):
        self.width = width   # ye ab property setter call karega (neeche define hai)

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("width positive honi chahiye")
        self.__width = value

r2 = RectangleV2(10)
r2.width = 20     # BILKUL WAHI syntax jo V1 me tha - kuch nahi tuta, validation transparently add ho gayi
print("V2 width:", r2.width)
try:
    r2.width = -5
except ValueError as e:
    print("ValueError:", e)
assert r2.width == 20
"""))

# ---------------------------------------------------------------------------
# 14. VALIDATION PATTERNS + CUSTOM EXCEPTIONS
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 13. Data Validation Patterns + Custom Exception Classes

**Kya hai:** Property setters me validation likhna best practice hai. Agar validation
domain-specific hai (jaise "invalid age"), to generic `ValueError` ke bajaye **custom
exception class** banana behtar hai — isse calling code specific `except` laga sakta hai aur
error messages bhi zyada meaningful hote hain.

**Syntax:**
```python
class MyError(Exception):
    pass
```
"""))

cells.append(code(r"""
class InvalidAgeError(Exception):
    # Custom exception - jab age invalid ho (negative, ya range se bahar, ya wrong type)
    pass

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age   # setter call hoga

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise InvalidAgeError(f"Age integer honi chahiye, mila: {type(value).__name__}")
        if value < 0 or value > 120:
            raise InvalidAgeError(f"Age valid range (0-120) me nahi hai: {value}")
        self.__age = value

s = Student("Ahmed", 20)
print(s.age)
try:
    s.age = -5
except InvalidAgeError as e:
    print("InvalidAgeError:", e)
try:
    s.age = "twenty"
except InvalidAgeError as e:
    print("InvalidAgeError:", e)
assert s.age == 20   # invalid assignments ne asal age nahi badla
"""))

# ---------------------------------------------------------------------------
# 15. CLASS-LEVEL CONSTANTS
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 14. Class-Level Constants

**Kya hai:** Class-level constant woh attribute hai jo class ke andar (methods se bahar)
define hota hai aur sab instances is single value ko share karte hain — convention ke tor par
UPPER_CASE naming use hoti hai.

**Kahan use hota hai:** Fixed values jo har object ke liye same rehti hain (PI, MAX_LIMIT,
DEFAULT_CURRENCY waghera).
"""))

cells.append(code(r"""
class Circle4:
    PI = 3.14159   # class-level constant - sab instances share karte hain, memory bhi bachti hai

    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return round(Circle4.PI * self.radius ** 2, 2)

print("Class ke through:", Circle4.PI)
c4a = Circle4(2)
c4b = Circle4(3)
print("Instance ke through bhi wahi value:", c4a.PI, c4b.PI)
assert Circle4.PI == 3.14159
assert c4a.PI is c4b.PI   # dono instances same object ko refer kar rahe hain (constant shared hai)
"""))

# ---------------------------------------------------------------------------
# 16. __slots__
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 15. `__slots__` — Memory Saving aur Typo-Protection

**Kya hai:** `__slots__` class attribute define karke hum Python ko batate hain ke instance
ke paas **sirf yehi fixed attributes** honge — Python phir har instance ke liye `__dict__`
nahi banata, seedha fixed slots allocate karta hai.

**Kyun use hota hai:**
1. **Memory saving** — bohat sari instances banani ho (lakhon objects) to `__dict__` ka
   overhead bachta hai.
2. **Typo protection** — agar galti se `obj.nmae = "x"` likh do (typo), error mil jayega
   instead of silently naya attribute ban jane ke.

**Syntax:**
```python
class C:
    __slots__ = ("x", "y")
```
"""))

cells.append(code(r"""
class PointSlots:
    __slots__ = ("x", "y")   # sirf ye do attributes allowed - koi __dict__ nahi banega

    def __init__(self, x, y):
        self.x = x
        self.y = y

ps = PointSlots(1, 2)
print(ps.x, ps.y)

try:
    ps.z = 100     # typo ya naya attribute add karne ki koshish - slots isay rokta hai
except AttributeError as e:
    print("AttributeError (typo-protection ka fayda):", e)

try:
    print(ps.__dict__)    # slots wale objects ka __dict__ hota hi nahi
except AttributeError as e:
    print("AttributeError:", e)
"""))

cells.append(md(r"""
**Gotcha:** `__slots__` aur properties ka naam clash nahi ho sakta — agar `__slots__` me
`"value"` likha hai aur class me `value` naam ki property bhi define karo, Python class
banate waqt hi error de dega. Neeche dikhate hain (dynamic `exec` + `try/except` ke sath
taake notebook crash na ho).
"""))

cells.append(code(r"""
# __slots__ + property same naam - class DEFINITION time par hi error aata hai
try:
    exec(
        "class BadSlots:\n"
        "    __slots__ = ('value',)\n"
        "    @property\n"
        "    def value(self):\n"
        "        return self.__value\n"
    )
except ValueError as e:
    print("ValueError (slots + property naam clash):", e)
"""))

cells.append(md(r"""
Doosri gotchas:
- Inheritance me agar parent class `__slots__` use karti hai lekin child nahi, to child ko
  phir bhi `__dict__` mil jata hai (memory benefit khatam) — dono jagah `__slots__` chahiye.
- Default values seedha `__slots__` se nahi mil sakte — `__init__` me set karne padte hain.
- Multiple inheritance me multiple non-empty `__slots__` wali classes combine karna tricky
  (layout conflict) ho sakta hai.
"""))

# ---------------------------------------------------------------------------
# 17. INFO HIDING VS ABSTRACTION
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 16. Information Hiding vs Abstraction — Farq Kya Hai

Ye dono terms aksar confuse hoti hain, interview me bhi poochi jati hain:

| Concept              | Focus                                                                 | Example                                             |
|-----------------------|------------------------------------------------------------------------|------------------------------------------------------|
| **Information Hiding**| Data ko chupana — kaunsa data bahar se access ho sakta hai, kaunsa nahi (`_`, `__`, properties) | `__balance` private rakhna, sirf `deposit()`/`withdraw()` se change hone dena |
| **Abstraction**       | Complexity ko chupana — "kya karna hai" dikhana, "kaise kar raha hai" chupana | `car.start()` call karo, engine ignition ka internal logic pata na ho |

**Simple yaad rakhne ka tareeqa:** Information hiding = **data** chupana (encapsulation ka
hissa). Abstraction = **implementation detail / complexity** chupana (jaise abstract classes,
interfaces — agle advanced notebook me detail me aayega).

Encapsulation in dono ko achieve karne ka mechanism hai — properties/access-modifiers use kar
ke hum information hide karte hain, aur clean method-based API de kar abstraction provide
karte hain.
"""))

# ---------------------------------------------------------------------------
# 18. COMMON MISTAKES / GOTCHAS
# ---------------------------------------------------------------------------
cells.append(md(r"""
## Common Mistakes / Gotchas

1. **Setter ke andar khud ko call karna (infinite recursion).** Setter ke andar
   `self.<same_name> = value` likhna bhool se — hamesha private attribute
   (`self.__name`) me store karo, property name me nahi.
2. **Sochna ke `__x` security hai.** Ye sirf naming convention + name mangling hai —
   `obj._ClassName__x` likh kar koi bhi access/modify kar sakta hai.
3. **`__slots__` + property/class-variable same naam** — class definition time par error.
4. **Getter/setter dono na hona** jab intention read-write ho — sirf `@property` likh kar
   bhool jana ke `@x.setter` bhi chahiye, phir confusion hota hai "attribute set kyun nahi ho raha".
5. **Property ke andar heavy computation** har baar chalana jab woh cheez cache ho sakti thi
   (performance gotcha — agar expensive ho to `functools.cached_property` dekho).
6. **`_protected` ko bahar se seedha access karna** kyunki "Python rokta nahi" — convention
   follow karo, sirf isliye ke chal jata hai iska matlab ye nahi ke sahi hai.

Neeche do live demos — dono safe tareeqe se (`try/except`) dikhaye gaye hain taake koi crash
na ho.
"""))

cells.append(code(r"""
import sys

# MISTAKE #1: setter apne aap ko hi call kar raha hai -> infinite recursion
class BadSetter:
    def __init__(self, value):
        self.value = value   # ye setter call karega

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.value = v   # BUG: 'self.__value' hona chahiye tha, yahan khud 'value' ko hi call kar raha hai

old_limit = sys.getrecursionlimit()
sys.setrecursionlimit(120)   # chhota kar dete hain taake RecursionError jaldi (aur cheap) mil jaye
try:
    bs = BadSetter(10)
except RecursionError:
    print("RecursionError pakड़ liya - common mistake: setter apne aap ko dobara call kar raha hai")
finally:
    sys.setrecursionlimit(old_limit)   # limit wapis normal kar do
"""))

cells.append(code(r"""
# MISTAKE #2: sochna ke __x 'security' deta hai
class Account:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance
    # koi setter nahi - balance sirf deposit/withdraw jaisi methods se change hona chahiye tha

acc2 = Account(100)
acc2._Account__balance = -500   # mangled naam se seedha access karke validation bypass kar diya!
print("Bypass ke baad balance:", acc2.balance)   # -500 -> proof ke __x security nahi, convention hai
assert acc2.balance == -500
"""))

# ---------------------------------------------------------------------------
# 19. REAL-WORLD PROBLEMS
# ---------------------------------------------------------------------------
cells.append(md(r"""
## Real-World Problems

Ab chaar realistic examples dekhte hain jo encapsulation + properties + validation ko sahi
tareeqe se combine karte hain.
"""))

cells.append(md(r"""
### 1. BankAccount — Balance Protection, Deposit/Withdraw with Validation

Requirement: `balance` kabhi bhi seedha set na ho sake (read-only property), sirf
`deposit()`/`withdraw()` ke zariye change ho, aur invalid operations par custom exception aaye.
"""))

cells.append(code(r"""
class InsufficientFundsError(Exception):
    # Custom exception - jab withdraw amount available balance se zyada ho
    pass

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = 0
        if balance > 0:
            self.deposit(balance)   # constructor bhi wahi validated path use karta hai

    @property
    def balance(self):
        return self.__balance   # read-only - koi setter nahi

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount positive hona chahiye")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount positive hona chahiye")
        if amount > self.__balance:
            raise InsufficientFundsError(f"Balance {self.__balance} hai, {amount} withdraw nahi ho sakta")
        self.__balance -= amount
        return self.__balance

acc = BankAccount("Imran", 1000)
print("Starting balance:", acc.balance)
acc.deposit(500)
print("Deposit ke baad:", acc.balance)
acc.withdraw(200)
print("Withdraw ke baad:", acc.balance)

try:
    acc.withdraw(999999)
except InsufficientFundsError as e:
    print("InsufficientFundsError:", e)

try:
    acc.balance = 999999    # property read-only hai
except AttributeError as e:
    print("AttributeError:", e)

assert acc.balance == 1300
"""))

cells.append(md(r"""
### 2. Temperature — Celsius/Fahrenheit Sync

Requirement: `celsius` aur `fahrenheit` dono properties honi chahiye jo hamesha ek doosre ke
sath sync rahen — koi bhi ek badlo, doosra automatically update ho.
"""))

cells.append(code(r"""
class Temperature:
    def __init__(self, celsius=0):
        self.celsius = celsius   # setter call hoga

    @property
    def celsius(self):
        return self.__celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Absolute zero se neeche temperature possible nahi")
        self.__celsius = value

    @property
    def fahrenheit(self):
        return round(self.__celsius * 9 / 5 + 32, 2)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9   # dusre setter ko call kar ke dono sync rehte hain

t = Temperature(25)
print(t.celsius, "C =", t.fahrenheit, "F")

t.fahrenheit = 98.6
print("Fahrenheit set karne ke baad celsius:", round(t.celsius, 2))

try:
    t.celsius = -300
except ValueError as e:
    print("ValueError:", e)

assert t.fahrenheit == 98.6
assert round(t.celsius, 2) == 37.0
"""))

cells.append(md(r"""
### 3. User — Password Hashing (Salt + SHA-256)

Requirement: Plaintext password **kabhi store nahi** karna. Har user ka apna random salt ho,
aur password verify karne ke liye hash compare karo, plaintext nahi.
"""))

cells.append(code(r"""
import hashlib
import secrets

class User:
    def __init__(self, username, password):
        self.username = username
        self.__salt = secrets.token_hex(8)              # har user ke liye random salt
        self.__password_hash = self.__hash_password(password)  # sirf hash store hota hai

    def __hash_password(self, password):
        # salt + password combine kar ke sha256 hash - plaintext kabhi save nahi hota
        return hashlib.sha256((self.__salt + password).encode()).hexdigest()

    def check_password(self, password):
        return self.__hash_password(password) == self.__password_hash

u = User("ahmed123", "MySecret@1")
print("Sahi password check:", u.check_password("MySecret@1"))
print("Ghalat password check:", u.check_password("wrongpass"))

try:
    print(u.__password_hash)    # bahar se seedha access nahi ho sakta (name mangling)
except AttributeError as e:
    print("AttributeError:", e)

assert u.check_password("MySecret@1") is True
assert u.check_password("wrong") is False
"""))

cells.append(md(r"""
### 4. Rectangle — Width/Height/Area/Perimeter

Requirement: `width` aur `height` positive honi chahiye (validated properties), `area` aur
`perimeter` computed (derived) properties hon.
"""))

cells.append(code(r"""
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("width positive honi chahiye")
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("height positive honi chahiye")
        self.__height = value

    @property
    def area(self):
        return self.__width * self.__height

    @property
    def perimeter(self):
        return 2 * (self.__width + self.__height)

r = Rectangle(4, 5)
print("Area:", r.area, "| Perimeter:", r.perimeter)
assert r.area == 20
assert r.perimeter == 18

try:
    r.width = -1
except ValueError as e:
    print("ValueError:", e)
"""))

# ---------------------------------------------------------------------------
# 20. LEETCODE
# ---------------------------------------------------------------------------
cells.append(md(r"""
## LeetCode Problems

Ye problems encapsulation/validation ke angle se choose ki gayi hain — sab me internal state
ko private rakh kar sirf defined methods ke zariye expose karna hai (design-style problems).
"""))

cells.append(md(r"""
### LC 1603. Design Parking System — Easy

https://leetcode.com/problems/design-parking-system/

**Bayan (Roman Urdu):** Ek parking system design karo jisme 3 tarah ki parking spots hain
(big=1, medium=2, small=3), har type ki fixed capacity di gayi hai. `addCar(carType)` method
call hone par agar us type ki jagah bachi hai to car park ho jaye (`True` return), warna
`False`.

**Approach:**
1. Constructor me har car-type ke available slots ko ek private dictionary/counter me store karo.
2. `add_car` me check karo ke counter > 0 hai; agar haan to 1 kam karo aur `True` return karo.
3. Warna `False` return karo.
4. Counters `__slots` (private) rakhte hain taake bahar se koi seedha count na badal sake —
   sirf `add_car()` ke zariye state change ho.

**Time complexity:** O(1) per `add_car` call.
**Space complexity:** O(1) — sirf 3 counters store ho rahe hain.
"""))

cells.append(code(r"""
class ParkingSystem:
    def __init__(self, big: int, medium: int, small: int):
        # private counters - bahar se seedha slots badalne nahi dete, sirf add_car() se change hota hai
        self.__slots = {1: big, 2: medium, 3: small}

    def add_car(self, carType: int) -> bool:
        if self.__slots.get(carType, 0) > 0:
            self.__slots[carType] -= 1
            return True
        return False

ps1 = ParkingSystem(1, 1, 0)
assert ps1.add_car(1) == True     # big slot mila
assert ps1.add_car(2) == True     # medium slot mila
assert ps1.add_car(3) == False    # small ki capacity hi 0 thi
assert ps1.add_car(1) == False    # big ki capacity khatam ho chuki
print("LC 1603 sab test cases pass")
"""))

cells.append(md(r"""
### LC 705. Design HashSet — Easy

https://leetcode.com/problems/design-hashset/

**Bayan (Roman Urdu):** Bina built-in `set`/hash-table library use kiye, apna `MyHashSet`
design karo jisme `add(key)`, `remove(key)`, aur `contains(key)` methods hon.

**Approach (bucket-based, encapsulated internals):**
1. Fixed number of buckets (jaise 1000) le lo, har bucket ek list hai.
2. `key % num_buckets` se index nikalo (simple hashing).
3. `add`: agar key us bucket me nahi hai to append karo (duplicate avoid).
4. `remove`: agar key bucket me hai to list se nikal do.
5. `contains`: bucket ke andar linear search kar ke batao.
6. Buckets aur helper `__index` method dono **private** rakhte hain — user ko sirf
   `add`/`remove`/`contains` API dikhti hai, internal storage encapsulated hai.

**Time complexity:** Average O(1) per operation (agar keys buckets me achi tarah distribute hon),
worst case O(n/buckets) ek bucket ke andar linear scan ki wajah se.
**Space complexity:** O(n + buckets) jahan n = stored keys ki tadaad.
"""))

cells.append(code(r"""
class MyHashSet:
    def __init__(self):
        self.__size = 1000
        self.__buckets = [[] for _ in range(self.__size)]   # encapsulated internal storage

    def __index(self, key):
        return key % self.__size   # private helper - bahar se call nahi hota (name mangled)

    def add(self, key: int) -> None:
        idx = self.__index(key)
        if key not in self.__buckets[idx]:
            self.__buckets[idx].append(key)

    def remove(self, key: int) -> None:
        idx = self.__index(key)
        if key in self.__buckets[idx]:
            self.__buckets[idx].remove(key)

    def contains(self, key: int) -> bool:
        idx = self.__index(key)
        return key in self.__buckets[idx]

hs = MyHashSet()
hs.add(1)
hs.add(2)
assert hs.contains(1) == True
assert hs.contains(3) == False
hs.add(2)                  # duplicate add - koi asar nahi hona chahiye
assert hs.contains(2) == True
hs.remove(2)
assert hs.contains(2) == False
print("LC 705 sab test cases pass")
"""))

cells.append(md(r"""
### LC 1470. Shuffle the Array — Easy

https://leetcode.com/problems/shuffle-the-array/

**Bayan (Roman Urdu):** Array `nums` di gayi hai length `2n`, jisme `[x1,...,xn,y1,...,yn]`
format me numbers hain. Isay `[x1,y1,x2,y2,...,xn,yn]` format me shuffle kar ke return karo.

**Approach:** Direct simulation — pehle half aur doosre half se ek-ek element interleave
(alternately) karte jao.

**Time complexity:** O(n).
**Space complexity:** O(n) — result array ke liye.
"""))

cells.append(code(r"""
def shuffle(nums: list[int], n: int) -> list[int]:
    result = []
    for i in range(n):
        result.append(nums[i])        # pehle half se element
        result.append(nums[i + n])    # doosre half se corresponding element
    return result

assert shuffle([2, 5, 1, 3, 4, 7], 3) == [2, 3, 5, 4, 1, 7]
assert shuffle([1, 2, 3, 4, 4, 3, 2, 1], 4) == [1, 4, 2, 3, 3, 2, 4, 1]
assert shuffle([1, 1, 2, 2], 2) == [1, 2, 1, 2]
print("LC 1470 sab test cases pass")
"""))

cells.append(md(r"""
### LC 2160. Minimum Sum of Four Digit Number After Splitting Digits — Easy

https://leetcode.com/problems/minimum-sum-of-four-digit-number-after-splitting-digits/

**Bayan (Roman Urdu):** Ek 4-digit number diya hai. Uske digits ko do naye 2-digit numbers me
split karo (koi bhi combination), taake dono ka sum **minimum** ho. Sum return karo.

**Approach:** Digits ko sort kar do (chhote pehle). Sabse chhote 2 digits dono numbers ke
**tens place** me daalo, aur bache hue 2 (bade) digits **ones place** me — isse sum minimum
hota hai (kyunki tens place ki value 10x zyada matter karti hai, is liye wahan chhote digits
hone chahiye).

**Time complexity:** O(1) — hamesha sirf 4 digits hain (sorting bhi O(4 log 4) = O(1)).
**Space complexity:** O(1).
"""))

cells.append(code(r"""
def minimum_sum(num: int) -> int:
    digits = sorted(str(num))                   # chhote digits pehle aa jayenge
    n1 = int(digits[0] + digits[2])              # sabse chhota + teesra chhota -> tens+ones
    n2 = int(digits[1] + digits[3])              # doosra chhota + sabse bada -> tens+ones
    return n1 + n2

assert minimum_sum(2932) == 52     # digits sorted: 2,2,3,9 -> 22 + 39 ya 23+29, min sum = 52
assert minimum_sum(4009) == 13     # digits sorted: 0,0,4,9 -> 04 + 09 = 13
print("LC 2160 sab test cases pass")
"""))

# ---------------------------------------------------------------------------
# 21. INTERVIEW Q&A
# ---------------------------------------------------------------------------
cells.append(md(r"""
## Interview Questions & Answers

**Q1. Encapsulation ka matlab kya hai, ek line me?**
A. Data aur us par kaam karne wale methods ko ek unit (class) me bundle karna, aur direct
uncontrolled access se protect karna.

**Q2. Python me "true private" attributes hote hain?**
A. Nahi. `__x` sirf naming convention + name mangling hai (`_ClassName__x`), enforce nahi
hoti — koi bhi mangled naam se access kar sakta hai.

**Q3. Name mangling kya hai aur kis liye hai?**
A. `self.__x` ko Python compile time par `self._ClassName__x` me convert karta hai, taake
subclasses accidentally parent ki "private" cheezein overwrite na karen — security ke liye
nahi.

**Q4. `_x` aur `__x` me farq?**
A. `_x` (single underscore) sirf convention hai — "internal use", bilkul normal access hota
hai. `__x` (double underscore) name-mangled hota hai — thoda extra mushkil access karna.

**Q5. `@property` kyun use karte hain instead of plain attribute?**
A. Taake attribute-jaisi syntax (`obj.x`) rakh sakein lekin validation/computation bhi kar
saken, aur baad me plain attribute se property me refactor karne par purana calling code na
tootey.

**Q6. `@property` aur `property()` function me farq?**
A. Koi functional farq nahi — `@property` decorator sirf `property()` builtin ka syntactic
sugar hai. Dono same kaam karte hain.

**Q7. Read-only property kaise banate hain?**
A. Sirf `@property` (getter) define karo, `@x.setter` bilkul mat likho — assignment karne par
Python khud `AttributeError` dega.

**Q8. Setter ke andar `self.x = value` likhna kyun galat hai (agar property ka naam bhi `x` ho)?**
A. Isse infinite recursion hoti hai — setter khud ko dobara call karta rehta hai. Hamesha
private backing attribute (`self.__x`) me store karo.

**Q9. `__slots__` kyun use karte hain?**
A. Memory bachane ke liye (per-instance `__dict__` avoid ho jata hai) aur typo-protection ke
liye (naye/galat attribute names silently allow nahi hote).

**Q10. `__slots__` ki limitation/gotcha bata do.**
A. Agar `__slots__` me koi naam property/class-variable ke naam se clash kare to class
definition time par error aata hai. Inheritance me sab classes me `__slots__` chahiye warna
benefit khatam ho jata hai.

**Q11. Encapsulation vs Abstraction — farq?**
A. Encapsulation = data ko bundle + protect karna (information hiding). Abstraction =
implementation complexity chupana, sirf "kya karna hai" (interface) dikhana.

**Q12. Custom exception classes kyun banate hain generic `ValueError` ke bajaye?**
A. Domain-specific error handling ke liye — calling code specific `except InvalidAgeError`
laga sakta hai, aur error messages/behaviour zyada meaningful hote hain.

**Q13. Class-level constant instance attribute se kaise differ karta hai?**
A. Class-level constant class ke andar (methods se bahar) define hota hai, sab instances
ek hi value share karte hain (memory bhi shared). Instance attribute har object ka apna alag
hota hai.

**Q14. Kya property ke andar validation fail hone par object create hi nahi hoga?**
A. Agar constructor (`__init__`) me validated property set ki jaye aur validation fail ho, to
`__init__` exception raise karega aur object banega hi nahi (partially-constructed object
zyada dair tak nahi rehta jab tak explicitly try/except na lagaya jaye).

**Q15. Password kabhi plaintext store kyun nahi karni chahiye?**
A. Agar database leak ho jaye to attacker seedha passwords padh lega. Isliye salt + strong
hash (jaise SHA-256, ya production me bcrypt/argon2) store karte hain, aur verify karte waqt
hash compare karte hain.

**Q16. `hasattr()` / `getattr()` encapsulation ke sath kaise use hote hain?**
A. `getattr(obj, 'x', default)` safe access deta hai bina `AttributeError` crash kiye —
`hasattr` check karta hai attribute exist karta hai ya nahi. Private/mangled attributes ke
sath bhi kaam karte hain agar mangled naam pass karo.

**Q17. Property ke andar exception raise karna theek hai?**
A. Haan — property getter/setter normal methods hi hain, exceptions raise kar sakte hain.
Bas caller ko pata hona chahiye ke `obj.x = value` fail ho sakta hai.
"""))

# ---------------------------------------------------------------------------
# 22. PRACTICE EXERCISES
# ---------------------------------------------------------------------------
cells.append(md(r"""
## Practice Exercises (khud karo)

1. **Wallet class** banao jisme `__balance` private ho, `add_funds(amount)` aur
   `spend(amount)` methods hon, `balance` ek read-only property ho.
   *Hint:* BankAccount example dekho, `InsufficientFundsError` jaisa custom exception use karo.

2. **Temperature3** class banao jisme `celsius`, `fahrenheit`, aur `kelvin` teenon properties
   sync rahen (kisi bhi ek ko set karo, baaki do automatically update hon).
   *Hint:* `kelvin = celsius + 273.15`.

3. **Product** class banao jisme `price` property ho jo kabhi negative na ho sake, aur
   `discounted_price(percent)` method ho jo computed value return kare (property nahi,
   kyunki argument leta hai).
   *Hint:* property method argument nahi le sakti — is liye ye normal method hona chahiye.

4. **`__slots__` wali `Point3D` class** banao (`x`, `y`, `z`) aur dikhao ke naya attribute
   (`w`) add karne ki koshish `AttributeError` deti hai.
   *Hint:* upar `PointSlots` example dekho.

5. **Password class** banao jo `set_password(raw)` method me strength validate kare (kam az
   kam 8 characters, ek digit, ek uppercase) — invalid hone par custom
   `WeakPasswordError` raise kare.
   *Hint:* `Student.age` setter jaisa validation pattern use karo.

6. **ReadOnlyConfig** class banao jisme constructor me values set hon lekin baad me koi bhi
   attribute change na ho sake (har property read-only ho).
   *Hint:* sirf getters define karo, koi setter nahi.

7. **BackwardsCompatible refactor practice:** Apni koi purani class lo jisme plain attribute
   tha, usay property me convert karo bina us class ko use karne wale kisi bhi test/code ko
   todey.
   *Hint:* RectangleV1 → RectangleV2 pattern follow karo.

8. **User class ko improve karo:** `change_password(old, new)` method add karo jo pehle
   `old` verify kare (`check_password`), phir hi `new` set kare.
   *Hint:* `check_password` already defined hai upar.
"""))

# ---------------------------------------------------------------------------
# 23. SUMMARY / CHEAT-SHEET
# ---------------------------------------------------------------------------
cells.append(md(r"""
## Summary / Cheat-Sheet

| Concept | Syntax | Note |
|---|---|---|
| Public | `self.x` | Kahin se bhi access |
| Protected | `self._x` | Convention only, enforce nahi hota |
| Private | `self.__x` | Name-mangled to `_ClassName__x`, security nahi |
| Getter (property) | `@property` upar `def x(self): return self.__x` | `obj.x` — no `()` |
| Setter | `@x.setter` upar `def x(self, value): ...` | `obj.x = value` |
| Deleter | `@x.deleter` upar `def x(self): del self.__x` | `del obj.x` |
| Read-only | Sirf getter define karo | Set karne par `AttributeError` |
| Old-style property | `x = property(getter, setter, deleter, doc)` | Same as decorator |
| Custom exception | `class MyError(Exception): pass` | Domain-specific error handling |
| Class constant | Class body me `CONST = value` | Sab instances share karte hain |
| `__slots__` | `__slots__ = ("x", "y")` | Memory + typo-protection, `__dict__` khatam |

**Golden rules:**
- Encapsulation = data bundle + protect. Abstraction = implementation complexity chupana.
- `@property` se attribute-jaisi syntax milti hai, validation/computation ke sath.
- Setter ke andar hamesha **private mangled attribute** me store karo, property name khud
  me nahi (warna infinite recursion).
- Python "private" ko force nahi karta — ye convention + team discipline par depend karta hai
  ("we are all consenting adults").
- Plain attribute se property me refactor karna backwards-compatible hota hai — is liye shuru
  me simple rakho, baad me zaroorat par property add karo.

**Aage kya:** Agla notebook — Inheritance aur Polymorphism.
"""))

save(r"OOP in Python/Basics/02_Encapsulation_Access_Modifiers_and_Properties.ipynb", cells)
