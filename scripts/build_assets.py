#!/usr/bin/env python3
"""Build the animated SVGs used by the GitHub profile README.

Run from the repo root:   python3 scripts/build_assets.py

Writes every graphic twice, into assets/dark/ and assets/light/, and the README
picks one through <picture> + prefers-color-scheme. All wording lives in the
CONTENT section, so edits never need SVG knowledge. Keep facts to verified ones,
never name employers or clients, and never use job-seeking language.

Text widths are measured with macOS system fonts (Palatino, Helvetica, Menlo)
only to lay things out; no font files are embedded in the SVGs.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# --------------------------------------------------------------------------- #
# CONTENT
# --------------------------------------------------------------------------- #
EYEBROW = "DATA & AI DELIVERY LEADER · INDIA · GLOBAL"
NAME = "Suman Mukherjee"
TAG_A, TAG_B = "I take AI from", "POC to P&L."
SUB = [
    "12+ years taking GenAI, ML and cloud-data programmes",
    "into governed production across insurance, life sciences",
    "and retail. Now leading a ~$5M Data & AI portfolio.",
]
TYPED = [
    "shipping GenAI & RAG into governed production",
    "agentic AI, with a human in the loop",
    "Responsible AI · LLMOps · model risk",
    "the model is rarely the bottleneck",
]
ORBIT_CHIPS = [("GenAI", 668, 118), ("RAG", 944, 122), ("Agents", 948, 268),
               ("LLMOps", 690, 322), ("Responsible AI", 866, 338)]
TICKER = ["GenAI", "RAG", "Agentic AI", "LLMOps", "Responsible AI", "Model risk",
          "Azure OpenAI", "AWS Bedrock", "Databricks", "Snowflake", "PySpark",
          "MLflow", "LangChain", "Power BI", "Customer 360", "Propensity models"]

# (final text, frames for the count-up, label, sub-label)
METRICS = [
    ("12+", [f"{i}+" for i in range(0, 13)], "YEARS IN AI & DATA", "SINCE 2014"),
    ("$5M", [f"${v/2:g}M" for v in range(0, 11)], "PORTFOLIO OWNED", "DATA & AI · INSURANCE"),
    ("~30%", [f"~{v}%" for v in range(0, 31, 3)], "LEAD CONVERSION LIFT", "PILOT MARKETS"),
    ("500TB+", [f"{v}TB" for v in range(0, 500, 50)] + ["500TB+"], "CLOUD DATA MIGRATED", "~$280K SAVED / YEAR"),
]

PIPELINE = [
    ("01", "The demo", ["Most AI dies as a POC.", "Start from the problem."]),
    ("02", "The data", ["Profiling, DQ checks,", "entity resolution first."]),
    ("03", "Guardrails", ["Responsible AI, model risk,", "human in the loop."]),
    ("04", "Production", ["Governed, audited, owned.", "LLMOps & MLOps in place."]),
    ("05", "P&L", ["Measured in conversion,", "retention and run-cost."]),
]

# (tag, title, metric, metric label, body, stack)
PROGRAMMES = [
    ("INSURANCE · GULF · 2024 → NOW", "Enterprise AI transformation", "~30%", "LEAD CONVERSION LIFT",
     "A ~$5M Data & AI portfolio: propensity models, GenAI cross-sell and a customer data "
     "platform across 15+ insurance products. 20+ people across 3 regions.",
     "AZURE ML · DATABRICKS · GENAI · CDP"),
    ("INSURANCE · GOVERNANCE", "AI/ML Centre of Practice", "", "GOVERNANCE FIRST",
     "Governance forum, LLMOps standards, Responsible AI controls and model-risk reviews, "
     "plus an agentic AI underwriting pilot with a human in the loop.",
     "LLMOPS · RESPONSIBLE AI · AZURE AI"),
    ("RETAIL · EUROPE & N. AMERICA", "Pricing analytics at scale", "14,000+", "STORES",
     "Pricing decision support, feature pipelines and ML retraining at retail scale, "
     "including a 100TB+ Azure migration.",
     "AZURE · DATABRICKS · SYNAPSE · ADLS"),
    ("MEDTECH · 12 APAC MARKETS", "Compliance ML", "70→95%", "PRECISION",
     "Anomaly detection that surfaces high-risk accounts for compliance and audit "
     "review, with far fewer false positives to chase.",
     "PYTHON · ANOMALY DETECTION · ENSEMBLES"),
    ("FINANCIAL SERVICES", "500TB+ AWS migration", "~$280K", "SAVED PER YEAR",
     "Delivery governance for a Redshift migration with a controlled cutover and a "
     "foundation for downstream ML workloads.",
     "REDSHIFT · GLUE · ATHENA"),
    ("INSURANCE · EARLIER", "AML detection & reporting", "~80%", "FASTER REPORTING",
     "An AML model that flags high-risk entities earlier, and industrialised Power BI "
     "reporting for 200+ users.",
     "DATABRICKS · POWER BI · PYTHON"),
]

# (file, top line, title, body, tags, badge)
PROJECTS = [
    ("portfolio", "mukherjeesuman.com", "Ask-me-anything portfolio",
     "A live answer engine grounded in my real work, a role-fit check that runs in "
     "your browser, and a scroll-driven film.",
     ["LLM Q&A", "Grounded answers", "Vercel"], "LIVE"),
    ("medicine", "sumankrsh/medicine-drug-advisor", "Medicine & Drug Advisor",
     "AI-powered medicine database and drug-interaction checker, focused on Indian "
     "medicines and mental-health drugs.",
     ["FastAPI", "React", "RAG"], ""),
    ("accelerator", "sumankrsh/ai-accelerator-toolkit", "AI-Accelerator Toolkit",
     "AI-readiness dashboards, a cloud blueprint generator, an ROI estimator and a "
     "GenAI playground for enterprise AI programmes.",
     ["Python", "Streamlit", "GenAI"], ""),
    ("sentiment", "sumankrsh/Sentiment-Analysis.ipynb", "Sentiment analysis with BERT",
     "Fine-tuned BERT with Hugging Face Transformers against a TF-IDF + Naive Bayes "
     "baseline: about 10% higher accuracy.",
     ["BERT", "Hugging Face", "NLP"], "★ 8"),
]

TOOLBOX = [
    ("GENAI & AGENTS", ["Azure OpenAI", "AWS Bedrock", "LangChain", "RAG", "Vector search",
                        "Agentic AI", "n8n"], False),
    ("ML & ANALYTICS", ["Python", "SQL", "PySpark", "MLflow", "Azure ML", "Propensity models",
                        "Power BI", "Tableau"], False),
    ("CLOUD & DATA", ["Azure", "Databricks", "Synapse", "AWS Redshift", "AWS Glue",
                      "Snowflake", "GCP"], False),
    ("GOVERNANCE", ["Responsible AI", "LLMOps", "Model risk", "Human in the loop",
                    "Audit-ready docs"], False),
    ("IN THE LAB NOW", ["LangGraph", "CrewAI", "Claude Agent SDK", "OpenAI Agents SDK", "MCP",
                        "A2A", "LLM evals", "Ollama", "Qdrant", "Azure AI Foundry",
                        "ISO/IEC 42001", "NIST AI RMF", "EU AI Act"], True),
]

CERTS = [
    (["Azure Solutions", "Architect Expert"], "MICROSOFT CERTIFIED"),
    (["TOGAF 9.2", "Enterprise Architect"], "THE OPEN GROUP"),
    (["Certified AI", "Professional"], "CAIP"),
    (["Project Management", "Professional"], "PMP · IN PROGRESS"),
]
EDUCATION = [
    ("PGP · AI & Machine Learning", "UT AUSTIN McCOMBS × GREAT LEARNING"),
    ("PGP · Data Engineering", "UMASS × SIMPLILEARN"),
    ("MBA · Finance & Systems", "SRM UNIVERSITY"),
]

BUTTONS = [  # (file, label, sub)
    ("btn-site", "Ask my AI anything", "mukherjeesuman.com"),
    ("btn-linkedin", "LinkedIn", "5K+ followers"),
    ("btn-email", "Email me", "replies in 24h"),
    ("btn-blog", "Read the blog", "AI in production"),
]

# --------------------------------------------------------------------------- #
# THEMES
# --------------------------------------------------------------------------- #
THEMES = {
    "dark": dict(bg1="#0A0913", bg2="#151034", card="#13111F", card2="#1A1630",
                 line="#2C2752", text="#F6F4FF", muted="#B9B2DB", dim="#827CAB",
                 violet="#8B6CFF", deep="#5B3DF5", lav="#C9BCFF", peach="#FFB39A",
                 green="#34D399", grid="#FFFFFF", grid_op=".07", blob_op=".55",
                 g1="#B9A8FF", g2="#FFB39A", core1="#EDE7FF", core2="#8B6CFF",
                 core3="#3A22B8", wave="#8B6CFF"),
    "light": dict(bg1="#FCFAF6", bg2="#F1ECFC", card="#FFFFFF", card2="#F8F5FF",
                  line="#E1DAF2", text="#15121F", muted="#4B4563", dim="#7D7797",
                  violet="#5B3DF5", deep="#4325D9", lav="#5B3DF5", peach="#E8775A",
                  green="#059669", grid="#2A2155", grid_op=".08", blob_op=".32",
                  g1="#5B3DF5", g2="#E8775A", core1="#F3EFFF", core2="#7C5CFF",
                  core3="#3A22B8", wave="#5B3DF5"),
}

# --------------------------------------------------------------------------- #
# HELPERS
# --------------------------------------------------------------------------- #
try:
    from PIL import ImageFont
    _F = {
        "serif": "/System/Library/Fonts/Palatino.ttc",
        "sans": "/System/Library/Fonts/Helvetica.ttc",
        "mono": "/System/Library/Fonts/Menlo.ttc",
    }

    def measure(text, kind="sans", size=16, bold=False, italic=False):
        idx = (2 if bold else 0) + (1 if italic and kind == "serif" else 0)
        if kind == "sans":
            idx = 1 if bold else 0
        if kind == "mono":
            return len(text) * size * 0.6
        return ImageFont.truetype(_F[kind], size, index=idx).getlength(text)
except Exception:  # PIL or fonts missing: fall back to averages
    def measure(text, kind="sans", size=16, bold=False, italic=False):
        return len(text) * size * {"serif": 0.5, "sans": 0.53, "mono": 0.6}[kind]


def e(s):
    return escape(s, {'"': "&quot;"})


def wrap(text, width_px, size, kind="sans", max_lines=None, slack=1.18):
    """Greedy wrap; `slack` leaves room for fallback fonts wider than Helvetica."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if measure(test, kind, size) * slack <= width_px:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        raise ValueError(f"Text needs {len(lines)} lines (max {max_lines}); shorten it: {text!r}")
    return lines


