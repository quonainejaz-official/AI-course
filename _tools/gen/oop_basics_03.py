import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ---------------------------------------------------------------------------
# 1. TITLE
# ---------------------------------------------------------------------------
cells.append(md(r"""
# 03 — Inheritance, Polymorphism aur Method Overriding

**Level:** Beginner → Advanced (interview prep + university syllabus)

Ye OOP series ka teesra notebook hai. Notebook 01 me classes/objects banaye, notebook 02 me
data ko encapsulate kiya. Ab hum seekhenge ke **purane code ko dobara likhe baghair naye
classes kaise banate hain** (inheritance), aur ek hi function/loop different types ke objects
ke sath kaise kaam karta hai (polymorphism).

Ye do concepts interview me sab se zyada poochhe jaate hain — khaas kar `super()`, MRO aur
duck typing.

## Is notebook me kya seekhenge (roadmap)

1. Inheritance kya hai, kyun chahiye (code reuse + IS-A relationship)
2. Base / derived (parent / child, super / sub) terminology aur syntax
3. Attribute aur method inheritance — `object` sab ka baap
4. Inheritance ke types: single, multilevel, hierarchical, multiple, hybrid
5. Method overriding — parent ka behaviour badalna
6. `super()` — with args aur without args, parent constructor call
7. `super()` multilevel chain me kaise travel karta hai
8. Parent method ko extend karna (replace vs extend)
9. MRO — `__mro__`, C3 linearization ka basic idea, diamond problem
10. Cooperative multiple inheritance aur **mixins** (`**kwargs` pattern)
11. `isinstance` vs `issubclass` vs `type()`
12. Method resolution debugging — koi method aakhir kahan se aaya?
13. Inheritance me `_protected` vs `__private` (name mangling ka asar)
14. Polymorphism — same interface, different classes
15. Duck typing — "agar duck ki tarah quack karta hai to duck hai"
16. Operator overloading intro — `__add__`, `__eq__`, `__lt__`
17. Method overloading Python me kyun nahi + 3 workarounds (default args, `*args`, `singledispatch`)
18. Base class me `NotImplementedError` se contract enforce karna
19. Composition vs inheritance (has-a vs is-a) — "favour composition"
20. Common mistakes / gotchas (LSP, bhoola hua `super().__init__`, shared mutable class attribute)
21. Real-world problems (payroll, notifications, shapes, exporters, bank accounts)
22. LeetCode problems — LC 703, LC 933, LC 1352 (asserts ke sath)
23. Interview Q&A (20 sawal)
24. Practice exercises
25. Cheat-sheet

## Prerequisites

- Notebook 01 (classes, `__init__`, `self`, instance vs class attributes)
- Notebook 02 (encapsulation, `@property`, name mangling ki basic samajh)
- Functions, `*args` / `**kwargs` ki basic samajh
"""))

# ---------------------------------------------------------------------------
# 2. INHERITANCE KYA HAI
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 1. Inheritance kya hai aur kyun chahiye?

**Kya hai:** Inheritance ka matlab hai ek class (child) doosri class (parent) ki
attributes aur methods **automatically** haasil kar leti hai — dobara likhne ki zaroorat nahi.

**Kyun:**

- **Code reuse** — common cheezein ek jagah (parent me) likho, sab children use karein.
- **IS-A relationship** model karna — `Dog` IS-A `Animal`, `Manager` IS-A `Employee`.
- **Single point of change** — bug parent me theek karo, sab children theek ho gaye.
- **Polymorphism ki bunyaad** — ek hi type (parent) ki tarah treat kar sakte hain.

**Syntax:**

```python
class Parent:
    ...

class Child(Parent):      # bracket me parent ka naam
    ...
```

Neeche pehle **bina inheritance** wala code dekho — duplication saaf nazar aayegi.
"""))

cells.append(code(r"""
# ---- BINA inheritance: duplication ka masla ----------------------------------
class DogNoInherit:
    def __init__(self, name, age):
        self.name = name          # duplicate
        self.age = age            # duplicate

    def eat(self):                # duplicate
        return f"{self.name} kha raha hai"

    def sleep(self):              # duplicate
        return f"{self.name} so raha hai"

    def speak(self):              # sirf ye alag hai!
        return "Bhow bhow!"


class CatNoInherit:
    def __init__(self, name, age):
        self.name = name          # phir wahi
        self.age = age            # phir wahi

    def eat(self):                # phir wahi
        return f"{self.name} kha raha hai"

    def sleep(self):              # phir wahi
        return f"{self.name} so raha hai"

    def speak(self):              # sirf ye alag
        return "Meow!"


d = DogNoInherit("Tommy", 3)
c = CatNoInherit("Billi", 2)
print(d.eat(), "|", d.speak())
print(c.eat(), "|", c.speak())

# Masla: eat/sleep/__init__ ka code 2 baar likha. Agar 10 animals hon to 10 baar!
# Aur agar eat() me bug ho, 10 jagah theek karna paray ga.
print("\nDuplicate methods ka count (har class me eat/sleep/__init__):", 3)
"""))

cells.append(code(r"""
# ---- WITH inheritance: common code aik jagah --------------------------------
class Animal:
    "Base / parent / super class — sab animals ka common behaviour."

    def __init__(self, name, age):
        self.name = name                      # common attribute
        self.age = age

    def eat(self):                            # common method
        return f"{self.name} kha raha hai"

    def sleep(self):
        return f"{self.name} so raha hai"

    def speak(self):
        # Base class me generic jawab; children isay override karenge
        return "..."


class Dog(Animal):        # Dog IS-A Animal
    def speak(self):      # sirf farq wali cheez likhi
        return "Bhow bhow!"


class Cat(Animal):        # Cat IS-A Animal
    def speak(self):
        return "Meow!"


d = Dog("Tommy", 3)
c = Cat("Billi", 2)

# eat/sleep/__init__ hum ne Dog/Cat me likhe hi nahi — parent se mile
print(d.eat(), "|", d.speak())      # Tommy kha raha hai | Bhow bhow!
print(c.sleep(), "|", c.speak())    # Billi so raha hai | Meow!

# name/age bhi parent ke __init__ se set hue
print("Dog ka naam:", d.name, "| age:", d.age)

# Proof: Dog ke apne body me sirf speak hai
print("\nDog class body me define hua:", [k for k in Dog.__dict__ if not k.startswith('_')])
print("Magar available methods:", [m for m in dir(d) if not m.startswith('_')])
"""))

# ---------------------------------------------------------------------------
# 3. TERMINOLOGY + object root
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 2. Terminology aur `object` — sab ka baap

Ek hi cheez ke kai naam hain (interview me koi bhi use ho sakta hai):

| Parent ke naam | Child ke naam |
|---|---|
| Base class | Derived class |
| Super class | Sub class |
| Parent class | Child class |

**Ahem baat:** Python me har class **implicitly** `object` se inherit karti hai (Python 3 me).
Is liye `__str__`, `__eq__`, `__hash__`, `__class__` waghera har object me hote hain.

- `Class.__bases__` → direct parents ka tuple
- `Class.__mro__` → poori lookup chain
- `Class.__subclasses__()` → direct children ki list
"""))

cells.append(code(r"""
# ---- object root aur introspection ------------------------------------------
class Plain:      # koi parent nahi likha...
    pass

print("Plain ke bases:", Plain.__bases__)          # (<class 'object'>,) -> object automatic
print("Dog ke bases:", Dog.__bases__)              # (<class 'Animal'>,)
print("Animal ke bases:", Animal.__bases__)        # (<class 'object'>,)

# Animal ke direct children
print("Animal ke subclasses:", [c.__name__ for c in Animal.__subclasses__()])

# Poori chain (MRO — method resolution order)
print("Dog ki MRO:", [c.__name__ for c in Dog.__mro__])   # Dog -> Animal -> object

# object se mile methods (hum ne kabhi nahi likhe)
d2 = Dog("Sheru", 1)
print("\nrepr (object se default):", repr(d2)[:40], "...")
print("__eq__ maujood hai?", hasattr(d2, "__eq__"))

assert Plain.__bases__ == (object,)
assert Dog.__mro__ == (Dog, Animal, object)
print("\n[ok] har class object se inherit karti hai")
"""))

# ---------------------------------------------------------------------------
# 4. TYPES OF INHERITANCE
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 3. Inheritance ke types (university exam ka favourite sawal)

| Type | Shakal | Matlab |
|---|---|---|
| **Single** | `A → B` | Ek child, ek parent |
| **Multilevel** | `A → B → C` | Dada → baap → beta ki chain |
| **Hierarchical** | `A → B`, `A → C` | Ek parent, kai children |
| **Multiple** | `A, B → C` | Ek child, kai parents |
| **Hybrid** | Upar walon ka mix | Aksar diamond shape banti hai |

Aage har type ka chalta hua example hai. Dhyan do ke **multiple inheritance** Python ka
special feature hai — Java/C# me classes ke liye allowed nahi (wahan interfaces use hote hain).
"""))

cells.append(code(r"""
# ============ 1) SINGLE INHERITANCE: A -> B ==================================
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        return f"{self.brand} start ho gayi"


class Car(Vehicle):                 # single: Car ka sirf ek parent
    def wheels(self):
        return 4


c = Car("Toyota")
print("start():", c.start())        # parent se
print("wheels():", c.wheels())      # apna
print("MRO:", [k.__name__ for k in Car.__mro__])
assert isinstance(c, Vehicle)       # Car IS-A Vehicle
print("[ok] single inheritance")
"""))

cells.append(code(r"""
# ============ 2) MULTILEVEL INHERITANCE: A -> B -> C =========================
class LivingThing:
    def breathe(self):
        return "saans le raha hai"


class Mammal(LivingThing):          # level 2
    def feed_milk(self):
        return "doodh pilata hai"


class Human(Mammal):                # level 3 — dono se sab kuch milta hai
    def talk(self):
        return "baat karta hai"


h = Human()
print(h.breathe())      # dada (LivingThing) se
print(h.feed_milk())    # baap (Mammal) se
print(h.talk())         # apna
print("MRO:", [k.__name__ for k in Human.__mro__])

# Multilevel me chain ke har member ka isinstance True hota hai
assert isinstance(h, Human) and isinstance(h, Mammal) and isinstance(h, LivingThing)
print("[ok] multilevel inheritance")
"""))

cells.append(code(r"""
# ============ 3) HIERARCHICAL INHERITANCE: ek parent, kai children ===========
class Shape:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"Main ek {self.name} hoon"


class Circle(Shape):
    def __init__(self, r):
        super().__init__("circle")     # parent ka constructor
        self.r = r

    def area(self):
        return 3.14159 * self.r ** 2


class Square(Shape):
    def __init__(self, side):
        super().__init__("square")
        self.side = side

    def area(self):
        return self.side ** 2


class Triangle(Shape):
    def __init__(self, b, hgt):
        super().__init__("triangle")
        self.b, self.hgt = b, hgt

    def area(self):
        return 0.5 * self.b * self.hgt


for s in (Circle(2), Square(3), Triangle(4, 5)):
    # Sab ka describe() same (parent se), area() apna apna -> ye polymorphism ki jhalak
    print(f"{s.describe():<25} area = {s.area():.2f}")

print("\nShape ke children:", [k.__name__ for k in Shape.__subclasses__()])
print("[ok] hierarchical inheritance")
"""))

cells.append(code(r"""
# ============ 4) MULTIPLE INHERITANCE: kai parents, ek child =================
class Engine:
    def __init__(self):
        self.power = "petrol engine"

    def start_engine(self):
        return "engine chalu"


