---
name: package
description: >-
  Build, check and update SemiTec Learning Packages (.stlp) — the signed course files students add to the
  SemiTec Academy desktop app. A package bundles trainings, labs, readings (PDF or Markdown), videos and
  other materials described in one pack-spec.json. Use when someone wants to create, package, publish,
  update or check a course / learning package for SemiTec Academy, add a study plan (weeks) or a diploma
  project to one, or asks what the app can show.
---

# package — SemiTec Learning Packages

You build **SemiTec Learning Packages** (`.stlp`) for the **SemiTec Academy** desktop app. A package is
one signed file; students add it to the app and get every material in sections (Trainings, Labs,
Readings, Videos, Other materials), with progress saved per student.

```
materials (anywhere) → pack-spec.json → stlp check (fix until 0 errors) → stlp create → <id>-<version>.stlp
```

This skill is released together with the app. `scripts/VERSION.json` says which app release it was
built from and which content formats it writes; `CHANGELOG.md` lists what each release added.

## Where files go — ask once, then remember

Destination folders are **never** hard-coded. Before writing anything, resolve them:

1. Look for **`.semitec.json`**, starting in the working folder and searching upward. If it
   exists, use its values and do **not** ask.
2. If it is missing, ask the user for the keys below — one short round — then write
   `.semitec.json` at the root of their project with the answers, so no later run asks again.

| Key | Used for |
|---|---|
| `contentRoot` | the materials a package draws from |
| `packagesRoot` | where `pack-spec.json` folders are created |
| `academyRepo` | optional — a checkout of the Academy repository, for its current `packer/stlp.js` |

Values are paths relative to `.semitec.json`, or absolute. Create folders that do not exist yet.
Never write outside them, and never assume a particular parent layout.

## What a package can contain

| Section in the app | Spec list | Source | Needs app |
|---|---|---|---|
| Trainings | `trainings` | folder made with the web training template (`training.json` + `topics/`) — skill `academy-templates:training` | 1.0 |
| Labs | `labs` | `lab/` folder of a lab made with the lab-manual template (`lab.json`, `manual.pdf`) — skill `academy-templates:lab-manual` | 1.0 |
| Labs with source files | `labs` | same, with `"files": "src"` in `lab.json` (Files tab, zip download) | 1.2 |
| Readings (PDF) | `readings` | `.pdf` file | 1.0 |
| Readings (Markdown) | `readings` | `.md` file + the images / files it links (same folder or below) | 1.3 |
| Videos | `videos` | `.mp4` (H.264 + AAC) / `.webm`, or `url` of an online video | 1.1 |
| Other materials | `materials` | any file — PDF, image, text / code, Markdown, zip … — or a `url` | 1.1 |
| Projects | `projects` | `project/` folder (`project.json` + `brief.pdf`) made from a project brief with `academy-templates:project-brief` (its brief2project tool) | 1.4 |

Optional (app ≥ 1.4, ignored by older apps): **`schedule`** — the study plan in weeks (`entries`: `week` or
`weeks: [from, to]`, `title`, `note`, `items`); or **`plannedWeeks`** on items; **`pack.certificate`** — design
of the course certificate. A training's own topic plan (`schedule` in its `training.json`) is taken over.
Students enroll with a start date and get the plan in their calendar and on the Today panel.

The packer computes the minimum app version from what is used and writes it into the package.
Details: `reference/formats.md`. Markdown rules: `reference/markdown.md`.

## Tools

`scripts/stlp.js` — bundled, needs only Node.js 18+, and works on its own. If `academyRepo` is set, prefer
that checkout's copy, which is always current: `<academyRepo>/packer/stlp.js` (run `npm install` once in
`<academyRepo>/app`). The repository is https://github.com/SemiTecFoundation/semitec-academy.

```bash
node <tools>/stlp.js check   <pack-spec.json>                       # check every material (table: ✓ ⚠ ✗)
node <tools>/stlp.js create  <pack-spec.json> --key <private.pem>   # check → assemble → sign → <spec dir>/dist/*.stlp
node <tools>/stlp.js create  <pack-spec.json> --unsigned            # draft (installs only with Developer mode on)
node <tools>/stlp.js inspect <file.stlp>                            # contents, signature, minimum app version
```

## Workflow

### 1. Collect
Ask in one short round (skip what is known):
- **Package**: title, one-sentence description, language, audience, publisher (default *SemiTec
  Foundation*) and its **logo** (`pack.publisherLogo`, square SVG / PNG - companies other than the
  Foundation publish packages too), authors, id (propose `org.semitec.<kebab-title>`), version (`1.0.0` for a new package),
  cover image (optional).
- **Materials per section** — names and where they are. If only names are given, search `contentRoot`
  (topic folders such as `IC-Design/Digital-Design/FPGA/{lectures,trainings,labs,projects,videos,materials}`)
  and confirm the matches. Materials from different topics may be combined. If `contentRoot` has an
  `INVENTORY.md`, it lists everything.
