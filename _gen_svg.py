# -*- coding: utf-8 -*-
"""Generates the inline SVG graphics. viewBox widths are ~1000 units so the
figures render close to 1:1 at desktop width and scale down cleanly."""
import os
OUT = "_svg"
MONO = 'font-family="IBM Plex Mono, ui-monospace, monospace"'
SANS = 'font-family="Libre Franklin, Helvetica Neue, Arial, sans-serif"'
W = 1000

# ---------------------------------------------------------------- 1. enforcement gap
def enforcement_gap():
    sq, gap, per_row = 34, 8, 16
    gw = per_row * sq + (per_row - 1) * gap          # 664
    def grid(filled):
        out = []
        for i in range(32):
            r, c = divmod(i, per_row)
            x, y = c * (sq + gap), r * (sq + gap)
            if i < filled:
                out.append(f'<rect x="{x}" y="{y}" width="{sq}" height="{sq}" fill="var(--flag)"/>')
            else:
                out.append(f'<rect x="{x}" y="{y}" width="{sq}" height="{sq}" fill="var(--paper)" stroke="var(--rule)" stroke-width="1.2"/>')
        return "\n    ".join(out)
    return f'''<svg viewBox="0 0 {W} 250" role="img" aria-labelledby="gapT gapD" xmlns="http://www.w3.org/2000/svg">
  <title id="gapT">DCWP&#8217;s review versus the Comptroller&#8217;s review of the same 32 companies</title>
  <desc id="gapD">Of 32 companies&#8217; bias audits and websites reviewed, DCWP identified one instance of non-compliance. The State Comptroller, reviewing the same 32, identified at least 17 instances of potential non-compliance.</desc>

  <text x="0" y="12" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">DCWP&#8217;S OWN REVIEW OF 32 COMPANIES</text>
  <text x="{gw}" y="12" text-anchor="end" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">1 FLAGGED</text>
  <g transform="translate(0,26)">
    {grid(1)}
  </g>

  <line x1="0" y1="128" x2="{gw}" y2="128" stroke="var(--rule)" stroke-width="1"/>

  <text x="0" y="154" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">THE COMPTROLLER&#8217;S REVIEW OF THE SAME 32</text>
  <text x="{gw}" y="154" text-anchor="end" {MONO} font-size="11.5" letter-spacing="1.5" font-weight="600" fill="var(--flag)">17 FLAGGED</text>
  <g transform="translate(0,168)">
    {grid(17)}
  </g>
</svg>'''

# ---------------------------------------------------------------- 2. twelve-month window
def audit_window():
    H = 210
    x0, x1 = 96, 740
    bary, barh = 96, 30
    month = (x1 - x0) / 12.0
    ticks = []
    for m in range(0, 13, 3):
        x = x0 + m * month
        ticks.append(f'<line x1="{x:.1f}" y1="{bary+barh}" x2="{x:.1f}" y2="{bary+barh+6}" stroke="var(--slate-lt)" stroke-width="1"/>')
        ticks.append(f'<text x="{x:.1f}" y="{bary+barh+21}" text-anchor="middle" {MONO} font-size="11" fill="var(--slate-lt)">{m} MO</text>')
    ticks = "\n  ".join(ticks)
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="winT winD" xmlns="http://www.w3.org/2000/svg">
  <title id="winT">The twelve-month audit validity window</title>
  <desc id="winD">A bias audit is valid for twelve months from the date it is conducted. Every use of the tool must fall inside that window, which makes the audit an annual obligation rather than a one-time clearance.</desc>
  <defs>
    <pattern id="lapsed" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="var(--flag)" stroke-width="1.8" opacity="0.45"/>
    </pattern>
  </defs>

  <text x="{x0}" y="36" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--pass)">TOOL MAY BE USED</text>
  <text x="{x1+16}" y="36" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--flag)">MAY NOT</text>

  <rect x="{x0}" y="{bary}" width="{x1-x0}" height="{barh}" fill="var(--pass-tint)" stroke="var(--pass)" stroke-width="1.2"/>
  <rect x="{x1}" y="{bary}" width="{W-x1-16}" height="{barh}" fill="url(#lapsed)" stroke="var(--flag)" stroke-width="1.2"/>

  <line x1="{x0}" y1="{bary-28}" x2="{x0}" y2="{bary+barh}" stroke="var(--ink)" stroke-width="1.5"/>
  <circle cx="{x0}" cy="{bary-28}" r="4.5" fill="var(--ink)"/>
  <text x="{x0-4}" y="{bary-38}" {SANS} font-size="14" font-weight="600" fill="var(--ink)">Audit conducted</text>

  <line x1="{x1}" y1="{bary-28}" x2="{x1}" y2="{bary+barh}" stroke="var(--flag)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <circle cx="{x1}" cy="{bary-28}" r="4.5" fill="var(--flag)"/>
  <text x="{x1}" y="{bary-38}" text-anchor="middle" {SANS} font-size="14" font-weight="600" fill="var(--flag)">Audit lapses</text>

  {ticks}
  <text x="{x0}" y="{H-12}" {MONO} font-size="11.5" fill="var(--slate)">EVERY USE OF THE TOOL MUST FALL INSIDE THE SHADED WINDOW.</text>
