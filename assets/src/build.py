"""Generates the animated black & white SVGs used by the profile README.

Every image is written twice, as <name>-light.svg and <name>-dark.svg, so the
README can swap them with <picture> to match the reader's GitHub theme.

Edit the text below, then run:  python3 assets/src/build.py
"""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..")

# ---- design tokens ---------------------------------------------------------
THEMES = {
    "light": dict(paper="#ffffff", ink="#111111", soft="#ececec", muted="#6b6b6b", dots="#e4e4e4"),
    "dark": dict(paper="#0d1117", ink="#f2f2f2", soft="#2b313a", muted="#9aa0a6", dots="#1f252d"),
}
SANS = "font-family=\"ui-rounded,'SF Pro Rounded','Nunito','Segoe UI',system-ui,sans-serif\""
MONO = "font-family=\"ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace\""

TAGLINES = [
    "Electrical engineer who builds products end to end",
    "Full-stack  ·  Next.js  ·  Supabase  ·  MERN",
    "Founder of PupMeow, live for pet families in Delhi NCR",
    "Open to Product / Analyst internships",
]


def e(s):
    return escape(s, {'"': "&quot;"})


def svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<defs>{defs}</defs>{body}</svg>"
    )


def text(x, y, s, size, fill, weight=400, anchor="middle", spacing=0, font=SANS, extra="", attrs=""):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}" letter-spacing="{spacing}" {font} {attrs}>{e(s)}{extra}</text>'
    )


def spin(a, b, cx, cy, dur, begin=0, spline=True):
    """Rock an element between angles a and b around (cx, cy)."""
    ease = ' calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"' if spline else ""
    return (
        f'<animateTransform attributeName="transform" type="rotate" values="{a} {cx} {cy};{b} {cx} {cy};{a} {cx} {cy}"'
        f' dur="{dur}s" begin="{begin}s" repeatCount="indefinite"{ease}/>'
    )


def blink(ry, dur=4.2, begin=0):
    return (
        f'<animate attributeName="ry" values="{ry};{ry};0.4;{ry}" keyTimes="0;0.9;0.95;1" '
        f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
    )


def card(w, h, t):
    """Rounded paper card with a faint dot grid and an ink outline."""
    defs = (
        f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.3" fill="{t["dots"]}"/></pattern>'
        f'<clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath>'
    )
    back = f'<rect width="{w}" height="{h}" rx="22" fill="{t["paper"]}"/><rect width="{w}" height="{h}" fill="url(#dots)" clip-path="url(#c)"/>'
    edge = f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="21" fill="none" stroke="{t["ink"]}" stroke-width="2"/>'
    return defs, back, edge


def heart(x, y, s, fill):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 4 C-8 -2 -6 -9 0 -5 C6 -9 8 -2 0 4 Z" fill="{fill}"/>'


def paw(x, y, s, color, rot=90):
    """One paw print centred on (x, y), pointing in the direction of `rot` degrees."""
    toes = "".join(f'<ellipse cx="{tx}" cy="{ty}" rx="2.6" ry="3.4" transform="rotate({tr} {tx} {ty})"/>'
                   for tx, ty, tr in [(-6.5, -6, -25), (-2.2, -10, -8), (2.2, -10, 8), (6.5, -6, 25)])
    return (
        f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" fill="{color}">'
        f'<path d="M0 -3 C5 -3 8 2 7 5 C6 8 3 7 0 7 C-3 7 -6 8 -7 5 C-8 2 -5 -3 0 -3 Z"/>{toes}</g>'
    )


def paw_trail(width, y, count, color, s=1.0, dur=6.0, x0=0):
    """Paw prints that appear one after another, like a pet walking across."""
    out = []
    step = width / count
    for i in range(count):
        x = x0 + step * (i + 0.5)
        dy = -6 if i % 2 == 0 else 6
        b = dur * i / count
        out.append(
            f'<g opacity="0.1">{paw(round(x, 1), y + dy, s, color)}'
            f'<animate attributeName="opacity" values="0.1;0.9;0.9;0.1" keyTimes="0;0.05;0.45;0.6" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/></g>'
        )
    return "".join(out)


