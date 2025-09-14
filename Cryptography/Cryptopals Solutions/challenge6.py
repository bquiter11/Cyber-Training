# Challenge 6: Break repeating-key XOR
# Put the provided base64 blob in set1/6.txt
import base64, itertools, pathlib

def hamming(a: bytes, b: bytes) -> int:
    x = int.from_bytes(a, 'big') ^ int.from_bytes(b, 'big')
    return x.bit_count()

data_b64 = pathlib.Path(__file__).with_name("6.txt").read_text()
ct = base64.b64decode(data_b64)

# guess key sizes
candidates = []
for ks in range(2, 41):
    chunks = [ct[i:i+ks] for i in range(0, ks*8, ks)]
    if len(chunks) >= 2 and len(chunks[-1]) == ks:
        d = sum(hamming(chunks[i], chunks[i+1]) for i in range(len(chunks)-1))
        norm = d / (ks * (len(chunks)-1))
        candidates.append((norm, ks))
candidates.sort()

def break_single_byte_xor(bs: bytes):
    def score(s: bytes) -> float:
        freq = " etaoinshrdlcumwfgypbvkjxqETAOINSHRDLCUMWFGYPBVKJXQ'"
        try: t = s.decode()
        except: return -1
        return sum((i+1) for ch in t for i,c in enumerate(freq) if ch==c)
    best = max(((k, bytes(b ^ k for b in bs)) for k in range(256)), key=lambda kv: score(kv[1]))
    return best[0]

best_pt, best_key = None, None
for _, ks in candidates[:5]:
    blocks = [ct[i:i+ks] for i in range(0, len(ct), ks)]
    transposed = list(itertools.zip_longest(*blocks, fillvalue=0))
    key = bytes(break_single_byte_xor(bytes(col)) for col in transposed)
    pt = bytes(ct[i] ^ key[i % len(key)] for i in range(len(ct)))
    try:
        test = pt.decode()
    except:
        continue
    if best_pt is None or test.count(" ") > best_pt.count(" "):
        best_pt, best_key = test, key

print("key:", best_key)
print(best_pt[:500])  # print a chunk; file is long
