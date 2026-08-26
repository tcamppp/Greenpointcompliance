# -*- coding: utf-8 -*-
"""Assembles the Greenpoint Compliance static site."""
import io, os

SITE  = "https://greenpointcompliance.com"
EMAIL = "hello@greenpointcompliance.com"

def svg(name):
    with io.open(os.path.join("_svg", name + ".svg"), encoding="utf-8") as f:
        return f.read()

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=IBM+Plex+Mono:wght@400;500;600"
         "&family=Libre+Franklin:wght@500;600;700"
         "&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400"
         "&display=swap")

FAVICON = ("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27%3E"
           "%3Cpath d=%27M2 2h20v16l-6 4H2z%27 fill=%27%2314402D%27/%3E%3C/svg%3E")

MARK = ('<svg class="mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path d="M2 2h20v16l-6 4H2z" fill="#14402D"/>'
        '<path d="M6.5 9.5h11M6.5 13.5h7" stroke="#fff" stroke-width="1.7" stroke-linecap="square"/>'
        '</svg>')

NAV = [
    ("nyc-local-law-144-bias-audit-guide.html", "Guide"),
    ("four-fifths-rule-calculator.html", "Calculator"),
    ("services.html", "Services"),
    ("about.html", "About"),
]

def head(title, desc, canonical, og_type="website", extra="", og_image=None):
    og = f'<meta property="og:image" content="{SITE}/{og_image}">\n' if og_image else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{canonical}">
{og}<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{extra}</head>
<body>'''

def chrome(current):
    def link(h, l):
        cur = ' aria-current="page"' if h == current else ''
        return '<a href="%s"%s>%s</a>' % (h, cur, l)
    nav = "\n".join(link(h, l) for h, l in NAV)
    return f'''<div class="cta-bar"><div class="wrap">
<span><strong>State Comptroller, December 2025:</strong> DCWP flagged 1 of 32 employers reviewed. The Comptroller found 17.</span>
<span class="dot">&mdash;</span>
<a href="mailto:{EMAIL}">Book a free scoping call &rarr;</a>
</div></div>
<header class="site-head"><div class="wrap">
<a class="brand" href="index.html">{MARK}Greenpoint</a>
<nav class="site-nav" aria-label="Main">
{nav}
</nav></div></header>'''

def cta_band(h2, p):
    return f'''<section class="cta-band"><div class="wrap">
<h2>{h2}</h2>
<p>{p}</p>
<a class="btn btn-solid" href="mailto:{EMAIL}">{EMAIL}</a>
</div></section>'''

FOOT_LINKS = " &middot; ".join(f'<a href="{h}">{l}</a>' for h, l in NAV) + ' &middot; <a href="legal.html">Legal &amp; Privacy</a>'

FOOTER = f'''</main>
<footer class="site-foot"><div class="wrap">
<div><p><strong>Greenpoint AI Compliance LLC</strong><br>418 Broadway, Ste R<br>Albany, NY 12207</p>
<p>{FOOT_LINKS}</p></div>
<p class="disclaimer">Greenpoint AI Compliance LLC provides regulatory consulting and independent assessment services. Nothing on this site is legal advice, and no attorney&ndash;client relationship is created by using it or by contacting us. See <a href="legal.html">Legal &amp; Privacy</a>.</p>
</div></footer>
</body>
</html>
'''

def write(name, parts):
    with io.open(name, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("wrote", name)

# ============================================================ the six questions
SIX = [
    ("Did you take any part in developing, testing, training or selling the tool you are being asked to audit?",
     "No. Greenpoint does not build, sell, license, resell or implement AEDTs, applicant tracking systems or assessment platforms."),
    ("Who performs the disparate impact analysis, and what is their background?",
     "One named person, with a compliance and regulatory testing background. The work is not handed to a subcontractor you never meet."),
    ("Will you publish your methodology, or only the results?",
     "The methodology goes in the report, alongside the figures. If you cannot see how a number was reached, you cannot defend it."),
    ("Is any part of your fee tied to what the audit finds?",
     "No. The fee is fixed and agreed in writing before the work starts. It does not move based on the outcome."),
    ("If you also sell platform or governance software, how is the audit team separated from it?",
     "The question does not arise. There is no platform, no software, and no product to cross-sell."),
    ("Will a named individual sign the audit summary as auditor of record?",
     "Yes. The summary is signed, and the person who signed it will answer questions about it."),
]

def six_list():
    items = "\n".join(
        f'<li><strong>{q}</strong></li>' for q, _ in SIX
    )
    return f'<ol class="q-list">{items}</ol>'

def six_ledger():
    rows = "\n".join(
        f'''<div class="ledger-row">
<p class="q">{i}. {q}</p>
<p class="a"><span class="tag">Greenpoint</span>{a}</p>
</div>''' for i, (q, a) in enumerate(SIX, 1)
    )
    return f'<div class="ledger">\n{rows}\n</div>'

# ============================================================ FAQ
FAQ = [
    ("Who has to comply with Local Law 144?",
     "Employers and employment agencies that use an automated employment decision tool to substantially assist or replace discretionary decision-making in hiring or promotion, where the candidate or employee is located in New York City. The test is where the candidate sits, not where the company is headquartered. A fully remote company with one applicant in the five boroughs is covered for that evaluation."),
    ("How often does the audit have to be done?",
     "The audit must have been conducted no more than one year before the tool is used. That makes it a recurring obligation rather than a one-time clearance, and it is the requirement employers most often miss after the first year."),
    ("What is the four-fifths rule?",
     "An impact ratio compares each demographic group's selection rate against the rate of the most-selected group. Under the EEOC's four-fifths guideline, a ratio below 0.80 is treated as evidence of adverse impact warranting further examination. Local Law 144 requires those ratios to be calculated and published. It does not itself make 0.80 a pass-fail line."),
    ("Is a failing impact ratio a violation?",
     "Not of Local Law 144. The statute requires you to calculate and publish, not to pass. The same figure is squarely relevant under Title VII, the New York City Human Rights Law and the New York State Human Rights Law, where the exposure is class litigation rather than a per-day penalty. Publishing a bad number is required. Not publishing it is the violation."),
    ("Who qualifies as an independent auditor?",
     "A person or firm not involved in using, developing or distributing the tool, and holding no employment or financial relationship with the employer that would compromise independence. DCWP maintains no approved auditor list, so the selection is the employer's responsibility and the employer's risk."),
    ("Can our AEDT vendor perform the audit?",
     "A vendor auditing its own tool, or paying the party that does, is the arrangement most likely to fail the independence requirement. It is also the most common one in the market. Ask the six questions on this page of anyone you are considering."),
    ("What has to be published, and for how long?",
     "A summary of the most recent bias audit, publicly available on your website, covering the source and explanation of the data used, the number of individuals assessed who fall into unknown categories, and the selection or scoring rates and impact ratios for every required category. The distribution date of the tool goes alongside it. The summary must stay posted for at least six months after the tool's most recent use."),
    ("What are the penalties?",
     "Between $500 and $1,500 per violation, and each day a violation continues is treated as a separate violation. Failing to conduct the audit, failing to publish the summary and failing to give notice are each independently actionable."),
    ("What if we have never collected demographic data?",
     "The rules address this. Where historical data is insufficient, test data may be substituted, and that substitution carries its own disclosure requirement. Reconstructing or substituting data is one of the main things that moves the cost of an engagement."),
    ("We are not sure any of our tools count as AEDTs. Where do we start?",
     "With an inventory rather than an audit. Every system touching hiring, screening, ranking, assessment or promotion gets the AEDT definition applied to it in writing. That is what the exposure review produces, and roughly a third of them conclude that nothing in the stack meets the definition."),
]

def faq_html():
    items = "\n".join(
        f'''<details>
