# Elliptic-Curve Cryptography support

# Represents a element from a finite field set
class FieldElement:

    def __init__(self, num, order):
        if num >= order or num < 0:
            error = 'Num {} not in field range 0 to {}'.format(num, order-1)
            raise ValueError(error)
        self.num = num
        self.order = order

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.order, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.order == other.order

    def __ne__(self, other):
        # inverse of the == operator
        return not (self == other)        

    def checkOrder(self, other):
        if self.order != other.order:
            raise TypeError('Cannot execute the operation between two number in different fields')
        return True

    def __add__(self, other):
        self.checkOrder(self, other)
        num = (self.num + other.num) % self.order
        return self.__class__(num, self.order)

    def __sub__(self, other):
        self.checkOrder(other)
        num = (self.num - other.num) % self.order
        return self.__class__(num, self.order)

    def __mul__(self, other):
        self.checkOrder(other)
        num = (self.num * other.num) % self.order
        return self.__class__(num, self.order)

    def __pow__(self, exponent):
        # num = (self.num ** exponent) % self.order -> this version works for positive number, but is slow
        # num = pow(self.num, exponent, self.order) -> this is faster

        n = exponent % (self.order - 1)
        num = pow(self.num, n, self.order)
        return self.__class__(num, self.order)

    def __truediv__(self, other):
        self.checkOrder(other)
        # with fermat's little theorem:
        num = self.num * pow(other.num, self.order - 2, self.order) % self.order
        return self.__class__(num, self.order)

    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num=num, prime=self.prime)        

