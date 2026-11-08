"""Teaching-first slide layouts (v2): one idea per slide, problem -> picture -> code + output
-> common mistake -> real job -> interview answer -> recap.

Usage:
    from teach_kit import *            # layouts + build()
    build([cover(...), why(...), ...], "slides/src/module10.html")
"""
import html
import re
from pathlib import Path

REPO = "github.com/CodeMitVishal/python-pro"
HERE = Path(__file__).parent
KW = ("def|class|return|for|in|if|elif|else|with|as|import|from|async|await|yield|try|except|"
      "finally|raise|lambda|None|True|False|not|and|or|is|while|nonlocal|global|pass|del")
TOKENS = re.compile(rf"""(?P<s>f?"[^"\n]*"|f?'[^'\n]*')|(?P<c>\#[^\n]*)|(?P<d>@[\w.]+)|(?P<k>\b(?:{KW})\b)|(?P<o>.|\n)""")


def hl(code: str) -> str:
    out = []
    for m in TOKENS.finditer(code.strip("\n")):
        text = html.escape(m.group())
        out.append(text if m.lastgroup == "o" else f'<span class="{m.lastgroup}">{text}</span>')
    return "".join(out)


def fit(src: str, box: int, size: int, max_h: int = 640) -> int:
    """Largest font (<= size) so the code fits the box width AND the slide height."""
    lines = src.strip(chr(10)).splitlines() or [""]
    by_width = (box - 70) / (max(len(line) for line in lines) * 0.61)
    by_height = (max_h - 56) / (len(lines) * 1.5)
    return max(17, min(size, int(by_width), int(by_height)))


def foot(label):
    return f'<p class="foot-l">Python Pro · {label}</p><p class="foot-r">{REPO}</p>'


def head(eyebrow, h2, kind=""):
    badge = f'<span class="kind {kind}">{KINDS[kind]}</span>' if kind else ""
    return f'<div><p class="eyebrow">{badge}{eyebrow}</p><h2>{h2}</h2></div>'


KINDS = {"why": "WHY", "pic": "PICTURE IT", "code": "TRY IT", "trace": "STEP BY STEP", "bad": "COMMON MISTAKE",
         "job": "IN REAL JOBS", "iq": "INTERVIEW", "recap": "RECAP"}


# --------------------------------------------------------------------------- layouts
def cover(num, name, tagline, toc, mod):
    rows = "".join(f"<div><span>{a}</span><span>{b}</span></div>" for a, b in toc)
    return f"""<section class="dark" style="flex-direction:row;align-items:center;gap:100px">
  <div style="width:680px;display:flex;flex-direction:column;gap:20px">
    <p class="num">MODULE</p><p class="big">{num}</p><h1>{name}</h1>
    <p style="font-size:32px;line-height:1.4">{tagline}</p></div>
  <div style="flex:1" class="toc"><p class="num" style="font-size:22px;margin-bottom:10px">YOU WILL LEARN</p>{rows}</div>
  {foot(mod)}</section>"""


def why(mod, eyebrow, h2, problem, idea, example=None):
    ex = f'<div class="code" style="font-size:{fit(example, 760, 28)}px">{hl(example)}</div>' if example else ""
    return f"""<section>{head(eyebrow, h2, "why")}
  <div class="row">
    <div class="col" style="flex:1"><p class="label">THE PROBLEM</p><p class="body">{problem}</p>{ex}</div>
    <div class="idea"><p class="label" style="color:#121826">THE IDEA</p><p>{idea}</p></div>
  </div>{foot(mod)}</section>"""


def picture(mod, eyebrow, h2, analogy, flow, caption=""):
    boxes = []
    for i, (title, sub) in enumerate(flow):
        if i:
            boxes.append('<div class="arrow">&#8594;</div>')
        boxes.append(f'<div class="box"><p class="bt">{title}</p><p class="bs">{sub}</p></div>')
    cap = f'<p class="body" style="text-align:center">{caption}</p>' if caption else ""
    return f"""<section>{head(eyebrow, h2, "pic")}
  <div class="analogy">{analogy}</div>
  <div class="flow">{"".join(boxes)}</div>{cap}
  {foot(mod)}</section>"""


