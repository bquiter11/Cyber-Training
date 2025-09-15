# Challenge 7: AES in ECB mode

import base64
from pathlib import Path

KEY = b"YELLOW SUBMARINE"

path = Path(r"C:\Users\brian\OneDrive\Documents\7.txt")
b64 = path.read_text()

ct = base64.b64decode(b64)
pt = AES.new(KEY, AES.MODE_ECB).decrypt(ct)

print(pt.decode(errors="replace")[:500])
