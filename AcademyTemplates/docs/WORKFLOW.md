# Authoring, packaging and delivery workflow

## Use skills independently first

Each authoring skill has a complete standalone use case. A lab manual can be printed or shared with its
source files. A training can open in a browser. A project brief can be sent to a student. A diploma
document is normally submitted or defended outside Academy. None of these outcomes requires a package.

The package skill is a distribution step for Academy, not the normal way to create content. It gathers
selected materials, validates their references and creates an `.stlp` archive. The archive contains copies;
the editable sources remain in the materials repository.

## Responsibilities

| Repository | Owns | Does not own |
|---|---|---|
| `semitec-academy-skills` | skill instructions, templates, validators, the offline package builder, plugin releases | real lessons, production keys, released `.stlp` files |
| `semitec-academy-materials` | real course sources, package specifications, signed course archives and catalog entries | Academy application code |
| `semitec-academy` | app behavior, the `.stlp` format, public trusted keys and student installers | course content and built courses |

## Typical paths

### Standalone lab

```text
lecturer → lab-manual skill → manual.pdf + lab.json + src/ → students or LMS
```

### Standalone interactive training

```text
lecturer → training skill → training folder / self-contained HTML → browser or web platform
```

### Academy course

```text
authors → standalone labs + trainings + readings + briefs
        → package skill + pack-spec.json
        → stlp check → signed .stlp
        → materials release or catalog
        → Academy app
```

## Contributor workflow

1. Work in a branch and choose the narrowest affected skill.
2. Update the relevant template, script or reference; do not add a real course as an example.
3. Add or update a fictional fixture if behavior changes.
4. Run the local structural and integration checks.
5. If a package-format or training-engine contract changes, update `COMPATIBILITY.md` and coordinate the
   corresponding Academy change before releasing.
6. Release one new plugin ZIP only after the test workflow is green.