# ---- characters (origin = where the feet touch the ground) -----------------
def sitting_cat(x, y, s, t):
    ink, paper, soft = t["ink"], t["paper"], t["soft"]
    st = f'stroke="{ink}" stroke-width="3" stroke-linejoin="round"'
    whiskers = "".join(
        f'<line x1="{sx * 20}" y1="{y1}" x2="{sx * 38}" y2="{y2}" stroke="{ink}" stroke-width="1.6" stroke-linecap="round"/>'
        for sx in (-1, 1) for y1, y2 in ((-77, -81), (-73, -71))
    )
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        # tail sways behind the body
        f'<path d="M22 -8 C56 -6 62 -46 44 -62" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round">{spin(-8, 10, 22, -8, 2.6)}</path>'
        f'<path d="M-30 0 C-34 -40 -20 -62 0 -62 C20 -62 34 -40 30 0 Z" fill="{paper}" {st}/>'
        f'<path d="M-10 -40 Q0 -34 10 -40" fill="none" stroke="{soft}" stroke-width="3" stroke-linecap="round"/>'
        f'<ellipse cx="-11" cy="-3" rx="9" ry="6" fill="{paper}" {st}/><ellipse cx="11" cy="-3" rx="9" ry="6" fill="{paper}" {st}/>'
        # head tilts gently
        f'<g>{spin(-5, 5, 0, -62, 5)}'
        f'<path d="M-25 -90 L-21 -118 L-4 -103 Z" fill="{paper}" {st}/><path d="M25 -90 L21 -118 L4 -103 Z" fill="{paper}" {st}/>'
        f'<path d="M-20 -97 L-18.5 -110 L-11 -103 Z" fill="{soft}"/><path d="M20 -97 L18.5 -110 L11 -103 Z" fill="{soft}"/>'
        f'<ellipse cx="0" cy="-82" rx="30" ry="25" fill="{paper}" {st}/>'
        f'<ellipse cx="-11" cy="-85" rx="3.2" ry="4.2" fill="{ink}">{blink(4.2)}</ellipse>'
        f'<ellipse cx="11" cy="-85" rx="3.2" ry="4.2" fill="{ink}">{blink(4.2)}</ellipse>'
        f'<ellipse cx="-19" cy="-75" rx="5" ry="3" fill="{soft}"/><ellipse cx="19" cy="-75" rx="5" ry="3" fill="{soft}"/>'
        f'<path d="M-3 -78 L3 -78 L0 -74.5 Z" fill="{ink}"/>'
        f'<path d="M-6 -71 Q-3 -68 0 -72 Q3 -68 6 -71" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>'
        f"{whiskers}</g></g>"
    )


def sitting_dog(x, y, s, t):
    ink, paper, soft = t["ink"], t["paper"], t["soft"]
    st = f'stroke="{ink}" stroke-width="3" stroke-linejoin="round"'
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        # happy tail wag
        f'<path d="M-24 -12 C-44 -14 -52 -30 -50 -46" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round">{spin(-20, 22, -24, -12, 0.45)}</path>'
        f'<path d="M-32 0 C-36 -38 -22 -60 0 -60 C22 -60 36 -38 32 0 Z" fill="{paper}" {st}/>'
        f'<ellipse cx="0" cy="-34" rx="13" ry="16" fill="{soft}"/>'
        f'<ellipse cx="-12" cy="-3" rx="10" ry="6" fill="{paper}" {st}/><ellipse cx="12" cy="-3" rx="10" ry="6" fill="{paper}" {st}/>'
        f'<g>{spin(4, -4, 0, -60, 3.4)}'
        # floppy ears flap
        f'<g>{spin(0, 10, -24, -104, 1.7)}<ellipse cx="-31" cy="-84" rx="11" ry="22" transform="rotate(18 -31 -84)" fill="{ink}"/></g>'
        f'<g>{spin(0, -10, 24, -104, 1.7)}<ellipse cx="31" cy="-84" rx="11" ry="22" transform="rotate(-18 31 -84)" fill="{ink}"/></g>'
        f'<ellipse cx="0" cy="-86" rx="31" ry="28" fill="{paper}" {st}/>'
        f'<ellipse cx="12" cy="-92" rx="9" ry="8" fill="{soft}"/>'
        f'<ellipse cx="-12" cy="-92" rx="3.6" ry="4.2" fill="{ink}">{blink(4.2, 5.1, 1.3)}</ellipse>'
        f'<ellipse cx="12" cy="-92" rx="3.6" ry="4.2" fill="{ink}">{blink(4.2, 5.1, 1.3)}</ellipse>'
        f'<ellipse cx="0" cy="-75" rx="15" ry="11" fill="{paper}" {st}/>'
        f'<ellipse cx="0" cy="-80" rx="5.5" ry="3.8" fill="{ink}"/>'
        # panting tongue
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 2.5;0 0" dur="0.55s" repeatCount="indefinite"/>'
        f'<path d="M-5 -70 L-5 -63 Q0 -57 5 -63 L5 -70 Z" fill="{soft}" {st}/></g>'
        f'<path d="M0 -76 L0 -71 M-8 -71 Q-4 -67 0 -71 Q4 -67 8 -71" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>'
        f"</g></g>"
    )


