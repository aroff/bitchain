from FieldElement import FieldElement
from Point import Point

a = FieldElement(0, 223)
b = FieldElement(7, 223)
x = FieldElement(15, 223)
y = FieldElement(86, 223)

p = Point(x, y, a, b)
#print(7 * p)