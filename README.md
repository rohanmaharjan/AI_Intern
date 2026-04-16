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
     Variables in Python:<br />
     x = 10        # integer<br >
     name = "Ram"  # string<br >
     pi = 3.14     # float<br >
     is_valid = True  # boolean<br >
     **Rules for naming variable**<br >
     - Must start with a letter or underscore(_)
     - Cannot start with a number
     - Case-sensative (Age and age are different)
     - Should avoid reserved keywords such as class, def, if, for<br >
     Data-Types
     - integer (int): whole number e.g. x = 5<br >
     - float (float): Decimal number e.g y = 5.5<br >
     - string (str): Text e.g. name = "Rohan"<br >
     - boolean (bool): Logical values e.g. flag = True<br >
     - list: Ordered mutable collection e.g. nums = [1, 2, 3, 7, 8]<br >
     - tuple: Ordered immutable collection e.g. nums1 = (1, 2, 3, 4)<br >
     - set: unordered unique elements e.g. number = {1, 2, 3, 4}<br >
     - dictionary (dict): Key-value pairs e.g. student = { "name": "rohan", "age": 21 }<br />
       **Note: You can use type() function to check variable's type.**<br />
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
Default input:<br />
name = input("Enter your name: ")<br />
print("Hello,", name)<br />
It always takes data as string from the user. <br />
Converting into other data types:<br />
age = int(input("Enter your age: "))   # converts to integer<br />
pi = float(input("Enter value of pi: "))  # converts to float<br />
**Output**<br />
It is used to display data to the user. It use print() function. <br />
print("Hello World")   # simple output<br />
print("Name:", name)   # multiple values<br />
print(f"Age is {age}") # formatted string (f-string)<br />
**Formatting Output**<br />
x = 10<br />
y = 20<br />
print("Sum of {} and {} is {}".format(x, y, x+y)) # Output: Sum of 10 and 20 is 30
<br />
**End and Separator Paramenters:**<br />
print("Hello", end=" ")   # changes line ending<br />
print("World")            # Output: Hello World<br />
print(1, 2, 3, sep="-")   # Output: 1-2-3<br />






       

