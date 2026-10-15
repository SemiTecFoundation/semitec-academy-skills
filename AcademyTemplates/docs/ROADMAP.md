# Roadmap

## Planned templates

| Template (skill) | Family | What it makes | Notes |
|---|---|---|---|
| `lab-worksheet` | PDF | short fill-in sheet students complete during a lab | from a lab's `lab.json` + manual |
| `lab-report` | PDF / Markdown | the structure students follow when they hand in lab results | hand-in and grading belong to a separate system, designed in an internal note published in neither repository |
| `defense-slides` | PDF (Beamer) / PPTX | diploma / thesis defense slides | today an outline in `diploma-project/reference/slides-outline.md` |
| `course-page` | Web | course page: syllabus by week, lectures, labs, assignments, reading list | links lab manuals and trainings |
| `lecture-slides` | Web | lecture presentations from Markdown, speaker notes, PDF export | |
| `spec` | PDF | technical specification / design document | for diploma and industry projects |
| `research-report` | PDF | research / progress report | |
| `syllabus` | PDF | official course syllabus | |
| `grant-proposal` | PDF | grant / funding proposal | |

## Skill features

- **project-brief:** export the topic record straight to the platform API; a brief → `diploma-project`
  starter (same metadata).
- **diploma-project:** Armenian variant as a first-class `latex-hy/` template; plagiarism-safe citation
  checker; `defense-slides`.
- **lab-manual:** worksheet output from the same source; auto-generated waveform figures from simulation.
- **training:** convert Markdown / slides into topics; quiz drafting from the text; Armenian labels by
  default; accessibility check.
- **package:** see `skills/package/ROADMAP.md` (video conversion, quiz drafting, release notes,
  size budget, catalogue entry, CI check).
- **plugin:** evals per skill (`claude plugin eval`), a `/academy` command that asks what to make and
  hands over to the right skill.
