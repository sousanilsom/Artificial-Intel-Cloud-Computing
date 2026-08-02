import os

files_content = {
    "variable.py": '''# HOS03A: Multiple Assignments
print("\\nMultiple assignments")
a, b, c = 5, 3.2, "Hello"
print(a)
print(b)
print(c)

x = y = z = "python"
print(x)
print(y)
print(z)
''',
    "Strings.py": '''# HOS03A: String Functions & Concatenation
message = "this is also a string"
print(message)
print(message.title())
print(message.upper())
print(message.lower())

first_message = "Hi"
second_message = "how are you?"
full_message = first_message + " " + second_message
print(full_message)
''',
    "Numbers.py": '''# HOS03A: Numbers and Floating Point Operations
print("\\nFloat")
a = 2.2
b = 2
c = 0.1

print(a + b)
print(a + c)
print(a * b)
print(a ** b)
''',
    "Membership.py": '''# HOS03A: Membership Operators
a = 10
b = 20
elements = [1, 2, 3, 4, 5]

if a in elements:
    print("Line1 - a is available in the given list")
else:
    print("Line1 - a is not available in the given list")

if b not in elements:
    print("Line2 - b is not available in the given list")
else:
    print("Line2 - b is available in the given list")

a = 2
if a in elements:
    print("Line3 - a is available in the given list")
else:
    print("Line3 - a is not available in the given list")
''',
    "Identity.py": '''# HOS03A: Identity Operators
a = 20
b = 20

if (a is b):
    print("Line 1 - a and b have same identity")
else:
    print("Line 1 - a and b do not have same identity")

if (id(a) == id(b)):
    print("Line 2 - a and b have same identity")
else:
    print("Line 2 - a and b do not have same identity")

b = 30
if (a is b):
    print("Line 3 - a and b have same identity")
else:
    print("Line 3 - a and b do not have same identity")

if (a is not b):
    print("Line 4 - a and b do not have same identity")
else:
    print("Line 4 - a and b have same identity")
''',
    "Userinput.py": '''# HOS03A: User Input & Type Conversion
name = input("Please enter your name: ")
print("\\nWelcome to python, " + name + "!")
print("The type of the variable name is ", type(name))

age = input("\\nEnter your age: ")
age = int(age)
print("\\nYour age is ", age)
print("The type of the variable age is ", type(age))
''',
    "IfControl.py": '''# HOS03A: Decision Making
print('How old are you?')
age = int(input())

if age < 22:
    print('You are too young to have a drink.')
elif age >= 80:
    print('Ok, you will get a free drink.')
else:
    print('Sure, enjoy your drink.')
''',
    "WhileControl.py": '''# HOS03A: While Loop
print('This program will sum of numbers from 1 to a number you enter.')
print('Please enter a ending number: ')
num = int(input())
total = 0

while num >= 1:
    total += num
    num -= 1

print('The sum is: ' + str(total))
''',
    "While-else.py": '''# HOS03A: While Loop with Else
count = 0
while count < 5:
    print(count, " is less than 5")
    count = count + 1
else:
    print(count, " is not less than 5")
''',
    "ForControl.py": '''# HOS03A: For Loop
import random

for i in range(1, random.randint(5, 15)):
    print('This for loop has already run ' + str(i) + ' times.')
''',
    "ForElse.py": '''# HOS03A: For Loop with Else
for num in range(10, 20):
    for i in range(2, num):
        if num % i == 0:
            j = num / i
            print('%d equals %d * %d' % (num, i, j))
            break
    else:
        print(num, 'is a prime number')
''',
    "Break.py": '''# HOS03A: Break Statement
print("For-Break")
for letter in 'Python':
    if letter == 'h':
        break
    print('Current Letter :', letter)

print("\\nWhile-Break")
var = 10
while var > 0:
    print('Current variable value :', var)
    var = var - 1
    if var == 5:
        break
print("Good bye!")
''',
    "Continue.py": '''# HOS03A: Continue Statement
print("For-Continue")
for letter in 'Python':
    if letter == 'h':
        continue
    print('Current Letter :', letter)

print("\\nWhile-Continue")
var = 10
while var > 0:
    var = var - 1
    if var == 5:
        continue
    print('Current variable value :', var)
print("Good bye!")
''',
    "DataConversion.py": '''# HOS03A: Data Conversion
price = 10
print('How many beers you want?')
print('Your total price is: $' + str(price * int(input())))
'''
}

for filename, content in files_content.items():
    with open(filename, "w") as f:
        f.write(content)
    print(f"Created: {filename}")

print("\nAll 14 HOS03A files generated successfully!")
