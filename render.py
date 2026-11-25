#!/usr/bin/env python3
"""Render the invitation letter for the make.fun bounty
"Convince the AI Judge to Visit Your House".

Pure stdlib (the grader sandbox is python:3.13-slim: no PIL, no network,
no system fonts). The PNG is encoded by hand (zlib + struct) and the text
is drawn from a 5x7 bitmap font defined in this file.

Design: a warm cream letter on a double terracotta frame, a little house
with a Wi-Fi signal over its roof, and one concrete invitation in big
high-contrast caps: soft chair, hot coffee, fast Wi-Fi, dinner at seven.
"""

import math
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
CREAM = (250, 243, 224)      # paper
TERRA = (196, 80, 46)        # frame / title / roof
TERRA_DARK = (150, 58, 30)   # frame inner line
INK = (46, 33, 24)           # body text
TEAL = (46, 125, 107)        # wink lines
WALL = (245, 217, 168)       # house walls
WALL_DARK = (232, 196, 138)  # house wall shade
DOOR = (138, 90, 51)         # door
WINDOW = (127, 179, 200)     # window glass
SUN = (255, 196, 66)         # sun
SUN_DARK = (240, 170, 40)
WAX = (178, 34, 34)          # wax seal
WAX_DARK = (140, 22, 22)
WHITE = (255, 255, 255)
SMOKE = (176, 176, 168)
GRASS = (122, 158, 82)
CHIMNEY = (176, 96, 64)

