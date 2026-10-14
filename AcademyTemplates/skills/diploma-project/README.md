# diploma-project — template for the final diploma / thesis document

For **students** (and their supervisors) who write the final document of a diploma, thesis or research
project, and prepare the defense. It comes **after** the brief made with `../project-brief`.

## With an AI agent (recommended)
Use the skill `academy-templates:diploma-project` (or `academy-diploma-project` in the Claude app), then
say e.g. *"Help me write my bachelor thesis on the FPGA sensor platform — here are my notes and results"*.
The agent follows `SKILL.md`:
1. collects the project details (title, student(s), supervisor(s), department, degree, work type, field);
2. settles the **language** (Latin → `latex/`, pdfLaTeX; Armenian → XeLaTeX variant) and the **mode**
   (one student or a cross-disciplinary pair);
3. picks the output: LaTeX (recommended), Word / PDF from the Markdown skeleton, or a slides outline;
4. writes the chapters from your material — results and citations are never invented, missing parts are
   marked `[TODO: …]` / `[CITATION NEEDED]`;
5. builds the PDF.

## By hand
1. Copy `latex/` to a new folder.
2. Fill `metadata.tex` (title, author, supervisor, …) and write one chapter per file in `sections/`.
3. Add images to `images/`, TikZ diagrams to `diagrams/`, references to `references.bib`,
   abbreviations to `abbreviations.tex`, glossary terms to `glossary.tex`.
4. Build: `latexmk -pdf main.tex` (Latin). For Armenian start from `examples/fpga-sensor-platform-hy/`
   and build with `latexmk -xelatex main.tex`.

## What is in the document
Title page (one or two students) · abstract · introduction · background · methodology · design /
implementation · results · conclusion · references · abbreviations · glossary · appendices.
`reference/document-structure.md` marks each part required / optional per work type.

## Files

| Path | Content |
|---|---|
| `SKILL.md` | instructions for the AI assistant |
| `latex/` | the template: `main.tex`, `diplomastyle.sty`, `metadata.tex`, `sections/`, `diagrams/`, `images/`, `abbreviations.tex`, `glossary.tex`, `references.bib`, `README.md` (command reference) |
| `reference/template-guide.md` | **the complete guide**: languages, simple vs cross-disciplinary, every command |
| `reference/document-structure.md` · `formatting-and-figures.md` · `slides-outline.md` | structure, figures and citations, defense slides |
| `templates/diploma-template.md` | Markdown skeleton (for Word / Google Docs authors) |
| `examples/` | `example-outline.md`; `fpga-sensor-platform-hy/` — full Armenian XeLaTeX example with PDF |
| `slides/` | defense-slides template (planned: Beamer or PPTX) |
| `sample-output.pdf` | the empty template compiled |