</svg>'''

# ---------------------------------------------------------------- 3. coverage
def coverage():
    H = 300
    bx, by, bw, bh = 560, 52, 400, 214
    labels = [("Denver", False), ("Austin", False), ("Queens, NY", True), ("Chicago", False)]
    rows = []
    for i, (lab, ins) in enumerate(labels):
        y = by + 34 + i * 40
        stroke = "var(--flag)" if ins else "var(--rule)"
        fill   = "var(--flag-tint)" if ins else "var(--paper)"
        tcol   = "var(--flag)" if ins else "var(--slate)"
        rows.append(
            f'<rect x="{bx+22}" y="{y-18}" width="{bw-44}" height="30" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
            f'<circle cx="{bx+42}" cy="{y-3}" r="5.5" fill="{tcol}" opacity="{"1" if ins else "0.4"}"/>'
            f'<text x="{bx+60}" y="{y+2}" {MONO} font-size="12.5" font-weight="{"600" if ins else "400"}" fill="{tcol}">{lab}</text>'
        )
    rows = "\n  ".join(rows)
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="covT covD" xmlns="http://www.w3.org/2000/svg">
  <title id="covT">Coverage follows the candidate, not the company</title>
  <desc id="covD">An employer headquartered outside New York, screening a pool of applicants, is covered by Local Law 144 for the evaluation of any applicant located in New York City.</desc>
  <defs>
    <marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--slate-lt)"/>
    </marker>
  </defs>

  <text x="24" y="30" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">THE EMPLOYER</text>
  <rect x="24" y="52" width="300" height="104" fill="var(--paper)" stroke="var(--rule)" stroke-width="1.2"/>
  <text x="52" y="92" {SANS} font-size="16" font-weight="600" fill="var(--ink)">Headquarters</text>
  <text x="52" y="116" {MONO} font-size="12.5" fill="var(--slate)">Anywhere</text>
  <text x="52" y="136" {MONO} font-size="12.5" fill="var(--slate-lt)">Not the test</text>

  <rect x="24" y="176" width="300" height="76" fill="var(--panel)" stroke="var(--rule)" stroke-width="1.2"/>
  <text x="52" y="208" {SANS} font-size="15" font-weight="600" fill="var(--ink)">Screening tool</text>
  <text x="52" y="232" {MONO} font-size="12.5" fill="var(--slate)">One AEDT, one posting</text>

  <path d="M336 158 L546 158" stroke="var(--slate-lt)" stroke-width="1.5" marker-end="url(#arw)"/>

  <text x="{bx}" y="30" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">THE APPLICANT POOL</text>
  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="var(--rule)" stroke-width="1.2"/>
  {rows}
  <text x="{bx+22}" y="{by+bh-30}" {MONO} font-size="11.5" fill="var(--flag)">ONE NYC APPLICANT PUTS THAT</text>
  <text x="{bx+22}" y="{by+bh-13}" {MONO} font-size="11.5" fill="var(--flag)">EVALUATION IN SCOPE.</text>
</svg>'''