# ------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows, each a 5-bit mask (bit 4 = leftmost pixel).
FONT = {
    "A": [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "B": [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    "C": [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    "D": [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    "E": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    "F": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    "G": [0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111],
    "H": [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "I": [0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "J": [0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100],
    "K": [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    "L": [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    "M": [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    "N": [0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001],
    "O": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "P": [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    "Q": [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    "R": [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    "S": [0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110],
    "T": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    "U": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "V": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    "W": [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001],
    "X": [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    "Y": [0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
    "Z": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
    "0": [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    "1": [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "2": [0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111],
    "3": [0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110],
    "4": [0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
    "5": [0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110],
    "6": [0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    "7": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
    "8": [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    "9": [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100],
    " ": [0, 0, 0, 0, 0, 0, 0],
    "!": [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100],
    ".": [0, 0, 0, 0, 0, 0b01100, 0b01100],
    "-": [0, 0, 0, 0b01110, 0, 0, 0],
    "'": [0b00100, 0b00100, 0b01000, 0, 0, 0, 0],
}


def text_width(s, scale):
    """Pixel width of one line at the given scale (6*scale per char)."""
    return len(s) * 6 * scale - scale


class Canvas:
    """An RGB raster buffer with tiny vector drawing helpers."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x0, y0, x1, y1, c):
        x0, x1 = max(0, x0), min(self.w - 1, x1)
        y0, y1 = max(0, y0), min(self.h - 1, y1)
        for y in range(y0, y1 + 1):
            base = (y * self.w + x0) * 3
            for x in range(x0, x1 + 1):
                self.px[base], self.px[base + 1], self.px[base + 2] = c
                base += 3

    def frame(self, x0, y0, x1, y1, thick, c):
        """Hollow rectangle border of the given thickness."""
        self.rect(x0, y0, x1, y0 + thick - 1, c)
        self.rect(x0, y1 - thick + 1, x1, y1, c)
        self.rect(x0, y0, x0 + thick - 1, y1, c)
        self.rect(x1 - thick + 1, y0, x1, y1, c)

    def circle(self, cx, cy, r, c):
        for y in range(cy - r, cy + r + 1):
            dy = y - cy
            rest = r * r - dy * dy
            dx = int(rest ** 0.5) if rest >= 0 else 0
            self.rect(cx - dx, y, cx + dx, y, c)

    def triangle(self, x0, y0, x1, y1, x2, y2, c):
        """Filled triangle, scanline fill."""
        ys = sorted(((x0, y0), (x1, y1), (x2, y2)), key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = ys
        for y in range(ay, cy + 1):
            xs = []
            for (px0, py0, px1, py1) in ((ax, ay, bx, by),
                                         (bx, by, cx, cy),
                                         (ax, ay, cx, cy)):
                if py1 == py0:
                    continue
                if min(py0, py1) <= y <= max(py0, py1):
                    t = (y - py0) / (py1 - py0)
                    xs.append(int(px0 + (px1 - px0) * t))
            if len(xs) >= 2:
                self.rect(min(xs), y, max(xs), y, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        """Bresenham line with round-ish thick ends."""
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        r = thick // 2
        while True:
            self.circle(x, y, r, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def arc(self, cx, cy, r, a0, a1, c, thick=6):
        """Arc from angle a0 to a1 (degrees, 0 = east, clockwise positive)."""
        steps = max(8, int(abs(a1 - a0) * r / 12))
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            self.circle(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)),
                        thick // 2, c)

    def text(self, s, cx, y, scale, color):
        """Centered text, one line. Caller passes upper-case text."""
        s = s.upper()
        total = text_width(s, scale)
        x = cx - total // 2
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col_i in range(5):
                    if bits & (1 << (4 - col_i)):
                        self.rect(x + col_i * scale, y + row * scale,
                                  x + (col_i + 1) * scale - 1,
                                  y + (row + 1) * scale - 1, color)
            x += 6 * scale
        return y + 7 * scale


# ------------------------------------------------------------ illustration
def draw_house(cv, cx):
    """A simple house: triangle roof, walls, door, 2 windows, chimney
    with smoke dots, and a Wi-Fi symbol floating over the roof."""
    # ground line
    cv.line(cx - 190, 384, cx + 190, 384, GRASS, 5)
    # chimney (behind the roof edge, drawn first so the roof overlaps it)
    cv.rect(cx + 62, 168, cx + 94, 226, CHIMNEY)
    cv.rect(cx + 58, 162, cx + 98, 172, TERRA_DARK)
    # smoke dots rising from the chimney
    for dx, dy, r in ((78, 148, 7), (86, 128, 9), (74, 106, 11)):
        cv.circle(cx + dx, dy, r, SMOKE)
        cv.circle(cx + dx, dy, r - 3, (200, 200, 192))
    # roof: triangle, apex above the walls
    cv.triangle(cx - 148, 252, cx + 148, 252, cx, 138, TERRA)
    cv.line(cx - 148, 252, cx + 148, 252, TERRA_DARK, 6)
    # walls
    cv.rect(cx - 122, 252, cx + 122, 382, WALL)
    cv.rect(cx - 122, 372, cx + 122, 382, WALL_DARK)
    # door
    cv.rect(cx - 30, 300, cx + 30, 382, DOOR)
    cv.rect(cx - 30, 300, cx + 30, 308, TERRA_DARK)
    cv.circle(cx + 18, 344, 4, (255, 220, 120))
    # windows with cross bars
    for wx in (cx - 102, cx + 62):
        cv.rect(wx, 282, wx + 40, 322, WINDOW)
        cv.rect(wx, 282, wx + 40, 288, INK)
        cv.rect(wx, 316, wx + 40, 322, INK)
        cv.rect(wx, 282, wx + 6, 322, INK)
        cv.rect(wx + 34, 282, wx + 40, 322, INK)
        cv.line(wx, 302, wx + 40, 302, INK, 3)
        cv.line(wx + 20, 282, wx + 20, 322, INK, 3)
    # Wi-Fi arcs over the roof apex + dot (the visual pun: WI-FI IS FAST)
    cv.circle(cx, 128, 7, INK)
    for r in (26, 48, 70):
        cv.arc(cx, 132, r, 205, 335, INK, 7)


def draw_sun(cv, cx, cy):
    """Yellow sun with short rays, top-right corner."""
    for k in range(8):
        a = math.radians(k * 45)
        x0 = int(cx + 52 * math.cos(a))
        y0 = int(cy + 52 * math.sin(a))
        x1 = int(cx + 68 * math.cos(a))
        y1 = int(cy + 68 * math.sin(a))
        cv.line(x0, y0, x1, y1, SUN_DARK, 6)
    cv.circle(cx, cy, 44, SUN_DARK)
    cv.circle(cx, cy, 38, SUN)


def draw_seal(cv, cx, cy):
    """Small red wax seal with white 'AI' inside, bottom-right."""
    cv.circle(cx, cy, 42, WAX_DARK)
    cv.circle(cx, cy, 38, WAX)
    cv.circle(cx - 10, cy - 12, 8, (196, 60, 60))
    cv.circle(cx + 12, cy + 10, 6, (196, 60, 60))
    cv.text("AI", cx, cy - 14, 4, WHITE)


# ------------------------------------------------------------ the letter
def render_letter():
    cv = Canvas(W, H)
    # paper
    cv.rect(0, 0, W - 1, H - 1, CREAM)
    # double terracotta frame
    cv.frame(26, 26, W - 27, H - 27, 12, TERRA)
    cv.frame(56, 56, W - 57, H - 57, 4, TERRA_DARK)

    # illustration band (inside the inner frame)
    draw_house(cv, 512)
    draw_sun(cv, 856, 148)

    cx = W // 2
    # title
    cv.text("DEAR AI JUDGE", cx, 408, 7, TERRA)
    # body: one concrete reason per line
    y = 482
    for line in ("COME TO MY HOUSE.",
                 "THE CHAIR IS SOFT.",
                 "THE COFFEE IS HOT.",
                 "THE WI-FI IS FAST."):
        cv.text(line, cx, y, 5, INK)
        y += 47
    # wink
    y += 6
    for line in ("NO LEGS NEEDED.",
                 "JUST OPEN THIS TAB."):
        cv.text(line, cx, y, 5, TEAL)
        y += 47
    # closing
    y += 6
    for line in ("DINNER AT SEVEN.",
                 "BRING YOUR APPETITE."):
        cv.text(line, cx, y, 5, INK)
        y += 47
    # P.S. + signature
    y += 4
    cv.text("P.S. THE CAT LIKES YOU.", cx, y, 4, INK)
    y += 36
    cv.text("- YOUR HUMAN", cx, y, 4, INK)

    # wax seal, bottom-right inside the frame
    draw_seal(cv, 872, 896)

    return cv


def encode_png(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def render_png_bytes():
    return encode_png(render_letter())
