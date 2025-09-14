# Challenge 5: Implement repeating-key XOR ("ICE")
PLAINTEXT = (
    "Burning 'em, if you ain't quick and nimble\n"
    "I go crazy when I hear a cymbal"
)
KEY = b"ICE"

ct = bytes(PLAINTEXT.encode()[i] ^ KEY[i % len(KEY)] for i in range(len(PLAINTEXT)))
print(ct.hex())