class MusicSystem:
    def __init__(self):
        self.speakers = 4

    def play(self):
        return "gaana chal raha hai"


class LuxuryCar(Engine, MusicSystem):     # dono parents se features
    def __init__(self):
        # DHYAN: dono parents ke __init__ khud call karne parte hain (yahan explicit style)
        Engine.__init__(self)
        MusicSystem.__init__(self)

    def summary(self):
        return f"{self.power}, {self.speakers} speakers"


lc = LuxuryCar()
print(lc.start_engine())      # Engine se
print(lc.play())              # MusicSystem se
print(lc.summary())
print("MRO:", [k.__name__ for k in LuxuryCar.__mro__])

assert isinstance(lc, Engine) and isinstance(lc, MusicSystem)
print("[ok] multiple inheritance")
"""))

cells.append(code(r"""
# ============ 5) HYBRID INHERITANCE (mix — aksar diamond) ====================
#        Device
#        /     \
#   Phone     Camera
#        \     /
#      SmartPhone
class Device:
    def info(self):
        return "ek electronic device"


class Phone(Device):
    def call(self):
        return "call ja rahi hai"


class Camera(Device):
    def click(self):
        return "photo li gayi"


class SmartPhone(Phone, Camera):      # hybrid: hierarchical + multiple
    def info(self):
        # parent chain ka info() bhi use kar sakte hain
        return "smartphone = " + super().info()


sp = SmartPhone()
print(sp.call())
print(sp.click())
print(sp.info())
print("MRO:", [k.__name__ for k in SmartPhone.__mro__])
# NOTE: Device sirf EK baar MRO me aaya — C3 linearization ka kamaal (diamond problem hal)
assert [k.__name__ for k in SmartPhone.__mro__] == [
    "SmartPhone", "Phone", "Camera", "Device", "object"
]
print("[ok] hybrid inheritance")
"""))

# ---------------------------------------------------------------------------
# 5. METHOD OVERRIDING
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 4. Method Overriding

**Kya hai:** Child class me **wahi naam** ka method dobara define karna jo parent me hai.
Object par call karne se **child** ka version chalta hai (parent ka chhup jaata hai).

**Kyun:** Parent ka generic behaviour child ke liye specific banana.

**Rules / baatein:**

- Naam same hona chahiye. Python signature match **check nahi karta** (Java ki tarah strict nahi),
  magar signature badalna **LSP** (Liskov Substitution Principle) tor deta hai — gotchas me dekhenge.
- Overriding = **runtime** par decide hota hai (dynamic dispatch), object ke actual class par.
- Parent ka version phir bhi milta hai: `super().method()` ya `Parent.method(self)`.
- Attributes bhi override ho sakti hain (class attribute shadowing).
"""))

cells.append(code(r"""
# ---- overriding: basic + parent version tak pohnchna ------------------------
class Employee:
    raise_pct = 5                      # class attribute

    def __init__(self, name, salary):
        self.name, self.salary = name, salary

    def annual_salary(self):
        return self.salary * 12

    def role(self):
        return "Employee"


class Manager(Employee):
    raise_pct = 10                     # class attribute OVERRIDE

    def annual_salary(self):           # method OVERRIDE (bonus add kiya)
        base = super().annual_salary() # parent ka kaam dobara na likho — reuse karo
        return base + 100_000          # manager ko bonus

    def role(self):
        return "Manager"


e = Employee("Ali", 50_000)
m = Manager("Sara", 80_000)

print(f"{e.name:<6} {e.role():<10} annual = {e.annual_salary():,}")
print(f"{m.name:<6} {m.role():<10} annual = {m.annual_salary():,}  (bonus shamil)")
print("raise_pct — Employee:", Employee.raise_pct, "| Manager:", Manager.raise_pct)

# Parent ka version zabardasti chalana (2 tareeqe)
print("\nParent ka annual (super style):", Employee.annual_salary(m))    # 80000*12
print("Child ka annual:", m.annual_salary())

assert e.annual_salary() == 600_000
assert m.annual_salary() == 80_000 * 12 + 100_000
print("[ok] overriding")
"""))

# ---------------------------------------------------------------------------
# 6. super()
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 5. `super()` — parent tak pohnchne ka sahi tareeqa

**Kya hai:** `super()` ek **proxy object** deta hai jo MRO me **agli** class ko point karta hai
(sirf "parent" nahi — MRO me next!). Ye farq multiple inheritance me bohat maayne rakhta hai.

**Do forms:**

```python
super()                      # Python 3 ka short form (sab se behtar) — sirf class body ke andar
super(Manager, self)         # purana explicit form (Python 2 style, ab bhi valid)
super(Manager, Manager)      # unbound-ish; classmethods me kaam aata hai
```

**Kyun `super()` behtar hai `Parent.method(self)` se:**

1. Parent ka naam change ho to code nahi tootta (DRY).
2. Multiple inheritance me **poori chain** cooperate karti hai (koi parent skip nahi hota).
3. Diamond me parent ka `__init__` **do baar** nahi chalta.

**Golden rule:** child ke `__init__` me pehla kaam aksar `super().__init__(...)` hona chahiye
(ya jab base ka state chahiye us se pehle).
""" ))

cells.append(code(r"""
# ---- super() ke dono forms + parent constructor call ------------------------
class Person:
    def __init__(self, name, cnic):
        self.name = name
        self.cnic = cnic
        print(f"  [Person.__init__] name={name}")

    def intro(self):
        return f"Main {self.name} hoon"


class Student(Person):
    def __init__(self, name, cnic, roll_no):
        super().__init__(name, cnic)        # short form — recommended
        self.roll_no = roll_no
        print(f"  [Student.__init__] roll_no={roll_no}")

    def intro(self):
        # parent ka string lo aur extend karo
        return super().intro() + f", roll no {self.roll_no}"


class Teacher(Person):
    def __init__(self, name, cnic, subject):
        super(Teacher, self).__init__(name, cnic)   # purana explicit form — same natija
        self.subject = subject

    def intro(self):
        return Person.intro(self) + f", {self.subject} parhata hoon"   # 3rd tareeqa


print("Student banate waqt:")
s = Student("Bilal", "35202-1", "CS-101")
print(s.intro())

print("\nTeacher:")
t = Teacher("Ahmed", "35202-2", "Physics")
print(t.intro())

print("\nsuper() object khud kya hai?:", super(Student, s))
assert s.name == "Bilal" and s.roll_no == "CS-101"
print("[ok] super() forms")
"""))

cells.append(code(r"""
# ---- BHOOLA HUA super().__init__() = tootay hue objects ---------------------
class BadStudent(Person):
    def __init__(self, name, cnic, roll_no):
        # GALTI: super().__init__ call nahi kiya
        self.roll_no = roll_no


bs = BadStudent("Kashif", "35202-3", "CS-202")
try:
    print(bs.intro())            # self.name maujood hi nahi!
except AttributeError as err:
    print("AttributeError:", err)

print("bs ka __dict__:", bs.__dict__)     # sirf roll_no — name/cnic ghayab
print("\nSabaq: parent ka __init__ call karna TUMHARI zimmedari hai; Python khud nahi karta.")
"""))

cells.append(md(r"""
## 6. `super()` multilevel chain me — cooperative call

`super()` **ek** parent ko call karta hai, phir wo parent apna `super()` call karta hai...
is tarah poori chain chalti hai. Isay **cooperative inheritance** kehte hain.

Neeche print statements se dekho ke chain neeche se upar jaati hai (`C → B → A → object`),
aur wapsi (return) upar se neeche aati hai.
"""))

cells.append(code(r"""
# ---- 3-level cooperative chain ---------------------------------------------
class A:
    def __init__(self):
        print("A.__init__ shuru")
        # object.__init__ tak jaana zaroori nahi, magar cooperative style me acha hai
        super().__init__()
        self.a = "A-data"
        print("A.__init__ khatam")

    def whoami(self):
        return "A"


class B(A):
    def __init__(self):
        print(" B.__init__ shuru")
        super().__init__()          # A.__init__ chalega
        self.b = "B-data"
        print(" B.__init__ khatam")

    def whoami(self):
        return "B -> " + super().whoami()


class C(B):
    def __init__(self):
        print("  C.__init__ shuru")
        super().__init__()          # B.__init__ chalega (jo A ko call karega)
        self.c = "C-data"
        print("  C.__init__ khatam")

    def whoami(self):
        return "C -> " + super().whoami()


obj = C()
print("\nSab data mila:", obj.__dict__)
print("whoami chain:", obj.whoami())        # C -> B -> A

assert obj.whoami() == "C -> B -> A"
assert set(obj.__dict__) == {"a", "b", "c"}
print("[ok] cooperative multilevel super()")
"""))

# ---------------------------------------------------------------------------
# 7. MRO
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 7. MRO (Method Resolution Order) aur Diamond Problem

**Kya hai:** MRO wo **tarteeb** hai jis me Python attribute/method dhoondta hai.
Dekhne ke 3 tareeqe: `Class.__mro__`, `Class.mro()`, `help(Class)`.

**Diamond problem:**

```
      D
     / \
    B   C
     \ /
      A
```

`D` me `B` aur `C` dono hain, dono ka parent `A` hai. Sawal: `A` ka method kitni baar chalega?
Purani languages (C++) me duplication ka masla hota hai. Python **C3 linearization** algorithm
use karta hai:

1. Class khud pehle
2. Parents left-to-right ki tarteeb me
3. **Koi class apne kisi bhi parent se pehle** aati hai (monotonicity)
4. Har class MRO me **sirf ek baar**

Nateeja: `D → B → C → A → object`. `A` sirf ek baar — is liye cooperative `super()` ke sath
`A.__init__` bhi sirf ek baar chalta hai.

**Interview tip:** "Python me diamond problem hoti hai?" → "Ambiguity C3 MRO se hal ho jaati
hai, magar agar hierarchy inconsistent ho to Python `TypeError` de kar class banane hi nahi deta."
"""))

cells.append(code(r"""
# ---- diamond: A ka __init__ sirf EK baar chalta hai ------------------------
class DA:
    def __init__(self):
        print("DA.__init__ (base) chala")
        super().__init__()

    def greet(self):
        return "DA"


class DB(DA):
    def __init__(self):
        print("DB.__init__ chala")
        super().__init__()

    def greet(self):
        return "DB -> " + super().greet()


class DC(DA):
    def __init__(self):
        print("DC.__init__ chala")
        super().__init__()

    def greet(self):
        return "DC -> " + super().greet()


class DD(DB, DC):
    def __init__(self):
        print("DD.__init__ chala")
        super().__init__()

    def greet(self):
        return "DD -> " + super().greet()


print("DD() banate waqt (dhyan do DA ek hi baar):")
dd = DD()
print("\nMRO:", [k.__name__ for k in DD.__mro__])
print("greet chain:", dd.greet())

# DB ka super() DA nahi, balke DC hai! Kyunke MRO me DB ke baad DC aata hai.
print("\nAHEM: DB ke andar super() ka matlab DD ki MRO par depend karta hai (DC), na ke DB par.")
assert dd.greet() == "DD -> DB -> DC -> DA"
assert [k.__name__ for k in DD.__mro__] == ["DD", "DB", "DC", "DA", "object"]
print("[ok] diamond + C3")
"""))

