#!/usr/bin/env python3
"""Saltwater Verdict — one-page visual summary of world news,
Tuesday 24 November 2026. Drawn from scratch with Pillow.
Writes exactly one file: entry.png (1024x1024, deterministic)."""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSerif-Bold.ttf", 33)
F_SUB = font("DejaVuSans.ttf", 15)
F_SUB_B = font("DejaVuSans-Bold.ttf", 15)
F_PANEL = font("DejaVuSans-Bold.ttf", 14)
F_CAP = font("DejaVuSans-Bold.ttf", 14)
F_CAP2 = font("DejaVuSans.ttf", 11)
F_REG = font("DejaVuSans-Bold.ttf", 13)
F_TIME = font("DejaVuSans-Bold.ttf", 12)
F_HEAD = font("DejaVuSans-Bold.ttf", 12)
F_DET = font("DejaVuSans.ttf", 11)
F_SMALL = font("DejaVuSans.ttf", 10)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 10)
F_TL = font("DejaVuSans-Bold.ttf", 11)
F_TL2 = font("DejaVuSans.ttf", 11)

PAPER = (247, 242, 232)
INK = (22, 26, 34)
NAVY = (18, 33, 61)
NAVY2 = (28, 52, 92)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
LINE = (190, 182, 168)
MUTED = (96, 96, 96)

CONFIRMED = (27, 120, 55)
REPORTED = (176, 124, 0)
CLAIMED = (178, 48, 32)

