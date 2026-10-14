# Quality checklist — before a brief is published

Run through this list, fix what you can, and give the author the rest as a list.

## Completeness
- [ ] `grep -rn '\\missing' sections metadata.tex` is empty, or each remaining item is reported to the author.
- [ ] Title page and card: title, supervisor, department, work type, degree level, duration filled in.
- [ ] Chapters 1–11 present. 12–14 present unless the author removed them.

## Clarity for the student
- [ ] The problem statement fits in 2–4 sentences and names a concrete result.
- [ ] Every goal starts with a verb and can be checked at the defense.
- [ ] The MVP is listed explicitly. Out-of-scope items are named.
- [ ] Every task is one action with one result. Stretch tasks are marked `\optionaltask`.
- [ ] Technical terms are defined in the glossary on first use, or are in the learning path.

## Learning path and onboarding
- [ ] Prerequisites list a self-check for each item.
- [ ] 8–20 learning rows per student. The 3–5 core topics are `\apply`.
- [ ] Every row has a specific resource (chapter, tutorial number, module), and the resource exists. Uncertain ones are marked `\missing{verify}`.
- [ ] 2–5 warm-up exercises, from simple to project-like, each with an estimated time and `\donewhen{}`.
- [ ] Milestone 1 = warm-ups accepted.
- [ ] The tracker covers every week of the plan, and its task numbers match chapter 6.

## Feasibility
- [ ] The MVP fits in about 60–70% of the duration at the degree level. If not, items have moved to Extensions.
- [ ] Required equipment, licences and data are available, or the risk is listed with a plan B.
- [ ] The plan respects university deadlines.

## Cross-department mode
- [ ] Each student has an individual topic title and a task list that is a complete diploma for their own department.
- [ ] Neither student is blocked on the other for the first half: emulation, mocks or recorded data are planned.
- [ ] The interfaces table is filled in and has an agreement week.
- [ ] Each student has a learning-path table.

## Assessment
- [ ] Acceptance criteria are listed.
- [ ] Rubric weights sum to 100%. Pass / good / excellent are concrete and differ.

## Language and form
- [ ] The whole text uses the chosen language variant (reformed or classical spelling consistently; English chapter titles of the skeleton translated).
- [ ] Acronyms are in `abbreviations.tex`. Latin technical terms are not translated awkwardly.
- [ ] The build has no errors. Undefined references or citations: check `main.log` for `undefined`.
- [ ] Two pages rendered to an image look right: tables are not overflowing and there are no empty pages.

## Integrity
- [ ] No invented names, dates, companies, equipment or grading rules.
- [ ] References are real. URLs and editions are verified or flagged.
