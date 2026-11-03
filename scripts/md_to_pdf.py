#!/usr/bin/env python
"""Render FINAL_REPORT.md as a LaTeX-typeset PDF.

Pipeline: Markdown -> LaTeX (article class, Latin Modern, booktabs tables,
hyperref links) -> PDF via pdflatex. The output deliberately reads as a
typeset document rather than a Word export: Computer Modern/Latin Modern
serif, justified text, indented paragraphs, rule-based tables and
numbered-free section headings and flush-left, consistently spaced paragraphs.

Usage (from the repository root):
    python scripts\\md_to_pdf.py
Requires a TeX distribution on PATH (pdflatex) with the packages listed in
PREAMBLE. The PDF is written next to the Markdown source, replacing the
existing file. Intermediate files are written to a temporary directory and
removed on success.
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
DOCS = REPO / "docs"
SRC = DOCS / "FINAL_REPORT.md"
OUT = DOCS / "FINAL_REPORT.pdf"

PREAMBLE = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[english]{babel}
\usepackage{microtype}
\usepackage[a4paper,top=2.4cm,bottom=2.4cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}
\urlstyle{same}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\setlength{\emergencystretch}{3em}
\titleformat{\section}{\normalfont\Large\bfseries}{}{0pt}{}
\titlespacing*{\section}{0pt}{15pt plus 2pt minus 2pt}{6pt}
\titleformat{\subsection}{\normalfont\large\bfseries}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{12pt plus 2pt minus 2pt}{4pt}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries}{}{0pt}{}
\titlespacing*{\subsubsection}{0pt}{9pt plus 1pt minus 1pt}{3pt}
\pagestyle{plain}
"""

LIST_OPTIONS = "leftmargin=1.5em,itemsep=3pt,topsep=3pt,parsep=0pt"
TABLE_TOTAL_WIDTH = 0.90  # share of \textwidth used by table columns

ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape(text: str) -> str:
    return "".join(ESCAPES.get(ch, ch) for ch in text)


def inline(text: str, stash: list[str] | None = None) -> str:
    """Convert inline Markdown to LaTeX, protecting generated commands."""
    if stash is None:
        stash = []

    def hold(latex: str) -> str:
        stash.append(latex)
        return f"\x00{len(stash) - 1}\x00"

    text = re.sub(
        r"`([^`]+)`",
        lambda m: hold(r"\texttt{" + escape(m.group(1)) + "}"),
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: hold(
            r"\href{" + m.group(2) + "}{" + inline(m.group(1), stash) + "}"
        ),
        text,
    )
    text = re.sub(
        r"<((?:https?|mailto):[^>\s]+)>",
        lambda m: hold(r"\url{" + m.group(1) + "}"),
        text,
    )

    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"\\emph{\1}", text)

    def restore(match: re.Match[str]) -> str:
        return stash[int(match.group(1))]

    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", restore, text)
    return text


def is_table_row(line: str) -> bool:
    return line.lstrip().startswith("|")


def is_separator_row(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells)


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [c.strip() for c in stripped.split("|")]


def render_table(rows: list[str]) -> str:
    parsed = [split_row(r) for r in rows if not is_separator_row(r)]
    if not parsed:
        return ""
    width = max(len(r) for r in parsed)
    parsed = [r + [""] * (width - len(r)) for r in parsed]

    longest = [max(len(row[i]) for row in parsed) for i in range(width)]
    weights = [max(n, 8) for n in longest]
    shares = [max(TABLE_TOTAL_WIDTH * w / sum(weights), 0.075) for w in weights]
    scale = TABLE_TOTAL_WIDTH / sum(shares)
    shares = [s * scale for s in shares]

    spec = "".join(f"p{{{s:.3f}\\textwidth}}" for s in shares)
    header, body = parsed[0], parsed[1:]
    lines = [
        r"\begingroup\small",
        rf"\begin{{longtable}}{{@{{}}{spec}@{{}}}}",
        r"\toprule",
        " & ".join(rf"\textbf{{{inline(c)}}}" for c in header) + r" \\",
        r"\midrule",
        r"\endhead",
    ]
    for row in body:
        lines.append(" & ".join(inline(c) for c in row) + r" \\")
    lines += [r"\bottomrule", r"\end{longtable}", r"\endgroup"]
    return "\n".join(lines)


def render_paragraph(lines: list[str], centred: bool = False) -> str:
    # Join wrapped lines before inline conversion so bold/italic spans that
    # cross a line boundary are still recognised. Markdown hard breaks (two
    # trailing spaces) become LaTeX line breaks between segments.
    segments: list[str] = []
    current: list[str] = []
    for raw in lines:
        current.append(raw.strip())
        if raw.endswith("  "):
            segments.append(" ".join(current).strip())
            current = []
    if current:
        segments.append(" ".join(current).strip())
    body = r" \\".join(inline(segment) for segment in segments)
    if centred:
        return "\\begin{center}\\small\n" + body + "\n\\end{center}"
    if len(lines) == 1 and re.fullmatch(r"\*\*[^*]+\*\*", lines[0].strip()):
        return "\\noindent " + body
    return body


