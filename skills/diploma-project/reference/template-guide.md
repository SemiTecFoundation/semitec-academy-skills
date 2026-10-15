# Diploma Template — Complete Guide

The authoritative reference for producing a diploma / thesis / research-project
document with this template. It covers the shipped **Latin/pdfLaTeX** template and both project modes (simple single-student and
cross-disciplinary two-student), and every template feature — functions, images,
diagrams, tables, abbreviations, glossary, references, and building. Read this
before generating a document.

---

## 1. Decide the setup

### 1a. Language / script

| Content language | Style file | Engine | Fonts |
|------------------|-----------|--------|-------|
| **Latin script** (English, etc.) | `diplomastyle.sty` (in `latex/`) | **pdfLaTeX** (+ BibTeX) | Times |

Use a separate reviewed language-specific skill for non-Latin scripts. It needs reproducible builds and
fictional fixtures before it can join the shared product.

### 1b. Project mode → simple or cross-disciplinary

- **Simple:** one student. Set a single author.
- **Cross-disciplinary:** two students (often different departments), one shared
  project. Set the second student too.

The **title page adapts automatically** —
a single author is shown plainly; a second author makes it a two-student layout.
Leave the second-author fields unset for a simple diploma.

---

## 2. Files & structure

```
main.tex            wires the document together (which chapters, in order)
diplomastyle.sty    shared Latin-script style
metadata.tex        project details — EDIT the placeholders
abbreviations.tex   acronyms  → "List of Abbreviations"
glossary.tex        glossary terms → "Glossary"
references.bib      bibliography (Latin variant; BibTeX)
sections/           ONE FILE PER CHAPTER (01-…, 02-…, …)
diagrams/           TikZ diagrams, one .tex each
images/             image files (png/jpg/pdf)
.latexmkrc          makes `latexmk` run BibTeX + makeglossaries automatically
```

**One chapter per file.** Each `sections/NN-name.tex` starts with `\chapter{...}`.
To add a chapter, create the file and add `\input{sections/NN-name}` in `main.tex`.

---

## 3. Metadata & title page

Set these in `metadata.tex`:

| Setter | Meaning |
|--------|---------|
| `\setauthor{}` | the (first) student |
| `\setsupervisor{}` | supervisor |
| `\setcosupervisor{}` | optional co-supervisor |
| `\setdepartment{}` · `\setprogram{}` · `\setdegree{}` · `\setfield{}` | academic details |
| **`\setsecondauthor{}`** | second student → **cross-disciplinary mode** |
| **`\setsecondauthordept{}`** | second student's department |
| **`\setsecondsupervisor{}`** | second student's supervisor |

Optional fields left unset simply don't appear (handled with `\ifdefempty`, so an
empty value never prints a stray label). `\maketitlepage` builds the page.

---

## 4. The custom functions

Use these inside your chapter files.

| Command | Purpose |
|---------|---------|
| `\problemstatement{...}` | a titled callout box for the problem statement |
| `\summarybox{...}` | a "Summary" callout box |
| `\keypoint{...}` | a "Key Point" callout box |
| `\notebox{...}` | a "Note" callout box |
| `\addimage[label]{images/file}{width}{caption}` | centered figure from an image |
| `\adddiagram[label]{name}{width}{caption}` | centered figure from a TikZ diagram file |
| `\gls{key}` | print a glossary/abbreviation term |
| `\citep{key}` / `\citet{key}` | cite a reference (Latin variant) |
| `\ref{label}` | cross-reference a figure/table/chapter |

Structure commands (already placed in `main.tex`): `\maketitlepage`,
`\frontmatterpages`, `\mainmatterstart`, `\printglossarysection` (prints the
abbreviations + glossary), and for the Latin variant `\printbibsection` /
`\appendixsection{}` / `\makebackpage`.

---

## 5. Images

1. Put the file in `images/` (PNG/JPG for photos & screenshots, **vector PDF** for
   charts/diagrams made elsewhere).
2. Insert it:
   ```latex
   \addimage[fig:screenshot]{images/dashboard.png}{0.7}{The main dashboard.}
   ```
   - The **third argument is the width** as a fraction of the text width (`0.7` =
     70%). This is how you control size.
   - The image is **centered** and given a numbered **caption** automatically; the
     optional `[label]` lets you `\ref{fig:screenshot}` it.