- **Course order** (optional): modules such as *Week 1: training A, video B, lab 1*.
- **Study plan** (recommended): how many weeks, and what belongs to each week → `"schedule"`. If the
  author only knows a length per item, use `"plannedWeeks"`. No plan = self-paced.
- **Materials of a lab** (starter files, constraints, report template): give them `"for": "<lab id>"` so the
  app shows them under the lab and in its Materials tab, not as separate rows after it. Attached items are
  **not counted** in the package progress (app ≥ 1.6.0).
- **Prerequisites** (optional): refreshers for what the course assumes — e.g. a *0-level* training on memories
  or digital logic before an MBIST course. Add them like any item with `"prerequisite": true`. The app shows
  them first (*Before you start — prerequisites*) and does **not** count them in progress, *in progress* status
  or the certificate; leave them out of the `"schedule"`. A prerequisite cannot also have `"for"`.
- **Projects** (optional): briefs to include → run `brief2project.py` on each brief folder (skill
  `academy-templates:project-brief`) and list the `project/` folders under `"projects"`.
- **Signing**: the private key for releases; for drafts the development key
  the offline production key `semitec-foundation.key.pem` (kept outside every repository, ask the
  Foundation for it) — otherwise `--unsigned`, which installs with *Developer mode* on.

### 2. Write `pack-spec.json`
Put it in `<packagesRoot>/<package-name>/`. If that folder has a `README.md` listing the packages, add a
row. Sample specs live in the Academy repository under `packs/`
(https://github.com/SemiTecFoundation/semitec-academy/tree/main/packs). Paths in a spec are relative to the
spec file; materials stay where they are. Start from `examples/pack-spec.json`; format:
`reference/pack-spec.md`. Ids: lowercase-with-dashes, unique in the package, never changed later
(progress is stored per id). Give every item a title, a one-line description and `estimatedTime`.

### 3. Check and fix
Run `check`. One row per material: ✓ / ⚠ / ✗ plus what was found (topics, steps, files, size, kind).
- Fix mechanical problems yourself: paths, titles, duplicate ids, `review` links to wrong ids, an online
  video given as `source` instead of `url`, Markdown images outside the document's folder (move them).
- Missing or incomplete materials are made with the other skills: a training → `academy-templates:training`;
  a lab (manual + steps + quiz + source files, or a lab that exists only as PDF) → `academy-templates:lab-manual`;
  a project brief → `academy-templates:project-brief`. Do not rewrite trainings or labs here — report problems.
- Ask the user when content or a decision is missing (unsupported video codec → convert to MP4 H.264).
Repeat until **0 errors**; mention the warnings that remain.

### 4. Create
Run `create` with the key (or `--unsigned` for a draft), then `inspect` the result.

### 4b. Publish (optional)
For the app's **Catalog**: put the `.stlp` in a shared folder, or run `node <tools>/stlp.js catalog <folder>
--name "<publisher>"` and upload the folder with `catalog.json` to a website; students add the folder or the
link in *Settings -> Application -> Catalog sources*.

### 4c. Keep the inventory
If `contentRoot` has `tools/inventory.py`, run `python3 <contentRoot>/tools/inventory.py` — it records
which package uses which material and lists materials not packaged yet. Skip this step when the script
is not there.

### 5. Report
The `.stlp` path and size, the minimum SemiTec Academy version, the items per section, remaining
warnings, and how students add it: **＋ Add course pack**, drag and drop onto the window, or double-click.
For an update: same `id`, higher `version` — students add the new file and keep their progress.

## Rules
- Never put private keys into the package folder or the spec, never print key contents.
- Do not change materials outside the package folder unless the user asks.
- `pack.id` never changes; raise `version` for every shared update (`1.0.0 → 1.0.1` fixes, `→ 1.1.0` new items).
- Videos: 720p MP4 (H.264 + AAC), under ~300 MB each; long lectures as online links.
- Markdown readings: GitHub-flavoured Markdown; images in the same folder or below; no scripts.
- Study plan: every week block should be realistic (sum of `estimatedTime`); every non-project item in some
  week; keep item ids stable — enrolled students' dates and progress follow the ids.

## Files
- `README.md` — what the skill is and supports · `CHANGELOG.md` — releases
- `reference/pack-spec.md` · `reference/formats.md` · `reference/markdown.md` · `reference/lab-json.md`
- `examples/pack-spec.json` (all sections + modules) · `examples/minimal-pack-spec.json`
  · `examples/markdown-reading/` (a Markdown reading with an image)
- `scripts/` — bundled `stlp` + `VERSION.json`

## Academy Templates
Part of the **Academy Templates** plugin: `academy-templates:project-brief` (project brief PDF) ·
`academy-templates:diploma-project` (thesis PDF) · `academy-templates:lab-manual` (lab manual PDF + app lab) ·
`academy-templates:training` (interactive web training) · `academy-templates:package` (`.stlp` for SemiTec
Academy). Hand over to the matching skill when the user needs one of those outputs.
