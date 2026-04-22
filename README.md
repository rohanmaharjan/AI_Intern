# AI_Intern
# Getting Started With Python Basics
# Instalation and runnig Python
   a. Download Python
   - Go to python.org
   - Choose latest stable version<br />
   b. Verify Installation
   - open Command Prompt or Termainal and type<br />
     python --version or python3 --version
     You should see your installed python version (e.g. 3.12.2)<br />
   c. Running Python
   - Interactive mode<br />
     Open terminal and type<br />
     python<br />
     you should see >>> prompt
   - Script mode<br />
     python filename.py or py filename.py<br />
# Variables and Data Types
     A variable refers to a name that refers to a value stored in memory.
     Variables in Python:
     x = 10        # integer
     name = "Ram"  # string
     pi = 3.14     # float
     is_valid = True  # boolean
     
     **Rules for naming variable**
     - Must start with a letter or underscore(_)
     - Cannot start with a number
     - Case-sensative (Age and age are different)
     - Should avoid reserved keywords such as class, def, if, for
     Data-Types
     - integer (int): whole number e.g. x = 5
     - float (float): Decimal number e.g y = 5.5
     - string (str): Text e.g. name = "Rohan"
     - boolean (bool): Logical values e.g. flag = True
     - list: Ordered mutable collection e.g. nums = [1, 2, 3, 7, 8]
     - tuple: Ordered immutable collection e.g. nums1 = (1, 2, 3, 4)
     - set: unordered unique elements e.g. number = {1, 2, 3, 4}
     - dictionary (dict): Key-value pairs e.g. student = { "name": "rohan", "age": 21 }
       **Note: You can use type() function to check variable's type.**
       Example: print(type(x))<br />
# Operators>
Operators are special symbols that perform operations on variables and values.<br /> **Types of Operators**
- Arithemattic Operators: +, -, *, /, //(floor division), %, ** (exponent)
- Comparision or Relational Operators: Used to compare True or False. ==, !=, >, <, <=, >=
- Logical Operators: Used to combine conditional statemants. and, or, not
- Assignment Operators: Used to assign values with shorthand. =, +=, -=, *=, /=, %=, **=
- Bitwise Operators: Works at binary level. &(AND), |(OR), ^(XOR), ~(NOT), <<(Left Shift), >>(Right Shift)
- Membership Operators: Check if value exists in a qequence. in, not in<br />
Example:<br/>
num = [1, 2, 3]<br />
print(2 in num) # true<br />
print(5 not in num) # true
- Identity Operators: Check if two objects share the same memory location.<br/>
Example: <br />
x = [1, 2, 3]<br />
y = [1, 2, 3]<br />
z = x<br />
print(x is y)      # False (different objects)<br />
print(x is z)      # True (same object)<br />
print(x is not y)  # True<br />
# Input and Output
**Input**<br /> Used to take data form the user. It used input() function to take data and it always returns data as a **string**.<br />
Default input:
```python
name = input("Enter your name: ")
print("Hello,", name)
```

---

It always takes data as string from the user. <br />
Converting into other data types:
```python
age = int(input("Enter your age: "))   # converts to integer
pi = float(input("Enter value of pi: "))  # converts to float
```

---

**Output**<br />
It is used to display data to the user. It use print() function. <br />
print("Hello World")   # simple output<br />
print("Name:", name)   # multiple values<br />
print(f"Age is {age}") # formatted string (f-string)<br />
**Formatting Output**
```python
x = 10
y = 20
print("Sum of {} and {} is {}".format(x, y, x+y)) # Output: Sum of 10 and 20 is 30
```

---

**End and Separator Paramenters:**
```python
print("Hello", end=" ")   # changes line ending
print("World")            # Output: Hello World
print(1, 2, 3, sep="-")   # Output: 1-2-3
```

---

# Conditional Statements
Conditional statements let you control the flow of execution based on conditions (True/False).<br />
## if Statement
Executes a block of code if the condition is true.

```python
x = 10
if x > 5:
    print("x is greater than 5")
```

---

## if-else Statement
Provides an alternative block if the condition is false.

```python
x = 3
if x > 5:
    print("x is greater than 5")
else:
    print("x is not greater than 5")
```

---

# if-elif-else statement
Checks multiple conditions in sequence.
```python
marks = 75

if marks >= 90:
    print("Grade: A")
elif marks >= 75:
    print("Grade: B")
elif marks >= 50:
    print("Grade: C")
else:
    print("Grade: F")
```

