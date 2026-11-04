"""Generates every animated SVG used by the profile README.

Edit the text below, then run:  python3 assets/src/build.py
"""
import os
import random
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..")
random.seed(11)

# ---- design tokens ---------------------------------------------------------
BG = "#0b0820"
CARD = "#130c2e"
LINE = "#2c2060"
CYAN = "#00f7ff"
VIOLET = "#b57bff"
TEXT = "#ece7ff"
MUTED = "#a99fd0"
FONT = "font-family=\"'SF Pro Display','Segoe UI','Helvetica Neue',Arial,sans-serif\""


def e(s):
    return escape(s, {'"': "&quot;"})


def svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<defs>{SHIMMER}{defs}</defs>{body}</svg>"
    )


SHIMMER = (
    f'<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="#c9a0ff"/><stop offset="1" stop-color="{CYAN}"/>'
    f'<animate attributeName="x1" values="-1;0" dur="4s" repeatCount="indefinite"/>'
    f'<animate attributeName="x2" values="0;1" dur="4s" repeatCount="indefinite"/></linearGradient>'
    f'<linearGradient id="cv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
)


def card(x, y, w, h, delay=0.0, r=16):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{CARD}" stroke="{VIOLET}" stroke-opacity="0.35">'
        f'<animate attributeName="stroke-opacity" values="0.25;0.9;0.25" dur="4s" begin="{delay:.2f}s" repeatCount="indefinite"/></rect>'
    )


def text(x, y, s, size=14, fill=TEXT, weight=400, anchor="start", spacing=0, extra=""):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}" letter-spacing="{spacing}" {FONT}>{e(s)}{extra}</text>'
    )


def lines(x, y, rows, size=14, fill=MUTED, gap=21, anchor="start"):
    return "".join(text(x, y + i * gap, r, size, fill, anchor=anchor) for i, r in enumerate(rows))


def pulse_dot(cx, cy, color=CYAN, delay=0.0):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="4" fill="{color}"><animate attributeName="r" values="3;5;3" dur="2s" begin="{delay}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0.4;1" dur="2s" begin="{delay}s" repeatCount="indefinite"/></circle>'
    )


def particles(n, w, h, y0):
    out = []
    for _ in range(n):
        x = random.randint(10, w - 10)
        y = random.randint(y0, h + 20)
        r = random.choice([1.2, 1.8, 2.4, 3])
        d = random.uniform(6, 13)
        b = random.uniform(0, 8)
        col = random.choice([CYAN, VIOLET, "#ffffff"])
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity="0">'
            f'<animate attributeName="cy" values="{y};-10" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0.9;0" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(out)


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


# ---- header ----------------------------------------------------------------
def header():
    pills = [("PRODUCT", CYAN), ("ANALYTICS", VIOLET), ("FULL-STACK", CYAN)]
    pill_svg = ""
    for i, (t, c) in enumerate(pills):
        x = 245 + i * 185
        pill_svg += (
            f'<g transform="translate({x},262)"><rect width="140" height="34" rx="17" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-opacity="0.6">'
            f'<animate attributeName="stroke-opacity" values="0.3;0.95;0.3" dur="3s" begin="{i * 0.8}s" repeatCount="indefinite"/></rect>'
            + text(70, 22, t, 13, c, 600, "middle", 3)
            + "</g>"
        )
    defs = (
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0b0820"><animate attributeName="stop-color" values="#0b0820;#1a0b3d;#07182e;#0b0820" dur="10s" repeatCount="indefinite"/></stop>'
        '<stop offset="1" stop-color="#150a33"><animate attributeName="stop-color" values="#150a33;#06223a;#2a0e4f;#150a33" dur="10s" repeatCount="indefinite"/></stop></linearGradient>'
        f'<radialGradient id="g1"><stop offset="0" stop-color="#7b2ff7" stop-opacity="0.6"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="g2"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.45"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
        '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#7b2ff7" stroke-opacity="0.2"/>'
        '<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="40 40" dur="6s" repeatCount="indefinite"/></pattern>'
        '<filter id="blur"><feGaussianBlur stdDeviation="6"/></filter><clipPath id="c"><rect width="1000" height="340" rx="20"/></clipPath>'
    )
    body = (
        '<g clip-path="url(#c)"><rect width="1000" height="340" fill="url(#bg)"/><rect width="1000" height="340" fill="url(#grid)"/>'
        '<ellipse cx="220" cy="90" rx="380" ry="210" fill="url(#g1)"><animate attributeName="cx" values="220;340;220" dur="9s" repeatCount="indefinite"/></ellipse>'
        '<ellipse cx="820" cy="280" rx="380" ry="210" fill="url(#g2)"><animate attributeName="cx" values="820;680;820" dur="11s" repeatCount="indefinite"/></ellipse>'
        + particles(40, 1000, 340, 260)
        + text(500, 82, "HELLO, I'M", 15, CYAN, 500, "middle", 10, '<animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>')
        + f'<text x="500" y="180" text-anchor="middle" font-size="100" font-weight="800" letter-spacing="4" fill="{CYAN}" filter="url(#blur)" opacity="0.4" {FONT}>RONAK SINGH'
        '<animate attributeName="opacity" values="0.45;0.15;0.45" dur="3s" repeatCount="indefinite"/></text>'
        + text(500, 180, "RONAK SINGH", 100, "url(#sh)", 800, "middle", 4)
        + text(500, 228, "I turn real problems into shipped products", 22, TEXT, 400, "middle")
        + pill_svg
        + '</g><rect x="1" y="1" width="998" height="338" rx="20" fill="none" stroke="url(#sh)" stroke-width="1.5" opacity="0.8"/>'
    )
    write("header.svg", svg(1000, 340, body, defs))


