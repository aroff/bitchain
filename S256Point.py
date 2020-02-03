from Point import Point
from S256Field import S256Field

# Constants
A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

class S256Point(Point):

    def __init__(self, x, y, a = None, b = None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x, y, a, b)

    # verify signature
    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N) # is calculated using Fermat's little theorem on the order of the group n, which is prime
        u = z * s_inv % N # we mod by N , as that's the order of the group
        v = sig.r * s_inv % N # v = r/s . we mod by N , as that's the order of the group
        total = u * G + v * self # uH + vP 
        return total.x.num == sig.r # check if x coordinate is equal to r
    
    # returns the binary version of the SEC format
    def sec(self, compressed=True):
        # if compressed, starts with b'\x02' if self.y.num is even, b'\x03' if self.y is odd
        # then self.x.num
        # remember, you have to convert self.x.num/self.y.num to binary (some_integer.to_bytes(32, 'big'))
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            # if non-compressed, starts with b'\x04' followod by self.x and then self.y
            return b'\x04' + self.x.num.to_bytes(32, 'big') + \
                self.y.num.to_bytes(32, 'big')     

G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
