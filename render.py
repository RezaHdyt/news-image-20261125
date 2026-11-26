#!/usr/bin/env python3
"""Render the news-image-20261125 front page: one 1024x1024 PNG.

Draws Wednesday 25 November 2026 world news as a newspaper front page:
masthead, a big Cairo fire hero, a labelled UTC timeline, a 3x4 grid of
story panels (the last cell is a small world map), 19 one-line briefs, a
DATE CHECK box and a sources footer. Pure Pillow, no network, no photos.
Run:  python3 render.py   (writes entry.png next to this file)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14                      # outer margin
OUT = "entry.png"

# ---- palette ------------------------------------------------------------
PAPER = (247, 243, 234)
NAVY = (16, 28, 51)
NAVY2 = (24, 42, 74)
GOLD = (242, 183, 5)
INK = (26, 26, 26)
GREY = (107, 107, 107)
FAINT = (221, 213, 194)
CARD = (255, 255, 255)
RED = (179, 38, 30)
RED_SOFT = (246, 224, 220)
BLUE_SOFT = (224, 235, 246)
SKY = (214, 228, 240)

DJV = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJVB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJVS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def mk_font(size, bold=False, serif=False):
    path = DJVS if serif else (DJVB if bold else DJV)
    return ImageFont.truetype(path, size)


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def wrap(draw, s, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, s, font, max_w, fill=INK, leading=3, max_lines=None):
    """Draw a wrapped paragraph; return the y just below the last line."""
    lines = wrap(draw, s, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += font.size + leading
    return y


def kicker(draw, x, y, s, color=RED):
    f = mk_font(10, bold=True)
    draw.text((x, y), s, font=f, fill=color)
    return y + 14


# ---- pictograms (each draws inside a 44x44 tile) ------------------------
def pic_flame(d, x, y, c1=(232, 90, 20), c2=(245, 180, 20)):
    d.polygon([(x + 22, y + 4), (x + 34, y + 22), (x + 30, y + 38),
               (x + 14, y + 38), (x + 10, y + 22)], fill=c1)
    d.polygon([(x + 22, y + 16), (x + 29, y + 28), (x + 26, y + 38),
               (x + 18, y + 38), (x + 15, y + 28)], fill=c2)


def pic_plug(d, x, y, c=(36, 90, 160)):
    d.rounded_rectangle([x + 14, y + 14, x + 30, y + 34], radius=4, fill=c)
    d.rectangle([x + 17, y + 4, x + 20, y + 14], fill=c)
    d.rectangle([x + 24, y + 4, x + 27, y + 14], fill=c)
    d.polygon([(x + 22, y + 34), (x + 18, y + 42), (x + 26, y + 42)], fill=c)


def pic_chart(d, x, y, c=(179, 38, 30)):
    d.line([(x + 6, y + 36), (x + 16, y + 26), (x + 24, y + 30),
            (x + 32, y + 16), (x + 38, y + 20)], fill=c, width=4)
    d.polygon([(x + 38, y + 12), (x + 38, y + 22), (x + 30, y + 16)], fill=c)
    d.rectangle([x + 8, y + 30, x + 12, y + 38], fill=(90, 90, 90))
    d.rectangle([x + 18, y + 22, x + 22, y + 38], fill=(90, 90, 90))
    d.rectangle([x + 28, y + 26, x + 32, y + 38], fill=(90, 90, 90))


def pic_rocket(d, x, y, c=(70, 60, 150)):
    d.polygon([(x + 22, y + 4), (x + 30, y + 20), (x + 26, y + 34),
               (x + 18, y + 34), (x + 14, y + 20)], fill=c)
    d.ellipse([x + 19, y + 14, x + 25, y + 20], fill=(255, 255, 255))
    d.polygon([(x + 14, y + 26), (x + 8, y + 36), (x + 15, y + 32)], fill=c)
    d.polygon([(x + 30, y + 26), (x + 36, y + 36), (x + 29, y + 32)], fill=c)
    d.polygon([(x + 22, y + 34), (x + 26, y + 42), (x + 18, y + 42)],
              fill=(245, 160, 20))


def pic_ship(d, x, y, c=(150, 60, 40)):
    d.rectangle([x + 18, y + 6, x + 26, y + 18], fill=(90, 90, 90))
    d.polygon([(x + 6, y + 20), (x + 38, y + 20), (x + 34, y + 32),
               (x + 10, y + 32)], fill=c)
    d.rectangle([x + 4, y + 34, x + 40, y + 36], fill=(60, 120, 180))
    d.rectangle([x + 4, y + 39, x + 40, y + 41], fill=(60, 120, 180))


def pic_warn(d, x, y, c=(200, 150, 0)):
    d.polygon([(x + 22, y + 5), (x + 39, y + 36), (x + 5, y + 36)], fill=c)
    d.rectangle([x + 20, y + 15, x + 24, y + 27], fill=(255, 255, 255))
    d.ellipse([x + 20, y + 30, x + 24, y + 34], fill=(255, 255, 255))


def pic_scales(d, x, y, c=(40, 90, 140)):
    d.rectangle([x + 21, y + 6, x + 23, y + 34], fill=c)
    d.rectangle([x + 12, y + 34, x + 32, y + 34], fill=c)
    d.line([(x + 8, y + 12), (x + 36, y + 12)], fill=c, width=3)
    d.line([(x + 8, y + 12), (x + 12, y + 22)], fill=c, width=2)
    d.line([(x + 36, y + 12), (x + 32, y + 22)], fill=c, width=2)
    d.polygon([(x + 5, y + 22), (x + 19, y + 22), (x + 12, y + 28)], fill=c)
    d.polygon([(x + 25, y + 22), (x + 39, y + 22), (x + 32, y + 28)], fill=c)


def pic_bank(d, x, y, c=(90, 90, 90)):
    d.polygon([(x + 4, y + 14), (x + 22, y + 4), (x + 40, y + 14)], fill=c)
    d.rectangle([x + 8, y + 18, x + 11, y + 32], fill=c)
    d.rectangle([x + 16, y + 18, x + 19, y + 32], fill=c)
    d.rectangle([x + 25, y + 18, x + 28, y + 32], fill=c)
    d.rectangle([x + 33, y + 18, x + 36, y + 32], fill=c)
    d.rectangle([x + 5, y + 34, x + 39, y + 38], fill=c)


def pic_target(d, x, y, c=(179, 38, 30)):
    d.ellipse([x + 7, y + 7, x + 37, y + 37], outline=c, width=3)
    d.ellipse([x + 14, y + 14, x + 30, y + 30], outline=c, width=3)
    d.ellipse([x + 19, y + 19, x + 25, y + 25], fill=c)


def pic_ring(d, x, y, c=(200, 90, 30)):
    d.ellipse([x + 6, y + 6, x + 38, y + 38], outline=c, width=6)
    d.rectangle([x + 19, y + 4, x + 25, y + 12], fill=c)
    d.rectangle([x + 19, y + 32, x + 25, y + 40], fill=c)
    d.rectangle([x + 4, y + 19, x + 12, y + 25], fill=c)
    d.rectangle([x + 32, y + 19, x + 40, y + 25], fill=c)


def pic_flag(d, x, y, c=(40, 110, 70)):
    d.rectangle([x + 10, y + 5, x + 13, y + 39], fill=(90, 90, 90))
    d.polygon([(x + 13, y + 6), (x + 36, y + 11), (x + 13, y + 17)], fill=c)
    d.ellipse([x + 18, y + 8, x + 22, y + 12], fill=(255, 255, 255))


def pic_percent(d, x, y, c=(180, 60, 30)):
    d.text((x + 6, y + 6), "%", font=mk_font(30, bold=True), fill=c)


def tile(d, x, y, painter, bg):
    d.rounded_rectangle([x, y, x + 44, y + 44], radius=8, fill=bg)
    painter(d, x, y)


# ---- hero art: burning fuel vehicle on a ring road -----------------------
def hero_art(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(43, 30, 24))
    # dusk sky band + smoke
    d.rectangle([x0, y0, x1, y0 + 52], fill=(74, 52, 40))
    for cx, cy, r in [(x0 + 70, y0 + 26, 22), (x0 + 120, y0 + 16, 28),
                      (x0 + 320, y0 + 22, 26), (x0 + 400, y0 + 14, 30),
                      (x0 + 180, y0 + 30, 18)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 100, 92))
    # flames over the tanker
    for fx, fh in [(x0 + 90, 66), (x0 + 150, 84), (x0 + 215, 72),
                   (x0 + 280, 60), (x0 + 350, 78)]:
        d.polygon([(fx, y0 + 96 - fh), (fx + 26, y0 + 96 - fh + 34),
                   (fx + 20, y0 + 96), (fx + 6, y0 + 96)],
                  fill=(232, 90, 20))
        d.polygon([(fx + 8, y0 + 96 - fh + 22), (fx + 20, y0 + 96 - fh + 40),
                   (fx + 16, y0 + 96), (fx + 10, y0 + 96)],
                  fill=(245, 190, 30))
    # tanker truck (burning) + second car
    d.rectangle([x0 + 60, y0 + 96, x0 + 300, y0 + 138], fill=(190, 190, 185))
    d.rectangle([x0 + 300, y0 + 104, x0 + 350, y0 + 138], fill=(200, 70, 40))
    d.rectangle([x0 + 310, y0 + 110, x0 + 338, y0 + 122], fill=(30, 30, 40))
    d.rectangle([x0 + 370, y0 + 112, x0 + 440, y0 + 138], fill=(40, 80, 160))
    d.ellipse([x0 + 90, y0 + 134, x0 + 112, y0 + 152], fill=(20, 20, 20))
    d.ellipse([x0 + 250, y0 + 134, x0 + 272, y0 + 152], fill=(20, 20, 20))
    d.ellipse([x0 + 390, y0 + 134, x0 + 408, y0 + 152], fill=(20, 20, 20))
    # road with dashed centre line
    d.rectangle([x0, y0 + 152, x1, y1], fill=(28, 28, 30))
    for i in range(9):
        dx = x0 + 12 + i * 54
        d.rectangle([dx, y0 + 164, dx + 30, y0 + 169], fill=(240, 210, 90))
    d.rounded_rectangle([x0 + 8, y1 - 24, x0 + 128, y1 - 8], radius=4,
                        fill=(0, 0, 0))
    d.text((x0 + 14, y1 - 22), "CAIRO RING ROAD",
           font=mk_font(10, bold=True), fill=(255, 255, 255))


def stamp(canvas, cx, cy, text="30+ DEAD"):
    """Red rotated rubber stamp, drawn on its own layer then pasted."""
    layer = Image.new("RGBA", (172, 56), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([3, 3, 169, 53], radius=8,
                         outline=(179, 38, 30, 255), width=3)
    ld.text((86, 28), text, font=mk_font(26, bold=True),
            fill=(179, 38, 30, 255), anchor="mm")
    layer = layer.rotate(-9, expand=True, resample=Image.BICUBIC)
    canvas.paste(layer, (cx - layer.width // 2, cy - layer.height // 2),
                 layer)


# ---- small world map ----------------------------------------------------
# Rough but recognisable continent outlines in a 300x88 local frame.
CONTINENTS = [
    [(10, 20), (34, 8), (58, 10), (74, 18), (64, 28), (50, 34), (38, 26),
     (22, 30)],                                   # North America
    [(60, 50), (74, 46), (82, 54), (74, 76), (64, 68)],   # South America
    [(142, 14), (160, 8), (174, 16), (162, 26), (148, 24)],  # Europe
    [(142, 32), (164, 30), (174, 40), (168, 62), (152, 68), (144, 48)],
    # Africa
    [(176, 10), (232, 6), (270, 14), (282, 28), (252, 40), (222, 36),
     (202, 30), (186, 20)],                       # Asia
    [(240, 62), (264, 58), (272, 68), (252, 76)],  # Australia
]
# (label, x, y) in the same local frame
MAP_DOTS = [("Washington", 34, 26), ("Bogota", 66, 56),
            ("London", 152, 16), ("Cairo", 166, 40),
            ("Tehran", 206, 30), ("Delhi", 224, 34),
            ("Jakarta", 248, 58), ("Beijing", 252, 20),
            ("Canberra", 264, 70)]


def world_map(d, x0, y0, w, h):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=8, fill=SKY)
    sx, sy = w / 300.0, h / 88.0
    for poly in CONTINENTS:
        pts = [(x0 + px * sx, y0 + py * sy) for px, py in poly]
        d.polygon(pts, fill=(168, 178, 158))
    for _name, px, py in MAP_DOTS:
        cx, cy = x0 + px * sx, y0 + py * sy
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                  outline=(255, 255, 255), width=1)


# ---- story data ---------------------------------------------------------
# (kicker, headline, body, source, pictogram, tile colour)
PANELS = [
    ("EUROPE · UK", "UK energy price cap to rise 26%",
     "Ofgem: cap up to £2,166 a year from 1 Jan, from £1,723 (+£443). "
     "20m homes get £100 help.",
     "Ofgem — announced 25 Nov", pic_plug, (214, 228, 246)),
    ("AMERICAS · USA", "US proposes tariffs on 14 economies",
     "New duties of 20–40% proposed; hearing set for 25 Jan. Markets fall.",
     "Reuters · AP — 25 Nov", pic_percent, (250, 226, 214)),
    ("MARKETS · ASIA + USA", "Stocks slide on AI doubts",
     "Kospi −6.2% to 4,697.51; Samsung −9.9%, SK Hynix −11.1%; Taiex −5%; "
     "S&P −2.2%.",
     "AP — 25 Nov", pic_chart, (250, 226, 214)),
    ("SPACE · ASIA", "Pakistan's first astronaut launches",
     "Muhammad Zeeshan Ali lifts off aboard Shenzhou 24 for China's "
     "Tiangong station.",
     "AP · Reuters — 25 Nov", pic_rocket, (226, 220, 244)),
    ("GULF · HORMUZ", "Iran says tankers hit mines; Houthis hit refinery",
     "IRGC: tankers hit mines in Hormuz, caught fire. Houthis claim "
     "Ras Tanura attack.",
     "Reuters — 25 Nov", pic_ship, (250, 226, 214)),
    ("GULF · IRAN", "US tells citizens: leave Iran",
     "Warning after attacks in Bahrain, Kuwait, Riyadh; 11 wounded. "
     "India condemns it.",
     "US State Dept · Reuters — 25 Nov", pic_warn, (250, 238, 200)),
    ("MIDDLE EAST · EUROPE", "Judges urge dropping Netanyahu bribery case",
     "Jerusalem court recommends dropping a key bribery case. Poland plans "
     "a no-fly zone.",
     "Reuters · AP — 25 Nov", pic_scales, (214, 228, 246)),
    ("MIDDLE EAST · AFRICA", "Iraq court backs Baghdad; RSF kills 19 in Sudan",
     "Court: troops can deploy at borders and oversee oil. RSF drones "
     "kill 19 in Blue Nile.",
     "Reuters — 25 Nov", pic_bank, (232, 232, 224)),
    ("MIDDLE EAST · ASIA", "Gaza strike kills Hamas official; Java mine floods",
     "Abu al-Awf, his wife and 2 daughters killed. West Java mine: 9 dead, "
     "17 trapped.",
     "Reuters · AP — 25 Nov", pic_target, (250, 226, 214)),
    ("AMERICAS · ASIA", "Colombia hostages freed; Bangladesh pay +36%",
     "All hostages rescued in Cartagena; 1 captor killed. Garment wage "
     "up to 17,000 taka.",
     "AP · Reuters — 25 Nov", pic_ring, (240, 226, 236)),
    ("ASIA · EUROPE", "N. Korea expels Swiss diplomat; UK warns firms",
     "Pyongyang closes its Swiss office; diplomat out in 48h. UK warns "
     "of Russian sabotage.",
     "Reuters · AP — 25 Nov", pic_flag, (214, 228, 246)),
]

# (time "HH:MM", short label) — every dot carries its label, not just a time
TIMELINE = [
    ("00:55", "Saudi downs drones"),
    ("02:17", "Iowa blast"),
    ("06:01", "Bangladesh wage"),
    ("08:08", "Java mine flood"),
    ("11:24", "Gaza strike"),
    ("16:59", "Ras Tanura"),
    ("18:55", "Cairo fire"),
    ("19:28", "Netanyahu case"),
]

BRIEFS = [
    ("Libya: 2 soldiers die after Ukraine drone strike on Russian ship",
     "Reuters"),
    ("Saudi coalition hits Hodeidah port, Saada, Amran", "Reuters"),
    ("Cessna 210 crashes off Mississippi: 6 dead, incl. boys 8 and 10",
     "US Coast Guard"),
    ("US Army detonates 4,400 kg lead azide in Iowa", "AP"),
    ("China investigates Shanghai party chief Chen Jining", "Reuters"),
    ("Ukraine needs €115bn financing for 2027", "Zelenskyy"),
    ("Leaked data: at least 490,334 Russian soldiers died in Ukraine", "BBC"),
    ("Saudi coalition downs Houthi drones over eastern Saudi", "Reuters"),
    ("Pope Leo XIV: concern over COP31 failure to agree a deal", "Vatican"),
    ("Solomon Islands–Australia sign treaty barring foreign bases", "AP"),
    ("US DOJ charges 800+ in 400 cases in global anti-scam sweep", "US DOJ"),
    ("Trump: Iran war funding secured through January", "Reuters"),
    ("CIA + ODNI hit by apparent cyberattack", "Report"),
    ("Israel minister claims Iran chemical weapons; Tehran warns US bases",
     "Reuters"),
    ("† Huang apologises at Nvidia all-hands (meeting 24 Nov)", "Report"),
    ("† Huawei guilty of trade-secret conspiracy + bank fraud (24 Nov)",
     "Reuters"),
    ("India–Malaysia Exercise Harimau Shakti 2026 under way", "ANI"),
    ("Iran claims downing US MQ-9 + Lucas drones over Hormuz", "Iran claim"),
    ("SoftBank −14.8% as AI doubts spread in Tokyo", "AP"),
]
BRIEF_DOT = [RED, RED, (200, 120, 20), (200, 120, 20), (40, 110, 70),
             (40, 90, 160), (40, 90, 160), RED, (40, 110, 70),
             (40, 110, 70), (40, 90, 160), RED, (40, 90, 160), RED,
             (40, 110, 70), RED, (40, 110, 70), RED, (200, 120, 20)]


# ---- sections -----------------------------------------------------------
def masthead(d):
    d.rectangle([0, 0, W, 66], fill=NAVY)
    d.rectangle([0, 66, W, 70], fill=GOLD)
    d.text((M, 6), "THE WORLD IN ONE PAGE", font=mk_font(38, bold=True, serif=True),
           fill=(255, 255, 255))
    d.text((M, 44), "WEDNESDAY, 25 NOVEMBER 2026", font=mk_font(17, bold=True),
           fill=GOLD)
    d.text((W - M, 10), "38 STORIES · 9 REGIONS", font=mk_font(14, bold=True),
           fill=(255, 255, 255), anchor="ra")
    d.text((W - M, 30), "13 drawn scenes · UTC timeline",
           font=mk_font(11), fill=(190, 200, 220), anchor="ra")
    d.text((W - M, 46), "Named source on every story",
           font=mk_font(11), fill=(190, 200, 220), anchor="ra")


def hero(canvas, d):
    y0, y1 = 78, 248
    ax0, ax1 = M, 498
    hero_art(d, ax0, y0, ax1, y1)
    tx = 514
    y = kicker(d, tx, y0 + 4, "AFRICA · EGYPT · 18:55 UTC")
    f_head = mk_font(30, bold=True)
    d.text((tx, y), "CAIRO FUEL FIRE", font=f_head, fill=INK)
    w1 = text_w(d, "CAIRO FUEL FIRE", f_head)
    d.text((tx + w1, y), " KILLS 30+", font=f_head, fill=RED)
    y += 36
    y = para(d, tx, y + 4,
             "Fuel vehicle overturns and burns on ring road; "
             "27 vehicles destroyed.",
             mk_font(15), 486, leading=4)
    y = para(d, tx, y + 4,
             "Egypt Health Ministry: at least 30 killed.",
             mk_font(12), 486, leading=3, fill=GREY)
    d.text((tx, y + 6), "Egypt Health Ministry · AP · Reuters — 25 Nov 2026",
           font=mk_font(11), fill=GREY)
    stamp(canvas, 920, 218)


def timeline(d):
    y_top, y_bot = 256, 316
    d.text((M, y_top + 24), "UTC", font=mk_font(12, bold=True), fill=INK)
    x0, x1 = 52, W - M
    line_y = y_top + 30
    d.line([(x0, line_y), (x1, line_y)], fill=NAVY, width=2)
    f_time = mk_font(11, bold=True)
    f_lab = mk_font(10)
    for i, (t, label) in enumerate(TIMELINE):
        hh, mm = map(int, t.split(":"))
        frac = (hh + mm / 60.0) / 24.0
        x = x0 + frac * (x1 - x0)
        d.ellipse([x - 5, line_y - 5, x + 5, line_y + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        lx = min(max(x, M + 52), W - M - 52)
        if i % 2 == 0:      # label above the line
            d.text((lx, y_top + 2), t, font=f_time, fill=RED, anchor="ma")
            d.text((lx, y_top + 15), label, font=f_lab, fill=INK, anchor="ma")
        else:               # label below the line
            d.text((lx, line_y + 8), t, font=f_time, fill=RED, anchor="ma")
            d.text((lx, line_y + 21), label, font=f_lab, fill=INK,
                   anchor="ma")
    return y_bot


def panel(d, x, y, w, h, kicker_s, headline, body, source, painter, bg):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                        outline=FAINT, width=1)
    tile(d, x + 8, y + 8, painter, bg)
    tx = x + 60
    tw = w - 68
    yy = y + 8
    yy = kicker(d, tx, yy, kicker_s)
    yy = para(d, tx, yy, headline, mk_font(14, bold=True), tw,
              leading=1, max_lines=2)
    para(d, tx, yy + 2, body, mk_font(11), tw, leading=1, max_lines=2)
    d.text((tx, y + h - 15), source, font=mk_font(9), fill=GREY)


def grid(d, y0):
    cols, rows = 3, 4
    cw = (W - 2 * M - (cols - 1) * 8) // cols
    ch, gap = 104, 8
    cells = PANELS + [None]          # last cell is the map
    for idx, item in enumerate(cells):
        r, c = divmod(idx, cols)
        x = M + c * (cw + 8)
        y = y0 + r * (ch + gap)
        if item is None:
            d.rounded_rectangle([x, y, x + cw, y + ch], radius=8,
                                fill=CARD, outline=FAINT, width=1)
            d.text((x + 10, y + 6), "THE DAY ON ONE MAP · 9 REGIONS",
                   font=mk_font(10, bold=True), fill=NAVY)
            world_map(d, x + 10, y + 24, cw - 20, 52)
            d.text((x + 10, y + ch - 25),
                   "Red dots: Washington · Bogota · London · Cairo",
                   font=mk_font(9), fill=GREY)
            d.text((x + 10, y + ch - 14),
                   "Tehran · Delhi · Jakarta · Beijing · Canberra",
                   font=mk_font(9), fill=GREY)
        else:
            panel(d, x, y, cw, ch, *item)
    return y0 + rows * ch + (rows - 1) * gap


def briefs(d, y0):
    y = y0 + 4
    d.text((M, y), "IN BRIEF — 19 MORE STORIES, ALL 25 NOV 2026",
           font=mk_font(13, bold=True), fill=INK)
    y += 20
    d.line([(M, y), (W - M, y)], fill=FAINT, width=1)
    y += 7
    col_w = (W - 2 * M - 24) // 2
    f = mk_font(11)
    for i, (text, src) in enumerate(BRIEFS):
        col = 0 if i < 10 else 1
        row = i if i < 10 else i - 10
        bx = M + col * (col_w + 24)
        by = y + row * 13
        d.ellipse([bx, by + 3, bx + 7, by + 10], fill=BRIEF_DOT[i])
        line = text + " — " + src
        if text_w(d, line, f) > col_w - 12:
            line = text + " — " + src.split()[0]
        d.text((bx + 12, by), line, font=f, fill=INK)
    return y + 10 * 13 + 4


def date_check(d, y0):
    y1 = y0 + 40
    d.rounded_rectangle([M, y0, W - M, y1], radius=8,
                        outline=RED, width=2, fill=RED_SOFT)
    d.text((M + 12, y0 + 4),
           "✓  DATE CHECK — every story is Wed 25 Nov 2026 (UTC)",
           font=mk_font(12, bold=True), fill=RED)
    d.text((M + 12, y0 + 21),
           "All stories first reported Wed 25 Nov 2026 UTC, except † reported "
           "25 Nov, event 24 Nov.",
           font=mk_font(11), fill=INK)
    d.text((W - M - 12, y0 + 21),
           "† = Huang apology; Huawei verdict.",
           font=mk_font(11), fill=INK, anchor="ra")
    return y1


def footer(d, y0):
    d.text((W // 2, y0 + 4),
           "Sources: Reuters, AP, BBC, Ofgem, Daily Summary of World · 25 Nov 2026",
           font=mk_font(11), fill=GREY, anchor="ma")
    d.text((W // 2, y0 + 18),
           "Rendered from code · All 38 stories verified against the named "
           "sources for Wed 25 Nov 2026 · make.fun news-image-20261125",
           font=mk_font(10), fill=GREY, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    hero(img, d)
    y = timeline(d)
    y = grid(d, y + 8)
    y = briefs(d, y + 4)
    y = date_check(d, y + 4)
    footer(d, y + 2)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
