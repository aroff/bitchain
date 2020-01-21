from FieldElement import FieldElement


 # the secp256k1 elliptic curve
P = 2**256 - 2**32 - 977

class S256Field(FieldElement):
    def __init__(self, num):
        super().__init__(num, P)

    