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
| `semitec-academy` | app behavior, the `.stlp` format, Foundation keys, locally trusted publisher keys and student installers | course content and built courses |

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
        → stlp check → publisher self-review → optional certificate + signed .stlp
        → materials release or catalog → recipient trusts publisher key → Academy app
```

`stlp check` confirms technical validity; it is not an institutional approval queue. Partners may create
and publish their own materials without a Foundation agreement. The publisher chooses author attribution,
content rights, a feedback contact and whether the package offers a course certificate. Recipients decide
which publisher public keys to trust in the Academy app. Details: [PUBLISHING.md](PUBLISHING.md).

## Contributor workflow

1. Work in a branch and choose the narrowest affected skill.
2. Update the relevant template, script or reference; do not add a real course as an example.
3. Add or update a fictional fixture if behavior changes.
4. Run the local structural and integration checks.
5. If a package-format or training-engine contract changes, update `COMPATIBILITY.md` and coordinate the
   corresponding Academy change before releasing.
6. Release one new plugin ZIP only after the test workflow is green.

## Current delivery contract

Package and individual training certificates are optional author/publisher choices in both training formats
(1: JSON; 2: custom HTML/CSS/JavaScript). New designs use HTML/CSS/JavaScript with a sample author preview.
Every author handoff states certificate offered/not offered and links any certificate preview. Every training
has `index_preview.html` with all sections open. Package order and study plan are mandatory. The builder and
Academy import both check the files and metadata. Downloads always preserve complete folders and supporting
sources; author preview HTML is omitted by default, including from open packages, and is included only after an explicit package-password unlock. Custom presentations use explicit
bridge progress or Academy's manual steps. See [the package contract](../skills/package/reference/pack-spec.md) for publisher metadata and password setup.
