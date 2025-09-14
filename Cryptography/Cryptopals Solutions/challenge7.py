# Challenge 7: AES in ECB mode
# Requires: pip install pycryptodome
# Put the base64 ciphertext in set1/7.txt (from cryptopals)
from Crypto.Cipher import AES
import base64, pathlib

KEY = b"YELLOW SUBMARINE"
b64 = pathlib.Path(__file__).with_name("7.txt").read_text()
ct = base64.b64decode(b64)
pt = AES.new(KEY, AES.MODE_ECB).decrypt(ct)
print(pt.decode(errors="replace")[:500])