<summary>{q}</summary>
<div class="answer"><p>{a}</p></div>
</details>''' for q, a in FAQ
    )
    return f'<div class="qa">\n{items}\n</div>'

def faq_schema():
    import json
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ
        ]
    })

# ================================================================= INDEX
index_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService",
"name":"Greenpoint AI Compliance LLC",
"description":"Independent bias audits for automated employment decision tools under New York City Local Law 144.",
"url":"%s/","email":"%s",
"address":{"@type":"PostalAddress","streetAddress":"418 Broadway, Ste R","addressLocality":"Albany","addressRegion":"NY","postalCode":"12207","addressCountry":"US"},
"areaServed":{"@type":"City","name":"New York City"},
"knowsAbout":["NYC Local Law 144","Automated Employment Decision Tools","Algorithmic bias auditing","Adverse impact analysis","Four-fifths rule"],
"serviceType":"Independent bias audit"}
</script>
<script type="application/ld+json">%s</script>
''' % (SITE, EMAIL, faq_schema())

index_body = f'''
<main>

<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">NYC Local Law 144 &middot; Automated Employment Decision Tools</span>
      <h1>Your hiring tool needs an audit.<em>Most employers fail the math, not the law.</em></h1>
      <p class="lede">Independent bias audits for employers running automated screening on New York City candidates. Fixed price, agreed before the work starts, and documentation that holds up when somebody asks to see it.</p>
      <div class="hero-actions">
        <a class="btn btn-solid" href="services.html">See engagements &amp; pricing</a>
        <a class="btn btn-ghost" href="nyc-local-law-144-bias-audit-guide.html">Read the compliance guide</a>
      </div>
    </div>

    <div class="exhibit" id="calculator">
      <div class="exhibit-head">
        <span>Exhibit A &middot; Impact ratio</span>
        <span>Editable</span>
      </div>
      <div class="exhibit-body">
        <p class="eyebrow" style="margin-bottom:0.7rem">Selection rate by group &middot; enter your own numbers</p>
        <div class="audit-scroll"><table class="audit">
          <caption class="sr-only">Four-fifths rule impact ratio calculator</caption>
          <thead>
            <tr>
              <th scope="col">Group</th><th scope="col">Selected</th><th scope="col">Applicants</th>
              <th scope="col">Rate</th><th scope="col">Ratio</th><th scope="col"><span class="sr-only">Result</span></th>
            </tr>
          </thead>
          <tbody id="rows">
            <tr><td>Group A</td>
              <td><input type="number" min="0" value="120" aria-label="Group A selected"></td>
              <td><input type="number" min="1" value="400" aria-label="Group A applicants"></td>
              <td class="rate">&mdash;</td><td class="ratio">&mdash;</td><td class="flagcell"></td></tr>
            <tr><td>Group B</td>
              <td><input type="number" min="0" value="45" aria-label="Group B selected"></td>
              <td><input type="number" min="1" value="250" aria-label="Group B applicants"></td>
              <td class="rate">&mdash;</td><td class="ratio">&mdash;</td><td class="flagcell"></td></tr>
            <tr><td>Group C</td>
              <td><input type="number" min="0" value="60" aria-label="Group C selected"></td>
              <td><input type="number" min="1" value="300" aria-label="Group C applicants"></td>
              <td class="rate">&mdash;</td><td class="ratio">&mdash;</td><td class="flagcell"></td></tr>
          </tbody>
        </table></div>
      </div>
      <div class="exhibit-foot" id="verdict-note">
        <strong>Impact ratio</strong> = each group&#39;s selection rate divided by the highest group&#39;s rate. Under the EEOC four-fifths guideline, below <strong>0.80</strong> is treated as evidence of adverse impact.
      </div>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <span class="eyebrow">What changed</span>
    <h2 class="section-title">The cheap period is over.</h2>
    <p class="section-intro">On 2 December 2025 the New York State Comptroller published an audit of how the Department of Consumer and Worker Protection enforces Local Law 144. Its reviewers looked at the same 32 companies DCWP had already looked at, and reached a very different conclusion.</p>

    <figure class="figure">
      {svg("enforcement-gap")}
      <figcaption>Office of the New York State Comptroller, report 2024-N-6, covering July 2023 through June 2025. DCWP identified one instance of non-compliance across the 32 companies it reviewed. The Comptroller identified at least 17 instances of potential non-compliance in the same set.</figcaption>
    </figure>

    <div class="stat-band">
      <div><span class="n flag">17</span><p class="l">Instances of potential non-compliance the Comptroller found among companies DCWP had cleared</p></div>
      <div><span class="n">2</span><p class="l">AEDT complaints DCWP received across the entire two-year audit period</p></div>
      <div><span class="n flag">75%</span><p class="l">Of test calls to 311 about AEDT issues were routed somewhere other than DCWP</p></div>
    </div>

    <div class="callout" style="margin-top:2.4rem">
      <p><strong>What DCWP agreed to do about it.</strong> The department concurred with the findings and committed to fixing complaint routing, cross-training staff, writing consistent complaint-handling policies, and interviewing employers about their tools rather than waiting for someone to file a complaint.</p>
      <p>Enforcement between 2023 and 2025 was complaint-driven and thin. Two complaints in two years is not a compliance record. It is a measurement failure, and it has now been measured.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <span class="eyebrow">What the law requires</span>
    <h2 class="section-title">Three obligations, in order. Missing any one is a violation.</h2>
    <ol class="steps">
      <li><span class="num">01</span><div>
        <h3>Audit before use</h3>
        <p>An independent bias audit conducted no more than one year before the tool is used, covering selection or scoring rates by sex, by race and ethnicity, and by their intersections.</p>
      </div></li>
      <li><span class="num">02</span><div>
        <h3>Publish the summary</h3>
        <p>A summary of the most recent audit posted publicly on your website, with the distribution date of the tool. It stays up for at least six months after the tool&#39;s last use. The opt-out instructions belong here too.</p>
      </div></li>
      <li><span class="num">03</span><div>
        <h3>Notify candidates</h3>
        <p>At least ten business days before use, naming the job qualifications and characteristics the tool assesses, with a route to request an alternative process that is actually available rather than theoretical.</p>
      </div></li>
    </ol>

    <figure class="figure framed" style="margin-top:3rem">
      {svg("audit-window")}
      <figcaption>The audit does not clear the tool permanently. It clears it for twelve months. Companies that commissioned an audit in the first compliance year and treated it as finished are the population the Comptroller&#39;s findings point at.</figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <span class="eyebrow">Who this reaches</span>
    <h2 class="section-title">Coverage follows the candidate, not the company.</h2>
    <p class="section-intro">Your headquarters is not the test. If you post a remote role and one applicant lives in Staten Island, that evaluation is in scope. For anyone hiring remotely at any scale, the working assumption should be that you are covered until you have established otherwise in writing.</p>
    <div class="cards">
      <article class="card">
        <h3>Employers</h3>
        <p>Any company using a screening, ranking, assessment or promotion tool on candidates or employees located in New York City. Most exposure sits in the applicant tracking system or an assessment vendor the company assumed was manual.</p>
      </article>
      <article class="card">
        <h3>Employment agencies</h3>
        <p>The statute names employment agencies directly. If you screen candidates on behalf of a client using a tool that scores or ranks them, the obligation attaches to you and not only to the employer you place them with.</p>
      </article>
      <article class="card">
        <h3>Staffing and RPO firms</h3>
        <p>High-volume placement is where automated screening earns its keep, and where a single tool touches thousands of New York City candidates a year. Volume raises both the compliance obligation and the underlying discrimination exposure.</p>
      </article>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <span class="eyebrow">Choosing an auditor</span>
    <h2 class="section-title">Six questions worth asking anyone who offers to audit your tool.</h2>
    <p class="section-intro">DCWP publishes no approved auditor list. Selecting one is the employer&#39;s responsibility, and a report signed by a party that fails the independence test is worse than no report, because it documents that you tried and got it wrong. These six questions separate an audit from a PDF shaped like one.</p>
    {six_list()}
    <a class="more" href="about.html#six">How Greenpoint answers all six &rarr;</a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <span class="eyebrow">Engagements</span>
    <h2 class="section-title">Scoped and priced before the work starts.</h2>
    <div class="cards">
      <article class="card">
        <h3>Exposure review</h3>
        <p>Inventory every tool touching hiring or promotion, apply the AEDT definition to each in writing, and produce a scoping memo you can hand to counsel. The right first step when you do not yet know whether you are covered.</p>
        <div class="price">$1,500<span>Credited in full against a subsequent audit</span></div>
      </article>
      <article class="card">
        <h3>Independent bias audit</h3>
        <p>Impact ratio analysis by sex, by race and ethnicity, and by every required intersection. Published summary drafted, candidate notice reviewed, workpapers retained behind every figure.</p>
        <div class="price">From $9,000<span>Scales with the number of tools in scope</span></div>
      </article>
      <article class="card">
        <h3>AI governance baseline</h3>
        <p>For organizations whose AI exposure runs past hiring. Enterprise inventory, risk classification against the NIST AI Risk Management Framework, control design and evidence practices.</p>
        <div class="price">From $15,000<span>Scoped on assessment</span></div>
      </article>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <span class="eyebrow">Common questions</span>
    <h2 class="section-title">What employers ask before they commission anything.</h2>
    {faq_html()}
  </div>
</section>

{cta_band("Find out whether you are covered before somebody else does.",
          "A twenty-minute scoping call is free and usually settles the question. If you are not in scope, we will tell you that and we are done.")}
'''

