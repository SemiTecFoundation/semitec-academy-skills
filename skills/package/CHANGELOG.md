# Changelog — package skill (SemiTec Learning Packages)

The skill is released with the SemiTec Academy app; the release number is the app version it was
built from (see `scripts/VERSION.json`). Packages made with an older skill keep opening in newer apps.

## 1.6.2
- Bundled packer rebuilt from SemiTec Academy 1.6.2.
- Signing: releases use the offline **production** key; the app trusts no development key, so a
  draft is built with `--unsigned` and installs only with *Developer mode* on.
- `prerequisite` documented in `reference/pack-spec.md` and `reference/formats.md`.
- Destination folders come from `.semitec.json` (`contentRoot`, `packagesRoot`, `academyRepo`).

## 1.6.0
- **Prerequisites**: `"prerequisite": true` on any item — an optional refresher shown before the course,
  not counted in progress, *in progress* status or the certificate, and not planned; checked (not with
  `for`, at least one counted item, warning when listed in the schedule).
- **Attached materials (`for`) no longer count** in the package progress or certificate.
- Bundled packer from SemiTec Academy 1.6.0.

## 1.5.0
- **Publisher logo**: `pack.publisherLogo` (+ `publisherUrl`); `check` warns when it is missing.
- **`"for"`**: attach an item (usually a material) to a lab / training / project; checked; attached items
  need no week in the schedule.
- **Project `category`** (research, diploma, thesis, course-project, capstone, internship, other).
- **`stlp catalog <folder>`**: writes `catalog.json` + `catalog-assets/` for publishing on a website.
- Bundled packer from SemiTec Academy 1.5.0.

## 1.4.0
- **Projects** (item type `project`, format 1, app ≥ 1.4.0): `"projects": [{ "id", "source": "<brief>/project" }]`,
  made with `academy-templates:project-brief` → `tools/brief2project.py`; checked (weekly plan, milestones,
  deliverables, brief PDF).
- **Study plans:** `"schedule"` (weeks → items) and `"plannedWeeks"` on items; a training's own topic plan
  (`schedule` in `training.json`) is copied into the package. `check` prints the plan length and warns
  about items without a week.
- **Course certificate:** `pack.certificate` (certificate.json design).
- Bundled packer from SemiTec Academy 1.4.0 (`scripts/lib/schedule.js` added).

## 1.3.0
- App renamed **SemiTec Academy**; packages are **SemiTec Learning Packages** with the extension **`.stlp`**
  (was `.stp`, which clashes with STEP CAD files); the tool is `stlp.js`.
- **Markdown readings** (reading format 2): `.md` + images, checked for broken / outside links; also
  Markdown as an *other material*.
- Skill moved into the Academy Templates plugin (`Products/Skills/AcademyTemplates/skills/package`) as
  `academy-templates:package` (was `semitec-learning-package`);
  app and packer moved to `Products/Academy`.

## 1.2.0
- **Lab source files** (lab format 2): `"files"` in `lab.json`, step links to files; checked and packed.
- Lab-manual template + skill produce the `lab/` folder (manual, steps, quiz, source files).

## 1.1.0
- **Pack spec** (`pack-spec.json`) with `check` and `create`.
- **Videos** and **other materials**; pack page in sections; course-order modules.

## 1.0.0
- First release: trainings, labs, PDF readings; signed packages; local accounts and progress.
