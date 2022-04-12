'''
    File name: rijndael_field.py
    Author: Maks Górski
    Date created: 11/01/2020
    Date last modified: 11/11/2020
    Python Version: 3.6
    Purpose: Definied algebra of Rijndael Field.
'''

__all__ = ['Rijndael']
__author__ = "Maks Górski"
__license__ = "Public domain"
__email__ = "maksymilian_gorski@wp.pl"

import random

class Rijndael:
    
    reducer = [1,1,0,1,1,0,0,0,1]

    def __init__(self, binary_array):
        if len(binary_array) != 8:
            raise ValueError("The input array must be the length of 8.")

        for i in binary_array:
            if i != 1 and i != 0:
                raise ValueError("Elements of the array must be equal to 0 or 1.")
        
        self.values = binary_array

    def __int__(self):
        int_value = 0
        for i, value in enumerate(self.values):
            int_value += value * 2**i
        return int_value

    def __add__(self, other):
        sum = [0] * len(self.values)
        for i in range(len(sum)):
            if self.values[i] ^ other.values[i]:
                sum[i] = 1
        return self.__class__(sum)

    def __sub__(self, other):
        sub = [0] * len(self.values)
        for i in range(len(sub)):
            if self.values[i] ^ other.values[i]:
                sub[i] = 1
        return self.__class__(sub)

    def __neg__(self):
        return self

    def __mul__(self, scalar):
        a = self
        print(a)
        for i in range(scalar-1):
            a = a + self

        return a
    
    __rmul__ = __mul__

    # def __matmul__(self, other):
    #     if self == Rijndael.zero() or other == Rijndael.zero():
    #         return self.__class__.zero()
    #     exp = Rijndael.log(self) + Rijndael

    def __div__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        for i in range(len(self.values)):
            if self.values[i] != other.values[i]:
                return False
        return True

    def __str__(self):
        string = ""
        for i in range(len(self.values)-1,-1,-1):
            string += str(self.values[i]) + "; "
        return string

    
    def __hash__(self):
        return hash(tuple(self.values))

    def log(self):
        if int(self) == 0:
            raise ValueError("Argument of the logarithm must not be 0.")

        power = Rijndael.generator()
        for i in range(1,256,1):
            if(power.values == self.values):
                return i
            power = self.__class__.long_multiplication(power, Rijndael.generator())

    def invert(self):
        raise NotImplementedError

    @classmethod
    def exponentation(cls, self, exponent):
        if(exponent == 0):
            return Rijndael.one()

        rij = self
        for i in range(exponent-1):
            rij = Rijndael.long_multiplication(rij, self)
        return rij

    @classmethod
    def long_multiplication(cls, self, other):
        product = [0] * (len(self.values) + len(other.values) - 1)
        for i, value1 in enumerate(self.values):
            for j, value2 in enumerate(other.values):
                product[i + j] ^= value1 * value2

        for i in range(len(product)-1,7,-1):
            if product[i] == 1:
                reducer_index = 0
                for j in range(i-8, i+1, 1):
                    product[j] ^= Rijndael.reducer[reducer_index]
                    reducer_index += 1
            
        ret = [0] * 8
        for i in range(len(self.values)):
            ret[i] = product[i]
            
        return self.__class__(ret)
    
    @classmethod
    def fast_multiplication(cls, self, other):
        NotImplemented

    @classmethod
    def zero(cls):
        return cls([0] * 8)
    
    @classmethod
    def one(cls):
        values = [0] * 8
        values[0] = 1
        return cls(values)

    @classmethod
    def generator(cls):
        return cls.from_int(3)

    @classmethod
    def from_int(cls, number):
        if number > 255 or number < 0:
            raise ValueError("Entered integer must be in range from 0 to 255.")
        values = [0] * 8
        for i in range(len(values)-1,-1,-1):
            if number >= 2**i:
                values[i] += 1
                number -= 2**i
        return cls(values)

    @classmethod
    def all_elements(cls):
        for i in range(256):
            values = [0] * 8
            num = i
            for j in range(len(values)-1,-1,-1):
                if num == 0:
                    values[j] = 0
                    continue

                if num >= 2**(j):
                    values[j] = 1
                    num -= 2**(j)
                else:
                    values[j] = 0
            yield cls(values)

    @staticmethod
    def random_element():
        return Rijndael.from_int(random.randrange(0, 256))

if __debug__ and __name__ == '__main__':
    zero = Rijndael.zero()
    one = Rijndael.one()

    for i, value in enumerate(Rijndael.all_elements()):
        assert i == int(value)

    for i in Rijndael.all_elements():
        assert i == i
        assert i + zero == i
        assert Rijndael.long_multiplication(i, Rijndael.one()) == i
        assert i + (-i) == zero
        assert Rijndael.exponentation(i,2) == Rijndael.long_multiplication(i,i)
        assert Rijndael.exponentation(i,5) == Rijndael.long_multiplication(Rijndael.exponentation(i,2),Rijndael.exponentation(i,3))
        #try:
        #    assert i/i == one
        #except: 
        #    assert i == zero
        #try:
        #    assert i * i.invert() == one
        #except:
        #    assert i.invert() == zero
        #for j in Rijndael.all_elements():
        #    assert i + j == j + i
        #    assert Rijndael.long_multiplication(i,j) == Rijndael.long_multiplication(j,i)
        #    assert Rijndael.exponentation(Rijndael.long_multiplication(i,j), 2) == Rijndael.long_multiplication(Rijndael.exponentation(i,2), Rijndael.exponentation(j,2))
        #    for k in Rijndael.all_elements():
        #        assert i + (j + k) == (i + j) + k
        #        assert Rijndael.long_multiplication(i,(j + k)) == Rijndael.long_multiplication(i,j) + Rijndael.long_multiplication(i,k)