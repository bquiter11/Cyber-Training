import pathlib, binascii

path = pathlib.Path(r"C:\Users\brian\OneDrive\Documents\8.txt")
lines = path.read_text().splitlines()

def repeated_blocks_score(bs: bytes, block=16):
    blocks = [bs[i:i+block] for i in range(0, len(bs), block)]
    return len(blocks) - len(set(blocks))

best = max(
    ((i, repeated_blocks_score(binascii.unhexlify(line.strip()))) for i, line in enumerate(lines, 1)),
    key=lambda x: x[1]
)

print("ECB likely on line:", best[0], "with repeat score:", best[1])
