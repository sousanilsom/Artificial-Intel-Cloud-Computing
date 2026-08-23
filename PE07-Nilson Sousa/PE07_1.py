import math
class Shape():
    def __init__(self):
        pass
class Rectangle(Shape):
    def __init__(self):
        self.side_lengths = [5, 4] # x, y

    # task: return number of sides
    def getEdges(self):
        # a rectangle always has 4 sides
        return 4
    # task: return computed perimeter
    def computePerimeter(self):
        # perimeter = 2 * (length + width)
        x, y = self.side_lengths
        return 2 * (x + y)
    # task: return the area of the rectangle
    def computeArea(self):
        # area = length * width
        x, y = self.side_lengths
        return x * y

class Triangle(Shape):
    def __init__(self):
        self.side_lengths = [3, 6, 7] # 3 sides

    # task: return number of sides
    def getEdges(self):
        # a triangle always has 3 sides
        return 3
    # task: return computed perimeter
    def computePerimeter(self):
        # perimeter = sum of all 3 sides
        a, b, c = self.side_lengths
        return a + b + c
    # task: return the area of the triangle given 3 sides
    def computeArea(self):
        # Heron's formula: area = sqrt(s * (s-a) * (s-b) * (s-c))
        # where s is the semi-perimeter of the triangle
        # ref: https://www.cuemath.com/measurement/area-of-triangle-with-3-sides/
        a, b, c = self.side_lengths
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area

# creating objects for rectangle and triangle
r = Rectangle()
t = Triangle()

# calling its methods to print the # of sides, perimeter and the area.
print(r.getEdges())
print(r.computePerimeter())
print(r.computeArea())

print(t.getEdges())
print(t.computePerimeter())
print(t.computeArea())
