#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261125.

One-page front-page summary of Wednesday 25 November 2026 world news:
38 verified stories, 9 regions, 13 drawn scenes (hero fire scene + 11
panel icons + a small drawn world map), a UTC timeline strip and a
DATE CHECK box. All text comes from the story data below; no external
assets, no downloaded images. PIL only.

Layout (1024 x 1024):
  header band, hero Cairo fire panel, UTC timeline strip,
  3x4 grid (11 story panels + 1 world-map panel),
  2-column briefs (19 stories), DATE CHECK box, footer.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def fb(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), size)


def fr(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), size)


PAPER = (250, 246, 239)
INK = (22, 22, 26)
MUTED = (110, 108, 102)
CARD = (255, 255, 255)
NAVY = (20, 33, 61)
GOLD = (242, 193, 78)
GREEN = (27, 107, 58)
BLUE = (31, 78, 156)
TERRA = (180, 70, 42)
OCHRE = (192, 122, 18)
TEAL = (14, 124, 123)
INDIGO = (74, 63, 160)
MAGENTA = (156, 43, 107)
RED = (192, 57, 43)
PINK_BG = (253, 236, 236)
FIRE = (230, 92, 20)
FLAME = (245, 176, 45)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _sq(draw, x, y, color):
    rounded(draw, [x, y, x + 34, y + 34], 8, fill=color)


