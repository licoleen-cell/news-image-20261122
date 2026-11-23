"""Draw the front page of THE WORLD for Sunday 22 November 2026.

Output: image.png (1024x1024). Deterministic: same bytes on every run.
"""

from PIL import Image, ImageDraw, ImageFont

import math

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
    ("LIBYA", "Benghazi", "Suspected drone hits Russian warship",
     "At Benghazi naval base; 10 lightly wounded, officials say."),
    ("UKRAINE", "Dymer", "Drone hits Dymer, near Kyiv",
     "At least 3 killed."),
    ("GULF", "Manama", "Bahrain says Iran struck plant",
     "IRGC claims the strike."),
    ("INDONESIA", "Cikande", "Factory fire kills three in Banten",
     "Blaze at a candy plant in Cikande leaves dozens missing."),
    ("SPACE", "Mercury", "BepiColombo reaches orbit around Mercury",
     "European-Japanese probe arrives after an eight-year voyage."),
    ("WEST BANK", "Ramallah", "Settlers burn cars across West Bank",
     "Israel opens a probe into arson in four villages."),
    ("NIGERIA", "Bayelsa", "Boat capsize kills 24 in Nigeria",
     "At least 24 died; the vessel carried mourners to a funeral."),
    ("MARKETS", "New York, Friday", "Wall Street slides into correction",
     "S&P 500 falls 3.7% to 6,910; Nasdaq drops 5.3% on Friday."),
    ("MEXICO", "Sinaloa, Friday", "Mexico captures El Chapo Isidro",
     "11 killed as special forces arrest the Los Mazatlecos boss."),
]


def panel(draw, box, story):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    kick, place, head, sub = story

    f_kick = font(SERIF_BOLD, 12)
    x = tracked(draw, (x0, y0), kick, f_kick, ACCENT, tracking=1.4)
    f_place = font(SERIF_COND, 11)
    label = ". " + place
    if x + text_w(draw, label, f_place) < x1:
        draw.text((x + 5, y0 + 1), label, font=f_place, fill=MUTED)

    top = y0 + KICK_H
    budget = h - KICK_H - 4

    # one headline size across the grid; only the standfirst may shrink
    head_f = font(SERIF_BOLD, HEAD_SIZE)
    head_lines = wrap(draw, head, head_f, w)
    head_h = len(head_lines) * int(HEAD_SIZE * 1.1)
    sub_f = font(SERIF, 12)
    sub_lines = wrap(draw, sub, sub_f, w)
    sub_h = len(sub_lines) * int(12 * 1.34)
    if head_h + 5 + sub_h > budget:
        sub_f = font(SERIF, 11)
        sub_lines = wrap(draw, sub, sub_f, w)
        sub_h = len(sub_lines) * int(11 * 1.34)

    y = para(draw, (x0, top), head_lines, head_f, INK, int(head_f.size * 1.1))
    para(draw, (x0, y + 5), sub_lines, sub_f, SOFT, int(sub_f.size * 1.34))
    return top + head_h + 5 + sub_h


def panel_height(draw, w, story):
    kick, place, head, sub = story
    head_f = font(SERIF_BOLD, HEAD_SIZE)
    head_lines = wrap(draw, head, head_f, w)
    for sub_size in (12, 11):
        sub_f = font(SERIF, sub_size)
        sub_lines = wrap(draw, sub, sub_f, w)
        if len(head_lines) * int(HEAD_SIZE * 1.1) + 5 \
                + len(sub_lines) * int(sub_size * 1.34) <= MAX_BODY:
            sub_h = len(sub_lines) * int(sub_size * 1.34)
            break
    return KICK_H + len(head_lines) * int(HEAD_SIZE * 1.1) + 5 + sub_h


GUT, PAD, ROW_GAP = 30, 5, 14


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
KICK_H = 19
MAX_BODY = 3 * int(HEAD_SIZE * 1.1) + 5 + 2 * int(12 * 1.34)


def footer(draw, y):
    rule(draw, y, M, W - M, 2)
    f = font(SERIF_COND, 10)
    total = sum(text_w(draw, c, f) + 1.2 for c in FOOTER) - 1.2
    x = (W - total) / 2
    for c in FOOTER:
        draw.text((x, y + 7), c, font=f, fill=MUTED)
        x += text_w(draw, c, f) + 1.2


FLAME = (211, 84, 22)
SMOKE = (156, 152, 144)
CITY = (72, 68, 62)