# (utc time, headline, one-line detail, confidence)
# confidence: C = confirmed by officials/courts, R = reported by wires,
# L = claimed by one side, not independently verified.
REGIONS = [
    ("MIDDLE EAST", (179, 64, 42), [
        ("00:00", "FOUR TANKERS HIT MINES IN HORMUZ",
         "Iran says mines struck four tankers; maritime centre: unconfirmed.", "L"),
        ("18:58", "IRGC: WE HIT A CONTAINER SHIP",
         "Revolutionary Guard says vessel sailed dark through a closed lane.", "R"),
        ("14:27", "DRONE HITS RIYADH PIF TOWER, 11 HURT",
         "Houthi strike on finance district tower; second hit in a week.", "C"),
        ("16:51", "HOUTHIS 60 KM FROM ADEN, ARMY WARNS",
         "Yemen military: fighters massed north of the interim capital.", "R"),
        ("10:42", "SAUDI STRIKES IN YEMEN: 25 DEAD/MISSING",
         "Buses and trucks hit in Wadi Maabaq, Lahj; six wounded.", "R"),
        ("11:40", "ISRAEL KILLS HAMAS SECURITY CHIEF",
         "Brig. Gen. Nahel hit in Gaza strike; six more killed Tuesday.", "C"),
    ]),
    ("EUROPE & UKRAINE", (31, 78, 121), [
        ("08:14", "UKRAINE DRONES HIT RUSSIAN SHIPS",
         "Cargo ship Sparta II struck in Gulf of Finland; corvette off Libya.", "C"),
        ("08:14", "POLAND: RUSSIA VIOLATED OUR AIRSPACE",
         "Warsaw accuses Moscow of a deliberate new incursion.", "R"),
        ("00:30", "ZELENSKY: FOUR-WAY TALKS, ASAP",
         "Kyiv ready Tuesday; repeats call for full NATO membership.", "R"),
        ("02:15", "NATO VOWS TO DEFEND SPACE",
         "Rutte: alliance will answer threats after nuclear-satellite reports.", "C"),
        ("24 NOV", "GERMANY FIRST INTO UKRAINE DELTA",
         "Berlin signs access to Kyiv's battlefield management system.", "R"),
        ("12:55", "UK SANCTIONS HOUTHIS, 4 OFFICIALS",
         "Asset freezes, travel bans over Red Sea attacks and abuses.", "C"),
    ]),
    ("ASIA", (123, 94, 0), [
        ("20:41", "HUAWEI GUILTY: TRADE SECRETS, FRAUD",
         "US jury convicts on 10 of 12 counts; racketeering acquitted.", "C"),
        ("02:37", "CHINA: DEATH SENTENCE FOR SPYING",
         "Official 'Ma' sold 35 secrets for over 1m yuan, state press says.", "R"),
        ("24 NOV", "SHENZHOU-24: FIRST FOREIGN ASTRONAUT",
         "Pakistan's Zeeshan Ali joins China crew aboard Tiangong.", "C"),
        ("24 NOV", "SEOUL +6.3%, NIKKEI +3.9% ON HUANG",
         "Asian stocks surge as Nvidia chief returns days after exit talk.", "C"),
        ("24 NOV", "QUAKE 5.6 SHAKES NEPAL BORDER",
         "Tremor strikes near the Chinese border; no toll reported yet.", "C"),
        ("08:16", "HANOI HOTPOT BLAST KILLS AT LEAST 6",
         "Gas leak suspected; packed restaurant, 10+ hurt, rubble searched.", "C"),
    ]),
    ("AMERICAS", (46, 107, 52), [
        ("17:35", "25 HOSTAGES HELD IN CARTAGENA STORE",
         "Gunmen seize a supermarket; five older women freed, troops sent.", "C"),
        ("11:45", "CAR BOMB INJURES 23 IN COLOMBIA",
         "Blast outside regional offices in Villavicencio; narcoterror blamed.", "C"),
        ("02:09", "EL CHAPO ISIDRO CAUGHT, MEXICO TO TRY",
         "US drone aided the Sinaloa capture; 4 soldiers, 16 gunmen dead.", "C"),
        ("01:03", "PENTAGON REBUKES CANADA ON F-35S",
         "US calls Ottawa a weak partner; only 41.9% of its jets flyable.", "R"),
        ("00:52", "US BLACKLISTS MEGASPEED, 6 FIRMS",
         "Nvidia-linked Singapore firm hit over alleged Beijing spy link.", "C"),
        ("01:06", "BUKELE NAMES 3 SOLDIERS LOST IN HAITI",
         "Blast kills Salvadorans on anti-gang mission; families get $200k.", "C"),
    ]),
    ("AFRICA", (108, 52, 131), [
        ("24 NOV", "SENEGAL REGAIN AFCON TITLE",
         "Sports court appeal hands the champions their crown back.", "C"),
        ("08:35", "CONGO PLANE LOST; REBELS CLAIM HIT",
         "Cessna 208 missing in South Kivu; shootdown claim unverified.", "L"),
        ("10:10", "GAZA MENINGITIS ALERT: 272 CASES",
         "October infections 8x normal; 15 dead this year, ministry says.", "C"),
        ("13:45", "HAFTAR VISITS TURKEY FOR FIRST TIME",
         "Libya's eastern commander to meet Erdogan in Ankara.", "C"),
        ("05:54", "MALAYSIA TO RETURN MIGRANTS",
         "Thousands sent back to Myanmar after ICJ genocide ruling.", "R"),
        ("03:00", "ICJ: MYANMAR GUILTY OF GENOCIDE",
         "Court finds state responsible over 2017 Rohingya operations.", "C"),
    ]),
    ("SPORT & THE WORLD", (14, 107, 107), [
        ("03:50", "HASINA PLANS RETURN ON 16 DECEMBER",
         "Exiled ex-PM to fly home for Victory Day; Dhaka wants extradition.", "R"),
        ("02:38", "INDONESIA NAMES TWO VP CANDIDATES",
         "Prabowo picks Amran Sulaiman and Sugiono to replace Gibran.", "C"),
        ("04:14", "KOREA SHELTERS ISLAND AS JETS NEAR",
         "Russian aircraft enter air-defence zone; fighters scrambled.", "C"),
        ("24 NOV", "SARKOZY, BRUNI FACE 2027 TRIAL",
         "Ex-president and wife to stand trial; date set Tuesday.", "R"),
        ("24 NOV", "UCL: REAL 5-1 PSV, ARSENAL 2-2 BVB",
         "Madrid rout; Gunners draw at Dortmund in Champions League.", "C"),
        ("24 NOV", "US SANCTIONS IRAN EXCHANGE HOUSES",
         "Treasury hits 24+ shadow-banking outlets as talks stall.", "R"),
    ]),
]