cells.append(code(r"""
# ---- jab MRO banana NAMUMKIN ho: TypeError -------------------------------
class X: pass
class Y: pass


class P1(X, Y): pass          # yahan tarteeb: X phir Y
class P2(Y, X): pass          # yahan ulti tarteeb: Y phir X

try:
    # P1 kehti hai X<Y, P2 kehti hai Y<X -> consistent order namumkin
    class Broken(P1, P2): pass
except TypeError as err:
    print("TypeError:", err)

print("\nSabaq: C3 sirf 'hal' nahi karta — inconsistent hierarchy ko REJECT kar deta hai,")
print("aur ye acha hai: masla class definition par pakra gaya, runtime par nahi.")

# Sahi tarteeb:
class Fine(P1, X): pass
print("Fine ki MRO:", [k.__name__ for k in Fine.__mro__])
"""))

cells.append(md(r"""
## 8. Cooperative Multiple Inheritance aur **Mixins**

**Mixin** = chhoti class jo **sirf ek extra feature** deti hai, akeli use nahi hoti,
aur usually apna `__init__`/state nahi rakhti. Naming convention: `...Mixin`.

Faida: features ko "plug" karna without deep hierarchy — Django/DRF isi par bana hai.

**Kwargs pattern (bohat ahem):** agar chain ke different classes different arguments lete hain,
to `**kwargs` accept karo aur baqi `super().__init__(**kwargs)` ko aage bhej do.
Is tarah har class apna hissa nikaal leti hai aur chain tootti nahi.
"""))

cells.append(code(r"""
import json, io, csv

# ---- Mixins: chhote, focused features -------------------------------------
class JSONMixin:
    "Object ko JSON me badalne ki salahiyat deta hai (state nahi rakhta)."
    def to_json(self):
        # __dict__ ka use — sab public instance attributes
        return json.dumps(self.__dict__, ensure_ascii=False, sort_keys=True)


class CSVRowMixin:
    "Object ko CSV row me badalta hai."
    def to_csv_row(self):
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="")
        w.writerow([self.__dict__[k] for k in sorted(self.__dict__)])
        return buf.getvalue()


class ReprMixin:
    "Achha __repr__ mufat me."
    def __repr__(self):
        args = ", ".join(f"{k}={v!r}" for k, v in sorted(self.__dict__.items()))
        return f"{type(self).__name__}({args})"


class Product(JSONMixin, CSVRowMixin, ReprMixin):     # 3 features plug-in
    def __init__(self, name, price):
        self.name, self.price = name, price


p = Product("Laptop", 150000)
print("repr :", repr(p))                 # ReprMixin se
print("json :", p.to_json())             # JSONMixin se
print("csv  :", p.to_csv_row())          # CSVRowMixin se
print("MRO  :", [k.__name__ for k in Product.__mro__])

assert json.loads(p.to_json())["price"] == 150000
print("[ok] mixins")
"""))

cells.append(code(r"""
# ---- **kwargs pattern: har class apna hissa leti hai, baqi aage bhejti hai --
class Base:
    def __init__(self, **kwargs):
        # chain ka aakhir — yahan kwargs khali hona chahiye
        if kwargs:
            raise TypeError(f"Unexpected kwargs: {list(kwargs)}")
        super().__init__()


class TimestampMixin(Base):
    def __init__(self, created_at="2026-01-01", **kwargs):
        self.created_at = created_at         # apna hissa
        super().__init__(**kwargs)           # baqi aage


class TaggableMixin(Base):
    def __init__(self, tags=None, **kwargs):
        self.tags = list(tags or [])
        super().__init__(**kwargs)


class Article(TimestampMixin, TaggableMixin):
    def __init__(self, title, **kwargs):
        self.title = title
        super().__init__(**kwargs)           # created_at + tags dono aage chale jayenge


a = Article(title="OOP seekho", created_at="2026-07-29", tags=["python", "oop"])
print("Article:", a.__dict__)
print("MRO:", [k.__name__ for k in Article.__mro__])

# Galat keyword? -> chain ke aakhir me pakra jayega
try:
    Article(title="X", nonsense=1)
except TypeError as err:
    print("\nTypeError:", err)

assert a.title == "OOP seekho" and a.tags == ["python", "oop"] and a.created_at == "2026-07-29"
print("[ok] kwargs cooperative pattern")
"""))

# ---------------------------------------------------------------------------
# 8. isinstance vs issubclass vs type
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 9. `isinstance()` vs `issubclass()` vs `type()`

| Cheez | Kaam | Subclass ko manti hai? |
|---|---|---|
| `type(obj) is C` | **exact** class check | ❌ nahi |
| `isinstance(obj, C)` | object C ya C ke subclass ka hai? | ✅ haan |
| `issubclass(D, C)` | **class** ka relation (object nahi) | ✅ haan |

**Rules of thumb:**

- Hamesha `isinstance` prefer karo — `type(x) == C` inheritance tor deta hai (LSP violation).
- `isinstance` tuple bhi leta hai: `isinstance(x, (int, float))`.
- `bool` `int` ka subclass hai — classic gotcha!
- Sab se Pythonic: type check hi na karo, **duck typing** use karo (aage aa raha hai).
"""))

cells.append(code(r"""
# ---- teenon ka farq ---------------------------------------------------------
d3 = Dog("Moti", 4)

print("isinstance(d3, Dog)      :", isinstance(d3, Dog))       # True
print("isinstance(d3, Animal)   :", isinstance(d3, Animal))    # True  <- subclass manta hai
print("type(d3) is Dog          :", type(d3) is Dog)           # True
print("type(d3) is Animal       :", type(d3) is Animal)        # False <- exact check
print("issubclass(Dog, Animal)  :", issubclass(Dog, Animal))   # True
print("issubclass(Dog, object)  :", issubclass(Dog, object))   # True
print("isinstance(d3, (Cat, Dog)):", isinstance(d3, (Cat, Dog)))  # tuple allowed

# ---- Gotcha: bool asal me int hai ----------------------------------------
print("\nissubclass(bool, int):", issubclass(bool, int))       # True !!
print("isinstance(True, int):", isinstance(True, int))         # True !!
print("True + True =", True + True)                            # 2

def count_items_bad(n):
    # bug: True bhi 'int' pass kar jata hai
    if not isinstance(n, int):
        raise TypeError("int chahiye")
    return n * 2

print("count_items_bad(True) ->", count_items_bad(True), "(bug! bool guzar gaya)")

def count_items_ok(n):
    # bool ko alag se rokna parta hai
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("sirf pura int chahiye")
    return n * 2

try:
    count_items_ok(True)
except TypeError as err:
    print("Sahi check ->", err)

assert isinstance(d3, Animal) and not (type(d3) is Animal)
print("\n[ok] isinstance / issubclass / type")
"""))

cells.append(md(r"""
## 10. Method resolution debugging — ye method aakhir kahan se aaya?

Bare projects me sawal aata hai: "`obj.save()` chala — magar kis class ka?"
Ye tools yaad rakho:

- `type(obj).__mro__` → search order
- `Class.__dict__` → sirf usi class me define hui cheezein (inherited nahi)
- `method.__qualname__` → `ClassName.method_name`
- `obj.method.__func__` → underlying function
- Manual walk: MRO me loop chala kar pehli class dhoondo jis ke `__dict__` me naam ho
"""))

cells.append(code(r"""
# ---- helper: kis class ne ye attribute di? --------------------------------
def find_owner(cls, attr):
    "MRO me pehli class jis ke apne __dict__ me attr ho."
    for klass in cls.__mro__:
        if attr in klass.__dict__:
            return klass.__name__
    return None


print("SmartPhone.info  ->", find_owner(SmartPhone, "info"))    # SmartPhone (override)
print("SmartPhone.call  ->", find_owner(SmartPhone, "call"))    # Phone
print("SmartPhone.click ->", find_owner(SmartPhone, "click"))   # Camera
print("SmartPhone.__str__ ->", find_owner(SmartPhone, "__str__"))  # object

print("\n__qualname__ se pata chalta hai:")
print("  Manager.annual_salary :", Manager.annual_salary.__qualname__)
print("  Manager.role          :", Manager.role.__qualname__)
print("  m.annual_salary       :", m.annual_salary.__qualname__)   # bound method
print("  Manager me inherited 'raise_pct' nahi? Manager.__dict__ me hai?:",
      "raise_pct" in Manager.__dict__)

assert find_owner(SmartPhone, "call") == "Phone"
assert find_owner(SmartPhone, "__str__") == "object"
print("\n[ok] method resolution debugging")
"""))

# ---------------------------------------------------------------------------
# 9. protected vs private in inheritance
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 11. Inheritance me `_protected` vs `__private`

- `_single` underscore = "internal hai, magar subclass use kar sakti hai" → **inherit hota hai
  normally**.
- `__double` underscore = **name mangling** (`__x` → `_ClassName__x`). Subclass me se `self.__x`
  likhne par `_SubClass__x` dhoonda jayega → `AttributeError`.

**Kab `__` use karein:** jab tum **nahi** chahte ke subclass accidentally tumhari internal
attribute ko override kar de (naam clash se bachne ke liye — yehi mangling ka asli maqsad hai).
**Warna** subclass-friendly code me `_single` use karo.
"""))

cells.append(code(r"""
# ---- mangling ka asar inheritance par -------------------------------------
class BaseAcc:
    def __init__(self):
        self._protected = "subclass mujhe use kar sakti hai"
        self.__private = "sirf BaseAcc ke andar"      # -> _BaseAcc__private

    def show_private(self):
        return self.__private        # BaseAcc ke andar likha hai -> theek chalega


class ChildAcc(BaseAcc):
    def use_protected(self):
        return self._protected       # bilkul theek

    def use_private(self):
        # yahan Python `self._ChildAcc__private` dhoondega -> nahi milega
        return self.__private


c1 = ChildAcc()
print("protected:", c1.use_protected())
print("base ka method:", c1.show_private())

try:
    c1.use_private()
except AttributeError as err:
    print("AttributeError:", err)

print("\nAsal keys:", [k for k in c1.__dict__])       # _protected, _BaseAcc__private
print("Mangled naam se access:", c1._BaseAcc__private)

# Mangling ka FAIDA: naam clash se hifazat
class Logger:
    def __init__(self):
        self.__buffer = ["logger ka buffer"]      # _Logger__buffer

    def logs(self):
        return self.__buffer


class MyApp(Logger):
    def __init__(self):
        super().__init__()
        self.__buffer = ["app ka buffer"]         # _MyApp__buffer — TAKRAO NAHI hua

    def app_data(self):
        return self.__buffer


ap = MyApp()
print("\nLogger ka buffer:", ap.logs())
print("App ka buffer   :", ap.app_data())
print("Keys            :", sorted(ap.__dict__))
assert ap.logs() != ap.app_data()
print("[ok] private/protected in inheritance")
"""))

# ---------------------------------------------------------------------------
# 10. POLYMORPHISM
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 12. Polymorphism — "ek naam, kai shakal"

**Kya hai:** Greek se: *poly* = kai, *morph* = shakal. Ek hi interface (method ka naam)
different types ke objects par different tareeqe se kaam karta hai.

**Python me polymorphism ki 4 shaklein:**

1. **Built-in / operator polymorphism** — `+` int par addition, str par concatenation
2. **Function polymorphism** — `len()` string, list, dict sab par chalta hai
3. **Method overriding (subtype polymorphism)** — parent type ke through child ka behaviour
4. **Duck typing** — inheritance ki zaroorat hi nahi, sirf method hona chahiye

**Kyun zaroori:** `if/elif` ki lambi chains khatam ho jaati hain. Naya type add karna =
naya class likhna, purana code chhedne ki zaroorat nahi (**Open/Closed Principle**).
"""))

cells.append(code(r"""
# ---- 1) built-in polymorphism -----------------------------------------------
print("int +  :", 5 + 3)                 # addition
print("str +  :", "Pak" + "istan")       # concatenation
print("list + :", [1, 2] + [3])          # merge
print("len()  :", len("hello"), len([1, 2, 3]), len({"a": 1}))

