"""Generate the animated SVGs used by the profile README.

Run: python3 assets/build.py   (writes into assets/)
Everything is plain SVG + CSS so GitHub renders it with no outside service.
"""
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

BG_TOP = "#0b1020"
BG_BOTTOM = "#141a33"
ACCENT = "#ff7a45"   # signal orange
ACCENT_2 = "#7dd3fc"  # sky
TEXT = "#e6edf3"
MUTED = "#8b98b5"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"


def defs(card_id: str) -> str:
    return f"""<defs>
    <linearGradient id="bg-{card_id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
    <linearGradient id="accent-{card_id}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT_2}"/>
    </linearGradient>
    <pattern id="grid-{card_id}" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#ffffff" stroke-opacity="0.04"/>
    </pattern>
  </defs>"""


def header() -> str:
    w, h = 1000, 250
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Moaiz Attiq, CS at UT Dallas">
  {defs("h")}
  <style>
    .rise {{ animation: rise .9s ease-out both; }}
    .d1 {{ animation-delay: .1s; }} .d2 {{ animation-delay: .5s; }} .d3 {{ animation-delay: .9s; }} .d4 {{ animation-delay: 1.3s; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .scan {{ animation: scan 6s linear infinite; }}
    @keyframes scan {{ from {{ transform: translateX(-300px); }} to {{ transform: translateX(1100px); }} }}
    .pulse {{ animation: pulse 1.6s ease-in-out infinite; transform-origin: 72px 210px; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
    .cursor {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
  </style>
  <rect width="{w}" height="{h}" rx="18" fill="url(#bg-h)"/>
  <rect width="{w}" height="{h}" rx="18" fill="url(#grid-h)"/>
  <rect class="scan" x="0" y="0" width="220" height="{h}" fill="url(#accent-h)" opacity="0.06"/>
  <rect x="0" y="{h - 4}" width="{w}" height="4" fill="url(#accent-h)"/>

  <text class="rise d1" x="56" y="62" font-family="{MONO}" font-size="16" fill="{MUTED}">~/github/moaizattiq <tspan fill="{ACCENT}">$</tspan> whoami<tspan class="cursor" fill="{ACCENT}">▍</tspan></text>
  <text class="rise d2" x="54" y="124" font-family="{SANS}" font-size="64" font-weight="800" fill="{TEXT}" letter-spacing="-1.5">Moaiz Attiq</text>
  <text class="rise d3" x="56" y="164" font-family="{SANS}" font-size="22" fill="{MUTED}">CS @ <tspan fill="{TEXT}" font-weight="600">UT Dallas</tspan>  ·  builds things from scratch, then measures them</text>

  <g class="rise d4">
    <rect x="56" y="194" width="310" height="32" rx="16" fill="#ffffff" fill-opacity="0.06" stroke="{ACCENT}" stroke-opacity="0.5"/>
    <circle class="pulse" cx="72" cy="210" r="5" fill="#3fb950"/>
    <text x="86" y="215" font-family="{MONO}" font-size="13" fill="{TEXT}">open to Summer 2027 SWE internships</text>
  </g>

  <g class="rise d3" font-family="{MONO}" font-size="13" fill="{MUTED}" text-anchor="end">
    <text x="944" y="62"><tspan fill="{ACCENT_2}">35×</tspan> faster than Postgres FTS</text>
    <text x="944" y="86"><tspan fill="{ACCENT_2}">376,748</tspan> calls forecast</text>
  </g>
</svg>
"""


TERMINAL_LINES = [
    ("cmd", "whoami"),
    ("out", "moaiz attiq · cs @ ut dallas · class of 2029"),
    ("cmd", "cat now.txt"),
    ("out", "→ leading a 6-person forecasting team for Vets4Warriors"),
    ("out", "→ looking for a Summer 2027 SWE internship"),
]


def terminal() -> str:
    w = 1000
    line_h = 26
    top = 70
    h = top + line_h * len(TERMINAL_LINES) + 30
    rows = []
    for i, (kind, text) in enumerate(TERMINAL_LINES):
        y = top + i * line_h
        delay = 0.35 + i * 0.45
        body = escape(text)
        if kind == "cmd":
            content = f'<tspan fill="{ACCENT}">❯</tspan> <tspan fill="{TEXT}">{body}</tspan>'
        elif kind == "win":
            content = f'<tspan fill="#3fb950">{body}</tspan>'
        elif kind == "motto":
            content = f'<tspan fill="{ACCENT_2}" font-style="italic">{body}</tspan>'
        else:
            content = f'<tspan fill="{MUTED}">{body}</tspan>'
        rows.append(
            f'  <text class="ln" style="animation-delay:{delay:.2f}s" x="36" y="{y}" '
            f'font-family="{MONO}" font-size="15">{content}</text>'
        )
    last_y = top + (len(TERMINAL_LINES)) * line_h
    cursor_delay = 0.35 + len(TERMINAL_LINES) * 0.45
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Terminal: who I am, what I am doing now, wins">
  {defs("t")}
  <style>
    .ln {{ animation: show .25s ease-out both; }}
    @keyframes show {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    .cursor {{ animation: blink 1s step-end infinite {cursor_delay:.2f}s; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
  </style>
  <rect width="{w}" height="{h}" rx="14" fill="url(#bg-t)"/>
  <rect width="{w}" height="{h}" rx="14" fill="url(#grid-t)"/>
  <rect width="{w}" height="38" rx="14" fill="#ffffff" fill-opacity="0.04"/>
  <circle cx="26" cy="19" r="6" fill="#ff5f57"/><circle cx="46" cy="19" r="6" fill="#febc2e"/><circle cx="66" cy="19" r="6" fill="#28c840"/>
  <text x="{w // 2}" y="24" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">moaiz@utd: ~</text>
{chr(10).join(rows)}
  <text class="cursor" x="36" y="{last_y}" font-family="{MONO}" font-size="15" fill="{ACCENT}">❯ ▍</text>
</svg>
"""


PROJECTS = [
    {
        "slug": "oneflow",
        "title": "OneFlow",
        "tag": "HackUTD 2026",
        "metric": "739 tests",
        "desc": "Projects 24 months of cash flow and ranks your next money move by dollar impact.",
        "stack": ["TypeScript", "Next.js", "PostgreSQL", "Gemini"],
    },
    {
        "slug": "trail-search",
        "title": "Trail Search",
        "tag": "Built from scratch",
        "metric": "35× faster than Postgres",
        "desc": "Hand-written tokenizer, inverted index and BM25. No search libraries.",
        "stack": ["Python", "FastAPI", "PostgreSQL", "React"],
    },
    {
        "slug": "vets4war",
        "title": "Vets4Warriors Forecast",
        "tag": "UT Dallas EPICS · Project lead",
        "metric": "89–94% daily accuracy",
        "desc": "Forecasts calls to a 24/7 veteran support line and turns them into staffing.",
        "stack": ["Python", "LightGBM", "FastAPI", "Nuxt"],
    },
    {
        "slug": "sentinel-live",
        "title": "Sentinel Live",
        "tag": "Hook 'em Hacks",
        "metric": "117 tests in 24 hours",
        "desc": "Flags patients getting worse after discharge from voice check-ins and wearables.",
        "stack": ["TypeScript", "Python", "FastAPI", "MongoDB"],
    },
    {
        "slug": "elephantvoices",
        "title": "ElephantVoices Cleaner",
        "tag": "HackSMU VII",
        "metric": "8–50 Hz rumbles",
        "desc": "Finds elephant calls below human hearing in noisy field recordings.",
        "stack": ["Python", "PyTorch", "DSP"],
    },
    {
        "slug": "wwm-crm",
        "title": "Walk With Me CRM",
        "tag": "UT Dallas EPICS",
        "metric": "500+ records in daily use",
        "desc": "Data tool a nonprofit's staff use every day.",
        "stack": ["TypeScript", "Vue"],
    },
]

CARD_W, CARD_H = 480, 200
CHAR_W = 7.9  # approx width of a 13px monospace glyph


def chip_row(stack: list[str], y: int) -> str:
    x = 28
    parts = []
    for name in stack:
        width = int(len(name) * 7.3 + 22)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="24" rx="12" fill="#ffffff" fill-opacity="0.06" stroke="{ACCENT_2}" stroke-opacity="0.35"/>'
            f'<text x="{x + width / 2}" y="{y + 16}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{ACCENT_2}">{escape(name)}</text>'
        )
        x += width + 8
    return "\n  ".join(parts)


def card(p: dict) -> str:
    cid = p["slug"]
    max_chars = int((CARD_W - 56) / CHAR_W)
    lines = wrap(p["desc"], max_chars)[:2]
    desc = "\n  ".join(
        f'<text x="28" y="{122 + i * 20}" font-family="{MONO}" font-size="13" fill="{MUTED}">{escape(t)}</text>'
        for i, t in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" role="img" aria-label="{escape(p['title'])}: {escape(p['metric'])}">
  {defs(cid)}
  <style>
    .glow {{ animation: glow 3s ease-in-out infinite; }}
    @keyframes glow {{ 0%,100% {{ stroke-opacity: .25; }} 50% {{ stroke-opacity: .7; }} }}
  </style>
  <rect x="1" y="1" width="{CARD_W - 2}" height="{CARD_H - 2}" rx="16" fill="url(#bg-{cid})"/>
  <rect x="1" y="1" width="{CARD_W - 2}" height="{CARD_H - 2}" rx="16" fill="url(#grid-{cid})"/>
  <rect class="glow" x="1" y="1" width="{CARD_W - 2}" height="{CARD_H - 2}" rx="16" fill="none" stroke="url(#accent-{cid})" stroke-width="2"/>
  <rect x="28" y="0" width="56" height="4" rx="2" fill="url(#accent-{cid})"/>
  <text x="28" y="44" font-family="{MONO}" font-size="12" fill="{ACCENT}">{escape(p['tag'])}</text>
  <text x="28" y="76" font-family="{SANS}" font-size="26" font-weight="800" fill="{TEXT}">{escape(p['title'])}</text>
  <text x="28" y="100" font-family="{MONO}" font-size="14" font-weight="700" fill="{ACCENT_2}">{escape(p['metric'])}</text>
  {desc}
  {chip_row(p['stack'], CARD_H - 44)}
</svg>
"""


def main() -> None:
    (OUT / "header.svg").write_text(header(), encoding="utf-8")
    (OUT / "terminal.svg").write_text(terminal(), encoding="utf-8")
    for p in PROJECTS:
        (OUT / f"card-{p['slug']}.svg").write_text(card(p), encoding="utf-8")
    print("wrote", 2 + len(PROJECTS), "svgs to", OUT)


if __name__ == "__main__":
    main()
