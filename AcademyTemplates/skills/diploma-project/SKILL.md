---
name: diploma-project
description: >-
  Create a diploma, thesis, or research-project document and its defense slides
  from a standard academic structure. Use when a student or author wants to draft,
  outline, or produce a diploma/thesis/research project — as a LaTeX document, a
  PDF, a Word (.docx) file, or a slide deck. Includes a ready, compilable LaTeX
  template with custom commands for the title page, figures, diagrams, tables,
  glossary, and references. Trigger on "diploma project", "thesis", "graduation
  project", "research project write-up", or turning project details into a
  formatted academic document or defense presentation.
---

# Diploma / Thesis / Research Project Template

This skill turns a student's project information into a **complete, well-structured
academic document** (diploma, thesis, or research project) and, optionally, a
**defense slide deck** — following a standard academic structure that authors
customize.

It ships a **ready-to-compile LaTeX template** as the primary format, plus
format-agnostic guidance so the same structure can also be produced as Word/PDF.

## What's in the package

```
diploma-project/
  latex/            ← the LaTeX template (compilable; primary format)
    main.tex, diplomastyle.sty, metadata.tex, glossary.tex, references.bib
    sections/  diagrams/  images/   + README.md with the full command reference
  slides/           ← defense-slides template (Beamer or PPTX) — coming next
  reference/        ← format-agnostic guidance
    document-structure.md · formatting-and-figures.md · slides-outline.md
  templates/
    diploma-template.md   ← a plain-Markdown skeleton (for non-LaTeX authors)
  examples/
    example-outline.md            ← a short Markdown outline example
    fpga-sensor-platform-hy/      ← full worked example: a cross-department FPGA
                                    diploma TASK DEFINITION in Armenian, built with a
                                    XeLaTeX variant of the style (diplomastyle-hy.sty).
                                    Shows Armenian typesetting, TikZ diagrams, a
                                    register-map table, and a compiled PDF.
  sample-output.pdf ← what the LaTeX template compiles to (placeholder content)
```

> **Languages.** The primary `latex/` template uses pdfLaTeX + Times (Latin). For
> **Armenian** (or other non-Latin scripts), use the XeLaTeX approach shown in
> `examples/fpga-sensor-platform-hy/` — `fontspec` with an Armenian-capable font
> (FreeSerif), built with `xelatex`. That `diplomastyle-hy.sty` can be adopted as
> the template's Armenian variant.

> **Read `reference/template-guide.md` first — it is the complete guide** to every
> feature: the two language variants, simple vs cross-disciplinary projects, all the
> custom functions, images, diagrams, tables, abbreviations, glossary, references,
> and building. This SKILL is the summary; the guide has the detail.

## How to use it

1. **Collect the project details** — title, student(s), supervisor(s), institution /
   department, degree and **work type** (diploma / thesis / research project),
   field, and a short description of the problem, method, and results.

   Then settle **two choices** (see the guide §1):
   - **Language:** Latin script → `latex/` + `diplomastyle.sty`, build with
     **pdfLaTeX**. Armenian / non-Latin → the **XeLaTeX** variant
     `diplomastyle-hy.sty` (copy `examples/fpga-sensor-platform-hy/`).
   - **Mode:** **simple** (one student) or **cross-disciplinary** (two students,
     often different departments). Both are supported — for cross-disciplinary set
     the second student (`\setsecondauthor…` in the Latin variant, `\setstudenttwo…`
     in the Armenian one) and the title page becomes a two-student layout.

2. **Pick the output the author wants:**
   - **LaTeX** (recommended for a formal thesis) — use the `latex/` template.
   - **Word (.docx) or PDF** — use the `templates/diploma-template.md` skeleton and
     `reference/` guidance, then follow the `docx` / `pdf` skill to build the file.
   - **Slides** — follow `reference/slides-outline.md` and the `pptx` skill (until
     the `slides/` template lands).

3. **For the LaTeX template** (`latex/`):
   - Fill in `metadata.tex` (title, author, …).
   - Write each chapter in `sections/NN-*.tex`. Use the custom commands:
     `\problemstatement{}`, `\addimage[label]{images/f}{width}{caption}`,
     `\adddiagram[label]{name}{width}{caption}`, `\gls{key}`, `\citep{key}`.
   - Add images to `images/`, TikZ diagrams to `diagrams/`, references to
     `references.bib`, **abbreviations to `abbreviations.tex`** and glossary terms
     to `glossary.tex` (kept separate; every defined entry is listed via
     `\glsaddall`, with no page numbers).
   - One chapter per file in `sections/`.
   - Build with `latexmk -pdf main.tex` (Latin) or `latexmk -xelatex main.tex`
     (Armenian). The `.latexmkrc` runs BibTeX + makeglossaries automatically.
   - The **complete reference is `reference/template-guide.md`**; `latex/README.md`
     is the Latin-variant quick reference.

4. **Choose depth by work type.** A research project is lighter than a full thesis;
   `reference/document-structure.md` marks each section required/optional and how it
   scales. Include required sections; add optional ones as content warrants.

5. **Keep the author's material central.** Do not invent results or citations —
   leave clearly marked placeholders (`[TODO: …]`, `[CITATION NEEDED]`) where
   information is missing. Follow `reference/formatting-and-figures.md` for
   captions, tables, diagrams, and citation style.

## Customizing

Universities differ. Treat the structure and the LaTeX title page as a sensible
default and adjust section names, order, required/optional status, and the title
page to match the author's institution. A topic-posting system can store several templates
(e.g. one per university or per work type).

## Academy Templates
Part of the **Academy Templates** plugin: `academy-templates:project-brief` (project brief PDF) ·
`academy-templates:diploma-project` (thesis PDF) · `academy-templates:lab-manual` (lab manual PDF + app lab) ·
`academy-templates:training` (interactive web training) · `academy-templates:package` (`.stlp` for SemiTec
Academy). Hand over to the matching skill when the user needs one of those outputs.