def mono(text, x, y, size, fill, track=0.0, anchor="start", extra=""):
    """Mono text with a fixed width so layout is identical on every machine."""
    tl = len(text) * (size * 0.6 + track)
    return (f'<text class="mono" x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" textLength="{tl:.1f}" lengthAdjust="spacing" {extra}>'
            f'{e(text)}</text>')


def mono_w(text, size, track=0.0):
    return len(text) * (size * 0.6 + track)


CSS_BASE = """
.serif{font-family:'Iowan Old Style','Palatino Linotype','Book Antiqua',Palatino,Georgia,serif}
.sans{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace}
.tb{transform-box:fill-box;transform-origin:center}
.up{animation:up .8s cubic-bezier(.2,.7,.2,1) both}
.fade{animation:fade 1s ease both}
.float{animation:float 6s ease-in-out infinite}
.blink{animation:blink 1.05s steps(1) infinite}
.flow{animation:flow 1.6s linear infinite}
.ping{animation:ping 3.2s cubic-bezier(.2,.6,.3,1) infinite}
.spin{animation:spin 40s linear infinite}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes blink{0%{opacity:1}50%{opacity:0}}
@keyframes flow{to{stroke-dashoffset:-16}}
@keyframes ping{0%{transform:scale(.7);opacity:.75}100%{transform:scale(1.9);opacity:0}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes d1{0%{transform:translate(0,0)}100%{transform:translate(70px,40px)}}
@keyframes d2{0%{transform:translate(0,0)}100%{transform:translate(-80px,-30px)}}
@keyframes d3{0%{transform:translate(0,0)}100%{transform:translate(40px,50px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def svg(W, H, t, body, css="", defs="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" fill="none" role="img">'
            + (f'<title>{e(title)}</title>' if title else "")
            + f'<style>{CSS_BASE}{css}</style>'
            + f'<defs>{text_grad(t)}{defs}</defs>{body}</svg>\n')


def text_grad(t):
    return (f'<linearGradient id="gtext" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{t["g1"]}"/><stop offset="1" stop-color="{t["g2"]}"/>'
            f'</linearGradient>'
            f'<linearGradient id="grun" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["peach"]}"/>'
            f'</linearGradient>')


def backdrop(W, H, t, r=22, blobs=True, uid="bd"):
    """Gradient panel with drifting aurora blobs and a faded dot grid."""
    d = (f'<clipPath id="{uid}c"><rect width="{W}" height="{H}" rx="{r}"/></clipPath>'
         f'<linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1">'
         f'<stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>'
         f'<filter id="{uid}b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>'
         f'<pattern id="{uid}p" width="22" height="22" patternUnits="userSpaceOnUse">'
         f'<circle cx="2" cy="2" r="1.1" fill="{t["grid"]}"/></pattern>'
         f'<radialGradient id="{uid}m" cx=".5" cy=".45" r=".7">'
         f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
         f'<mask id="{uid}k"><rect width="{W}" height="{H}" fill="url(#{uid}m)"/></mask>')
    b = f'<g clip-path="url(#{uid}c)"><rect width="{W}" height="{H}" fill="url(#{uid}g)"/>'
    if blobs:
        b += (f'<g filter="url(#{uid}b)" opacity="{t["blob_op"]}">'
              f'<circle cx="{W*0.14:.0f}" cy="{H*0.1:.0f}" r="{min(170, H*0.45):.0f}" fill="{t["violet"]}" '
              f'style="animation:d1 18s ease-in-out infinite alternate"/>'
              f'<circle cx="{W*0.86:.0f}" cy="{H*0.98:.0f}" r="{min(190, H*0.5):.0f}" fill="{t["peach"]}" opacity=".7" '
              f'style="animation:d2 22s ease-in-out infinite alternate"/>'
              f'<circle cx="{W*0.56:.0f}" cy="{-H*0.05:.0f}" r="{min(140, H*0.4):.0f}" fill="{t["deep"]}" '
              f'style="animation:d3 26s ease-in-out infinite alternate"/></g>')
    b += (f'<rect width="{W}" height="{H}" fill="url(#{uid}p)" opacity="{t["grid_op"]}" mask="url(#{uid}k)"/>'
          f'</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{r}" stroke="{t["line"]}"/>')
    return d, b


def star(cx, cy, s, fill):
    return (f'<path d="M{cx} {cy-s} C{cx+s*.15} {cy-s*.15} {cx+s*.15} {cy-s*.15} {cx+s} {cy} '
            f'C{cx+s*.15} {cy+s*.15} {cx+s*.15} {cy+s*.15} {cx} {cy+s} '
            f'C{cx-s*.15} {cy+s*.15} {cx-s*.15} {cy+s*.15} {cx-s} {cy} '
            f'C{cx-s*.15} {cy-s*.15} {cx-s*.15} {cy-s*.15} {cx} {cy-s}Z" fill="{fill}"/>')


def runner(x, y, w, h, r, dur, delay, uid):
    """A short light that runs around a rounded rectangle's border."""
    per = 2 * (w + h)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" stroke="url(#grun)" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-dasharray="{per*0.12:.0f} {per*0.88:.0f}" opacity=".95">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="{-per:.0f}" dur="{dur}s" '
            f'begin="{delay}s" repeatCount="indefinite"/></rect>')


