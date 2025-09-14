import binascii

def score_english(s: bytes) -> float:
    freq = "ETAOIN SHRDLUetaoinshrdlu"  # common letters
    try:
        text = s.decode()
    except UnicodeDecodeError:
        return 0
    return sum(ch in freq for ch in text)

best_score = 0
best_result = None

with open(r"C:\Users\brian\OneDrive\Documents\4.txt") as f:
    for line in f:
        ct = binascii.unhexlify(line.strip())
        for key in range(256):
            pt = bytes([c ^ key for c in ct])
            sc = score_english(pt)
            if sc > best_score:
                best_score = sc
                best_result = (pt, key, line.strip())

print("Line:", best_result[2])
print("Key:", best_result[1])
print("Plaintext:", best_result[0].decode(errors="ignore"))

