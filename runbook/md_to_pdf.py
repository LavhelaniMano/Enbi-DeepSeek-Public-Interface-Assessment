#!/usr/bin/env python
"""Render FINAL_REPORT.md to a Word-looking PDF.

Pipeline: Markdown -> styled HTML (Calibri/Cambria, blue headings, banded tables)
-> PDF via headless Microsoft Edge (print-to-PDF).

Usage (from the runbook directory):
    .\\.venv\\Scripts\\python.exe runbook\\md_to_pdf.py
The PDF is written next to the Markdown source. PDFs are gitignored repo-wide,
so the output stays local, per project policy.
"""
import pathlib
import subprocess
import sys

import markdown

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "FINAL_REPORT.md"
OUT = HERE.parent / "FINAL_REPORT.pdf"
TMP_HTML = HERE.parent / ".FINAL_REPORT_build.html"

EDGE_CANDIDATES = [
    pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    pathlib.Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
]

CSS = """
@page { size: A4; margin: 2.2cm 2cm 2.2cm 2cm; }
html, body { margin: 0; padding: 0; }
body {
  font-family: Calibri, "Segoe UI", sans-serif;
  font-size: 11pt; line-height: 1.4; color: #1a1a1a;
}
h1 {
  font-family: Calibri Light, Calibri, sans-serif;
  font-size: 23pt; font-weight: 600; color: #2F5496;
  text-align: center; margin: 0 0 6pt 0;
}
/* metadata block right under the title */
h1 + p {
  text-align: center; color: #595959; font-size: 10.5pt;
  margin: 0 0 16pt 0; padding-bottom: 10pt;
  border-bottom: 1.5pt solid #2F5496;
}
h2 {
  font-family: Calibri Light, Calibri, sans-serif;
  font-size: 15pt; font-weight: 600; color: #2F5496;
  margin: 16pt 0 6pt 0; page-break-after: avoid;
  border-bottom: 0.5pt solid #B4C6E7; padding-bottom: 2pt;
}
h3 {
  font-family: Calibri Light, Calibri, sans-serif;
  font-size: 12.5pt; font-weight: 600; color: #2F5496;
  margin: 12pt 0 4pt 0; page-break-after: avoid;
}
p { margin: 0 0 8pt 0; }
ul, ol { margin: 0 0 8pt 0; padding-left: 24pt; }
li { margin-bottom: 4pt; }
strong { color: #1F3864; }
a { color: #0563C1; text-decoration: none; }
table {
  border-collapse: collapse; width: 100%; font-size: 9.5pt;
  margin: 6pt 0 12pt 0; page-break-inside: auto;
}
th {
  background: #2F5496; color: #ffffff; font-weight: bold;
  text-align: left; padding: 4pt 6pt;
  border: 0.5pt solid #2F5496;
}
td {
  padding: 4pt 6pt; vertical-align: top;
  border: 0.5pt solid #B4C6E7;
}
tbody tr:nth-child(even) td { background: #EDF2F8; }
tr { page-break-inside: avoid; }
img {
  max-width: 100%; height: auto; display: block;
  border: 0.75pt solid #D0D0D0; margin: 4pt auto 12pt auto;
}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Final Project Report: Public-Interface Observations of Enbi</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>"""


def main() -> int:
    if not SRC.exists():
        print(f"missing source: {SRC}")
        return 1
    edge = next((p for p in EDGE_CANDIDATES if p.exists()), None)
    if edge is None:
        print("Edge not found; cannot print to PDF")
        return 1

    text = SRC.read_text(encoding="utf-8")
    # python-markdown does not turn two-space line endings into <br>; do it here
    # so the report's metadata block under the title keeps its line structure.
    text = text.replace("  \n", "  <br>\n")
    body = markdown.markdown(text, extensions=["tables"])
    TMP_HTML.write_text(TEMPLATE.format(css=CSS, body=body), encoding="utf-8")

    cmd = [
        str(edge), "--headless=new", "--disable-gpu",
        "--no-pdf-header-footer",
        "--user-data-dir=" + str(pathlib.Path.home() / "AppData/Local/Temp/edge-pdf-profile"),
        f"--print-to-pdf={OUT}",
        TMP_HTML.resolve().as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not OUT.exists() or OUT.stat().st_size == 0:
        cmd[1] = "--headless"  # older Edge fallback
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    TMP_HTML.unlink(missing_ok=True)

    if not OUT.exists() or OUT.stat().st_size == 0:
        print("PDF not produced; Edge said:", (r.stderr or r.stdout)[:600])
        return 1
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(str(OUT)).pages)
    except Exception:
        pages = "?"
    print(f"wrote {OUT.name}: {OUT.stat().st_size/1024:.0f} KB, {pages} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