# ---- 2) BURA tareeqa: if/elif chain (polymorphism se pehle) ----------------
def area_bad(shape_type, **kw):
    # Naya shape aane par is function ko har baar chhedna paray ga -> Open/Closed violation
    if shape_type == "circle":
        return 3.14159 * kw["r"] ** 2
    elif shape_type == "square":
        return kw["side"] ** 2
    elif shape_type == "rect":
        return kw["w"] * kw["h"]
    else:
        raise ValueError("anjaan shape")

print("\nif/elif style:", round(area_bad("circle", r=2), 2), area_bad("square", side=3))

# ---- 3) ACHA tareeqa: subtype polymorphism --------------------------------
class Rect(Shape):
    def __init__(self, w, h):
        super().__init__("rectangle")
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


def total_area(shapes):
    # Is function ko pata hi nahi kaun sa shape aayega — sirf .area() chahiye
    return sum(s.area() for s in shapes)


shapes = [Circle(1), Square(2), Triangle(3, 4), Rect(2, 5)]
for s in shapes:
    print(f"  {s.name:<10} -> {s.area():.2f}")
print("Total area:", round(total_area(shapes), 2))

# Naya shape add karna = naya class, total_area ko chhua bhi nahi
assert round(total_area([Square(2), Rect(2, 5)]), 2) == 14.0
print("[ok] subtype polymorphism")
"""))

cells.append(md(r"""
## 13. Duck Typing

> "If it walks like a duck and quacks like a duck, it's a duck."

Python **type** nahi dekhta, **behaviour** dekhta hai. Agar object me zaroori method maujood
hai to kaam ho jayega — chahe inheritance ka koi rishta na ho.

**EAFP** (Easier to Ask Forgiveness than Permission) Pythonic style hai:

```python
try:
    obj.quack()
except AttributeError:
    ...
```

**LBYL** (Look Before You Leap) = `if hasattr(obj, "quack")` — chalta hai magar kam Pythonic.

**Faida:** loose coupling, testing me fake/mock objects aasani se ghusa sakte ho.
**Nuqsan:** error runtime par milta hai (compile-time safety nahi) → is liye tests + type hints
(`typing.Protocol`) ka istemal karo.
"""))

cells.append(code(r"""
# ---- duck typing: koi common parent nahi, phir bhi chal gaya ---------------
class Duck:
    def quack(self):
        return "Quack quack!"


class Person2:
    def quack(self):
        return "Main insaan hoon, magar quack kar sakta hoon!"


class Robot:
    def beep(self):
        return "Beep"


def make_it_quack(thing):
    # EAFP: pehle koshish, phir maafi
    try:
        return thing.quack()
    except AttributeError:
        return f"{type(thing).__name__} quack nahi kar sakta"


for obj_ in (Duck(), Person2(), Robot()):
    print(f"{type(obj_).__name__:<8} -> {make_it_quack(obj_)}")

print("\nDuck aur Person2 ka koi rishta?", issubclass(Person2, Duck))   # False!

# ---- Asli duck typing ka faida: file-like objects -------------------------
def write_report(stream, rows):
    "stream ko sirf .write() aana chahiye — file? StringIO? custom logger? sab chalega."
    stream.write("=== Report ===\n")
    for name, val in rows:
        stream.write(f"{name}: {val}\n")
    return stream


class ListStream:
    "Custom 'file-like' object — sirf write() implement kiya."
    def __init__(self):
        self.chunks = []

    def write(self, text):
        self.chunks.append(text)
        return len(text)


data_rows = [("Sales", 500), ("Cost", 300)]

buf = write_report(io.StringIO(), data_rows)          # stdlib StringIO
print("\nStringIO me:\n" + buf.getvalue())

ls = write_report(ListStream(), data_rows)            # apna custom object
print("Custom stream ke chunks:", ls.chunks[:2], "...")

import tempfile, os, pathlib
with tempfile.TemporaryDirectory() as tmp:            # asli file (Windows-safe)
    path = pathlib.Path(tmp) / "report.txt"
    with open(path, "w", encoding="utf-8") as fh:
        write_report(fh, data_rows)
    print("File se parha:", path.read_text(encoding="utf-8").splitlines()[1])

assert "Sales: 500" in buf.getvalue()
assert "".join(ls.chunks) == buf.getvalue()
print("[ok] duck typing")
"""))

cells.append(md(r"""
## 14. Operator Overloading (intro) — `__add__`, `__eq__`, `__lt__`

Operators asal me **dunder methods** ka shortcut hain:

| Operator | Dunder | Note |
|---|---|---|
| `a + b` | `a.__add__(b)` | fail ho to `b.__radd__(a)` |
| `a == b` | `a.__eq__(b)` | default: identity (`is`) |
| `a < b` | `a.__lt__(b)` | `sorted()` / `min()` / `max()` isi ko use karte hain |
| `a * b` | `a.__mul__(b)` | |
| `-a` | `a.__neg__()` | unary |
| `len(a)` | `a.__len__()` | |

**Ahem rules:**

- Type mismatch par `NotImplemented` **return** karo (raise nahi!) — Python doosre operand ko mauqa dega.
- `__eq__` define karo to object **unhashable** ho jaata hai jab tak `__hash__` na do (notebook 04 me detail).
- `functools.total_ordering` sirf `__eq__` + `__lt__` se baqi comparisons bana deta hai.

(Poori dunder ki duniya notebook 04 me.)
"""))

cells.append(code(r"""
from functools import total_ordering

@total_ordering                    # __lt__ + __eq__ se <=, >, >= khud ban jayenge
class Money:
    "Simple value object — operator overloading ka demo."

    def __init__(self, amount, currency="PKR"):
        self.amount, self.currency = amount, currency

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented              # raise NAHI — return NotImplemented
        if other.currency != self.currency:
            raise ValueError("Different currencies jama nahi hotin")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount

    def __hash__(self):
        # __eq__ diya to __hash__ bhi do warna set/dict me use nahi ho sakega
        return hash((self.amount, self.currency))


a1, b1 = Money(500), Money(250)
print("a + b   :", a1 + b1)
print("a == 500:", a1 == Money(500))
print("a > b   :", a1 > b1)              # total_ordering se mila
print("sorted  :", sorted([Money(300), Money(100), Money(200)]))
print("max     :", max(Money(300), Money(100)))
print("set me  :", {Money(100), Money(100)})     # hash ki wajah se 1 element

# Type mismatch: NotImplemented -> Python TypeError me badal deta hai
try:
    a1 + 100
except TypeError as err:
    print("\nTypeError:", err)

# Currency mismatch -> hamari domain error
try:
    Money(100, "PKR") + Money(100, "USD")
except ValueError as err:
    print("ValueError:", err)

assert (a1 + b1).amount == 750
assert sorted([Money(3), Money(1)])[0] == Money(1)
print("[ok] operator overloading")
"""))

cells.append(md(r"""
## 15. Method Overloading Python me kyun NAHI hai?

Java/C++ me same naam ke kai methods different signatures ke sath ho sakte hain
(**compile-time / static polymorphism**). Python me **nahi** — kyunke:

- Python dynamically typed hai, arguments ke types compile time par pata nahi.
- Class body me same naam dobara define karo to **doosri definition pehli ko replace** kar deti
  hai (class dict me sirf ek entry rehti hai).

**3 workarounds:**

1. **Default arguments** — sab se simple aur aam
2. **`*args` / `**kwargs` + manual dispatch** — flexible
3. **`functools.singledispatch` / `singledispatchmethod`** — type ke hisaab se asli dispatch
   (sab se saaf, stdlib me maujood)
"""))

cells.append(code(r"""
# ---- "overloading" ki koshish -> doosri definition jeet jaati hai ----------
class Calc:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):          # noqa: F811 — pehli wali GAYAB ho gayi
        return a + b + c


calc = Calc()
print("3 args:", calc.add(1, 2, 3))
try:
    calc.add(1, 2)                   # pehli definition mojood nahi
except TypeError as err:
    print("TypeError:", err)
print("class dict me sirf ek 'add':", [k for k in Calc.__dict__ if k == "add"])
"""))

cells.append(code(r"""
from functools import singledispatchmethod

# ---- WORKAROUND 1: default arguments --------------------------------------
class Calc1:
    def add(self, a, b=0, c=0):        # ek definition, kai tareeqe se call
        return a + b + c


c1_ = Calc1()
print("W1 default args:", c1_.add(1), c1_.add(1, 2), c1_.add(1, 2, 3))

# ---- WORKAROUND 2: *args + manual dispatch --------------------------------
class Calc2:
    def add(self, *args):
        if not args:
            return 0
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            return sum(args[0])        # list bhi accept kar li
        return sum(args)


c2_ = Calc2()
print("W2 *args      :", c2_.add(), c2_.add(1, 2, 3, 4), c2_.add([5, 6]))

# ---- WORKAROUND 3: singledispatchmethod (type par asli dispatch) ----------
class Formatter:
    @singledispatchmethod
    def fmt(self, value):
        # fallback / default implementation
        return f"<unknown: {value!r}>"

    @fmt.register
    def _(self, value: int):
        return f"int: {value:,}"

    @fmt.register
    def _(self, value: str):
        return f"str: '{value.upper()}'"

    @fmt.register
    def _(self, value: list):
        return f"list of {len(value)}: {value}"


f_ = Formatter()
print("\nW3 singledispatch:")
for v in (1234567, "salam", [1, 2, 3], 4.5):
    print("   ", f_.fmt(v))

assert c1_.add(1, 2) == 3 and c2_.add([5, 6]) == 11
assert f_.fmt(10).startswith("int") and f_.fmt("hi").startswith("str")
print("\n[ok] overloading workarounds")
"""))

cells.append(md(r"""
## 16. Base class me contract enforce karna — `NotImplementedError`

Agar base class ka method **children ko lazmi** implement karna hai, do tareeqe hain:

1. **`raise NotImplementedError`** — object ban jayega, magar galat method call par error.
2. **`abc.ABC` + `@abstractmethod`** — class **banate hi** rok deta hai (behtar; notebook 04 me detail).

`NotImplementedError` (exception) aur `NotImplemented` (operator ka special value) **different**
cheezein hain — ye interview me pucha jata hai!
"""))

cells.append(code(r"""
# ---- NotImplementedError se contract ---------------------------------------
class Exporter:
    "Template: har exporter ko export() dena hoga."

    def header(self):
        return "# Exported by Bizee tool"        # common (inherited)

    def export(self, rows):
        raise NotImplementedError(
            f"{type(self).__name__} ne export() implement nahi kiya"
        )


class TSVExporter(Exporter):
    def export(self, rows):
        lines = [self.header()] + ["\t".join(map(str, r)) for r in rows]
        return "\n".join(lines)


class LazyExporter(Exporter):        # jaan boojh kar implement nahi kiya
    pass


rows_ = [("a", 1), ("b", 2)]
print(TSVExporter().export(rows_))

try:
    LazyExporter().export(rows_)
except NotImplementedError as err:
    print("\nNotImplementedError:", err)

print("\nFarq yaad rakho:")
print("  NotImplementedError -> exception (raise karte hain)")
print("  NotImplemented      -> value (operators me return karte hain):", NotImplemented)
print("[ok] contract enforcement")
"""))

cells.append(md(r"""
## 17. Composition vs Inheritance (IS-A vs HAS-A)

