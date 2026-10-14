---
name: training
description: >-
  Create an interactive web training (HTML, works offline): topics with subsections, interactive blocks
  (scroll-and-learn, accordions, tabs, zoom, hotspots, animations, drag and drop), a quiz per topic that
  unlocks the next one, a certificate, themes and layouts — all content in JSON. Use when a lecturer wants
  to build, update or translate a training, tutorial, interactive lesson or self-paced course module.
---

# SKILL — creating a training with AI

Instructions for an AI assistant (or a person) who builds a new training from this template.
Read `reference/content-format.md` for every field.

## Workflow

1. **Copy** the whole `training/` skill folder (engine + example content) to `Foundation/Products/LearningMaterials/<topic>/trainings/<topic>-<name>/` (e.g. `IC-Design/Digital-Design/FPGA/trainings/fpga-vivado-flow`; or where the user wants). Use a **last-level** topic (one without sub-topics); if its material folders do not exist yet, run `python3 Foundation/Products/LearningMaterials/tools/inventory.py --init <topic>` first.
2. **`training.json`** — set a new `id` (progress is stored per id), `title`, `subtitle`, `language`, `hours`, `passThreshold`, default `layout` and `theme`; list the topic files in order. For Armenian / Russian set `language` and translate the UI strings in `labels`.
3. **Topics** — delete the demo files in `topics/` and write one JSON file per topic (`01-intro.json`, `02-…`). For every topic:
   - 2–5 subsections, each with a stable `id` (kebab-case) and a few blocks;
   - use an interactive block where it helps understanding (process → `scrolly`/`stepper`, picture with parts → `reveal`, alternatives → `tabs`, details → `accordion`, classification → `categorize`, sequence → `sort`);
   - a quiz of 3–8 questions; mix types; **every question has `review`** pointing to the subsection(s) that teach the answer; use `multiple` when more than one answer is right.
4. **Assets** — put pictures and SVGs in `assets/`. SVG rules: `viewBox` set, own white background `<rect>`, ids prefixed per file (e.g. `sr-arrow`), `data-step` / `data-until` for step animations, CSS `@keyframes` inside `<style>` for continuous animation.
5. **`certificate.json`** — issuer, signatures, texts, `style` (design, font, colours).
6. **Theme** (optional) — copy `css/themes/foundation.css` to a new name, change variables only, add the name to `themes`.
7. **Validate** — `python3 tools/validate.py` must report 0 errors.
8. **Preview** — `python3 -m http.server` in the folder → <http://localhost:8000>.
9. **Preview & certificate style** — open `index.html?mode=preview`: every topic is open and the
   *Certificate* page shows a sample certificate with design / font / colour controls. Copy the
   generated `"style"` JSON into `certificate.json`, or describe the change to the AI.
10. **Bundle** — `python3 tools/build_single_file.py` → `dist/training.html` (standalone, for students)
    and `dist/training-preview.html` (all open, for reviewers). Both work by double-click.
11. **Platform** — to run inside a portal with a database, follow `INTEGRATION.md` (do not change the JS).

## Rules

- Do **not** edit `js/` or `css/app.css` for content or look — only JSON, assets and theme files.
- Keep ids stable after publishing: progress and review links use them.
- Correct-answer indices start at 0. `order` items and `sort` items are written in the **correct** order (the app shuffles them).
- `single`/`truefalse` have exactly one correct index; otherwise use `multiple`.
- Hotspot coordinates are percent of the picture (`x = px / viewBoxWidth * 100`). The number badge sits on the
  spot's top-left corner: keep labels away from it or set `"badge": "tr" | "bl" | "br"`.
- Pictures: `reveal` shows the picture full width with the explanation under it; `scrolly` gives the picture
  about two thirds of the width — draw SVGs with large text (≥ 13 px at a 760 px viewBox) so they stay readable.
  `stepper` controls sit under the picture and do not move; keep each step text to 1–3 sentences.
- Each subsection is **one page** (the student scrolls inside it and presses Next): keep it to 2–4 minutes of reading
  and give it a clear title — the title is shown on the Next button and in the review links.
- Set `version` in `training.json` when you publish changed content.

## Example prompts

- *"Create a new topic `topics/<nn>-ecc.json` about Hamming SECDED codes: 3 subsections (why ECC, encoding with a stepper animation of check-bit calculation, decoding and syndrome with a reveal picture), and a 6-question quiz with review links."*
- *"Translate all topics and UI labels to Armenian, keep ids unchanged."*
- *"Add a theme `ocean.css`: teal accent, dark-blue header, 16px radius. Make it the default."*
- *"Change the certificate to the modern design, sans font, accent #0b5d5b, signatures: …"*
- *"Make topic 4 easier: add a flip-card summary at the end and lower its quiz threshold to 0.6."*
- *"Make the certificate portrait, minimal design, add a third signature for the department head."*
- *"Prepare this training for our platform: platform mode, no URL parameters, progress via REST at `/api/progress/{trainingId}/me`."*

## Study plan (optional)
If the author says how long the training takes in weeks, add `"schedule"` to `training.json`: the number
of weeks and which topics belong to each week (topic ids). `python3 tools/validate.py` checks it.
SemiTec Academy maps the weeks onto the student's calendar from the day they enroll.

## Use in SemiTec Academy

A finished training folder can be put into a SemiTec Learning Package (`.stlp`) for the desktop app with the
`academy-templates:package` skill (`AcademyTemplates/skills/package`): add it to `"trainings"` in the pack spec with the
path of this folder. The app brings its own engine — only `training.json`, `topics/`, `assets/`,
`certificate.json` (and custom themes) are packed; progress and quizzes are saved per student.

## Academy Templates
Part of the **Academy Templates** plugin: `academy-templates:project-brief` (project brief PDF) ·
`academy-templates:diploma-project` (thesis PDF) · `academy-templates:lab-manual` (lab manual PDF + app lab) ·
`academy-templates:training` (interactive web training) · `academy-templates:package` (`.stlp` for SemiTec
Academy). Hand over to the matching skill when the user needs one of those outputs.
