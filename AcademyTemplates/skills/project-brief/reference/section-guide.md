# Section guide — what each chapter of a brief must contain

Status: **R** = required · **Rec** = recommended · **O** = optional.
Lengths are for a bachelor brief. A full brief is usually 8–15 pages.

| # | Chapter | Status | Length | File |
|---|---------|--------|--------|------|
| — | Title page + "Topic at a glance" card + contents | R (automatic) | 2 pp | `metadata.tex` |
| 1 | Context and motivation | R | ½–1 p | `01-context.tex` |
| 2 | Problem and project idea | R | 1–2 pp | `02-problem.tex` |
| 3 | Goals and expected outcomes | R | ½ p | `03-goals.tex` |
| 4 | Scope, MVP and constraints | R | ½–1 p | `04-scope.tex` |
| 5 | Technical description | R | 1–5 pp | `05-technical.tex` (may be split) |
| 6 | Roles and tasks | R | 1–2 pp | `06-roles-tasks.tex` |
| 7 | Learning path | R | 1–3 pp | `07-learning-path.tex` |
| 8 | Getting started | R | 1–2 pp | `08-getting-started.tex` |
| 9 | Work plan and milestones | R | ½–1 p | `09-work-plan.tex` |
| 10 | Deliverables | R | ½ p | `10-deliverables.tex` |
| 11 | Assessment and acceptance criteria | R | ½–1 p | `11-assessment.tex` |
| 12 | Final demonstration | Rec | ½ p | `12-demo.tex` |
| 13 | Extensions | O | ¼–½ p | `13-extensions.tex` |
| 14 | Supervision, collaboration and risks | Rec | ½ p | `14-supervision.tex` |
| 15 | Weekly progress tracker | Rec | 1–2 pp | `15-tracker.tex` |
| — | References / reading list, abbreviations, glossary, approval | R (automatic) | 1–2 pp | `references.bib` etc. |

---

## 1. Context and motivation
**Purpose:** a student new to the field understands why the project exists.
- Field context in plain words. The practical need, and who benefits.
- Partner organization and its role. The platform at a glance.
- Cross mode: which departments take part, and why the problem needs both.

## 2. Problem and project idea
- `\problemstatement{}`: 2–4 sentences, specific and checkable.
- The solution concept, an architecture diagram (TikZ), and a walk-through of the flow.
- What is new or interesting compared with a textbook exercise.

> ✗ "Develop a system for processing sensor data."
> ✓ "Build an FPGA pipeline that emulates three sensor types, filters them in
> real time, and streams the results to a web platform that can reconfigure
> the filters at runtime without regenerating the bitstream."

## 3. Goals and expected outcomes
- 3–6 goals. Each starts with a verb and is verifiable at the defense. Add a
  number where possible.
- Research questions or a hypothesis for research-type topics.
- **Learning outcomes:** skills, not topics ("can verify an RTL module with a
  self-checking testbench", not "Verilog").

## 4. Scope, MVP and constraints
- MVP = what must work for a pass. A bachelor MVP takes about 60–70% of the time.
- Out of scope: name the tempting things that are not required.
- Constraints: equipment, licences, data, lab hours, NDA. Assumptions.

## 5. Technical description
- Components and responsibilities; interfaces, formats, protocols; parameter
  and register tables; the starting point (reference designs, code).
- Say which decisions are left to the student.
- Split into several chapter files when it is longer than about 3 pages.

## 6. Roles and tasks
- `tasklist` per student: one verb, one result per task, 6–15 tasks. Mark
  stretch items with `\optionaltask`.
- *Individual topic* line: the title of that student's own diploma.
- `\keypoint{}`: what the examiners will focus on for this student.
- **Cross mode:** each part must stand alone as a diploma for its department.
  Add shared tasks (`tasklist{0}`) and an `interfaces` table, agreed by a
  stated week.

## 7. Learning path (the most important chapter for the student)
- **Prerequisites:** courses and knowledge assumed, each with a *self-check*
  and what to revise if weak.
- **Knowledge map** (`learningpath`): grouped rows with topic, level, where it
  is used in the project, and a resource.
  - Levels: `\aware` knows what it is · `\understand` can explain and read
    existing work · `\apply` can build with it.
  - 8–20 rows per student. Mark the 3–5 core topics `\apply`.
  - Every row has a **specific** resource: a book with chapter, an official
    tutorial, a course module, an app note or a paper (`\cite{}`).
  - Cross mode: one table per student, plus shared topics (interfaces, git).
- **Tools and skills:** software (with versions), equipment, languages,
  workflows (git, code review, lab notebook).

> ✗ "Learn FPGA programming."
> ✓ "AXI4-Lite slave interface · Apply · configuration registers in ch. 5 ·
> AMD PG155 + Vivado tutorial UG940, lab 3."

## 8. Getting started
- First-meeting checklist: access, accounts, equipment handover, safety.
- Environment setup: tool versions, install guide, build the reference example.
- 2–4 `warmup` exercises, each with an estimated time and a `\donewhen{}`
  acceptance condition. Each one builds toward the real project.
- "Read first": the 2–3 resources to start with.
- The first milestone in ch. 9 = warm-ups accepted.

## 9. Work plan and milestones
- `workplan` rows: weeks, phase, checkpoint result. The result must be checkable.
- Typical ~30-week bachelor plan: onboarding (1–3) → design (4–6) →
  implementation in 2–3 increments → integration and testing → evaluation →
  writing → defense preparation.
- Align with official university dates. Cross mode: integration checkpoints.

## 10. Deliverables
- `deliverables` rows: what, form, due, responsible. Usually: repository with
  README, hardware set-up, test/measurement data, diploma document (written
  with the diploma-project template), slides, demo video.

## 11. Assessment and acceptance criteria
- Hard acceptance criteria: all must be met to go to the defense.
- `rubric`: 4–7 criteria, weights summing to 100%, with concrete descriptions
  of pass / good / excellent. Follow official grading rules where they exist.
  The rubric supplements them; it does not replace them.

## 12. Final demonstration
A numbered scenario of observable steps. Writing it early makes the goal concrete.

## 13. Extensions
Not required for a pass. Ideas for strong students or a follow-up master's.
Good extensions reuse the MVP.

## 15. Weekly progress tracker
One row per week (`\weekrow`), grouped by phase (`\weekbreak`), derived from the
work plan and the task list. Each row has the planned work with task numbers, a
checkable result, an empty box to tick and a notes column. It starts on a new page
so it can be printed and used at the weekly meetings. The approval page is
optional: remove `\approvalblock` from `main.tex` if the institution does not need it.

## 14. Supervision, collaboration and risks
Roles of the supervisor(s) and mentor, meeting rhythm, channels. A `risks`
table with impact and mitigation (plan B).
