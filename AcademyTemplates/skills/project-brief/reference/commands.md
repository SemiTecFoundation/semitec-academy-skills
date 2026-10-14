# LaTeX command reference (`briefstyle.sty`)

Build: `latexmk -xelatex main.tex` (XeLaTeX + Biber; uses the included `.latexmkrc`).
Manual build: `xelatex main → biber main → xelatex main → xelatex main`.
Overleaf: set the compiler to **XeLaTeX**; Biber runs automatically.

## Package options
`\usepackage[<language>,<options>]{briefstyle}`
- language: `english` · `armenian` · `armenian-classical`
- `newpagechapters`: every chapter on a new page (default: continuous)
- `draft`: adds "DRAFT" to the page header

## Metadata (`metadata.tex`)
All are `\set<field>{value}`. Empty fields are not printed.

| Field | Setter | Shown on |
|---|---|---|
| title / subtitle | `\settopictitle` `\settopicsubtitle` | title page, card |
| document type line | `\setdoctype` (default is set by language and mode) | title page |
| version / date / status | `\setversion` `\setdate` `\setstatus` | title page |
| institution / faculty / city / year | `\setinstitution` `\setfaculty` `\setcity` `\setyear` | title page |
| student 1 / dept / supervisor | `\setstudentone` `\setdeptone` `\setsupervisorone` | title page, card, approval |
| student 2 / dept / supervisor | `\setstudenttwo` `\setdepttwo` `\setsupervisortwo` | **switches to cross mode** |
| force cross mode | `\setcrossmode{yes}` | |
| partner, industry mentor | `\setpartnerorg` `\setmentor` | title page, card, approval |
| platform fields | `\setworktype` `\setdegreelevel` `\setareas` `\setkeywords` `\setslots` `\setduration` `\setstartdate` `\setdeadline` `\setworklanguage` `\settools` `\setprerequisites` | card |

An empty student name prints "to be assigned" / «կնշանակվի», so the brief can
be published before a student is chosen.

## Mode-dependent text
- `\ifcross{...}`: printed only in cross-department mode
- `\ifsingle{...}`: printed only in single-student mode
- `\studentlabel{1}`: "Student 1" in cross mode, "Student" in single mode (same for `\supervisorlabel{n}`)

## Placeholders
- `\missing{text}`: red **[ text ]** for information still to be supplied.
  A published brief must have none. Check with `grep -rn '\\missing' .`

## Callout boxes
`\problemstatement{}` · `\summarybox{}` · `\keypoint{}` · `\notebox{}`

## Tasks
```latex
\begin{tasklist}{1}          % 1 = student 1, 2 = student 2, 0 = shared
  \task Design the FIFO buffer.               % → T1.1 (Armenian: Խ1.1)
  \task \optionaltask Add DMA transfer.       % → T1.2 (optional)
\end{tasklist}
```
`\label{}` after `\task` lets you reference a task: `\ref{...}` → T1.2.

## Learning path
```latex
\levellegend                                  % explains the three badges
\begin{learningpath}[Knowledge map — \studentlabel{1}.]
  \learngroup{Digital design}
  \learn{FSM design}{\apply}{control of the generator}{\cite{harris2021}, ch.~3}
  \learn{AXI4-Lite}{\understand}{configuration registers}{\cite{amd-pg155}}
  \learn{Timing closure}{\aware}{implementation reports}{\cite{ug906}}
\end{learningpath}
```
Levels: `\aware` · `\understand` · `\apply`

## Warm-up exercises
```latex
\begin{warmup}{Blink through AXI}{6 h}
  Create a block design with … 
  \donewhen{the LED rate changes when a register is written from the PS.}
\end{warmup}
```

## Tables (each row is one command; all tables break across pages)
| Environment | Row command |
|---|---|
| `workplan[caption]` | `\milestone{weeks}{phase}{checkpoint result}` |
| `deliverables[caption]` | `\deliverable{what}{form}{due}{responsible}` |
| `rubric[caption]` | `\criterion{criterion}{weight}{pass}{good}{excellent}` |
| `risks[caption]` | `\risk{risk}{impact}{mitigation}` |
| `interfaces[caption]` | `\iface{interface}{direction}{agreed format}` |
| `progresstracker[caption]` | `\weekrow{week}{planned work}{checkpoint}` (adds an empty ☐ box and a notes column); `\weekbreak{phase}` = shaded separator |

To label a table, put `\label{tab:x}` inside the caption: `[Work plan.\label{tab:plan}]`.

## Figures
- `\adddiagram[fig:label]{name}{0.8}{Caption.}` inserts the TikZ file `diagrams/name.tex`, scaled to 80% of the text width
- `\addimage[fig:label]{images/file.png}{0.7}{Caption.}`
- Colors for diagrams: `briefaccent`, `brieflight`, `briefapply`, `briefgray`

## References, abbreviations, glossary
- `references.bib` (BibLaTeX, UTF-8). Cite with `\cite{key}`. Printed as
  "References and Reading List" in **groups with their own label prefix**:
  Books `[B1]` (`@book`), Articles and papers `[A1]` (`@article`,
  `@inproceedings`, `@incollection`), User guides, datasheets and standards `[U1]`
  (`@manual`), Web resources `[W1]` (`@online`), Other `[M1]`. Pick the entry type
  accordingly. Citations in the text get the prefix automatically. Empty groups
  are skipped.
- `abbreviations.tex`: `\newacronym{key}{SHORT}{Long form}`
- `glossary.tex`: `\newglossaryentry{key}{name=…,description=…}`
- Use with `\gls{key}`. All defined entries are listed in definition order. No
  external index tool is needed.

## Structure commands (in `main.tex`)
`\maketitlepage` · `\frontmatterpages` (card + contents) · `\mainmatterstart` ·
`\printreferences` · `\printglossarysection` · `\approvalblock`
