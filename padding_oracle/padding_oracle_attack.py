# Starter code provided by Levente Buttyan
from Crypto.Cipher import DES
from Crypto.Util.strxor import strxor
from base64 import b64decode

PADDING_ERROR = True
PADDING_OK = False

def oracle(ciphertext):
    key = b64decode("bDMzdGhhY2s=")
    iv = ciphertext[:DES.block_size]
    payload = ciphertext[DES.block_size:]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    plaintext = cipher.decrypt(payload)

    plen = plaintext[-1]
    if (plen > DES.block_size-1):  # we allow only the minimum length padding needed
        return PADDING_ERROR
    elif (plen == 0):
        return PADDING_OK
    else:
        exp_padding = plaintext[-1].to_bytes(1, byteorder='big')*plen
        padding = plaintext[len(plaintext)-plen-1:-1]
        if (padding != exp_padding):
            return PADDING_ERROR
        else:
            return PADDING_OK

'''
=============================================================
The attack code that uses the above oracle can be found here.
Some parts are missing. Your task is to complete the program.
=============================================================
'''

# This is the ciphertext block that contains the password we want to break
Y = b'\x2d\x9a\x16\x26\x54\xb6\xca\x34'
#Y = b'\x7a\xd6\x4e\x9d\xf3\xe7\x2d\x14'    # another one for testing


# We always send a message of 2 blocks to the oracle:
# - the second block is the cipher block we want to break
# - the first block is the random block we play with


# We change the last byte of the random block until we get correct padding
r = 0
while (oracle(b'\x00'*(DES.block_size-1) + r.to_bytes(1, byteorder='big') + Y) == PADDING_ERROR):
    r += 1


# We know that the padding was correct, but don't know its length
# We determine the padding length here...
i = 1
while (i < DES.block_size):
    if (oracle(b'\x01'*(i) + b'\x00'*(DES.block_size-(i+1)) + r.to_bytes(1, byteorder='big') + Y) == PADDING_ERROR):
        plen = DES.block_size-i
        break
    i += 1
else:
    plen = 0

# Once we know the padding length, we also know the padding bytes themselves
# From the random block and padding bytes, we can compute the last bytes of the plaintext

P = plen.to_bytes(1, byteorder='big')*(plen+1)     # these are the padding bytes at the end
R = b'\x00'*plen + r.to_bytes(1, byteorder='big')  # these are the last bytes of the random block
X = b''
for i in range(plen+1):                            # their XOR will be the last bytes of the plaintext
    X += (P[i]^R[i]).to_bytes(1, byteorder='big')  # we store these bytes in X


# We determine the remaining missing bytes iteratively...
while (plen < DES.block_size-1):
    plen += 1                                      # we increase the padding length
    P = plen.to_bytes(1, byteorder='big')*plen     # end of the next valid padding
    R = b''
    for i in range(plen):                             # end of the random block that produces
        R += (P[i]^X[i]).to_bytes(1, byteorder='big') # the next valid padding

    r = 0           # byte in the random block that corresponds to the next missing byte
                    # we modify it until we get a correct padding again
    while (oracle(b'\x00'*(DES.block_size - (plen+1)) + r.to_bytes(1, byteorder='big') + R + Y) == PADDING_ERROR):
         #(oracle(____ put here: some byte x00 | r | R | Y ____) == PADDING_ERROR):
        r += 1
    X = (r^plen).to_bytes(1, byteorder='big') + X   # we compute the next missing byte
                                                    # and add to what we have so far

print(X)             # print what we have obtained at the end
