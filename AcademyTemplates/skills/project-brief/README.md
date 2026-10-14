# project-brief — template for defining student projects

For **supervisors and industry mentors** who define a diploma / thesis /
research project for students. The brief (task definition, առաջադրանք) tells
the student what the project is, **what to learn, how to get started, what to
do, by when, and how it will be assessed**.

(For the student's *final* diploma document, use `../diploma-project`.)

## With an AI agent (recommended)
Use the skill `academy-templates:project-brief` (Claude Code plugin) or upload
`dist/academy-project-brief.zip` in the Claude app (see `../../README.md`), then say e.g.
*"Help me define a bachelor diploma topic on …"*. The agent follows `SKILL.md`:
1. asks the language (English / Armenian reformed / Armenian classical) and the mode (one student / cross-department pair);
2. interviews you in short batches (`reference/interview.md`);
3. shows you a one-page skeleton to approve;
4. writes the brief, builds the PDF, runs the quality checklist;
5. gives you the PDF, the LaTeX source and a platform topic record.

## By hand
1. Copy `latex/` to a new folder.
2. In `main.tex`, choose `english`, `armenian` or `armenian-classical`.
3. Fill `metadata.tex` and the chapters in `sections/`. The comments at the top of each file say what to write.
4. Build: `latexmk -xelatex main.tex`, or use Overleaf with the XeLaTeX compiler.

Red **[ … ]** markers show what is still missing.

## What is in a brief
Topic-at-a-glance card · context · problem & idea · goals · scope & MVP ·
technical description · roles & tasks · **learning path** · **getting started
(warm-up exercises)** · work plan · deliverables · **assessment rubric** · demo ·
extensions · supervision & risks · reading list · glossary · approval.

Single-student and cross-department (two students, two departments) modes
switch automatically from `metadata.tex`.

See `reference/commands.md` for all commands, and `examples/` for a complete brief.

## For SemiTec Academy
`python3 tools/brief2project.py <brief-folder>` makes `project/` (project.json + brief.pdf): students
enroll in the project in the app, get the weekly plan in their calendar, tick weeks and keep notes.
Add the folder to a package with the package skill (`"projects"` in the pack spec). See
`reference/app-project.md`.
