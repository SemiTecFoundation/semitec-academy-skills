# Brief → SemiTec Academy project

`tools/brief2project.py` turns a finished brief into the **project** that students see in SemiTec Academy
(app ≥ 1.4.0). The brief stays the source of truth: edit the LaTeX, rebuild the PDF, run the tool again.

```bash
python3 tools/brief2project.py <brief-folder> [--pdf <compiled brief.pdf>] [--id <project-id>] [--out <dir>]
# → <brief-folder>/project/project.json + brief.pdf
```

| project.json | Taken from |
|---|---|
| `title`, `subtitle`, `workType`, `level`, `slots`, `duration`, `durationWeeks`, `supervisors`, `mentor`, `partner`, `areas`, `keywords`, `tools`, `prerequisites` | `metadata.tex` (`\settopictitle` …) |
| `summary` | first paragraph of the problem (or context) chapter |
| `goals`, `outcomes` | the goals chapter: first `enumerate`, the `itemize` after "Learning outcomes" |
| `weeks[]` — `{ week, phase, tasks, doneWhen }` | the progress tracker: `\weekbreak{phase}`, `\weekrow{week}{tasks}{done when}` |
| `milestones[]` — `{ weeks: [a, b], work, milestone }` | the work plan: `\milestone{1--4}{work}{milestone}` |
| `deliverables[]` — `{ title, form, when, dueWeek, who }` | `\deliverable{what}{form}{when}{who}` (`dueWeek` = last number in *when*) |
| `assessment[]` — `{ criterion, weight, pass, good, excellent }` | `\criterion{…}{…}{…}{…}{…}` |
| `learning[]` — `{ group, topic, level, usedFor, sources }` | `\learngroup`, `\learn{topic}{\apply|\understand|\aware}{used for}{sources}` (citations → "Author Year") |
| `category` | from the work type: research · diploma · thesis · course-project · capstone · internship · other (or `--category`) — the filter on the app's Projects page |
| `brief` | the compiled PDF (found in the folder, or `--pdf`) |

LaTeX is converted to light Markdown (`**bold**`, `*italic*`, `` `code` ``), cross-references become chapter
names, citations are removed from texts (kept as "Author Year" in `sources`).

**In the app:** the student enrolls with a start date; week *n* of the tracker is mapped to the calendar,
each week can be ticked and gets notes for the weekly meeting; milestones and deliverables get dates;
the Today panel shows this week's tasks. Keep **week numbers stable** between versions of a brief —
students' ticks are stored per week.

Checks before packaging: every tracker week has tasks and no `[placeholders]`, week numbers are unique,
milestones lie inside the duration. `academy-templates:package` checks the folder again (`stlp check`).
