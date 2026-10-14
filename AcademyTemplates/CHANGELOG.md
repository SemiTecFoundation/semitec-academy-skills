# Changelog — Academy Templates plugin

## 1.3.0 — 2026-10
- Destination folders are configuration, not assumptions: `training`, `lab-manual`, `project-brief`
  and `package` read `.semitec.json` (`contentRoot`, `packagesRoot`, `briefsRoot`, `academyRepo`),
  asking once and writing the file if it is missing. Documented in the README.
- No skill writes into a fixed folder layout any more, and `examples/pack-spec.json` is
  self-contained instead of reaching into sibling folders.
- **package** 1.6.2: bundled packer from SemiTec Academy 1.6.2; packages are signed with the
  production key only (no development key is trusted by the app), `prerequisite` documented.
- The optional topic record for a topic-posting system is marked optional.

## 1.2.0 — 2026-10
- **package** 1.5.0: publisher logo (`pack.publisherLogo`), materials attached to labs (`"for"`), project
  `category`, `stlp catalog` for publishing a catalog; bundled packer from SemiTec Academy 1.5.0.
- **project-brief:** `brief2project.py` writes the project `category` (from the work type, or `--category`).

## 1.1.0 — 2026-10
- **project-brief:** `tools/brief2project.py` — a finished brief becomes a SemiTec Academy project
  (`project/project.json` + `brief.pdf`): weekly plan from the progress tracker, milestones, deliverables,
  rubric, learning path; `reference/app-project.md`.
- **training:** optional `"schedule"` in `training.json` (topics per week); checked by `tools/validate.py`;
  the template's feature tour has a 2-week plan.
- **package** 1.4.0: projects, study plans (`schedule`, `plannedWeeks`), course certificate; bundled packer
  from SemiTec Academy 1.4.0.

## 1.0.0 — 2026-10
- Templates moved from `Platform/Templates` to `Products/Skills/AcademyTemplates` and packaged as the
  Claude Code plugin **`academy-templates`** (marketplace `semitec-skills` in `Products/Skills`).
- One skill per template, renamed to the plugin form:

  | Before | Now (Claude Code) | Now (alone) |
  |---|---|---|
  | `project-brief-template` | `academy-templates:project-brief` | `academy-project-brief` |
  | `diploma-project-template` | `academy-templates:diploma-project` | `academy-diploma-project` |
  | `lab-manual-template` | `academy-templates:lab-manual` | `academy-lab-manual` |
  | `training-template` | `academy-templates:training` | `academy-training` |
  | `semitec-learning-package` | `academy-templates:package` | `academy-package` |

- Family / category READMEs (`pdf/`, `web/`, `SKILLS.md`) merged into `README.md`, `docs/CONVENTIONS.md`,
  `docs/ADDING-A-TEMPLATE.md` and `docs/ROADMAP.md`.
- `tools/skills.py`: plugin layout, `dist/academy-<name>.zip`, stand-alone install with `academy-` names,
  `plugin` command; checks the plugin manifest.
- New `skills/diploma-project/README.md`.
- Skill contents as before: project-brief, diploma-project, lab-manual (lab format 2 with source files),
  training (paged subsections, delivery modes), package 1.3.0 (`.stlp`, Markdown readings).
