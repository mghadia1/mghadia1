#!/usr/bin/env python3
"""Generates the animated section-banner SVGs (dark + light for each section).

Run:  python3 _sections_template.py
Writes section-<id>-<theme>.svg next to this file.

These are slimmer siblings of the main hero: same palette and dot-grid, but
quieter, so they separate sections without competing with the top banner.
Each carries a motif that says something about its own section — a terminal
for the bio, twelve dots for the twelve projects, a sparkline for activity.
"""
import pathlib

from _hero_template import THEMES

W, H = 1000, 92

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{num} — {title}">
  <title>{num} — {title}</title>
  <defs>
    <linearGradient id="bg-{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg0}"/>
    </linearGradient>
    <linearGradient id="sheen-{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{scan}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{scan}" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="{scan}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="dots-{uid}" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.5" fill="{grid}" fill-opacity="{grid_op}"/>
    </pattern>
    <clipPath id="frame-{uid}"><rect width="{w}" height="{h}" rx="10"/></clipPath>
  </defs>

  <g clip-path="url(#frame-{uid})">
    <rect width="{w}" height="{h}" fill="url(#bg-{uid})"/>
    <rect width="{w}" height="{h}" fill="url(#dots-{uid})"/>

    <rect x="-200" y="0" width="200" height="{h}" fill="url(#sheen-{uid})">
      <animate attributeName="x" from="-200" to="{w}" dur="7s" repeatCount="indefinite"/>
    </rect>

    <rect x="0" y="0" width="4" height="{h}" fill="{accent}"/>

    <text x="30" y="64" fill="{accent}" fill-opacity="0.18" font-size="44" font-weight="700"
          font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace">{num}</text>

    <text x="100" y="55" fill="{name}" font-size="21" font-weight="700" letter-spacing="3.4"
          font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">{title}</text>

    <text x="101" y="72" fill="{muted}" font-size="11" letter-spacing="0.6"
          font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace">{sub}</text>

    {motif}

    <rect x="0.5" y="0.5" width="{w1}" height="{h1}" rx="10" fill="none" stroke="{accent}" stroke-opacity="0.20"/>
  </g>
</svg>
"""


def terminal(t):
    """Bio section: a small terminal window with a blinking cursor."""
    return f"""<g>
      <rect x="812" y="20" width="146" height="52" rx="6" fill="{t['pill_bg']}" stroke="{t['pill_stroke']}"/>
      <circle cx="824" cy="31" r="2.6" fill="{t['contour']}" fill-opacity="0.75"/>
      <circle cx="833" cy="31" r="2.6" fill="{t['contour']}" fill-opacity="0.45"/>
      <circle cx="842" cy="31" r="2.6" fill="{t['contour']}" fill-opacity="0.25"/>
      <rect x="824" y="44" width="62" height="4" rx="2" fill="{t['contour']}" fill-opacity="0.55"/>
      <rect x="824" y="56" width="94" height="4" rx="2" fill="{t['contour']}" fill-opacity="0.3"/>
      <rect x="892" y="42" width="8" height="8" rx="1" fill="{t['accent']}">
        <animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/>
      </rect>
    </g>"""


def cards(t):
    """Selected work: four panels, one highlighted in rotation."""
    out = []
    for i, (x, y) in enumerate([(838, 22), (886, 22), (838, 50), (886, 50)]):
        out.append(
            f"""<rect x="{x}" y="{y}" width="40" height="22" rx="4" fill="{t['pill_bg']}" stroke="{t['pill_stroke']}"/>
      <rect x="{x}" y="{y}" width="40" height="22" rx="4" fill="{t['accent']}" opacity="0">
        <animate attributeName="opacity" values="0;0.5;0" dur="4.4s" begin="{i * 1.1}s" repeatCount="indefinite"/>
      </rect>""")
    return "<g>\n      " + "\n      ".join(out) + "\n    </g>"


def twelve(t):
    """Projects: exactly twelve dots, one per public repo, lighting up in turn."""
    out = []
    i = 0
    for row in range(3):
        for col in range(4):
            cx, cy = 846 + col * 26, 26 + row * 20
            out.append(
                f"""<circle cx="{cx}" cy="{cy}" r="4.5" fill="{t['contour']}" fill-opacity="0.28">
        <animate attributeName="fill-opacity" values="0.28;1;0.28" dur="5s" begin="{round(i * 0.22, 2)}s" repeatCount="indefinite"/>
      </circle>""")
            i += 1
    return "<g>\n      " + "\n      ".join(out) + "\n    </g>"


def bars(t):
    """Toolkit: three stacked bars that draw themselves in."""
    out = []
    for i, (y, w) in enumerate([(30, 104), (43, 74), (56, 92)]):
        out.append(
            f"""<rect x="846" y="{y}" width="0" height="6" rx="3" fill="{t['contour']}" fill-opacity="{0.75 - i * 0.2:.2f}">
        <animate attributeName="width" from="0" to="{w}" dur="1s" begin="{round(0.2 + i * 0.18, 2)}s" fill="freeze"/>
      </rect>""")
    return "<g>\n      " + "\n      ".join(out) + "\n    </g>"


def spark(t):
    """Activity: a sparkline that draws itself, with a dot riding the last peak."""
    pts = "832,64 852,52 868,58 884,34 900,46 916,28 934,40 952,24"
    return f"""<g fill="none" stroke="{t['contour']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="{pts}" stroke-dasharray="320" stroke-dashoffset="320" opacity="0.85">
        <animate attributeName="stroke-dashoffset" from="320" to="0" dur="2.2s" begin="0.3s" fill="freeze"/>
      </polyline>
      <circle cx="952" cy="24" r="3.5" fill="{t['accent']}" stroke="none" opacity="0">
        <animate attributeName="opacity" values="0;1;0.3;1" dur="3s" begin="2.4s" repeatCount="indefinite"/>
      </circle>
    </g>"""


SECTIONS = [
    ("whoami", "01", "WHO AM I", "cs senior @ asu · graduating dec 2027", terminal),
    ("work", "02", "SELECTED WORK", "the four i can defend line by line", cards),
    ("projects", "03", "ALL TWELVE PROJECTS", "every repo public · every workflow green", twelve),
    ("toolkit", "04", "TOOLKIT", "what i actually reach for", bars),
    ("activity", "05", "ACTIVITY", "commits, languages, and cadence", spark),
]


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for sid, num, title, sub, motif in SECTIONS:
        for tname, theme in THEMES.items():
            svg = SVG.format(w=W, h=H, w1=W - 1, h1=H - 1, uid=f"{sid}-{tname}",
                             num=num, title=title, sub=sub,
                             motif=motif(theme), **theme)
            (here / f"section-{sid}-{tname}.svg").write_text(svg)
        print(f"wrote section-{sid}-<dark|light>.svg")