def leg(hx, hy, color, width, dur, begin):
    return (
        f'<line x1="{hx}" y1="{hy}" x2="{hx}" y2="0" stroke="{color}" stroke-width="{width}" stroke-linecap="round">'
        f"{spin(-22, 22, hx, hy, dur, begin)}</line>"
    )


def bob(dur):
    return f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="{dur}s" repeatCount="indefinite"/>'


def running_dog(x, t):
    ink, paper, soft, muted = t["ink"], t["paper"], t["soft"], t["muted"]
    st = f'stroke="{ink}" stroke-width="3" stroke-linejoin="round"'
    d = 0.42
    return (
        f'<g transform="translate({x} 0)">'
        + leg(-22, -30, muted, 7, d, -d / 2) + leg(24, -30, muted, 7, d, 0)
        + f'<g>{bob(d / 2)}'
        f'<path d="M-34 -44 C-46 -52 -50 -64 -46 -74" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round">{spin(-15, 25, -34, -44, 0.3)}</path>'
        f'<ellipse cx="0" cy="-40" rx="38" ry="17" fill="{paper}" {st}/>'
        f'<ellipse cx="-10" cy="-46" rx="12" ry="7" fill="{soft}"/>'
        f'<circle cx="40" cy="-60" r="17" fill="{paper}" {st}/>'
        f'<ellipse cx="55" cy="-55" rx="11" ry="8" fill="{paper}" {st}/>'
        f'<circle cx="63" cy="-57" r="3.4" fill="{ink}"/>'
        f'<circle cx="45" cy="-64" r="2.8" fill="{ink}"/>'
        f'<path d="M52 -48 Q54 -41 59 -44" fill="{soft}" stroke="{ink}" stroke-width="2"/>'
        f'<g>{spin(-10, 15, 34, -72, 0.42)}<ellipse cx="32" cy="-60" rx="6.5" ry="13" transform="rotate(-15 32 -60)" fill="{ink}"/></g>'
        f"</g>"
        + leg(-26, -30, ink, 7, d, 0) + leg(20, -30, ink, 7, d, -d / 2)
        + "</g>"
    )


