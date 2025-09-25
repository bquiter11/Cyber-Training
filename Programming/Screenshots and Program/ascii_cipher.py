

from typing import List

ALPHABET_SIZE = 256  # 0..255 covers all byte values

def normalize_key(key: int) -> int:

    """Reduce any integer to a number in 0..255."""

    return key % ALPHABET_SIZE

def encode_to_numbers(text: str, key: int) -> List[int]:

    """Turn each character into its ASCII number, shift by key, wrap around."""

    k = normalize_key(key)
    out = []
    for ch in text:
        original = ord(ch)        # 'A' -> 65, '!' -> 33, etc.
        shifted  = (original + k) % ALPHABET_SIZE
        out.append(shifted)
    return out

def decode_numbers(numbers: List[int], key: int) -> str:

    """Undo the shift and return the original text."""

    k = normalize_key(key)
    chars = []
    for n in numbers:
        original = (n - k) % ALPHABET_SIZE
        chars.append(chr(original))
    return ''.join(chars)

def save_numbers(path: str, numbers: List[int]) -> None:

    """Save numbers separated by single spaces (human-readable)."""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(' '.join(str(n) for n in numbers))

def load_numbers(path: str) -> List[int]:

    """Read numbers separated by spaces or commas from a file."""

    with open(path, 'r', encoding='utf-8') as f:
        data = f.read().replace(',', ' ')
    nums = []
    for piece in data.split():
        nums.append(int(piece))
    return nums

def prompt_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please type a whole number (like 5 or -12).")

def menu() -> None:
    print("="*60)
    print("ASCII Shifter — Encode/Decode")
    print("="*60)
    print("E) Encode text")
    print("D) Decode numbers from file")
    print("Q) Quit")
    print()

def main():
    while True:
        menu()
        choice = input("Pick one (E/D/Q): ").strip().lower()
        if choice == 'e':
            text = input("Type your message: ")
            key  = prompt_int("Type your numeric key (can be negative): ")
            nums = encode_to_numbers(text, key)
            save_numbers('encoded.txt', nums)
            print("\nEncoded numbers (also saved to encoded.txt):")
            print(' '.join(str(n) for n in nums))
            print("\nDone!")
        elif choice == 'd':
            key  = prompt_int("Type the numeric key you used to encode: ")
            try:
                nums = load_numbers('encoded.txt')
            except FileNotFoundError:
                print("I couldn't find 'encoded.txt'. Make sure you've encoded first,")
                print("or put your numbers into a file named encoded.txt in this folder.")
                continue
            text = decode_numbers(nums, key)
            with open('decoded.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            print("\nDecoded text (also saved to decoded.txt):")
            print(text)
            print("\nDone!")
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Please type E, D, or Q.")

if __name__ == '__main__':
    main()
