# Academy Templates

**Academy Templates** is one installable authoring product with several independent skills. A lecturer,
supervisor or student can use a skill to create a lab, interactive training, project brief or diploma
document and keep that result as a standalone file or folder. The **package** skill is optional: use it
only when selected materials should become one `.stlp` course for the SemiTec Academy desktop app.

![Authoring and delivery flow](docs/diagrams/authoring-flow.png)

## What each skill does

| Skill | Standalone result | When to package it |
|---|---|---|
| `project-brief` | Project task-definition PDF and optional Academy project folder | Add it only when students should track the project in Academy. |
| `diploma-project` | Thesis or diploma document and defence outline | Usually never; it is a final academic document. |
| `lab-manual` | Lab manual PDF, `lab.json`, quiz and source files | Add it when the lab belongs to an Academy course. |
| `training` | Interactive HTML training usable in a browser or another platform | Add it when it belongs to an Academy course. |
| `package` | One signed or test-only `.stlp` course archive | Use after choosing materials for Academy delivery. |

Packaging never changes an original lab, training or brief. It copies the materials chosen by the author
into a course archive, so the standalone source folders remain the editable originals.

## Install

Every version publishes one file: `AcademyTemplates-<version>.zip`. It contains this complete product,
including all skills, documentation and the offline package builder. The ZIP has one normal extraction
folder, `academy-templates/`, to keep its files together; that folder is the plugin root. There are no
per-skill ZIP downloads and no tracked `dist/` artifacts.

- **Claude Code:** add this repository as a marketplace, then install `academy-templates`.

  ```text
  /plugin marketplace add https://github.com/SemiTecFoundation/semitec-academy-skills
  /plugin install academy-templates@semitec-skills
  ```

- **Other agents:** download and extract the release ZIP, then configure the agent to load the required
  `skills/<name>/SKILL.md` folder. Each skill remains self-contained, so an agent may use only
  `training/` or only `lab-manual/` while retaining the same product version record.

- **Local development:** point Claude Code at the repository root:

  ```bash
  claude --plugin-dir /path/to/semitec-academy-skills
  ```

## Authoring and delivery workflow

This repository contains authoring capability, never real courses. The materials repository owns editable
course sources and released `.stlp` archives. The Academy app verifies, installs and presents those
archives to students.

1. Create or revise one standalone material with the relevant skill.
2. Validate it with that skill's command and keep its source under the materials repository.
3. If Academy delivery is wanted, use the package skill to select materials in `pack-spec.json`.
4. Run `stlp check`; fix errors; create an unsigned test archive or a signed release archive.
5. Release course archives from the materials repository or its catalog. Do not commit them here or in
   the app repository.

See [the detailed workflow](docs/WORKFLOW.md) for command-level ownership and
[the compatibility contract](docs/COMPATIBILITY.md) for the app/skill format boundary.

## Repository layout

```text
semitec-academy-skills/
├── .claude-plugin/
│   ├── plugin.json                 the Academy Templates plugin manifest
│   └── marketplace.json            marketplace entry for this repository
├── skills/                         independent authoring and packaging skills
│   ├── project-brief/
│   ├── diploma-project/
│   ├── lab-manual/
│   ├── training/
│   └── package/                    optional .stlp assembler and generated app packer
├── docs/                           workflow, compatibility, release rules and diagrams
├── tools/skills.py                 validates, tests and builds the one release ZIP
├── tests/fixtures/                 fictional test data, excluded from the release ZIP
├── CONTRIBUTING.md
└── CHANGELOG.md
```

The repository is the plugin root. There is no second `AcademyTemplates/` product folder to navigate.

## Contributors and releases

Run the following from the repository root:

```bash
python3 tools/skills.py check
python3 tools/skills.py test --academy /path/to/semitec-academy
python3 tools/skills.py release --out /tmp/AcademyTemplates-<version>.zip
```

`check` validates the plugin structure and release boundaries. `test` validates the standalone training,
builds a fictional package with the bundled packer and verifies that it matches the current Academy app.
`release` creates the one portable ZIP after checks pass. GitHub Actions repeats these checks for
contributions and attaches the ZIP and checksum to a tagged release.

Read [CONTRIBUTING.md](CONTRIBUTING.md), [RELEASING.md](docs/RELEASING.md) and
[ADDING-A-TEMPLATE.md](docs/ADDING-A-TEMPLATE.md) before changing product structure or adding a skill.