---

# nested if
an if inside another if
```python
num = 15

if num > 0:
    if num % 2 == 0:
        print("Positive even number")
    else:
        print("Positive odd number")
```

---

# Ternary operator / shoet hand if
Compact way to write if-else.
```python
x = 10
result = "Even" if x % 2 == 0 else "Odd"
print(result)   # Output: Even
```

---

# Loops
Loops are used to repeat a block of code multiple times until a condition is met.
# for loop
Used to iterate over a sequence (list, tuple, string, range, etc.).
```python
# Using range
for i in range(5):
    print(i)   # Output: 0 1 2 3 4

# Iterating a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

---

# while loop
Repeats as long as the condition is true.
```python
count = 0
while count < 5:
    print("Count:", count)
    count += 1
```

---

# loop control statemanet
- break --> exits loop immediately
- continue --> skips the current iteration and moves to the next
- else with loops --> runs if the loop finnishes normally (not interrupted by break).
```python
# break example
for i in range(10):
    if i == 5:
        break
    print(i)   # Output: 0 1 2 3 4

# continue example
for i in range(5):
    if i == 2:
        continue
    print(i)   # Output: 0 1 3 4

# else with loop
for i in range(3):
    print(i)
else:
    print("Loop finished!")  # runs after loop ends
```

---

# Nested loops
Loops inside loops.
```python
for i in range(3):
    for j in range(2):
        print(i, j)
```

---

# Data Structures in Python
Data structures are ways to store and organize data efficiently. Python provides several built-in ones.
# List
They are ordered and mutable collection and allows duplicates.
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")   # add element
fruits[1] = "mango"       # modify element
print(fruits)             # ['apple', 'mango', 'cherry', 'orange']
```

---

**List Operations**
```python
nums = [1, 2, 3]

nums.append(4)       # Add element -> [1,2,3,4]
nums.insert(1, 10)   # Insert at index -> [1,10,2,3,4]
nums.remove(2)       # Remove first occurrence -> [1,10,3,4]
nums.pop()           # Remove last element -> [1,10,3]
nums.pop(0)          # Remove at index -> [10,3]
nums.sort()          # Sort ascending -> [3,10]
nums.reverse()       # Reverse order -> [10,3]
len(nums)            # Length -> 2
```

---

# Tuple
They are ordered and immutable collection. They are faster than lists and used for fixed data.
```python
coords = (10, 20)
print(coords[0])   # 10
# coords[0] = 15 -> Error (immutable)
```

---

**Tuple Operations**
```python
coords = (10, 20, 30)
coords.count(10)     # Count occurrences -> 1
coords.index(20)     # Find index -> 1
len(coords)          # Length -> 3
```

---

# Set
Unordered, mutable collection. No duplicates are allowed.
```python
nums = {1, 2, 3, 3}
print(nums)   # {1, 2, 3}
nums.add(4)
print(nums)   # {1, 2, 3, 4}
```

---

**Set Operations**
```python
s = {1, 2, 3}

s.add(4)             # Add element -> {1,2,3,4}
s.remove(2)          # Remove element -> {1,3,4}
s.discard(5)         # Remove if exists, no error
s.clear()            # Empty set -> {}
s1 = {1,2,3}; s2 = {3,4,5}
s1.union(s2)         # {1,2,3,4,5}
s1.intersection(s2)  # {3}
s1.difference(s2)    # {1,2}
```

---

# Dictionary
They are key-value pairs. Keys must be unique and immutable.
```python
student = {"name": "Ram", "age": 20}
print(student["name"])   # Ram
student["age"] = 21      # update value
student["grade"] = "A"   # add new key-value
```

---

**Dictionary Operations**
```python
student = {"name": "Ram", "age": 20}

student["grade"] = "A"   # Add new key-value
student["age"] = 21      # Update value
del student["name"]      # Delete key
student.keys()           # dict_keys(['age','grade'])
student.values()         # dict_values([21,'A'])
student.items()          # dict_items([('age',21),('grade','A')])
student.get("age")       # 21
student.pop("grade")     # Remove key → returns 'A'
```

---

# Functions
Functions are reusable blocks of code that perform a specific task. They help make programs modular, organized, and easier to maintain.<br />
**Defining a Function**<br />**def** function_name()
```pyhton
def greet():
    print("Hello, welcome to Python!")
```