def build_tex(markdown_text: str) -> str:
    lines = markdown_text.replace("\r\n", "\n").split("\n")
    out: list[str] = [PREAMBLE, r"\begin{document}", r"\vspace*{0.4cm}"]
    title_done = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            text = inline(heading.group(2).strip())
            if level == 1 and not title_done:
                out.append(
                    "\\begin{center}\n{\\LARGE\\bfseries " + text + "\\par}\n\\end{center}"
                )
                out.append(r"\vspace{4pt}")
                title_done = True
            elif level == 1:
                out.append(r"\section*{" + text + "}")
            elif level == 2:
                out.append(r"\section*{" + text + "}")
            elif level == 3:
                out.append(r"\subsection*{" + text + "}")
            else:
                out.append(r"\subsubsection*{" + text + "}")
            i += 1
            continue

        if is_table_row(line):
            rows = []
            while i < len(lines) and is_table_row(lines[i]):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows))
            continue

        image = re.fullmatch(r"!\[([^\]]*)\]\(([^)\s]+)\)", stripped)
        if image:
            alt, path = image.group(1), image.group(2)
            out.append(
                "\\begin{center}\n"
                f"\\includegraphics[width=\\linewidth,height=0.40\\textheight,keepaspectratio]{{{path}}}\n"
                "\\end{center}"
                if alt is not None
                else ""
            )
            i += 1
            continue

        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            out.append(r"\medskip\noindent\rule{\linewidth}{0.4pt}\medskip")
            i += 1
            continue

        bullet = re.match(r"^\s{0,2}[-*]\s+(.*)$", line)
        if bullet:
            items: list[list[str]] = []
            while i < len(lines):
                current = lines[i]
                marker = re.match(r"^\s{0,2}[-*]\s+(.*)$", current)
                if marker:
                    items.append([marker.group(1)])
                elif current.strip() and items and current.startswith(("  ", "\t")):
                    items[-1].append(current.strip())
                else:
                    break
                i += 1
            rendered = [
                "\\item " + " ".join(inline(x) for x in item) for item in items
            ]
            out.append(
                f"\\begin{{itemize}}[{LIST_OPTIONS}]\n"
                + "\n".join(rendered)
                + "\n\\end{itemize}"
            )
            continue

        ordered = re.match(r"^\s{0,2}\d+\.\s+(.*)$", line)
        if ordered:
            items = []
            while i < len(lines):
                current = lines[i]
                marker = re.match(r"^\s{0,2}\d+\.\s+(.*)$", current)
                if marker:
                    items.append([marker.group(1)])
                elif current.strip() and items and current.startswith(("   ", "\t")):
                    items[-1].append(current.strip())
                else:
                    break
                i += 1
            rendered = [
                "\\item " + " ".join(inline(x) for x in item) for item in items
            ]
            out.append(
                "\\begin{enumerate}[label=\\arabic*.,"
                + LIST_OPTIONS
                + "]\n"
                + "\n".join(rendered)
                + "\n\\end{enumerate}"
            )
            continue

        paragraph = []
        while i < len(lines) and lines[i].strip():
            nxt = lines[i]
            if (
                re.match(r"^(#{1,4})\s+", nxt)
                or is_table_row(nxt)
                or re.fullmatch(r"!\[[^\]]*\]\([^)\s]+\)", nxt.strip())
                or re.match(r"^\s{0,2}[-*]\s+", nxt)
                or re.match(r"^\s{0,2}\d+\.\s+", nxt)
            ):
                break
            paragraph.append(nxt)
            i += 1
        centred = bool(paragraph) and paragraph[0].lstrip().startswith("**Project:**")
        out.append(render_paragraph(paragraph, centred=centred))

    out.append(r"\end{document}")
    return "\n\n".join(part for part in out if part)


def main() -> int:
    if not SRC.exists():
        print(f"missing source: {SRC}")
        return 1
    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        print("pdflatex not found on PATH; install a TeX distribution")
        return 1

    tex = build_tex(SRC.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="report-tex-") as tmp:
        build = pathlib.Path(tmp)
        tex_path = DOCS / "FINAL_REPORT_build.tex"
        tex_path.write_text(tex, encoding="utf-8")
        try:
            cmd = [
                pdflatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                "-output-directory=" + str(build),
                tex_path.name,
            ]
            for _ in range(2):
                r = subprocess.run(
                    cmd,
                    cwd=DOCS,
                    capture_output=True,
                    text=True,
                    encoding="cp1252",
                    errors="replace",
                    timeout=300,
                )
                if r.returncode != 0:
                    log = build / "FINAL_REPORT_build.log"
                    tail = (
                        log.read_text(encoding="utf-8", errors="replace")[-2500:]
                        if log.exists()
                        else (r.stdout or "")[-2500:]
                    )
                    print("LaTeX failed:\n" + tail)
                    return 1
            produced = build / "FINAL_REPORT_build.pdf"
            if not produced.exists():
                print("LaTeX produced no PDF")
                return 1
            shutil.copyfile(produced, OUT)
        finally:
            tex_path.unlink(missing_ok=True)

    print(f"wrote {OUT.name}: {OUT.stat().st_size / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
