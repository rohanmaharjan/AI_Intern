'''
Write a Python program that takes a student’s marks as input and prints the grade based on the following criteria:
90 and above → A
80 to 89 → B
70 to 79 → C
60 to 69 → D
Below 60 → Fail
'''

try:
    marks = float(input("Enter marks of student: "))

    if marks>=90:
        print("A")
    elif marks>=80:
        print("B")
    elif marks>=70:
        print("C")
    elif marks>=60:
        print("D")
    else:
        print("Fail")
except ValueError:
    print("Please Input Correct Marks")