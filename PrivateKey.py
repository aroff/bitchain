from random import randint
from S256Point import S256Point, N, G
from Signature import Signature

# this class will house our secret
class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def sign(self, z):
        k = randint(0, N) # random number integer from 0 to N. >>>>>>>>>>>>>>>> TODO: for real-world applications, need to use better generator
        r = (k * G).x.num; # is the x coordinate of kG
        k_inv = pow(k, N-2, N) # fermat's litthe theorem with n, which is a prime number
        s = (z + r * self.secret) * k_inv % N # s = (z + re) / k
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)