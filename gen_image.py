"""Draw the front page of THE WORLD for Sunday 22 November 2026.

Output: image.png (1024x1024). Deterministic: same bytes on every run.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 22  # page margin

INK = (17, 17, 17)
SOFT = (62, 60, 56)
MUTED = (112, 108, 99)
PAPER = (250, 248, 241)
RULE = (24, 24, 24)
ACCENT = (138, 24, 24)
SEA = (188, 208, 228)
LAND = (247, 241, 224)
LAND_EDGE = (166, 152, 124)
GRID_LINE = (163, 186, 209)

LON0, LAT0 = 18.0, 28.0  # view centred on the eastern Mediterranean
CONTINENTS = [
    [(-10, 36), (-1, 43), (-9, 44), (-2, 50), (3, 53), (7, 58), (12, 57),
     (14, 55), (22, 56), (30, 61), (40, 60), (41, 50), (36, 46), (29, 41),
     (23, 38), (16, 38), (12, 45), (3, 43), (-10, 36)],
    [(-17, 15), (-16, 22), (-6, 36), (10, 38), (22, 32), (33, 31), (36, 22),
     (43, 12), (51, 12), (42, -2), (40, -15), (35, -25), (25, -34),
     (18, -34), (12, -18), (9, -1), (3, 6), (-8, 5), (-17, 15)],
    [(30, 45), (40, 60), (52, 70), (70, 74), (95, 76), (120, 71), (140, 60),
     (146, 45), (130, 35), (122, 30), (110, 20), (100, 9), (95, 20),
     (88, 22), (80, 14), (72, 20), (60, 26), (50, 31), (43, 37), (35, 42),
     (30, 45)],
    [(-11, 36), (-9, 43), (-2, 44), (2, 43), (3, 37), (-6, 36), (-11, 36)],
    [(10, 57), (22, 57), (26, 66), (20, 71), (10, 65), (10, 57)],
    [(44, 37), (50, 40), (54, 37), (50, 30), (44, 32), (44, 37)],
]

FONT_DIR = "/usr/share/fonts/truetype/noto/"
SERIF_BLACK = FONT_DIR + "NotoSerif-Black.ttf"
SERIF_XBOLD = FONT_DIR + "NotoSerif-ExtraBold.ttf"
SERIF_BOLD = FONT_DIR + "NotoSerif-Bold.ttf"
SERIF_COND_BOLD = FONT_DIR + "NotoSerif-CondensedBold.ttf"
SERIF_COND = FONT_DIR + "NotoSerif-Condensed.ttf"
SERIF_XCOND = FONT_DIR + "NotoSerif-ExtraCondensed.ttf"
SERIF = FONT_DIR + "NotoSerif-Regular.ttf"
SERIF_ITALIC = FONT_DIR + "NotoSerif-Italic.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, size, max_w, max_lines, floor=12):
    """Largest font size whose wrapped text fits in max_lines."""
    s = size
    while s > floor:
        f = font(path, s)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        s -= 1
    f = font(path, floor)
    return f, wrap(draw, text, f, max_w)[:max_lines]


def tracked(draw, xy, text, f, fill, tracking=1.6, anchor_left=True):
    """Draw letterspaced small-caps style label. Returns width used."""
    x, y = xy
    if not anchor_left:
        total = sum(text_w(draw, c, f) + tracking for c in text) - tracking
        x -= total / 2
    for c in text:
        draw.text((x, y), c, font=f, fill=fill)
        x += text_w(draw, c, f) + tracking
    return x - tracking


def rule(draw, y, x0, x1, weight=1, fill=RULE):
    draw.rectangle([x0, y, x1 - 1, y + weight - 1], fill=fill)


def para(draw, xy, lines, f, fill, line_h):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += line_h
    return y


def center_text(draw, y, text, f, fill, tracking=0.0):
    total = sum(text_w(draw, c, f) + tracking for c in text) - tracking
    x = (W - total) / 2
    for c in text:
        draw.text((x, y), c, font=f, fill=fill)
        x += text_w(draw, c, f) + tracking
    return total


def ink_centered(draw, y_ink, text, f, fill, track=0.0):
    """Centre text horizontally, putting the top of the ink at y_ink."""
    w = text_w(draw, text, f)
    total = w + track * (len(text) - 1)
    x = (W - total) / 2
    off = draw.textbbox((0, 0), text, font=f)[1]
    for c in text:
        draw.text((x, y_ink - off), c, font=f, fill=fill)
        x += text_w(draw, c, f) + track
    return draw.textbbox((0, 0), text, font=f)[3] - off


def masthead(draw):
    small = font(SERIF_COND, 11)
    draw.text((M, 19), "VOL. XII . NO. 4,182", font=small, fill=MUTED)
    r = "LATE EDITION"
    draw.text((W - M - text_w(draw, r, small), 19), r, font=small, fill=MUTED)

    title = "THE WORLD"
    track = 6
    size = 152
    f = font(SERIF_BLACK, size)
    avail = W - 2 * M - 24
    while text_w(draw, title, f) + track * (len(title) - 1) > avail:
        size -= 2
        f = font(SERIF_BLACK, size)
    cap_h = ink_centered(draw, 34, title, f, INK, track)

    y = 34 + cap_h + 11
    rule(draw, y, M, W - M, 3)
    rule(draw, y + 6, M, W - M, 1)

    date_f = font(SERIF_BOLD, 19)
    dy = y + 16
    dt = "SUNDAY 22 NOVEMBER 2026"
    dw = text_w(draw, dt, date_f) + 3.4 * (len(dt) - 1)
    ink_centered(draw, dy, dt, date_f, INK, 3.4)
    mid = dy + 4
    rule(draw, int(mid), M, int((W - dw) / 2) - 14, 1)
    rule(draw, int(mid), int((W + dw) / 2) + 14, W - M, 1)

    rule(draw, y + 46, M, W - M, 5)
    return y + 46


def _project(lon, lat, cx, cy, r):
    """Orthographic projection; returns (x, y) or None if on the far side."""
    import math
    lam = math.radians(lon - LON0)
    phi = math.radians(lat)
    phi0 = math.radians(LAT0)
    cos_c = math.sin(phi0) * math.sin(phi) + math.cos(phi0) * math.cos(phi) * math.cos(lam)
    if cos_c < 0:
        return None
    return (cx + r * math.cos(phi) * math.sin(lam),
            cy - r * (math.cos(phi0) * math.sin(phi)
                      - math.sin(phi0) * math.cos(phi) * math.cos(lam)))


def globe(box, marker=True):
    """Orthographic globe centred on the eastern Mediterranean, plus a pin."""
    x0, y0, x1, y1 = box
    size = min(x1 - x0, y1 - y0)
    cx = (x0 + x1) / 2 + 6
    cy = (y0 + y1) / 2
    r = size / 2 - 4

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(layer)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEA + (255,))

    for lon in range(-180, 180, 30):
        pts = [p for p in (_project(lon, lat, cx, cy, r)
                           for lat in range(-90, 91, 3)) if p]
        if len(pts) > 1:
            g.line(pts, fill=GRID_LINE + (255,), width=1)
    for lat in (-60, -30, 0, 30, 60):
        pts = [p for p in (_project(lon, lat, cx, cy, r)
                           for lon in range(-180, 181, 3)) if p]
        if len(pts) > 1:
            g.line(pts, fill=GRID_LINE + (255,), width=1)

    for poly in CONTINENTS:
        pts = [p for p in (_project(lon, lat, cx, cy, r) for lon, lat in poly) if p]
        if len(pts) > 2:
            g.polygon(pts, fill=LAND + (255,))
    for poly in CONTINENTS:
        pts = [p for p in (_project(lon, lat, cx, cy, r) for lon, lat in poly) if p]
        if len(pts) > 2:
            g.line(pts + [pts[0]], fill=LAND_EDGE + (255,), width=1)

    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.paste(layer, (0, 0), mask)
    g = ImageDraw.Draw(base)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(92, 116, 138, 255), width=2)

    if marker:
        px, py = _project(30.7, 36.9, cx, cy, r)  # Antalya
        g.line([px + 9, py - 9, px + 40, py - 40], fill=ACCENT + (255,), width=2)
        g.ellipse([px - 4, py - 4, px + 4, py + 4], fill=ACCENT + (255,))
        g.ellipse([px - 11, py - 11, px + 11, py + 11], outline=ACCENT + (255,), width=2)
    return base


LEAD_KICKER = "CLIMATE SUMMIT COLLAPSES"
LEAD_HL = "COP31 collapses without a deal as Europe holds firm"
LEAD_DECK = "Antalya talks close two days late and empty-handed after the EU bloc refuses to sign a final text that never names coal, oil or gas."

LEAD_TEXT_X = M + 4
LEAD_TEXT_W = 570

LEAD_TOP = 203
LEAD_BOTTOM = 523
GRID_TOP = 537
FOOTER_Y = 984


def lead(draw, img, top, bottom):
    f_kick = font(SERIF_BOLD, 16)
    tracked(draw, (LEAD_TEXT_X, top + 1), LEAD_KICKER, f_kick, ACCENT, tracking=1.8)

    hl_f, hl_lines = fit(draw, LEAD_HL, SERIF_BLACK, 56, LEAD_TEXT_W, 3, floor=24)
    y = top + 29
    y = para(draw, (LEAD_TEXT_X, y), hl_lines, hl_f, INK, int(hl_f.size * 1.13))

    rule(draw, y + 8, LEAD_TEXT_X, LEAD_TEXT_X + LEAD_TEXT_W, 1, (150, 146, 136))
    y += 16
    deck_f, deck_lines = fit(draw, LEAD_DECK, SERIF_ITALIC, 18, LEAD_TEXT_W, 4, floor=13)
    y = para(draw, (LEAD_TEXT_X, y), deck_lines, deck_f, SOFT, int(deck_f.size * 1.42))

    art = globe((650, top + 4, 992, top + 288))
    img.paste(art, (0, 0), art)
    cap_f = font(SERIF_ITALIC, 11)
    cap = "Antalya, Turkey: the summit venue where talks ran past deadline."
    para(draw, (650, top + 294), wrap(draw, cap, cap_f, 340), cap_f, MUTED, 15)
    return y


STORIES = [
    ("LIBYA", "Benghazi", "Sea drone hits Russian warship",
     "Suspected Ukrainian drone."),
    ("UKRAINE", "Dymer", "Russian drone hits Kyiv apartment block",
     "Teams search the rubble."),
    ("GULF", "Manama", "Iran projectile hits Bahrain industrial site",
     "Two wounded at Sitra."),
    ("INDONESIA", "Cikande", "Factory fire kills three in Banten",
     "Dozens still missing."),
    ("SPACE", "Mercury", "BepiColombo reaches orbit around Mercury",
     "Eight years to Mercury."),
    ("WEST BANK", "Ramallah", "Settlers burn cars across West Bank",
     "Arson in four villages."),
    ("NIGERIA", "Bayelsa", "Boat capsize kills 24 in Nigeria",
     "Mourners to a funeral."),
    ("MARKETS", "New York, Friday", "Wall Street slides into correction",
     "S&P -3.7%, Nasdaq -5.3%."),
    ("MEXICO", "Sinaloa, Friday", "Mexico captures El Chapo Isidro",
     "11 killed; boss arrested."),
]


def panel(draw, box, story):
    x0, y0, x1, y1 = box
    w = x1 - x0
    kick, place, head, sub = story

    f_kick = font(SERIF_BOLD, 12)
    x = tracked(draw, (x0, y0), kick, f_kick, ACCENT, tracking=1.4)
    f_place = font(SERIF_COND, 11)
    label = ". " + place
    if x + text_w(draw, label, f_place) < x1:
        draw.text((x + 5, y0 + 1), label, font=f_place, fill=MUTED)

    top = y0 + KICK_H

    # every headline is sized to occupy at most HEAD_LINES lines, so the
    # one-line standfirst lands on the same baseline across the grid
    head_f, head_lines = fit(draw, head, SERIF_COND_BOLD, HEAD_SIZE, w,
                             HEAD_LINES, floor=18)
    y = para(draw, (x0, top), head_lines, head_f, INK, int(head_f.size * 1.1))

    sub_f = font(SERIF_XCOND, SUB_SIZE)
    sub_line = wrap(draw, sub, sub_f, w)
    para(draw, (x0, y + SUB_GAP), sub_line[:1], sub_f, SOFT, SUB_LINE_H)
    return y + SUB_GAP + SUB_LINE_H


def panel_height(draw, w, story):
    kick, place, head, sub = story
    head_f, head_lines = fit(draw, head, SERIF_COND_BOLD, HEAD_SIZE, w,
                             HEAD_LINES, floor=18)
    return KICK_H + len(head_lines) * int(head_f.size * 1.1) + SUB_GAP + SUB_LINE_H


GUT, PAD, ROW_GAP = 30, 5, 30


def grid_boxes(draw, top):
    """Panel boxes, row heights fitted to content. Shared with layout_check."""
    col_w = (W - 2 * M - 2 * GUT) / 3
    body_w = col_w - 2 * PAD
    boxes = []
    y = top
    for r in range(3):
        row = STORIES[r * 3:r * 3 + 3]
        h = max(panel_height(draw, body_w, s) for s in row)
        for c in range(3):
            x0 = M + c * (col_w + GUT) + PAD
            boxes.append((x0, y, x0 + body_w, y + h))
        y += h + ROW_GAP
    return boxes, y - ROW_GAP


def grid(draw, top, bottom):
    boxes, end = grid_boxes(draw, top)
    col_w = (W - 2 * M - 2 * GUT) / 3

    for i, box in enumerate(boxes):
        panel(draw, box, STORIES[i])
        c, r = i % 3, i // 3
        x0, y0, x1, y1 = box
        if c < 2:
            draw.rectangle([x1 + PAD + GUT / 2 - 0.5, y0 + 2,
                            x1 + PAD + GUT / 2 + 0.5, y1 - 4], fill=(198, 193, 182))
    for r in (0, 1):
        y = boxes[r * 3][3] + ROW_GAP / 2
        rule(draw, int(y), M, W - M, 1, (198, 193, 182))
    return end


FOOTER = "COP31 . Benghazi . Dymer . Bahrain . Cikande . Mercury . West Bank . Nigeria . Markets . Mexico"

HEAD_SIZE = 28
HEAD_LINES = 2
KICK_H = 19
SUB_SIZE = 27.4  # ~8.03px em when the page is shown 300px wide
SUB_LINE_H = 40
SUB_GAP = 5


def footer(draw, y):
    rule(draw, y, M, W - M, 2)
    f = font(SERIF_COND, 10)
    total = sum(text_w(draw, c, f) + 1.2 for c in FOOTER) - 1.2
    x = (W - total) / 2
    for c in FOOTER:
        draw.text((x, y + 7), c, font=f, fill=MUTED)
        x += text_w(draw, c, f) + 1.2


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    top = masthead(draw)
    lead(draw, img, LEAD_TOP, LEAD_BOTTOM)
    rule(draw, LEAD_BOTTOM, M, W - M, 3)
    rule(draw, LEAD_BOTTOM + 5, M, W - M, 1)

    grid(draw, GRID_TOP, FOOTER_Y - 6)
    footer(draw, FOOTER_Y)
    return img


def main():
    img = build()
    img.save("image.png", format="PNG", optimize=True)
    print("wrote image.png", img.size)


if __name__ == "__main__":
    main()
