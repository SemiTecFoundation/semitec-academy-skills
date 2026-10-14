# LaTeX diploma / thesis / research-project template

A modular LaTeX template. You mostly edit **`metadata.tex`**, the files in
**`sections/`**, **`references.bib`**, **`abbreviations.tex`**, and
**`glossary.tex`**, and drop your own
files into **`images/`** and **`diagrams/`**. All the machinery — packages, page
setup, and the custom commands — lives in **`diplomastyle.sty`**, so you rarely
touch `main.tex`.

## Files

```
main.tex            wires everything together (which sections are included, in order)
diplomastyle.sty    the style package: all packages + the custom commands
metadata.tex        your project details (title, author, supervisor, …)
sections/           one .tex per chapter — edit these
  00-abstract.tex … 07-appendix.tex
diagrams/           TikZ diagrams, one .tex each (see below)
images/             image files (png/jpg/pdf) you insert with \addimage
references.bib      bibliography database (BibTeX)
abbreviations.tex   acronyms  → "List of Abbreviations"
glossary.tex        glossary terms → "Glossary"
.latexmkrc          makes `latexmk` run bibtex + the glossary automatically
Makefile            convenience build targets
```

## Building the PDF

You need a TeX distribution (TeX Live or MiKTeX). Then, from this folder:

```
latexmk -pdf main.tex        # recommended: one command does everything
```

or, without latexmk:

```
pdflatex main
bibtex main
makeglossaries main
pdflatex main
pdflatex main
```

(The template was test-compiled with pdfLaTeX + BibTeX + makeglossaries; it uses
Times fonts and needs no on-the-fly font generation. It uses BibTeX/`natbib`, not
biber.)

## The custom commands

Put these in your section files:

| Command | What it does |
|---------|--------------|
| `\problemstatement{...}` | a titled callout box for the problem statement |
| `\summarybox{...}` / `\keypoint{...}` | other callout boxes |
| `\addimage[label]{images/file}{width}{caption}` | centered figure from an image; **width** is a fraction of the text width (e.g. `0.6`) |
| `\adddiagram[label]{name}{width}{caption}` | centered figure from `diagrams/name.tex` (a TikZ picture), scaled to **width** |
| `\gls{key}` | prints a glossary/acronym term (defined in `abbreviations.tex` / `glossary.tex`) |
| `\citep{key}` / `\citet{key}` | cite a reference from `references.bib` |
| `\ref{label}` | cross-reference a figure/table/chapter |

Metadata setters (in `metadata.tex`): `\setprojecttitle`, `\setauthor`,
`\setsupervisor`, `\setcosupervisor`, `\setinstitution`, `\setdepartment`,
`\setprogram`, `\setdegree`, `\setworktype`, `\setfield`, `\setcity`, `\setyear`.

Structure commands (already placed in `main.tex`): `\maketitlepage`,
`\frontmatterpages{...}`, `\mainmatterstart`, `\printbibsection`,
`\printglossarysection`, `\appendixsection{...}`, `\makebackpage`.

## Adding content

- **A new chapter:** create `sections/08-yourchapter.tex` starting with
  `\chapter{...}`, then add `\input{sections/08-yourchapter}` in `main.tex`.
- **An image:** drop it in `images/`, then
  `\addimage[fig:mine]{images/mine.png}{0.7}{Caption.}`.
- **A reference:** add a BibTeX entry to `references.bib`, cite with
  `\citep{key}`.
- **An abbreviation:** add a `\newacronym` to `abbreviations.tex`; **a glossary
  term:** add a `\newglossaryentry` to `glossary.tex`. Use either with `\gls{key}`.
  Every defined entry is listed even if unused (the style calls `\glsaddall`).

## Diagrams — the recommended way

**Use TikZ**, one diagram per file in `diagrams/`. TikZ is the best fit for a
LaTeX document because it is:

- **vector** (crisp at any size, scaled to your chosen width by `\adddiagram`),
- **text/versionable** (diffs well in git, no binary blobs), and
- **consistent** with the document's fonts and line style.

Each file contains only the picture (`\begin{tikzpicture}…\end{tikzpicture}`), as
in `diagrams/example-architecture.tex`, and you insert it with
`\adddiagram[label]{filename}{width}{caption}`.

For diagrams that are painful to hand-code, draw them in a tool that **exports
vector PDF** (e.g. draw.io / diagrams.net, Excalidraw, Inkscape, or `tikzit` which
edits TikZ visually), save the PDF into `images/`, and insert it with `\addimage`.
Avoid pasting raster screenshots of diagrams — they blur when scaled. (Mermaid and
similar are not native to LaTeX; export them to PDF/SVG→PDF first.)

A `sample-output.pdf` of this template (with placeholder content) is in the parent
folder so you can see what it produces.