index_js = '''<script>
(function () {
  var rows = document.querySelectorAll('#rows tr');
  var note = document.getElementById('verdict-note');
  function compute() {
    var data = [];
    rows.forEach(function (tr) {
      var i = tr.querySelectorAll('input');
      var sel = parseFloat(i[0].value), app = parseFloat(i[1].value);
      data.push({ tr: tr, rate: (isFinite(sel) && isFinite(app) && app > 0) ? sel / app : null });
    });
    var best = 0;
    data.forEach(function (d) { if (d.rate !== null && d.rate > best) best = d.rate; });
    var anyFail = false;
    data.forEach(function (d) {
      var rc = d.tr.querySelector('.rate'), ic = d.tr.querySelector('.ratio'), fc = d.tr.querySelector('.flagcell');
      if (d.rate === null || best === 0) { rc.textContent = '\\u2014'; ic.textContent = '\\u2014'; fc.innerHTML = ''; return; }
      var ratio = d.rate / best;
      rc.textContent = (d.rate * 100).toFixed(1) + '%';
      ic.textContent = ratio.toFixed(2);
      var fails = ratio < 0.8;
      if (fails) anyFail = true;
      fc.innerHTML = '<span class="verdict ' + (fails ? 'fail' : 'pass') + '">' + (fails ? 'Below 0.80' : 'Clears') + '</span>';
      ic.style.color = fails ? 'var(--flag)' : 'var(--ink)';
    });
    note.innerHTML = anyFail
      ? '<strong style="color:var(--flag)">At least one group falls below 0.80.</strong> Under the EEOC four-fifths guideline that is evidence of adverse impact warranting scrutiny. Local Law 144 requires you to calculate and publish these ratios. It does not let you withhold them because they look bad.'
      : '<strong>Impact ratio</strong> = each group\\'s selection rate divided by the highest group\\'s rate. Under the EEOC four-fifths guideline, below <strong>0.80</strong> is treated as evidence of adverse impact.';
  }
  document.querySelectorAll('#rows input').forEach(function (i) { i.addEventListener('input', compute); });
  compute();
})();
</script>'''

write("index.html", [
    head("NYC Local Law 144 Bias Audits | Greenpoint Compliance",
         "Independent bias audits for automated employment decision tools under NYC Local Law 144. Fixed-price engagements, audit-ready workpapers, and a free four-fifths rule calculator.",
         "", extra=index_schema),
    chrome("index.html"), index_body, FOOTER.replace("</body>", index_js + "\n</body>"),
])

# ================================================================= SERVICES
services_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList","name":"Local Law 144 engagements","itemListElement":[
{"@type":"Service","position":1,"name":"LL144 exposure review","description":"Inventory of tools touching hiring or promotion, written AEDT determination for each, and a scoping memo.","provider":{"@type":"Organization","name":"Greenpoint AI Compliance LLC"},"offers":{"@type":"Offer","price":"1500","priceCurrency":"USD"}},
{"@type":"Service","position":2,"name":"Independent bias audit","description":"Impact ratio analysis by sex, race and ethnicity and their intersections; published summary drafted; workpapers retained.","provider":{"@type":"Organization","name":"Greenpoint AI Compliance LLC"},"offers":{"@type":"Offer","priceCurrency":"USD","priceSpecification":{"@type":"PriceSpecification","minPrice":"9000","maxPrice":"14000","priceCurrency":"USD"}}},
{"@type":"Service","position":3,"name":"AI governance baseline","description":"AI inventory, risk classification, control design and evidence practices under the NIST AI Risk Management Framework.","provider":{"@type":"Organization","name":"Greenpoint AI Compliance LLC"},"offers":{"@type":"Offer","price":"15000","priceCurrency":"USD"}}]}
</script>
'''

services_body = f'''
<main>
<section class="page-head"><div class="wrap">
<span class="eyebrow">Engagements</span>
<h1>Scoped work, not billable hours</h1>
<p class="lede">Every engagement has a stated scope, a stated deliverable, and a price agreed in writing before anything starts. The starting figures below are real. What moves them is the number of tools in scope and the state of your data.</p>
</div></section>

<section class="section" style="border-top:none;padding-top:2.4rem"><div class="wrap"><div class="prose">

<h2 style="margin-top:0">Exposure review &mdash; $1,500</h2>
<p><strong>$1,500, credited in full against a subsequent bias audit.</strong> The right starting point when you do not yet know whether Local Law 144 applies to you.</p>
<ul>
<li>Inventory of every system touching hiring, screening, ranking, assessment or promotion</li>
<li>Written AEDT determination for each one, applying the DCWP final rules rather than a vendor&#39;s marketing claim</li>
<li>Identification of where in your stack the exposure actually sits, which is usually the applicant tracking system or an assessment provider</li>
<li>A scoping memo you can hand directly to employment counsel</li>
</ul>
<p>If nothing you use meets the definition, you get that in writing and the engagement ends there. That is a legitimate outcome and roughly a third of reviews reach it.</p>

<h2>Independent bias audit &mdash; from $9,000</h2>
<p>One tool on clean historical data sits at the starting figure. Multiple tools, multiple configurations, or reconstructing demographic data you never collected move it up.</p>
<ul>
<li>Selection rate and scoring rate analysis by sex, by race and ethnicity, and by intersectional category</li>
<li>Impact ratio calculation against the highest-selected group, with four-fifths guideline assessment</li>
<li>Treatment of unknown-category individuals, and disclosure language where historical data is insufficient</li>
<li>Drafted public summary meeting the content requirements at 6 RCNY &sect; 5-301</li>
<li>Review of your candidate notice and opt-out process for whether it is practically available</li>
<li>Retained workpapers supporting every figure published, signed by a named auditor of record</li>
</ul>
<p>Because the audit must be less than twelve months old every time the tool is used, this recurs. Clients who keep the tool in service commission it again against the same methodology, which makes the second engagement considerably lighter than the first.</p>
<p>Independence is the point of the engagement. Greenpoint has no relationship with any AEDT vendor, no implementation practice, and no financial interest in what the numbers say.</p>

