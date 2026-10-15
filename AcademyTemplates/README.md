# Academy Templates

**Academy Templates** is one installable authoring product with several independent skills. A lecturer,
supervisor or student can use a skill to create a lab, interactive training, project brief or diploma
document and keep that result as a standalone file or folder. The **package** skill is optional: use it
only when several materials should become one `.stlp` course for the SemiTec Academy desktop app.

![Authoring flow](docs/diagrams/authoring-flow.png)

## What each skill does

| Skill | Standalone result | When to package it |
|---|---|---|
| `project-brief` | project task-definition PDF and optional Academy project folder | Add it only when students should track the project in Academy. |
| `diploma-project` | thesis/diploma document and defence outline | Usually never; it is a final academic document. |
| `lab-manual` | lab manual PDF, `lab.json`, quiz and source files | Add it when the lab belongs to an Academy course. |
| `training` | interactive HTML training, usable in a browser or another platform | Add it when it belongs to an Academy course. |
| `package` | one signed or test-only `.stlp` course archive | Use after choosing more than one material for Academy delivery. |

Packaging does not change an original lab, training or brief. It copies chosen materials into a course
archive, so authors keep their standalone source folders as the editable originals.

## Install

### One release ZIP

Every version publishes one file: `AcademyTemplates-<version>.zip`. It contains the complete plugin,
including all skills, templates and the offline package builder. There are no per-skill ZIP downloads and
no tracked `dist/` artifacts in this repository.

- **Claude Code:** add this repository as a marketplace, then install `academy-templates`.

  ```text
  /plugin marketplace add https://github.com/SemiTecFoundation/semitec-academy-skills
  /plugin install academy-templates@semitec-skills
  ```

- **Other agents:** download and extract the single release ZIP. Configure the agent to load the required
  `AcademyTemplates/skills/<name>/SKILL.md` folder. The individual skill folders are deliberately
  self-contained, so an agent may use only `training/` or only `lab-manual/` while retaining the same
  product release and version record.

- **Local development:** point Claude Code at the plugin directory:

  ```bash
  claude --plugin-dir /path/to/AcademyTemplates
  ```

## Authoring and delivery workflow

The skills repository contains authoring capability, not real courses. The materials repository owns
editable course sources and released `.stlp` course archives. The Academy app verifies, installs and
presents those archives to students.

1. Create or revise one standalone material with the relevant skill.
2. Validate it with that skill's command and keep its source under the materials repository.
3. If Academy delivery is wanted, use the package skill to select several materials in `pack-spec.json`.
4. Run `stlp check`; fix errors; create an unsigned test archive or a signed release archive.
5. Publish course archives from the materials repository or its catalog. Do not commit them here or in the
   app repository.

See [WORKFLOW.md](docs/WORKFLOW.md) for command-level ownership, and
[COMPATIBILITY.md](docs/COMPATIBILITY.md) for the app/skill format contract.

## Repository layout

```text
AcademyTemplates/
├── .claude-plugin/plugin.json       one plugin version
├── skills/                          independent authoring and packaging skills
│   ├── project-brief/
│   ├── diploma-project/
│   ├── lab-manual/
│   ├── training/
│   └── package/                     optional .stlp assembler; includes generated app packer
├── docs/                            workflow, compatibility, release rules and diagrams
└── tools/skills.py                  validate, test and build the one release ZIP

tests/
└── fixtures/                        fictional test data; excluded from the release ZIP
```

## Contributors and releases

Run the following from the repository root:

```bash
python3 AcademyTemplates/tools/skills.py check
python3 AcademyTemplates/tools/skills.py test
python3 AcademyTemplates/tools/skills.py release --out /tmp/AcademyTemplates-1.4.0.zip
```

`check` validates the plugin structure and release boundaries. `test` validates the standalone training,
builds a fictional package with the bundled packer and, when given an Academy checkout, verifies that the
generated package and bundled packer match the current app. `release` creates the single ZIP after checks
pass. GitHub Actions repeats these checks for contributions and attaches the ZIP to a tagged release.

Read [CONTRIBUTING.md](../CONTRIBUTING.md), [RELEASING.md](docs/RELEASING.md) and
[ADDING-A-TEMPLATE.md](docs/ADDING-A-TEMPLATE.md) before changing product structure or adding a skill.