# --------------------------------------------------------------------------- #
# HERO
# --------------------------------------------------------------------------- #
def hero(t):
    W, H = 1000, 420
    defs, body = backdrop(W, H, t, uid="h")
    o = [body]

    # eyebrow + status pill
    o.append(f'<g class="fade" style="animation-delay:.05s">{star(68, 73, 7, t["violet"])}'
             + mono(EYEBROW, 84, 78, 12.5, t["lav"], track=2.2) + '</g>')
    px, py = 742, 46
    pill_txt = "OPEN TO CONVERSATIONS"
    pw = mono_w(pill_txt, 11, 1.5) + 50
    o.append(f'<g class="fade" style="animation-delay:.3s">'
             f'<rect x="{px}" y="{py}" width="{pw:.0f}" height="30" rx="15" fill="{t["card"]}" fill-opacity=".75" stroke="{t["line"]}"/>'
             f'<circle cx="{px+18}" cy="{py+15}" r="4" fill="{t["green"]}"/>'
             f'<circle cx="{px+18}" cy="{py+15}" r="4" fill="{t["green"]}" class="tb ping"/>'
             + mono(pill_txt, px + 32, py + 19.5, 11, t["text"], track=1.5) + '</g>')

    # name + tagline (widths measured, then locked with textLength)
    nw = measure(NAME, "serif", 64)
    o.append(f'<text class="serif up" x="60" y="140" font-size="64" fill="{t["text"]}" '
             f'textLength="{nw:.0f}" lengthAdjust="spacingAndGlyphs" style="animation-delay:.12s">{e(NAME)}</text>')
    aw = measure(TAG_A, "serif", 40)
    bw = measure(TAG_B, "serif", 40, italic=True)
    bx = 60 + aw + 12
    o.append(f'<g class="up" style="animation-delay:.3s">'
             f'<rect x="{bx-4:.0f}" y="200" width="{bw+10:.0f}" height="11" rx="4" fill="url(#gtext)" opacity=".32" '
             f'class="tb" style="transform-origin:0 50%;animation:grow 1s 1s cubic-bezier(.2,.7,.2,1) both"/>'
             f'<text class="serif" x="60" y="194" font-size="40" fill="{t["text"]}" textLength="{aw:.0f}" '
             f'lengthAdjust="spacingAndGlyphs">{e(TAG_A)}</text>'
             f'<text class="serif" x="{bx:.0f}" y="194" font-size="40" font-style="italic" fill="url(#gtext)" '
             f'textLength="{bw:.0f}" lengthAdjust="spacingAndGlyphs">{e(TAG_B)}</text></g>')

    for i, line in enumerate(SUB):
        o.append(f'<text class="sans up" x="60" y="{236 + i*23}" font-size="17" fill="{t["muted"]}" '
                 f'style="animation-delay:{.45 + i*.08:.2f}s">{e(line)}</text>')

    # typing terminal line
    fs, cw = 16, 16 * 0.6
    x0, base = 92, 327
    o.append(f'<g class="up" style="animation-delay:.75s">'
             f'<rect x="52" y="304" width="574" height="34" rx="11" fill="{t["card"]}" fill-opacity=".72" stroke="{t["line"]}"/>'
             f'<text class="mono" x="68" y="{base}" font-size="{fs}" fill="{t["violet"]}">›</text>')
    t_type, t_hold, t_del, t_gap = 0.055, 2.1, 0.02, 0.35
    events, clock = [], 1.0
    for p in TYPED:
        n = len(p)
        ev = [(clock + k * t_type, k * cw) for k in range(1, n + 1)]
        end_type = clock + n * t_type
        ev += [(end_type + t_hold + k * t_del, (n - k) * cw) for k in range(1, n + 1)]
        events.append(ev)
        clock = end_type + t_hold + n * t_del + t_gap
    T = clock
    cursor = [(0, 0.0)]
    for i, (p, ev) in enumerate(zip(TYPED, events)):
        frames = [(0, 0.0)] + ev
        kt = ";".join(f"{a / T:.5f}" for a, _ in frames)
        vals = ";".join(f"{b:.1f}" for _, b in frames)
        defs += (f'<clipPath id="ty{i}"><rect x="{x0}" y="306" height="30" width="0">'
                 f'<animate attributeName="width" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                 f'keyTimes="{kt}" values="{vals}"/></rect></clipPath>')
        o.append(f'<g clip-path="url(#ty{i})">' + mono(p, x0, base, fs, t["text"]) + '</g>')
        cursor += ev
    kt = ";".join(f"{a / T:.5f}" for a, _ in cursor)
    vals = ";".join(f"{x0 + b + 1:.1f}" for _, b in cursor)
    o.append(f'<rect x="{x0+1}" y="{base-14}" width="9" height="18" rx="1.5" fill="{t["peach"]}" class="blink">'
             f'<animate attributeName="x" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
             f'keyTimes="{kt}" values="{vals}"/></rect></g>')

    # orb + orbits + chips
    cx, cy = 806, 212
    defs += (f'<radialGradient id="oglow"><stop offset="0" stop-color="{t["violet"]}" stop-opacity=".5"/>'
             f'<stop offset="1" stop-color="{t["violet"]}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="ocore" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="{t["core1"]}"/>'
             f'<stop offset=".45" stop-color="{t["core2"]}"/><stop offset="1" stop-color="{t["core3"]}"/></radialGradient>'
             f'<clipPath id="ocl"><circle cx="{cx}" cy="{cy}" r="60"/></clipPath>')
    g = [f'<g class="fade" style="animation-delay:.5s">']
    for label, lx, ly in ORBIT_CHIPS:
        g.append(f'<line x1="{lx}" y1="{ly}" x2="{cx}" y2="{cy}" stroke="{t["violet"]}" stroke-opacity=".45" '
                 f'stroke-dasharray="3 5" class="flow"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="130" fill="url(#oglow)"/>')
    g.append(f'<g><circle cx="{cx}" cy="{cy}" r="128" stroke="{t["line"]}" stroke-width="1.2" stroke-dasharray="1 7"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
             f'dur="60s" repeatCount="indefinite"/></g>')
    ell = f'M{cx-168},{cy} a168,58 0 1,0 336,0 a168,58 0 1,0 -336,0'
    g.append(f'<g transform="rotate(-18 {cx} {cy})"><path d="{ell}" stroke="{t["lav"]}" stroke-opacity=".45" '
             f'stroke-dasharray="2 6"/>')
    for k, (col, rr) in enumerate([(t["peach"], 4.5), (t["lav"], 3.5), (t["violet"], 3)]):
        g.append(f'<circle r="{rr}" fill="{col}"><animateMotion dur="10s" begin="{-k*3.3:.1f}s" '
                 f'repeatCount="indefinite" path="{ell}"/></circle>')
    g.append('</g>')
    for k in range(2):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="60" stroke="{t["violet"]}" stroke-width="1.5" class="tb ping" '
                 f'style="animation-delay:{k*1.6}s"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="60" fill="url(#ocore)"/>')
    wave = "M{x0},{y} " + " ".join(f"q 15,{-a} 30,0 q 15,{a} 30,0" for a in [14, 14, 14, 14, 14, 14, 14, 14])
    g.append(f'<g clip-path="url(#ocl)" opacity=".85">'
             f'<path d="{wave.format(x0=cx-120, y=cy)}" stroke="#fff" stroke-width="2" stroke-opacity=".85">'
             f'<animateTransform attributeName="transform" type="translate" from="0 0" to="60 0" dur="1.8s" repeatCount="indefinite"/></path>'
             f'<path d="{wave.format(x0=cx-150, y=cy+4).replace("14", "8")}" stroke="#fff" stroke-width="1.5" stroke-opacity=".4">'
             f'<animateTransform attributeName="transform" type="translate" from="0 0" to="60 0" dur="2.6s" repeatCount="indefinite"/></path></g>')
    g.append(f'<ellipse cx="{cx-20}" cy="{cy-28}" rx="24" ry="12" fill="#fff" opacity=".22"/>')
    for k, (label, lx, ly) in enumerate(ORBIT_CHIPS):
        w = mono_w(label, 12, 0.4) + 26
        g.append(f'<g class="float" style="animation-delay:{-k*1.3:.1f}s">'
                 f'<rect x="{lx - w/2:.1f}" y="{ly-14}" width="{w:.1f}" height="28" rx="14" fill="{t["card"]}" stroke="{t["line"]}"/>'
                 + mono(label, lx, ly + 4.5, 12, t["text"], track=0.4, anchor="middle") + '</g>')
    g.append('</g>')
    o += g

    # ticker
    items = "  ·  ".join(i.upper() for i in TICKER) + "  ·  "
    fs_t, tr = 12, 1.6
    L = mono_w(items, fs_t, tr)
    defs += (f'<linearGradient id="tkf"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/>'
             f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<mask id="tkm"><rect width="{W}" height="{H}" fill="url(#tkf)"/></mask>')
    o.append(f'<line x1="24" y1="366" x2="{W-24}" y2="366" stroke="{t["line"]}"/>'
             f'<g mask="url(#tkm)"><g>'
             + mono(items, 0, 399, fs_t, t["dim"], track=tr) + mono(items, L, 399, fs_t, t["dim"], track=tr)
             + f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-L:.1f} 0" '
               f'dur="{L/38:.1f}s" repeatCount="indefinite"/></g></g>')

    css = "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    return svg(W, H, t, "".join(o), css, defs,
               title=f"{NAME}: Data & AI Delivery Leader. I take AI from POC to P&L.")


# --------------------------------------------------------------------------- #
# METRICS (count-up tiles)
# --------------------------------------------------------------------------- #
def metrics(t):
    W, H, gap = 1000, 168, 16
    tw = (W - 3 * gap) / 4
    o, defs = [], ""
    for i, (final, frames, label, sub) in enumerate(METRICS):
        x = i * (tw + gap)
        cx = x + tw / 2
        delay = 0.25 + i * 0.18
        defs += f'<clipPath id="mc{i}"><rect x="{x}" y="0" width="{tw}" height="{H}" rx="18"/></clipPath>'
        o.append(f'<g class="up" style="animation-delay:{delay - .2:.2f}s">'
                 f'<rect x="{x+.5}" y=".5" width="{tw-1}" height="{H-1}" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>')
        # shine sweep
        o.append(f'<g clip-path="url(#mc{i})"><rect x="{x-120}" y="-20" width="70" height="{H+40}" '
                 f'fill="{t["lav"]}" opacity=".07" transform="skewX(-18)">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;{tw+260} 0;{tw+260} 0" '
                 f'keyTimes="0;.35;1" dur="7s" begin="{1.5+i*0.6:.1f}s" repeatCount="indefinite" additive="sum"/></rect></g>')
        # count-up frames (ease-out timing)
        n = len(frames) - 1
        dur = 1.6
        times = [delay + dur * (1 - (1 - k / n) ** 2) for k in range(n + 1)]
        for k, f in enumerate(frames):
            vis = "visible" if k == 0 else "hidden"
            anim = ""
            if k > 0:
                anim += f'<set attributeName="visibility" to="visible" begin="{times[k]:.3f}s"/>'
            if k < n:
                anim += f'<set attributeName="visibility" to="hidden" begin="{times[k+1]:.3f}s"/>'
            o.append(f'<text class="sans" x="{cx:.1f}" y="78" font-size="46" font-weight="700" letter-spacing="-1" '
                     f'text-anchor="middle" fill="url(#gtext)" visibility="{vis}">{e(f)}{anim}</text>')
        o.append(mono(label, cx, 108, 11.5, t["text"], track=1.4, anchor="middle"))
        o.append(mono(sub, cx, 128, 10, t["dim"], track=1.2, anchor="middle"))
        # progress bar
        o.append(f'<rect x="{x+28}" y="{H-24}" width="{tw-56}" height="3" rx="1.5" fill="{t["line"]}"/>'
                 f'<rect x="{x+28}" y="{H-24}" width="{tw-56}" height="3" rx="1.5" fill="url(#gtext)" class="tb" '
                 f'style="transform-origin:0 50%;animation:grow {dur}s {delay}s cubic-bezier(.2,.7,.2,1) both"/>')
        o.append('</g>')
    css = "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    return svg(W, H, t, "".join(o), css, defs,
               title="12+ years in AI and data · $5M portfolio owned · ~30% lead conversion lift · 500TB+ cloud data migrated")