<h2>AI governance baseline &mdash; from $15,000</h2>
<p>For organizations whose AI exposure runs past hiring.</p>
<ul>
<li>Enterprise AI system inventory and use-case classification</li>
<li>Risk tiering mapped to the NIST AI Risk Management Framework</li>
<li>Control design, ownership assignment, and evidence retention practices</li>
<li>Board- or committee-ready summary of the program and its residual risks</li>
</ul>

<figure class="figure framed">
{svg("scope-drivers")}
<figcaption>A quote follows the scoping call, in writing, before you commit to anything. If the work turns out larger than scoped, that is a conversation rather than an invoice.</figcaption>
</figure>

<div class="callout">
<p><strong>Ongoing advisory.</strong> Some clients keep a standing monthly arrangement for regulatory monitoring, new-tool reviews and audit renewal. That runs $2,000 to $4,000 a month depending on scope, and it is only worth it once you have more than one tool in play.</p>
</div>

<h2>How engagements start</h2>
<ol>
<li><strong>Scoping call, twenty minutes, free.</strong> Usually enough to determine whether you are covered.</li>
<li><strong>Written proposal</strong> with fixed scope and fixed price. No retainer required to receive it.</li>
<li><strong>Kickoff</strong> with a data request list. Data quality drives the work more than anything else.</li>
<li><strong>Delivery</strong> of workpapers, published summary language, and a walkthrough with whoever owns the decision.</li>
</ol>

</div></div></section>

{cta_band("Start with the scoping call.",
          "Twenty minutes, no cost, and a straight answer about whether you have an obligation.")}
'''

write("services.html", [
    head("Bias Audit Engagements &amp; Pricing | Greenpoint Compliance",
         "Local Law 144 engagements with stated scope, deliverables and price: exposure review $1,500 credited against a full audit, independent bias audits from $9,000, AI governance baseline from $15,000.",
         "services.html", extra=services_schema),
    chrome("services.html"), services_body, FOOTER,
])

# ================================================================= ABOUT
about_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Taylor Campbell","honorificSuffix":"JD",
"jobTitle":"Founder","worksFor":{"@type":"Organization","name":"Greenpoint AI Compliance LLC"},
"knowsAbout":["NYC Local Law 144","Automated Employment Decision Tools","Adverse impact analysis","Regulatory compliance testing"]}
</script>
'''

about_body = f'''
<main>
<section class="page-head"><div class="wrap">
<span class="eyebrow">About</span>
<h1>A compliance practice, not a technology vendor</h1>
<p class="lede">Greenpoint exists because the market for this work splits between Big Four engagements priced for the Fortune 500 and software that produces a dashboard nobody can defend to a regulator.</p>
</div></section>

<section class="section" style="border-top:none;padding-top:2.4rem"><div class="wrap"><div class="prose">

<h2 style="margin-top:0">Why an independent auditor rather than a platform</h2>
<p>Local Law 144 requires that the auditor hold no financial relationship with the employer or with the tool that would compromise independence. A company that sells you monitoring software and also audits your tool has a structural problem with that requirement, however good the software happens to be.</p>
<p>Greenpoint does not sell AI tooling, does not implement hiring systems, and maintains no vendor partnerships. The only product is the audit and the workpapers behind it.</p>

<figure class="figure framed">
{svg("independence")}
<figcaption>Independence is not a claim in a marketing page. It is a set of things a firm has agreed not to do, which is why it is worth asking any prospective auditor to put its answers in writing.</figcaption>
</figure>

</div></div></section>

<section class="section tint"><div class="wrap" id="six">
<span class="eyebrow">The six questions</span>
<h2 class="section-title">Ask us the same six questions you should ask anyone else.</h2>
<p class="section-intro">A report signed by a party that fails the independence test is worse than no report, because it documents that you tried and got it wrong. Here is how this practice answers.</p>
{six_ledger()}
</div></section>

<section class="section"><div class="wrap"><div class="prose">

<h2 style="margin-top:0">Background</h2>
<div class="founder">
<figure style="margin:0">
<img src="taylor-campbell.jpg" alt="Taylor Campbell, founder of Greenpoint AI Compliance" width="880" height="1050" loading="lazy">
<figcaption class="cap"><strong>Taylor Campbell, JD</strong>Founder and auditor of record</figcaption>
</figure>
<div class="bio">
<p>Greenpoint was founded by Taylor Campbell, a compliance professional with a JD and a regulatory background spanning government, financial services and technology. That work includes the Government of the District of Columbia, PGIM, Russell Investments and Mutual of Omaha.</p>
<p>The background matters here for a specific reason. Algorithmic accountability regimes are converging on something financial services has done for decades. Keep an inventory of covered activity, test it on a schedule, document the test, retain the workpapers, and be able to show a regulator the evidence.</p>
</div>
</div>
<p>The mathematics is not new either. The four-fifths guideline has been in the EEOC&#39;s Uniform Guidelines since 1978 and predates machine learning by half a century. What is new is that the obligation now attaches to employers who have never run a testing program of any kind.</p>
<p>Most of the difficulty is not the statistics. It is building a repeatable process that produces defensible evidence, which is the problem regulated industries solved a long time ago.</p>

<h2>How we work</h2>
<ul>
<li><strong>Fixed scope and fixed price.</strong> You should know the cost before the work starts.</li>
<li><strong>Written determinations.</strong> A conclusion you cannot show to counsel is not useful to you.</li>
<li><strong>Findings delivered straight.</strong> If a tool produces a failing impact ratio, that appears in the report. The obligation is to calculate and publish, not to arrive at a comfortable number.</li>
<li><strong>No scope creep by invoice.</strong> If the work is larger than scoped, that is a conversation first.</li>
</ul>

<h2>Coverage</h2>
<p>Based in Brooklyn, working with employers nationally. Local Law 144 coverage follows the candidate rather than the employer, so most clients are not New York companies. They are companies that hire New Yorkers.</p>

</div></div></section>

{cta_band("Twenty minutes to find out where you stand.",
          "No cost, no proposal attached, and a straight answer about whether you have an obligation.")}
'''

write("about.html", [
    head("About | Greenpoint Compliance",
         "Independent Local Law 144 bias audit practice in Brooklyn, New York. No AEDT products, no implementation work, no vendor partnerships, and a named auditor of record on every report.",
         "about.html", og_type="profile", extra=about_schema, og_image="taylor-campbell-square.jpg"),
    chrome("about.html"), about_body, FOOTER,
])

# ================================================================= GUIDE
guide_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article",
"headline":"NYC Local Law 144 Bias Audit: Complete Compliance Guide (2026)",
"description":"A practical guide to Local Law 144 of 2021: scope, bias audit methodology, impact ratios, candidate notice, independent auditor criteria, penalties, and the 2026 enforcement shift.",
"author":{"@type":"Organization","name":"Greenpoint AI Compliance LLC"},
"publisher":{"@type":"Organization","name":"Greenpoint AI Compliance LLC"},
"datePublished":"2026-08-04","dateModified":"2026-08-26",
"mainEntityOfPage":"%s/nyc-local-law-144-bias-audit-guide.html"}
</script>
''' % SITE

guide_body = f'''
<main>
<section class="page-head"><div class="wrap">
<span class="eyebrow">Compliance guide</span>
<h1>NYC Local Law 144: the bias audit, explained properly</h1>
<p class="lede">Everything an employer needs to determine coverage, commission a defensible audit, and publish what the law actually asks for.</p>
<p class="meta">Updated August 2026 &middot; N.Y.C. Admin. Code &sect;&sect; 20-870 to 20-874 &middot; 6 RCNY &sect;&sect; 5-300 to 5-304</p>
</div></section>

<section class="section" style="border-top:none; padding-top:2.4rem"><div class="wrap"><div class="prose">

