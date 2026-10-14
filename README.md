# SemiTec Skills

Claude plugins of the SemiTec Foundation. This folder is a **plugin marketplace** (`semitec-skills`,
`.claude-plugin/marketplace.json`); each subfolder is one plugin.

| Plugin | Folder | Skills |
|---|---|---|
| `academy-templates` | [`AcademyTemplates/`](AcademyTemplates/README.md) | `project-brief`, `diploma-project`, `lab-manual`, `training`, `package` |

Add the marketplace once in Claude Code, then install plugins from it:

```text
/plugin marketplace add https://github.com/SemiTecFoundation/semitec-academy-skills
/plugin install academy-templates@semitec-skills
```

A new plugin = a new folder with `.claude-plugin/plugin.json` and `skills/`, plus an entry in
`.claude-plugin/marketplace.json` and a row in this table.