# --------------------------------------------------------------------------- #
# PIPELINE (POC to P&L)
# --------------------------------------------------------------------------- #
def pipeline(t):
    W, H = 1000, 240
    defs, body = backdrop(W, H, t, uid="p", blobs=True)
    o = [body]
    xs = [110 + i * 195 for i in range(5)]
    y = 82
    travel, cycle = 4.8, 6.4
    defs += (f'<linearGradient id="comet" x1="0" x2="1"><stop offset="0" stop-color="{t["violet"]}" stop-opacity="0"/>'
             f'<stop offset=".7" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["peach"]}"/></linearGradient>')
    o.append(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{t["line"]}" stroke-width="2"/>')
    o.append(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{t["violet"]}" stroke-opacity=".5" '
             f'stroke-width="2" stroke-dasharray="3 5" class="flow"/>')
    span = xs[-1] - xs[0]
    o.append(f'<rect x="{xs[0]-130}" y="{y-2}" width="130" height="4" rx="2" fill="url(#comet)">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;{span} 0;{span} 0" '
             f'keyTimes="0;{travel/cycle:.3f};1" dur="{cycle}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{travel/cycle:.3f};{(travel+.4)/cycle:.3f};1" '
             f'dur="{cycle}s" repeatCount="indefinite"/></rect>')
    for i, (num, title, cap) in enumerate(PIPELINE):
        x = xs[i]
        last = i == len(PIPELINE) - 1
        col = t["peach"] if last else t["violet"]
        p = (travel * (x - xs[0]) / span) / cycle
        a, b, c = max(p - .02, 0.0005), p, min(p + .14, .999)
        kts = f"0;{a:.3f};{b:.3f};{c:.3f};1"
        o.append(f'<g class="up" style="animation-delay:{.15 + i*.12:.2f}s">')
        o.append(f'<circle cx="{x}" cy="{y}" r="30" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>')
        o.append(f'<circle cx="{x}" cy="{y}" r="30" stroke="{col}" stroke-width="2.2" opacity="{.9 if last else 0}">'
                 + ("" if last else
                    f'<animate attributeName="opacity" values="0;0;1;.15;0" keyTimes="{kts}" dur="{cycle}s" repeatCount="indefinite"/>')
                 + '</circle>')
        o.append(f'<circle cx="{x}" cy="{y}" r="30" fill="{col}" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;.28;0;0" keyTimes="{kts}" dur="{cycle}s" repeatCount="indefinite"/></circle>')
        o.append(mono(num, x, y + 5, 14, col, anchor="middle"))
        o.append(f'<text class="serif" x="{x}" y="{y + 66}" font-size="23" text-anchor="middle" fill="{t["text"]}"'
                 + (f' font-style="italic"' if last else "") + f'>{e(title)}</text>')
        for j, line in enumerate(cap):
            o.append(f'<text class="sans" x="{x}" y="{y + 94 + j*20}" font-size="14" text-anchor="middle" '
                     f'fill="{t["muted"]}">{e(line)}</text>')
        o.append('</g>')
    return svg(W, H, t, "".join(o), "", defs,
               title="How I take AI from POC to P&L: the demo, the data, guardrails, production, P&L")


# --------------------------------------------------------------------------- #
# PROGRAMMES (selected work, no client names)
# --------------------------------------------------------------------------- #
def programmes(t):
    W, gap, cw, ch = 1000, 20, 490, 212
    rows = (len(PROGRAMMES) + 1) // 2
    H = rows * ch + (rows - 1) * gap
    o, defs = [], ""
    for i, (tag, title, metric, mlabel, text, stack) in enumerate(PROGRAMMES):
        x = (i % 2) * (cw + gap)
        y = (i // 2) * (ch + gap)
        o.append(f'<g class="up" style="animation-delay:{.1 + i*.1:.2f}s">')
        o.append(f'<rect x="{x+.5}" y="{y+.5}" width="{cw-1}" height="{ch-1}" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>')
        o.append(runner(x + .5, y + .5, cw - 1, ch - 1, 18, 9, -i * 1.5, f"pr{i}"))
        o.append(mono(tag, x + 26, y + 36, 10.5, t["violet"], track=1.3))
        o.append(f'<text class="serif" x="{x+26}" y="{y+70}" font-size="24" fill="{t["text"]}">{e(title)}</text>')
        if metric:
            o.append(f'<text class="sans" x="{x+cw-26}" y="{y+68}" font-size="30" font-weight="700" letter-spacing="-.5" '
                     f'text-anchor="end" fill="url(#gtext)">{e(metric)}</text>')
        else:  # shield with a check that draws itself
            sx, sy = x + cw - 48, y + 46
            o.append(f'<path d="M{sx} {sy-22} l18 7 v12 c0 12 -8 19 -18 23 c-10 -4 -18 -11 -18 -23 v-12 z" '
                     f'fill="{t["violet"]}" fill-opacity=".14" stroke="url(#gtext)" stroke-width="2" stroke-linejoin="round"/>'
                     f'<path d="M{sx-7} {sy} l5 5 l9 -10" stroke="url(#grun)" stroke-width="2.4" stroke-linecap="round" '
                     f'stroke-linejoin="round" stroke-dasharray="24" stroke-dashoffset="24" '
                     f'style="animation:draw .8s 1.2s ease-out forwards"/>')
        o.append(mono(mlabel, x + cw - 26, y + 86, 9.5, t["dim"], track=1.1, anchor="end"))
        for j, line in enumerate(wrap(text, cw - 52, 15, max_lines=3)):
            o.append(f'<text class="sans" x="{x+26}" y="{y+114 + j*21}" font-size="15" fill="{t["muted"]}">{e(line)}</text>')
        o.append(f'<line x1="{x+26}" y1="{y+ch-40}" x2="{x+cw-26}" y2="{y+ch-40}" stroke="{t["line"]}"/>')
        o.append(mono(stack, x + 26, y + ch - 17, 10, t["dim"], track=1.2))
        o.append('</g>')
    return svg(W, H, t, "".join(o), "@keyframes draw{to{stroke-dashoffset:0}}", defs, title="Selected programmes")


# --------------------------------------------------------------------------- #
# PROJECT CARDS
# --------------------------------------------------------------------------- #
def project(t, top, title, text, tags, badge):
    W, H = 490, 234
    o = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>']
    defs = (f'<radialGradient id="cg"><stop offset="0" stop-color="{t["violet"]}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{t["violet"]}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    o.append(f'<g clip-path="url(#cc)"><circle cx="{W-40}" cy="10" r="120" fill="url(#cg)" class="tb" '
             f'style="animation:breathe 6s ease-in-out infinite"/></g>')
    o.append(runner(.5, .5, W - 1, H - 1, 18, 8, 0, "pc"))
    # repo glyph
    o.append(f'<path d="M28 26h10a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H28z M28 26v13" stroke="{t["dim"]}" stroke-width="1.5" '
             f'stroke-linejoin="round"/>')
    o.append(mono(top, 50, 38, 12, t["dim"], track=0.2))
    if badge:
        live = badge == "LIVE"
        bw = mono_w(badge, 11, 1.2) + (36 if live else 22)
        o.append(f'<rect x="{W-24-bw:.1f}" y="21" width="{bw:.1f}" height="24" rx="12" fill="{t["card2"]}" stroke="{t["line"]}"/>')
        if live:
            o.append(f'<circle cx="{W-24-bw+15:.1f}" cy="33" r="3.5" fill="{t["green"]}"/>'
                     f'<circle cx="{W-24-bw+15:.1f}" cy="33" r="3.5" fill="{t["green"]}" class="tb ping"/>')
            o.append(mono(badge, W - 24 - bw + 26, 37, 11, t["text"], track=1.2))
        else:
            o.append(mono(badge, W - 24 - bw / 2, 37, 11, t["text"], track=1.2, anchor="middle"))
    o.append(f'<text class="serif" x="28" y="82" font-size="26" fill="{t["text"]}">{e(title)}</text>')
    for j, line in enumerate(wrap(text, W - 56, 15.5, max_lines=3)):
        o.append(f'<text class="sans" x="28" y="{112 + j*22}" font-size="15.5" fill="{t["muted"]}">{e(line)}</text>')
    tx = 28
    for tag in tags:
        w = mono_w(tag, 11.5, 0.3) + 24
        o.append(f'<rect x="{tx}" y="{H-46}" width="{w:.1f}" height="26" rx="13" fill="{t["card2"]}" stroke="{t["line"]}"/>')
        o.append(mono(tag, tx + w / 2, H - 28.5, 11.5, t["lav"], track=0.3, anchor="middle"))
        tx += w + 8
    o.append(f'<g class="nudge"><path d="M{W-48} {H-24} l12 -12 m-8 0 h8 v8" stroke="{t["violet"]}" stroke-width="2" '
             f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    css = ("@keyframes breathe{0%,100%{transform:scale(1);opacity:.8}50%{transform:scale(1.15);opacity:1}}"
           ".nudge{animation:nudge 2.4s ease-in-out infinite}"
           "@keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}")
    return svg(W, H, t, "".join(o), css, defs, title=title)


# --------------------------------------------------------------------------- #
# TOOLBOX
# --------------------------------------------------------------------------- #
def toolbox(t):
    W, lx, x0, x1 = 1000, 24, 196, 976
    ph, rgap, pgap = 30, 14, 9
    rows, y = [], 22
    for label, items, lab in TOOLBOX:
        x, line_y, pills = x0, y, []
        for it in items:
            w = mono_w(it, 12.5, 0.2) + 28
            if x + w > x1:
                x, line_y = x0, line_y + ph + 10
            pills.append((it, x, line_y, w))
            x += w + pgap
        rows.append((label, y, pills, lab))
        y = line_y + ph + rgap + 8
    H = y + 6
    defs, body = backdrop(W, H, t, uid="tb", blobs=False)
    o = [body]
    n_all = sum(len(r[2]) for r in rows)
    step = 0.35
    cyc = n_all * step
    k = 0
    for ri, (label, ry, pills, lab) in enumerate(rows):
        o.append(mono(label, lx, ry + 20, 10.5, t["lav"] if not lab else t["peach"], track=1.4))
        if ri:
            o.append(f'<line x1="{lx}" y1="{ry - 11}" x2="{W - lx}" y2="{ry - 11}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
        for it, x, py, w in pills:
            dash = ' stroke-dasharray="3 3"' if lab else ""
            o.append(f'<g class="up" style="animation-delay:{.05 + k*.025:.3f}s">'
                     f'<rect x="{x}" y="{py}" width="{w:.1f}" height="{ph}" rx="15" fill="{t["card"]}" stroke="{t["line"]}"{dash}/>'
                     f'<rect x="{x}" y="{py}" width="{w:.1f}" height="{ph}" rx="15" stroke="url(#grun)" stroke-width="1.5" '
                     f'opacity="0" style="animation:hi {cyc:.1f}s {k*step:.2f}s infinite"/>'
                     + mono(it, x + w / 2, py + 19.5, 12.5, t["text"] if not lab else t["muted"], track=0.2, anchor="middle")
                     + '</g>')
            k += 1
    hi = 100 * 2.2 / cyc
    css = (f"@keyframes hi{{0%{{opacity:0}}{hi/2:.2f}%{{opacity:1}}{hi:.2f}%{{opacity:0}}100%{{opacity:0}}}}")
    return svg(W, H, t, "".join(o), css, defs, title="Toolbox")


# --------------------------------------------------------------------------- #
# CREDENTIALS
# --------------------------------------------------------------------------- #
def credentials(t):
    W, gap, th = 1000, 16, 96
    H = th * 2 + gap
    o, defs = [], ""
    cwid = (W - 3 * gap) / 4
    ewid = (W - 2 * gap) / 3

    def seal(cx, cy, col, glyph, i):
        s = (f'<g><circle cx="{cx}" cy="{cy}" r="28" stroke="{col}" stroke-opacity=".55" stroke-dasharray="2 4"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
             f'dur="{24 + i*3}s" repeatCount="indefinite"/></g>'
             f'<circle cx="{cx}" cy="{cy}" r="21" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="1.5"/>')
        if glyph == "check":
            s += (f'<path d="M{cx-8} {cy+1} l5.5 5.5 l10.5 -11" stroke="{col}" stroke-width="2.6" stroke-linecap="round" '
                  f'stroke-linejoin="round" stroke-dasharray="30" stroke-dashoffset="30" '
                  f'style="animation:draw .7s {0.6 + i*.15:.2f}s ease-out forwards"/>')
        else:
            s += (f'<path d="M{cx-13} {cy-3} L{cx} {cy-10} L{cx+13} {cy-3} L{cx} {cy+4} Z" stroke="{col}" stroke-width="1.8" '
                  f'stroke-linejoin="round"/><path d="M{cx-7} {cy} v6 c0 4 14 4 14 0 v-6" stroke="{col}" stroke-width="1.8"/>')
        return s

    for i, (lines, issuer) in enumerate(CERTS):
        x = i * (cwid + gap)
        o.append(f'<g class="up" style="animation-delay:{.1 + i*.1:.2f}s">'
                 f'<rect x="{x+.5}" y=".5" width="{cwid-1:.1f}" height="{th-1}" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>'
                 + seal(x + 40, th / 2, t["violet"], "check", i))
        fs = min(15, 15 * (cwid - 92) / max(measure(ln, "sans", 15, bold=True) * 1.2 for ln in lines))
        for j, ln in enumerate(lines):
            o.append(f'<text class="sans" x="{x+76:.1f}" y="{33 + j*19}" font-size="{fs:.1f}" font-weight="600" '
                     f'fill="{t["text"]}">{e(ln)}</text>')
        o.append(mono(issuer, x + 76, 76, 9.5, t["dim"], track=0.9) + '</g>')
    for i, (title, issuer) in enumerate(EDUCATION):
        x = i * (ewid + gap)
        y = th + gap
        o.append(f'<g class="up" style="animation-delay:{.5 + i*.1:.2f}s">'
                 f'<rect x="{x+.5:.1f}" y="{y+.5}" width="{ewid-1:.1f}" height="{th-1}" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>'
                 + seal(x + 40, y + th / 2, t["peach"], "cap", i + 4)
                 + f'<text class="sans" x="{x+76:.1f}" y="{y+44}" font-size="{min(15.5, 15.5 * (ewid - 92) / (measure(title, "sans", 15.5, bold=True) * 1.2)):.1f}" '
                   f'font-weight="600" fill="{t["text"]}">{e(title)}</text>'
                 + mono(issuer, x + 76, y + 66, 9.5, t["dim"], track=0.7) + '</g>')
    css = "@keyframes draw{to{stroke-dashoffset:0}}"
    return svg(W, H, t, "".join(o), css, defs,
               title="Certifications: Azure Solutions Architect Expert, TOGAF 9.2, CAIP, PMP in progress. "
                     "Education: PGP AI & ML, PGP Data Engineering, MBA Finance & Systems")


# --------------------------------------------------------------------------- #
# CTA + BUTTONS + FOOTER
# --------------------------------------------------------------------------- #
def cta(t):
    W, H = 1000, 236
    defs, body = backdrop(W, H, t, uid="c")
    o = [body]
    o.append(f'<g class="fade">{star(68, 52, 6, t["violet"])}' + mono("START A CONVERSATION", 82, 57, 12, t["lav"], track=2.2) + '</g>')
    h1 = "Have an AI programme in mind?"
    w1 = measure(h1, "serif", 40)
    o.append(f'<text class="serif up" x="60" y="108" font-size="40" fill="{t["text"]}" textLength="{w1:.0f}" '
             f'lengthAdjust="spacingAndGlyphs" style="animation-delay:.1s">{e(h1)}</text>')
    h2 = "Let's talk."
    w2 = measure(h2, "serif", 40, italic=True)
    o.append(f'<text class="serif up" x="60" y="154" font-size="40" font-style="italic" fill="url(#gtext)" '
             f'textLength="{w2:.0f}" lengthAdjust="spacingAndGlyphs" style="animation-delay:.2s">{e(h2)}</text>')
    o.append(f'<text class="sans up" x="60" y="192" font-size="15.5" fill="{t["muted"]}" style="animation-delay:.3s">'
             f'AI transformation · GenAI &amp; agentic delivery · AI governance · advisory</text>')
    o.append(f'<text class="sans up" x="60" y="214" font-size="15.5" fill="{t["muted"]}" style="animation-delay:.35s">'
             f'I reply within 24 hours, straight from my inbox.</text>')
    bx, by, bw, bh = 712, 92, 236, 52
    defs += (f'<linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="{t["violet"]}"/>'
             f'<stop offset="1" stop-color="{t["deep"]}"/></linearGradient>'
             f'<filter id="bglow" x="-50%" y="-80%" width="200%" height="260%"><feGaussianBlur stdDeviation="14"/></filter>')
    o.append(f'<g class="up" style="animation-delay:.4s">'
             f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="{t["violet"]}" filter="url(#bglow)" '
             f'class="tb" style="animation:glow 2.8s ease-in-out infinite"/>'
             f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="url(#bg)"/>'
             f'<text class="sans" x="{bx+30}" y="{by+32}" font-size="17" font-weight="600" fill="#fff">Ask my AI anything</text>'
             f'<g class="nudge"><path d="M{bx+bw-44} {by+26} h16 m-6 -6 l6 6 l-6 6" stroke="#fff" stroke-width="2.2" '
             f'stroke-linecap="round" stroke-linejoin="round"/></g>'
             + mono("mukherjeesuman.com", bx + bw / 2, by + bh + 28, 11.5, t["dim"], track=1, anchor="middle") + '</g>')
    css = ("@keyframes glow{0%,100%{opacity:.35;transform:scale(.96)}50%{opacity:.75;transform:scale(1.04)}}"
           ".nudge{animation:nudge 1.8s ease-in-out infinite}"
           "@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}")
    return svg(W, H, t, "".join(o), css, defs, title="Have an AI programme in mind? Let's talk.")


def button(t, label, sub, primary=False):
    lw = measure(label, "sans", 15, bold=True)
    sw = mono_w(sub, 10, 0.8)
    W = int(max(lw * 1.2, sw) + 64)
    H = 54
    fill = "url(#bb)" if primary else t["card"]
    fg = "#fff" if primary else t["text"]
    sg = "#E9E3FF" if primary else t["dim"]
    defs = (f'<linearGradient id="bb" x1="0" x2="1"><stop offset="0" stop-color="{t["violet"]}"/>'
            f'<stop offset="1" stop-color="{t["deep"]}"/></linearGradient>')
    o = [f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="{fill}" stroke="{t["line"] if not primary else t["deep"]}" stroke-width="1.5"/>']
    if not primary:
        o.append(runner(.75, .75, W - 1.5, H - 1.5, 14, 6, 0, "b"))
    o.append(f'<text class="sans" x="18" y="24" font-size="15" font-weight="600" fill="{fg}">{e(label)}</text>')
    o.append(mono(sub, 18, 41, 10, sg, track=0.8))
    o.append(f'<g class="nudge"><path d="M{W-30} {H/2+5} l9 -9 m-6 0 h6 v6" stroke="{fg}" stroke-width="1.8" '
             f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    css = (".nudge{animation:nudge 2.2s ease-in-out infinite}"
           "@keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(2px,-2px)}}")
    return svg(W, H, t, "".join(o), css, defs, title=f"{label}: {sub}")


def footer(t):
    W, H = 1000, 90

    def wave(amp, length, y):
        segs = int(2 * W / length) + 3
        return f"M{-length} {y} " + " ".join(
            f"q {length/4:.1f} {-amp} {length/2:.1f} 0 q {length/4:.1f} {amp} {length/2:.1f} 0" for _ in range(segs))

    defs = ('<linearGradient id="ff"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".2" stop-color="#fff"/><stop offset=".8" stop-color="#fff"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="fm"><rect width="{W}" height="{H}" fill="url(#ff)"/></mask>')
    o = ['<g mask="url(#fm)">']
    for amp, length, y, op, dur, w in [(12, 260, 38, .9, 12, 2), (16, 340, 46, .55, 18, 1.5),
                                       (9, 200, 54, .4, 9, 1.2), (6, 420, 62, .3, 24, 1)]:
        o.append(f'<path d="{wave(amp, length, y)}" stroke="url(#grun)" stroke-width="{w}" opacity="{op}">'
                 f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{length} 0" '
                 f'dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append('</g>')
    return svg(W, H, t, "".join(o), "", defs, title="")



# --------------------------------------------------------------------------- #
# COMPACT (phones and narrow windows). Shown below 1100px viewport width.
# Always the dark palette: these are self-contained cards that read well on
# either GitHub theme, and it avoids combining width + colour-scheme rules.
# --------------------------------------------------------------------------- #
SUB_C = ["12+ years taking GenAI and ML", "into governed production."]
TYPED_C = ["GenAI & RAG in production", "agentic AI, human in the loop",
           "Responsible AI · LLMOps", "~$5M Data & AI portfolio"]
PROJECT_SHORT = {
    "portfolio": "Live AI answers grounded in my real work.",
    "medicine": "Drug-interaction checker built on RAG.",
    "accelerator": "AI readiness, cloud blueprints and ROI.",
    "sentiment": "Fine-tuned BERT: ~10% above a TF-IDF baseline.",
}


def typing(defs, o, t, phrases, x0, base, fs, clip_y, clip_h, uid):
    cw = fs * 0.6
    t_type, t_hold, t_del, t_gap = 0.055, 2.1, 0.02, 0.35
    events, clock = [], 1.0
    for p in phrases:
        n = len(p)
        ev = [(clock + k * t_type, k * cw) for k in range(1, n + 1)]
        end_type = clock + n * t_type
        ev += [(end_type + t_hold + k * t_del, (n - k) * cw) for k in range(1, n + 1)]
        events.append(ev)
        clock = end_type + t_hold + n * t_del + t_gap
    T = clock
    cursor = [(0, 0.0)]
    for i, (p, ev) in enumerate(zip(phrases, events)):
        frames = [(0, 0.0)] + ev
        defs.append(f'<clipPath id="{uid}{i}"><rect x="{x0}" y="{clip_y}" height="{clip_h}" width="0">'
                    f'<animate attributeName="width" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                    f'keyTimes="{";".join(f"{a / T:.5f}" for a, _ in frames)}" '
                    f'values="{";".join(f"{b:.1f}" for _, b in frames)}"/></rect></clipPath>')
        o.append(f'<g clip-path="url(#{uid}{i})">' + mono(p, x0, base, fs, t["text"]) + '</g>')
        cursor += ev
    o.append(f'<rect x="{x0+1}" y="{base - fs*0.85:.1f}" width="{fs*0.55:.1f}" height="{fs*1.1:.1f}" rx="1.5" '
             f'fill="{t["peach"]}" class="blink"><animate attributeName="x" dur="{T:.2f}s" repeatCount="indefinite" '
             f'calcMode="discrete" keyTimes="{";".join(f"{a / T:.5f}" for a, _ in cursor)}" '
             f'values="{";".join(f"{x0 + b + 1:.1f}" for _, b in cursor)}"/></rect>')


def hero_c(t):
    W, H = 600, 700
    d0, body = backdrop(W, H, t, uid="h")
    defs, o = [d0], [body]
    pill = "OPEN TO CONVERSATIONS"
    pw = mono_w(pill, 15, 1.5) + 58
    o.append(f'<g class="fade"><rect x="36" y="34" width="{pw:.0f}" height="40" rx="20" fill="{t["card"]}" '
             f'fill-opacity=".75" stroke="{t["line"]}"/><circle cx="60" cy="54" r="5" fill="{t["green"]}"/>'
             f'<circle cx="60" cy="54" r="5" fill="{t["green"]}" class="tb ping"/>'
             + mono(pill, 76, 59.5, 15, t["text"], track=1.5) + '</g>')
    cx, cy = 300, 200
    defs.append(f'<radialGradient id="oglow"><stop offset="0" stop-color="{t["violet"]}" stop-opacity=".5"/>'
                f'<stop offset="1" stop-color="{t["violet"]}" stop-opacity="0"/></radialGradient>'
                f'<radialGradient id="ocore" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="{t["core1"]}"/>'
                f'<stop offset=".45" stop-color="{t["core2"]}"/><stop offset="1" stop-color="{t["core3"]}"/></radialGradient>'
                f'<clipPath id="ocl"><circle cx="{cx}" cy="{cy}" r="58"/></clipPath>')
    chips = [("GenAI", 112, 132), ("RAG", 494, 120), ("Agents", 488, 282), ("LLMOps", 116, 280)]
    g = ['<g class="fade" style="animation-delay:.3s">']
    for _, lx, ly in chips:
        g.append(f'<line x1="{lx}" y1="{ly}" x2="{cx}" y2="{cy}" stroke="{t["violet"]}" stroke-opacity=".45" '
                 f'stroke-dasharray="3 5" class="flow"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="125" fill="url(#oglow)"/>')
    g.append(f'<g><circle cx="{cx}" cy="{cy}" r="112" stroke="{t["line"]}" stroke-width="1.4" stroke-dasharray="1 7"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
             f'dur="60s" repeatCount="indefinite"/></g>')
    ell = f'M{cx-160},{cy} a160,54 0 1,0 320,0 a160,54 0 1,0 -320,0'
    g.append(f'<g transform="rotate(-14 {cx} {cy})"><path d="{ell}" stroke="{t["lav"]}" stroke-opacity=".45" stroke-dasharray="2 6"/>')
    for k, (col, rr) in enumerate([(t["peach"], 5), (t["lav"], 4), (t["violet"], 3.5)]):
        g.append(f'<circle r="{rr}" fill="{col}"><animateMotion dur="10s" begin="{-k*3.3:.1f}s" repeatCount="indefinite" path="{ell}"/></circle>')
    g.append('</g>')
    for k in range(2):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="58" stroke="{t["violet"]}" stroke-width="1.6" class="tb ping" style="animation-delay:{k*1.6}s"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="url(#ocore)"/>')
    wave = " ".join("q 15,-14 30,0 q 15,14 30,0" for _ in range(8))
    g.append(f'<g clip-path="url(#ocl)"><path d="M{cx-120},{cy} {wave}" stroke="#fff" stroke-width="2.2" stroke-opacity=".85">'
             f'<animateTransform attributeName="transform" type="translate" from="0 0" to="60 0" dur="1.8s" repeatCount="indefinite"/></path></g>')
    g.append(f'<ellipse cx="{cx-20}" cy="{cy-27}" rx="23" ry="11" fill="#fff" opacity=".22"/>')
    for k, (label, lx, ly) in enumerate(chips):
        w = mono_w(label, 16, 0.4) + 30
        g.append(f'<g class="float" style="animation-delay:{-k*1.3:.1f}s"><rect x="{lx-w/2:.1f}" y="{ly-18}" width="{w:.1f}" '
                 f'height="36" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>'
                 + mono(label, lx, ly + 5.5, 16, t["text"], track=0.4, anchor="middle") + '</g>')
    g.append('</g>')
    o += g
    o.append(f'<g class="fade" style="animation-delay:.1s">{star(44, 362, 8, t["violet"])}'
             + mono("DATA & AI DELIVERY LEADER", 62, 368, 16, t["lav"], track=2) + '</g>')
    nw = min(measure(NAME, "serif", 62), 528)
    o.append(f'<text class="serif up" x="36" y="432" font-size="62" fill="{t["text"]}" textLength="{nw:.0f}" '
             f'lengthAdjust="spacingAndGlyphs" style="animation-delay:.15s">{e(NAME)}</text>')
    aw, bw = measure(TAG_A, "serif", 38), measure(TAG_B, "serif", 38, italic=True)
    bx = 36 + aw + 11
    o.append(f'<g class="up" style="animation-delay:.3s"><rect x="{bx-4:.0f}" y="490" width="{bw+10:.0f}" height="11" rx="4" '
             f'fill="url(#gtext)" opacity=".32" class="tb" style="transform-origin:0 50%;animation:grow 1s 1s cubic-bezier(.2,.7,.2,1) both"/>'
             f'<text class="serif" x="36" y="484" font-size="38" fill="{t["text"]}" textLength="{aw:.0f}" lengthAdjust="spacingAndGlyphs">{e(TAG_A)}</text>'
             f'<text class="serif" x="{bx:.0f}" y="484" font-size="38" font-style="italic" fill="url(#gtext)" textLength="{bw:.0f}" '
             f'lengthAdjust="spacingAndGlyphs">{e(TAG_B)}</text></g>')
    for i, line in enumerate(SUB_C):
        o.append(f'<text class="sans up" x="36" y="{532 + i*32}" font-size="25" fill="{t["muted"]}" '
                 f'style="animation-delay:{.45 + i*.08:.2f}s">{e(line)}</text>')
    o.append(f'<g class="up" style="animation-delay:.7s"><rect x="28" y="584" width="544" height="48" rx="14" fill="{t["card"]}" '
             f'fill-opacity=".72" stroke="{t["line"]}"/><text class="mono" x="46" y="615" font-size="21" fill="{t["violet"]}">›</text>')
    typing(defs, o, t, TYPED_C, 72, 615, 21, 586, 44, "tc")
    o.append('</g>')
    items = "  ·  ".join(i.upper() for i in TICKER) + "  ·  "
    L = mono_w(items, 15, 1.6)
    defs.append('<linearGradient id="tkf"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/>'
                '<stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                f'<mask id="tkm"><rect width="{W}" height="{H}" fill="url(#tkf)"/></mask>')
    o.append(f'<line x1="20" y1="648" x2="{W-20}" y2="648" stroke="{t["line"]}"/><g mask="url(#tkm)"><g>'
             + mono(items, 0, 682, 15, t["dim"], track=1.6) + mono(items, L, 682, 15, t["dim"], track=1.6)
             + f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-L:.1f} 0" dur="{L/38:.1f}s" repeatCount="indefinite"/></g></g>')
    return svg(W, H, t, "".join(o), "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}", "".join(defs),
               title=f"{NAME}: Data & AI Delivery Leader. I take AI from POC to P&L.")


def metrics_c(t):
    W, gap, th = 600, 16, 196
    tw = (W - gap) / 2
    H = th * 2 + gap
    o, defs = [], ""
    for i, (final, frames, label, sub) in enumerate(METRICS):
        x, y = (i % 2) * (tw + gap), (i // 2) * (th + gap)
        cx, delay = x + tw / 2, 0.25 + i * 0.18
        defs += f'<clipPath id="mc{i}"><rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="20"/></clipPath>'
        o.append(f'<g class="up" style="animation-delay:{delay-.2:.2f}s"><rect x="{x+.5}" y="{y+.5}" width="{tw-1}" height="{th-1}" '
                 f'rx="20" fill="{t["card"]}" stroke="{t["line"]}"/>'
                 f'<g clip-path="url(#mc{i})"><rect x="{x-120}" y="{y-20}" width="70" height="{th+40}" fill="{t["lav"]}" opacity=".07" '
                 f'transform="skewX(-18)"><animateTransform attributeName="transform" type="translate" values="0 0;{tw+300} 0;{tw+300} 0" '
                 f'keyTimes="0;.35;1" dur="7s" begin="{1.5+i*0.6:.1f}s" repeatCount="indefinite" additive="sum"/></rect></g>')
        n, dur = len(frames) - 1, 1.6
        times = [delay + dur * (1 - (1 - k / n) ** 2) for k in range(n + 1)]
        for k, f in enumerate(frames):
            anim = (f'<set attributeName="visibility" to="visible" begin="{times[k]:.3f}s"/>' if k else "") + \
                   (f'<set attributeName="visibility" to="hidden" begin="{times[k+1]:.3f}s"/>' if k < n else "")
            o.append(f'<text class="sans" x="{cx:.1f}" y="{y+90}" font-size="62" font-weight="700" letter-spacing="-1.5" '
                     f'text-anchor="middle" fill="url(#gtext)" visibility="{"visible" if k == 0 else "hidden"}">{e(f)}{anim}</text>')
        o.append(mono(label, cx, y + 128, 16, t["text"], track=0.8, anchor="middle"))
        o.append(mono(sub, cx, y + 153, 13.5, t["dim"], track=0.8, anchor="middle"))
        o.append(f'<rect x="{x+30}" y="{y+th-26}" width="{tw-60}" height="4" rx="2" fill="{t["line"]}"/>'
                 f'<rect x="{x+30}" y="{y+th-26}" width="{tw-60}" height="4" rx="2" fill="url(#gtext)" class="tb" '
                 f'style="transform-origin:0 50%;animation:grow {dur}s {delay}s cubic-bezier(.2,.7,.2,1) both"/></g>')
    return svg(W, H, t, "".join(o), "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}", defs,
               title="12+ years in AI and data · $5M portfolio owned · ~30% lead conversion lift · 500TB+ cloud data migrated")


def pipeline_c(t):
    W, row, top = 600, 132, 74
    H = top + row * (len(PIPELINE) - 1) + 104
    defs, body = backdrop(W, H, t, uid="p")
    o = [body]
    x, ys = 74, [top + i * row for i in range(len(PIPELINE))]
    travel, cycle, span = 4.8, 6.4, ys[-1] - ys[0]
    defs += (f'<linearGradient id="comet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["violet"]}" stop-opacity="0"/>'
             f'<stop offset=".7" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["peach"]}"/></linearGradient>')
    o.append(f'<line x1="{x}" y1="{ys[0]}" x2="{x}" y2="{ys[-1]}" stroke="{t["line"]}" stroke-width="2.5"/>'
             f'<line x1="{x}" y1="{ys[0]}" x2="{x}" y2="{ys[-1]}" stroke="{t["violet"]}" stroke-opacity=".5" stroke-width="2.5" stroke-dasharray="3 5" class="flow"/>'
             f'<rect x="{x-2.5}" y="{ys[0]-120}" width="5" height="120" rx="2.5" fill="url(#comet)">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {span};0 {span}" keyTimes="0;{travel/cycle:.3f};1" dur="{cycle}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{travel/cycle:.3f};{(travel+.4)/cycle:.3f};1" dur="{cycle}s" repeatCount="indefinite"/></rect>')
    for i, (num, title, cap) in enumerate(PIPELINE):
        y, last = ys[i], i == len(PIPELINE) - 1
        col = t["peach"] if last else t["violet"]
        p = (travel * (y - ys[0]) / span) / cycle
        kts = f"0;{max(p-.02, .0005):.3f};{p:.3f};{min(p+.14, .999):.3f};1"
        o.append(f'<g class="up" style="animation-delay:{.15+i*.12:.2f}s">'
                 f'<circle cx="{x}" cy="{y}" r="36" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.8"/>'
                 f'<circle cx="{x}" cy="{y}" r="36" stroke="{col}" stroke-width="2.6" opacity="{.9 if last else 0}">'
                 + ("" if last else f'<animate attributeName="opacity" values="0;0;1;.15;0" keyTimes="{kts}" dur="{cycle}s" repeatCount="indefinite"/>')
                 + f'</circle><circle cx="{x}" cy="{y}" r="36" fill="{col}" opacity="0"><animate attributeName="opacity" values="0;0;.28;0;0" '
                 f'keyTimes="{kts}" dur="{cycle}s" repeatCount="indefinite"/></circle>'
                 + mono(num, x, y + 6.5, 18, col, anchor="middle")
                 + f'<text class="serif" x="{x+64}" y="{y-8}" font-size="32" fill="{t["text"]}"' + (' font-style="italic"' if last else "")
                 + f'>{e(title)}</text>')
        o.append(f'<text class="sans" x="{x+64}" y="{y+26}" font-size="21" fill="{t["muted"]}">{e(" ".join(cap))}</text></g>'
                 if measure(" ".join(cap), "sans", 21) * 1.18 < W - x - 88 else
                 "".join(f'<text class="sans" x="{x+64}" y="{y+24+j*26}" font-size="21" fill="{t["muted"]}">{e(c)}</text>'
                         for j, c in enumerate(cap)) + '</g>')
    return svg(W, H, t, "".join(o), "", defs, title="How I take AI from POC to P&L: the demo, the data, guardrails, production, P&L")


def programmes_c(t):
    W, gap, pad = 600, 18, 26
    o, y = [], 0
    for i, (tag, title, metric, mlabel, text, stack) in enumerate(PROGRAMMES):
        lines = wrap(text, W - 2 * pad, 23, max_lines=5)
        ch = 176 + len(lines) * 31 + 64
        o.append(f'<g class="up" style="animation-delay:{.1+i*.08:.2f}s"><rect x=".5" y="{y+.5}" width="{W-1}" height="{ch-1}" rx="20" '
                 f'fill="{t["card"]}" stroke="{t["line"]}"/>' + runner(.5, y + .5, W - 1, ch - 1, 20, 9, -i * 1.5, "")
                 + mono(tag, pad, y + 46, 14.5, t["violet"], track=1.2))
        if metric:
            o.append(f'<text class="sans" x="{W-pad}" y="{y+64}" font-size="44" font-weight="700" letter-spacing="-1" text-anchor="end" '
                     f'fill="url(#gtext)">{e(metric)}</text>')
        else:
            sx, sy = W - pad - 26, y + 44
            o.append(f'<path d="M{sx} {sy-26} l22 8 v14 c0 14 -10 22 -22 27 c-12 -5 -22 -13 -22 -27 v-14 z" fill="{t["violet"]}" '
                     f'fill-opacity=".14" stroke="url(#gtext)" stroke-width="2.4" stroke-linejoin="round"/>'
                     f'<path d="M{sx-9} {sy} l6 6 l11 -12" stroke="url(#grun)" stroke-width="2.8" stroke-linecap="round" '
                     f'stroke-linejoin="round" stroke-dasharray="30" stroke-dashoffset="30" style="animation:draw .8s 1.2s ease-out forwards"/>')
        o.append(mono(mlabel, W - pad, y + 92, 13, t["dim"], track=1, anchor="end"))
        o.append(f'<text class="serif" x="{pad}" y="{y+138}" font-size="33" fill="{t["text"]}">{e(title)}</text>')
        for j, ln in enumerate(lines):
            o.append(f'<text class="sans" x="{pad}" y="{y+180+j*31}" font-size="23" fill="{t["muted"]}">{e(ln)}</text>')
        o.append(f'<line x1="{pad}" y1="{y+ch-50}" x2="{W-pad}" y2="{y+ch-50}" stroke="{t["line"]}"/>'
                 + mono(stack, pad, y + ch - 20, 14, t["dim"], track=1) + '</g>')
        y += ch + gap
    return svg(W, y - gap, t, "".join(o), "@keyframes draw{to{stroke-dashoffset:0}}", "", title="Selected programmes")


def toolbox_c(t):
    W, pad, ph = 600, 24, 42
    rows, y, k = [], 30, 0
    o_rows = []
    for label, items, lab in TOOLBOX:
        o_rows.append((label, y, lab))
        y += 18
        x = pad
        for it in items:
            w = mono_w(it, 18, 0.2) + 32
            if x + w > W - pad:
                x, y = pad, y + ph + 10
            rows.append((it, x, y, w, lab))
            x += w + 10
        y += ph + 34
    H = y - 6
    defs, body = backdrop(W, H, t, uid="tb", blobs=False)
    o = [body]
    for i, (label, ly, lab) in enumerate(o_rows):
        if i:
            o.append(f'<line x1="{pad}" y1="{ly-22}" x2="{W-pad}" y2="{ly-22}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
        o.append(mono(label, pad, ly, 14, t["peach"] if lab else t["lav"], track=1.4))
    cyc = len(rows) * 0.35
    for k, (it, x, py, w, lab) in enumerate(rows):
        dash = ' stroke-dasharray="4 4"' if lab else ""
        o.append(f'<g class="up" style="animation-delay:{.05+k*.025:.3f}s"><rect x="{x}" y="{py}" width="{w:.1f}" height="{ph}" rx="21" '
                 f'fill="{t["card"]}" stroke="{t["line"]}"{dash}/><rect x="{x}" y="{py}" width="{w:.1f}" height="{ph}" rx="21" '
                 f'stroke="url(#grun)" stroke-width="1.8" opacity="0" style="animation:hi {cyc:.1f}s {k*.35:.2f}s infinite"/>'
                 + mono(it, x + w / 2, py + 27.5, 18, t["muted"] if lab else t["text"], track=0.2, anchor="middle") + '</g>')
    hi = 100 * 2.2 / cyc
    return svg(W, H, t, "".join(o), f"@keyframes hi{{0%{{opacity:0}}{hi/2:.2f}%{{opacity:1}}{hi:.2f}%{{opacity:0}}100%{{opacity:0}}}}",
               defs, title="Toolbox")


def credentials_c(t):
    W, gap = 600, 14
    tw, th, eh = (W - gap) / 2, 172, 108
    o = []

    def seal(cx, cy, col, glyph, i, r=25):
        s = (f'<g><circle cx="{cx}" cy="{cy}" r="{r+7}" stroke="{col}" stroke-opacity=".55" stroke-dasharray="2 4"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{24+i*3}s" repeatCount="indefinite"/></g>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="1.8"/>')
        if glyph == "check":
            return s + (f'<path d="M{cx-9} {cy+1} l6 6 l12 -13" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" '
                        f'stroke-dasharray="34" stroke-dashoffset="34" style="animation:draw .7s {.6+i*.15:.2f}s ease-out forwards"/>')
        return s + (f'<path d="M{cx-15} {cy-3} L{cx} {cy-11} L{cx+15} {cy-3} L{cx} {cy+5} Z" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>'
                    f'<path d="M{cx-8} {cy+1} v7 c0 4 16 4 16 0 v-7" stroke="{col}" stroke-width="2"/>')

    for i, (lines, issuer) in enumerate(CERTS):
        x, y = (i % 2) * (tw + gap), (i // 2) * (th + gap)
        fs = min(22, 22 * (tw - 44) / max(measure(ln, "sans", 22, bold=True) * 1.2 for ln in lines))
        o.append(f'<g class="up" style="animation-delay:{.1+i*.1:.2f}s"><rect x="{x+.5}" y="{y+.5}" width="{tw-1}" height="{th-1}" rx="18" '
                 f'fill="{t["card"]}" stroke="{t["line"]}"/>' + seal(x + 54, y + 50, t["violet"], "check", i)
                 + "".join(f'<text class="sans" x="{x+22}" y="{y+108+j*27}" font-size="{fs:.1f}" font-weight="600" fill="{t["text"]}">{e(ln)}</text>'
                           for j, ln in enumerate(lines))
                 + mono(issuer, x + 22, y + th - 14, 12.5, t["dim"], track=0.6) + '</g>')
    y0 = 2 * th + gap + 18
    for i, (title, issuer) in enumerate(EDUCATION):
        y = y0 + i * (eh + gap)
        fs = min(22, 22 * (W - 130) / (measure(title, "sans", 22, bold=True) * 1.2))
        o.append(f'<g class="up" style="animation-delay:{.5+i*.1:.2f}s"><rect x=".5" y="{y+.5}" width="{W-1}" height="{eh-1}" rx="18" '
                 f'fill="{t["card"]}" stroke="{t["line"]}"/>' + seal(56, y + eh / 2, t["peach"], "cap", i + 4)
                 + f'<text class="sans" x="108" y="{y+48}" font-size="{fs:.1f}" font-weight="600" fill="{t["text"]}">{e(title)}</text>'
                 + mono(issuer, 108, y + 78, 13, t["dim"], track=0.6) + '</g>')
    H = y0 + 3 * eh + 2 * gap
    return svg(W, H, t, "".join(o), "@keyframes draw{to{stroke-dashoffset:0}}", "",
               title="Certifications and education")


def cta_c(t):
    W, H = 600, 520
    defs, body = backdrop(W, H, t, uid="c")
    o = [body, f'<g class="fade">{star(44, 56, 7, t["violet"])}' + mono("START A CONVERSATION", 60, 62, 15, t["lav"], track=2) + '</g>']
    for k, (txt, y, ital) in enumerate([("Have an AI programme", 128, False), ("in mind?", 180, False), ("Let's talk.", 236, True)]):
        w = measure(txt, "serif", 46, italic=ital)
        o.append(f'<text class="serif up" x="36" y="{y}" font-size="46" fill="{"url(#gtext)" if ital else t["text"]}"'
                 + (' font-style="italic"' if ital else "") + f' textLength="{w:.0f}" lengthAdjust="spacingAndGlyphs" '
                 f'style="animation-delay:{.1+k*.08:.2f}s">{e(txt)}</text>')
    for k, line in enumerate(["AI transformation · GenAI & agentic", "delivery · AI governance · advisory.",
                              "I reply within 24 hours."]):
        o.append(f'<text class="sans up" x="36" y="{290 + k*33}" font-size="23" fill="{t["muted"]}" '
                 f'style="animation-delay:{.3+k*.05:.2f}s">{e(line)}</text>')
    defs += (f'<linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["deep"]}"/></linearGradient>'
             f'<filter id="bglow" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="16"/></filter>')
    bx, by, bw, bh = 36, 388, 528, 72
    o.append(f'<g class="up" style="animation-delay:.45s"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="36" fill="{t["violet"]}" '
             f'filter="url(#bglow)" class="tb" style="animation:glow 2.8s ease-in-out infinite"/>'
             f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="36" fill="url(#bg)"/>'
             f'<text class="sans" x="{bx+bw/2-18}" y="{by+45}" font-size="27" font-weight="600" fill="#fff" text-anchor="middle">Ask my AI anything</text>'
             f'<g class="nudge"><path d="M{bx+bw-92} {by+36} h22 m-8 -8 l8 8 l-8 8" stroke="#fff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></g>'
             + mono("mukherjeesuman.com", W / 2, by + bh + 38, 16, t["dim"], track=1, anchor="middle") + '</g>')
    return svg(W, H, t, "".join(o), "@keyframes glow{0%,100%{opacity:.35;transform:scale(.97)}50%{opacity:.75;transform:scale(1.03)}}"
               ".nudge{animation:nudge 1.8s ease-in-out infinite}@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}",
               defs, title="Have an AI programme in mind? Let's talk.")


def project_c(t, key, top, title, tags, badge, H_fixed=None):
    W, pad = 480, 30
    short = PROJECT_SHORT[key]
    top = top.split("/")[-1]
    tl = wrap(title, W - 2 * pad, 46, kind="serif", max_lines=2, slack=1.1)
    bl = wrap(short, W - 2 * pad, 36, max_lines=3)
    y_title = 132
    y_body = y_title + (len(tl) - 1) * 52 + 64
    y_tags = y_body + (len(bl) - 1) * 46 + 40
    pills, x, ty = [], pad, y_tags
    for tag in tags:
        w = mono_w(tag, 24, 0.2) + 36
        if x + w > W - pad:
            x, ty = pad, ty + 58
        pills.append((tag, x, ty, w))
        x += w + 12
    H = ty + 48 + 34
    if H_fixed:  # equal heights so cards line up side by side; tags sit at the bottom
        shift = H_fixed - H
        pills = [(tg, px, py + shift, pw) for tg, px, py, pw in pills]
        H = H_fixed
    o = [f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="26" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>']
    defs = (f'<radialGradient id="cg"><stop offset="0" stop-color="{t["violet"]}" stop-opacity=".35"/><stop offset="1" stop-color="{t["violet"]}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="26"/></clipPath>')
    o.append(f'<g clip-path="url(#cc)"><circle cx="{W-50}" cy="20" r="170" fill="url(#cg)" class="tb" style="animation:breathe 6s ease-in-out infinite"/></g>')
    o.append(runner(.75, .75, W - 1.5, H - 1.5, 26, 8, 0, ""))
    o.append(mono(top, pad, 58, 21, t["dim"], track=0.2))
    if badge:
        live = badge == "LIVE"
        bw = mono_w(badge, 18, 1) + (52 if live else 32)
        o.append(f'<rect x="{W-pad-bw:.1f}" y="34" width="{bw:.1f}" height="36" rx="18" fill="{t["card2"]}" stroke="{t["line"]}"/>')
        if live:
            o.append(f'<circle cx="{W-pad-bw+21:.1f}" cy="52" r="5.5" fill="{t["green"]}"/><circle cx="{W-pad-bw+21:.1f}" cy="52" r="5.5" fill="{t["green"]}" class="tb ping"/>'
                     + mono(badge, W - pad - bw + 36, 58.5, 18, t["text"], track=1))
        else:
            o.append(mono(badge, W - pad - bw / 2, 58.5, 18, t["text"], track=1, anchor="middle"))
    for j, ln in enumerate(tl):
        o.append(f'<text class="serif" x="{pad}" y="{y_title + j*52}" font-size="46" fill="{t["text"]}">{e(ln)}</text>')
    for j, ln in enumerate(bl):
        o.append(f'<text class="sans" x="{pad}" y="{y_body + j*46}" font-size="36" fill="{t["muted"]}">{e(ln)}</text>')
    for tag, x, ty, w in pills:
        o.append(f'<rect x="{x}" y="{ty}" width="{w:.1f}" height="48" rx="24" fill="{t["card2"]}" stroke="{t["line"]}"/>'
                 + mono(tag, x + w / 2, ty + 32, 24, t["lav"], track=0.2, anchor="middle"))
    return svg(W, H, t, "".join(o), "@keyframes breathe{0%,100%{transform:scale(1);opacity:.8}50%{transform:scale(1.15);opacity:1}}",
               defs, title=title)


# --------------------------------------------------------------------------- #
def main():
    for name, t in THEMES.items():
        out = ASSETS / name
        out.mkdir(parents=True, exist_ok=True)
        files = {
            "hero.svg": hero(t), "metrics.svg": metrics(t), "pipeline.svg": pipeline(t),
            "programmes.svg": programmes(t), "toolbox.svg": toolbox(t),
            "credentials.svg": credentials(t), "cta.svg": cta(t), "footer.svg": footer(t),
        }
        for key, top, title, text, tags, badge in PROJECTS:
            files[f"project-{key}.svg"] = project(t, top, title, text, tags, badge)
        for i, (key, label, sub) in enumerate(BUTTONS):
            files[f"{key}.svg"] = button(t, label, sub, primary=(i == 0))
        for fname, content in files.items():
            (out / fname).write_text(content, encoding="utf-8")
        print(f"{name}: {len(files)} files")
    t = THEMES["dark"]
    out = ASSETS / "compact"
    out.mkdir(parents=True, exist_ok=True)
    files = {"hero.svg": hero_c(t), "metrics.svg": metrics_c(t), "pipeline.svg": pipeline_c(t),
             "programmes.svg": programmes_c(t), "toolbox.svg": toolbox_c(t),
             "credentials.svg": credentials_c(t), "cta.svg": cta_c(t)}
    import re as _re
    hmax = max(int(_re.search(r'height="(\d+)"', project_c(t, k, tp, ti, tg, b)).group(1))
               for k, tp, ti, _, tg, b in PROJECTS)
    for key, top, title, text, tags, badge in PROJECTS:
        files[f"project-{key}.svg"] = project_c(t, key, top, title, tags, badge, H_fixed=hmax)
    for fname, content in files.items():
        (out / fname).write_text(content, encoding="utf-8")
    print(f"compact: {len(files)} files")


if __name__ == "__main__":
    main()
