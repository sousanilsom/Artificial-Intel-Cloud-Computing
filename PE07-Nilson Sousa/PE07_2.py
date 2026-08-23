class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    # Suppose we want the print() function to print the coordinates of the Point object
    # instead of what we got. We can define a __str__() method in our class that controls
    # how the object gets printed. Let's look at how we can achieve this:
    # Redefining p1.__str__() --> our point coordinate system
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)
    # redefining __add__ function to overload an existing operator
    def __add__(self, rhs):
        x = self.x + rhs.x
        y = self.y + rhs.y
        return x, y

    # task: "-" operator overloading __sub__()
    def __sub__(self, rhs):
        # subtract the corresponding x and y coordinates
        x = self.x - rhs.x
        y = self.y - rhs.y
        return x, y

    # task: ">" operator overloading __gt__() (only if both x1 and y1 are greater than x2 and y2
    # (10, 2) > (8, 1) (return True)
    # (10, 2) > (12, 0) (return False since x1(10) is less than x2(12)
    def __gt__(self, rhs):
        # return True only when both x and y of self are greater than rhs's x and y
        return self.x > rhs.x and self.y > rhs.y

p1 = Point(13, 15)
p2 = Point(-1, 8)

print(p1)
print(p2)
print(p1 + p2) # p1+p2 ==> p1.__add__(p2), p1 <- self, p2 <- rhs

# task: "-" operator overloading __sub__()
print(p1 - p2)
# task: ">" operator overloading __gt__() (only if both x1 and y1 are greater than x2 and y2
# (10, 2) > (8, 1) (return True)
# (10, 2) > (12, 0) (return False since x1(10) is less than x2(12)
print(p1 > p2)
