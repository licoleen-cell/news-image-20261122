"""Draw the front page of THE WORLD for Sunday 22 November 2026.

Three tiers: a rail of the day's key numbers, three main stories, seven
medium reports with locator globes, and eight one-line briefs.
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
HAIR = (201, 196, 185)
ACCENT = (138, 24, 24)
GREEN = (26, 94, 56)
SEA = (188, 208, 228)
LAND = (247, 241, 224)
LAND_EDGE = (166, 152, 124)
GRID_LINE = (163, 186, 209)

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
SERIF_XCOND_BOLD = FONT_DIR + "NotoSerif-ExtraCondensedBold.ttf"
SERIF_XCOND = FONT_DIR + "NotoSerif-ExtraCondensed.ttf"
SERIF = FONT_DIR + "NotoSerif-Regular.ttf"
SERIF_ITALIC = FONT_DIR + "NotoSerif-Italic.ttf"

DATE_SIZE = 52
NUM_SIZE = 48
LEAD_KICKER_SIZE = 16
LEAD_HL_MAX, LEAD_HL_MIN = 36, 33
LEAD_DECK_SIZE = 17
MAIN_HL_MAX, MAIN_HL_MIN = 34, 32
MAIN_SUB_SIZE = 17
MED_HL_MAX, MED_HL_MIN = 24, 24
MED_SUB_SIZE = 14
FRIDAY_TAG_SIZE = 19
BRIEF_SIZE = 13
BRIEF_ROW = 17

NUMBERS = [
    ("2", "WOUNDED, BAHRAIN"),
    ("24", "DEAD, NIGERIA"),
    ("3", "DEAD, CIKANDE"),
    ("11", "DEAD, MEXICO"),
    ("9", "SHOT, CALIFORNIA"),
    ("8", "YEARS, MERCURY"),
]

LEAD_KICKER = "CLIMATE SUMMIT COLLAPSES"
LEAD_HL = "COP31 collapses without a deal as Europe holds firm"
LEAD_DECK = ("Antalya talks close two days late and empty-handed after the EU bloc "
             "refuses to sign a final text that never names coal, oil or gas.")

MAINS = [
    ("LIBYA . BENGHAZI", "Sea drone hits Russian warship",
     "Libyan officers say a suspected Ukrainian drone struck it.",
     None, (20.0, 33.0), (20.07, 32.12)),
    ("BAHRAIN . SITRA", "Iran projectile hits Bahrain industrial site",
     "Two wounded at Sitra; Iran's Guards claim two US radars hit.",
     ("CLAIM", ACCENT), (50.6, 26.2), (50.60, 26.15)),
]

MEDIUM = [
    ("UKRAINE . DYMER", "Russian drone hits Kyiv apartment block",
     "Rescue teams search the rubble in Dymer, near the capital.",
     None, (30.5, 50.4), (30.52, 50.45)),
    ("CIKANDE", "Factory fire kills at least three in Banten",
     "Blaze at a candy plant in Cikande leaves dozens missing.",
     None, (107.5, -6.2), (107.42, -6.17)),
    ("WEST BANK . RAMALLAH", "Settlers burn cars across West Bank",
     "Israel opens a probe into arson in four villages.",
     None, (35.2, 31.9), (35.20, 31.90)),
    ("NIGERIA . BAYELSA", "Boat capsize kills at least 24 in Nigeria",
     "At least 24 died; the vessel carried mourners to a funeral.",
     None, (6.3, 4.9), (6.28, 4.93)),
    ("MEXICO", "Mexico captures El Chapo Isidro",
     "11 killed as special forces arrest the Los Mazatlecos boss.",
     ("FRIDAY", ACCENT), (-107.5, 25.0), (-108.05, 25.57)),
    ("SPARTA II", "Fire-hit Russian ship still smoulders in Finnish waters",
     "16 crew evacuated, one lightly injured after Saturday fire.",
     None, (20.0, 58.0), (22.10, 59.80)),
]

LEGEND_TITLE = "HOW TO READ THE TAGS"
LEGEND = [
    ("CLAIM", ACCENT, "one side's account, not verified"),
    ("CONFIRMED", GREEN, "two or more independent sources"),
    ("FRIDAY", ACCENT, "dated Friday 20 Nov; markets shut"),
]

BRIEFS = [
    ("HOUTHIS", "Houthis claim strike on Saudi refinery", "CLAIM"),
    ("SUDAN", "Drones hit Khartoum homes and UN building", None),
    ("SOUTH SUDAN", "Raid on cattle camp kills civilians in South Sudan", None),
    ("BOLSONARO", "Bolsonaro stable in intensive care", None),
    ("CALIFORNIA", "9 shot at California concert; 1 critical", None),
    ("BEPI COLOMBO", "BepiColombo enters Mercury orbit after 8-year trip",
     "CONFIRMED"),
    ("MARKETS", "Wall Street: S&P -3.7%, Nasdaq -5.3%", "FRIDAY"),
]

FOOTER_L = "THREE MAIN STORIES . SIX MEDIUM REPORTS . SEVEN BRIEFS"
FOOTER_R = "PAGE ONE"

TYPE = {}
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


def uniform(draw, texts, path, size, max_w, max_lines, floor):
    """One size for a whole tier: small enough for the widest string."""
    s = size
    while s > floor:
        f = font(path, s)
        if all(len(wrap(draw, t, f, max_w)) <= max_lines for t in texts):
            return f
        s -= 1
    return font(path, floor)


def tracked(draw, xy, text, f, fill, tracking=1.6, anchor_left=True):
    """Draw letterspaced capitals. Returns the x after the last glyph."""
    x, y = xy
    if not anchor_left:
        x -= tracked_w(draw, text, f, tracking)
    for c in text:
        draw.text((x, y), c, font=f, fill=fill)
        x += text_w(draw, c, f) + tracking
    return x - tracking


def tracked_w(draw, text, f, tracking):
    return sum(text_w(draw, c, f) + tracking for c in text) - tracking


def rule(draw, y, x0, x1, weight=1, fill=RULE):
    draw.rectangle([x0, y, x1 - 1, y + weight - 1], fill=fill)


def para(draw, xy, lines, f, fill, line_h):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += line_h
    return y


def chip(draw, x, y, text, fill, size=9, fg=PAPER, padx=5, tracking=1.3,
         right=False):
    """Filled tag with letterspaced capitals. Returns (width, height)."""
    f = font(SERIF_COND_BOLD, size)
    w = tracked_w(draw, text, f, tracking) + 2 * padx
    h = int(round(size * 1.30)) + 4
    if right:
        x -= w
    draw.rectangle([x, y, x + w, y + h], fill=fill)
    bbox = draw.textbbox((0, 0), text, font=f)
    ty = y + (h - (bbox[3] - bbox[1])) / 2 - bbox[1]
    cx = x + padx
    for c in text:
        draw.text((cx, ty), c, font=f, fill=fg)
        cx += text_w(draw, c, f) + tracking
    return w, h


def ink_at(draw, cx, y_ink, text, f, fill, track=0.0):
    """Draw text centred on cx with the top of the ink at y_ink."""
    w = text_w(draw, text, f)
    total = w + track * (len(text) - 1)
    x = cx - total / 2
    off = draw.textbbox((0, 0), text, font=f)[1]
    for c in text:
        draw.text((x, y_ink - off), c, font=f, fill=fill)
        x += text_w(draw, c, f) + track
    return draw.textbbox((0, 0), text, font=f)[3] - off


def ink_centered(draw, y_ink, text, f, fill, track=0.0):
    return ink_at(draw, W / 2, y_ink, text, f, fill, track)


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
    cap_h = ink_centered(draw, 32, title, f, INK, track)
    TYPE["masthead"] = f.size

    y = 32 + cap_h + 10
    rule(draw, y, M, W - M, 3)
    rule(draw, y + 6, M, W - M, 1)

    date_f = font(SERIF_BOLD, DATE_SIZE)
    dt = "SUNDAY 22 NOVEMBER 2026"
    dy = y + 11
    dh = ink_at(draw, W / 2, dy, dt, date_f, INK, 3.2)
    TYPE["date"] = date_f.size
    dw = tracked_w(draw, dt, date_f, 3.2)
    mid = dy + dh * 0.52
    rule(draw, int(mid), M, int((W - dw) / 2) - 12, 1)
    rule(draw, int(mid), int((W + dw) / 2) + 12, W - M, 1)

    base = int(dy + dh + 10)
    rule(draw, base, M, W - M, 5)
    return base + 5


def _project(lon, lat, cx, cy, r, lon0, lat0):
    """Orthographic projection; returns (x, y) or None if on the far side."""
    import math
    lam = math.radians(lon - lon0)
    phi = math.radians(lat)
    phi0 = math.radians(lat0)
    cos_c = (math.sin(phi0) * math.sin(phi)
             + math.cos(phi0) * math.cos(phi) * math.cos(lam))
    if cos_c < 0:
        return None
    return (cx + r * math.cos(phi) * math.sin(lam),
            cy - r * (math.cos(phi0) * math.sin(phi)
                      - math.sin(phi0) * math.cos(phi) * math.cos(lam)))


def globe(box, centre=(18.0, 28.0), marker=None, grid=True, leader=False):
    """Orthographic locator globe with an optional pin, as an RGBA layer."""
    x0, y0, x1, y1 = box
    size = min(x1 - x0, y1 - y0)
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    r = size / 2 - 1
    lon0, lat0 = centre
    big = r > 34

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(layer)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEA + (255,))

    if grid and big:
        for lon in range(-180, 180, 30):
            pts = [p for p in (_project(lon, lat, cx, cy, r, lon0, lat0)
                               for lat in range(-90, 91, 3)) if p]
            if len(pts) > 1:
                g.line(pts, fill=GRID_LINE + (255,), width=1)
        for lat in (-60, -30, 0, 30, 60):
            pts = [p for p in (_project(lon, lat, cx, cy, r, lon0, lat0)
                               for lon in range(-180, 181, 3)) if p]
            if len(pts) > 1:
                g.line(pts, fill=GRID_LINE + (255,), width=1)

    for poly in CONTINENTS:
        pts = [p for p in (_project(lon, lat, cx, cy, r, lon0, lat0)
                           for lon, lat in poly) if p]
        if len(pts) > 2:
            g.polygon(pts, fill=LAND + (255,))
    for poly in CONTINENTS:
        pts = [p for p in (_project(lon, lat, cx, cy, r, lon0, lat0)
                           for lon, lat in poly) if p]
        if len(pts) > 2:
            g.line(pts + [pts[0]], fill=LAND_EDGE + (255,), width=1)

    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.paste(layer, (0, 0), mask)
    g = ImageDraw.Draw(base)
    g.ellipse([cx - r, cy - r, cx + r, cy + r],
              outline=(92, 116, 138, 255), width=2 if big else 1)

    if marker:
        px, py = _project(marker[0], marker[1], cx, cy, r, lon0, lat0) or (cx, cy)
        g.ellipse([px - 1.7, py - 1.7, px + 1.7, py + 1.7], fill=ACCENT + (255,))
        ring = max(3.2, r * 0.13)
        g.ellipse([px - ring, py - ring, px + ring, py + ring],
                  outline=ACCENT + (255,), width=2 if big else 1)
        if leader:
            g.line([px + 0.16 * r, py - 0.16 * r, px + 0.66 * r, py - 0.66 * r],
                   fill=ACCENT + (255,), width=2)
            g.ellipse([px + 0.66 * r - 2, py - 0.66 * r - 2,
                       px + 0.66 * r + 2, py - 0.66 * r + 2], fill=ACCENT + (255,))
    return base


def numbers_rail(draw, top):
    lab_f = font(SERIF_COND_BOLD, 10)
    tracked(draw, (M, top), "THE DAY IN NUMBERS", lab_f, ACCENT, tracking=2.0)

    y_num = top + 11
    num_f = font(SERIF_BLACK, NUM_SIZE)
    TYPE["numbers"] = num_f.size
    bb = draw.textbbox((0, 0), "24", font=num_f)
    y_lab = y_num + (bb[3] - bb[1]) + 2

    cell = (W - 2 * M) / 6
    small = font(SERIF_COND_BOLD, 9)
    for i in range(1, 6):
        x = M + cell * i
        draw.rectangle([int(x), y_num - 2, int(x), y_lab + 10], fill=HAIR)

    for i, (num, label) in enumerate(NUMBERS):
        cx = M + cell * (i + 0.5)
        ink_at(draw, cx, y_num, num, num_f, INK)
        lw = text_w(draw, label, small)
        draw.text((cx - lw / 2, y_lab), label, font=small, fill=SOFT)

    base = int(y_lab + 17)
    rule(draw, base, M, W - M, 2)
    return base + 2


def lead(img, draw, top):
    tx, tw = M + 2, 690
    k_f = font(SERIF_BOLD, LEAD_KICKER_SIZE)
    TYPE["lead_kicker"] = k_f.size
    tracked(draw, (tx, top), LEAD_KICKER, k_f, ACCENT, tracking=1.9)

    f, lines = fit(draw, LEAD_HL, SERIF_BLACK, LEAD_HL_MAX, tw, 2, LEAD_HL_MIN)
    TYPE["lead_hl"] = f.size
    TYPE["lead_hl_lines"] = len(lines)
    y = top + 23
    y = para(draw, (tx, y), lines, f, INK, int(f.size * 1.1))

    rule(draw, y + 8, tx, tx + tw, 1, HAIR)
    y += 15
    df, dlines = fit(draw, LEAD_DECK, SERIF_ITALIC, LEAD_DECK_SIZE, tw, 2,
                     LEAD_DECK_SIZE - 1)
    TYPE["lead_deck"] = df.size
    TYPE["lead_deck_lines"] = len(dlines)
    y = para(draw, (tx, y), dlines, df, SOFT, int(df.size * 1.3))

    art = globe((742, top, 996, top + 152), (18.0, 28.0), (30.7, 36.9),
                leader=True)
    img.paste(art, (0, 0), art)
    return y


def mains(img, draw, top):
    gap = 26
    cw = (W - 2 * M - gap) / 2
    art, tx = 76, 82
    tw = cw - tx - 4
    hl_f = uniform(draw, [m[1] for m in MAINS], SERIF_BLACK, MAIN_HL_MAX, tw, 2,
                   MAIN_HL_MIN)
    TYPE["main_hl"] = hl_f.size
    hl_lh = int(hl_f.size * 1.06)
    sub_f = font(SERIF, MAIN_SUB_SIZE)
    TYPE["main_sub"] = sub_f.size
    sub_lh = int(sub_f.size * 1.3)
    k_f = font(SERIF_COND_BOLD, 11)

    bottom = top
    for i, (kick, head, sub, tag, centre, pin) in enumerate(MAINS):
        x0 = M + i * (cw + gap)
        art_img = globe((x0, top, x0 + art, top + art), centre, pin)
        img.paste(art_img, (0, 0), art_img)

        kx = tracked(draw, (x0 + tx, top + 1), kick, k_f, ACCENT, tracking=1.3)
        if tag:
            chip(draw, x0 + cw, top - 2, tag[0], tag[1], size=9, right=True)

        y = para(draw, (x0 + tx, top + 20), wrap(draw, head, hl_f, tw), hl_f,
                 INK, hl_lh)
        y = para(draw, (x0 + tx, y + 4), wrap(draw, sub, sub_f, tw), sub_f,
                 SOFT, sub_lh)
        bottom = max(bottom, y)
        assert kx < x0 + cw, "main kicker overflow"
    return bottom


def medium(img, draw, top):
    gap, cols = 12, 3
    cw = (W - 2 * M - gap * (cols - 1)) / cols
    pad = 7
    tw = cw - 2 * pad
    badge = 34
    head_f = uniform(draw, [m[1] for m in MEDIUM], SERIF_XCOND_BOLD, MED_HL_MAX,
                     tw, 2, MED_HL_MIN)
    TYPE["medium_hl"] = head_f.size
    hl_lh = int(head_f.size * 1.04)
    sub_f = font(SERIF_XCOND, MED_SUB_SIZE)
    TYPE["medium_sub"] = sub_f.size
    sub_lh = int(sub_f.size * 1.28)
    k_f = font(SERIF_COND_BOLD, 10)

    heights = []
    for kick, head, sub, tag, centre, pin in MEDIUM:
        hl = wrap(draw, head, head_f, tw)
        sb = wrap(draw, sub, sub_f, tw)
        heights.append(badge + 5 + len(hl) * hl_lh + 3 + len(sb) * sub_lh)

    row_h = [max(heights[r * cols:(r + 1) * cols])
             for r in range((len(MEDIUM) + cols - 1) // cols)]
    row_top = [sum(row_h[:r]) + gap * r for r in range(len(row_h))]

    for i, (kick, head, sub, tag, centre, pin) in enumerate(MEDIUM):
        r, c = divmod(i, cols)
        x0 = M + c * (cw + gap)
        y0 = top + row_top[r]
        art_img = globe((x0, y0, x0 + badge, y0 + badge), centre, pin,
                        grid=False)
        img.paste(art_img, (0, 0), art_img)

        kx = x0 + badge + 7
        if tag and tag[0] == "FRIDAY":
            cwp, chp = chip(draw, kx, y0 + 1, "FRIDAY", ACCENT,
                            size=FRIDAY_TAG_SIZE, tracking=1.8)
            TYPE["friday_tag"] = FRIDAY_TAG_SIZE
            kx += cwp + 7
        kx = tracked(draw, (kx, y0 + 11 if not (tag and tag[0] == "FRIDAY")
                            else y0 + 13), kick, k_f, ACCENT, tracking=1.2)
        if tag and tag[0] != "FRIDAY":
            cwp, chp = chip(draw, x0 + cw - 2, y0 + 8, tag[0], tag[1],
                            size=8.5, tracking=1.2, right=True)
            assert kx + 6 <= x0 + cw - 2 - cwp, "medium tag overflow: %s" % kick

        y = para(draw, (x0 + pad, y0 + badge + 5),
                 wrap(draw, head, head_f, tw), head_f, INK, hl_lh)
        para(draw, (x0 + pad, y + 3), wrap(draw, sub, sub_f, tw), sub_f, SOFT,
             sub_lh)

        if c < cols - 1:
            draw.rectangle([int(x0 + cw + gap / 2), int(y0 + 2),
                            int(x0 + cw + gap / 2) + 1,
                            int(y0 + row_h[r] - 4)], fill=HAIR)

    return top + row_top[-1] + row_h[-1]


def legend(draw, x, y):
    """Tag key drawn inline on the IN BRIEF header line."""
    t_f = font(SERIF_COND_BOLD, 9)
    x = tracked(draw, (x, y + 3), LEGEND_TITLE, t_f, ACCENT, tracking=1.5) + 14
    body = font(SERIF_COND, 10)
    for tag, col, text in LEGEND:
        w, h = chip(draw, x, y - 1, tag, col, size=8.5)
        x += w + 5
        draw.text((x, y + 1), text, font=body, fill=SOFT)
        x += text_w(draw, text, body) + 18
    assert x <= W - M, "legend overflow"
    return x


def briefs(draw, top):
    slug = font(SERIF_COND_BOLD, 10)
    x = tracked(draw, (M, top + 2), "IN BRIEF", slug, ACCENT, tracking=1.8)
    legend(draw, x + 16, top)
    rule(draw, top + 17, M, W - M, 1, RULE)

    col_gap = 26
    col_w = (W - 2 * M - col_gap) / 2
    name_w = 112
    text_f = font(SERIF_COND, BRIEF_SIZE)
    TYPE["briefs"] = BRIEF_SIZE
    name_f = font(SERIF_COND_BOLD, 9.5)
    y = top + 22
    per_col = 4
    nrows = min(per_col, len(BRIEFS))
    # a 19pt FRIDAY tag is ~29px tall, taller than the 17px row pitch, so the
    # row that carries it gets extra space to keep it clear of the row above
    friday_rows = {i % per_col for i, b in enumerate(BRIEFS)
                   if b[2] == "FRIDAY"}
    row_tops, acc = [], 0
    for r in range(nrows):
        row_tops.append(acc)
        acc += BRIEF_ROW + (10 if r in friday_rows else 0)

    for i, (name, text, tag) in enumerate(BRIEFS):
        c, r = divmod(i, per_col)
        x0 = M + c * (col_w + col_gap)
        x_end = x0 + col_w
        ry = y + row_tops[r]
        if tag == "FRIDAY":
            w, h = chip(draw, x0, ry - 6, "FRIDAY", ACCENT,
                        size=FRIDAY_TAG_SIZE, tracking=1.8)
            nx = x0 + w + 7
            tracked(draw, (nx, ry + 1), name, name_f, INK, tracking=1.2)
            tx = nx + tracked_w(draw, name, name_f, 1.2) + 8
            assert tx + text_w(draw, text, text_f) <= x_end, (
                "brief overflow: %s" % text)
            draw.text((tx, ry), text, font=text_f, fill=SOFT)
            continue
        tracked(draw, (x0, ry + 1), name, name_f, INK, tracking=1.2)
        x = x0 + name_w
        if tag:
            col = {"CLAIM": ACCENT, "CONFIRMED": GREEN}.get(tag, ACCENT)
            w, h = chip(draw, x_end, ry - 2, tag, col, size=8.5, right=True)
            x_end -= w + 6
        assert x + text_w(draw, text, text_f) <= x_end, (
            "brief overflow: %s" % text)
        draw.text((x, ry), text, font=text_f, fill=SOFT)

    return y + row_tops[-1] + 18


def footer(draw, y):
    rule(draw, y, M, W - M, 2)
    f = font(SERIF_COND, 10)
    tracked(draw, (M, y + 6), FOOTER_L, f, MUTED, tracking=1.1)
    tracked(draw, (W - M, y + 6), FOOTER_R, f, MUTED, tracking=1.1,
            anchor_left=False)
    return y + 18


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = masthead(draw)
    TYPE["masthead_bottom"] = y
    y = numbers_rail(draw, y + 8)
    TYPE["numbers_bottom"] = y
    y = lead(img, draw, y + 6)
    TYPE["lead_bottom"] = y
    rule(draw, int(y + 4), M, W - M, 2)
    y = mains(img, draw, y + 11)
    TYPE["mains_bottom"] = y
    rule(draw, int(y + 4), M, W - M, 1, HAIR)
    rule(draw, int(y + 6), M, W - M, 1, HAIR)
    y = medium(img, draw, y + 12)
    TYPE["medium_bottom"] = y
    y = briefs(draw, y + 9)
    TYPE["briefs_bottom"] = y
    TYPE["footer_top"] = y + 12
    footer(draw, y + 9)
    TYPE["page_bottom"] = y + 9 + 18
    assert y + 9 + 18 <= H - M + 2, "page overflow: %d" % (y + 27)
    return img


def main(argv=None):
    import sys
    argv = sys.argv[1:] if argv is None else argv
    img = build()
    if "measure" in argv:
        for k in ("masthead", "date", "numbers", "lead_kicker", "lead_hl",
                  "lead_deck", "main_hl", "main_sub", "medium_hl", "medium_sub",
                  "friday_tag", "briefs"):
            if k in TYPE:
                print("%-10s %s" % (k, TYPE[k]))
        for k in ("masthead_bottom", "numbers_bottom", "lead_bottom",
                  "mains_bottom", "medium_bottom", "briefs_bottom",
                  "footer_top", "page_bottom"):
            print("%-16s %s" % (k, TYPE[k]))
        return
    img.save("image.png", format="PNG", optimize=True)
    print("wrote image.png", img.size)


if __name__ == "__main__":
    main()
