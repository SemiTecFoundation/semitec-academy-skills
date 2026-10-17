# Supported formats

Current packaging targets Academy 2.1.0+. The app and bundled checker share validation code.

| Kind | Supported formats |
|---|---|
| Training | 1: Academy JSON; 2: custom local HTML/CSS/JavaScript |
| Package container | 1: base; 2: branding; 3: optional password access |
| Lab | 1: steps/manual; 2: includes indexed source files |
| Reading | 1: PDF; 2: Markdown with local assets |
| Project / video / material | 1 |

Training formats 1 and 2 both support optional individual certificates, separately from an optional
package certificate. New certificate designs use HTML/CSS/JavaScript. Legacy JSON designs remain readable.
Course order and study plan are required for new builds/imports. Old installed learning records are
preserved, but a re-imported package must pass the current checker. Use [pack-spec.md](pack-spec.md) and
[archive-layout.md](archive-layout.md) for the current contract. Do not infer feature support from the
container format alone: check `minAppVersion` too.
