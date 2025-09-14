# Challenge 4: Detect single-character XOR in a file (one hex per line)
# Put the puzzle file as set1/4.txt (from cryptopals)
import binascii, pathlib

def score(s: bytes) -> float:
    freq = " etaoinshrdlcumwfgypbvkjxqETAOINSHRDLCUMWFGYPBVKJXQ'"
    try: txt = s.decode()
    except: return -1
    return sum((i+1) for ch in txt for i,c in enumerate(freq) if ch==c)

best_line = None
best = (-1,None,None)
for line in pathlib.Path(__file__).with_name("4.txt").read_text().splitlines():
    ct = binascii.unhexlify(line.strip())
    for k in range(256):
        pt = bytes(b ^ k for b in ct)
        sc = score(pt)
        if sc > best[0]:
            best = (sc, k, pt)
            best_line = line.strip()

print("line:", best_line)
print("key:", best[1])
print("plaintext:", best[2].decode(errors="replace"))