def draw_fire_smoke(draw, x, y, w, h, fire_color, smoke_h, building=True):
    """Flat scene of flames and a smoke column, drawn inside (x, y, w, h).

    fire_color paints the flames; smoke_h is the height of the smoke column in
    pixels, measured up from the top of the flames; building adds a simple city
    block behind the fire.
    """
    base = y + h - 1
    fire_h = min(h * 0.42, w * 0.52)
    r_top = w * 0.13
    smoke_h = max(0.0, min(smoke_h, h - fire_h - r_top - 1))

    if building:
        bx = x
        for bh, bw in ((0.40, 0.28), (0.58, 0.32), (0.44, 0.26)):
            draw.rectangle([bx, base - h * bh, bx + w * bw, base], fill=CITY)
            bx += w * (bw + 0.06)

    fw = w * 0.15
    fx = x + w * 0.5
    draw.polygon([(fx - fw * 1.9, base), (fx - fw * 0.8, base - fire_h * 0.66),
                  (fx - fw * 0.1, base)], fill=fire_color)
    draw.polygon([(fx - fw * 0.8, base), (fx, base - fire_h),
                  (fx + fw * 0.8, base)], fill=fire_color)
    draw.polygon([(fx + fw * 0.1, base), (fx + fw * 0.95, base - fire_h * 0.70),
                  (fx + fw * 1.9, base)], fill=fire_color)

    if smoke_h <= 0:
        return
    n = max(3, int(smoke_h / max(1.0, w * 0.20)))
    for i in range(n):
        t = (i + 1) / n
        r = w * (0.075 + 0.055 * t)
        cy = min(y + r + 1, base - fire_h - t * smoke_h)
        ox = t * w * 0.10
        draw.ellipse([fx - r + ox, cy - r, fx + r + ox, cy + r], fill=SMOKE)


SHIP = (58, 60, 66)
DECK = (128, 124, 116)


def draw_ship(draw, x, y, w, h, sea_color, fire=False, smoke=False,
              ship_type="warship"):
    """Flat sea and vessel scene, drawn inside (x, y, w, h).

    The lower two-fifths are sea in sea_color; the vessel sits on the waterline
    as a "warship" (low, pointed bow, gun turret) or a "cargo" ship (tall
    container stacks). fire and smoke add flames and a smoke plume amidships.
    """
    base = y + h - 1
    water_y = int(y + h * 0.60)

    def rect(x0, y0, x1, y1, fill):
        draw.rectangle([min(x0, x1 - 1), min(y0, y1 - 1),
                        max(x0, x1 - 1), max(y0, y1 - 1)], fill=fill)

    rect(x, water_y, x + w, base + 1, sea_color)

    hull_h = max(1, min(int(h * 0.13), int(h * 0.33)))
    hull_y = water_y - hull_h
    hl, hr = x + w * 0.10, x + w * 0.90
    if ship_type == "cargo":
        hull = [(hl, hull_y), (hr, hull_y), (hr - w * 0.02, water_y),
                (hl + w * 0.03, water_y)]
    else:
        hull = [(hl, hull_y), (hr - w * 0.12, hull_y), (hr, water_y - 1),
                (hl + w * 0.03, water_y)]
    draw.polygon(hull, fill=SHIP)

    if ship_type == "cargo":
        cw, ch = w * 0.16, h * 0.16
        cx = hl + w * 0.08
        for _ in range(3):
            rect(cx, hull_y - ch, cx + cw, hull_y, DECK)
            rect(cx + cw * 0.10, hull_y - ch * 0.55, cx + cw * 0.90, hull_y, SHIP)
            cx += cw * 1.18
        funnel_x, funnel_top = hl + w * 0.72, hull_y - h * 0.26
        rect(funnel_x, funnel_top, funnel_x + w * 0.07, hull_y, SHIP)
    else:
        deck_y = hull_y - h * 0.07
        rect(hl + w * 0.22, deck_y, hl + w * 0.62, hull_y, DECK)
        rect(hl + w * 0.44, deck_y - h * 0.09, hl + w * 0.54, deck_y, SHIP)
        rect(hl + w * 0.60, deck_y - h * 0.10, hl + w * 0.68, deck_y, SHIP)
        funnel_x, funnel_top = hl + w * 0.34, deck_y - h * 0.16
        rect(funnel_x, funnel_top, funnel_x + w * 0.06, deck_y, SHIP)

    fire_cx = x + w * 0.5
    fh = min(h * 0.20, hull_y - y)
    if fire:
        draw.polygon([(fire_cx - w * 0.07, hull_y), (fire_cx, hull_y - fh),
                      (fire_cx + w * 0.07, hull_y)], fill=FLAME)
        draw.polygon([(fire_cx - w * 0.13, hull_y), (fire_cx - w * 0.06,
                      hull_y - fh * 0.55), (fire_cx + w * 0.01, hull_y)],
                     fill=FLAME)
    if smoke:
        for i in range(4):
            r = min(w * (0.05 + 0.02 * i), max(1.0, (hull_y - y) / 2 - 1))
            cy = max(y + r + 1, hull_y - h * 0.24 - i * h * 0.11)
            cx = fire_cx + w * 0.04 * i
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)


def _mix(color, target, t):
    return tuple(int(round(color[i] + (target[i] - color[i]) * t))
                 for i in range(3))


