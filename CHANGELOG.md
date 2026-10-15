# Changelog — Academy Templates plugin

## 1.5.1 — 2026-10
- Repaired the GitHub release workflow after flattening the plugin root. It builds the release archive in
  the runner's temporary directory, preserving the rule that generated archives never enter the source tree.

## 1.5.0 — 2026-10
- Made the repository itself the `academy-templates` plugin root. The redundant
  `AcademyTemplates/` directory and duplicate README are gone; the canonical product files now live at
  the top level in `skills/`, `docs/`, `tools/`, `.claude-plugin/` and `tests/`.
- Updated the marketplace entry, documentation, validation runner and GitHub workflows for the flat layout.
  The portable release still extracts safely into one `academy-templates/` folder and excludes tests,
  CI configuration and marketplace-only metadata.
- Kept only examples that are useful as standalone demonstrations or exercised by automated checks. Real
  courses, package archives and private material remain excluded from this repository and its releases.

## 1.4.0 — 2026-10
- Academy Templates is now released as **one portable plugin ZIP** (`AcademyTemplates-<version>.zip`),
  rather than five per-skill ZIPs. The individual skills remain independently usable inside that product.
- Documented the primary workflow: create labs, trainings, briefs and diploma documents standalone;
  use the package skill only to gather selected materials into an Academy `.stlp` course.
- Removed generated `dist/` artifacts, the broken full package example and the unverified course-like
  FPGA examples. Small fictional fixtures now verify the package builder and project export without
  shipping a course as an example.
- Added structural, standalone-build, package-build and optional cross-repository compatibility checks;
  releases attach one tested archive and checksum through GitHub Actions.
- Added contributor, workflow, compatibility and release documentation plus maintained PNG diagrams.

## 1.3.0 — 2026-10
- Destination folders are configuration, not assumptions: `training`, `lab-manual`, `project-brief`
  and `package` read `.semitec.json` (`contentRoot`, `packagesRoot`, `briefsRoot`, `academyRepo`),
  asking once and writing the file if it is missing. Documented in the README.
- No skill names a fixed folder layout any more: the example topic paths are generic (`<sphere>/<topic>`)
  and the inventory step is described without naming one repository's script.
- The package example was described as self-contained. It was not; 1.4.0 removes it and uses test-only
  fictional fixtures instead.
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