# ---- link buttons ----------------------------------------------------------
BUTTONS = {
    "pupmeow": ("See PupMeow live", True),
    "linkedin": ("LinkedIn", False),
    "email": ("Email me", False),
    "leetcode": ("LeetCode", False),
}


def buttons():
    for i, (key, (label, primary)) in enumerate(BUTTONS.items()):
        w, h = 210, 54
        if primary:
            fill = 'fill="url(#cv)"'
            color = BG
        else:
            fill = f'fill="{CARD}" stroke="{VIOLET}" stroke-opacity="0.5"'
            color = TEXT
        body = (
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="27" {fill}/>'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="27" fill="none" stroke="url(#sh)" stroke-width="1.5" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;0" dur="3s" begin="{i * 0.6}s" repeatCount="indefinite"/></rect>'
            + text(w / 2 - 8, 33, label, 16, color, 700, "middle")
            + text(w - 34, 33, "↗", 16, color, 700, "middle",
                   extra='<animateTransform attributeName="transform" type="translate" values="0 0;3 -3;0 0" dur="1.6s" repeatCount="indefinite"/>')
        )
        write(f"btn-{key}.svg", svg(w, h, body))


# ---- stats strip -----------------------------------------------------------
def strip():
    items = [("4", "PROJECTS BUILT"), ("3", "LIVE ON THE WEB"), ("1", "REAL LAUNCH · DELHI NCR"), ("400+", "LEETCODE PROBLEMS SOLVED")]
    body = ""
    for i, (n, l) in enumerate(items):
        x = 6 + i * 248
        body += (
            card(x, 6, 236, 104, i * 0.7)
            + text(x + 118, 58, n, 40, "url(#cv)", 800, "middle",
                   extra=f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="3s" begin="{i * 0.5}s" repeatCount="indefinite"/>')
            + text(x + 118, 86, l, 11, MUTED, 500, "middle", 2.5)
        )
    write("strip.svg", svg(1000, 116, body))


# ---- section titles (dark + light variants) -------------------------------
TITLES = {
    "think": "HOW I THINK",
    "work": "SELECTED WORK",
    "toolkit": "TOOLKIT",
    "activity": "ACTIVITY",
    "now": "RIGHT NOW",
}


def titles():
    for theme, (a, b, track) in {
        "dark": (CYAN, "#c9a0ff", "#7b2ff7"),
        "light": ("#6d28d9", "#0891b2", "#c4b5fd"),
    }.items():
        grad = (
            f'<linearGradient id="t" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset="0.5" stop-color="{b}"/><stop offset="1" stop-color="{a}"/>'
            '<animate attributeName="x1" values="-1;0" dur="4s" repeatCount="indefinite"/><animate attributeName="x2" values="0;1" dur="4s" repeatCount="indefinite"/></linearGradient>'
        )
        for key, t in TITLES.items():
            body = (
                text(500, 46, t, 30, "url(#t)", 800, "middle", 6)
                + f'<rect x="420" y="64" width="160" height="2" rx="1" fill="{track}" opacity="0.5"/>'
                + f'<rect x="420" y="63" width="40" height="4" rx="2" fill="{a}"><animate attributeName="x" values="420;540;420" dur="3s" repeatCount="indefinite"/></rect>'
            )
            write(f"title-{key}-{theme}.svg", svg(1000, 80, body, grad))


# ---- principles ------------------------------------------------------------
PRINCIPLES = [
    ("01", "Problem first", ["Who hurts, when, and", "why today's options", "fail them."]),
    ("02", "Ruthless scope", ["The 'no' list matters", "as much as the", "roadmap."]),
    ("03", "Trust is a feature", ["Consent before contact.", "AI that knows its", "own limits."]),
    ("04", "Data decides", ["Measure what users", "do, not what they", "say they'd do."]),
    ("05", "Ship, then learn", ["A live product with", "real feedback beats a", "perfect doc."]),
]


def principles():
    body = ""
    w, gap = 186, 15.5
    for i, (n, t, rows) in enumerate(PRINCIPLES):
        x = 4 + i * (w + gap)
        body += (
            card(x, 6, w, 190, i * 0.5)
            + text(x + 20, 50, n, 26, "url(#cv)", 800)
            + f'<rect x="{x + 20}" y="62" width="28" height="3" rx="1.5" fill="{VIOLET}"><animate attributeName="width" values="28;60;28" dur="3s" begin="{i * 0.5}s" repeatCount="indefinite"/></rect>'
            + text(x + 20, 96, t, 17, TEXT, 700)
            + lines(x + 20, 124, rows, 13.5, MUTED, 20)
        )
    write("principles.svg", svg(1000, 202, body))


# ---- PupMeow ---------------------------------------------------------------
def pupmeow_brief():
    cols = [
        ("THE PROBLEM", ["Lost-pet alerts get buried in", "fifty WhatsApp groups. Adoption", "DMs end in 'transport fee' scams."]),
        ("WHO IT'S FOR", ["Dog and cat families, adopters", "and NGOs across Delhi NCR who", "need one place they can trust."]),
        ("THE INSIGHT", ["People won't leave WhatsApp.", "So PupMeow doesn't replace chat.", "It hands the conversation back."]),
    ]
    body = ""
    for i, (h, rows) in enumerate(cols):
        x = 6 + i * 333
        body += (
            card(x, 6, 321, 160, i * 0.7)
            + pulse_dot(x + 26, 41, [CYAN, VIOLET, CYAN][i], i * 0.4)
            + text(x + 42, 46, h, 13, [CYAN, VIOLET, CYAN][i], 700, spacing=3)
            + lines(x + 22, 84, rows, 15, TEXT, 24)
        )
    write("pupmeow-brief.svg", svg(1000, 172, body))


DECISIONS = [
    ("Free forever, no selling", ["Kills the scam incentive.", "Priced listings get removed."]),
    ("Chat stays on WhatsApp", ["Zero new habits to learn,", "so far less friction."]),
    ("Numbers unlock on consent", ["Both sides agree first.", "Private by default, no spam."]),
    ("A4 poster + QR for lost pets", ["Meets the search where it", "happens: streets and groups."]),
    ("AI with an emergency banner", ["A pet-care bot must know", "when to say 'see a vet now'."]),
    ("PWA before app stores", ["Ship fast, install in one tap,", "learn before building Android."]),
]


def pupmeow_decisions():
    body = text(10, 26, "PRODUCT DECISIONS, AND WHY", 13, VIOLET, 700, spacing=3)
    w, h = 321, 112
    for i, (t, rows) in enumerate(DECISIONS):
        col, row = i % 3, i // 3
        x, y = 6 + col * 333, 44 + row * 124
        body += (
            card(x, y, w, h, i * 0.4)
            + f'<circle cx="{x + 31}" cy="{y + 32}" r="12" fill="{CYAN}" fill-opacity="0.12" stroke="{CYAN}" stroke-opacity="0.6">'
            f'<animate attributeName="fill-opacity" values="0.08;0.3;0.08" dur="3s" begin="{i * 0.4}s" repeatCount="indefinite"/></circle>'
            + f'<path d="M{x + 25} {y + 32} l4 4 l8 -9" fill="none" stroke="{CYAN}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            + text(x + 54, y + 38, t, 16, TEXT, 700)
            + lines(x + 22, y + 68, rows, 14, MUTED, 21)
        )
    write("pupmeow-decisions.svg", svg(1000, 44 + 2 * 124, body))


FEATURES = ["Lost & Found", "Free adoption", "Playdates", "Pet health", "Kaia AI helper", "Community feed", "Installable PWA"]


def chips(name, label, items, color=CYAN):
    widths = [int(len(it) * 8.1 + 34) for it in items]
    rows, row, used = [], [], 0
    for it, w in zip(items, widths):
        if row and used + w > 940:
            rows.append(row)
            row, used = [], 0
        row.append((it, w))
        used += w + 10
    rows.append(row)
    h = 64 + len(rows) * 50
    body = card(4, 4, 992, h - 8, 0, 18) + text(500, 38, label, 13, VIOLET, 700, "middle", 3)
    i = 0
    for r, row in enumerate(rows):
        total = sum(w for _, w in row) + 10 * (len(row) - 1)
        x, y = 500 - total / 2, 54 + r * 50
        for it, w in row:
            body += (
                f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="19" fill="{color}" fill-opacity="0.07" stroke="{color}" stroke-opacity="0.45">'
                f'<animate attributeName="fill-opacity" values="0.05;0.22;0.05" dur="4s" begin="{i * 0.35}s" repeatCount="indefinite"/></rect>'
                + text(x + w / 2, y + 25, it, 14.5, TEXT, 600, "middle")
            )
            x += w + 10
            i += 1
    write(name, svg(1000, h, body))


# ---- FinSight --------------------------------------------------------------
def finsight():
    feats = ["P&L, sector allocation, gainers and losers", "Company financials, ratios and AI summaries",
             "Portfolio and watchlist management", "Gemini assistant that explains the numbers", "JWT auth with email verification"]
    body = card(6, 6, 988, 268, 0, 20)
    # mini animated chart
    pts = [(40, 246), (95, 230), (150, 236), (205, 212), (260, 220), (315, 192), (370, 200), (440, 166)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    body += (
        text(40, 56, "FinSight AI", 30, "url(#sh)", 800)
        + text(40, 86, "Investing research without the tab chaos", 16, TEXT, 500)
        + lines(40, 118, ["Investors juggle tabs for prices, news, portfolio and questions.",
                          "One dashboard answers: how am I doing, and why?"], 14, MUTED, 21)
        + f'<path d="{d} L440 258 L40 258 Z" fill="{CYAN}" fill-opacity="0.08"/>'
        + f'<path d="{d}" fill="none" stroke="url(#cv)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="500" stroke-dashoffset="500">'
        '<animate attributeName="stroke-dashoffset" values="500;0;0" keyTimes="0;0.5;1" dur="5s" repeatCount="indefinite"/></path>'
        + f'<circle cx="440" cy="166" r="5" fill="{CYAN}"><animate attributeName="r" values="3;7;3" dur="2s" repeatCount="indefinite"/></circle>'
        + f'<line x1="500" y1="36" x2="500" y2="244" stroke="{LINE}"/>'
        + text(530, 56, "WHAT IT DOES", 13, VIOLET, 700, spacing=3)
    )
    for i, f in enumerate(feats):
        y = 92 + i * 36
        body += (
            f'<circle cx="540" cy="{y - 5}" r="9" fill="{CYAN}" fill-opacity="0.12" stroke="{CYAN}" stroke-opacity="0.6"/>'
            f'<path d="M535 {y - 5} l3.5 3.5 l6.5 -7" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            + text(562, y, f, 15, TEXT)
        )
    write("finsight.svg", svg(1000, 280, body))


# ---- smaller builds --------------------------------------------------------
def mini(name, title, sub, rows, tags, why, delay):
    body = card(4, 4, 482, 252, delay, 18) + text(28, 48, title, 22, "url(#sh)", 800) + text(28, 74, sub, 14, VIOLET, 600)
    body += lines(28, 108, rows, 14, TEXT, 21)
    x = 28
    for t in tags:
        w = int(len(t) * 7.6 + 26)
        body += f'<rect x="{x}" y="172" width="{w}" height="28" rx="14" fill="{CYAN}" fill-opacity="0.08" stroke="{CYAN}" stroke-opacity="0.4"/>' + text(x + w / 2, 191, t, 12.5, CYAN, 600, "middle")
        x += w + 8
    body += text(28, 228, why, 13, MUTED) + text(458, 228, "↗", 16, CYAN, 700, "end")
    write(name, svg(490, 260, body))


# ---- right now -------------------------------------------------------------
def now():
    cols = [
        ("BUILDING", ["Growing PupMeow across", "Delhi NCR, polishing", "FinSight AI"]),
        ("LEARNING", ["Product analytics,", "Next.js, TypeScript,", "system design basics"]),
        ("PRACTISING", ["DSA daily on LeetCode", "in C++"]),
        ("LOOKING FOR", ["Product / Analyst", "internships and", "placements"]),
    ]
    body = ""
    for i, (h, rows) in enumerate(cols):
        x = 6 + i * 248
        color = CYAN if i % 2 == 0 else VIOLET
        if i == 3:
            body += f'<rect x="{x}" y="6" width="236" height="150" rx="16" fill="url(#cv)" fill-opacity="0.14" stroke="url(#sh)" stroke-width="1.5"/>'
        else:
            body += card(x, 6, 236, 150, i * 0.6)
        body += pulse_dot(x + 24, 39, color, i * 0.5) + text(x + 38, 44, h, 12.5, color, 700, spacing=3)
        body += lines(x + 20, 82, rows, 15, TEXT, 22)
    write("now.svg", svg(1000, 162, body))


# ---- footer ----------------------------------------------------------------
def footer():
    def wave(y, amp, color, op, dur, reverse=False):
        d = f"M0 {y}" + "".join(f" Q{k * 500 + 125} {y - amp} {k * 500 + 250} {y} T{(k + 1) * 500} {y}" for k in range(5)) + " V260 H0 Z"
        a, b = (-1000, 0) if reverse else (0, -1000)
        return f'<path d="{d}" fill="{color}" opacity="{op}"><animateTransform attributeName="transform" type="translate" from="{a} 0" to="{b} 0" dur="{dur}s" repeatCount="indefinite"/></path>'

    defs = f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#150a33"/><stop offset="1" stop-color="{BG}"/></linearGradient><clipPath id="c"><rect width="1000" height="240" rx="20"/></clipPath>'
    body = (
        '<g clip-path="url(#c)"><rect width="1000" height="240" fill="url(#bg)"/>'
        + particles(26, 1000, 240, 120)
        + wave(150, 26, "#7b2ff7", 0.45, 16) + wave(168, 20, CYAN, 0.30, 11, True) + wave(188, 16, VIOLET, 0.40, 8)
        + f'<rect y="205" width="1000" height="35" fill="{BG}" opacity="0.85"/>'
        + text(500, 74, "Let's build something people love.", 32, "url(#sh)", 800, "middle")
        + text(500, 108, "Open to Product / Analyst internships  ·  ronaksingh18062005@gmail.com", 15, MUTED, 400, "middle")
        + text(500, 228, "PROBLEM  →  BUILD  →  SHIP  →  LEARN  →  REPEAT", 14, "url(#sh)", 700, "middle", 6)
        + '</g><rect x="1" y="1" width="998" height="238" rx="20" fill="none" stroke="url(#sh)" stroke-width="1.5" opacity="0.7"/>'
    )
    write("footer.svg", svg(1000, 240, body, defs))


if __name__ == "__main__":
    header()
    buttons()
    strip()
    titles()
    principles()
    pupmeow_brief()
    pupmeow_decisions()
    chips("pupmeow-features.svg", "WHAT'S INSIDE", FEATURES)
    finsight()
    mini("kinematics.svg", "Kinematics Simulator", "3-DOF robotic arm, from scratch",
         ["Denavit-Hartenberg forward kinematics with", "custom Vector3 and Matrix4x4 classes, an", "ASCII visualiser and MATLAB plots."],
         ["C++17", "MATLAB", "CMake"], "Taught me to break hard systems into clean pieces", 0.3)
    mini("movies.svg", "IMDb Top 250 Explorer", "Fast movie discovery in vanilla JS",
         ["Search by title, director or actor, filter by", "genre and rating, and keep favourites and", "a watchlist."],
         ["JavaScript", "HTML", "CSS"], "My first lesson in effortless search and filters", 1.0)
    chips("toolkit-product.svg", "PRODUCT & ANALYTICS",
          ["Problem discovery", "Scoping & prioritisation", "User flows", "Trade-off decisions", "Metrics thinking", "Dashboards", "Ship & iterate"], VIOLET)
    now()
    footer()