def draw_building_symbol(draw, x, y, w, h, building_shape="parliament",
                         symbol="ballot", color=SOFT):
    """Flat institution scene with an emblem, drawn inside (x, y, w, h).

    Every shape is a flat roof slab carried on a row of pillars - never a
    pitched roof - and the whole facade keeps a margin so nothing is clipped at
    the edge of the box. building_shape is "parliament" (wide, six pillars),
    "court" (narrow, four pillars) or "office" (glass slab, window grid). symbol
    is "ballot" (box), "gavel" (hammer and block) or "thermometer", drawn on a
    pale seal in the middle of the facade. color paints the building.
    """
    m = max(3.0, min(w, h) * 0.08)
    ix0, iy0 = x + m, y + m
    ix1, iy1 = x + w - 1 - m, y + h - 1 - m
    iw, ih = max(1.0, ix1 - ix0), max(1.0, iy1 - iy0)
    light = _mix(color, PAPER, 0.70)
    shade = _mix(color, INK, 0.35)

    roof_h = max(2.0, ih * 0.10)
    plinth_h = max(2.0, ih * 0.09)

    if building_shape == "office":
        bx0, bx1 = ix0 + iw * 0.14, ix1 - iw * 0.14
        body_top = iy0 + ih * 0.16
        draw.rectangle([bx0, body_top, bx1, iy1 - plinth_h], fill=color)
        draw.rectangle([bx0 - iw * 0.04, body_top - roof_h,
                        bx1 + iw * 0.04, body_top], fill=shade)
        draw.rectangle([bx0 - iw * 0.02, iy1 - plinth_h, bx1 + iw * 0.02, iy1],
                       fill=shade)
        cols, rows = 4, 3
        pad_x, pad_y = (bx1 - bx0) * 0.10, ih * 0.05
        cell_w = (bx1 - bx0 - 2 * pad_x) / cols
        cell_h = (iy1 - plinth_h - body_top - 2 * pad_y) / rows
        for r in range(rows):
            for c in range(cols):
                wx = bx0 + pad_x + c * cell_w + cell_w * 0.18
                wy = body_top + pad_y + r * cell_h + cell_h * 0.20
                draw.rectangle([wx, wy, wx + cell_w * 0.64,
                                wy + cell_h * 0.60], fill=light)
    else:
        wide = building_shape == "parliament"
        inset = iw * (0.05 if wide else 0.16)
        bx0, bx1 = ix0 + inset, ix1 - inset
        body_top = iy0 + ih * (0.30 if wide else 0.36)
        n = 6 if wide else 4
        draw.rectangle([bx0 - iw * 0.03, body_top - roof_h,
                        bx1 + iw * 0.03, body_top], fill=shade)
        gap = (bx1 - bx0) / n
        pw = gap * 0.52
        for i in range(n):
            px0 = bx0 + i * gap + (gap - pw) / 2
            draw.rectangle([px0, body_top, px0 + pw, iy1 - plinth_h],
                           fill=color)
        draw.rectangle([bx0, body_top, bx1, body_top + ih * 0.07], fill=light)
        draw.rectangle([bx0 - iw * 0.02, iy1 - plinth_h, bx1 + iw * 0.02, iy1],
                       fill=shade)

    cx = (ix0 + ix1) / 2.0
    cy = (iy0 + iy1) / 2.0 + ih * 0.08
    r = min(iw * 0.30, ih * 0.34)
    s = r * 1.25
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER,
                 outline=shade, width=max(1, int(r * 0.10)))

    if symbol == "ballot":
        x0, x1 = cx - s * 0.45, cx + s * 0.45
        yb = cy + s * 0.42
        yt = yb - s * 0.50
        draw.rectangle([x0, yt, x1, yb], fill=shade)
        draw.rectangle([cx - s * 0.20, yt + s * 0.10, cx + s * 0.20,
                        yt + s * 0.14], fill=PAPER)
        draw.rectangle([cx - s * 0.16, yt - s * 0.34, cx + s * 0.16,
                        yt + s * 0.06], fill=PAPER, outline=shade,
                       width=max(1, int(s * 0.04)))
    elif symbol == "gavel":
        draw.rectangle([cx - s * 0.45, cy - s * 0.42, cx + s * 0.10,
                        cy - s * 0.12], fill=shade)
        draw.polygon([(cx - s * 0.20, cy - s * 0.12),
                      (cx - s * 0.08, cy - s * 0.12),
                      (cx + s * 0.26, cy + s * 0.44),
                      (cx + s * 0.14, cy + s * 0.44)], fill=shade)
        draw.rectangle([cx - s * 0.02, cy + s * 0.42, cx + s * 0.46,
                        cy + s * 0.52], fill=shade)
    else:
        draw.rectangle([cx - s * 0.12, cy - s * 0.50, cx + s * 0.12,
                        cy + s * 0.14], fill=PAPER, outline=shade,
                       width=max(1, int(s * 0.05)))
        draw.rectangle([cx - s * 0.06, cy - s * 0.14, cx + s * 0.06,
                        cy + s * 0.16], fill=ACCENT)
        draw.ellipse([cx - s * 0.18, cy + s * 0.06, cx + s * 0.18,
                      cy + s * 0.42], fill=ACCENT, outline=shade,
                     width=max(1, int(s * 0.05)))


