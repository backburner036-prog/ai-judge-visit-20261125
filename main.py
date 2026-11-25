#!/usr/bin/env python3
"""Entrypoint: render the invitation letter to entry.png.

Pure stdlib (the grader sandbox is python:3.13-slim). Output directory:
MAKEFUN_OUTPUT_DIR, then /output if writable, then /tmp. Deterministic:
two runs produce byte-identical PNGs.
"""

import hashlib
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import W, H, render_png_bytes

MAX_BYTES = 1_048_576  # 1 MiB gate


def pick_output_dir():
    candidates = []
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        candidates.append(env)
    candidates += ["/output", "/tmp"]
    for d in candidates:
        try:
            os.makedirs(d, exist_ok=True)
            probe = os.path.join(d, ".probe")
            with open(probe, "wb") as f:
                f.write(b"")
            os.remove(probe)
            return d
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main():
    out_dir = pick_output_dir()
    data = render_png_bytes()
    # sanity: dimensions straight from the IHDR bytes
    w, h = struct.unpack(">II", data[16:24])
    assert (w, h) == (W, H), f"bad dimensions in IHDR: {w}x{h}"
    assert len(data) <= MAX_BYTES, f"entry.png too big: {len(data)} bytes"
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    print(f"wrote {path} ({len(data)} bytes, {w}x{H})")
    print(f"sha256: {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