TIMELINE = [
    ("00:00", "Hormuz: 4 tankers hit mines"),
    ("02:09", "El Chapo Isidro captured"),
    ("08:14", "Ukraine drones hit Sparta II"),
    ("11:40", "Hamas security chief killed"),
    ("14:27", "Riyadh PIF tower struck"),
    ("20:41", "Huawei guilty in US court"),
]

PINS = [  # (lon, lat, label)
    (56, 26, "Hormuz"), (47, 25, "Riyadh"), (31, 50, "Kyiv"),
    (34, 31, "Gaza"), (0, 51, "London"), (116, 40, "Beijing"),
    (127, 37, "Seoul"), (106, 21, "Hanoi"), (-75, 10, "Cartagena"),
    (-99, 19, "Mexico"), (15, -4, "Congo"), (-17, 15, "Dakar"),
    (107, -6, "Jakarta"), (130, 37, "Ulleungdo"),
]


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def conf_color(code):
    return {"C": CONFIRMED, "R": REPORTED, "L": CLAIMED}[code]


def dot(draw, x, y, r, color):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color)


def scene_hormuz(d, x, y, w, h):
    """Dusk strait: tanker, flames, drifting mines."""
    d.rectangle([x, y, x + w, y + h], fill=(23, 52, 84))
    d.rectangle([x, y, x + w, y + 34], fill=(233, 150, 66))
    d.ellipse([x + w - 66, y + 8, x + w - 26, y + 48], fill=(244, 196, 120))
    d.rectangle([x, y + 62, x + w, y + h], fill=(16, 74, 110))
    for i in range(5):
        wx = x + 12 + i * 64
        d.arc([wx, y + 74, wx + 56, y + 92], 0, 180, fill=(120, 170, 205), width=2)
    # tanker hull and bridge
    d.rectangle([x + 30, y + 78, x + 218, y + 104], fill=(24, 24, 28))
    d.rectangle([x + 178, y + 58, x + 212, y + 78], fill=(230, 230, 225))
    d.rectangle([x + 186, y + 44, x + 196, y + 58], fill=(200, 60, 40))
    for cx in (60, 100, 140):
        d.rectangle([x + cx, y + 66, x + cx + 14, y + 78], fill=(240, 120, 60))
    # flames licking the deck
    for fx, fh in ((52, 26), (84, 34), (118, 22), (152, 30)):
        d.polygon([(x + fx, y + 80), (x + fx + 9, y + 80 - fh),
                   (x + fx + 18, y + 80)], fill=(245, 130, 32))
        d.polygon([(x + fx + 4, y + 80), (x + fx + 9, y + 80 - fh + 12),
                   (x + fx + 14, y + 80)], fill=(250, 205, 60))
    # mines
    for mx, my in ((252, 96), (286, 108), (238, 118)):
        dot(d, x + mx, y + my, 5, (40, 40, 40))
        for ang in range(0, 360, 45):
            import math
            dx = 7 * math.cos(math.radians(ang))
            dy = 7 * math.sin(math.radians(ang))
            d.line([x + mx, y + my, x + mx + dx, y + my + dy],
                   fill=(40, 40, 40), width=2)
    d.text((x + 10, y + h - 20), "STRAIT OF HORMUZ  00:00 UTC",
           font=F_SMALL_B, fill=(255, 255, 255))