GRASS = (86, 122, 78)
TRACK = (150, 146, 138)


def draw_sport_vehicle(draw, x, y, w, h, kind="football", team_color=ACCENT,
                       score="4-0"):
    """Flat sport or transport scene with a scoreline, inside (x, y, w, h).

    kind "football" draws a green pitch with centre circle and a ball; "racing"
    draws a grey track with lane lines and a car. team_color paints the ball
    panel accent and the car body; score is printed large in team_color at the
    top of the scene.
    """
    base = y + h - 1
    if kind == "racing":
        gray = TRACK
        draw.rectangle([x, y, x + w - 1, base], fill=gray)
        lane = _mix(gray, INK, 0.45)
        inset = max(1, h * 0.06)
        draw.rectangle([x + inset, y + inset, x + w - 1 - inset,
                        base - inset], outline=PAPER,
                       width=max(1, int(h * 0.03)))
        for i in range(3):
            ty = y + h * (0.30 + i * 0.20)
            draw.line([(x + inset, ty), (x + w - 1 - inset, ty)],
                      fill=lane, width=max(1, int(h * 0.02)))
        body_y0, body_y1 = y + h * 0.40, y + h * 0.62
        bx0, bx1 = x + w * 0.18, x + w * 0.72
        draw.rectangle([bx0, body_y0, bx1, body_y1], fill=team_color)
        draw.polygon([(bx0 + w * 0.20, body_y0), (bx0 + w * 0.34, y + h * 0.26),
                      (bx1 - w * 0.16, y + h * 0.26), (bx1 - w * 0.04, body_y0)],
                     fill=_mix(team_color, PAPER, 0.55))
        for wx in (bx0 + w * 0.06, bx1 - w * 0.14):
            r = h * 0.10
            draw.ellipse([wx, body_y1 - r * 0.4, wx + r * 2, body_y1 + r * 1.6],
                         fill=INK)
    else:
        draw.rectangle([x, y, x + w - 1, base], fill=GRASS)
        grass_light = _mix(GRASS, PAPER, 0.16)
        for i in range(4):
            if i % 2 == 0:
                bx0 = x + i * w * 0.25
                draw.rectangle([bx0, y, bx0 + w * 0.25 - 1, base],
                               fill=grass_light)
        inset = max(1, min(w, h) * 0.06)
        draw.rectangle([x + inset, y + inset, x + w - 1 - inset,
                        base - inset], outline=PAPER,
                       width=max(1, int(h * 0.022)))
        draw.line([(x + w * 0.5, y + inset), (x + w * 0.5, base - inset)],
                  fill=PAPER, width=max(1, int(h * 0.022)))
        cr = h * 0.14
        cx, cy = x + w * 0.5, y + h * 0.50
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=PAPER,
                     width=max(1, int(h * 0.022)))

        # white ball with a single black pentagon, kept clear of the edges
        margin = max(2.0, min(w, h) * 0.10) + max(1, int(h * 0.022))
        br = min(w, h) * 0.15
        br = min(br, (w - 2 * margin) / 2, (h - 2 * margin) / 2)
        bx = min(max(x + w * 0.68, x + margin + br), x + w - margin - br)
        by = min(max(base - h * 0.22, y + margin + br), base - margin - br)
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255),
                     outline=INK, width=max(1, int(br * 0.10)))
        pr = br * 0.46
        panel = [(bx + pr * math.cos(math.radians(-90 + 72 * i)),
                  by + pr * math.sin(math.radians(-90 + 72 * i)))
                 for i in range(5)]
        draw.polygon(panel, fill=INK)

    if score:
        f = font(SERIF_BLACK, max(1, int(h * 0.20)))
        tw = text_w(draw, score, f)
        draw.text((x + (w - tw) / 2.0, y + h * 0.055), score, font=f,
                  fill=team_color)


# ---------------------------------------------------------------- variant D
# Frame only: 18 real stories, no open slots.

D_NUMBERS = [
    ("12", "AT LEAST 12 CARS BURNED"),
    ("720/9", "INDIA DECLARE 720/9"),
    ("4-0", "LIVERPOOL BEAT MAN UTD 4-0"),
    ("51-30", "DALLAS BEAT TENNESSEE 51-30"),
    ("50", "WEMBANYAMA SCORES 50"),
]


