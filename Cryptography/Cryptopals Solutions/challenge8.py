# Challenge 8: Detect AES in ECB mode (by repeated 16-byte blocks)
# Put the hex-encoded lines in set1/8.txt
import pathlib, binascii

lines = pathlib.Path(__file__).with_name("8.txt").read_text().splitlines()
def repeated_blocks_score(bs: bytes, block=16):
    blocks = [bs[i:i+block] for i in range(0, len(bs), block)]
    return len(blocks) - len(set(blocks))  # how many repeats

best = max(((i, repeated_blocks_score(binascii.unhexlify(line.strip()))) for i, line in enumerate(lines, 1)),
           key=lambda x: x[1])
print("ECB likely on line:", best[0], "with repeat score:", best[1])
