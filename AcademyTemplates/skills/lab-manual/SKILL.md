---
name: lab-manual
description: >-
  Create a laboratory work for students: a print-ready PDF lab manual (XeLaTeX, English / Armenian /
  classical Armenian) AND the matching lab folder for the SemiTec Academy app (lab.json with steps and a
  check quiz, source files, manual.pdf). Use when a lecturer wants to write, update or translate a lab,
  lab manual, laboratory work or hands-on exercise, or turn an existing lab PDF into an app lab.
---

# Lab manual + app lab (SemiTec Foundation)

One lab = two outputs that stay in sync:

```
lab-manual-folder/
├── latex/          the manual: main.tex, metadata.tex, sections/, diagrams/, images/ (+ labstyle.sty, lang/)
└── lab/            what goes into a SemiTec Learning Package (.stlp):
    ├── lab.json    steps (same ids as \labstep in the manual), check quiz, "files"
    ├── manual.pdf  built from latex/ by tools/build.py
    └── src/        source files students view in the app and download as a zip
```

Tools (Python 3 + a TeX distribution with XeLaTeX and the FreeSerif fonts):
- `python3 <skill>/tools/build.py <lab-folder>` — compile, copy `manual.pdf` into `lab/`, write each step's
  page into `lab.json`, run the checker. `--sync-steps` adds manual steps missing in lab.json.
  The first build copies `labstyle.sty`, `lang/`, `.latexmkrc` into the lab's `latex/` (also compiles on Overleaf).
- `python3 <skill>/tools/check_lab.py <lab-folder>` — checks lab.json, files, quiz, manual, and that the
  `\labstep` ids equal the lab.json step ids.

## Where files go — ask once, then remember

Destination folders are **never** hard-coded. Before writing anything, resolve them:

1. Look for **`.semitec.json`**, starting in the working folder and searching upward. If it
   exists, use its values and do **not** ask.
2. If it is missing, ask the user for the keys below — one short round — then write
   `.semitec.json` at the root of their project with the answers, so no later run asks again.

| Key | Used for |
|---|---|
| `contentRoot` | where course materials live; labs go to `<contentRoot>/<topic>/labs/` |

Values are paths relative to `.semitec.json`, or absolute. Create folders that do not exist yet.
Never write outside them, and never assume a particular parent layout.

## Workflow

### 1. Interview (one short round)
Lab title and number, course, language (english / armenian / armenian-classical), duration, difficulty,
group size, equipment and software (with versions), prerequisites (trainings, earlier labs), the
objectives, the procedure as a list of steps, what is measured / shown, what is handed in and how it is
graded, starter files (code, testbench, constraints, scripts). Ask for existing material (old PDF, code).

### 2. Create the folder
Copy the template (`latex/` and `lab/`) to the new lab folder — for a SemiTec Learning Package usually
`Foundation/…/Labs/<course>/lab-NN-<name>/`. `examples/lab-01-shift-register/` is a complete example.

### 3. Write the manual (`latex/`)
- `metadata.tex`: all fields; `\setlabid{lab-NN-name}` = the lab's id in the package.
- `sections/01…07`: follow the comments at the top of each file and `reference/section-guide.md`.
- Procedure: one `\labstep[files]{id}{Title}` per action with a visible result; ids lowercase-with-dashes;
  end key steps with `\expected{…}` or `\checkpoint{…}`. Show code with `\srcfile{src/…}{caption}` (the
  same file students get) or a short `lstlisting`.
- Diagrams: TikZ in `diagrams/<name>.tex`, included with `\adddiagram{name}{0.8}{caption}`.
- Leave nothing as `\missing{…}` in a final version (red in the PDF). Commands: `reference/commands.md`.

### 4. Write the app part (`lab/`)
- `lab.json` (format: `reference/lab-json.md`): the **same step ids and titles** as the manual, each step
  1–3 sentences (the manual has the details), `hint` where students get stuck, `files` links per step.
- `"files": "src"` and the starter files in `lab/src/` (rtl/, sim/, constraints/, scripts/ …). Mark the
  parts students complete with `TODO`.
- Check quiz: 3–6 questions about understanding, each with `review` → the step that teaches it; use
  `multiple` when several answers are right; `passThreshold` 0.7–0.8.

### 5. Build and check
`python3 tools/build.py <lab-folder>` until it reports **0 errors** (warnings: decide with the user).
Look at the PDF (page breaks, figures, code width). For other languages switch the option in `main.tex`.

### 6. Hand over
Report the PDF, the lab folder and the check result. To give the lab to students in the app, add the
**lab/** folder to a course pack with the `academy-templates:package` skill (`AcademyTemplates/skills/package`):
`"labs": [ { "id": "lab-01-…", "source": "<path>/lab" } ]`.

## From an existing lab PDF (no LaTeX source)
Create only the `lab/` folder: copy the PDF as `lab/manual.pdf`, write `lab.json` (steps from the PDF's
procedure, with `manualPage` set by hand), add `src/`, run `check_lab.py` on the folder (the LaTeX check
is skipped when there is no `latex/`).

## Rules
- Step ids never change after students used the lab (progress is stored per id).
- Technical terms (FPGA, RTL, LUT) stay in Latin script in Armenian text.
- Code in the manual and in `src/` must be the same files — include with `\srcfile`, do not paste copies.
- Do not put solutions into `src/` — only starter code with `TODO`.

## Files
- `latex/` template · `lab/` template · `tools/build.py`, `tools/check_lab.py`
- `reference/section-guide.md` (what to write where) · `reference/commands.md` (LaTeX commands) ·
  `reference/lab-json.md` (lab.json formats 1 and 2)
- `examples/lab-01-shift-register/` complete lab (manual + app folder) · `sample-output-*.pdf`

## Academy Templates
Part of the **Academy Templates** plugin: `academy-templates:project-brief` (project brief PDF) ·
`academy-templates:diploma-project` (thesis PDF) · `academy-templates:lab-manual` (lab manual PDF + app lab) ·
`academy-templates:training` (interactive web training) · `academy-templates:package` (`.stlp` for SemiTec
Academy). Hand over to the matching skill when the user needs one of those outputs.

## Where new material goes
Course content lives in `<content>/<topic>/`, where `<content>` is `contentRoot` (see *Where files go*) — e.g.
`IC-Design/Digital-Design/FPGA/labs/fpga-lab01-leds/` (the folder holds `latex/` and `lab/`). Folder
names are `<topic>-<short-name>` (they become ids in packages). Use a **last-level** topic (one without
sub-topics). Where `<content>/tools/inventory.py` exists, run it with `--init <topic>` first if the
topic's folders are missing, and again after adding material; skip this when the script is absent.