def d_masthead(draw):
    f_small = font(SERIF_COND, 10)
    draw.text((M, 14), "VOL. XII . NO. 4,182", font=f_small, fill=MUTED)
    right = "LATE EDITION"
    draw.text((W - M - text_w(draw, right, f_small), 14), right,
              font=f_small, fill=MUTED)

    title = "THE WORLD"
    track = 5
    size = 106
    f = font(SERIF_BLACK, size)
    avail = W - 2 * M - 12
    while text_w(draw, title, f) + track * (len(title) - 1) > avail:
        size -= 2
        f = font(SERIF_BLACK, size)
    cap_h = ink_centered(draw, 28, title, f, INK, track)

    y = 28 + cap_h + 8
    rule(draw, y, M, W - M, 3)
    rule(draw, y + 6, M, W - M, 1)

    date_f = font(SERIF_BOLD, 21)
    dt = "SUNDAY 22 NOVEMBER 2026"
    dy = y + 14
    dw = text_w(draw, dt, date_f) + 3.2 * (len(dt) - 1)
    ink_centered(draw, dy, dt, date_f, INK, 3.2)
    mid = dy + 4
    rule(draw, int(mid), M, int((W - dw) / 2) - 12, 1)
    rule(draw, int(mid), int((W + dw) / 2) + 12, W - M, 1)

    y2 = y + 44
    rule(draw, y2, M, W - M, 5)
    return y2 + 5


def d_numbers(draw, y):
    """Five figures from clean facts; each label repeats its headline's words.

    The label sits below the digit's ink box with a 5px gap, so it can never
    cover the numeral, and it wraps inside its own column.
    """
    col = (W - 2 * M) / len(D_NUMBERS)
    lf = font(SERIF_BOLD, 11)
    for i, (num, label) in enumerate(D_NUMBERS):
        cx = M + col * (i + 0.5)
        size = 44
        f = font(SERIF_BLACK, size)
        while text_w(draw, num, f) > col - 12 and size > 26:
            size -= 1
            f = font(SERIF_BLACK, size)
        bb = draw.textbbox((0, 0), num, font=f)
        draw.text((cx - text_w(draw, num, f) / 2, y - bb[1]), num, font=f,
                  fill=INK)
        ly = y + (bb[3] - bb[1]) + 5
        for ln in wrap(draw, label, lf, col - 8)[:2]:
            draw.text((cx - text_w(draw, ln, lf) / 2, ly), ln, font=lf,
                      fill=ACCENT)
            ly += 14
        if i:
            x = M + col * i - 0.5
            draw.rectangle([x, y + 4, x + 1, y + 52], fill=(206, 201, 190))
    return y + 62


# Only hours that the sources state: nothing is placed by guesswork.
D_PINS = [
    (1.0, "01:00 Wembanyama tipoff"),
    (3.5, "03:30 Strathmore, California"),
    (5.83, "05:50 Verstappen finish"),
    (10.0, "10:00 Hong Kong polls shut"),
    (13.0, "13:00 Barcelona kick-off"),
    (16.5, "16:30 Liverpool kick-off"),
    (18.0, "18:00 NFL kick-offs"),
]


def d_timeline(draw, y):
    """24-hour UTC rail: one marker per source-stated hour, labels kept clear."""
    x0, x1 = M, W - M
    span = x1 - x0

    def hx(h):
        return x0 + span * h / 24.0

    tracked(draw, (x0, y), "SUNDAY 22 NOVEMBER, HOUR BY HOUR IN UTC",
            font(SERIF_BOLD, 10), ACCENT, tracking=1.2)

    axis = y + 24
    draw.rectangle([x0, axis, x1 - 1, axis + 1], fill=RULE)

    tick_f = font(SERIF_COND, 8)
    for h in range(0, 24, 2):
        tx = hx(h)
        draw.rectangle([tx, axis + 3, tx, axis + 7], fill=(120, 116, 106))
        lab = "%02d" % h
        draw.text((tx - text_w(draw, lab, tick_f) / 2, axis + 9), lab,
                  font=tick_f, fill=MUTED)

    lab_f = font(SERIF_COND, 11)
    for i, (h, text) in enumerate(D_PINS):
        px = hx(h)
        draw.polygon([(px, axis - 14), (px + 5, axis - 9), (px, axis - 4),
                      (px - 5, axis - 9)], fill=ACCENT)
        tw = text_w(draw, text, lab_f)
        left = min(max(px - tw / 2.0, x0), x1 - tw)
        ly = axis + 24 + (i % 2) * 15
        draw.line([(px, axis + 2), (px, ly - 3)], fill=(176, 172, 162),
                  width=1)
        draw.text((left, ly - 2), text, font=lab_f, fill=SOFT)
    return axis + 24 + 15 + 16


D_REGIONS = [
    ("EUROPE", (62, 92, 138)),
    ("MIDDLE EAST", (168, 112, 46)),
    ("ASIA", (140, 62, 70)),
    ("AMERICAS", (72, 110, 84)),
    ("SPORT", (92, 84, 130)),
]


