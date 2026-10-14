# Interview — what to collect from the brief's author

The author is a supervisor (lecturer / researcher) or an industry employee
defining a project for students. Ask in **batches of 3–5 questions**, in the
order below. Batch A is the minimum for a first draft. Batches B–E fill in the
rest. Skip anything the author has already answered in a document they shared.

Each question lists where the answer goes (`→ chapter / metadata field`).

---

## Batch 0 — Setup (always first)
1. Which language should the brief be in: **English**, **Armenian (reformed
   spelling)**, or **Armenian (classical spelling)**? Should the title also
   appear in a second language? → `main.tex` option, `\settopicsubtitle`
2. Is this for **one student** or a **cross-department pair** (which two
   departments)? → mode, `\setdeptone`, `\setdepttwo`
3. Output: PDF (LaTeX), Word, or both? → build path

## Batch A — The essentials (enough for a first draft)
4. In two or three sentences, what is the project? What should exist at the end
   that does not exist now? → ch. 2 problem statement
5. Why does it matter, and for whom (lab, company, course, Foundation programme)?
   → ch. 1
6. What are the 3–5 things that **must** work for a successful defense?
   → ch. 3 goals, ch. 4 MVP
7. What is explicitly **not** required, even though a student might be tempted?
   → ch. 4 out of scope, ch. 13 extensions
8. Degree level (bachelor / master), work type (diploma / thesis / research
   project / internship), duration, and start date? → metadata

## Batch B — Technical content
9. What hardware, software, data or lab equipment is used? Is it available now?
   → ch. 1 platform, ch. 4 constraints, `\settools`
10. What are the main components and how do they connect (a rough sketch or a
    list is fine)? → ch. 2 diagram, ch. 5
11. Are there interfaces, data formats, protocols, register maps or parameters
    already decided? → ch. 5 tables
12. What does the student receive on day one (reference design, code, previous
    student work, documentation)? → ch. 5 starting point, ch. 8
13. Which design decisions should the **student** make themselves? → ch. 5
    (leave them open, say so)

## Batch C — The student: learning and onboarding
14. Which courses / knowledge should the student **already have**? How would you
    check it? → ch. 7 prerequisites, `\setprerequisites`
15. What will the student have to **learn new** for this project? Which 3–5
    topics are most important to master (level *apply*)? → ch. 7 table
16. Which books, courses, vendor tutorials, application notes or papers do you
    recommend? (If none, the agent proposes well-known ones for the author to
    confirm.) → `references.bib`, ch. 7
17. What should the student do in the first 2–4 weeks? Is there a small
    exercise that proves they are ready (e.g. "blink an LED through AXI",
    "simulate a FIFO")? → ch. 8 warm-up exercises
18. Accounts / access the student needs: repository, lab keys, licences, VPN,
    NDA? → ch. 8 checklist

## Batch D — Plan, deliverables, assessment
19. Key dates: university deadlines (pre-defense, submission, defense) and any
    partner deadlines? → ch. 9
20. What must be handed in besides the diploma document (code, hardware,
    measurements, video, user guide)? → ch. 10
21. How will you judge the work? What separates a pass from an excellent
    result? Any official grading rules to follow? → ch. 11 rubric
22. What should the final demonstration show? → ch. 12

## Batch E — People and logistics
23. Supervisor(s), co-supervisor, industry mentor (names, titles, roles)?
    Partner organization? → metadata, ch. 14
24. Meeting frequency and communication channel? → ch. 9 note, ch. 14
25. Main risks (equipment delays, licence, steep learning curve) and the plan B?
    → ch. 14 risks
26. How many students can take this topic (slots), and the application deadline?
    → `\setslots`, `\setdeadline`
27. Ideas for strong students or a follow-up master's thesis? → ch. 13

---

## Tips for the agent
- Rough answers are fine: turn them into precise text yourself, then show it to
  the author in the Step 3 skeleton for confirmation.
- When the author does not know, propose a sensible default for the degree
  level and **label it as a proposal** (e.g. a standard 30-week plan, a
  standard rubric), or leave `\missing{...}`.
- Do not ask about things the template already handles (layout, numbering,
  fonts, title page).