def run_snippet(code: str, setup: str = "", after: str = "") -> str:
    """Run the slide's code and return what it prints, so the OUTPUT box is never wrong."""
    import os
    import subprocess
    import sys
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "snippet.py"
        script.write_text(setup + "\n" + code.strip("\n") + "\n" + after + "\n", encoding="utf-8")
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONHASHSEED": "0"}
        r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=tmp,
                           timeout=60, env=env, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"slide snippet failed:\n{code}\n---\n{r.stderr[-800:]}")
    return r.stdout


def code_out(mod, eyebrow, h2, code, output=None, steps=(), code_w=None, setup="", after=""):
    if output is None:
        output = run_snippet(code, setup, after)
    output = output.strip(chr(10))
    longest = max(len(line) for line in code.strip(chr(10)).splitlines())
    if code_w is None:                                  # as wide as the code needs at 26px
        code_w = max(700, min(1060, int(longest * 0.61 * 26 + 80)))
    right_w = 1664 - 48 - code_w
    out_size = max(22, min(26, int((right_w - 64) / (max(len(x) for x in output.splitlines() or [""]) * 0.61 + 1))))
    st = "".join(f'<div class="step"><span>{i}</span><p>{s}</p></div>' for i, s in enumerate(steps, 1))
    return f"""<section>{head(eyebrow, h2, "code")}
  <div class="row">
    <div class="code" style="width:{code_w}px;font-size:{fit(code, code_w, 28)}px">{hl(code)}</div>
    <div class="col" style="width:{right_w}px"><div class="term" style="font-size:{out_size}px"><p class="tl">OUTPUT</p>{html.escape(output)}</div>
      {f'<div class="steps">{st}</div>' if st else ""}</div>
  </div>{foot(mod)}</section>"""


def trace(mod, eyebrow, h2, head_row, rows, note=""):
    th = "".join(f"<th>{h}</th>" for h in head_row)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    n = f'<p class="tipbar">{note}</p>' if note else ""
    return f"""<section>{head(eyebrow, h2, "trace")}
  <table class="tbig">{"<tr>" + th + "</tr>"}{trs}</table>{n}
  {foot(mod)}</section>"""


def mistake(mod, eyebrow, h2, bad, bad_note, good, good_note):
    w = 780
    return f"""<section>{head(eyebrow, h2, "bad")}
  <div class="row">
    <div class="col" style="flex:1"><p class="pill-bad">&#10007; WRONG</p>
      <div class="code" style="font-size:{fit(bad, w, 27)}px">{hl(bad)}</div><p class="body">{bad_note}</p></div>
    <div class="col" style="flex:1"><p class="pill-good">&#10003; RIGHT</p>
      <div class="code" style="font-size:{fit(good, w, 27)}px">{hl(good)}</div><p class="body">{good_note}</p></div>
  </div>{foot(mod)}</section>"""


def job(mod, eyebrow, h2, items):
    cs = "".join(f'<div class="card"><h3>{t}</h3><div class="code" style="font-size:{fit(c, 760, 25)}px;padding:16px 22px">'
                 f'{hl(c)}</div></div>' for t, c in items)
    return f"""<section>{head(eyebrow, h2, "job")}
  <div class="grid">{cs}</div>{foot(mod)}</section>"""


def interview(mod, question, answer, code=None, follow=None):
    pts = "".join(f"<li>{a}</li>" for a in answer)
    right = f'<div class="code" style="width:760px;font-size:{fit(code, 760, 26)}px">{hl(code)}</div>' if code else ""
    fu = f'<p class="tipbar"><b>Follow-up they ask next:</b> {follow}</p>' if follow else ""
    return f"""<section>{head("Say this in the interview", "&#8220;" + question + "&#8221;", "iq")}
  <div class="row"><ul class="answer" style="flex:1">{pts}</ul>{right}</div>{fu}
  {foot(mod)}</section>"""


def recap(mod, h2, points, practice):
    pts = "".join(f'<div class="step"><span>{i}</span><p>{p}</p></div>' for i, p in enumerate(points, 1))
    return f"""<section>{head("Remember these", h2, "recap")}
  <div class="row"><div class="steps" style="flex:1">{pts}</div>
  <div class="idea" style="width:620px"><p class="label" style="color:#121826">PRACTICE NOW</p><p style="font-size:30px;overflow-wrap:anywhere">{practice}</p></div></div>
  {foot(mod)}</section>"""