def d_regions(draw, y):
    """Flat colour strip: one chip per region covered on the page."""
    gap = 6
    chip_w = (W - 2 * M - gap * (len(D_REGIONS) - 1)) / len(D_REGIONS)
    label_f = font(SERIF_BOLD, 9)
    for i, (name, color) in enumerate(D_REGIONS):
        cx = M + i * (chip_w + gap)
        draw.rectangle([cx, y, cx + chip_w - 1, y + 13], fill=color)
        tw = text_w(draw, name, label_f) + 1.6 * (len(name) - 1)
        tx = cx + (chip_w - tw) / 2
        for ch in name:
            draw.text((tx, y + 2), ch, font=label_f, fill=PAPER)
            tx += text_w(draw, ch, label_f) + 1.6
    return y + 13


D_TAG_COLORS = {"CLAIM": ACCENT, "REPORTED": (146, 106, 18)}


def d_tag(draw, xy, name):
    """Small coloured flag; the text stays clear of every other element."""
    x, y = xy
    f = font(SERIF_BOLD, 9)
    label = name
    tw = text_w(draw, label, f) + 2 * (len(label) - 1)
    color = D_TAG_COLORS[name]
    draw.rectangle([x, y, x + tw + 7, y + 12], fill=color)
    tx = x + 3.5
    for c in label:
        draw.text((tx, y + 1), c, font=f, fill=PAPER)
        tx += text_w(draw, c, f) + 2
    return x + tw + 7


D_MAP_PINS = [
    (1, 30.7, 36.9, "COP31 ANTALYA"),
    (2, 20.1, 32.1, "BENGHAZI"),
    (3, 50.6, 26.15, "SITRA"),
]


def d_map(draw, y, h=58):
    """Plain world outline with three numbered pins for the lead stories."""
    x0, x1 = M, W - M
    w = x1 - x0
    top = y + 13

    def px(lon):
        return x0 + (lon + 180) / 360.0 * w

    def py(lat):
        return top + (78 - lat) / 156.0 * h

    tracked(draw, (x0, y), "WHERE THE DAY HAPPENED", font(SERIF_BOLD, 9),
            SOFT, tracking=1.2)
    draw.rectangle([x0, top, x1 - 1, top + h - 1], fill=(232, 240, 246),
                   outline=(198, 214, 228))

    for poly in CONTINENTS:
        pts = [(px(lon), py(lat)) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)

    for n, lon, lat, label in D_MAP_PINS:
        cx, cy = px(lon), py(lat)
        r = 7
        draw.line([(cx, cy), (cx, cy - 10)], fill=ACCENT, width=2)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT)
        f = font(SERIF_BOLD, 10)
        draw.text((cx - text_w(draw, str(n), f) / 2, cy - 6), str(n),
                  font=f, fill=PAPER)
        lf = font(SERIF_BOLD, 9)
        lw = text_w(draw, label, lf)
        lx = min(max(cx - lw / 2, x0 + 2), x1 - lw - 2)
        ly = min(cy + r + 2, top + h - 11)
        draw.rectangle([lx - 2, ly - 1, lx + lw + 2, ly + 10], fill=(232, 240, 246))
        draw.text((lx, ly - 1), label, font=lf, fill=SOFT)
    return top + h


D_LEADS = [
    ("COP31", "Antalya", "CLIMATE TALKS END WITH NO DEAL",
     "Summit closes two days late; no final text names coal, oil or gas.",
     "building", ""),
    ("LIBYA", "Benghazi", "SUSPECTED DRONE HITS RUSSIAN WARSHIP",
     "At Benghazi naval base; 10 lightly wounded, officials say.",
     "ship", ""),
    ("BAHRAIN", "Sitra", "BAHRAIN SAYS IRAN STRUCK PLANT",
     "IRGC claims the strike.", "fire", "CLAIM"),
]


def d_illustration(draw, box, kind, color=ACCENT):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if kind == "building":
        draw_building_symbol(draw, x0, y0, w, h, "parliament", "thermometer",
                             color)
    elif kind == "ship":
        draw_ship(draw, x0, y0, w, h, (126, 150, 172), fire=True, smoke=True)
    else:
        draw_fire_smoke(draw, x0, y0, w, h, FLAME, h * 0.40)


