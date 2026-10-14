# Adding a template

1. **Create `skills/<name>/`** — a short, plain name (`lab-worksheet`, `course-page`, `spec`).
2. **Template files** — PDF: `latex/` (main.tex, style, `lang/`, `sections/`, `diagrams/`), compiled
   `sample-output-*.pdf`. Web: the page engine, a content skeleton, `tools/` for checks and bundling.
   Reuse the conventions in [CONVENTIONS.md](CONVENTIONS.md) (style file of `project-brief` for PDFs,
   engine and themes of `training` for web pages).
3. **`SKILL.md`** with frontmatter:
   ```yaml
   ---
   name: <name>                       # = folder name
   description: >-
     What it makes, for whom, and the phrases that should trigger it. What it is NOT for.
   ---
   ```
   Body: the workflow (collect → skeleton → write → build → check → hand over), the tools with exact
   commands, the rules (no invented facts, `\missing{}` markers), and the files of the skill.
4. **`README.md`** for people (by hand and with AI), **`reference/`**, **`examples/`** (one complete case).
5. **Register it:** a row in the skills table and the tools table of [`../README.md`](../README.md), its
   build requirement in `NEEDS` of `tools/skills.py`, an entry in [`../CHANGELOG.md`](../CHANGELOG.md);
   raise `version` in `.claude-plugin/plugin.json`; remove it from [ROADMAP.md](ROADMAP.md).
6. **Check and package:** `python3 tools/skills.py zip && python3 tools/skills.py check` → 0 errors;
   optional `claude plugin validate .`.
7. If students should get it in SemiTec Academy, make sure the **package** skill can take its output
   (a PDF reading, a Markdown reading, a lab folder or a training folder); a new kind of content needs
   a new app format first (`Products/Academy/docs/VERSIONING.md`).