# ---------------------------------------------------------------- 4. impact bars
def impact_bars():
    H = 260
    x0, axw = 150, 720
    rows = [("Group A", 1.00, "30.0%"), ("Group B", 0.60, "18.0%"), ("Group C", 0.67, "20.0%")]
    thr = x0 + axw * 0.80
    bars = []
    for i, (name, ratio, rate) in enumerate(rows):
        y = 58 + i * 52
        bwid = axw * ratio
        fail = ratio < 0.80
        col = "var(--flag)" if fail else "var(--pine)"
        bars.append(
            f'<text x="{x0-14}" y="{y+19}" text-anchor="end" {MONO} font-size="12.5" fill="var(--ink)">{name}</text>'
            f'<rect x="{x0}" y="{y}" width="{bwid:.1f}" height="28" fill="{col}"/>'
            f'<text x="{x0+bwid-11:.1f}" y="{y+19}" text-anchor="end" {MONO} font-size="12.5" font-weight="600" fill="#fff">{ratio:.2f}</text>'
            f'<text x="{x0+bwid+12:.1f}" y="{y+19}" {MONO} font-size="11.5" fill="var(--slate-lt)">rate {rate}</text>'
        )
    bars = "\n  ".join(bars)
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="irT irD" xmlns="http://www.w3.org/2000/svg">
  <title id="irT">Impact ratios against the four-fifths guideline</title>
  <desc id="irD">Group A sets the reference rate at 1.00. Group C returns 0.67 and Group B returns 0.60. Both fall below the 0.80 four-fifths guideline.</desc>

  <text x="{x0}" y="28" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">IMPACT RATIO AGAINST THE HIGHEST-SELECTED GROUP</text>
  <line x1="{thr:.1f}" y1="42" x2="{thr:.1f}" y2="{H-58}" stroke="var(--flag)" stroke-width="1.3" stroke-dasharray="5 4"/>
  <text x="{thr+10:.1f}" y="{H-62}" {MONO} font-size="12" font-weight="600" fill="var(--flag)">0.80</text>
  <text x="{thr+10:.1f}" y="{H-46}" {MONO} font-size="10.5" fill="var(--flag)">FOUR-FIFTHS</text>
  <line x1="{x0}" y1="{H-70}" x2="{x0+axw}" y2="{H-70}" stroke="var(--rule)" stroke-width="1"/>
  {bars}
  <text x="{x0}" y="{H-14}" {MONO} font-size="11.5" fill="var(--slate)">TWO OF THREE GROUPS FALL BELOW THE GUIDELINE. BOTH FIGURES STILL GET PUBLISHED.</text>