<div class="toc">
<p>Contents</p>
<ol>
<li><a href="#scope">Who is actually covered</a></li>
<li><a href="#aedt">What counts as an AEDT</a></li>
<li><a href="#math">How the audit math works</a></li>
<li><a href="#auditor">Who qualifies as independent</a></li>
<li><a href="#publish">What you must publish</a></li>
<li><a href="#notice">Candidate notice and the opt-out</a></li>
<li><a href="#penalties">Penalties and the 2026 enforcement shift</a></li>
<li><a href="#mistakes">The five mistakes we see most</a></li>
</ol>
</div>

<h2 id="scope">1. Who is actually covered</h2>
<p>Local Law 144 applies to employers and employment agencies that use an automated employment decision tool to substantially assist or replace discretionary decision-making for hiring or promotion, where the candidate or employee is located in New York City.</p>
<p>The critical word is <em>located</em>. Coverage follows the candidate, not the company. Your headquarters is irrelevant. If you post a remote role and one applicant lives in Staten Island, that evaluation is in scope. For any company hiring remotely at scale, the practical assumption should be that you are covered unless you have affirmatively established otherwise.</p>

<figure class="figure framed">
{svg("coverage")}
<figcaption>The most expensive misreading of this statute is treating it as a New York employer&#39;s problem. It is a New York candidate&#39;s protection, and it travels with them.</figcaption>
</figure>

<p>The law imposes obligations on employers, not on vendors. Your applicant tracking system provider has no direct duty here, which means their cooperation depends entirely on what your contract says. This surprises people, and it explains why vendor questionnaires so often go unanswered.</p>

<h2 id="aedt">2. What counts as an AEDT</h2>
<p>DCWP&#39;s final rules define an AEDT as a computational process derived from machine learning, statistical modeling, data analytics or artificial intelligence that issues a simplified output, meaning a score, classification or recommendation, used to substantially assist or replace discretionary decision-making.</p>
<p>Two qualifiers do most of the work:</p>
<ul>
<li><strong>Simplified output.</strong> A tool that surfaces raw information without scoring or ranking generally falls outside the definition.</li>
<li><strong>Substantially assist.</strong> The rules narrowed this considerably from the original 2022 proposal. A tool whose output is one input among many, weighted no more heavily than the others by a human decision-maker, may fall outside scope. This is a fact-specific judgment you should document rather than assume.</li>
</ul>
<p>In practice, exposure hides in places nobody inventories: resume parsers that rank, assessment platforms that produce percentile scores, interview scheduling tools with knockout logic, and recruitment marketing systems that decide who sees a posting at all.</p>

<h2 id="math">3. How the audit math works</h2>
<p>This is where most compliance conversations go quiet, and it is the substance of the exercise.</p>
<p>The audit calculates <strong>selection rates</strong> for each demographic category, then converts them into <strong>impact ratios</strong> by dividing each group&#39;s rate by the rate of the most-selected group. The required categories are sex, race and ethnicity, and their intersections. Not just &ldquo;women&rdquo; and &ldquo;Asian&rdquo; but &ldquo;Asian women.&rdquo;</p>

<table>
<thead><tr><th>Group</th><th>Selected</th><th>Applicants</th><th>Selection rate</th><th>Impact ratio</th></tr></thead>
<tbody>
<tr><td>Group A</td><td>120</td><td>400</td><td>30.0%</td><td>1.00</td></tr>
<tr><td>Group B</td><td>45</td><td>250</td><td>18.0%</td><td>0.60</td></tr>
<tr><td>Group C</td><td>60</td><td>300</td><td>20.0%</td><td>0.67</td></tr>
</tbody>
</table>

<figure class="figure framed">
{svg("impact-bars")}
<figcaption>Group A has the highest selection rate, so it becomes the denominator and its own ratio is 1.00 by definition. Group B returns 0.60 and Group C returns 0.67, both below the EEOC&#39;s four-fifths guideline of 0.80.</figcaption>
</figure>

<div class="callout">
<p><strong>A point that is widely misunderstood.</strong> Local Law 144 does not make 0.80 a pass-fail line. It requires you to calculate and publish the ratios. A failing ratio is not itself a violation of Local Law 144, but it is highly relevant under Title VII, the New York City Human Rights Law and the New York State Human Rights Law, which is a considerably larger problem than a DCWP penalty.</p>
<p>Publishing a bad number is required. Not publishing it is the violation.</p>
</div>

<p>For scoring tools rather than pass-fail tools, the analysis uses scoring rates, meaning the proportion of each group scoring above the median, rather than selection rates. The rules also address what to do when historical data is unavailable and when test data may be substituted, which carries its own disclosure requirement.</p>
<p>You can run the calculation on your own numbers using the <a href="four-fifths-rule-calculator.html">four-fifths rule calculator</a>.</p>

<h2 id="auditor">4. Who qualifies as independent</h2>
<p>The auditor must not have been involved in using, developing or distributing the tool, and must hold no employment or financial relationship with the employer that would compromise independence.</p>
<p>DCWP maintains no approved auditor list. Selecting a qualified independent auditor is the employer&#39;s responsibility and the employer&#39;s risk. Two arrangements regularly fail this test:</p>
<ul>
<li>An audit performed by the vendor that supplies the tool, or by a party the vendor pays.</li>
<li>An audit performed by a firm that also implemented the tool for you, or that holds an ongoing advisory role creating a financial interest in the outcome.</li>
</ul>
<p>There are <a href="about.html#six">six questions worth putting to any prospective auditor</a> before you engage one. Ask for the answers in writing.</p>

<h2 id="publish">5. What you must publish</h2>
<p>A summary of the most recent bias audit must be publicly available on your website. It needs to include the source and explanation of the data used, the number of individuals assessed who fall into unknown categories, and the selection or scoring rates and impact ratios for all required categories. The distribution date of the tool goes alongside it.</p>
<p>The summary must remain posted for at least six months after the tool&#39;s most recent use. A common failure is posting the summary and then quietly removing it when the numbers become inconvenient, or when a site redesign drops the page.</p>

<h2 id="notice">6. Candidate notice and the opt-out</h2>
<p>Candidates and employees must be notified at least ten business days before the tool is used. The notice must state that an AEDT will be used, identify the job qualifications and characteristics it assesses, and describe the data collected, its source, and the employer&#39;s retention policy.</p>
<p>Notice can be given through the employment section of your website, in the job posting itself, or by mail or email. For current employees, a written policy or procedure works.</p>
<p>The opt-out deserves specific attention. Candidates may request an alternative selection process. The law does not prescribe what the alternative must be, but it has to be actually available. A manual resume review or panel interview that happens, not a theoretical option no candidate has ever successfully used. If your process cannot accommodate an opt-out in practice, you have a problem regardless of what your policy says.</p>

<h2 id="penalties">7. Penalties and the 2026 enforcement shift</h2>
<p>DCWP enforces the law under N.Y.C. Admin. Code &sect;&sect; 20-870 to 20-874. Penalties run from $500 for a first violation up to $1,500, and each day a violation continues is treated as a separate violation. Failing to conduct the audit, failing to publish the summary and failing to provide notice are each independently actionable.</p>
<p>Enforcement from 2023 through 2025 was largely complaint-driven and thin. That changed on 2 December 2025, when the New York State Comptroller published report 2024-N-6, an audit of DCWP&#39;s enforcement of this statute covering July 2023 through June 2025.</p>

<div class="callout flagged">
<p><strong>The finding that matters.</strong> DCWP reviewed the websites and bias audits of 32 companies and identified one instance of non-compliance. The Comptroller reviewed the same 32 and identified at least 17 instances of potential non-compliance.</p>
<p>The audit also found that DCWP had received two AEDT complaints across the entire two-year period, and that 75 percent of test calls placed to 311 about AEDT issues were routed somewhere other than DCWP.</p>
</div>

