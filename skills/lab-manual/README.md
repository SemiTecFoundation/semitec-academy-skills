# Lab manual template

A laboratory work in two forms that stay in sync:

1. a print-ready **PDF lab manual** (XeLaTeX; English, Armenian, classical Armenian) with a
   "Lab at a glance" card, numbered procedure steps, code listings from the lab's source files,
   checkpoints, measurements, questions and grading;
2. the **app lab** for SemiTec Academy (`lab/`): `lab.json` (the same steps as a checklist + a check
   quiz), `manual.pdf`, and the source files students view and download (`src/`).

The manual and `lab/` folder can be used or shared on their own. Use the package skill only when this lab
is one selected part of an Academy course with other materials.

```
lab-manual/
├── SKILL.md                 instructions for an AI assistant
├── latex/                   manual template (main.tex, metadata.tex, sections/, diagrams/, labstyle.sty, lang/)
├── lab/                     app-lab template (lab.json, src/, manual.pdf after a build)
├── tools/build.py           compile → lab/manual.pdf → step pages into lab.json → check
├── tools/check_lab.py       checks lab.json, files, quiz, manual and manual ↔ lab.json step ids
├── reference/               section-guide.md · commands.md · lab-json.md
├── examples/lab-01-shift-register/   complete example (manual + app lab with 6 source files)
└── sample-output-*.pdf      English example; Armenian and classical Armenian template
```

## Make a lab

```bash
cp -r lab-manual/latex lab-manual/lab  my-labs/lab-02-counter/          # (the folder needs latex/ and lab/)
# edit latex/metadata.tex, latex/sections/*.tex, lab/lab.json, put starter files into lab/src/
python3 lab-manual/tools/build.py my-labs/lab-02-counter                 # PDF + lab.json pages + check
```

Requirements: TeX Live / MacTeX / MiKTeX with XeLaTeX, Biber, latexmk and the GNU FreeFont fonts
(`FreeSerif`); Python 3. On Overleaf: upload `latex/` and compile with XeLaTeX.

## Into the app

Add the `lab/` folder to a SemiTec Learning Package (`skills/package`):

```json
"labs": [ { "id": "lab-02-counter", "source": "my-labs/lab-02-counter/lab" } ]
```

In SemiTec Academy the lab has the tabs **Manual** (this PDF; steps link to their page),
**Steps** (checklist), **Files** (source files, *Download all* as zip) and **Check quiz**.
