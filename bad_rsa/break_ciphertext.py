# CAUTION: this script is written in Python 2, run it as "python break_ciphertext.py"

import bad_rsa 

#My imports were not working, so I moved this here.
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

f = open("rsapubkey.txt", "r")
e = long(f.readline())
n = long(f.readline())
f.close()

rsa = bad_rsa.bad_rsa({'e':e, 'n':n, 'd':0})

key = rsa.getKey()
e = key['e']
n = key['n']

print("\nPublic key: ")
print(e)
print(n)

f = open("ciphertext.txt", "r")
ciphertext = long(f.read())
f.close()

print("\nCiphertext: ")
print(ciphertext)

# Compute the plaintext as the e-th root of the ciphertext.
# Identify and use the appropriate function for computing e-th root in the textbookRSA.py module!
plaintext = findInvPow(ciphertext, e)

print("\nPlaintext recovered: ")
print(plaintext)

plaintext_ascii = ''.join([chr(int(hex(plaintext)[i:i+2], 16)) for i in xrange(2,len(hex(plaintext))-1,2)])

print("\nPrinted as a string: ")
print(plaintext_ascii + "\n")