def scene_court(d, x, y, w, h):
    """Courtroom: columns, gavel, verdict ribbon."""
    d.rectangle([x, y, x + w, y + h], fill=(242, 232, 214))
    d.rectangle([x, y, x + w, y + 26], fill=(18, 33, 61))
    d.text((x + 12, y + 5), "NEW YORK  •  FEDERAL COURT", font=F_SMALL_B,
           fill=(255, 255, 255))
    for cx in (28, 76, 228, 276):
        d.rectangle([x + cx, y + 34, x + cx + 18, y + 96], fill=(190, 178, 152))
        d.rectangle([x + cx - 4, y + 30, x + cx + 22, y + 38], fill=(150, 136, 108))
        d.rectangle([x + cx - 4, y + 94, x + cx + 22, y + 100], fill=(150, 136, 108))
    # bench
    d.rectangle([x + 108, y + 52, x + 212, y + 100], fill=(96, 66, 40))
    d.rectangle([x + 108, y + 52, x + 212, y + 60], fill=(122, 86, 52))
    # gavel: light wood so it reads against the dark bench
    d.rectangle([x + 128, y + 66, x + 176, y + 80], fill=(176, 122, 62))
    d.rectangle([x + 128, y + 66, x + 176, y + 80], outline=(90, 58, 30), width=1)
    d.line([x + 176, y + 73, x + 206, y + 60], fill=(140, 96, 48), width=6)
    d.rectangle([x + 138, y + 84, x + 168, y + 90], fill=(120, 82, 44))
    # verdict ribbon
    d.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 6], fill=(178, 48, 32))
    d.text((x + 16, y + h - 24), "GUILTY  •  10 OF 12 COUNTS", font=F_SMALL_B,
           fill=(255, 255, 255))


def scene_ship(d, x, y, w, h):
    """Night sea: grey cargo ship, drone, blast star."""
    d.rectangle([x, y, x + w, y + h], fill=(14, 34, 58))
    for sx, sy, sr in ((40, 16, 2), (120, 10, 1), (200, 22, 2), (280, 12, 1),
                       (90, 28, 1), (250, 30, 2)):
        dot(d, x + sx, y + sy, sr, (220, 225, 235))
    d.rectangle([x, y + 66, x + w, y + h], fill=(22, 68, 104))
    for i in range(4):
        wx = x + 20 + i * 78
        d.arc([wx, y + 76, wx + 60, y + 94], 0, 180, fill=(130, 175, 210), width=2)
    # cargo ship
    d.rectangle([x + 48, y + 82, x + 232, y + 106], fill=(120, 124, 128))
    d.rectangle([x + 196, y + 60, x + 226, y + 82], fill=(150, 154, 158))
    for cx in (70, 110, 150):
        d.rectangle([x + cx, y + 70, x + cx + 26, y + 82], fill=(200, 80, 50))
    d.text((x + 58, y + 84), "SPARTA II", font=F_SMALL_B, fill=(255, 255, 255))
    # blast star
    bx, by = x + 262, y + 52
    pts = []
    import math
    for k in range(16):
        r = 26 if k % 2 == 0 else 10
        a = math.radians(k * 22.5 - 90)
        pts.append((bx + r * math.cos(a), by + r * math.sin(a)))
    d.polygon(pts, fill=(250, 190, 40))
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 240, 160))
    # drone
    dx, dy = x + 108, y + 34
    d.line([dx - 14, dy - 8, dx + 14, dy + 8], fill=(200, 200, 200), width=2)
    d.line([dx - 14, dy + 8, dx + 14, dy - 8], fill=(200, 200, 200), width=2)
    d.rectangle([dx - 7, dy - 5, dx + 7, dy + 5], fill=(60, 60, 64))
    dot(d, dx - 16, dy - 10, 4, (180, 180, 180))
    dot(d, dx + 16, dy - 10, 4, (180, 180, 180))
    d.text((x + 10, y + h - 20), "GULF OF FINLAND  08:14 UTC",
           font=F_SMALL_B, fill=(255, 255, 255))