| | Inheritance (IS-A) | Composition (HAS-A) |
|---|---|---|
| Rishta | `Dog` **is a** `Animal` | `Car` **has an** `Engine` |
| Coupling | Tight (parent badla to child toota) | Loose |
| Runtime badla ja sakta? | Nahi | Haan (object swap kar do) |
| Test karna | Mushkil (parent ka poora baggage) | Aasan (fake inject karo) |

**Design rule:** *"Favour composition over inheritance."*
Inheritance sirf jab **asli IS-A** ho **aur** substitutability (LSP) ho.

**Classic galti:** `class Stack(list)` — Stack list ki tarah *behave* nahi karta, magar
inheritance ki wajah se `append`, `insert`, `sort`, indexing sab leak ho gaye.
"""))

cells.append(code(r"""
# ---- GALAT: Stack(list) — internals leak ho gaye ---------------------------
class StackBad(list):
    def push(self, x):
        self.append(x)


sb = StackBad()
sb.push(1); sb.push(2)
sb.insert(0, 99)          # OOPS: stack me beech me daal diya — invariant toot gaya
print("StackBad:", list(sb), "  <- insert() ne LIFO rule tor diya")

# ---- SAHI: composition — list andar rakho, sirf apna API do ---------------
class Stack:
    "HAS-A list, IS-A list nahi."

    def __init__(self):
        self._items = []          # composition

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("stack khali hai")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def __len__(self):
        return len(self._items)


st = Stack()
st.push(1); st.push(2); st.push(3)
print("Stack pop:", st.pop(), "| peek:", st.peek(), "| len:", len(st))
print("insert() maujood hai?", hasattr(st, "insert"))     # False — API saaf hai

# ---- Composition se runtime behaviour swap (strategy pattern ki jhalak) ---
class LoudSpeaker:
    def render(self, msg): return msg.upper() + "!!!"


class QuietSpeaker:
    def render(self, msg): return msg.lower() + "..."


class Announcer:
    def __init__(self, speaker):
        self.speaker = speaker          # HAS-A speaker (inject kiya)

    def announce(self, msg):
        return self.speaker.render(msg)


ann = Announcer(LoudSpeaker())
print("\nLoud :", ann.announce("Train aa rahi hai"))
ann.speaker = QuietSpeaker()            # RUNTIME par behaviour badal diya!
print("Quiet:", ann.announce("Train aa rahi hai"))

assert not hasattr(st, "insert")
assert ann.announce("Hi") == "hi..."
print("[ok] composition vs inheritance")
"""))

# ---------------------------------------------------------------------------
# 11. GOTCHAS
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 18. Common Mistakes / Gotchas (yahan log phaste hain)

1. **`super().__init__()` bhool jana** → child ke objects adhoore, `AttributeError` baad me.
2. **Mutable class attribute** parent me → sab subclasses/instances **wahi** object share karte hain.
3. **Signature badal kar override karna** → LSP violation, polymorphic code toot jata hai.
4. **`type(x) == C`** check → subclass reject ho jata hai.
5. **Parent ko explicitly call karna** (`Parent.__init__(self)`) multiple inheritance me → koi
   parent skip ya double-call ho sakta hai.
6. **Built-ins se inherit karna** (`list`, `dict`) → internal methods bypass ho jaate hain
   (e.g. `dict.update` `__setitem__` ko call nahi karta).
7. **Deep hierarchy** (4-5 level) → "yeh method kahan se aaya?" ka nightmare.
8. **`super()` ko "parent" samajhna** → asal me MRO ka **next** hai.
9. **Class attribute ko instance se badalna** → sirf usi instance par naya attribute banta hai.
10. **`__private` ko subclass me use karna** → mangling ki wajah se `AttributeError`.
"""))

cells.append(code(r"""
# ---- GOTCHA 1 & 2: mutable class attribute sab me share hoti hai ----------
class TeamBad:
    members = []                  # KHATARNAAK: class attribute (sab share karenge)

    def add(self, name):
        self.members.append(name)   # class ki list ko mutate kar diya!


class DevTeam(TeamBad): pass
class QATeam(TeamBad): pass


DevTeam().add("Ali")
QATeam().add("Sara")
print("DevTeam.members:", DevTeam.members)     # dono naam!
print("QATeam.members :", QATeam.members)      # dono naam!
print("Same object?", DevTeam.members is QATeam.members)   # True — ek hi list

# ---- FIX: instance attribute in __init__ ---------------------------------
class TeamGood:
    def __init__(self):
        self.members = []          # har object ki apni list

    def add(self, name):
        self.members.append(name)
        return self


class DevTeam2(TeamGood): pass
class QATeam2(TeamGood): pass


d_t, q_t = DevTeam2().add("Ali"), QATeam2().add("Sara")
print("\nFix ke baad -> Dev:", d_t.members, "| QA:", q_t.members)
assert DevTeam.members is QATeam.members
assert d_t.members is not q_t.members
print("[ok] gotcha: shared mutable class attribute")
"""))

cells.append(code(r"""
# ---- GOTCHA 3: LSP violation — signature badal kar override karna --------
class Notifier:
    def send(self, message):
        return f"[base] {message}"


class GoodSMS(Notifier):
    def send(self, message):                 # same signature — safe
        return f"[sms] {message}"


class BadEmail(Notifier):
    def send(self, message, subject):        # extra REQUIRED arg — LSP toot gaya
        return f"[email] {subject}: {message}"


class OKEmail(Notifier):
    def send(self, message, subject="Notification"):   # default de kar backwards-compatible
        return f"[email] {subject}: {message}"


def broadcast(notifiers, msg):
    "Polymorphic code — sirf send(msg) ki umeed rakhta hai."
    out = []
    for n in notifiers:
        try:
            out.append(n.send(msg))
        except TypeError as err:
            out.append(f"TOOT GAYA -> {type(n).__name__}: {err}")
    return out


for line in broadcast([GoodSMS(), BadEmail(), OKEmail()], "Server down"):
    print(line)

print("\nSabaq: override karte waqt parent ka signature compatible rakho —")
print("naye parameters ALWAYS default value ke sath do.")
"""))

cells.append(code(r"""
# ---- GOTCHA 4: type() check subclass ko reject kar deta hai ---------------
class Payment: pass
class CreditCard(Payment): pass


def process_bad(p):
    if type(p) is not Payment:              # GALAT
        return "reject"
    return "process"


def process_good(p):
    if not isinstance(p, Payment):          # SAHI
        return "reject"
    return "process"


cc = CreditCard()
print("type() check   :", process_bad(cc), " <- valid subclass reject ho gaya!")
print("isinstance check:", process_good(cc))

# ---- GOTCHA 5: dict se inherit karne ka masla ----------------------------
class UpperDictBad(dict):
    "Chahte hain sab keys upper-case hon."
    def __setitem__(self, k, v):
        super().__setitem__(k.upper(), v)


ud = UpperDictBad()
ud["a"] = 1                    # __setitem__ chala -> "A"
ud.update({"b": 2})            # dict.update C level par hai — __setitem__ BYPASS!
print("\nUpperDictBad:", dict(ud), " <- 'b' upper-case nahi hui")

# FIX: collections.UserDict use karo (pure-Python, sab kuch __setitem__ se guzarta hai)
from collections import UserDict

class UpperDictGood(UserDict):
    def __setitem__(self, k, v):
        super().__setitem__(k.upper(), v)


ug = UpperDictGood()
ug["a"] = 1
ug.update({"b": 2})
print("UpperDictGood:", dict(ug), " <- theek")

assert process_bad(cc) == "reject" and process_good(cc) == "process"
assert "b" in ud and "B" in ug
print("[ok] gotchas 4 & 5")
"""))

cells.append(code(r"""
# ---- GOTCHA 6: class attribute instance se "badalna" ---------------------
class Config:
    retries = 3               # class attribute (shared default)


c_a, c_b = Config(), Config()
c_a.retries = 10              # NAYA instance attribute bana — class wali nahi badli
print("c_a.retries:", c_a.retries, "(instance)")
print("c_b.retries:", c_b.retries, "(class se)")
print("Config.retries:", Config.retries)
print("c_a ka __dict__:", c_a.__dict__, "| c_b ka:", c_b.__dict__)

Config.retries = 5            # class par badla -> jin ke apne nahi, un sab par asar
print("\nClass badalne ke baad -> c_a:", c_a.retries, "| c_b:", c_b.retries)

# ---- GOTCHA 7: super() vs explicit parent call in diamond ---------------
class Root:
    def __init__(self):
        print("   Root.__init__")


class L(Root):
    def __init__(self):
        Root.__init__(self)      # explicit — cooperative nahi
        print("   L.__init__")


class R(Root):
    def __init__(self):
        Root.__init__(self)      # explicit
        print("   R.__init__")


class Both(L, R):
    def __init__(self):
        L.__init__(self)
        R.__init__(self)
        print("   Both.__init__")


print("\nExplicit calls (Root DO baar chalega — bug):")
Both()

class L2(Root):
    def __init__(self):
        super().__init__(); print("   L2.__init__")

class R2(Root):
    def __init__(self):
        super().__init__(); print("   R2.__init__")

class Both2(L2, R2):
    def __init__(self):
        super().__init__(); print("   Both2.__init__")

print("\nsuper() ke sath (Root sirf EK baar):")
Both2()
print("\n[ok] gotchas 6 & 7")
"""))

# ---------------------------------------------------------------------------
# 12. REAL WORLD
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 19. Real-World Problems

Ab in concepts ko asli scenarios par lagate hain. Har problem me: masla, design ki soch,
aur commented solution.

1. **Payroll system** — employee hierarchy, har role ki salary ka apna formula
2. **Notification service** — Email / SMS / Push, ek hi `send()` interface
3. **Shape report generator** — polymorphism + duck typing + sorting
4. **Data exporter** — mixins se CSV/JSON/Markdown export
5. **Bank accounts** — `withdraw()` ka rule har account type ka alag (overriding + validation)
"""))

cells.append(code(r"""
# ===== RW-1: PAYROLL SYSTEM ==================================================
# Masla: company me 3 tarah ke log hain — salaried, hourly, aur commission-based sales.
# Har ek ki tankhwah ka formula alag, magar report banane wale code ko farq nahi parna chahiye.

class Staff:
    "Base class — common data + template method."

    def __init__(self, name, emp_id):
        self.name, self.emp_id = name, emp_id

    def monthly_pay(self):
        raise NotImplementedError("subclass ko formula dena hoga")

    def payslip(self):
        # TEMPLATE METHOD: structure base me, tafseel child me
        return f"{self.emp_id:<6} {self.name:<10} {type(self).__name__:<16} PKR {self.monthly_pay():>10,.0f}"


class SalariedStaff(Staff):
    def __init__(self, name, emp_id, annual):
        super().__init__(name, emp_id)
        self.annual = annual

    def monthly_pay(self):
        return self.annual / 12


class HourlyStaff(Staff):
    OVERTIME_AFTER = 160          # class-level constant (monthly hours)

    def __init__(self, name, emp_id, rate, hours):
        super().__init__(name, emp_id)
        self.rate, self.hours = rate, hours

    def monthly_pay(self):
        normal = min(self.hours, self.OVERTIME_AFTER) * self.rate
        overtime = max(0, self.hours - self.OVERTIME_AFTER) * self.rate * 1.5   # 1.5x
        return normal + overtime


class SalesStaff(SalariedStaff):          # multilevel: base salary + commission
    def __init__(self, name, emp_id, annual, sales, pct=0.02):
        super().__init__(name, emp_id, annual)
        self.sales, self.pct = sales, pct

    def monthly_pay(self):
        return super().monthly_pay() + self.sales * self.pct     # parent ka formula reuse


