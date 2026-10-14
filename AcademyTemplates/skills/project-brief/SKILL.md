---
name: project-brief
description: >-
  Help a supervisor, lecturer or industry mentor define a student project — a
  diploma / thesis / research-project BRIEF (task definition, առաջադրանք) that
  tells the student what the project is, what to learn, how to get started, what
  to do, by when, and how it will be assessed. Produces a compiled PDF (LaTeX,
  XeLaTeX) in English, Armenian (reformed spelling) or Armenian (classical
  spelling), single-student or cross-department (two students), plus a platform
  topic record (JSON). Trigger on "define a diploma topic", "project brief",
  "task definition", "առաջադրանք", "thesis topic for students", "post a research
  topic". NOT for writing the student's final diploma (use diploma-project).
---

# Project Brief / Task Definition Template

A **brief** is written by the *supervisor* (or an industry employee acting as
mentor) **before** the student starts. It is the student's map of the project:

| The brief answers | Chapter |
|---|---|
| Why does this project exist? | 1 Context · 2 Problem and idea |
| What exactly must be achieved? | 3 Goals · 4 Scope & MVP · 5 Technical description |
| Who does what? | 6 Roles and tasks (per student in cross-department mode) |
| What must I learn, to what level, from where? | 7 Learning path |
| How do I start in the first weeks? | 8 Getting started (setup + warm-up exercises) |
| When is what due? | 9 Work plan and milestones · 10 Deliverables |
| How will I be judged? | 11 Assessment rubric |
| What will the final demo look like? What else could I do? | 12 Demo · 13 Extensions |
| Who helps me, and what could go wrong? | 14 Supervision and risks |

The student's *final* diploma document is a different template (`../diploma-project`).

## Where files go — ask once, then remember

Destination folders are **never** hard-coded. Before writing anything, resolve them:

1. Look for **`.semitec.json`**, starting in the working folder and searching upward. If it
   exists, use its values and do **not** ask.
2. If it is missing, ask the user for the keys below — one short round — then write
   `.semitec.json` at the root of their project with the answers, so no later run asks again.

| Key | Used for |
|---|---|
| `contentRoot` | where course materials live; projects go to `<contentRoot>/<topic>/projects/` |
| `briefsRoot` | optional — where finished briefs are collected, if the user keeps them apart |

Values are paths relative to `.semitec.json`, or absolute. Create folders that do not exist yet.
Never write outside them, and never assume a particular parent layout.

## Package contents

```
project-brief/
  SKILL.md                  ← this file: the workflow for the AI agent
  README.md                 ← quick start for humans
  latex/                    ← the compilable template (XeLaTeX + Biber)
    main.tex                  chapter order + language option
    briefstyle.sty            style + all custom commands
    lang/brief-lang-*.tex     fixed words: english · armenian · armenian-classical
    metadata.tex              title, people, platform fields
    sections/01…14-*.tex      one chapter per file, guidance in the comments
    references.bib  abbreviations.tex  glossary.tex  diagrams/  images/
  reference/
    interview.md              questions to ask the supervisor (what to collect)
    section-guide.md          what each chapter must contain + good/bad examples
    languages.md              choosing the language; reformed vs classical spelling
    commands.md               LaTeX command reference
    quality-checklist.md      review before publishing
    platform-mapping.md       brief → platform research_topics record
    app-project.md            brief → SemiTec Academy project (project.json)
  tools/
    brief2project.py          brief → project/project.json + brief.pdf for SemiTec Academy
  templates/
    brief-template.md         Markdown skeleton (for Word / Docs output)
    topic-record.json         platform record skeleton
  examples/
    fpga-sensor-platform-hy/  full cross-department example, Armenian (reformed)
  sample-output-*.pdf       the empty template compiled in each language
```

## Workflow (follow in order)

### Step 1 — Settle the setup (ask; never assume)
Ask the author **before drafting**:
1. **Language of the brief:** `english`, `armenian` (reformed spelling) or
   `armenian-classical`. Do not guess the Armenian spelling from the author's
   name or the institution: ask. Then write the **whole** text in that spelling
   (see `reference/languages.md`). Technical terms (FPGA, AXI, API, RTL) stay in Latin.
2. **Mode:** single student, or cross-department (two students from different
   departments sharing one system, each with an independent diploma).
3. **Output:** PDF via LaTeX (default), or Word / a Claude doc via
   `templates/brief-template.md`. Same chapters either way.