def running_cat(x, t):
    ink, paper, soft, muted = t["ink"], t["paper"], t["soft"], t["muted"]
    st = f'stroke="{ink}" stroke-width="3" stroke-linejoin="round"'
    d = 0.38
    return (
        f'<g transform="translate({x} 0)">'
        + leg(-18, -26, muted, 6, d, -d / 2) + leg(20, -26, muted, 6, d, 0)
        + f'<g>{bob(d / 2)}'
        f'<path d="M-30 -38 C-52 -44 -54 -70 -40 -84" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round">{spin(-8, 12, -30, -38, 1.1)}</path>'
        f'<ellipse cx="0" cy="-34" rx="32" ry="13" fill="{paper}" {st}/>'
        f'<path d="M-8 -46 Q-4 -38 0 -46 M4 -46 Q8 -38 12 -46" fill="none" stroke="{soft}" stroke-width="2.5"/>'
        f'<path d="M24 -58 L26 -76 L37 -64 Z" fill="{paper}" {st}/><path d="M37 -64 L46 -77 L49 -59 Z" fill="{paper}" {st}/>'
        f'<circle cx="37" cy="-52" r="14" fill="{paper}" {st}/>'
        f'<ellipse cx="43" cy="-54" rx="2.3" ry="3" fill="{ink}">{blink(3, 3.6)}</ellipse>'
        f'<circle cx="50.5" cy="-49" r="1.9" fill="{ink}"/>'
        f'<path d="M48 -47 L62 -50 M48 -45 L62 -43" stroke="{ink}" stroke-width="1.4" stroke-linecap="round"/>'
        f"</g>"
        + leg(-22, -26, ink, 6, d, 0) + leg(16, -26, ink, 6, d, -d / 2)
        + "</g>"
    )


def bouncing_ball(x, t):
    ink, paper = t["ink"], t["paper"]
    return (
        f'<g transform="translate({x} 0)"><g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 -50;0 -10;0 -50" keyTimes="0;0.5;1" '
        f'calcMode="spline" keySplines="0.55 0 1 0.45;0 0.55 0.45 1" dur="0.75s" repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.9s" repeatCount="indefinite"/>'
        f'<circle r="10" fill="{paper}" stroke="{ink}" stroke-width="2.6"/>'
        f'<path d="M-10 0 Q0 -7 10 0 M-10 0 Q0 7 10 0" fill="none" stroke="{ink}" stroke-width="1.6"/></g></g></g>'
    )


def butterfly(t, path, dur):
    ink, paper = t["ink"], t["paper"]
    return (
        f'<g><animateMotion path="{path}" dur="{dur}s" repeatCount="indefinite" rotate="0"/>'
        f'<g><animateTransform attributeName="transform" type="scale" values="1 1;0.25 1;1 1" dur="0.28s" repeatCount="indefinite"/>'
        f'<ellipse cx="-6" cy="-3" rx="6" ry="7" fill="{paper}" stroke="{ink}" stroke-width="2"/>'
        f'<ellipse cx="6" cy="-3" rx="6" ry="7" fill="{paper}" stroke="{ink}" stroke-width="2"/>'
        f'<ellipse cx="-4.5" cy="5" rx="4" ry="4" fill="{paper}" stroke="{ink}" stroke-width="2"/>'
        f'<ellipse cx="4.5" cy="5" rx="4" ry="4" fill="{paper}" stroke="{ink}" stroke-width="2"/></g>'
        f'<line x1="0" y1="-6" x2="0" y2="8" stroke="{ink}" stroke-width="2.6" stroke-linecap="round"/></g>'
    )


def floating(inner, x, y, dur, begin, rise=34, drift=10):
    """Something that drifts up and fades out (hearts, zzz)."""
    return (
        f'<g transform="translate({x} {y})"><g opacity="0">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{drift} {-rise}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.7;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f"{inner}</g></g>"
    )


def ground(x1, x2, y, t):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t["ink"]}" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 9"/>'


