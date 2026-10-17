---
name: training
description: >-
  Create an interactive web training (HTML, works offline): topics with subsections, interactive blocks
  (scroll-and-learn, accordions, tabs, zoom, hotspots, animations, drag and drop), a quiz per topic that
  unlocks the next one, a certificate, themes and layouts. The default is Academy JSON content; an explicit
  custom-web format is available for a lesson that needs its own local JavaScript interactions. Use when a
  lecturer wants to build, update or translate a training, tutorial, interactive lesson or self-paced course module.
---
# Create and update standalone trainings

Create educational material in its own folder. Packaging is a separate optional step using the package
skill. Follow the user's established output location and source language. Read
[reference/content-format.md](reference/content-format.md) for JSON block and quiz fields.

## Choose one of two formats

1. **Format 1: Academy JSON.** Use the maintained template for topics, interactive blocks, quizzes and
   sequential progression. Keep `training.json`, `topics/`, HTML, JS/CSS, assets and certificate files together.
2. **Format 2: custom local web.** Use for JavaScript lessons, simulators or slide frameworks. Keep the
   publisher's HTML/CSS/JavaScript together; declare a local HTML entry. Bundle all dependencies locally,
   without remote scripts, Node/Electron APIs or a server requirement. Verify double-click offline use.

Both formats can offer an optional individual certificate. The package can separately offer an optional
course certificate. Never select a different training format merely to add a certificate.

```json
{
  "format": 2,
  "id": "web-lesson",
  "title": "Example lesson",
  "runtime": {"kind": "web", "entry": "index.html"},
  "progress": {"mode": "manual", "steps": [
    {"id": "review", "title": "Review the lesson"},
    {"id": "practice", "title": "Complete the exercise"}
  ]},
  "certificate": "certificate/index.html"
}
```

Omit `certificate` when the author does not want it. For bridge integration instead of manual steps set
`"progress":{"mode":"bridge"}`. Academy injects `window.SemiTecAcademy` inside its sandbox:

```js
if (window.SemiTecAcademy) {
  SemiTecAcademy.onState(({state, user}) => restore(state, user));
  SemiTecAcademy.save({completedSections}, {percent: 50, completed: false});
  // Only when the author-defined learning requirements are satisfied:
  SemiTecAcademy.complete({completedSections});
}
```

The web page must also work when the bridge is absent, using its own standalone progress storage.
Do not mark completion merely on page load. Test resume and completion inside Academy. For Reveal or
another presentation without such integration, use manual steps; Academy renders and counts them outside
the iframe. Both modes count toward the package's overall progress and optional certificate.

## Learner entry and author preview

Every generated training must include **`index_preview.html`** with all sections unlocked and no saved
learner progress. For format 1 run `python3 tools/build_single_file.py <training-folder>`: it creates
`index_offline.html` and `index_preview.html`. Keep the runtime `index.html` and source files too.
For format 2, implement a distinct preview page and verify every section opens, including quiz-restricted
sections; a file named preview alone is not enough. The normal entry must not depend on or link to the
preview, and must work by double-click without a localhost server.

In a package, the recommended optional password scope is `preview`: learners can study and download the
normal training without it; Academy excludes author preview HTML until they enter the publisher's package
password. Do not put an unlocked preview into the normal entry or another disguised file. Set format-1
`delivery.urlParams: false` to prevent a normal learner URL switching into preview mode. The package skill
owns password verification metadata. With no package password configured, learner downloads still exclude author previews; the author keeps them in the source folder. This is delivery control, not encryption of distributed sources.

## Optional certificates and visible author review

State explicitly whether the author wants a certificate. Respect a prior choice; otherwise ask once
before inventing issuer/signature information. Omit the reference when no certificate is offered.
Use the `certificate/` HTML/CSS/JavaScript template for new certificates. Edit its layout/styles freely,
including local logos/assets. `certificate/index_preview.html` shows sample data and must visibly say it
is a preview, not an issued credential. See [reference/certificates.md](reference/certificates.md).

Academy sends identity/completion data to the sandboxed certificate via `postMessage`; use `textContent`
for learner text. Legacy JSON certificate configs remain readable for existing material, but do not limit
new designs to those style presets. For standalone custom lessons, integrate the same HTML design in the
lesson's completion flow; Academy cannot inject a completion screen into an arbitrary web application.

## Finish and report

1. Check accuracy, wording, section IDs, navigation, required assets and offline operation.
2. Generate the normal offline entry and the all-open preview. Open both; verify they have different
   progression behavior. Open the certificate preview if offered.
3. Run `python3 tools/validate.py <training-folder>`. For packaging, run the package check too.
4. Report the output folder, learner entry, **author preview**, format, progress method and **certificate:
   offered/not offered**. Link the certificate preview when present. Mention any untested behavior.
5. Do not publish, upload or create a release without the user's instruction for that material.

Standalone training topic schedules are optional. A package always needs mandatory course order and a
study plan covering counted items. Training source, previews, certificates and local dependencies stay
in one folder so a package download can preserve the complete material.
