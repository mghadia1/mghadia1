#!/usr/bin/env python3
"""Generates the animated profile hero SVGs (dark + light variants).

Run:  python3 _hero_template.py
Writes hero-dark.svg and hero-light.svg next to this file.

Design notes: the motif is a segmentation scan — a sweeping scanline over
contour outlines that trace themselves, echoing the U-Net work in surgiseg-ml.
Everything is inline SMIL/CSS so GitHub's image proxy serves it unmodified.
"""
import pathlib

THEMES = {
    "dark": dict(
        bg0="#050b12", bg1="#0b1f26", bg2="#123039",
        grid="#2dd4bf", grid_op="0.10",
        name="#eaf6f4", tag="#8fded3", muted="#6f9aa3",
        accent="#2dd4bf", accent2="#5eead4",
        pill_bg="#0e2a32", pill_stroke="#1f5c66", pill_text="#a7ede2",
        contour="#2dd4bf", scan="#5eead4", glow_op="0.28",
    ),
    "light": dict(
        bg0="#f6fbfb", bg1="#e6f4f2", bg2="#d6ece9",
        grid="#0f766e", grid_op="0.14",
        name="#08282b", tag="#0f766e", muted="#4b7a80",
        accent="#0d9488", accent2="#0f766e",
        pill_bg="#ffffff", pill_stroke="#a7d5cf", pill_text="#0f766e",
        contour="#0d9488", scan="#14b8a6", glow_op="0.18",
    ),
}

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="270" viewBox="0 0 1000 270" role="img" aria-label="Mayank Ghadia — Machine Learning, Computer Vision, Applied ML Systems">
  <title>Mayank Ghadia — Machine Learning, Computer Vision, Applied ML Systems</title>
  <defs>
    <linearGradient id="bg-{ns}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg0}"/>
      <stop offset="55%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="scanGrad-{ns}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{scan}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{scan}" stop-opacity="{glow_op}"/>
      <stop offset="100%" stop-color="{scan}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ruleGrad-{ns}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{accent2}" stop-opacity="0.15"/>
    </linearGradient>
    <pattern id="dots-{ns}" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.5" fill="{grid}" fill-opacity="{grid_op}"/>
    </pattern>
    <clipPath id="frame-{ns}"><rect width="1000" height="270" rx="14"/></clipPath>
  </defs>

  <g clip-path="url(#frame-{ns})">
    <rect width="1000" height="270" fill="url(#bg-{ns})"/>
    <rect width="1000" height="270" fill="url(#dots-{ns})"/>

    <!-- segmentation contours that trace themselves, right side -->
    <g fill="none" stroke="{contour}" stroke-width="1.6" stroke-linecap="round" opacity="0.55">
      <path d="M700 74 C 762 42, 856 56, 892 104 C 926 150, 900 206, 840 218 C 776 231, 714 202, 700 156 C 690 124, 690 96, 700 74 Z"
            stroke-dasharray="900" stroke-dashoffset="900">
        <animate attributeName="stroke-dashoffset" from="900" to="0" dur="3.2s" begin="0.2s" fill="freeze"/>
        <animate attributeName="opacity" values="0.75;0.4;0.75" dur="5s" begin="3.4s" repeatCount="indefinite"/>
      </path>
      <path d="M742 116 C 776 96, 838 102, 856 136 C 872 168, 848 196, 810 198 C 772 200, 742 178, 738 152 C 736 138, 736 126, 742 116 Z"
            stroke-dasharray="620" stroke-dashoffset="620" opacity="0.7">
        <animate attributeName="stroke-dashoffset" from="620" to="0" dur="2.6s" begin="0.9s" fill="freeze"/>
      </path>
      <circle cx="800" cy="150" r="4" fill="{contour}" stroke="none" opacity="0">
        <animate attributeName="opacity" values="0;1;0.35;1" dur="4s" begin="3s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- sweeping scanline -->
    <g>
      <rect x="-260" y="0" width="260" height="270" fill="url(#scanGrad-{ns})">
        <animate attributeName="x" from="-260" to="1000" dur="6.5s" repeatCount="indefinite"/>
      </rect>
      <rect x="-260" y="0" width="1.5" height="270" fill="{scan}" opacity="0.5">
        <animate attributeName="x" from="-130" to="1130" dur="6.5s" repeatCount="indefinite"/>
      </rect>
    </g>

    <!-- name + rule + tagline -->
    <g font-family="ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
      <text x="60" y="106" fill="{name}" font-size="52" font-weight="700" letter-spacing="-1.2">Mayank Ghadia</text>

      <rect x="62" y="126" width="0" height="3" rx="1.5" fill="url(#ruleGrad-{ns})">
        <animate attributeName="width" from="0" to="330" dur="1.1s" begin="0.35s" fill="freeze"/>
      </rect>

      <text x="62" y="164" fill="{tag}" font-size="17.5" font-weight="500" opacity="0">
        Machine Learning · Computer Vision · Applied ML Systems
        <animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="0.8s" fill="freeze"/>
      </text>

      <text x="62" y="192" fill="{muted}" font-size="13.5"
            font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace" opacity="0">
        CS senior @ Arizona State University · graduating Dec 2027
        <animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="1.1s" fill="freeze"/>
      </text>
    </g>

    <!-- focus pills -->
    <g font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace" font-size="12.5">
      {pills}
    </g>

    <rect x="0.5" y="0.5" width="999" height="269" rx="14" fill="none" stroke="{accent}" stroke-opacity="0.22"/>
  </g>
</svg>
"""

PILL = """<g opacity="0">
        <rect x="{x}" y="216" width="{w}" height="28" rx="14" fill="{pill_bg}" stroke="{pill_stroke}"/>
        <text x="{tx}" y="234.5" fill="{pill_text}">{label}</text>
        <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{begin}s" fill="freeze"/>
      </g>"""


def build(theme: dict, ns: str) -> str:
    x, pills = 62, []
    for i, label in enumerate(["real data", "held-out eval", "tests + CI"]):
        w = 22 + len(label) * 7.6
        pills.append(PILL.format(x=x, w=round(w, 1), tx=x + 11, label=label,
                                 begin=round(1.35 + i * 0.18, 2), **theme))
        x += w + 10
    return SVG.format(pills="\n      ".join(pills), ns=ns, **theme)


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for name, theme in THEMES.items():
        (here / f"hero-{name}.svg").write_text(build(theme, name))
        print(f"wrote hero-{name}.svg")
