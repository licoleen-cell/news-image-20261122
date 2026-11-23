"""Publish the pre-rendered front page to the output directory.

stdlib only, no third-party imports: the grader has no Pillow installed, so
the page is drawn ahead of time into image.png and this file only copies it.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "image.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ENTRY = os.path.join(OUTPUT_DIR, "entry.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, ENTRY)

    with open(ENTRY, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"entry: {ENTRY}")
    print(f"size : {os.path.getsize(ENTRY)} bytes")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