EXTRA_CSS = """
.kind { display:inline-block; font-size:20px; letter-spacing:2px; padding:4px 14px; border-radius:999px;
  background:#121826; color:#F2C14E; margin-right:16px; vertical-align:2px; }
.kind.bad { background:#C2413B; color:#fff; } .kind.iq { background:#2F5E9E; color:#fff; }
.kind.job { background:#2E7D5B; color:#fff; } .kind.recap { background:#F2C14E; color:#121826; }
.label { font-size:22px; font-weight:700; letter-spacing:3px; color:#2F5E9E; }
.body { font-size:34px; line-height:1.45; color:#3F4859; } .body b { color:#121826; }
.idea { width:760px; background:#F2C14E; border-radius:24px; padding:40px 44px; display:flex; flex-direction:column; gap:18px; }
.idea p:last-child { font-size:40px; line-height:1.3; font-weight:700; color:#121826; }
.analogy { background:#FFFDF8; border:1px solid #E3DFD3; border-radius:22px; padding:26px 36px; font-size:34px; line-height:1.45; }
.analogy b { color:#121826; }
.flow { display:flex; align-items:stretch; gap:18px; }
.box { flex:1; background:#1C2436; border-radius:20px; padding:26px 26px; display:flex; flex-direction:column; gap:10px; }
.bt { font-size:30px; font-weight:700; color:#F2C14E; font-family:'Roboto Mono', monospace; }
.bs { font-size:26px; line-height:1.4; color:#E6E9F0; }
.arrow { align-self:center; font-size:56px; color:#2F5E9E; font-weight:700; }
.term { background:#0D1117; border-radius:20px; padding:22px 30px 26px; font-family:'Roboto Mono', monospace;
  line-height:1.5; color:#7EE2A8; white-space:pre-wrap; overflow-wrap:anywhere; }
.tl { font-family:'Space Grotesk', Arial, sans-serif; font-size:18px; letter-spacing:3px; color:#8A93A6; margin-bottom:8px; }
.steps { display:flex; flex-direction:column; gap:16px; }
.step { display:flex; gap:18px; align-items:flex-start; font-size:28px; line-height:1.35; }
.step span { flex:none; width:46px; height:46px; border-radius:50%; background:#2F5E9E; color:#fff; font-weight:700;
  display:flex; align-items:center; justify-content:center; font-size:24px; }
.step b { color:#121826; }
.pill-bad, .pill-good { align-self:flex-start; font-size:24px; font-weight:700; letter-spacing:2px; padding:6px 18px; border-radius:999px; color:#fff; }
.pill-bad { background:#C2413B; } .pill-good { background:#2E7D5B; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
.answer { font-size:33px; line-height:1.45; padding-left:36px; display:flex; flex-direction:column; gap:14px; }
.answer b { color:#121826; }
.tipbar { background:#E8EEF7; border-left:6px solid #2F5E9E; border-radius:12px; padding:18px 26px; font-size:28px; line-height:1.4; }
table.tbig { font-size:30px; color:#3F4859; } table.tbig td { padding:14px 16px; } table.tbig td:first-child { font-family:"Roboto Mono", monospace; color:#121826; }
.d { color:#C9A0FF; }
section.dark h1 { font-size:84px; }
"""


def build(slides, out_html):
    deck = (HERE / "python-pro-slides.html").read_text(encoding="utf-8")
    head_html = deck[:deck.index("</style>")] + EXTRA_CSS + "</style></head><body>\n"
    Path(out_html).write_text(head_html + "\n\n".join(slides) + "\n</body></html>", encoding="utf-8")
    print(f"{len(slides)} slides -> {out_html}")


# Hidden code that runs the slide's test functions with pytest and prints a clean summary.
PYTEST = r"""
if __name__ == "__main__":
    import contextlib, io, re, pytest
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pytest.main(["-v", "-p", "no:cacheprovider", "-p", "no:warnings", "--no-header", "-rN", "--tb=line", __file__])
    for line in buf.getvalue().splitlines():
        line = re.sub(r"^.*::", "", line)
        line = re.sub(r" *\[ *[0-9]+%\]$", "", line)
        line = re.sub(r" in [0-9.]+s", "", line).strip(" =")
        if line and not line.startswith(("collect", "test session")):
            print(line)
"""