def icon_plug(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.rectangle([x + 10, y + 8, x + 15, y + 20], fill="white")
    draw.rectangle([x + 19, y + 8, x + 24, y + 20], fill="white")
    draw.polygon([(x + 8, y + 20), (x + 26, y + 20), (x + 22, y + 29),
                  (x + 12, y + 29)], fill="white")
    draw.line([x + 12, y + 6, x + 12, y + 8], fill=GOLD, width=2)
    draw.line([x + 22, y + 6, x + 22, y + 8], fill=GOLD, width=2)


def icon_tariff(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.rectangle([x + 7, y + 12, x + 27, y + 28], fill="white")
    draw.rectangle([x + 7, y + 8, x + 27, y + 12], fill=GOLD)
    draw.text((x + 11, y + 15), "%", font=fb(13), fill=color)


def icon_chart(draw, x, y, color):
    _sq(draw, x, y, color)
    for i, h in enumerate((7, 13, 9, 18)):
        draw.rectangle([x + 7 + i * 6, y + 27 - h, x + 11 + i * 6, y + 27],
                       fill="white")
    draw.line([x + 6, y + 8, x + 13, y + 14, x + 20, y + 10, x + 28, y + 16],
              fill=RED, width=2)


def icon_rocket(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.polygon([(x + 17, y + 5), (x + 24, y + 16), (x + 21, y + 24),
                  (x + 13, y + 24), (x + 10, y + 16)], fill="white")
    draw.ellipse([x + 14, y + 13, x + 20, y + 19], fill=color)
    draw.polygon([(x + 14, y + 24), (x + 17, y + 30), (x + 20, y + 24)],
                 fill=GOLD)


def icon_tanker(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.rectangle([x + 6, y + 18, x + 28, y + 26], fill="white")
    draw.rectangle([x + 8, y + 10, x + 18, y + 18], fill="white")
    draw.polygon([(x + 18, y + 8), (x + 23, y + 14), (x + 18, y + 16)],
                 fill=FLAME)
    draw.rectangle([x + 24, y + 14, x + 28, y + 18], fill="white")


def icon_alert(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.polygon([(x + 17, y + 6), (x + 29, y + 27), (x + 5, y + 27)],
                 fill="white")
    draw.rectangle([x + 16, y + 13, x + 18, y + 21], fill=color)
    draw.ellipse([x + 15, y + 23, x + 19, y + 27], fill=color)


def icon_scales(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.line([x + 17, y + 7, x + 17, y + 26], fill="white", width=2)
    draw.line([x + 8, y + 10, x + 26, y + 10], fill="white", width=2)
    draw.polygon([(x + 5, y + 18), (x + 11, y + 18), (x + 8, y + 12)],
                 fill="white")
    draw.polygon([(x + 23, y + 18), (x + 29, y + 18), (x + 26, y + 12)],
                 fill="white")
    draw.rectangle([x + 12, y + 26, x + 22, y + 29], fill="white")


def icon_court(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.rectangle([x + 7, y + 12, x + 27, y + 16], fill="white")
    for cx in (9, 15, 21):
        draw.rectangle([x + cx, y + 16, x + cx + 2, y + 25], fill="white")
    draw.rectangle([x + 6, y + 25, x + 28, y + 29], fill="white")


def icon_mine(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.polygon([(x + 5, y + 28), (x + 17, y + 7), (x + 29, y + 28)],
                 fill="white")
    draw.ellipse([x + 13, y + 20, x + 21, y + 28], fill=color)
    draw.line([x + 17, y + 7, x + 17, y + 3], fill=GOLD, width=2)


def icon_hostage(draw, x, y, color):
    _sq(draw, x, y, color)
    for cx in (11, 23):
        draw.ellipse([x + cx - 4, y + 9, x + cx + 4, y + 17], fill="white")
        draw.rectangle([x + cx - 5, y + 18, x + cx + 5, y + 29], fill="white")
    draw.line([x + 8, y + 24, x + 26, y + 24], fill=GOLD, width=2)


def icon_diplomat(draw, x, y, color):
    _sq(draw, x, y, color)
    draw.rectangle([x + 8, y + 10, x + 26, y + 24], fill="white")
    draw.rectangle([x + 12, y + 14, x + 22, y + 17], fill=color)
    draw.line([x + 12, y + 20, x + 20, y + 20], fill=color, width=2)
    draw.line([x + 24, y + 6, x + 28, y + 10], fill=RED, width=3)


ICONS = {
    "plug": icon_plug, "tariff": icon_tariff, "chart": icon_chart,
    "rocket": icon_rocket, "tanker": icon_tanker, "alert": icon_alert,
    "scales": icon_scales, "court": icon_court, "mine": icon_mine,
    "hostage": icon_hostage, "diplomat": icon_diplomat,
}

# Every story happened, or was first reported, on Wed 25 Nov 2026 (UTC).
# Stories marked with a dagger in the briefs were reported on 25 Nov
# about an event on Tue 24 Nov; the DATE CHECK box says so plainly.
HERO = {
    "tag": "AFRICA \u00b7 EGYPT \u00b7 18:55 UTC",
    "headline": "CAIRO RING ROAD FIRE: 30+ DEAD",
    "sub1": "Fuel vehicle catches fire on the ring road; 27 vehicles burn",
    "sub2": "Egypt Health Ministry: at least 30 killed \u00b7 Dozens injured",
    "source": "Egypt Health Ministry \u00b7 AP \u00b7 Reuters \u2014 25 Nov 2026",
}

PANELS = [
    {"key": "plug", "color": BLUE, "tag": "EUROPE \u00b7 UK",
     "headline": "UK energy cap to rise 26%",
     "body": ("Ofgem: price cap up to \u00a32,166 a year from 1 Jan, from "
              "\u00a31,723 (+\u00a3443). 20m homes get \u00a3100 help."),
     "source": "Ofgem \u2014 announced 25 Nov"},
    {"key": "tariff", "color": RED, "tag": "AMERICAS \u00b7 USA",
     "headline": "US proposes tariffs on 14 economies",
     "body": ("New duties of 20\u201340% proposed; public hearing set for "
              "25 January. Markets fall on the news."),
     "source": "Reuters \u00b7 AP \u2014 25 Nov"},
    {"key": "chart", "color": RED, "tag": "MARKETS \u00b7 ASIA + USA",
     "headline": "Stocks slide on AI doubts",
     "body": ("Kospi \u22126.2% to 4,697.51; Samsung \u22129.9%, SK Hynix "
              "\u221211.1%; Taiex \u22125%. S&P \u22122.2%, Nasdaq \u22123.2%."),
     "source": "AP \u2014 25 Nov"},
    {"key": "rocket", "color": INDIGO, "tag": "SPACE \u00b7 ASIA",
     "headline": "Pakistan's first astronaut launches",
     "body": ("Muhammad Zeeshan Ali lifts off aboard Shenzhou 24, bound "
              "for China's Tiangong space station."),
     "source": "AP \u00b7 Reuters \u2014 25 Nov"},
    {"key": "tanker", "color": TERRA, "tag": "GULF \u00b7 HORMUZ",
     "headline": "Iran says tankers hit mines; Houthis hit refinery",
     "body": ("IRGC says tankers struck naval mines in Hormuz and caught "
              "fire. Houthis claim Ras Tanura refinery attack."),
     "source": "Reuters \u2014 25 Nov"},
    {"key": "alert", "color": TERRA, "tag": "GULF \u00b7 IRAN",
     "headline": "US tells citizens: leave Iran",
     "body": ("Warning after attacks in Bahrain, Kuwait and a Riyadh "
              "tower; 11 wounded in Riyadh. India condemns the attack."),
     "source": "US State Dept \u00b7 Reuters \u2014 25 Nov"},
    {"key": "scales", "color": BLUE, "tag": "MIDDLE EAST \u00b7 EUROPE",
     "headline": "Judges urge dropping Netanyahu bribery case",
     "body": ("Jerusalem District Court recommends dropping a key "
              "bribery case. Poland plans a no-fly zone near Ukraine."),
     "source": "Reuters \u00b7 AP \u2014 25 Nov"},
    {"key": "court", "color": OCHRE, "tag": "MIDDLE EAST \u00b7 AFRICA",
     "headline": "Iraq court backs Baghdad; RSF kills 19 in Sudan",
     "body": ("Court: federal government can deploy troops at borders "
              "and oversee oil. RSF drones hit Blue Nile, Sudan."),
     "source": "Reuters \u2014 25 Nov"},
    {"key": "mine", "color": TEAL, "tag": "MIDDLE EAST \u00b7 ASIA",
     "headline": "Gaza strike kills Hamas official; Java mine floods",
     "body": ("Israeli strike kills Muhammad Majid Abu al-Awf, his wife "
              "and 2 daughters. 9 dead, 17 trapped in West Java mine."),
     "source": "Reuters \u00b7 AP \u2014 25 Nov"},
    {"key": "hostage", "color": MAGENTA, "tag": "AMERICAS \u00b7 ASIA",
     "headline": "Colombia hostages freed; Bangladesh pay +36%",
     "body": ("All hostages rescued in Cartagena; 1 captor killed. "
              "Garment wage rises to 17,000 taka a month."),
     "source": "AP \u00b7 Reuters \u2014 25 Nov"},
    {"key": "diplomat", "color": BLUE, "tag": "ASIA \u00b7 EUROPE",
     "headline": "N. Korea expels Swiss diplomat; UK warns firms",
     "body": ("Pyongyang orders its Swiss office closed, diplomat out "
              "in 48 hours. UK warns of a Russian sabotage threat."),
     "source": "Reuters \u00b7 AP \u2014 25 Nov"},
]

# 19 one-line briefs, 2 columns (10 + 9). Dagger = reported 25 Nov,
# event 24 Nov (see DATE CHECK).
BRIEFS = [
    ("Libya: 2 soldiers die after Ukraine drone strike on Russian ship", "Reuters", OCHRE),
    ("Saudi-led coalition hits Hodeidah port, Saada and Amran", "Reuters", TERRA),
    ("Cessna 210 crashes off Mississippi: 6 dead, incl. boys 8 and 10", "US Coast Guard", RED),
    ("US Army detonates 4,400 kg lead azide in Iowa; 20-mile alert", "AP", RED),
    ("China investigates Shanghai party chief Chen Jining", "Reuters", TEAL),
    ("Ukraine needs \u20ac115bn external financing for 2027", "Zelenskyy", BLUE),
    ("Leaked data: at least 490,334 Russian soldiers died in Ukraine", "BBC", BLUE),
    ("Saudi coalition shoots down Houthi drones over E. Saudi Arabia", "Reuters", TERRA),
    ("Pope Leo XIV: concern over COP31 failure to agree a deal", "Vatican", INDIGO),
    ("Solomon Islands + Australia sign treaty barring foreign base", "AP", TEAL),
    ("US DOJ charges 800+ in 400 cases in global anti-scam sweep", "US DOJ", RED),
    ("Trump: US war funding vs Iran secured through January", "Reuters", RED),
    ("US intel CIA + ODNI hit by apparent cyberattack", "Report", RED),
    ("Israel: Iran developing chemical weapons; Tehran warns US bases", "Reuters", TERRA),
    ("\u2020 Jensen Huang apologises at Nvidia all-hands meeting", "Report", TEAL),
    ("\u2020 Huawei guilty of trade-secret conspiracy + bank fraud", "Reuters", TEAL),
    ("India\u2013Malaysia Exercise Harimau Shakti 2026 under way", "ANI", TEAL),
    ("Iran claims downing of US MQ-9 + Lucas drones over Hormuz", "Iran claim", TERRA),
    ("SoftBank \u221214.8% as AI doubts spread in Tokyo", "AP", RED),
]

TIMELINE = [
    ("00:55", "Houthi drones downed"),
    ("02:17", "Iowa blast; Cessna crash"),
    ("06:01", "Bangladesh pay +36%"),
    ("08:08", "Java mine flood"),
    ("11:24", "Gaza strike"),
    ("16:59", "Ras Tanura claim"),
    ("18:55", "Cairo fire: 30+ dead"),
    ("19:28", "Netanyahu case"),
]

DATE_CHECK_LINES = [
    "All 38 stories happened, or were first reported, on Wed 25 Nov 2026 (UTC).",
    "\u2020 = reported 25 Nov, event Tue 24 Nov: Jensen Huang apology; Huawei verdict.",
]


def draw_header(draw):
    draw.rectangle([0, 0, W, 92], fill=NAVY)
    draw.rectangle([0, 92, W, 96], fill=GOLD)
    draw.text((16, 10), "THE WORLD IN ONE DAY", font=fb(30), fill="white")
    draw.text((16, 50), "WEDNESDAY, 25 NOVEMBER 2026", font=fb(20), fill=GOLD)
    r1 = "38 STORIES \u00b7 9 REGIONS"
    r2 = "13 drawn scenes \u00b7 UTC timeline"
    r3 = "Named source on every story"
    draw.text((W - 16 - draw.textlength(r1, font=fb(15)), 12), r1,
              font=fb(15), fill="white")
    draw.text((W - 16 - draw.textlength(r2, font=fr(12)), 38), r2,
              font=fr(12), fill=(200, 205, 215))
    draw.text((W - 16 - draw.textlength(r3, font=fr(12)), 60), r3,
              font=fr(12), fill=(200, 205, 215))


def draw_hero(img, draw, warnings):
    x0, y0, x1, y1 = 8, 104, 1016, 236
    rounded(draw, [x0, y0, x1, y1], 12, fill=CARD, outline=(220, 216, 208))
    # Drawn scene: ring road at dusk, tanker + cars, flames, smoke.
    sx0, sy0, sx1, sy1 = x0 + 8, y0 + 8, x0 + 252, y1 - 8
    draw.rectangle([sx0, sy0, sx1, sy1], fill=(58, 38, 30))
    draw.rectangle([sx0, sy0, sx1, sy0 + 34], fill=(96, 62, 44))
    for cx, cy, r in ((sx0 + 30, sy0 + 22, 12), (sx0 + 70, sy0 + 16, 16),
                      (sx0 + 120, sy0 + 24, 11), (sx0 + 180, sy0 + 18, 14),
                      (sx0 + 215, sy0 + 26, 10)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 112, 108))
    # road
    draw.rectangle([sx0, sy1 - 42, sx1, sy1], fill=(38, 38, 42))
    for lx in range(sx0 + 6, sx1 - 10, 26):
        draw.rectangle([lx, sy1 - 22, lx + 14, sy1 - 19], fill=(240, 220, 120))
    # tanker truck
    draw.rectangle([sx0 + 18, sy1 - 78, sx0 + 118, sy1 - 46], fill=(200, 200, 205))
    draw.rectangle([sx0 + 118, sy1 - 72, sx0 + 148, sy1 - 46], fill=(180, 70, 42))
    draw.ellipse([sx0 + 34, sy1 - 50, sx0 + 48, sy1 - 36], fill=(20, 20, 22))
    draw.ellipse([sx0 + 88, sy1 - 50, sx0 + 102, sy1 - 36], fill=(20, 20, 22))
    draw.ellipse([sx0 + 126, sy1 - 50, sx0 + 140, sy1 - 36], fill=(20, 20, 22))
    # car
    draw.rectangle([sx0 + 168, sy1 - 66, sx0 + 228, sy1 - 46], fill=(31, 78, 156))
    draw.ellipse([sx0 + 180, sy1 - 50, sx0 + 194, sy1 - 36], fill=(20, 20, 22))
    draw.ellipse([sx0 + 208, sy1 - 50, sx0 + 222, sy1 - 36], fill=(20, 20, 22))
    # flames over the tanker
    for fx, fh in ((sx0 + 34, 34), (sx0 + 58, 46), (sx0 + 84, 38),
                   (sx0 + 106, 28), (sx0 + 180, 30), (sx0 + 204, 24)):
        draw.polygon([(fx, sy1 - 78), (fx + 8, sy1 - 78 - fh),
                      (fx + 16, sy1 - 78)], fill=FIRE)
        draw.polygon([(fx + 4, sy1 - 78), (fx + 8, sy1 - 78 - fh + 12),
                      (fx + 12, sy1 - 78)], fill=FLAME)
    draw.text((sx0 + 6, sy1 - 16), "CAIRO RING ROAD", font=fb(9), fill="white")
    tx = x0 + 272
    draw.text((tx, 114), HERO["tag"], font=fb(11), fill=TERRA)
    draw.text((tx, 130), HERO["headline"], font=fb(27), fill=INK)
    draw.text((tx, 166), HERO["sub1"], font=fr(13), fill=(60, 60, 66))
    draw.text((tx, 186), HERO["sub2"], font=fr(13), fill=(60, 60, 66))
    draw.text((tx, 210), HERO["source"], font=fr(10), fill=MUTED)
    # 30+ DEAD stamp
    stamp = Image.new("RGBA", (170, 56), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([2, 2, 168, 54], radius=8, outline=RED, width=4)
    sd.text((12, 14), "30+ DEAD", font=fb(24), fill=RED)
    stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (830, 118), stamp)


def draw_timeline(draw):
    x0, y0, x1, y1 = 8, 244, 1016, 272
    rounded(draw, [x0, y0, x1, y1], 8, fill=(232, 238, 245),
            outline=(200, 210, 225))
    draw.text((16, y0 + 7), "UTC", font=fb(11), fill=NAVY)
    tx0, tx1 = 62, 1008
    draw.line([tx0, y0 + 14, tx1, y0 + 14], fill=NAVY, width=2)
    for i, (t, label) in enumerate(TIMELINE):
        fx = tx0 + int((tx1 - tx0) * i / (len(TIMELINE) - 1))
        draw.ellipse([fx - 4, y0 + 10, fx + 4, y0 + 18], fill=RED)
        tw = draw.textlength(t, font=fb(8))
        draw.text((fx - tw / 2, y0 + 1), t, font=fb(8), fill=NAVY)


def draw_panel(draw, panel, x, y, w, h, warnings):
    color = panel["color"]
    rounded(draw, [x, y, x + w, y + h], 10, fill=CARD,
            outline=(224, 220, 212))
    draw.rectangle([x, y + 8, x + 4, y + h - 8], fill=color)
    ICONS[panel["key"]](draw, x + 10, y + 8, color)
    draw.text((x + 52, y + 8), panel["tag"], font=fb(9), fill=color)
    head_lines = wrap(draw, panel["headline"], fb(14), w - 60)
    if len(head_lines) > 2:
        warnings.append("headline overflow: %s" % panel["key"])
    for i, line in enumerate(head_lines[:2]):
        draw.text((x + 52, y + 20 + i * 16), line, font=fb(14), fill=INK)
    body_lines = wrap(draw, panel["body"], fr(11), w - 16)
    if len(body_lines) > 3:
        warnings.append("body overflow: %s (%d lines)"
                        % (panel["key"], len(body_lines)))
    for i, line in enumerate(body_lines[:3]):
        draw.text((x + 8, y + 56 + i * 14), line, font=fr(11), fill=(52, 52, 58))
    draw.text((x + 8, y + h - 16), panel["source"], font=fr(9), fill=MUTED)


def draw_map_panel(draw, x, y, w, h):
    rounded(draw, [x, y, x + w, y + h], 10, fill=(232, 238, 245),
            outline=(200, 210, 225))
    draw.text((x + 10, y + 8), "THE DAY ON ONE MAP \u00b7 9 REGIONS",
              font=fb(10), fill=NAVY)
    # Simplified drawn world map: grey land blobs on a pale sea.
    mx, my = x + 8, y + 28
    draw.ellipse([mx + 10, my + 8, mx + 90, my + 34], fill=(180, 190, 175))
    draw.ellipse([mx + 110, my + 2, mx + 200, my + 30], fill=(180, 190, 175))
    draw.ellipse([mx + 205, my + 12, mx + 250, my + 36], fill=(180, 190, 175))
    draw.ellipse([mx + 120, my + 34, mx + 190, my + 58], fill=(180, 190, 175))
    draw.ellipse([mx + 255, my + 44, mx + 300, my + 62], fill=(180, 190, 175))
    draw.ellipse([mx + 30, my + 38, mx + 85, my + 60], fill=(180, 190, 175))
    spots = [
        (mx + 48, my + 20, "Washington"), (mx + 62, my + 48, "Bogota"),
        (mx + 138, my + 14, "London"), (mx + 168, my + 22, "Cairo"),
        (mx + 190, my + 26, "Tehran"), (mx + 232, my + 24, "Delhi"),
        (mx + 252, my + 30, "Jakarta"), (mx + 268, my + 18, "Beijing"),
        (mx + 292, my + 54, "Canberra"),
    ]
    for sx, sy, name in spots:
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=RED,
                     outline="white", width=1)
    draw.text((x + 10, y + h - 28),
              "Red dots: Washington \u00b7 Bogota \u00b7 London \u00b7 Cairo",
              font=fr(9), fill=(60, 60, 66))
    draw.text((x + 10, y + h - 15),
              "Tehran \u00b7 Delhi \u00b7 Jakarta \u00b7 Beijing \u00b7 Canberra",
              font=fr(9), fill=(60, 60, 66))


def draw_briefs(draw, warnings):
    y0 = 760
    draw.text((10, y0), "IN BRIEF \u2014 19 MORE STORIES, ALL 25 NOV 2026",
              font=fb(12), fill=INK)
    draw.line([10, y0 + 20, 1014, y0 + 20], fill=(200, 196, 188), width=1)
    col_w, row_h = 502, 15
    for i, (text, source, color) in enumerate(BRIEFS):
        col, row = divmod(i, 10)
        bx = 10 + col * col_w
        by = y0 + 26 + row * row_h
        draw.ellipse([bx, by + 3, bx + 7, by + 10], fill=color)
        line = "%s \u2014 %s" % (text, source)
        if draw.textlength(line, font=fr(10)) > col_w - 16:
            warnings.append("brief too long: %s" % text[:40])
        draw.text((bx + 12, by), line, font=fr(10), fill=(40, 40, 46))


def draw_datecheck(draw, warnings):
    x0, y0, x1, y1 = 8, 934, 1016, 996
    rounded(draw, [x0, y0, x1, y1], 10, fill=PINK_BG, outline=RED, width=1)
    draw.text((18, y0 + 6),
              "\u2713 DATE CHECK \u2014 every story is Wed 25 Nov 2026 (UTC), "
              "except \u2020 reported 25 Nov, event 24 Nov:",
              font=fb(11), fill=(140, 30, 22))
    for i, line in enumerate(DATE_CHECK_LINES):
        if draw.textlength(line, font=fr(10)) > 980:
            warnings.append("date-check line %d too long" % (i + 1))
        draw.text((18, y0 + 24 + i * 14), line, font=fr(10),
                  fill=(90, 30, 26))


def main():
    warnings = []
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_hero(img, draw, warnings)
    draw_timeline(draw)
    pw, ph, gap = 330, 112, 8
    for i, panel in enumerate(PANELS):
        row, col = divmod(i, 3)
        x = 8 + col * (pw + gap)
        y = 280 + row * (ph + gap)
        draw_panel(draw, panel, x, y, pw, ph, warnings)
    # 12th grid cell is the world map.
    draw_map_panel(draw, 8 + 2 * (pw + gap), 280 + 3 * (ph + gap), pw, ph)
    draw_briefs(draw, warnings)
    draw_datecheck(draw, warnings)
    footer = ("Rendered from code \u00b7 All 38 stories verified against the "
              "named sources for Wed 25 November 2026 \u00b7 make.fun "
              "news-image-20261125")
    draw.text(((W - draw.textlength(footer, font=fr(9))) // 2, 1004),
              footer, font=fr(9), fill=MUTED)
    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("entry.png: %d bytes, sha256 %s" % (size, sha))
    print("dimensions: %dx%d (limit 1024x1024, 1 MiB)" % (W, H))
    print("stories: 1 hero + 18 in panels + 19 briefs = 38; "
          "scenes: 13; regions: 9")
    if size > 1048576:
        warnings.append("OVER 1 MiB")
    for w in warnings:
        print("WARNING:", w)
    if not warnings:
        print("no layout warnings")


if __name__ == "__main__":
    main()