<p>DCWP concurred with the findings and committed to fixing complaint routing, cross-training staff, adopting written complaint-handling policies, and pursuing enforcement that does not depend on somebody filing a complaint first. Employment practices have since advised clients to expect more frequent investigations and higher cumulative penalties.</p>
<p>The long period during which non-compliance carried a low expected cost has ended. Anything commissioned under the old posture is worth re-examining under the new one.</p>

<h2 id="mistakes">8. The five mistakes we see most</h2>
<ol>
<li><strong>Assuming you are not covered because you are not in New York.</strong> Coverage follows the candidate. Remote hiring almost guarantees exposure.</li>
<li><strong>Not knowing what is in the stack.</strong> Companies routinely discover AEDTs embedded in tools they believed were manual. Start with an inventory, not an audit.</li>
<li><strong>Treating it as one and done.</strong> The audit must be less than a year old every time the tool is used. It is an annual program.</li>
<li><strong>Using an auditor who is not independent.</strong> Vendor-supplied audits are the most common version and the least defensible.</li>
<li><strong>Publishing the summary and letting it lapse.</strong> Six months minimum after last use, and it has to stay findable.</li>
</ol>

<h2>Where to start</h2>
<p>If you do not know whether you are covered, the sequence is: inventory every tool touching hiring or promotion, apply the AEDT definition to each in writing, then audit what is in scope. Most organizations can complete the first two steps internally. The third requires independence by definition.</p>
<p>Our <a href="services.html">exposure review</a> handles the first two steps and produces a written AEDT determination for every system in your stack, plus a scoping memo you can hand to counsel.</p>

<p style="margin-top:2.5rem; font-size:0.86rem; color:var(--slate-lt)">This guide is general information about a regulatory requirement, not legal advice. Application to your specific hiring process should be reviewed with employment counsel.</p>

</div></div></section>

{cta_band("Not sure whether your tools are in scope?",
          "Twenty minutes on a call usually settles it. If you are not covered, we will say so and we are done.")}
'''

write("nyc-local-law-144-bias-audit-guide.html", [
    head("NYC Local Law 144 Bias Audit: Complete Compliance Guide (2026)",
         "What NYC Local Law 144 requires in 2026: who is covered, how the bias audit math works, impact ratios and the four-fifths rule, candidate notice, independent auditor criteria, penalties, and the post-Comptroller enforcement shift.",
         "nyc-local-law-144-bias-audit-guide.html", og_type="article", extra=guide_schema),
    chrome("nyc-local-law-144-bias-audit-guide.html"), guide_body, FOOTER,
])

# ================================================================= CALCULATOR
calc_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"Four-Fifths Rule Impact Ratio Calculator",
"applicationCategory":"BusinessApplication","operatingSystem":"Any","url":"%s/four-fifths-rule-calculator.html",
"description":"Free calculator for adverse impact analysis. Enter selection counts by demographic group to compute selection rates and impact ratios against the EEOC four-fifths guideline.",
"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
"publisher":{"@type":"Organization","name":"Greenpoint AI Compliance LLC"}}
</script>
''' % SITE

calc_body = f'''
<main>
<section class="page-head"><div class="wrap">
<span class="eyebrow">Free tool</span>
<h1>Four-fifths rule calculator</h1>
<p class="lede">Enter selection counts by group. The calculator returns selection rates, impact ratios against the highest-selected group, and a four-fifths guideline assessment.</p>
<p class="meta">No signup &middot; nothing is transmitted &middot; all calculation happens in your browser</p>
</div></section>

<section class="section" style="border-top:none;padding-top:2rem"><div class="wrap">
<div class="exhibit" style="max-width:780px">
<div class="exhibit-head"><span>Adverse impact analysis</span><span>Editable</span></div>
<div class="exhibit-body">
<p class="eyebrow" style="margin-bottom:0.7rem">Add or remove rows to match your categories</p>
<div class="audit-scroll"><table class="audit">
<thead><tr>
<th scope="col">Group</th><th scope="col">Selected</th><th scope="col">Applicants</th>
<th scope="col">Rate</th><th scope="col">Ratio</th><th scope="col"><span class="sr-only">Result</span></th>
</tr></thead>
<tbody id="rows"></tbody>
</table></div>
<div style="display:flex;gap:0.6rem;margin-top:1rem;flex-wrap:wrap">
<button type="button" class="btn btn-ghost" id="addrow" style="font-size:0.78rem;padding:0.5rem 0.9rem">Add group</button>
<button type="button" class="btn btn-ghost" id="reset" style="font-size:0.78rem;padding:0.5rem 0.9rem">Reset to example</button>
</div>
</div>
<div class="exhibit-foot" id="verdict-note"></div>
</div>
</div></section>

<section class="section"><div class="wrap"><div class="prose">
<h2 style="margin-top:0">How the calculation works</h2>
<p>The impact ratio is the simplest defensible measure of whether a selection process treats groups differently. Three steps:</p>
<ol>
<li><strong>Selection rate</strong> for each group is the number selected divided by the number of applicants.</li>
<li><strong>Reference group</strong> is whichever group has the highest selection rate. It becomes the denominator and its own ratio is 1.00 by definition.</li>
<li><strong>Impact ratio</strong> is each group&#39;s selection rate divided by the reference rate.</li>
</ol>

<figure class="figure framed">
{svg("impact-bars")}
<figcaption>A worked example. Under the EEOC&#39;s Uniform Guidelines on Employee Selection Procedures, a ratio below four-fifths is generally regarded as evidence of adverse impact. The guideline dates to 1978 and long predates machine learning.</figcaption>
</figure>

<p>What is new is that automated tools now produce these disparities at scale and, increasingly, that the law requires you to measure and publish them.</p>

<div class="callout">
<p><strong>A ratio below 0.80 is not automatically illegal.</strong> It is a screening threshold that shifts the analysis toward whether the selection procedure is job-related and consistent with business necessity. Nor does NYC Local Law 144 treat 0.80 as pass-fail. It requires you to calculate and publish the ratios regardless of what they say.</p>
</div>

<h2>What the calculator does not do</h2>
<p>This tool computes impact ratios for the categories you enter. A compliant Local Law 144 bias audit requires more:</p>
<ul>
<li><strong>Intersectional categories.</strong> Not just sex and race separately, but their combinations. Hispanic women, Black men, and so on. This is where disparities frequently appear that single-axis analysis misses entirely.</li>
<li><strong>Scoring rate analysis</strong> for tools that produce scores rather than pass-fail outcomes, measured as the proportion of each group scoring above the median.</li>
<li><strong>Treatment of unknown-category individuals</strong>, which must be counted and disclosed.</li>
<li><strong>Independence.</strong> An audit you run yourself does not satisfy the statute. The auditor must not hold an employment or financial relationship with you that compromises independence.</li>
</ul>
<p>Use this to understand your exposure before commissioning an audit, not as a substitute for one. The <a href="nyc-local-law-144-bias-audit-guide.html">full compliance guide</a> covers what a defensible audit actually requires.</p>

<h2>Statistical significance and small samples</h2>
<p>Impact ratios computed on small applicant pools are unstable. With twenty applicants in a group, a single hiring decision can move the ratio by 0.15 or more. The Uniform Guidelines acknowledge this, and practitioners typically supplement the ratio with a significance test, either a two-proportion z-test or Fisher&#39;s exact test, when group sizes are small.</p>
<p>A practical rule: treat ratios computed on fewer than about thirty applicants per group as directional rather than conclusive, and say so in whatever you publish.</p>

<p style="margin-top:2.5rem;font-size:0.86rem;color:var(--slate-lt)">This calculator is provided for general educational use. It is not legal advice and does not constitute a bias audit under NYC Local Law 144 or any other law.</p>
</div></div></section>

{cta_band("Twenty minutes to find out where you stand.",
          "No cost, no proposal attached, and a straight answer about whether you have an obligation.")}
'''