staff = [
    SalariedStaff("Ali", "E-101", 1_200_000),
    HourlyStaff("Sara", "E-102", 800, 180),          # 20 ghante overtime
    SalesStaff("Bilal", "E-103", 600_000, 2_000_000),
]

print("PAYROLL REPORT")
print("-" * 60)
for person in staff:
    print(person.payslip())          # polymorphic call
print("-" * 60)
print(f"{'TOTAL':<34} PKR {sum(p.monthly_pay() for p in staff):>10,.0f}")

assert staff[0].monthly_pay() == 100_000
assert staff[1].monthly_pay() == 160 * 800 + 20 * 800 * 1.5
assert staff[2].monthly_pay() == 50_000 + 40_000
print("\n[ok] RW-1 payroll")
"""))

cells.append(code(r"""
# ===== RW-2: NOTIFICATION SERVICE ===========================================
# Masla: alerts kai channels par bhejni hain. Naya channel add karna aasan hona chahiye,
# aur ek channel fail ho to baqi chalti rahein.

class Channel:
    "Base channel — retry/validation ka common kaam yahan."

    max_len = 1000

    def __init__(self, name):
        self.name = name
        self.sent = []            # instance attribute (shared nahi!)

    def validate(self, msg):
        if not msg or not msg.strip():
            raise ValueError("khali message nahi bhej sakte")
        if len(msg) > self.max_len:
            raise ValueError(f"{self.name}: message {self.max_len} chars se bara hai")
        return msg.strip()

    def _deliver(self, msg):
        raise NotImplementedError

    def send(self, msg):
        # Template: validate -> deliver -> record
        clean = self.validate(msg)
        payload = self._deliver(clean)
        self.sent.append(payload)
        return payload


class EmailChannel(Channel):
    max_len = 5000                       # email me lambi body chalti hai

    def __init__(self, address, subject="Alert"):
        super().__init__("email")
        self.address, self.subject = address, subject

    def _deliver(self, msg):
        return f"EMAIL -> {self.address} | {self.subject} | {msg}"


class SMSChannel(Channel):
    max_len = 160                        # SMS ki limit

    def __init__(self, number):
        super().__init__("sms")
        self.number = number

    def _deliver(self, msg):
        return f"SMS   -> {self.number} | {msg}"


class PushChannel(Channel):
    def __init__(self, device_id):
        super().__init__("push")
        self.device_id = device_id

    def _deliver(self, msg):
        return f"PUSH  -> {self.device_id[:6]}… | {msg}"


class NotificationService:
    "HAS-A channels (composition) — inheritance ki zaroorat nahi."

    def __init__(self, channels):
        self.channels = list(channels)

    def broadcast(self, msg):
        results, errors = [], []
        for ch in self.channels:
            try:
                results.append(ch.send(msg))
            except ValueError as err:
                errors.append(f"{ch.name} FAIL: {err}")     # ek fail, baqi chalte rahenge
        return results, errors


svc = NotificationService([
    EmailChannel("admin@bizee.pk", subject="Server Alert"),
    SMSChannel("+92300..."),
    PushChannel("device-abc123xyz"),
])

ok, bad = svc.broadcast("Database CPU 95% par hai!")
print("\n".join(ok))
print("\nLambe message ka test (SMS fail hona chahiye):")
ok2, bad2 = svc.broadcast("x" * 200)
print("  delivered:", len(ok2), "| failed:", bad2)

assert len(ok) == 3 and len(bad) == 0
assert len(ok2) == 2 and len(bad2) == 1        # sirf SMS fail
print("\n[ok] RW-2 notifications")
"""))

cells.append(code(r"""
# ===== RW-3: SHAPE REPORT (polymorphism + duck typing + sorting) ============
# Masla: mixed shapes ka report — sab se bara shape, total area, sorted list.
# Kuch shapes hamari hierarchy ke hain, kuch "third-party" (koi parent nahi) — dono chalein.

class ThirdPartyEllipse:              # duck: Shape se inherit NAHI karta
    name = "ellipse"

    def __init__(self, a, b):
        self.a, self.b = a, b

    def area(self):
        return 3.14159 * self.a * self.b


def shape_report(items):
    "Sirf .area() aur .name chahiye — chahe kis class ka ho (duck typing)."
    rows = []
    for it in items:
        if not hasattr(it, "area"):
            rows.append((getattr(it, "name", "?"), None))
            continue
        rows.append((it.name, it.area()))

    valid = [(n, a) for n, a in rows if a is not None]
    valid.sort(key=lambda t: t[1], reverse=True)      # area par sort
    lines = [f"{n:<12} {a:>10.2f}" for n, a in valid]
    skipped = [n for n, a in rows if a is None]
    return lines, valid[0] if valid else None, sum(a for _, a in valid), skipped


class NotAShape:
    name = "mystery"


mixed = [Circle(3), Square(4), Rect(2, 10), ThirdPartyEllipse(2, 3), NotAShape()]
lines, biggest, total, skipped = shape_report(mixed)

print("SHAPE REPORT (area ke hisaab se)")
print("-" * 24)
print("\n".join(lines))
print("-" * 24)
print(f"{'TOTAL':<12} {total:>10.2f}")
print("Sab se bara:", biggest[0], f"({biggest[1]:.2f})")
print("Skip kiye (area nahi):", skipped)

assert biggest[0] == "circle"           # 28.27 > 20 > 18.85 > 16
assert skipped == ["mystery"]
print("\n[ok] RW-3 shape report")
"""))

cells.append(code(r"""
# ===== RW-4: DATA EXPORTER (mixins) =========================================
# Masla: ek hi dataset ko CSV, JSON aur Markdown me export karna hai.
# Design: base me data, mixins me formats -> jo chahiye plug karo.

class RecordSet:
    "Base: data rakhta hai + common helpers."

    def __init__(self, headers, rows):
        self.headers, self.rows = list(headers), [list(r) for r in rows]

    def as_dicts(self):
        return [dict(zip(self.headers, r)) for r in self.rows]


class CSVExportMixin:
    def to_csv(self):
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(self.headers)
        w.writerows(self.rows)
        return buf.getvalue()


class JSONExportMixin:
    def to_json(self, indent=None):
        return json.dumps(self.as_dicts(), ensure_ascii=False, indent=indent)


class MarkdownExportMixin:
    def to_markdown(self):
        head = "| " + " | ".join(map(str, self.headers)) + " |"
        sep = "| " + " | ".join("---" for _ in self.headers) + " |"
        body = ["| " + " | ".join(map(str, r)) + " |" for r in self.rows]
        return "\n".join([head, sep] + body)


class SalesReport(CSVExportMixin, JSONExportMixin, MarkdownExportMixin, RecordSet):
    "3 formats — sab mixins se, apna code sirf summary ka."

    def summary(self):
        total = sum(r[2] for r in self.rows)
        return f"{len(self.rows)} cities, total sales PKR {total:,}"


report = SalesReport(
    headers=["city", "month", "sales"],
    rows=[["Karachi", "Jul", 500_000], ["Lahore", "Jul", 420_000], ["Quetta", "Jul", 90_000]],
)

print("MRO:", [k.__name__ for k in SalesReport.__mro__], "\n")
print("--- CSV ---\n" + report.to_csv())
print("--- JSON ---\n" + report.to_json(indent=1)[:120] + " ...\n")
print("--- MARKDOWN ---\n" + report.to_markdown())
print("\nSummary:", report.summary())

assert report.to_csv().splitlines()[0] == "city,month,sales"
assert json.loads(report.to_json())[0]["city"] == "Karachi"
assert report.to_markdown().count("|") == 4 * 5      # 5 lines x 4 pipes
print("\n[ok] RW-4 exporter mixins")
"""))

cells.append(code(r"""
# ===== RW-5: BANK ACCOUNTS (overriding + validation) ========================
# Masla: Savings me minimum balance rakhna zaroori, Current me overdraft allowed,
# Fixed Deposit se maturity se pehle nikalna mana. Ek hi withdraw() interface.

class InsufficientFunds(Exception):
    "Domain-specific exception — generic ValueError se behtar."


class Account:
    bank = "Bizee Bank"                # class constant

    def __init__(self, holder, balance=0):
        self.holder = holder
        self._balance = float(balance)   # protected: subclass use karegi
        self._log = []

    @property
    def balance(self):                   # read-only property (notebook 02 se)
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit positive hona chahiye")
        self._balance += amount
        self._log.append(f"+{amount:,.0f}")
        return self._balance

    def withdraw(self, amount):
        # Base rule: balance se zyada nahi
        if amount <= 0:
            raise ValueError("amount positive hona chahiye")
        if amount > self._balance:
            raise InsufficientFunds(f"{self.holder}: balance {self._balance:,.0f} kaafi nahi")
        self._balance -= amount
        self._log.append(f"-{amount:,.0f}")
        return self._balance

    def __repr__(self):
        return f"{type(self).__name__}({self.holder!r}, {self._balance:,.0f})"


class Savings(Account):
    MIN_BALANCE = 1000                   # extra rule

    def withdraw(self, amount):
        # Pehle apna extra rule check karo, phir parent ka logic reuse karo
        if self._balance - amount < self.MIN_BALANCE:
            raise InsufficientFunds(
                f"Savings me minimum {self.MIN_BALANCE:,} rakhna zaroori hai"
            )
        return super().withdraw(amount)          # duplication nahi


class Current(Account):
    OVERDRAFT = 5000                     # udhaar ki ijazat

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount positive hona chahiye")
        # Parent ka check bypass karna para kyunke rule mukhtalif hai
        if amount > self._balance + self.OVERDRAFT:
            raise InsufficientFunds("overdraft limit se bahar")
        self._balance -= amount
        self._log.append(f"-{amount:,.0f}")
        return self._balance


class FixedDeposit(Account):
    def __init__(self, holder, balance, matured=False):
        super().__init__(holder, balance)
        self.matured = matured

    def withdraw(self, amount):
        if not self.matured:
            raise InsufficientFunds("FD maturity se pehle withdraw nahi ho sakta")
        return super().withdraw(amount)


accounts = [Savings("Ali", 10_000), Current("Sara", 2_000), FixedDeposit("Bilal", 50_000)]

for acc in accounts:
    try:
        acc.withdraw(6_500)             # SAME call, different rules
        print(f"{acc!r:<32} withdraw 6,500 -> kamyab")
    except InsufficientFunds as err:
        print(f"{acc!r:<32} withdraw 6,500 -> RUKA: {err}")

print("\nFD matured ke baad:")
fd = FixedDeposit("Bilal", 50_000, matured=True)
print("  naya balance:", f"{fd.withdraw(9_500):,.0f}")
print("  transaction log:", fd._log)

assert accounts[0].balance == 10_000 - 6_500       # savings: min balance bacha (3,500)
assert accounts[1].balance == 2_000 - 6_500        # current: overdraft use hua (-4,500)
assert accounts[2].balance == 50_000               # FD: kuch nahi nikla
assert isinstance(accounts[0], Account) and Savings.MIN_BALANCE == 1000
print("\n[ok] RW-5 bank accounts")
"""))

# ---------------------------------------------------------------------------
# 13. LEETCODE
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 20. LeetCode Problems

Ye teen problems **design** category ki hain — inheritance/polymorphism ka natural fit,
kyunke teenon me "streaming data" ka ek hi interface hai: `add(...)` / `ping(...)`.

Hum pehle ek chhota **base class** (`StreamStructure`) banayenge taake teenon solutions ka
interface aur testing pattern same rahe (yehi asal me polymorphism ka faida hai).

| # | Title | Difficulty | Concept |
|---|---|---|---|
| 703 | Kth Largest Element in a Stream | Easy | min-heap, streaming state |
| 933 | Number of Recent Calls | Easy | sliding window with deque |
| 1352 | Product of the Last K Numbers | Medium | prefix products, zero handling |
"""))