---

**Calling a Function**<br />function_name()
```python
greet()   # Output: Hello, welcome to Python!
```

---

# Functions with Parameters
Parameters allow you to pass values into a function.
```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)   # Output: 8
```

---

# Default Parameters
```python
def greet(name="Guest"):
    print("Hello,", name)

greet()          # Output: Hello, Guest
greet("Ram")     # Output: Hello, Ram
```

---

# Return Statement
Functions can return values using return.
```python
def square(x):
    return x * x

print(square(4))   # Output: 16
```

---

# String Methods
A string is a sequence of characters enclosed in single quotes '...', double quotes "...", or triple quotes '''...''' / """...""" (for multi-line). Strings are immutable i.e. once created, they cannot be changed directly.
```python
text1 = 'Hello'
text2 = "World"
text3 = '''This is
a multi-line string'''
```

---

**Concatenation**
```python
a = "Hello"
b = "World"
print(a + " " + b)   # Hello World
```

---

**Repetition**
```python
print("Hi! " * 3)    # Hi! Hi! Hi!
```

---

**Indexing and Slicing**
```python
text = "Python"
print(text[0])       # P (first character)
print(text[-1])      # n (last character)
print(text[0:4])     # Pyth (slice from index 0 to 3)
print(text[::-1])    # nohtyP (reverse string)
```

---

**Length**
```python
print(len("Python"))   # 6
```

---

**Other String Methods**
```python
"hello".upper()                  #"HELLO"
"HELLO".lower()                  #hello"
"python".capitalize()            #Python"
"hello world".title()            #Hello world"
" hi ".strip()                   #"hi"
"apple".replace("a","A")         #"Apple"
"a,b,c".split(",")               #['a', 'b', 'c']
" ".join(["Hello","World"])      #"Hello World"
"Python".find("th")              #2
"banana".count("a")              #3
```

---

# File Handling
File handling allows you to create, read, write, and manage files directly from Python programs.
# Opening a file
Use open() function
```python
f = open("example.txt", "r")   # open for reading
```

---

**Modes**
- "r": read (default)
- "w": write (creates/overwrites file)
- "a": append (adds to end of file)
- "b": binary mode (images, videos)
- "x": create new file (error if exists)

# Reading from a File
```python
f = open("example.txt", "r")
print(f.read())       # read entire file
print(f.readline())   # read one line
print(f.readlines())  # read all lines into list
f.close()
```

---

# Writing to a File
```python
f = open("example.txt", "w")
f.write("Hello, Python!\n")
f.write("File handling is easy.")
f.close()
```

---

# Appending to a File
```python
f = open("example.txt", "a")
f.write("\nThis line is appended.")
f.close()
```

---

# Using with
It automatically closes file after use.
```python
with open("example.txt", "r") as f:
    data = f.read()
    print(data)
```

---

**Always use seek(0) if you want to read after writing, because the file pointer moves to the end after write/apend operations**

# Object-Oriented Programmig
OOP is a programming paradigm that organizes code into objects (instances) and classes (blueprints). It helps make code more modular, reusable, and easier to maintain.
```python
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def drive(self):
        print(f"{self.brand} {self.model} is driving")

# Create object
my_car = Car("Toyota", "Corolla")
my_car.drive()   # Output: Toyota Corolla is driving
```

---

## Key OOP Concepts
**Encapsulation**<br />Encapsulation is a fundamental principle of Object-Oriented Programming (OOP) that involves bundling data (attributes) and the methods that operate on that data into a single unit, typically a class. 
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance   # private attribute
    
    def deposit(self, amount):
        self.__balance += amount
    
    def get_balance(self):
        return self.__balance
```

---

**Inheritance**<br />Allows a class to inherit properties/methods from another class.
```python
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):   # Dog inherits from Animal
    def speak(self):
        print("Woof!")

d = Dog()
d.speak()   # Output: Woof!
```

---

**Polymorphism**<br />Same method name behaves differently depending on the object.
```python
class Cat:
    def speak(self):
        print("Meow!")

class Dog:
    def speak(self):
        print("Woof!")

for pet in [Cat(), Dog()]:
    pet.speak()
# Output: Meow! Woof!
```

---

**Abstraction**<br />Hiding implementation details, showing only essential features.
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r * self.r

c = Circle(5)
print(c.area())   # 78.5
```

---






       

