# Conventions

What all Academy Templates share, so that every Foundation document and page looks and works alike.

## PDF templates (project-brief, diploma-project, lab-manual)

- **Engine:** XeLaTeX + Biber, built with `latexmk -xelatex main.tex` (also on Overleaf with the XeLaTeX
  compiler). The Latin diploma template uses pdfLaTeX (`latexmk -pdf`); its Armenian variant uses XeLaTeX.
- **Languages:** English, Armenian (reformed spelling), Armenian (classical spelling) — chosen with a
  package option in `main.tex`; labels live in `latex/lang/`. Technical terms stay in Latin script.
- **Fonts:** FreeSerif / FreeSans / FreeMono (Armenian + Latin), included in TeX Live and MacTeX.
- **Structure:** `main.tex`, a style file (`briefstyle.sty`, `labstyle.sty`, `diplomastyle.sty`),
  `metadata.tex` for all document data, one chapter per file in `sections/`, TikZ diagrams in `diagrams/`,
  `references.bib` grouped as Books [B], Articles [A], User guides [U]; abbreviations and glossary lists;
  callout boxes.
- **Missing information** is never invented: red `\missing{…}` markers (or `[TODO: …]`) show what the
  author still has to give.
- Every PDF template ships `sample-output-*.pdf` for each supported language.

## Web templates (training)

- **Self-contained:** HTML + CSS + JavaScript in one folder, works offline, no build step to view;
  `tools/build_single_file.py` makes one HTML file to share.
- **Content separate from layout:** all content in JSON (`training.json`, `topics/*.json`), all styling
  in theme files; both can be written or changed by prompting an AI.
- **Accessible:** keyboard navigation, contrast, works at phone width.
- **Same look** (colours, typography) as the PDF templates; same three languages for labels.
- **Delivery modes:** standalone, preview, platform (`INTEGRATION.md`); the SemiTec Academy app runs the
  same engine in platform mode.

## Outputs for SemiTec Academy

- A lab's `lab/` folder (lab-manual), a training folder (training), PDFs and Markdown files are the
  inputs of the **package** skill; it checks them and builds one signed `.stlp`.
- Ids (lab id, training id, step / topic ids) are lowercase-with-dashes and never change after release —
  students' progress is stored per id.

## Skill folders

- Folder name = skill name (`skills/<name>/`, lowercase, digits, `-`); `SKILL.md` frontmatter `name` is
  the same; `description` says what it makes and when to use it (≤ 1024 characters).
- Each skill has `SKILL.md` (for the assistant), `README.md` (for people), `reference/` (detailed
  guidance), `examples/` (a complete worked example) and its tools (`tools/` or `scripts/`).
- Paths in `SKILL.md` are relative to the skill folder, so the skill works the same in the plugin, in
  `~/.claude/skills/academy-<name>/` and as a zip in the Claude app.
- Other skills are referred to by their plugin name (`academy-templates:<name>`).
