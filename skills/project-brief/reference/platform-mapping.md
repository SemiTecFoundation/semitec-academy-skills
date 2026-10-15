# Brief → topic record (optional)

**Optional.** A brief can also be described as a **research topic** record for a
topic-posting system. The SemiTec Foundation has one internally; it is not public,
so skip this file unless the author asks for the record. Nothing else in the skill
depends on it. Skeleton: `templates/topic-record.json`.

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
Those are candidates for new fields in whatever system consumes the record.