# ---- header ----------------------------------------------------------------
def header(t):
    W, H = 1000, 336
    defs, back, edge = card(W, H, t)
    ink, muted = t["ink"], t["muted"]

    n = len(TAGLINES)
    slot = 3.6
    seg = 1 / n
    lines = "".join(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{seg * 0.12:.3f};{seg * 0.88:.3f};{seg:.3f};1" dur="{slot * n}s" begin="{i * slot}s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 10;0 0;0 0;0 -10;0 -10" keyTimes="0;{seg * 0.12:.3f};{seg * 0.88:.3f};{seg:.3f};1" dur="{slot * n}s" begin="{i * slot}s" repeatCount="indefinite"/>'
        + text(500, 208, s, 19, muted, 500)
        + "</g>"
        for i, s in enumerate(TAGLINES)
    )

    squiggle = "M320 170" + "".join(" q10 -7 20 0 t20 0" for _ in range(9))
    underline = (
        f'<path d="{squiggle}" pathLength="100" fill="none" stroke="{ink}" stroke-width="3" stroke-linecap="round" stroke-dasharray="100" stroke-dashoffset="100">'
        f'<animate attributeName="stroke-dashoffset" values="100;0;0;-100" keyTimes="0;0.25;0.8;1" dur="6s" repeatCount="indefinite"/></path>'
    )

    pills = ""
    for i, label in enumerate(["PRODUCT", "ANALYTICS", "FULL-STACK"]):
        px = 291 + i * 145
        pills += (
            f'<g transform="translate({px} 238)"><rect width="128" height="30" rx="15" fill="{t["paper"]}" stroke="{ink}" stroke-width="2"/>'
            + text(64, 20, label, 12, ink, 700, "middle", 2.5, MONO)
            + "</g>"
        )

    hearts = "".join(floating(heart(0, 0, 1.1, ink), 905 + dx, 150, 2.6, b) for dx, b in ((-12, 0), (14, 1.3)))

    body = (
        back
        + text(500, 84, "hi, i'm", 15, muted, 500, "middle", 5, MONO)
        + text(500, 152, "Ronak Singh", 76, ink, 800, "middle", -1)
        + underline
        + lines
        + pills
        + ground(40, 960, 286, t)
        + sitting_cat(120, 284, 1.15, t)
        + butterfly(t, "M215 80 C255 50 300 105 260 130 C230 150 190 120 215 80 Z", 7)
        + sitting_dog(880, 284, 1.15, t)
        + hearts
        + paw_trail(W, 312, 18, ink, 0.75, 8)
        + edge
    )
    return svg(W, H, body, defs)


# ---- PupMeow: pets chasing a ball ------------------------------------------
def pupmeow_walk(t):
    W, H = 1000, 130
    pack = (
        f'<g><animateTransform attributeName="transform" type="translate" from="-320 0" to="{W + 120} 0" dur="12s" repeatCount="indefinite"/>'
        + running_cat(0, t) + running_dog(150, t) + bouncing_ball(250, t)
        + "</g>"
    )
    body = f'<g transform="translate(0 112)">{ground(10, W - 10, 2, t)}{pack}</g>'
    return svg(W, H, body)


def paws(t):
    return svg(1000, 50, paw_trail(1000, 25, 20, t["ink"], 1.0, 7))


# ---- footer ----------------------------------------------------------------
def sleeping_cat(t):
    ink, paper, soft = t["ink"], t["paper"], t["soft"]
    st = f'stroke="{ink}" stroke-width="3" stroke-linejoin="round"'
    breathe = '<animate attributeName="ry" values="27;30;27" dur="3.2s" repeatCount="indefinite"/><animate attributeName="cy" values="168;165;168" dur="3.2s" repeatCount="indefinite"/>'
    zs = "".join(
        floating(text(0, 0, "z", size, ink, 700), 112 + i * 6, 118 - i * 4, 3.6, i * 1.2, 30, 16)
        for i, size in enumerate((14, 17, 20))
    )
    return (
        f'<ellipse cx="180" cy="168" rx="54" ry="27" fill="{paper}" {st}>{breathe}</ellipse>'
        f'<path d="M150 150 Q170 144 190 150" fill="none" stroke="{soft}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M232 176 C246 190 226 200 200 199 C172 198 142 198 128 194" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
        f'<path d="M110 156 L108 130 L126 144 Z" fill="{paper}" {st}/><path d="M136 142 L150 124 L154 148 Z" fill="{paper}" {st}/>'
        f'<circle cx="132" cy="166" r="25" fill="{paper}" {st}/>'
        f'<path d="M118 166 Q123 171 128 166 M137 166 Q142 171 147 166" fill="none" stroke="{ink}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<ellipse cx="117" cy="176" rx="4.5" ry="2.6" fill="{soft}"/><ellipse cx="148" cy="176" rx="4.5" ry="2.6" fill="{soft}"/>'
        f'<path d="M130 174 L135 174 L132.5 177 Z" fill="{ink}"/>'
        + zs
    )