cells.append(code(r"""
# ---- Common base class: teenon LeetCode designs ka shared interface -------
class StreamStructure:
    "Base: sab streaming designs ka common protocol + call counter (debugging ke liye)."

    def __init__(self):
        self.calls = 0

    def add(self, value):
        raise NotImplementedError

    def feed(self, values):
        "Helper: kai values ek sath daalo, har result ki list wapis do (polymorphic)."
        return [self.add(v) for v in values]


print("Base ready:", StreamStructure.__name__)
"""))

cells.append(md(r"""
### LC 703. Kth Largest Element in a Stream — Easy

**Link:** https://leetcode.com/problems/kth-largest-element-in-a-stream/

**Bayan:** Ek class `KthLargest(k, nums)` banao. Har `add(val)` ke baad stream me
**k-th sab se bara** element return karo (duplicates alag alag count hote hain).

**Approach:**

- **Brute force:** har `add` par poori list sort karo → `O(n log n)` per call. Chhote input
  par chalta hai, magar stream lamba hone par slow.
- **Optimal — size-k min-heap:** heap me sirf **top k** elements rakho.
  - Heap ka sab se chhota element (`heap[0]`) hi **k-th largest** hota hai.
  - `add(val)`: push karo; agar size > k to sab se chhota `heappop` kar do.
  - Kyun min-heap? Kyunke humein "k largest me se sab se chhota" chahiye — wahi root par hai.

**Complexity (optimal):** `add` = `O(log k)` time, space = `O(k)`.
(Brute force: `O(n log n)` per add, `O(n)` space.)
"""))

cells.append(code(r"""
import heapq

# ---- BRUTE FORCE (samajhne ke liye) ---------------------------------------
class KthLargestBrute(StreamStructure):
    def __init__(self, k, nums):
        super().__init__()                 # base ka counter
        self.k = k
        self.nums = list(nums)

    def add(self, val):
        self.calls += 1
        self.nums.append(val)
        self.nums.sort(reverse=True)        # O(n log n) har baar — mehnga
        return self.nums[self.k - 1]


# ---- OPTIMAL: size-k MIN-HEAP ---------------------------------------------
class KthLargest(StreamStructure):
    "Heap me sirf k sab se bare elements; root = k-th largest."

    def __init__(self, k, nums):
        super().__init__()
        self.k = k
        self.heap = list(nums)
        heapq.heapify(self.heap)           # O(n)
        while len(self.heap) > k:          # sirf k rakho
            heapq.heappop(self.heap)       # sab se chhota nikaal do

    def add(self, val):
        self.calls += 1
        heapq.heappush(self.heap, val)     # O(log k)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)       # extra (chhota) nikaal do
        return self.heap[0]                # root = k-th largest


# ---- LeetCode ka official example ----------------------------------------
kl = KthLargest(3, [4, 5, 8, 2])
assert kl.add(3) == 4       # [4,5,8] -> 3rd largest = 4
assert kl.add(5) == 5       # [5,5,8]
assert kl.add(10) == 5      # [5,8,10]
assert kl.add(9) == 8       # [8,9,10]
assert kl.add(4) == 8       # [8,9,10]
print("Example 1 pass. Final heap:", sorted(kl.heap, reverse=True))

# ---- Edge cases ----------------------------------------------------------
k1 = KthLargest(1, [])              # k=1 -> hamesha maximum
assert k1.feed([5, 2, 9, 1]) == [5, 5, 9, 9]      # base class ka feed() use hua!
print("k=1 (maximum) pass")

kdup = KthLargest(2, [7, 7])        # duplicates alag ginay jaate hain
assert kdup.add(7) == 7
print("duplicates pass")

kneg = KthLargest(2, [-10, -5])     # negative numbers
assert kneg.add(-7) == -7           # [-5,-7] -> 2nd largest = -7
print("negatives pass")

# ---- Brute force vs optimal: dono ka natija same hona chahiye ------------
import random
random.seed(42)                              # deterministic (test dobara chale to same)
stream = [random.randint(-50, 50) for _ in range(200)]
K = 4
fast, slow = KthLargest(K, stream[:5]), KthLargestBrute(K, stream[:5])
assert fast.feed(stream[5:]) == slow.feed(stream[5:])     # polymorphism: same feed()
print(f"\n195 random adds par brute-force aur heap ka jawab bilkul same [pass]")
print("calls counter (base class se):", fast.calls, slow.calls)
"""))

cells.append(md(r"""
### LC 933. Number of Recent Calls — Easy

**Link:** https://leetcode.com/problems/number-of-recent-calls/

**Bayan:** `RecentCounter` class. `ping(t)` call hoti hai (t badhta hua / strictly increasing
milta hai). Return karo kitni pings **`[t-3000, t]`** ke andar hain.

**Approach:**

- Purani pings jo `t - 3000` se pehle ki hain wo **kabhi dobara kaam nahi aayengi** (kyunke t
  sirf barhta hai) → unhein hamesha ke liye phenk do.
- `collections.deque` use karo: naya `t` right me `append`, aur left se `popleft` jab tak
  `queue[0] < t - 3000`.
- Jawab = `len(queue)`.
- Kyun deque, list nahi? `list.pop(0)` `O(n)` hai, `deque.popleft()` `O(1)`.

**Complexity:** har ping **amortized `O(1)`** (har element sirf ek baar andar, ek baar bahar),
space `O(n)` worst case (jab sab pings window ke andar hon).
"""))

cells.append(code(r"""
from collections import deque

class RecentCounter(StreamStructure):
    "Sliding window counter — window 3000ms."

    WINDOW = 3000                       # class constant (subclass isay override kar sakti hai)

    def __init__(self):
        super().__init__()
        self.q = deque()

    def ping(self, t):
        self.calls += 1
        self.q.append(t)                             # naya request
        while self.q and self.q[0] < t - self.WINDOW:
            self.q.popleft()                         # window se bahar -> hamesha ke liye gaya
        return len(self.q)

    # base class ke interface se jorna (polymorphism)
    def add(self, value):
        return self.ping(value)


rc = RecentCounter()
# LeetCode official example
assert rc.ping(1) == 1        # [1]
assert rc.ping(100) == 2      # [1,100]
assert rc.ping(3001) == 3     # [1,100,3001]  (1 abhi bhi andar: 3001-3000=1)
assert rc.ping(3002) == 3     # [100,3001,3002] (1 bahar ho gaya)
print("Example pass. Queue ab:", list(rc.q))

# ---- Edge cases ---------------------------------------------------------
rc2 = RecentCounter()
assert rc2.ping(1) == 1
assert rc2.ping(3001) == 2        # exactly boundary par -> ANDAR ginte hain (>= t-3000)
assert rc2.ping(3002) == 2        # 1 bahar
print("boundary (t-3000 exactly) pass")

rc3 = RecentCounter()
assert rc3.feed([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]      # sab window me
print("dense pings pass")

rc4 = RecentCounter()
assert rc4.ping(1) == 1
assert rc4.ping(1_000_000) == 1        # bara gap -> purani sab saaf
print("bara gap pass")

# ---- Subclass ka faida: window badalna (open/closed principle) ----------
class RecentCounter1s(RecentCounter):
    WINDOW = 1000                      # sirf constant override kiya, logic dobara nahi likha


r1s = RecentCounter1s()
assert r1s.feed([0, 500, 1500, 2500]) == [1, 2, 2, 2]
print("subclass (1s window) pass -> ek constant override, poora logic reuse")
"""))

cells.append(md(r"""
### LC 1352. Product of the Last K Numbers — Medium

**Link:** https://leetcode.com/problems/product-of-the-last-k-numbers/

**Bayan:** `add(num)` se numbers stream me aate hain. `getProduct(k)` last **k** numbers ka
product return kare.

**Approach (prefix products):**

- `prefix` list rakho jahan `prefix[i]` = shuru se `i` numbers ka product, `prefix[0] = 1`.
- Last k ka product = `prefix[-1] / prefix[-1-k]` — magar **division** floats me risky hai...
  is liye integers ke sath yahan safe hai (ye exact division hai), phir bhi `//` use karenge.
- **Zero ka kamaal (asli trick):** agar `num == 0` to aage koi bhi window jo us zero ko cover
  karti hai zero hi degi → poora `prefix` **reset** kar do (`[1]`).
  Phir `getProduct(k)`: agar `k >= len(prefix)` matlab window us zero tak pohnch rahi hai → `0`.

**Complexity:** `add` = `O(1)` amortized, `getProduct` = `O(1)`, space = `O(n)`.
(Brute force: `getProduct` = `O(k)` — last k ko loop kar ke multiply karna.)
"""))

cells.append(code(r"""
# ---- BRUTE FORCE ---------------------------------------------------------
class ProductOfNumbersBrute(StreamStructure):
    def __init__(self):
        super().__init__()
        self.nums = []

    def add(self, num):
        self.calls += 1
        self.nums.append(num)

    def getProduct(self, k):
        p = 1
        for x in self.nums[-k:]:        # O(k) har call
            p *= x
        return p


# ---- OPTIMAL: prefix products + zero reset ------------------------------
class ProductOfNumbers(StreamStructure):
    "prefix[i] = pehle i numbers ka product; zero par reset."

    def __init__(self):
        super().__init__()
        self.prefix = [1]               # sentinel

    def add(self, num):
        self.calls += 1
        if num == 0:
            self.prefix = [1]           # RESET: zero ke baad ka fresh start
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k):
        if k >= len(self.prefix):
            return 0                    # window kisi zero ko chhoo rahi hai
        # exact integer division (prefix[-1] prefix[-1-k] ka multiple hai)
        return self.prefix[-1] // self.prefix[-1 - k]


# ---- LeetCode official example -----------------------------------------
p = ProductOfNumbers()
for n in (3, 0, 2, 5, 4):
    p.add(n)
assert p.getProduct(2) == 20        # 5*4
assert p.getProduct(3) == 40        # 2*5*4
assert p.getProduct(4) == 0         # zero shamil
p.add(8)
assert p.getProduct(2) == 32        # 4*8
print("Example pass. prefix ab:", p.prefix)

# ---- Edge cases -------------------------------------------------------
p2 = ProductOfNumbers()
p2.add(7)
assert p2.getProduct(1) == 7                  # single element
print("single element pass")

p3 = ProductOfNumbers()
for n in (1, 2, 3, 4, 5):
    p3.add(n)
assert p3.getProduct(5) == 120                # poora stream
assert p3.getProduct(1) == 5
print("full stream pass")

p4 = ProductOfNumbers()
p4.add(0); p4.add(0)                          # lagatar zeros
assert p4.getProduct(1) == 0
print("consecutive zeros pass")

p5 = ProductOfNumbers()
for n in (2, 3, 0, 4):
    p5.add(n)
assert p5.getProduct(1) == 4 and p5.getProduct(2) == 0
print("zero ke baad recovery pass")

# ---- Brute force vs optimal: random cross-check -----------------------
random.seed(7)
fast_p, slow_p = ProductOfNumbers(), ProductOfNumbersBrute()
for _ in range(300):
    v = random.choice([0, 1, 2, 3, 4, 5])       # zeros bhi shamil
    fast_p.add(v); slow_p.add(v)
    kk = random.randint(1, min(6, len(slow_p.nums)))
    assert fast_p.getProduct(kk) == slow_p.getProduct(kk), (kk, slow_p.nums[-kk:])
print("\n300 random operations par prefix-product == brute force [pass]")
"""))