calc_js = r'''<script>
(function(){
  var tbody=document.getElementById('rows'), note=document.getElementById('verdict-note');
  var DEFAULTS=[['White men',120,400],['Black women',45,250],['Hispanic men',60,300],['Asian women',38,180]];
  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;'); }
  function rowHTML(name,sel,app){
    return '<tr>'+
      '<td><input type="text" class="gname" value="'+esc(name)+'" aria-label="Group name" style="width:7.5rem;text-align:left"></td>'+
      '<td><input type="number" min="0" class="gsel" value="'+sel+'" aria-label="Selected"></td>'+
      '<td><input type="number" min="1" class="gapp" value="'+app+'" aria-label="Applicants"></td>'+
      '<td class="rate">—</td><td class="ratio">—</td><td class="flagcell"></td></tr>';
  }
  function build(data){ tbody.innerHTML=data.map(function(d){return rowHTML(d[0],d[1],d[2]);}).join(''); bind(); compute(); }
  function bind(){ tbody.querySelectorAll('input').forEach(function(i){ i.oninput=compute; }); }
  function compute(){
    var trs=[].slice.call(tbody.querySelectorAll('tr')), data=[];
    trs.forEach(function(tr){
      var s=parseFloat(tr.querySelector('.gsel').value), a=parseFloat(tr.querySelector('.gapp').value);
      data.push({tr:tr,rate:(isFinite(s)&&isFinite(a)&&a>0)?s/a:null,
                 name:tr.querySelector('.gname').value||'Group', n:a});
    });
    var best=0; data.forEach(function(d){ if(d.rate!==null&&d.rate>best) best=d.rate; });
    var fails=[], small=false;
    data.forEach(function(d){
      var rc=d.tr.querySelector('.rate'), ic=d.tr.querySelector('.ratio'), fc=d.tr.querySelector('.flagcell');
      if(d.rate===null||best===0){ rc.textContent='—'; ic.textContent='—'; fc.innerHTML=''; return; }
      if(d.n<30) small=true;
      var r=d.rate/best;
      rc.textContent=(d.rate*100).toFixed(1)+'%';
      ic.textContent=r.toFixed(2);
      var bad=r<0.8; if(bad) fails.push(d.name);
      ic.style.color=bad?'var(--flag)':'var(--ink)';
      fc.innerHTML='<span class="verdict '+(bad?'fail':'pass')+'">'+(bad?'Below 0.80':'Clears')+'</span>';
    });
    var msg;
    if(fails.length){
      msg='<strong style="color:var(--flag)">'+fails.length+' group'+(fails.length>1?'s fall':' falls')+
          ' below 0.80:</strong> '+fails.map(esc).join(', ')+'. Under the EEOC four-fifths guideline this is evidence of adverse impact warranting examination of whether the procedure is job-related and consistent with business necessity.';
    } else {
      msg='<strong>All groups clear 0.80.</strong> Impact ratio = each group\'s selection rate divided by the highest group\'s rate.';
    }
    if(small) msg+=' <em>At least one group has fewer than 30 applicants. Treat those ratios as directional, not conclusive.</em>';
    note.innerHTML=msg;
  }
  document.getElementById('addrow').onclick=function(){
    tbody.insertAdjacentHTML('beforeend',rowHTML('New group',0,100)); bind(); compute();
  };
  document.getElementById('reset').onclick=function(){ build(DEFAULTS); };
  build(DEFAULTS);
})();
</script>'''

write("four-fifths-rule-calculator.html", [
    head("Four-Fifths Rule Calculator | Adverse Impact &amp; Selection Rate Analysis",
         "Free four-fifths rule calculator. Enter selection counts by demographic group to compute selection rates and impact ratios against the EEOC 0.80 adverse impact threshold. Runs entirely in your browser.",
         "four-fifths-rule-calculator.html", og_type="article", extra=calc_schema),
    chrome("four-fifths-rule-calculator.html"), calc_body,
    FOOTER.replace("</body>", calc_js + "\n</body>"),
])

# ================================================================= LEGAL
legal_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Greenpoint AI Compliance LLC","url":"%s/","email":"%s","address":{"@type":"PostalAddress","streetAddress":"418 Broadway, Ste R","addressLocality":"Albany","addressRegion":"NY","postalCode":"12207","addressCountry":"US"}}
</script>
''' % (SITE, EMAIL)

legal_body = f'''
<main>
<section class="page-head"><div class="wrap">
<span class="eyebrow">Legal</span>
<h1>Legal notices, disclaimers and privacy</h1>
<p class="lede">Entity information, terms of use, our independence position, and how this site handles data, which is to say almost not at all.</p>
<p class="meta">Effective 26 August 2026 &middot; Last updated 26 August 2026</p>
</div></section>

<section class="section" style="border-top:none;padding-top:2.4rem"><div class="wrap"><div class="prose">

<div class="toc">
<p>Contents</p>
<ol>
<li><a href="#entity">Entity information</a></li>
<li><a href="#nolegal">No legal advice; no attorney&ndash;client relationship</a></li>
<li><a href="#independence">Independence and conflicts of interest</a></li>
<li><a href="#terms">Terms of use</a></li>
<li><a href="#calculator">The calculator: limitations</a></li>
<li><a href="#privacy">Privacy policy</a></li>
<li><a href="#cookies">Cookies and tracking</a></li>
<li><a href="#rights">Your data rights</a></li>
<li><a href="#ip">Intellectual property</a></li>
<li><a href="#accessibility">Accessibility</a></li>
<li><a href="#contact">Contact</a></li>
</ol>
</div>

<h2 id="entity">1. Entity information</h2>
<p>This website is operated by <strong>Greenpoint AI Compliance LLC</strong>, a limited liability company organized under the laws of the State of New York.</p>
<table>
<tbody>
<tr><th>Legal entity</th><td>Greenpoint AI Compliance LLC</td></tr>
<tr><th>Jurisdiction</th><td>New York, United States</td></tr>
<tr><th>Registered address</th><td>418 Broadway, Ste R, Albany, NY 12207, USA</td></tr>
<tr><th>Contact</th><td>{EMAIL}</td></tr>
<tr><th>Nature of business</th><td>Regulatory compliance consulting and independent assessment services</td></tr>
</tbody>
</table>
<p>Greenpoint AI Compliance LLC is not a law firm, is not an accounting firm, and does not provide legal, accounting, tax or investment advice.</p>

<h2 id="nolegal">2. No legal advice; no attorney&ndash;client relationship</h2>
<p>All content on this site, including the compliance guide, the calculator and any downloadable material, is general information about regulatory requirements. It is not legal advice and must not be relied upon as such.</p>
<p>Using this site, contacting us, or receiving a proposal does not create an attorney&ndash;client relationship, and no such relationship exists at any point. We are consultants, not counsel. Statutes, regulations and enforcement practice change frequently in this area, and application to your specific circumstances requires review by a qualified attorney licensed in the relevant jurisdiction.</p>
<p>Where our work touches questions of legal interpretation, such as whether a particular tool meets a statutory definition or whether an obligation attaches to a particular hiring process, we will say so and recommend you obtain a legal opinion. We do not substitute for one.</p>

<h2 id="independence">3. Independence and conflicts of interest</h2>
<p>New York City Administrative Code &sect;&sect; 20-870 through 20-874 requires that bias audits of automated employment decision tools be conducted by an independent auditor. We take that requirement seriously and it constrains what work we accept.</p>
<p>Greenpoint AI Compliance LLC:</p>
<ul>
<li>Does not develop, sell, license, resell or implement automated employment decision tools, applicant tracking systems, assessment platforms or any related software.</li>
<li>Does not hold equity, revenue-sharing arrangements, referral arrangements or any other financial interest in a vendor of such tools.</li>
<li>Does not accept compensation contingent on the outcome or findings of an assessment.</li>
<li>Will decline any engagement where a relationship exists that would compromise independence under applicable law, and will disclose in writing any relationship that could reasonably be perceived as bearing on independence.</li>
</ul>
<p>If you become aware of any circumstance that you believe affects our independence with respect to an engagement, tell us. We would rather decline work than sign a report whose independence can be questioned.</p>

