# Content types, formats and app versions

Every item in a package has a **type** and a **format number**. Each SemiTec Academy release can open a
set of formats; the packer writes the formats it used and the minimum app version into the package.

| Type | Format | What it is | SemiTec Academy |
|---|---|---|---|
| package container | 1 | zip: `manifest.json` (+ SHA-256 per file), `signature.json` (Ed25519), `content/` | ≥ 1.0.0 |
| training | 1 | training-template JSON (`training.json`, `topics/`, `assets/`, `certificate.json`) | ≥ 1.0.0 |
| lab | 1 | `lab.json` (steps, quiz) + `manual.pdf` | ≥ 1.0.0 |
| lab | 2 | lab format 1 + source files (`"files"`) | ≥ 1.2.0 |
| reading | 1 | PDF | ≥ 1.0.0 |
| reading | 2 | Markdown document + its images / linked files | ≥ 1.3.0 |
| video | 1 | MP4 / WebM file, or online link | ≥ 1.1.0 |
| material | 1 | any file (kind: pdf, image, text, markdown, video, file) or link | ≥ 1.1.0 (Markdown view ≥ 1.3.0; older apps offer the file for saving) |
| project | 1 | `project.json` (weekly plan, milestones, deliverables, rubric, learning path) + `brief.pdf` — from the project-brief template | ≥ 1.4.0 |

**Optional additions (no new format, older apps ignore them):** `publisherLogo` / `publisherUrl`,
`for` (item attached to a lab, app 1.5.0+), project `category`; `schedule` (package study plan),
`plannedWeeks` on items, a training's own topic plan (`schedule` in `training.json`), `certificate`
(course certificate design). SemiTec Academy ≥ 1.4.0 uses them for enrollment, the calendar, the Today
panel and the course certificate.

The packer chooses the format from the content: a lab without `files` stays format 1, a PDF reading
stays format 1 — so packages open in the oldest app that can show them. `stlp create --target-app 1.2.0`
refuses to build when a material needs a newer app.

The authoritative table is `app/src/shared/versions.js` in the Academy repository (https://github.com/SemiTecFoundation/semitec-academy) (copied into
`scripts/lib/versions.js` of this skill).