</svg>'''

# ---------------------------------------------------------------- 5. independence
def independence():
    H = 262
    excluded = [("Selling AEDT software", 24, 52), ("Implementing hiring systems", 24, 156),
                ("Vendor referral fees", 690, 52), ("Fees tied to findings", 690, 156)]
    boxes = []
    for label, x, y in excluded:
        cy = y + 27
        boxes.append(
            f'<rect x="{x}" y="{y}" width="286" height="54" fill="var(--paper)" '
            f'stroke="var(--rule)" stroke-width="1.2" stroke-dasharray="5 4"/>'
            f'<g stroke="var(--flag)" stroke-width="2" stroke-linecap="round">'
            f'<line x1="{x+20}" y1="{cy-6}" x2="{x+32}" y2="{cy+6}"/>'
            f'<line x1="{x+32}" y1="{cy-6}" x2="{x+20}" y2="{cy+6}"/></g>'
            f'<text x="{x+46}" y="{cy+5}" {MONO} font-size="12.5" fill="var(--slate)">{label}</text>'
        )
    boxes = "\n  ".join(boxes)
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="indT indD" xmlns="http://www.w3.org/2000/svg">
  <title id="indT">What independence excludes</title>
  <desc id="indD">The audit and its workpapers sit inside the practice. Selling AEDT software, implementing hiring systems, vendor referral fees, and fees tied to findings all sit outside it.</desc>

  <text x="{W//2}" y="28" text-anchor="middle" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">EVERYTHING ELSE IS OUT OF BOUNDS</text>
  <rect x="360" y="66" width="280" height="130" fill="var(--pine-tint)" stroke="var(--pine)" stroke-width="1.8"/>
  <text x="500" y="114" text-anchor="middle" {SANS} font-size="19" font-weight="700" fill="var(--pine)">The audit</text>
  <text x="500" y="142" text-anchor="middle" {MONO} font-size="11.5" letter-spacing="1.2" fill="var(--pine)">AND THE WORKPAPERS</text>
  <text x="500" y="162" text-anchor="middle" {MONO} font-size="11.5" letter-spacing="1.2" fill="var(--pine)">BEHIND IT</text>
  {boxes}
  <text x="{W//2}" y="{H-12}" text-anchor="middle" {MONO} font-size="11.5" fill="var(--slate)">NO PRODUCT TO CROSS-SELL MEANS NO INTEREST IN WHAT THE NUMBERS SAY.</text>
</svg>'''

# ---------------------------------------------------------------- 6. scope drivers
def scope_drivers():
    H = 268
    rows = [("AEDTs in scope", "One tool", "A stack of them", 0.22),
            ("Condition of your data", "Clean and complete", "Reconstructed", 0.55),
            ("Analysable group sizes", "Most categories hold", "Thin throughout", 0.38)]
    x0, axw = 330, 620
    out = []
    for i, (label, lo, hi, pos) in enumerate(rows):
        y = 74 + i * 62
        out.append(
            f'<text x="{x0-24}" y="{y+6}" text-anchor="end" {SANS} font-size="15" font-weight="600" fill="var(--ink)">{label}</text>'
            f'<line x1="{x0}" y1="{y}" x2="{x0+axw}" y2="{y}" stroke="var(--rule)" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="{x0}" y1="{y}" x2="{x0+axw*pos:.1f}" y2="{y}" stroke="var(--pine)" stroke-width="7" stroke-linecap="round"/>'
            f'<circle cx="{x0+axw*pos:.1f}" cy="{y}" r="7.5" fill="var(--paper)" stroke="var(--pine)" stroke-width="2.8"/>'
            f'<text x="{x0}" y="{y+25}" {MONO} font-size="11" fill="var(--slate-lt)">{lo.upper()}</text>'
            f'<text x="{x0+axw}" y="{y+25}" text-anchor="end" {MONO} font-size="11" fill="var(--slate-lt)">{hi.upper()}</text>'
        )
    out = "\n  ".join(out)
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="sdT sdD" xmlns="http://www.w3.org/2000/svg">
  <title id="sdT">What moves the price of an engagement</title>
  <desc id="sdD">Three factors set the fee: the number of automated employment decision tools in scope, the condition of your historical data, and how many demographic categories produce group sizes large enough to analyse.</desc>
  <text x="24" y="30" {MONO} font-size="11.5" letter-spacing="1.5" fill="var(--slate-lt)">THREE FACTORS SET THE FEE</text>
  {out}
  <text x="24" y="{H-14}" {MONO} font-size="11.5" fill="var(--slate)">HOURS ARE NOT ONE OF THEM.</text>
</svg>'''

for name, fn in [("enforcement-gap", enforcement_gap), ("audit-window", audit_window),
                 ("coverage", coverage), ("impact-bars", impact_bars),
                 ("independence", independence), ("scope-drivers", scope_drivers)]:
    open(os.path.join(OUT, name + ".svg"), "w").write(fn())
print("regenerated 6 graphics at ~1000-unit viewBox")
