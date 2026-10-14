# Brief → platform topic record

A brief is the document package of a **research topic** on the platform
(`Spec/objects/research-topic.md`; the template object in
`Spec/objects/template.md`). After the brief is final, produce the record so the
supervisor can post the topic. Skeleton: `templates/topic-record.json`.

| `research_topics` field | Source in the brief |
|---|---|
| `title` | `\settopictitle` |
| `description` | problem statement (ch. 2) + goals (ch. 3) + MVP (ch. 4), as rich text, about 150–300 words |
| `supervisor` | `\setsupervisorone` (platform user) |
| `co_supervisors` | `\setsupervisortwo`, plus the industry mentor if they are a platform user |
| `organization` | `\setpartnerorg` (or the supervisor's university) |
| `areas` | `\setareas`, mapped to the `research_areas` option set |
| `requirements` | `\setprerequisites` + the prerequisite list of ch. 7 (short) |
| `work_type` | `\setworktype` → `diploma` / `thesis` / `research_project` / `internship` / `other` |
| `degree_level` | `\setdegreelevel` → `bachelor` / `master` / `phd` |
| `slots` | `\setslots` (cross mode: 2, one per department) |
| `deadline` | `\setdeadline` (ISO date) |
| `template` | `project-brief` (this template) |
| `status` | `open` when published |
| attachment | the compiled brief PDF |

Brief-specific information that has no field yet (language variant, mode,
departments, duration, learning-path topics) goes into `extra` in the JSON.
It is a candidate for new fields: see the open questions on tracking thesis
work (#22) and templates (#38–41).