def lying_dog(t):
    ink, paper, soft = t["ink"], t["paper"], t["soft"]
    st = f'stroke="{ink}" stroke-width="3" stroke-linejoin="round"'
    breathe = '<animate attributeName="ry" values="23;26;23" dur="3.6s" repeatCount="indefinite"/><animate attributeName="cy" values="172;169;172" dur="3.6s" repeatCount="indefinite"/>'
    return (
        f'<path d="M896 168 C916 160 928 146 926 132" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round">{spin(-14, 18, 896, 168, 1.1)}</path>'
        f'<ellipse cx="852" cy="172" rx="54" ry="23" fill="{paper}" {st}>{breathe}</ellipse>'
        f'<ellipse cx="866" cy="160" rx="14" ry="8" fill="{soft}"/>'
        f'<ellipse cx="884" cy="190" rx="17" ry="8" fill="{paper}" {st}/>'
        f'<ellipse cx="790" cy="193" rx="15" ry="7" fill="{paper}" {st}/><ellipse cx="814" cy="195" rx="15" ry="7" fill="{paper}" {st}/>'
        f'<circle cx="802" cy="168" r="25" fill="{paper}" {st}/>'
        f'<g>{spin(0, 6, 812, 146, 2.4)}<ellipse cx="818" cy="164" rx="9" ry="19" transform="rotate(22 818 164)" fill="{ink}"/></g>'
        f'<ellipse cx="782" cy="178" rx="12" ry="9" fill="{paper}" {st}/>'
        f'<ellipse cx="773" cy="175" rx="4" ry="3" fill="{ink}"/>'
        f'<path d="M788 162 Q793 167 798 162" fill="none" stroke="{ink}" stroke-width="2.4" stroke-linecap="round"/>'
        + floating(heart(0, 0, 1.2, ink), 800, 130, 3.2, 0.6, 30, -6)
    )


def footer(t):
    W, H = 1000, 240
    defs, back, edge = card(W, H, t)
    ink, muted = t["ink"], t["muted"]
    body = (
        back
        + text(500, 84, "Thanks for stopping by!", 34, ink, 800, "middle", -0.5)
        + text(500, 118, "learn  →  build  →  ship  →  repeat", 14, muted, 500, "middle", 2, MONO)
        + f'<g transform="translate(500 158)"><rect x="-150" y="-19" width="300" height="34" rx="17" fill="{t["paper"]}" stroke="{ink}" stroke-width="2"/>'
        + text(0, 3, "ronaksingh18062005@gmail.com", 13, ink, 600, "middle", 0.5, MONO)
        + "</g>"
        + ground(70, 260, 203, t) + ground(740, 950, 203, t)
        + sleeping_cat(t)
        + lying_dog(t)
        + paw_trail(W, 222, 18, ink, 0.7, 8)
        + edge
    )
    return svg(W, H, body, defs)


# ---- project banners (animated, one per project) -----------------------------
def banner_base(t, title, sub):
    W, H = 480, 170
    defs, back, edge = card(W, H, t)
    return W, H, defs, back, edge, (
        text(24, 38, title, 20, t["ink"], 800, "start", -0.3)
        + text(24, 58, sub, 11, t["muted"], 500, "start", 1.5, MONO)
    )


