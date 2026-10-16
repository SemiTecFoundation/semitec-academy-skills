---
name: training
description: >-
  Create an interactive web training (HTML, works offline): topics with subsections, interactive blocks
  (scroll-and-learn, accordions, tabs, zoom, hotspots, animations, drag and drop), a quiz per topic that
  unlocks the next one, a certificate, themes and layouts. The default is Academy JSON content; an explicit
  custom-web format is available for a lesson that needs its own local JavaScript interactions. Use when a
  lecturer wants to build, update or translate a training, tutorial, interactive lesson or self-paced course module.
---

# SKILL — creating a training with AI

Instructions for an AI assistant (or a person) who builds a new training from this template.
Read `reference/content-format.md` for every field.

## Choose the training format

Use **format 1** for nearly all new trainings: the maintained JSON template gives authors subsections,
interactive blocks, quizzes, themes and individual training certificates. Its engine is supplied by the
template standalone and by Academy when it is packaged.

Use **format 2** only when a lesson already has, or genuinely needs, a custom browser experience such as
a circuit simulator, a visual logic exercise or another local JavaScript application. It is a complete
local web folder and requires SemiTec Academy 1.9.0 or later. It does not use the JSON topic engine and
does not issue an individual training certificate. It can still count toward an optional package certificate.

## Where files go — ask once, then remember

Destination folders are **never** hard-coded. Before writing anything, resolve them:

1. Look for **`.semitec.json`**, starting in the working folder and searching upward. If it
   exists, use its values and do **not** ask.
2. If it is missing, ask the user for the keys below — one short round — then write
   `.semitec.json` at the root of their project with the answers, so no later run asks again.

| Key | Used for |
|---|---|
| `contentRoot` | where course materials live; trainings go to `<contentRoot>/<topic>/trainings/` |

Values are paths relative to `.semitec.json`, or absolute. Create folders that do not exist yet.
Never write outside them, and never assume a particular parent layout.

## Workflow

1. **Copy** the whole `training/` skill folder (engine + example content) to
   `<content>/<topic>/trainings/<topic>-<name>/`, where `<content>` is `contentRoot` (see *Where files go*) (e.g.
   `<sphere>/<topic>/trainings/<topic>-<name>`). Ask the user if you are unsure. Use a
   **last-level** topic (one without sub-topics). If that workspace has
   an inventory script and the topic's material folders do not exist yet, run it with `--init <topic>`
   first; skip this when there is none.
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

### Format 2 — custom local web training

Do not copy the JSON template merely to place custom scripts inside it. Create a focused folder instead:

```text
logic-playground/
├── training.json
├── index.html
├── js/                 custom lesson scripts
├── css/                custom lesson styles
└── assets/             local images, fonts or media
```

```json
{
  "format": 2,
  "id": "logic-playground",
  "title": "Logic playground",
  "hours": "1 h",
  "runtime": { "kind": "web", "entry": "index.html" }
}
```

`runtime.entry` must be a local `.html` file in the folder. Keep all scripts, CSS, images, fonts and
media local. Do not use CDNs, remote images, fetch/XHR/WebSocket, embedded frames, forms, Electron,
Node.js or a preload API: Academy blocks those capabilities when the training is packaged.

Academy adds `window.SemiTecAcademy` only inside a packaged format-2 training. It is a small progress API:

```js
SemiTecAcademy.onState(({ state, user }) => restore(state || {}, user));
SemiTecAcademy.save({ selectedGate: 'AND' }, { percent: 50 });
SemiTecAcademy.complete({ selectedGate: 'AND', solved: true });
```

`state` must be a plain object; `percent` is 0–100. `requestState()`, `getState()` and `getUser()` are
also available. Guard the API if the same page is previewed outside Academy, for example
`if (window.SemiTecAcademy) { … }`. Validate with `python3 tools/validate.py`, then use the package skill
to run `stlp check`; that tool verifies the entry and copies the full web folder.

## Rules

- For format 1, do **not** edit `js/` or `css/app.css` for content or look — only JSON, assets and theme files.
- For format 2, author only your lesson's own local HTML, CSS and JavaScript. Never copy or depend on the
  format-1 engine files; never expose secrets in browser code.
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

## Matching a publisher package style

When this training is part of a branded Academy package, its iframe does **not** inherit the package's
`pack.branding`. Create a matching training theme instead: copy `css/themes/foundation.css` to
`css/themes/<publisher>.css`, change only its variables, then set both `"theme": "<publisher>"` and
include the name in `"themes"` in `training.json`. Use the package's `accent`, `accentInk` and optional
`accentSoft` as the matching variables, but keep readable text and focus contrast. Do not edit engine JS,
`css/app.css`, or inject a stylesheet from the package manifest. Certificate colours remain in
`certificate.json → style`. A format-2 lesson has its own CSS, so use the same approved colours directly
there while maintaining readable text and focus contrast.

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
`academy-templates:package` skill (`skills/package`): add it to `"trainings"` in the pack spec with the
path of this folder. For format 1 the app supplies its engine and packs `training.json`, `topics/`, assets,
certificate and custom themes. For format 2 the packer copies the complete local web folder and Academy
saves state only through `window.SemiTecAcademy`.

## Academy Templates
Part of the **Academy Templates** plugin: `academy-templates:project-brief` (project brief PDF) ·
`academy-templates:diploma-project` (thesis PDF) · `academy-templates:lab-manual` (lab manual PDF + app lab) ·
`academy-templates:training` (interactive web training) · `academy-templates:package` (`.stlp` for SemiTec
Academy). Hand over to the matching skill when the user needs one of those outputs.