def draw_map(d, x, y, w, h):
    """Rough equirectangular world sketch with story pins."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 240))
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)

    def px(lon, lat):
        return (x + 8 + (lon + 180) / 360.0 * (w - 16),
                y + 6 + (90 - lat) / 180.0 * (h - 12))

    def land(points, fill):
        d.polygon([px(lo, la) for lo, la in points], fill=fill)

    sand = (196, 178, 138)
    land([(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 66), (-82, 62),
          (-76, 45), (-70, 42), (-80, 32), (-84, 30), (-97, 26), (-105, 20),
          (-117, 33), (-125, 40), (-140, 60), (-158, 58), (-168, 66)], sand)
    land([(-78, 10), (-60, 5), (-50, 0), (-40, -8), (-48, -20), (-58, -34),
          (-70, -40), (-73, -50), (-70, -20), (-80, -5), (-78, 10)], sand)
    land([(-10, 36), (0, 43), (10, 55), (18, 58), (28, 60), (30, 55),
          (23, 40), (19, 42), (12, 44), (3, 43), (-2, 37), (-10, 36)], sand)
    land([(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
          (51, 11), (48, -2), (40, -12), (32, -26), (20, -35), (12, -18),
          (9, -2), (-8, 4), (-16, 12), (-17, 15), (-10, 30), (-6, 35)], sand)
    land([(-10, 70), (20, 70), (40, 68), (60, 70), (90, 75), (120, 73),
          (140, 72), (160, 66), (180, 66), (162, 60), (140, 40), (127, 40),
          (122, 30), (110, 20), (105, 8), (100, 6), (95, 15), (90, 22),
          (80, 8), (72, 20), (60, 25), (50, 29), (43, 12), (35, 28),
          (30, 36), (23, 36), (19, 42), (10, 44), (-10, 70)], sand)
    # Australia
    land([(114, -22), (122, -14), (132, -12), (142, -11), (150, -23),
          (153, -27), (150, -37), (140, -38), (130, -32), (115, -35),
          (114, -22)], sand)
    for lon, lat, label in PINS:
        px_, py_ = px(lon, lat)
        dot(d, px_, py_, 4, (178, 48, 32))
        d.ellipse([px_ - 6, py_ - 6, px_ + 6, py_ + 6], outline=(178, 48, 32),
                  width=1)


def hero_panel(d, x, y, w, h, scene, kicker, head, detail):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    scene(d, x + 1, y + 1, w - 2, 118)
    d.text((x + 10, y + 122), kicker, font=F_SMALL_B, fill=(178, 48, 32))
    for i, ln in enumerate(wrap(d, head, F_CAP, w - 20)):
        d.text((x + 10, y + 138 + i * 16), ln, font=F_CAP, fill=INK)
    for i, ln in enumerate(wrap(d, detail, F_CAP2, w - 20)[:2]):
        d.text((x + 10, y + 172 + i * 12), ln, font=F_CAP2, fill=MUTED)


def region_cell(d, x, y, w, h, name, color, stories):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 24], fill=color)
    d.text((x + 10, y + 5), name, font=F_REG, fill=WHITE)
    _tw = d.textlength("6 STORIES", font=F_SMALL_B)
    d.text((x + w - 10 - _tw, y + 5), "6 STORIES", font=F_SMALL_B,
           fill=(255, 255, 255))
    yy = y + 28
    for time, head, detail, conf in stories:
        dot(d, x + 10, yy + 5, 4, conf_color(conf))
        d.text((x + 20, yy - 2), time, font=F_TIME, fill=color)
        tw = d.textlength(time, font=F_TIME)
        d.text((x + 20 + tw + 7, yy - 2), head, font=F_HEAD, fill=INK)
        d.text((x + 20, yy + 13), detail, font=F_DET, fill=(70, 70, 70))
        yy += 26


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 88], fill=GOLD)
    d.text((16, 8), "THE WORLD IN ONE DAY", font=F_TITLE, fill=WHITE)
    d.text((16, 56), "TUESDAY 24 NOVEMBER 2026", font=F_SUB_B,
           fill=(240, 200, 90))
    right = "36 DATED STORIES  •  6 REGIONS  •  3 DRAWN SCENES"
    d.text((W - 16 - d.textlength(right, font=F_SUB), 14), right,
           font=F_SUB, fill=(200, 210, 225))
    # legend with real coloured dots (text alone cannot colour them)
    _lx = W - 16
    for _lab, _col in (("CLAIMED", CLAIMED), ("REPORTED", REPORTED),
                       ("CONFIRMED", CONFIRMED)):
        _w = d.textlength(_lab, font=F_SMALL)
        d.text((_lx - _w, 40), _lab, font=F_SMALL, fill=(170, 182, 200))
        dot(d, _lx - _w - 9, 45, 4, _col)
        _lx = _lx - _w - 20
    _pre = "ALL TIMES UTC  •  HOW SURE:"
    d.text((_lx - d.textlength(_pre, font=F_SMALL), 40), _pre, font=F_SMALL,
           fill=(170, 182, 200))
    d.text((W - 16 - d.textlength("SALTWATER VERDICT", font=F_SMALL_B), 60),
           "SALTWATER VERDICT", font=F_SMALL_B, fill=(240, 200, 90))

    # ---- hero: three drawn scenes ----
    hero_panel(d, 14, 96, 324, 200, scene_hormuz, "LEAD  •  THE STRAIT",
               "Four tankers hit mines in Hormuz",
               "Iran reports the strikes; a US-led maritime centre says the claims are unconfirmed.")
    hero_panel(d, 350, 96, 324, 200, scene_court, "LEAD  •  THE COURTROOM",
               "Huawei guilty of trade secrets and bank fraud",
               "A US jury convicts on 10 of 12 counts and clears the firm of racketeering.")
    hero_panel(d, 686, 96, 324, 200, scene_ship, "LEAD  •  THE WAR AT SEA",
               "Ukraine drones strike Russian ships",
               "Cargo ship Sparta II hit in the Gulf of Finland; a corvette struck off Libya.")

    # ---- region grid: 2 columns x 3 rows ----
    xs = (14, 514)
    ys = (304, 496, 688)
    for i, (name, color, stories) in enumerate(REGIONS):
        region_cell(d, xs[i % 2], ys[i // 2], 496, 184, name, color, stories)

    # ---- bottom band: map + UTC timeline ----
    d.rectangle([14, 880, 510, 1000], fill=CARD, outline=LINE, width=1)
    d.text((24, 887), "WHERE IT HAPPENED — 14 PLACES, ONE DAY",
           font=F_SMALL_B, fill=NAVY2)
    draw_map(d, 24, 905, 476, 87)

    d.rectangle([514, 880, 1010, 1000], fill=CARD, outline=LINE, width=1)
    d.text((524, 887), "THE DAY IN UTC", font=F_SMALL_B, fill=NAVY2)
    yy = 905
    for time, event in TIMELINE:
        d.text((524, yy), time, font=F_TL, fill=(178, 48, 32))
        d.text((574, yy), event, font=F_TL2, fill=INK)
        yy += 13
    d.text((524, 986), "MARKETS 24 NOV: KOSPI +6.3%  •  NIKKEI +3.9%  •  BRENT $86.7  •  GOLD $3,620",
           font=F_SMALL, fill=MUTED)

    # ---- footer strip ----
    d.text((14, 1007), "Sources: wire, court and official reports first published 24 Nov 2026. Times UTC.",
           font=F_SMALL, fill=MUTED)
    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    print(build())
