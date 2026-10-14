# Academy Templates

**Academy Templates** is the SemiTec Foundation's set of templates for course and research material,
packaged as one **Claude Code plugin** (`academy-templates`) with **one skill per template**.
Each skill is a folder with the template files, the tools that build and check them, and a `SKILL.md`
that tells an AI assistant how to do the whole job — interview the author, write, build, check.
Every template also works by hand, without AI.

```
                    ┌──────────────── PDF ─────────────────┐   ┌──── Web ────┐
 supervisor ──────► │ project-brief    task definition PDF │   │             │
 student ─────────► │ diploma-project  thesis PDF + slides │   │             │
 lecturer ────────► │ lab-manual       manual PDF + lab/ ──┼─┐ │ training ───┼─┐  interactive HTML training
                    └──────────────────────────────────────┘ │ └─────────────┘ │
                       PDFs, Markdown, videos, files ────────┼─────────────────┤
                                                             ▼                 ▼
                                    package   pack-spec.json → check → signed .stlp ─► SemiTec Academy app
```

## The skills

| Skill in Claude Code | Alone (Claude app) | Family | For | Makes | Needs |
|---|---|---|---|---|---|
| [`academy-templates:project-brief`](skills/project-brief/README.md) | `academy-project-brief` | PDF | supervisors, industry mentors | the **brief (task definition, առաջադրանք)** of a diploma / thesis / research project: goals, scope, learning path, warm-up, 30-week plan, rubric; one student or a cross-department pair; + platform topic record (JSON) | XeLaTeX |
| [`academy-templates:diploma-project`](skills/diploma-project/README.md) | `academy-diploma-project` | PDF | students | the **final diploma / thesis document** (and defense-slides outline), Latin or Armenian | pdfLaTeX / XeLaTeX |
| [`academy-templates:lab-manual`](skills/lab-manual/README.md) | `academy-lab-manual` | PDF + app | lecturers | a **lab manual PDF** and the matching **app lab** (`lab.json` steps + check quiz, source files) | XeLaTeX, Python 3 |
| [`academy-templates:training`](skills/training/README.md) | `academy-training` | Web | lecturers | an **interactive web training**: topics, interactive blocks, quizzes that unlock topics, certificate; standalone / preview / platform modes | Python 3 |
| [`academy-templates:package`](skills/package/README.md) | `academy-package` | Package | course authors | a **SemiTec Learning Package** (`.stlp`) for the [SemiTec Academy](https://github.com/SemiTecFoundation/semitec-academy#readme) app from trainings, labs, PDF / Markdown readings, videos, files, projects — with a week-by-week **study plan** | Node.js 18+ |

All PDF templates support **English, Armenian (reformed) and Armenian (classical)** (diploma-project:
Latin template + Armenian XeLaTeX variant). Ask in plain words — the right skill is chosen from its
description:

- *"Define a bachelor diploma topic on a JTAG-based memory test for two students"* → `project-brief`
- *"Help me write my thesis from these notes, in Armenian"* → `diploma-project`
- *"Make Lab 3 (UART transmitter) with a manual, steps, a quiz and starter files"* → `lab-manual`
- *"Turn my FSM lecture into an interactive training with a quiz per topic"* → `training`
- *"Package trainings 1–2, labs 1–3 and the Markdown notes as the course 'Digital Design 1'"* → `package`

**Which family?** Signed, printed, archived or submitted → **PDF**. Clicked through, practised,
self-checked → **Web**. Handed to students as one course file for the desktop app → **Package**
(it bundles the outputs of the other skills).

## Install

**Claude Code — as a plugin (recommended).** The folder above this one is a plugin marketplace called
`semitec-skills`; add it from GitHub, or from a local clone by path:

```text
/plugin marketplace add https://github.com/SemiTecFoundation/semitec-academy-skills
/plugin install academy-templates@semitec-skills
```

Then `/skills` lists `academy-templates:project-brief` … `academy-templates:package`.
After a change: raise `version` in `.claude-plugin/plugin.json` and run `/plugin marketplace update semitec-skills`.
To try changes without installing: `claude --plugin-dir <path>/AcademyTemplates` (edits are live).

**Claude Code — skills only (no plugin).** `python3 tools/skills.py install` copies each skill as
`academy-<name>` to `~/.claude/skills/` (`--project DIR` → `DIR/.claude/skills/`).

**Claude app (desktop / web).** Upload `dist/academy-<name>.zip` in Settings → Skills — one zip per skill,
each self-contained (the package zip includes its packer).

**Without AI.** Open the skill's `README.md`: copy the template, fill it in, run its build / check tools.

## Tools and scripts

| Tool | Where | What it does |
|---|---|---|
| `tools/skills.py` | plugin | `list` the skills · `check` frontmatter, files named in SKILL.md, READMEs, plugin manifest, zips · `zip` → `dist/` · `install` (stand-alone) · `plugin` (install commands) |
| `latexmk -xelatex main.tex` | project-brief, lab-manual, diploma-project (Armenian) | compile a document (Biber, glossaries via `.latexmkrc`); `latexmk -pdf` for the Latin diploma template |
| `skills/project-brief/tools/brief2project.py <brief>` | project-brief | brief → `project/` (project.json + brief.pdf) for SemiTec Academy: weekly plan, milestones, deliverables, rubric, learning path |
| `skills/lab-manual/tools/build.py <lab>` | lab-manual | compile the manual → copy to `lab/manual.pdf` → write each step's manual page into `lab.json` → check |
| `skills/lab-manual/tools/check_lab.py <lab>` | lab-manual | check `lab.json`, source files, quiz, manual, and that manual and app steps match |
| `skills/training/tools/validate.py [folder]` | training | check JSON, ids, block and question types, review links, answers, referenced files |
| `skills/training/tools/build_single_file.py` | training | one self-contained HTML (`dist/training.html`, `dist/training-preview.html`) |
| `skills/training/tools/dev_server.py` | training | local server + demo progress API (the reference for platform integration) |
| `skills/package/scripts/stlp.js` | package | `check` / `create` / `inspect` SemiTec Learning Packages — bundled copy of the Academy repository's `packer/stlp.js` (https://github.com/SemiTecFoundation/semitec-academy), regenerate with `bundle-skill` |

## Folder

```
AcademyTemplates/
├── .claude-plugin/plugin.json      plugin manifest (name academy-templates, version)
├── README.md                       ← you are here
├── CHANGELOG.md                    plugin releases
├── docs/
│   ├── CONVENTIONS.md              shared look and technology (PDF, web), languages, folder rules
│   ├── ADDING-A-TEMPLATE.md        how to add a new template / skill
│   └── ROADMAP.md                  planned templates and skill features
├── skills/
│   ├── project-brief/              SKILL.md · README · latex/ · reference/ · templates/ · examples/ · sample-output-*.pdf
│   ├── diploma-project/            SKILL.md · README · latex/ · slides/ · reference/ · templates/ · examples/ · sample-output.pdf
│   ├── lab-manual/                 SKILL.md · README · latex/ · lab/ · tools/ · reference/ · examples/ · sample-output-*.pdf
│   ├── training/                   SKILL.md · README · INTEGRATION.md · engine (index.html, js/, css/) · content (training.json, topics/, assets/) · tools/ · dist/ · examples/
│   └── package/                    SKILL.md · README · CHANGELOG · ROADMAP · reference/ · examples/ · scripts/ (bundled stlp)
├── tools/skills.py                 maintenance and install
└── dist/academy-<name>.zip         generated, for the Claude app
```

## Versions

- The **plugin** has one version (`.claude-plugin/plugin.json`, history in `CHANGELOG.md`).
- The **package** skill also follows the SemiTec Academy app: its `CHANGELOG.md` and
  `scripts/VERSION.json` say which app release and content formats it supports.
- The **training** skill's engine is copied into the app (https://github.com/SemiTecFoundation/semitec-academy, `npm run sync-engine` in `app/`).

Release checklist: update the skill → `python3 tools/skills.py zip` → `python3 tools/skills.py check`
(0 errors) → raise the plugin version and add a `CHANGELOG.md` entry.

## Destination folders — `.semitec.json`

The `training`, `lab-manual`, `project-brief` and `package` skills never hard-code where your files go.
On first use they look for **`.semitec.json`**, searching from the working folder upward; if it is not
there they ask you once and write it, so later runs stay quiet. Create it yourself to skip the question:

```json
{
  "contentRoot":  "LearningMaterials",
  "packagesRoot": "LearningMaterials/Packages",
  "briefsRoot":   "Briefs",
  "academyRepo":  "../semitec-academy"
}
```

| Key | Used by | Meaning |
|---|---|---|
| `contentRoot` | training, lab-manual, project-brief, package | where course materials live — trainings, labs and projects are created under `<contentRoot>/<topic>/` |
| `packagesRoot` | package | where `pack-spec.json` folders are created |
| `briefsRoot` | project-brief | optional — where finished briefs are collected, if you keep them apart from the course content |
| `academyRepo` | package | optional — a checkout of [semitec-academy](https://github.com/SemiTecFoundation/semitec-academy), so the skill can use its current `packer/stlp.js` instead of the bundled copy |

Paths are relative to `.semitec.json` itself, or absolute. Only the keys a skill needs have to be
present. `diploma-project` writes wherever you tell it and needs no configuration.