---

## 6. Diagrams — the recommended way

**Use TikZ**, one diagram per file in `diagrams/` — it is vector (scales cleanly to
the width you pick), text-based (diffs in git), and matches the document fonts.

1. Create `diagrams/architecture.tex` containing **only** the picture:
   ```latex
   \begin{tikzpicture}[...]
     ...
   \end{tikzpicture}
   ```
2. Insert and size it:
   ```latex
   \adddiagram[fig:arch]{architecture}{0.7}{System architecture.}
   ```
   `name` is the filename without `.tex`; the third argument is the width fraction;
   it is centered, scaled, and captioned automatically.

Libraries already loaded: `positioning`, `arrows.meta`, `shapes.geometric`, `calc`. Add more in the style file.

**For diagrams too complex to hand-code**, draw them in a tool that exports **vector
PDF** (draw.io / diagrams.net, Inkscape, `tikzit`), save the PDF in `images/`, and
insert it with `\addimage`. Avoid raster screenshots of diagrams — they blur when
scaled. (Mermaid etc. are not native to LaTeX; export to PDF first.)

---

## 7. Tables

Use `booktabs` rules:
```latex
\begin{table}[htbp]
  \centering
  \caption{Evaluation results.}
  \label{tab:results}
  \begin{tabular}{lcc}
    \toprule
    Method & Metric A & Metric B \\
    \midrule
    Baseline & 0.70 & 0.65 \\
    Ours     & 0.82 & 0.79 \\
    \bottomrule
  \end{tabular}
\end{table}
```
The FPGA example's register-map table is a good model for a wider table.

---

## 8. Abbreviations (List of Abbreviations)

Define acronyms in **`abbreviations.tex`**:
```latex
\newacronym{fpga}{FPGA}{Field-Programmable Gate Array}
```
Use them in text with `\gls{fpga}` (prints the full form the first time, the short
form after). **Every defined abbreviation is listed even if you never use it in the
text** — the style calls `\glsaddall`. The list shows **no page numbers** (the
`nonumberlist` option), which is the correct style for a "List of Abbreviations".

> This is the key gotcha: without `\glsaddall`, `glossaries` prints only the
> acronyms actually used with `\gls{}`, so defined-but-unused ones silently vanish.
> The template already handles this — just define them in `abbreviations.tex`.

## 9. Glossary

Define terms in **`glossary.tex`** (kept separate from abbreviations):
```latex
\newglossaryentry{metadata}{name=metadata,
  description={data that describes the structure of other data}}
```
Use with `\gls{metadata}`. Same behavior: all listed, no page numbers.

`\printglossarysection` (already in `main.tex`) prints both the abbreviations and
the glossary.

## 10. References (Latin variant)

Add BibTeX entries to `references.bib`, cite with `\citep{key}` / `\citet{key}`;
`\printbibsection` prints them.

---

## 11. Building

| Template | Command |
|----------|---------|
| Included Latin template (`diplomastyle.sty`) | `latexmk -pdf main.tex` |

The included `.latexmkrc` makes `latexmk` run **BibTeX and makeglossaries**
automatically, so one command builds the whole PDF. Manual sequence if needed:
`pdflatex/xelatex → (bibtex) → makeglossaries → pdflatex/xelatex → pdflatex/xelatex`.

A glossary that looks empty almost always means the glossary step didn't run —
use `latexmk`, or run `makeglossaries main` between LaTeX passes.

---

## 12. Fictional outline

- **`example-outline.md`** — a short, single-student outline (shape only).
- **`../sample-output.pdf`** — the Latin template compiled with placeholder content.

---

## 13. Customizing for an institution

Treat the structure and the title page as a sensible default. Institutions differ
in required sections, title-page layout, and citation style — adjust `metadata.tex`,
the section files, and (for layout) the `\maketitlepage` block in the style file.
The platform can store several templates (e.g. one per university or per work type).
`reference/document-structure.md` lists which sections are required vs optional and
how they scale for diploma / thesis / research project.