### Step 2 — Interview the author
Use `reference/interview.md`. Ask in **small batches** (3–5 questions per
message), starting with the essentials (idea, goals, student profile, equipment,
duration). Accept rough answers and notes in any language. If the author gives a
document, an email or an old brief, extract answers from it first and ask only
for what is missing.

### Step 3 — Propose the skeleton for approval
Before writing full chapters, send the author a short plan: title (+ title in
the second language), 3–6 goals, MVP vs out of scope, the task list per
student, the main learning topics, and the milestone outline. Iterate until
they agree. This prevents rewriting long LaTeX later.

### Step 4 — Write the brief
- Copy `latex/` to a new folder named after the topic. Set the language option
  in `main.tex`, fill `metadata.tex`, and write each `sections/NN-*.tex`.
- Follow `reference/section-guide.md` for each chapter. Use the custom
  environments (`tasklist`, `learningpath`, `warmup`, `workplan`, `deliverables`,
  `rubric`, `risks`, `interfaces`); see `reference/commands.md`.
- **The learning path is the most valuable part for students.** Every row needs
  a concrete resource (book chapter, vendor tutorial, course module, paper) in
  `references.bib`. Use well-known sources and **verify that they exist**. If you
  are unsure of an exact edition, URL or chapter, mark it `\missing{verify}`
  instead of inventing it.
- Anything the author has not supplied stays as `\missing{...}` (printed in red).
  **Never invent** names, dates, equipment, partner companies or grading rules.
- Draw the architecture as TikZ in `diagrams/` (copy the style of the example).
- Delete chapters 12–14 only if the author says so; they are short and useful.

### Step 5 — Build and check
- Build: `latexmk -xelatex main.tex` (XeLaTeX + Biber; fonts: FreeSerif family,
  included in TeX Live / MacTeX / Overleaf).
- Run `reference/quality-checklist.md`. In particular:
  `grep -rn '\\missing' sections metadata.tex` must be empty for a final version,
  or the remaining items must be listed for the author.
- Render a couple of pages to an image and check the layout.

### Step 6 — Hand over
- Give the author the PDF and the source folder.
- Produce the platform topic record (`templates/topic-record.json`, mapping in
  `reference/platform-mapping.md`) so the topic can be posted.
- For students in **SemiTec Academy**: run `python3 <skill>/tools/brief2project.py <brief-folder>` → writes
  `<brief-folder>/project/` (`project.json` with the weekly plan from the progress tracker, milestones,
  deliverables, rubric, learning path, goals; `brief.pdf`). Fix what it reports (placeholders, missing
  tracker rows), then add the folder to a package with `academy-templates:package` (`"projects"`).
  Students enroll with a start date and get the 30-week plan in their calendar. Details:
  `reference/app-project.md`.
- Tell the author which `\missing` items remain and which sources to double-check.

## Rules
- The brief is a **contract with a student**: specific, finite and checkable.
  Prefer "implement a 16-tap FIR filter and measure its frequency response" over
  "study digital filters".
- Size it for the degree level: a bachelor MVP should fit in about 60–70% of the
  available time. Say so if the author's scope is too large, and propose what to
  move to Extensions.
- In cross-department mode, each student's part must be a **complete, defensible
  diploma for their own department**; the `interfaces` table must let them work
  in parallel.
- Keep the author's voice and decisions; the agent structures and completes, it
  does not redefine the project.

## Academy Templates
Part of the **Academy Templates** plugin: `academy-templates:project-brief` (project brief PDF) ·
`academy-templates:diploma-project` (thesis PDF) · `academy-templates:lab-manual` (lab manual PDF + app lab) ·
`academy-templates:training` (interactive web training) · `academy-templates:package` (`.stlp` for SemiTec
Academy). Hand over to the matching skill when the user needs one of those outputs.

## Where new material goes
Course content lives in `<content>/<topic>/`, where `<content>` is `contentRoot` (see *Where files go*) — e.g.
`IC-Design/Digital-Design/Verification/projects/verif-<name>/` (the brief's LaTeX + `project/` from
brief2project.py). If `briefsRoot` is set, finished briefs are collected there instead of under the
topic.
Folder names are `<topic>-<short-name>` (they become ids in packages). Use a **last-level** topic (one
without sub-topics). Where `<content>/tools/inventory.py` exists, run it with `--init <topic>` first if
the topic's folders are missing, and again after adding material; skip this when the script is absent.