def d_leads(draw, y):
    """Three lead stories: illustration left, headline and standfirst right."""
    gap = 10
    card_w = (W - 2 * M - 2 * gap) / 3
    art_w = 84
    txt_w = card_w - art_w - 8
    hk_f = font(SERIF_BOLD, 10)
    head_f = font(SERIF_BOLD, 21)
    sub_f = font(SERIF, 18)
    sub_lh = int(18 * 1.30)
    head_lh = int(21 * 1.10)

    tallest = 0
    for i, (kick, place, head, sub, kind, tag) in enumerate(D_LEADS):
        x0 = M + i * (card_w + gap)
        head_lines = wrap(draw, head, head_f, txt_w)[:3]
        sub_lines = wrap(draw, sub, sub_f, txt_w)[:3]
        th = 13 + len(head_lines) * head_lh + 4 + len(sub_lines) * sub_lh
        tallest = max(tallest, th)

    for i, (kick, place, head, sub, kind, tag) in enumerate(D_LEADS):
        x0 = M + i * (card_w + gap)
        tx = x0 + art_w + 8
        d_illustration(draw, (x0, y, x0 + art_w, y + tallest), kind,
                       (62, 92, 138) if i == 0 else ACCENT)
        kx = tracked(draw, (tx, y), kick, hk_f, ACCENT, tracking=1.4)
        px_ = kx + 4
        draw.text((px_, y + 1), place, font=font(SERIF_COND, 10), fill=MUTED)
        if tag:
            tag_w = text_w(draw, tag, font(SERIF_BOLD, 9)) + 2 * (len(tag) - 1)
            d_tag(draw, (tx + txt_w - tag_w - 7, y), tag)
        head_lines = wrap(draw, head, head_f, txt_w)[:3]
        yy = para(draw, (tx, y + 13), head_lines, head_f, INK, head_lh)
        sub_lines = wrap(draw, sub, sub_f, txt_w)[:3]
        para(draw, (tx, yy + 4), sub_lines, sub_f, SOFT, sub_lh)
    return y + tallest


D_MIDS = [
    ("UKRAINE", "Dymer, near Kyiv", "At least 3 killed.", ""),
    ("FOOTBALL", "Liverpool 4-0 Man Utd", "4-0, kick-off 16:30 UTC.", ""),
    ("FOOTBALL", "Barcelona 3-2 Villarreal", "3-2, kick-off 13:00 UTC.", ""),
    ("NFL", "Dallas 51-30 Tennessee", "51-30, kick-off 18:00 UTC.", ""),
    ("NFL", "Kansas City 34-7 Arizona", "34-7, kick-off 18:00 UTC.", ""),
    ("NFL", "Buffalo 26-9 Miami", "26-9, kick-off 18:00 UTC.", ""),
    ("UKRAINE", "Russia fires 186 drones", "161 downed, Kyiv says.", ""),
    ("WEST BANK", "Settlers burn 12 cars", "Four villages hit overnight.",
     "REPORTED"),
    ("CRICKET", "India declare 720/9", "Lead 352; NZ 119/2 in reply.", ""),
    ("VATICAN", "Pope Leo XIV eats with poor", "1,300 guests at the Vatican.",
     ""),
]


def d_mids(draw, y, cols=5):
    """Ten medium stories in two rows; only the standfirst length is trimmed."""
    gap = 12
    col_w = (W - 2 * M - gap * (cols - 1)) / cols
    kf = font(SERIF_BOLD, 9)
    head_f = font(SERIF_BOLD, 19)
    sub_f = font(SERIF, 18)
    head_lh = int(19 * 1.10)
    sub_lh = int(18 * 1.20)

    rows = [D_MIDS[i:i + cols] for i in range(0, len(D_MIDS), cols)]
    yy = y
    for r, row in enumerate(rows):
        tag_h = 16 if any(item[3] for item in row) else 0
        row_h = 11 + tag_h + 2 * head_lh + 3 + sub_lh + 9
        for c, (kick, head, sub, tag) in enumerate(row):
            x0 = M + c * (col_w + gap)
            tracked(draw, (x0, yy), kick, kf, ACCENT, tracking=1.2)
            hy = yy + 11
            if tag:
                d_tag(draw, (x0, yy + 13), tag)
                hy = yy + 29
            head_lines = wrap(draw, head, head_f, col_w)[:2]
            ny = para(draw, (x0, hy), head_lines, head_f, INK, head_lh)
            sub_lines = wrap(draw, sub, sub_f, col_w)[:1]
            para(draw, (x0, ny + 3), sub_lines, sub_f, SOFT, sub_lh)
        if r == 0:
            rule(draw, int(yy + row_h - 5), M, W - M, 1, (206, 201, 190))
        yy += row_h
    return yy


D_LIST = [
    ("HONG KONG", "98.79% turnout, polls shut 18:00 HKT (10:00 UTC)", "REPORTED"),
    ("NEPAL", "PM Balendra Shah lands in Delhi", ""),
    ("F1", "Verstappen wins, finishes 05:50 UTC", ""),
    ("USA", "Strathmore shooting, 9 shot at concert, ~03:30 UTC", ""),
    ("NBA", "Wembanyama 50 points, 18 rebounds", ""),
]