<h2 id="terms">4. Terms of use</h2>
<p>By accessing this site you agree to these terms. If you do not agree, do not use the site.</p>
<p><strong>Permitted use.</strong> You may read, print and share this site&rsquo;s content for your own informational and internal business purposes.</p>
<p><strong>No warranty.</strong> This site and its content are provided &ldquo;as is,&rdquo; without warranty of any kind, express or implied, including any warranty of accuracy, completeness, merchantability or fitness for a particular purpose. Regulatory status changes, and material on this site may be out of date at the moment you read it.</p>
<p><strong>Limitation of liability.</strong> To the maximum extent permitted by law, Greenpoint AI Compliance LLC shall not be liable for any indirect, incidental, consequential, special or punitive damages, or any loss of profits, revenue, data or goodwill, arising from your use of or reliance on this site. Our total aggregate liability arising from your use of this site shall not exceed one hundred US dollars ($100). Nothing in these terms limits liability for fraud or for any liability that cannot lawfully be limited.</p>
<p><strong>Engagements are governed separately.</strong> These terms apply to the website only. Any services we provide are governed exclusively by a written engagement letter, which controls in the event of any conflict with these terms.</p>
<p><strong>Third-party links.</strong> Links to third-party sites are provided for convenience. We do not endorse and are not responsible for their content.</p>
<p><strong>Governing law.</strong> These terms are governed by the laws of the State of New York, without regard to conflict of laws principles. Any dispute shall be brought exclusively in the state or federal courts located in the State of New York.</p>
<p><strong>Changes.</strong> We may revise these terms at any time. The effective date at the top of this page indicates the current version.</p>

<h2 id="calculator">5. The calculator: limitations</h2>
<p>The four-fifths rule calculator on this site performs an arithmetic operation on numbers you enter. It is provided free and without warranty.</p>
<ul>
<li><strong>It does not constitute a bias audit</strong> under NYC Local Law 144 or any other law. A compliant audit requires independence, intersectional analysis, treatment of unknown-category individuals, and documentation the calculator does not produce.</li>
<li><strong>It does not assess statistical significance.</strong> Ratios computed on small groups are unstable and should be treated as directional only.</li>
<li><strong>It does not constitute a legal conclusion.</strong> A ratio below 0.80 is a screening threshold, not a finding of unlawful discrimination.</li>
<li><strong>Nothing you enter is transmitted to us.</strong> All calculation happens in your browser. We do not receive, store or have any means of accessing the figures you type.</li>
</ul>

<h2 id="privacy">6. Privacy policy</h2>
<p>This is a static informational website. It does not use accounts, forms, logins or payment processing. Our data practices are correspondingly minimal.</p>

<h3>What we collect through the website</h3>
<p><strong>Effectively nothing.</strong> We do not operate contact forms, newsletter signups, chat widgets or user accounts. We do not run advertising or behavioural tracking. The calculator processes data locally in your browser and transmits nothing.</p>
<p>Our hosting provider (Cloudflare) processes standard server request data, meaning IP address, user agent, requested URL and timestamp, as a technical necessity of delivering the site and protecting it from abuse. This is handled under Cloudflare&rsquo;s own privacy terms.</p>
<p>This site loads web fonts from Google Fonts. Doing so causes your browser to make a request to Google&rsquo;s servers, which may log your IP address. If you would prefer to avoid this, most browsers and privacy extensions can block third-party font requests. The site remains fully functional without them.</p>

<h3>What we collect when you contact us</h3>
<p>If you email us, we receive whatever you send, typically your name, email address, employer and a description of your situation. We use it solely to respond and, if you engage us, to perform the work. We do not sell it, rent it or share it for marketing purposes, and we do not add you to any mailing list without your express request.</p>

<h3>Client and engagement data</h3>
<p>Assessment engagements necessarily involve sensitive data, including demographic information about job applicants. That data is governed by the engagement letter and any data processing agreement executed with the client, not by this privacy policy. Our standard practice is to require pseudonymised or aggregated data wherever the analysis permits, to hold data only for as long as necessary, and to retain workpapers for seven years as professional standards require.</p>

<h3>Retention</h3>
<p>Email correspondence is retained for as long as necessary for the business purpose for which it was sent, and thereafter as required by applicable recordkeeping obligations.</p>

<h2 id="cookies">7. Cookies and tracking</h2>
<p><strong>This site sets no cookies.</strong> No analytics, no advertising pixels, no session storage, no local storage, no fingerprinting. There is no consent banner because there is nothing to consent to.</p>
<p>If this changes, for example if we add privacy-respecting analytics, we will update this section and the effective date above before doing so.</p>

<h2 id="rights">8. Your data rights</h2>
<p>Depending on where you live, you may have rights to access, correct, delete or restrict processing of personal information we hold about you, and to object to processing or request portability. This may include rights under the EU and UK General Data Protection Regulation, the California Consumer Privacy Act as amended, and comparable state laws.</p>
<p>Because we hold almost nothing, most such requests resolve quickly. To exercise any right, email <a href="mailto:{EMAIL}">{EMAIL}</a> and we will respond within the period the applicable law requires. We will not discriminate against you for exercising these rights.</p>
<p><strong>We do not sell or share personal information</strong> as those terms are defined under the California Consumer Privacy Act or any comparable state law.</p>

<h2 id="ip">9. Intellectual property</h2>
<p>All content on this site, including text, layout, design, graphics and the calculator, is &copy; 2026 Greenpoint AI Compliance LLC unless otherwise noted. You may quote briefly with attribution and a link. You may not republish substantial portions, or reproduce the calculator, without written permission.</p>
<p>Statutory text, regulatory citations and government publications referenced on this site are in the public domain. Third-party names and marks referenced are the property of their respective owners, and their mention does not imply any affiliation or endorsement.</p>

<h2 id="accessibility">10. Accessibility</h2>
<p>We aim to meet WCAG 2.1 Level AA. If you encounter a barrier to using this site, email us and we will address it, and tell you when it is fixed.</p>

<h2 id="contact">11. Contact</h2>
<p>Questions about anything on this page, or about our independence, data handling or terms:</p>
<p><strong>Greenpoint AI Compliance LLC</strong><br>
418 Broadway, Ste R<br>
Albany, NY 12207, USA<br>
<a href="mailto:{EMAIL}">{EMAIL}</a></p>

</div></div></section>
'''

write("legal.html", [
    head("Legal, Disclaimers &amp; Privacy | Greenpoint AI Compliance LLC",
         "Legal notices, terms of use, independence statement and privacy policy for Greenpoint AI Compliance LLC. This site sets no cookies and runs no tracking.",
         "legal.html", extra=legal_schema),
    chrome("legal.html"), legal_body, FOOTER,
])

# ================================================================= sitemap / robots
PAGES = [("", "1.0"), ("nyc-local-law-144-bias-audit-guide.html", "0.9"),
         ("four-fifths-rule-calculator.html", "0.9"), ("services.html", "0.8"),
         ("about.html", "0.6"), ("legal.html", "0.3")]
urls = "\n".join(
    '  <url><loc>%s/%s</loc><lastmod>2026-08-26</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>'
    % (SITE, p, pr) for p, pr in PAGES)
with io.open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '\n</urlset>\n')
print("wrote sitemap.xml")

with io.open("robots.txt", "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
print("wrote robots.txt")

with io.open("_headers", "w", encoding="utf-8") as f:
    f.write("""/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/styles.css
  Cache-Control: public, max-age=604800

/*.jpg
  Cache-Control: public, max-age=2592000
""")
print("wrote _headers")
