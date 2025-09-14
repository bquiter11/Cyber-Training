# Challenge 3: Break single-byte XOR
import binascii, string

HEX = "1b37373331363f78151b7f2b783431333d78397828372d36" \
      "3c78373e783a393b3736"

def score(s: bytes) -> float:
    freq = " etaoinshrdlcumwfgypbvkjxqETAOINSHRDLCUMWFGYPBVKJXQ'"
    return sum((i+1) for ch in s.decode(errors="ignore") for i,c in enumerate(freq) if ch==c)

ct = binascii.unhexlify(HEX)
best = max(((k, bytes(b ^ k for b in ct)) for k in range(256)), key=lambda kv: score(kv[1]))
key, pt = best
print(key, pt.decode(errors="replace"))
