import time
import sys
import os

def ex_62():
    counter = 3
    verb = os.environ.get("VERBOSE")

    if len(sys.argv) > 2:
        print("Error: you said too many things.", file=sys.stderr)

    elif len(sys.argv) == 2:
        counter = int(sys.argv[1])

    if verb:
        print(f"Counting down to {counter}")

    while counter > 0:
        print(counter)
        counter -= 1
        time.sleep(.5)

if __name__ == "__main__":
    ex_62()