def finsight(t):
    ink, muted, soft = t["ink"], t["muted"], t["soft"]
    W, H, defs, back, edge, head = banner_base(t, "FinSight AI", "MARKETS  ·  PORTFOLIO  ·  GEMINI")
    pts = [(24, 140), (80, 118), (130, 128), (190, 92), (250, 104), (310, 70), (370, 84), (430, 44)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    grid = "".join(f'<line x1="24" y1="{y}" x2="456" y2="{y}" stroke="{soft}" stroke-width="1.5" stroke-dasharray="3 6"/>' for y in (80, 110, 140))
    bars = "".join(
        f'<rect x="{x}" y="{150 - h}" width="10" height="{h}" rx="2" fill="{soft}"><animate attributeName="height" values="{h};{h + 12};{h}" dur="{2 + i * 0.3}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{150 - h};{138 - h};{150 - h}" dur="{2 + i * 0.3}s" repeatCount="indefinite"/></rect>'
        for i, (x, h) in enumerate(zip(range(34, 450, 52), (14, 22, 18, 30, 24, 36, 28, 40)))
    )
    line = (
        f'<path d="{d}" pathLength="100" fill="none" stroke="{ink}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100">'
        f'<animate attributeName="stroke-dashoffset" values="100;0;0;0" keyTimes="0;0.5;0.9;1" dur="5s" repeatCount="indefinite"/></path>'
    )
    dot = (
        f'<circle r="6" fill="{ink}"><animateMotion path="{d}" dur="5s" keyPoints="0;1;1" keyTimes="0;0.5;1" calcMode="linear" repeatCount="indefinite"/></circle>'
    )
    tag = (
        f'<g transform="translate(372 24)" opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.45;0.55;0.9;1" dur="5s" repeatCount="indefinite"/>'
        f'<rect width="84" height="26" rx="13" fill="{t["paper"]}" stroke="{ink}" stroke-width="2"/>' + text(42, 17.5, "+12.4%", 12, ink, 700, "middle", 0.5, MONO) + "</g>"
    )
    return svg(W, H, back + head + grid + bars + line + dot + tag + edge, defs)


def kinematics(t):
    ink, muted, soft, paper = t["ink"], t["muted"], t["soft"], t["paper"]
    W, H, defs, back, edge, head = banner_base(t, "Kinematics Sim", "3-DOF  ·  DENAVIT-HARTENBERG  ·  C++")
    rot = lambda a, b, dur: (
        f'<animateTransform attributeName="transform" type="rotate" values="{a};{b};{a}" keyTimes="0;0.5;1" calcMode="spline" '
        f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}s" repeatCount="indefinite"/>'
    )
    arm = (
        f'<g transform="translate(330 148)">'
        f'<rect x="-34" y="0" width="68" height="10" rx="5" fill="{ink}"/>'
        f'<g>{rot(-55, -115, 4)}<line x1="0" y1="0" x2="62" y2="0" stroke="{ink}" stroke-width="9" stroke-linecap="round"/>'
        f'<g transform="translate(62 0)"><g>{rot(35, -40, 4)}<line x1="0" y1="0" x2="50" y2="0" stroke="{muted}" stroke-width="7" stroke-linecap="round"/>'
        f'<g transform="translate(50 0)"><g>{rot(20, -25, 4)}<line x1="0" y1="0" x2="26" y2="0" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>'
        f'<circle cx="28" r="5" fill="{paper}" stroke="{ink}" stroke-width="2.5"/></g></g>'
        f'<circle r="6" fill="{paper}" stroke="{ink}" stroke-width="2.5"/></g></g>'
        f'<circle r="7" fill="{paper}" stroke="{ink}" stroke-width="2.5"/></g></g>'
    )
    mat = "".join(
        text(24, 92 + i * 17, row.replace(" ", "\u00a0"), 12, muted, 500, "start", 1, MONO) for i, row in enumerate(("[ c  -s   0   a·c ]", "[ s   c   0   a·s ]", "[ 0   0   1    d  ]", "[ 0   0   0    1  ]"))
    )
    return svg(W, H, back + head + mat + arm + edge, defs)


