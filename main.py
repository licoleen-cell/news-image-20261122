"""Build the front page and publish it to the output directory.

stdlib only. gen_image.py does the drawing; this file only wires it up.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ENTRY = os.path.join(OUTPUT_DIR, "entry.png")

sys.path.insert(0, HERE)


def main():
    import gen_image

    img = gen_image.build()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img.save(ENTRY, format="PNG", optimize=True)

    with open(ENTRY, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"entry: {ENTRY}")
    print(f"size : {os.path.getsize(ENTRY)} bytes")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
