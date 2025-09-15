import base64
from pathlib import Path
import collections

def hamming(a: bytes, b: bytes) -> int:
    if len(a) != len(b):
        raise ValueError("equal lengths required")
    return (int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).bit_count()

def repeating_xor(data: bytes, key: bytes) -> bytes:
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

def english_score(bs: bytes) -> float:
    try:
        s = bs.decode("ascii")
    except UnicodeDecodeError:
        return float("inf")
    if any(ord(c) < 9 or (13 < ord(c) < 32) for c in s):
        return float("inf")
    freq = {
        ' ': 0.182, 'E': 0.102, 'T': 0.091, 'A': 0.081, 'O': 0.076, 'N': 0.073,
        'I': 0.069, 'H': 0.069, 'S': 0.063, 'R': 0.061, 'D': 0.043, 'L': 0.040,
        'U': 0.028, 'M': 0.025, 'W': 0.024, 'F': 0.022, 'C': 0.022, 'G': 0.020,
        'Y': 0.020, 'P': 0.019, 'B': 0.015, 'V': 0.010, 'K': 0.008, 'X': 0.002,
        'J': 0.002, 'Q': 0.001, 'Z': 0.001
    }
    counts = collections.Counter(c if c.isalpha() else ' ' for c in s.upper())
    total = len(s)
    chi = 0.0
    for ch, exp in freq.items():
        obs = counts.get(ch, 0) / total
        chi += (obs - exp) ** 2 / (exp + 1e-9)
    return chi

def break_single_byte_xor(col: bytes) -> int:
    best_k, best_sc = 0, float("inf")
    for k in range(256):
        pt = bytes(b ^ k for b in col)
        sc = english_score(pt)
        if sc < best_sc:
            best_sc, best_k = sc, k
    return best_k

def main():
    assert hamming(b"this is a test", b"wokka wokka!!!") == 37
    path = Path(r"C:\Users\brian\OneDrive\Documents\6.txt")
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path}")
    b64_text = path.read_text().strip()
    ct = base64.b64decode(b64_text)
    candidates = []
    for K in range(2, 41):
        blocks = [ct[i:i+K] for i in range(0, K*4, K)]
        if len(blocks[-1]) != K:
            continue
        d = (hamming(blocks[0], blocks[1]) +
             hamming(blocks[1], blocks[2]) +
             hamming(blocks[2], blocks[3])) / 3.0
        candidates.append((d / K, K))
    candidates.sort()
    best_pt, best_key, best_sc = None, None, float("inf")
    print("Top keysize guesses:", [k for _, k in candidates[:5]])
    for _, K in candidates[:5]:
        cols = []
        for j in range(K):
            col = bytearray()
            for i in range(j, len(ct), K):
                col.append(ct[i])
            cols.append(bytes(col))
        key = bytes(break_single_byte_xor(col) for col in cols)
        pt = repeating_xor(ct, key)
        sc = english_score(pt)
        print(f"K={K:2d} key={key!r} score={sc:.2f}")
        if sc < best_sc:
            best_sc, best_key, best_pt = sc, key, pt
    print("\nRecovered key (bytes):", best_key)
    try:
        print("Recovered key (ascii):", best_key.decode())
    except UnicodeDecodeError:
        pass
    print("\nPlaintext preview:\n")
    print(best_pt.decode(errors="replace")[:800])

if __name__ == "__main__":
    main()