def movies(t):
    ink, muted, soft, paper = t["ink"], t["muted"], t["soft"], t["paper"]
    W, H, defs, back, edge, head = banner_base(t, "Movie Explorer", "IMDB TOP 250  ·  VANILLA JS")
    frames = "".join(
        f'<g transform="translate({i * 80} 0)"><rect x="6" y="92" width="68" height="52" rx="5" fill="{paper}" stroke="{ink}" stroke-width="2.5"/>'
        f'<path transform="translate(40 118) scale(1.5)" d="M0 -8 L2.4 -2.5 L8 -2 L3.8 2 L5 8 L0 5 L-5 8 L-3.8 2 L-8 -2 L-2.4 -2.5 Z" fill="{ink if i % 2 == 0 else soft}"/>'
        + "".join(f'<rect x="{x + 6}" y="{y}" width="8" height="6" rx="1.5" fill="{ink}"/>' for x in (0, 20, 40, 60) for y in (80, 148))
        + "</g>"
        for i in range(8)
    )
    strip = (
        f'<g><animateTransform attributeName="transform" type="translate" from="0 0" to="-160 0" dur="4s" repeatCount="indefinite"/>{frames}</g>'
    )
    clip = f'<clipPath id="s"><rect x="0" y="70" width="{W}" height="100"/></clipPath>'
    return svg(W, H, back + head + f'<g clip-path="url(#s)">{strip}</g>' + edge, defs + clip)


# ---- journey timeline ----------------------------------------------------------
def journey(t):
    W, H = 1000, 170
    defs, back, edge = card(W, H, t)
    ink, muted, paper = t["ink"], t["muted"], t["paper"]
    steps = [("B.Tech EE", "engineering base"), ("DSA in C++", "LeetCode daily"), ("FinSight AI", "MERN + Gemini"), ("PupMeow", "live in Delhi NCR")]
    xs = [130, 377, 623, 870]
    line = (
        f'<line x1="{xs[0]}" y1="78" x2="{xs[-1]}" y2="78" stroke="{ink}" stroke-width="3" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
        f'<animate attributeName="stroke-dashoffset" values="100;0;0;0" keyTimes="0;0.55;0.95;1" dur="8s" repeatCount="indefinite"/></line>'
    )
    nodes = ""
    for i, ((a, b), x) in enumerate(zip(steps, xs)):
        beg = 8 * 0.55 * i / (len(steps) - 1)
        pop = (
            f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{beg / 8:.3f};{beg / 8 + 0.04:.3f};0.95;1" dur="8s" repeatCount="indefinite"/>'
        )
        nodes += (
            f'<g opacity="0">{pop}<circle cx="{x}" cy="78" r="12" fill="{paper}" stroke="{ink}" stroke-width="3"/><circle cx="{x}" cy="78" r="4.5" fill="{ink}"/>'
            + text(x, 118, a, 17, ink, 800)
            + text(x, 140, b, 12, muted, 500, "middle", 1, MONO)
            + "</g>"
        )
    now = (
        f'<g transform="translate({xs[-1]} 78)"><circle r="12" fill="none" stroke="{ink}" stroke-width="2"><animate attributeName="r" values="12;26" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.7;0" dur="2s" repeatCount="indefinite"/></circle></g>'
    )
    body = back + text(500, 42, "THE JOURNEY SO FAR", 13, muted, 700, "middle", 5, MONO) + line + nodes + now + edge
    return svg(W, H, body, defs)


# ---- open to work pill -------------------------------------------------------
def open_pill(t):
    W, H = 520, 46
    ink, paper = t["ink"], t["paper"]
    body = (
        f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="21" fill="{paper}" stroke="{ink}" stroke-width="2"/>'
        f'<circle cx="30" cy="23" r="6" fill="{ink}"/>'
        f'<circle cx="30" cy="23" r="6" fill="none" stroke="{ink}" stroke-width="2"><animate attributeName="r" values="6;16" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0" dur="1.8s" repeatCount="indefinite"/></circle>'
        + text(52, 28, "OPEN TO WORK  ·  Product / Analyst internships & placements", 13, ink, 700, "start", 1, MONO)
    )
    return svg(W, H, body)


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


if __name__ == "__main__":
    for mode, t in THEMES.items():
        write(f"header-{mode}.svg", header(t))
        write(f"pupmeow-walk-{mode}.svg", pupmeow_walk(t))
        write(f"paws-{mode}.svg", paws(t))
        write(f"footer-{mode}.svg", footer(t))
        write(f"finsight-{mode}.svg", finsight(t))
        write(f"kinematics-{mode}.svg", kinematics(t))
        write(f"movies-{mode}.svg", movies(t))
        write(f"journey-{mode}.svg", journey(t))
        write(f"open-{mode}.svg", open_pill(t))
