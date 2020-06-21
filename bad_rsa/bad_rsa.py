# CAUTION: this module is written in Python 2

import os
import random
import math

####Prime Functions####
def millerRabin(m, k):
    """
    Miller Rabin pseudo-prime test
    return True means likely a prime, (how sure about that, depending on k)
    return False means definitely a composite.
    """
    s=1
    d = (m-1)/2
    while d%2 == 0:
        d /= 2
        s += 1
    for r in range(0,k):
        rand_num = random.randint(1,m-1)
        y = pow(rand_num, d, m)
        prime = False
        if (y == 1):
            prime = True            
        for i in range(0,s):
            if (y == m-1):
                prime = True
                break
            else:
                y = (y*y)%m                
        if not prime:
            return False
    return True

def findAPrime(a, b, k):
    """Return a pseudo prime number roughly between a and b,
    (could be larger than b). Raise ValueError if cannot find a
    pseudo prime after 10 * ln(x) + 3 tries. """
    x = random.randint(a, b)
    for i in range(0, int(10 * math.log(x) + 3)):
        if millerRabin(x, k):
            return x
        else:
            x += 1

    raise ValueError

####Modular Arithmetics####
def gcd(x, y):
    """returns the Greatest Common Divisor of x and y"""
    while y != 0:
        (x, y) = (y, x % y)
    return x

def egcd(a, b):
    """return a tuple of three values: x, y and z, such that x is
    the GCD of a and b, and x = y * a + z * b"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modInv(a, m):
    """returns the multiplicative inverse of a in modulo m as a
    positive value between zero and m-1"""
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def modExp(a, d, n):
    """returns a ** d (mod n)"""
    assert d >= 0
    assert n >= 0
    base2D = int2baseTwo(d)
    base2DLength = len(base2D)
    modArray = []
    result = 1
    for i in range(1, base2DLength + 1):
        if i == 1:
            modArray.append(a % n)
        else:
            modArray.append((modArray[i - 2] ** 2) % n)
    for i in range(0, base2DLength):
        if base2D[i] == 1:
            result *= base2D[i] * modArray[i]
    return result % n

def findInvPow(x,n):
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

def int2baseTwo(x):
    """x is a positive integer. Convert it to base two as a list of integers
    in reverse order as a list."""
    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse

####RSA Functions#####
class bad_rsa:
    def __init__(self, rsaKey=None):
        if rsaKey == None:
            rsaKey = self._newKey(2 ** 1023, (2 ** 1024) - 1, 100)
        self.key = rsaKey
    
    def _newKey(self, a, b, k):
        try:
            p = findAPrime(a, b, k)
            while True:
                q = findAPrime(a, b, k)
                if q != p:
                    break
        except:
            raise ValueError

        n = p * q
        m = (p - 1) * (q - 1)

        # Optimize for decryption speed        
        #while True:
            #limit = findInvPow(n, 4) >> 16
            #d = random.randint(1, limit)
            #if gcd(d, m) == 1:
            #    break
        #e = modInv(d, m)
        
        #e = 3               
        e = 2**16 + 1
        d = modInv(e, m)
        
        return {'n': n, 'e':e, 'd':d}
        
    def encrypt(self, msg):
        msgNum = int(msg.encode('hex'), 16)
        msgCrypt = modExp(msgNum, self.key['e'], self.key['n'])
        return msgCrypt
    
    def decrypt(self, num):
        msgNum = modExp(num, self.key['d'], self.key['n'])
        msg = ''.join([chr(int(hex(msgNum)[i:i+2], 16)) for i in xrange(2,len(hex(msgNum))-1,2)])
        return msg
    
    def getKey(self):
        return self.key

