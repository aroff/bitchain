from Point import Point
from S256Field import S256Field

# Constants
A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

class S256Point(Point):

    def __init__(self, x, y, a = None, b = None):
        a, b = S256Field(A), S256Field(B)
        return super().__init__(x, y, a, b)


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)

print(infinity)
#S256Point(infinity)