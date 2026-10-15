# Training template (web)

Interactive training pages: topics with subtopics, interactive learning blocks, a quiz at the
end of every topic that unlocks the next one, review hints after a failed quiz, and a printable
certificate at the end. All content is JSON, all styling is a theme file — both can be
generated or changed by prompting an AI (see [the training skill](https://github.com/SemiTecFoundation/semitec-academy-skills/blob/main/AcademyTemplates/skills/training/SKILL.md)).

The template ships with a **feature tour**: every demo topic is named after a feature and
shows how to use it.

| # | Topic | Feature shown |
|---|---|---|
| 1 | Welcome & How It Works | navigation, tables, callouts, code |
| 2 | Scroll and Learn | sticky SVG that changes while scrolling (`scrolly`) |
| 3 | Click to Expand | accordion, flip cards |
| 4 | Zoom In and Compare | zoom viewer (wheel, drag, +/−), before/after slider |
| 5 | Multi Tabs | tabs with code, tables, pictures |
| 6 | Click to Reveal | hotspots on a picture; hotspot quiz |
| 7 | Animations | step player (`stepper`), continuous SVG animation with pause |
| 8 | Drag and Drop | ordering and grouping activities |
| 9 | Quiz Types | single, true/false, multiple, order, match, hotspot; per-quiz threshold |
| 10 | Different Views, Themes, Delivery & Certificate | sidebar / top-bar layouts, themes, delivery modes, certificate |

## Open it — three delivery modes

| Mode | What the student gets | Open with |
|---|---|---|
| **standalone** | topics unlock by quizzes, progress saved in the browser | `dist/training.html` (double-click) or `index.html` via a server |
| **preview** | **all topics open**, nothing saved, certificate preview with style controls | `dist/training-preview.html` or `index.html?mode=preview` |
| **platform** | topics unlock by quizzes, progress saved in **your platform's database** | embedded by the platform — see [`INTEGRATION.md`](INTEGRATION.md) |

- `python3 tools/build_single_file.py` builds both single files (everything inside: JSON, CSS, JS, themes, pictures).
- `python3 tools/dev_server.py` serves the folder **plus a demo progress API** → <http://localhost:8000/examples/>
  with working demos of all modes (REST, iframe + postMessage, same-page adapter).

## How it works for the student

- **One subtopic per page:** scroll to read it, then **Next** at the bottom (or the numbered pills on top,
  or the contents). The last page of a topic is its **quiz**.
- **Contents** on the left (sidebar layout) or on top (top-bar layout); topics expand to subtopics;
  ☰ shows / hides the contents. *View ▾* switches layout and theme and resets progress.
- A topic's quiz must reach the **pass threshold** to unlock the next topic. Questions with several
  correct answers say *Select all correct answers*.
- On a fail the quiz lists the **subtopics to read again** (links). Those pages show a box with
  *Back to the quiz*; *Try again* re-shuffles the questions.
- After the last quiz the **certificate** unlocks: type a name → *Create* → *Print / save as PDF*.
- Progress (visited pages, every quiz attempt, scores, certificate) is one JSON object per user —
  saved in the browser, or by a platform. Reopening the training continues at the last page.

## Folder structure

```
training/
├── index.html              page shell (do not edit for content)
├── training.json           title, settings, topic list
├── certificate.json        certificate texts and style
├── topics/                 one JSON file per topic: subsections (blocks) + quiz
├── assets/                 pictures, SVG diagrams and animations
├── css/
│   ├── app.css             layout + components (engine)
│   ├── certificate.css     certificate designs: classic, modern, minimal
│   └── themes/             foundation.css, midnight.css, paper.css (variables only)
├── js/                     engine: md, core, progress, blocks, quiz, certificate, app
├── dist/                   training.html (standalone) · training-preview.html (preview)
├── examples/               delivery-mode demos: index, platform-iframe, platform-same-page
├── tools/
│   ├── validate.py         checks JSON, ids, answers, review links, files
│   ├── build_single_file.py  bundles everything into dist/*.html
│   └── dev_server.py       local server + demo progress REST API
├── reference/
│   ├── content-format.md   every field of every file
│   └── labels-hy.json      Armenian UI texts (paste into training.json → labels)
├── INTEGRATION.md          modes, configuration, REST / iframe / JS adapter, events, state format, DB tables
└── SKILL.md                AI workflow and example prompts
```

## Make a new training

1. Copy this folder, change `id` and `title` in `training.json`.
2. Replace the demo files in `topics/` (keep the format — see `reference/content-format.md`).
3. Adjust `certificate.json`; pick or create a theme.
4. `python3 tools/validate.py` → 0 errors; preview; `python3 tools/build_single_file.py` to publish.

Plain HTML/CSS/JavaScript, no frameworks, no build step, works offline, keyboard accessible,
responsive down to phone width, respects *reduce motion*.
