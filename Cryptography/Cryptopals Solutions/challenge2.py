# Challenge 2: Fixed XOR (XOR two equal-length hex buffers)
import binascii

A = "1c0111001f010100061a024b53535009181c"
B = "686974207468652062756c6c277320657965"

ba = binascii.unhexlify(A)
bb = binascii.unhexlify(B)
res = bytes(x ^ y for x, y in zip(ba, bb))
print(res.hex())
