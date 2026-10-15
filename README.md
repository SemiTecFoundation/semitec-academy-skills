# SemiTec Skills

This repository develops the **Academy Templates** authoring product. It is one plugin with several
independent skills: project briefs, diploma documents, lab manuals, interactive trainings and an optional
Academy package builder.

The repository is a Claude Code marketplace (`semitec-skills`), and every version is also released as
one downloadable `AcademyTemplates-<version>.zip`. The release ZIP is the portable product for agents
that do not use the marketplace.

| Product | Folder | Purpose |
|---|---|---|
| `academy-templates` | [`AcademyTemplates/`](AcademyTemplates/README.md) | Create standalone educational materials; optionally assemble several materials as one `.stlp` course for SemiTec Academy. |

For Claude Code, install from the marketplace:

```text
/plugin marketplace add https://github.com/SemiTecFoundation/semitec-academy-skills
/plugin install academy-templates@semitec-skills
```

For another agent, download the single release ZIP, extract it, and point that agent at the required
folder under `AcademyTemplates/skills/`. See the plugin's [installation guide](AcademyTemplates/README.md#install).

Contributors should start with [CONTRIBUTING.md](CONTRIBUTING.md). New skills belong in the same plugin
when they help create educational materials or package them for Academy; a distinct product belongs in a
new plugin folder and marketplace entry.