def d_list(draw, y, cols=2):
    """Short items at 19pt, two columns. A text too long for the rest of its
    first line drops to its own line instead of being clipped or crowded."""
    gap = 16
    col_w = (W - 2 * M - gap) / cols
    kf = font(SERIF_BOLD, 12)
    tf = font(SERIF, 19)
    tf_lh = 22
    tracked(draw, (M, y), "IN BRIEF", font(SERIF_BOLD, 10), SOFT, tracking=1.2)
    y += 14
    half = (len(D_LIST) + 1) // 2

    def kick_w(kick):
        return sum(text_w(draw, c, kf) + 1.0 for c in kick) - 1.0

    def layout(kick, text):
        """(offset of the text block from the kicker line, lines)."""
        if text_w(draw, text, tf) <= col_w - kick_w(kick) - 6:
            return -2, [text]
        return tf_lh - 3, wrap(draw, text, tf, col_w)

    def item_h(item):
        dy, lines = layout(item[0], item[1])
        h = dy + 2 + len(lines) * tf_lh
        if item[2]:
            h += 16
        return max(h, 26)

    row_y = [y]
    for i in range(half):
        pair = [D_LIST[i]] + ([D_LIST[i + half]] if i + half < len(D_LIST) else [])
        row_y.append(row_y[-1] + max(item_h(it) for it in pair))
    for i, (kick, text, tag) in enumerate(D_LIST):
        col, row = (0, i) if i < half else (1, i - half)
        x0 = M + col * (col_w + gap)
        yy = row_y[row]
        kx = tracked(draw, (x0, yy), kick, kf, INK, tracking=1.0)
        dy, lines = layout(kick, text)
        ty = yy + dy
        for n, ln in enumerate(lines):
            tx = kx + 5 if (n == 0 and dy < 0) else x0
            draw.text((tx, ty), ln, font=tf, fill=SOFT)
            ty += tf_lh
        if tag:
            d_tag(draw, (x0, ty + 1), tag)
    return row_y[half] - 4


D_DATES = [
    ("MEXICO . MARKETS", "Friday 20 Nov"),
    ("BEPICOLOMBO", "Saturday 21 Nov, 18:24 UTC"),
    ("SPARTA II", "Saturday 21 Nov, ~06:50 UTC"),
    ("BOLSONARO", "Friday 20 Nov"),
    ("CIKANDE", "Saturday 21 Nov, night"),
    ("NIGERIA", "held, date not confirmed"),
    ("ESTONIA", "decided Fri 20 Nov, announced Sun 15 Nov, effective 1 Dec"),
]


def d_datecheck(draw, y):
    """Red box: stories from other days, deliberately kept out of the page."""
    x0, x1 = M, W - M
    pad = 7
    gap = 14
    hf = font(SERIF_BOLD, 10)
    of = font(SERIF_BOLD, 12)
    df = font(SERIF, 11)
    row_h = 13
    col_w = (x1 - x0 - pad * 2 - gap) / 2
    half = 4
    h = 6 + 14 + 4 + half * row_h + pad
    draw.rectangle([x0, y, x1 - 1, y + h - 1], fill=(250, 236, 234),
                   outline=ACCENT, width=2)
    tracked(draw, (x0 + pad, y + 5), "DATE CHECK . NOT YET 22 NOVEMBER", hf,
            ACCENT, tracking=1.2)
    top = y + 6 + 15
    for i, (name, when) in enumerate(D_DATES):
        col, row = (0, i) if i < half else (1, i - half)
        cx = x0 + pad + col * (col_w + gap)
        yy = top + row * row_h
        ow = text_w(draw, name, of)
        draw.text((cx, yy), name, font=of, fill=ACCENT)
        lines = wrap(draw, when, df, col_w - ow - 8)
        draw.text((cx + ow + 6, yy + 2), lines[0] if lines else when,
                  font=df, fill=SOFT)
    return y + h


D_FOOTER_STORIES = 18


def d_footer(draw, y):
    """Bottom rule, paper name and the count of stories on the page."""
    rule(draw, y, M, W - M, 3)
    f = font(SERIF_BOLD, 12)
    left = "THE WORLD . SUNDAY 22 NOVEMBER 2026"
    right = "%d STORIES" % D_FOOTER_STORIES
    draw.text((M, y + 7), left, font=f, fill=INK)
    draw.text((W - M - text_w(draw, right, f), y + 7), right, font=f, fill=INK)
    return y + 24


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = d_masthead(draw)
    y = d_numbers(draw, y + 4)
    y = d_timeline(draw, y + 8)
    y += 5
    rule(draw, y, M, W - M, 1, (150, 146, 136))
    y = d_regions(draw, y + 6)
    y = d_map(draw, y + 8)
    y = d_leads(draw, y + 8)
    y = d_mids(draw, y + 8)
    y = d_list(draw, y + 6)
    y = d_datecheck(draw, y + 8)
    y = d_footer(draw, y + 7)
    return img, y


def render(path):
    img, y = build()
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, img.size, "frame bottom", y)


def main():
    img, _ = build()
    img.save("image.png", format="PNG", optimize=True)
    print("wrote image.png", img.size)


if __name__ == "__main__":
    main()
