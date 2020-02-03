from FieldElement import FieldElement


 # the secp256k1 elliptic curve
P = 2**256 - 2**32 - 977

class S256Field(FieldElement):
    def __init__(self, num, order = None):
        super().__init__(num, order = P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

    def sqrt(self):
        return self**((P + 1) // 4)

