# package — SemiTec Learning Packages (`.stlp`)

Builds **SemiTec Learning Packages** (`.stlp`): one signed file per course that students add to the
**SemiTec Academy** desktop app (https://github.com/SemiTecFoundation/semitec-academy). A package can hold any number of
trainings, labs, readings, videos and other materials; the app shows them in sections, tracks each
student's progress and verifies which trusted publisher signed the file and that it was not changed.

Use this skill only for **Academy delivery**. Labs, trainings, project briefs and diploma documents are
complete standalone results already; packaging copies selected materials into one course archive and does
not replace their original folders.

The skill is versioned **with the app**: each app release that adds a content type or format gets a new
skill release (see [`CHANGELOG.md`](CHANGELOG.md) and `scripts/VERSION.json`).

## What it supports (built for Academy 1.8.0)

| Content | From | Shown in SemiTec Academy as | App |
|---|---|---|---|
| Training | web training template (JSON topics, quizzes, certificate) | the interactive training, progress and certificate per student | ≥ 1.0 |
| Lab | lab-manual template (`lab/`: `lab.json`, `manual.pdf`) | tabs *Manual*, *Steps* (checklist), *Check quiz* | ≥ 1.0 |
| Lab source files | `"files"` in `lab.json` | tab *Files*: viewer, *Save file*, *Download all* (zip) | ≥ 1.2 |
| Reading — PDF | any PDF | PDF reader: outline, zoom, resume, pages-read tracking | ≥ 1.0 |
| Reading — Markdown | `.md` + its images | document reader: outline, tables, code with copy, text size, read tracking | ≥ 1.3 |
| Video | `.mp4` / `.webm`, or a link | player with resume and watched tracking; links open in the browser | ≥ 1.1 |
| Other material | any file or link | PDF / image / code / Markdown viewer, *Save a copy*, *Open with default app* | ≥ 1.1 |
| Project | `project/` folder from the project-brief template (`project.json` + brief PDF) | independently tracked advanced work: start a plan, weekly dates, ticks, notes, milestones, deliverables, rubric, brief | ≥ 1.4 |
| Study plan | `schedule` (weeks → items) or `plannedWeeks` on items; topic weeks from a training's `schedule` | enrollment with a start date; *Study plan* view, Calendar, Today panel, reminders | ≥ 1.4 |
| Publisher | `pack.publisher` + `pack.publisherLogo` (+ `publisherUrl`, `contact`) | name and logo on every card; feedback contact in Pack details; filter by publisher | 1.5 / 1.7 |
| Publisher package style | `pack.branding` with `accent`, `accentInk`, optional `accentSoft` | publisher colours on that package's details, labs, projects, readings and materials; Academy shell stays learner-controlled | ≥ 1.8 |
| Materials of a lab | `"for": "<lab id>"` on a material | shown under the lab (course order, study plan) and in the lab's *Materials* tab | 1.5 |
| Project category | `"category"` on a project (research, diploma, thesis, course-project, capstone, internship, other) | category badge and filter on the Projects page | 1.5 |
| Catalog | `stlp catalog <folder>` -> `catalog.json` | the app's Catalog: install / update with one click | 1.5 |
| Course certificate | optional `pack.certificate` → `certificate.json` | publisher certificate after every counted item; omit it for no course certificate | ≥ 1.4 |

Course order (modules), a cover image, package versions (updates keep progress) and signing are
supported for all.

## How it works

```
pack-spec.json ──► stlp check ──► stlp create ──► org.semitec.<name>-<version>.stlp ──► SemiTec Academy
 (list of all       checks every     copies the materials, writes      signed zip: manifest with a
  materials and     material; ✗      the manifest, computes the        SHA-256 of every file +
  their paths)      blocks create    minimum app version, signs        Ed25519 signature
```

1. **pack-spec.json** lists the package (id, version, title …) and the materials by section with their
   paths. Format: [`reference/pack-spec.md`](reference/pack-spec.md).
2. **check** validates each material deeply (training topics and quizzes, lab steps and files, PDF and
   Markdown files, videos, links) and prints a table.
3. **create** builds and signs the package (private key) — or `--unsigned` for a test.

### Publisher styles

A package can carry a small, safe colour-only brand: `accent`, `accentInk` and optional `accentSoft`.
The checker accepts only `#RRGGBB` values and verifies readable button text. It produces package format 2,
which needs Academy 1.8.0. This does not accept arbitrary CSS or change the Academy navigation. Use a
training's own theme file for interactive lesson styling and `certificate.json → style` for certificates.

## Use it

**With Claude Code** — install the Academy Templates plugin (see `../../README.md`); the skill is
`academy-templates:package`. Then ask: *"Make a SemiTec package 'Digital Design 1' with the trainings FSM basics and Timing, labs 1–3
from Labs/dd1, the lecture notes in Lectures/dd1 (Markdown) and the intro video."*

**Other agents** — download the single `AcademyTemplates-<version>.zip` release, then load this
`package/` folder when a course archive is needed. There is no separate package-skill ZIP.

**Without AI** — the same commands by hand:

```bash
node scripts/stlp.js check  my-course/pack-spec.json
node scripts/stlp.js create my-course/pack-spec.json --key /secure/your-publisher.key.pem
```

## Folder

| Path | Content |
|---|---|
| `SKILL.md` | instructions for the AI assistant |
| `CHANGELOG.md` | skill / app releases and what each added |
| `ROADMAP.md` | planned skill features |
| `reference/pack-spec.md` | the spec format and every check |
| `reference/formats.md` | content types, format numbers, app versions |
| `reference/markdown.md` | what Markdown readings support |
| `reference/lab-json.md` | the lab format (made by the lab-manual template) |
| repository `tests/fixtures/package/minimal/` | fictional package used by repository integration tests; it is not shipped to users |
| `scripts/` | bundled packer (`stlp.js`, `lib/`, `fflate`) and `VERSION.json` — regenerate, do not edit |

Regenerate `scripts/` after an app release:
`node <academy>/packer/stlp.js bundle-skill <skills>/skills/package/scripts`, where
`<academy>` and `<skills>` are checkouts of https://github.com/SemiTecFoundation/semitec-academy and
https://github.com/SemiTecFoundation/semitec-academy-skills.
