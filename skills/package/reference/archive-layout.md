# `.stlp` archive layout

This is a fictional layout for authors. The archive is a ZIP; the builder writes `manifest.json` and
file hashes and optionally signs them. Do not create a manifest by hand or publish test packages.

```text
course.stlp
├── manifest.json                  identity, authors/publisher, items, mandatory modules and schedule,
│                                 optional certificate/access/branding, minimum app version, file hashes
├── signature.json                 present when signed; Ed25519 key ID and signature
└── content/
    ├── certificate/               optional package HTML/CSS/JS certificate
    │   ├── index.html
    │   ├── index_preview.html     visibly marked sample certificate
    │   ├── certificate.css
    │   └── certificate.js
    ├── trainings/
    │   ├── json-lesson/            training format 1
    │   │   ├── training.json
    │   │   ├── index.html
    │   │   ├── index_offline.html
    │   │   ├── index_preview.html
    │   │   ├── topics/01-intro.json
    │   │   ├── js/                maintained runtime, also kept for standalone use
    │   │   ├── css/
    │   │   ├── assets/
    │   │   └── certificate/       optional HTML/CSS/JS design and preview
    │   └── web-lesson/             training format 2 (custom page, simulator or slide framework)
    │       ├── training.json      runtime entry, progress mode/steps, optional certificate reference
    │       ├── index.html
    │       ├── index_preview.html all sections open; publisher implements this behavior
    │       ├── js/
    │       ├── css/
    │       ├── assets/
    │       ├── vendor/            local framework dependencies, if used
    │       └── certificate/       optional HTML/CSS/JS design and preview
    ├── labs/practice/
    │   ├── lab.json
    │   ├── manual.pdf
    │   ├── src/
    │   └── materials/
    ├── projects/capstone/
    │   ├── project.json
    │   ├── brief.pdf
    │   ├── src/
    │   ├── requirements/
    │   └── materials/
    ├── readings/primer/primer.pdf
    ├── videos/introduction/introduction.mp4
    └── materials/data/data.csv
```

Not every category is required; include the categories you need. Certificates are optional independently
at package and training levels. Source folders are kept complete for trainings, labs and projects; put
all supporting files beneath the material's folder. Root authoring tools, node_modules, generated dist
and skill documentation are excluded from training bundles. Bundle browser dependencies under `vendor/`.

The editable input is [pack-spec.md](pack-spec.md), including a valid order/plan example. The compiler
maps each source into its own category/item directory and calculates file hashes. `manifest.modules`
gives the course order; `manifest.schedule` gives the study plan. Every counted item must appear in both.
`manifest.certificate` for a web design is `{"kind":"web","entry":"certificate/index.html"}`.
A training certificate is a local HTML reference in that training's `training.json`, also recorded on
its manifest item. The source folder can be used independently of a package.

Academy downloads a **complete folder** per item, from either By type or Course order. Lab/project copies
include metadata, manual/brief, sources, requirements and materials. Attachments declared as separate
items with `for` are copied into `academy-attachments/<id>/`. JSON training copies include a portable
`index.html`; custom training copies keep their declared entry and assets. PDF-only items still download
in a folder. External links download a link description, not remotely hosted content.

If a package's preview password has not been entered, exported folders exclude author preview HTML,
including certificate previews. Normal learner HTML/assets remain. Only after a configured package password is successfully entered are previews included. A package with no password also excludes previews from learner downloads. Author sources and the archive retain the preview files.
Academy clears preview/package unlocks whenever a package archive is installed again, including a package with the same version, so learners enter the password again after each installation.
All downloaded editable sources are learner-owned local copies; the password is not encryption.
