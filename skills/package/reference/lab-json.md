# `lab.json` — lab formats 1 and 2

A lab is a folder with `lab.json` and (usually) the lab manual PDF made with the laboratory PDF template.

```json
{
  "title": "Lab 1: A 4-bit shift register on the FPGA",
  "summary": "Markdown: what the student builds",
  "difficulty": "beginner",
  "estimatedTime": "2 h",
  "equipment": ["<your board>", "Vivado 2024.2+"],
  "objectives": ["Write sequential logic with `always_ff`", "…"],
  "manual": "manual.pdf",
  "files": "src",
  "steps": [
    { "id": "rtl", "title": "Write the shift register", "md": "Markdown text",
      "code": "always_ff @(posedge clk) …", "hint": "Markdown, shown on request", "manualPage": 2,
      "files": ["src/rtl/shift4.sv"] }
  ],
  "quiz": {
    "title": "Lab 1 check", "passThreshold": 0.75,
    "questions": [
      { "id": "q1", "type": "single", "text": "…", "options": ["A", "B", "C"], "correct": [0], "review": ["rtl"] }
    ]
  }
}
```

| Field | Required | Meaning |
|---|---|---|
| `title` | ✓ | shown in the app |
| `summary`, `objectives` | | Markdown; shown above the steps |
| `difficulty`, `estimatedTime`, `equipment` | | shown in the lab header |
| `manual` | recommended | PDF in the lab folder; opens in the *Manual* tab |
| `files` | | **format 2:** source files of the lab — a folder (`"src"`) or a list of files / folders (`["src/", "scripts/run.tcl"]`). Shown in the app's *Files* tab (text viewer with line numbers and copy). **Download folder** exports the entire lab with its manual, source files and supporting materials |
| `steps[]` | ✓ | `id` (unique, lowercase), `title`; optional `md`, `code`, `hint`, `manualPage` (filled by `tools/build.py`), `files` (links to files listed in `files`) |
| `quiz` | recommended | same question types as trainings: `single`, `truefalse`, `multiple`, `order`, `match`, `hotspot`; `review` = step ids to re-read when wrong |

**Format 1** = without `files` (opens in SemiTec Academy ≥ 1.0.0). **Format 2** = with `files`
(needs SemiTec Academy ≥ 1.2.0); the packer detects it automatically.

The student ticks steps and passes the quiz; the lab is complete when all steps are ticked and the
quiz is passed. Progress: 70 % steps + 30 % quiz.

Question fields: `single`/`truefalse` → `options`, `correct: [index]`; `multiple` → `correct: [i, j]`;
`order` → `items` in the correct order; `match` → `categories: [{id,label}]`, `items: [{text, category}]`;
`hotspot` → `src`, `spots: [{id,x,y,w,h}]` in percent, `correct: [ids]`. Indices start at 0.
