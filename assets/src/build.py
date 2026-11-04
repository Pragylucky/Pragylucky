"""Generates the animated SVGs used by the profile README.

Edit the text below, then run:  python3 assets/src/build.py
"""
import os
import random
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..")
random.seed(11)

# ---- design tokens ---------------------------------------------------------
BG = "#0b0820"
CYAN = "#00f7ff"
VIOLET = "#b57bff"
PINK = "#ff8fc7"
TEXT = "#ece7ff"
MUTED = "#a99fd0"
FONT = "font-family=\"'SF Pro Display','Segoe UI','Helvetica Neue',Arial,sans-serif\""

SHIMMER = (
    f'<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="#c9a0ff"/><stop offset="1" stop-color="{CYAN}"/>'
    f'<animate attributeName="x1" values="-1;0" dur="4s" repeatCount="indefinite"/>'
    f'<animate attributeName="x2" values="0;1" dur="4s" repeatCount="indefinite"/></linearGradient>'
)


def e(s):
    return escape(s, {'"': "&quot;"})


def svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<defs>{SHIMMER}{defs}</defs>{body}</svg>"
    )


def text(x, y, s, size=14, fill=TEXT, weight=400, anchor="start", spacing=0, extra=""):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}" letter-spacing="{spacing}" {FONT}>{e(s)}{extra}</text>'
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


def paw(x, y, s, color, rot=90):
    """One paw print centred on (x, y), pointing in the direction of `rot` degrees."""
    toes = "".join(f'<ellipse cx="{tx}" cy="{ty}" rx="2.6" ry="3.4" transform="rotate({tr} {tx} {ty})"/>'
                   for tx, ty, tr in [(-6.5, -6, -25), (-2.2, -10, -8), (2.2, -10, 8), (6.5, -6, 25)])
    return (
        f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" fill="{color}">'
        f'<path d="M0 -3 C5 -3 8 2 7 5 C6 8 3 7 0 7 C-3 7 -6 8 -7 5 C-8 2 -5 -3 0 -3 Z"/>{toes}</g>'
    )


def paw_trail(width, y, count, colors, s=1.0, dur=6.0):
    """Paw prints that appear one after another, like a pet walking across."""
    out = []
    step = width / count
    for i in range(count):
        x = step * (i + 0.5)
        dy = -7 if i % 2 == 0 else 7
        b = dur * i / count
        out.append(
            f'<g opacity="0.18">{paw(round(x, 1), y + dy, s, colors[i % len(colors)])}'
            f'<animate attributeName="opacity" values="0.18;1;1;0.18" keyTimes="0;0.05;0.45;0.6" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/></g>'
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
            f'<g transform="translate({x},250)"><rect width="140" height="34" rx="17" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-opacity="0.6">'
            f'<animate attributeName="stroke-opacity" values="0.3;0.95;0.3" dur="3s" begin="{i * 0.8}s" repeatCount="indefinite"/></rect>'
            + text(70, 22, t, 13, c, 600, "middle", 3)
            + "</g>"
        )
    defs = (
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0b0820"><animate attributeName="stop-color" values="#0b0820;#1a0b3d;#07182e;#0b0820" dur="10s" repeatCount="indefinite"/></stop>'
        '<stop offset="1" stop-color="#150a33"><animate attributeName="stop-color" values="#150a33;#06223a;#2a0e4f;#150a33" dur="10s" repeatCount="indefinite"/></stop></linearGradient>'
        '<radialGradient id="g1"><stop offset="0" stop-color="#7b2ff7" stop-opacity="0.6"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></radialGradient>'
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
        + text(500, 76, "HELLO, I'M", 15, CYAN, 500, "middle", 10, '<animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>')
        + f'<text x="500" y="172" text-anchor="middle" font-size="100" font-weight="800" letter-spacing="4" fill="{CYAN}" filter="url(#blur)" opacity="0.4" {FONT}>RONAK SINGH'
        '<animate attributeName="opacity" values="0.45;0.15;0.45" dur="3s" repeatCount="indefinite"/></text>'
        + text(500, 172, "RONAK SINGH", 100, "url(#sh)", 800, "middle", 4)
        + text(500, 218, "Electrical Engineer  •  Full Stack Builder  •  Product & Analytics Mind", 19, TEXT, 400, "middle")
        + pill_svg
        + paw_trail(1000, 314, 16, [CYAN, VIOLET, PINK], 0.85, 8)
        + '</g><rect x="1" y="1" width="998" height="338" rx="20" fill="none" stroke="url(#sh)" stroke-width="1.5" opacity="0.8"/>'
    )
    write("header.svg", svg(1000, 340, body, defs))


# ---- PupMeow paw-print trail -----------------------------------------------
def paws():
    write("paws.svg", svg(1000, 50, paw_trail(1000, 25, 20, ["#0e7c72", "#f2a93b", PINK, VIOLET], 1.1, 7)))


# ---- footer ----------------------------------------------------------------
def footer():
    def wave(y, amp, color, op, dur, reverse=False):
        d = f"M0 {y}" + "".join(f" Q{k * 500 + 125} {y - amp} {k * 500 + 250} {y} T{(k + 1) * 500} {y}" for k in range(5)) + " V260 H0 Z"
        a, b = (-1000, 0) if reverse else (0, -1000)
        return f'<path d="{d}" fill="{color}" opacity="{op}"><animateTransform attributeName="transform" type="translate" from="{a} 0" to="{b} 0" dur="{dur}s" repeatCount="indefinite"/></path>'

    # a heart that beats next to the tagline
    heart = (
        f'<g transform="translate(500 136)"><path d="M0 6 C-14 -4 -9 -16 0 -9 C9 -16 14 -4 0 6 Z" fill="{PINK}">'
        '<animateTransform attributeName="transform" type="scale" values="1;1.25;1;1.15;1" dur="1.4s" repeatCount="indefinite"/></path></g>'
    )
    defs = f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#150a33"/><stop offset="1" stop-color="{BG}"/></linearGradient><clipPath id="c"><rect width="1000" height="240" rx="20"/></clipPath>'
    body = (
        '<g clip-path="url(#c)"><rect width="1000" height="240" fill="url(#bg)"/>'
        + particles(26, 1000, 240, 120)
        + wave(160, 26, "#7b2ff7", 0.45, 16) + wave(176, 20, CYAN, 0.30, 11, True) + wave(194, 16, VIOLET, 0.40, 8)
        + f'<rect y="208" width="1000" height="32" fill="{BG}" opacity="0.85"/>'
        + text(500, 66, "Thanks for stopping by!", 32, "url(#sh)", 800, "middle")
        + text(500, 100, "Learn  →  Build  →  Ship  →  Repeat", 16, MUTED, 500, "middle", 3)
        + heart
        + paw_trail(1000, 226, 18, [CYAN, VIOLET, PINK], 0.7, 8)
        + '</g><rect x="1" y="1" width="998" height="238" rx="20" fill="none" stroke="url(#sh)" stroke-width="1.5" opacity="0.7"/>'
    )
    write("footer.svg", svg(1000, 240, body, defs))


if __name__ == "__main__":
    header()
    paws()
    footer()
