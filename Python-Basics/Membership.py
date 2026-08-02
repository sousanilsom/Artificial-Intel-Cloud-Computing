# HOS03A: Membership Operators
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