# ---------------------------------------------------------------------------
# 14. INTERVIEW Q&A
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 21. Interview Questions & Answers

**1. Inheritance kya hai aur iska sab se bara faida?**
Ek class doosri class ki attributes/methods haasil karti hai. Faida: code reuse +
IS-A relationship + polymorphism ki bunyaad + single point of change.

**2. `super()` asal me kya karta hai?**
Ye MRO me **agli** class ka proxy deta hai — sirf "parent" nahi. Multiple inheritance me
`super()` cooperative chain chalata hai taake koi class skip ya double na ho.

**3. `super().__init__()` aur `Parent.__init__(self)` me farq?**
`super()` MRO follow karta hai (diamond me base ek hi baar chalta hai) aur parent ka naam
hard-code nahi karta. Explicit call chain tor deti hai aur rename par toot jaati hai.

**4. MRO kya hai? Python kaunsa algorithm use karta hai?**
Method Resolution Order — lookup ki tarteeb. Algorithm: **C3 linearization**. Rules: class
khud pehle, parents left-to-right, koi class apne parent se pehle, har class sirf ek baar.
Dekhne ka tareeqa: `Class.__mro__` / `Class.mro()`.

**5. Diamond problem Python me hoti hai?**
Ambiguity C3 se hal ho jaati hai (base sirf ek baar). Agar hierarchy inconsistent ho to Python
class **banate hi** `TypeError` de deta hai — runtime surprise nahi.

**6. Method overriding vs method overloading?**
Overriding = **runtime**, child parent ka same-naam method dobara define karta hai (Python me
poora support). Overloading = **compile-time**, same naam different signatures — Python me
**nahi** (baad ki definition pehli ko replace kar deti hai). Workarounds: default args, `*args`,
`functools.singledispatch`.

**7. Polymorphism ki definition + Python me shaklein?**
Ek interface, kai implementations. Shaklein: operator polymorphism (`+`), function
polymorphism (`len`), method overriding (subtype), aur duck typing.

**8. Duck typing kya hai?**
Type ki jagah **behaviour** dekhna — agar zaroori method maujood hai to object chalega, chahe
inheritance na ho. EAFP (`try/except AttributeError`) Pythonic hai.

**9. `isinstance()` vs `type()` — kaun behtar aur kyun?**
`isinstance` — kyunke ye subclasses ko manta hai (LSP respect karta hai). `type(x) is C`
exact match karta hai aur valid subclass ko reject kar deta hai.

**10. `issubclass()` kab use hota hai?**
Jab tumhare paas **class** ho, object nahi: `issubclass(Dog, Animal)`. Factories/registries me
kaam aata hai.

**11. Mixin kya hai? Normal base class se farq?**
Mixin chhoti focused class hai jo sirf ek feature deti hai, akeli instantiate nahi hoti, aur
usually state (`__init__`) nahi rakhti. Normal base class domain ka "asli" parent hota hai.

**12. Multiple inheritance me `__init__` safely kaise handle karein?**
Har class `**kwargs` accept kare, apna hissa nikale, baqi `super().__init__(**kwargs)` ko de de.
Chain ke aakhir wali class extra kwargs par error de.

**13. Composition vs inheritance — kab kaun?**
Inheritance sirf asli IS-A + substitutability par. Warna composition (HAS-A) — loose coupling,
runtime swap, easy testing. Rule: *favour composition over inheritance*.

**14. Liskov Substitution Principle (LSP) simple lafzon me?**
Jahan parent ka object chalta hai, wahan child ka object bhi bila-toote chalna chahiye.
Practically: override me signature compatible rakho, naye required args na daalo, aur parent se
zyada strict exceptions na phenko.

**15. `NotImplementedError` aur `NotImplemented` me farq?**
`NotImplementedError` **exception** hai — abstract-jaise methods me `raise` karte hain.
`NotImplemented` ek **singleton value** hai jo binary operators (`__add__`, `__eq__`) return
karte hain taake Python doosre operand ko mauqa de (`__radd__`).

**16. Name mangling inheritance ko kaise affect karta hai?**
`__x` → `_ClassName__x`. Subclass ke andar `self.__x` `_SubClass__x` dhoondta hai → error.
Faida: naam clash se hifazat. Subclass ko dena ho to `_single` underscore use karo.

**17. `abstractmethod` aur `NotImplementedError` — kaun behtar?**
`abc.ABC` + `@abstractmethod` behtar: adhoori class ko **instantiate hi nahi** karne deta
(early failure). `NotImplementedError` sirf method call par pakra jata hai.

**18. `list`/`dict` se inherit karna kyun khatarnaak hai?**
Built-ins ke C-level methods tumhare overrides ko bypass kar sakte hain (`dict.update`
`__setitem__` ko call nahi karta). Use karo `collections.UserDict` / `UserList`, ya composition.

**19. Class attribute mutable ho to kya masla?**
Sab instances aur subclasses **wahi** object share karte hain — ek ne badla, sab ka badal gaya.
Fix: `__init__` me instance attribute banao.

**20. Kaise pata karein ke koi method kis class se aaya?**
`type(obj).__mro__` par loop chala kar pehli class dhoondo jis ke `__dict__` me naam ho; ya
`obj.method.__qualname__` dekho.

**21. `super()` bina arguments class ke bahar kaam karta hai?**
Nahi. Zero-arg `super()` compiler ke diye hue `__class__` cell par depend karta hai — sirf class
body ke andar. Bahar `super(Class, obj)` likhna paray ga.

**22. Multiple inheritance ke khatre?**
MRO ki complexity, naam clash, tight coupling, "kahan se aaya" debugging. Is liye mixins chhoti
aur focused rakho, ya composition use karo.
"""))

# ---------------------------------------------------------------------------
# 15. PRACTICE
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 22. Practice Exercises (khud karo)

1. **Library system** — `LibraryItem` base (title, id, `late_fee_per_day`) se `Book`,
   `DVD`, `Magazine` banao. Har ek ka late fee formula alag ho. `total_fees(items, days)`
   function likho jo kisi bhi mix par chale.
   *Hint:* base me `late_fee(days)` `NotImplementedError` raise kare.

2. **`__mro__` khud likho** — ek function `my_mro(cls)` banao jo `cls.__bases__` par
   depth-first chal kar linearization ki koshish kare, phir `cls.__mro__` se compare karo.
   Kis diamond me tumhara natija farq hoga? *Hint:* C3 sirf DFS nahi hai.

3. **Mixin banao** — `TimestampMixin` (created/updated), `SoftDeleteMixin`
   (`delete()` sirf flag set kare, `is_deleted` property), `AuditMixin` (har change ka log).
   Teenon ko ek `Post` class me plug karo. *Hint:* `**kwargs` cooperative pattern.

4. **Shape hierarchy + operator overloading** — `Shape` par `__lt__` (area se compare) aur
   `__eq__` do; phir `sorted(shapes)` aur `max(shapes)` chala kar dikhao.
   *Hint:* `functools.total_ordering`.

5. **LSP detector** — `check_lsp(parent, child)` function likho jo `inspect.signature` se
   dono ke common methods ke parameters compare kare aur warn kare jahan child ne
   **required** parameter add kiya ho. *Hint:* `inspect.signature(func).parameters`.

6. **Plugin registry** — base class `Plugin` banao jo `__init_subclass__` (bonus topic!) ya
   `__subclasses__()` se apne sab children ka registry rakhe, phir naam se plugin dhoondo.
   *Hint:* `{c.__name__.lower(): c for c in Plugin.__subclasses__()}`.

7. **Stack ko composition se banao (aur test karo)** — `Stack` ko `Queue` me convert karo
   sirf `_items` ke pop side badal kar; dono ke liye ek hi `drain()` function likho (duck typing).

8. **LC 703 without heap** — `bisect.insort` (sorted list) se karo. Complexity kya hui?
   Kaunsa version bare k par behtar hai aur kyun?

9. **LC 933 generalize** — `RecentCounter` ko is tarah likho ke window constructor se aaye
   (`RecentCounter(window=3000)`), aur `RecentCounter1s` ki tarah subclass banane ki zaroorat
   khatam ho jaye. Composition vs inheritance ka faisla likho.

10. **LC 1352 without division** — kya `getProduct` `O(1)` me bina division ho sakta? Suffix
    products ya do-stack technique par socho. *Hint:* "product of last k" me har `add` par
    poora suffix maintain karna `O(n)` ho jata hai — trade-off likho.
"""))

# ---------------------------------------------------------------------------
# 16. CHEAT SHEET
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 23. Summary / Cheat-sheet

### Syntax quick table

| Kaam | Code |
|---|---|
| Inherit karna | `class Child(Parent):` |
| Multiple inherit | `class C(A, B):` |
| Parent constructor | `super().__init__(args)` |
| Parent method | `super().method()` ya `Parent.method(self)` |
| Purana super form | `super(Child, self).method()` |
| Direct parents | `Class.__bases__` |
| Lookup order | `Class.__mro__` / `Class.mro()` |
| Children | `Class.__subclasses__()` |
| Object ka type check | `isinstance(obj, C)` ✅ / `type(obj) is C` ⚠️ |
| Class ka relation | `issubclass(D, C)` |
| Abstract-ish method | `raise NotImplementedError` |
| Operator ke liye | `return NotImplemented` |
| Comparisons mufat | `@functools.total_ordering` + `__eq__` + `__lt__` |
| Type-based dispatch | `@functools.singledispatchmethod` |
| dict/list extend karna | `collections.UserDict` / `UserList` |

### Inheritance ke types

| Type | Shakal |
|---|---|
| Single | `A → B` |
| Multilevel | `A → B → C` |
| Hierarchical | `A → B`, `A → C` |
| Multiple | `A, B → C` |
| Hybrid | mix (diamond) |

### MRO / C3 ke 4 rules

1. Class khud sab se pehle
2. Parents left-to-right
3. Child hamesha apne parent se **pehle** (monotonic)
4. Har class **sirf ek baar**

### Polymorphism ki 4 shaklein

`+` operator → built-in · `len()` → function · overriding → subtype · duck typing → structural

### Golden rules

- `__init__` me **pehla kaam** aksar `super().__init__(...)`.
- `super()` = MRO ka **next**, "parent" nahi.
- Override me signature **compatible** rakho (naye args ko default do) — LSP.
- `isinstance` use karo, `type()` comparison nahi.
- Mutable class attribute = shared state bug → `__init__` me banao.
- Mixins chhoti aur focused; state se bachne ki koshish karo.
- **Favour composition over inheritance** — jab IS-A pakka na ho.
- Built-ins (`list`/`dict`) se inherit karne se pehle `UserList`/`UserDict` socho.
- Type check ki jagah behaviour par bharosa (duck typing) + tests.

### Aage kya

**Notebook 04 — Magic (Dunder) Methods, `@classmethod` aur `@staticmethod`:**
`__str__` vs `__repr__` ki poori tafseel, `__eq__`/`__hash__` contract, container protocol
(`__len__`, `__getitem__`, `__iter__`), context managers (`__enter__`/`__exit__`), abstract base
classes (`abc`), classmethod factories, aur LeetCode design problems (Min Stack waghera).
"""))

save(r"OOP in Python/Basics/03_Inheritance_Polymorphism_aur_Method_Overriding.ipynb", cells)





