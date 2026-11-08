"""Build the teaching-style slides: one HTML + PDF per module, plus the full course PDF.

    python slides/src/build_course.py            # every module in slides/src/modules/
    python slides/src/build_course.py 10 11      # only these modules (fast while editing)
    python slides/src/build_course.py --html     # HTML only, no PDF rendering

Each module file slides/src/modules/mNN.py defines SLIDES (a list of teach_kit layouts).
Code on "TRY IT" slides is executed while building, so the OUTPUT boxes are always real.
"""
import importlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent                                  # slides/
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "modules"))
from teach_kit import build  # noqa: E402

RENDER = Path.home() / ".claude" / "slides-template" / "render.ps1"
HTML_DIR, PDF_DIR = HERE / "html", ROOT / "modules"


def render(html: Path, pdf: Path) -> None:
    subprocess.run(["powershell", "-File", str(RENDER), "-Html", str(html), "-Out", str(pdf)],
                   check=True, capture_output=True)


def check_overflow(pdf: Path) -> list[str]:
    """Text below the content area (y > 950 of 1080) or past the right margin means it doesn't fit."""
    import pymupdf
    problems = []
    for n, page in enumerate(pymupdf.open(pdf), 1):
        scale = 1080 / page.rect.height
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                x0, y0, x1, y1 = (v * scale for v in line["bbox"])
                if not text or "Python Pro ·" in text or text.startswith("github.com/CodeMitVishal"):
                    continue
                if y1 > 952 or x1 > 1800:
                    problems.append(f"{pdf.name} slide {n}: '{text[:50]}' ends at y={y1:.0f} x={x1:.0f}")
    return problems


def main(args: list[str]) -> None:
    html_only = "--html" in args
    wanted = [a.zfill(2) for a in args if a.isdigit()]
    files = sorted((HERE / "modules").glob("m[0-9][0-9].py"))
    HTML_DIR.mkdir(exist_ok=True)
    PDF_DIR.mkdir(exist_ok=True)
    problems = []
    for f in files:
        num = f.stem[1:]
        if wanted and num not in wanted:
            continue
        slides = importlib.import_module(f.stem).SLIDES
        html = HTML_DIR / f"module-{num}.html"
        build(slides, html)
        if not html_only:
            pdf = PDF_DIR / f"Module-{num}.pdf"
            render(html, pdf)
            problems += check_overflow(pdf)
    if not html_only and not wanted:                # full course = all module PDFs in order
        import pymupdf
        course = pymupdf.open()
        for pdf in sorted(PDF_DIR.glob("Module-*.pdf")):
            course.insert_pdf(pymupdf.open(pdf))
        course.save(ROOT / "python-pro-slides.pdf", garbage=3, deflate=True)
        print(f"course PDF: {len(course)} slides")
    print("\n".join(problems) or "no overflow found")


if __name__ == "__main__":
    main(sys.argv[1:])
