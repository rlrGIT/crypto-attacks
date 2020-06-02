#Thank you to Levente Buttyan (CrySyS Labs) for the design

import sys, getopt
import Crypto.Cipher.AES
import Crypto.Util.Counter

keystring = ''
inputfile = ''
outputfile = ''

try:
   opts, args = getopt.getopt(sys.argv[1:],"hk:i:o:")
except getopt.GetoptError:
   print('aes_ctr.py -k <keystring> -i <inputfile> -o <outputfile>')
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print('aes_ctr.py -k <keystring> -i <inputfile> -o <outputfile>')
      sys.exit()
   elif opt == "-k":
      keystring = arg
   elif opt == "-i":
      inputfile = arg
   elif opt == "-o":
      outputfile = arg


if len(keystring) != 16:
   print('Error: key string must be 16 character long')
   sys.exit(2)

if len(inputfile) == 0:
   print('Error: name of input file is missing')
   sys.exit(2)

if len(outputfile) == 0:
   print('Error: name of output file is missing')
   sys.exit(2)

ifile = open(inputfile, "rb")
ofile = open(outputfile, "wb")

ctr = Counter.new(128)
cipher = AES.new(keystring.encode("ASCII"), AES.MODE_CTR, counter=ctr)

eof = False
while (eof == False):
    plainblock = ifile.read(16)
    if len(plainblock) == 16:
        cipherblock = cipher.encrypt(plainblock)
        ofile.write(cipherblock)
    else:
        eof = True       
        if len(plainblock) > 0:
            # padding to fit block size
            plainblock += b'\x80'
            for i in range(16-len(plainblock)):
                plainblock += b'\x00'
            cipherblock = cipher.encrypt(plainblock) 
            ofile.write(cipherblock)

ifile.close() 
ofile.close()

print('Done.')
