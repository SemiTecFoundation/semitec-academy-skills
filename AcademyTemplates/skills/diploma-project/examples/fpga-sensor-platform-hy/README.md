# FPGA սենսորային հարթակ — դիպլոմային նախագծի առաջադրանք (հայերեն)

Combined, Armenian-language **task definition (առաջադրանք)** for the cross-department
bachelor diploma *"FPGA-Based Sensor Data Acquisition, Processing and Analytics
Platform"* (AMD AUP ZU3 / Zynq UltraScale+). Two students: Microelectronics (FPGA/RTL)
and Software/CE (data platform). Built from the diploma template, adapted for Armenian.

## Build (XeLaTeX required; glossary needs makeglossaries)

```
latexmk -xelatex main.tex       # uses the included .latexmkrc — does everything
# or manually:
xelatex main.tex ; makeglossaries main ; xelatex main.tex ; xelatex main.tex
```

Needs XeLaTeX and the **FreeSerif / FreeSans / FreeMono** fonts (GNU FreeFont — cover
Armenian and Latin, so technical terms like FPGA / AXI / RTL stay in Latin inside
Armenian text).

## Files

```
main.tex             document body — lists the chapters, in order
diplomastyle-hy.sty  Armenian/XeLaTeX style — fonts, Armenian captions, custom commands
metadata.tex         title, students, supervisors, institution — EDIT the [placeholders]
abbreviations.tex    acronyms  → «Հապավումների ցանկ» (List of Abbreviations)
glossary.tex         glossary terms → «Բառարան» (Glossary)
sections/            ONE FILE PER CHAPTER:
                       01-context · 02-idea · 03-goals · 04-fpga · 05-communication
                       06-data · 07-mvp · 08-student1 · 09-student2 · 10-demo · 11-extensions
diagrams/            architecture.tex · rtl-pipeline.tex  (TikZ)
FPGA-arajadrank.pdf  the compiled result
```

## Editing

- **A chapter:** edit the matching file in `sections/`. To add one, create
  `sections/NN-name.tex` starting with `\chapter{...}` and add `\input{sections/NN-name}`
  in `main.tex`.
- **An abbreviation:** add a `\newacronym` to `abbreviations.tex`; **a glossary term:**
  add a `\newglossaryentry` to `glossary.tex`. Every defined entry is listed even if
  unused (the style calls `\glsaddall`).
- **Placeholders:** fill the `[...]` in `metadata.tex` (student names, supervisors,
  university, faculty).

The style file (`diplomastyle-hy.sty`) is the Armenian counterpart of the reusable
diploma template's `diplomastyle.sty`.
