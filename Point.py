from FieldElement import FieldElement

# point 

class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is none and self.y is none:
            return
        if self.y**2 != self.x**3 + a * x + b:
            raise TypeError('Points {}, {} are not on the same curve'.format(x, y))

