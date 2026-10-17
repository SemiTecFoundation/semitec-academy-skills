---
name: package
description: >-
  Build, check and update SemiTec Learning Packages (.stlp) — the signed course files students add to the
  SemiTec Academy desktop app. A package bundles trainings, labs, readings (PDF or Markdown), videos and
  other materials described in one pack-spec.json. Use when someone wants to create, package, publish,
  update or check a course / learning package for SemiTec Academy, add a study plan (weeks) or a diploma
  project to one, or asks what the app can show. Do not use it merely to create one standalone lab,
  training, brief or diploma document; those skills work without a package.
---
# Package standalone learning materials

Use this skill to gather selected standalone folders into a `.stlp` for Academy. Authoring and standalone
use do not require packaging. Follow existing output paths or `.semitec.json` configuration; clarify only
missing information. Never include unrelated or private source material implicitly.

Read [reference/pack-spec.md](reference/pack-spec.md) for fields, password scope, progress and certificate
semantics; [reference/archive-layout.md](reference/archive-layout.md) for the complete folder structure.
The bundled `scripts/stlp.js` shares its checker with Academy 2.1.0. It needs Node.js; no installation is
needed. If an Academy checkout is configured, its `packer/stlp.js` can be used instead.

## Build workflow

1. Select complete source folders for trainings, labs and projects, including HTML, scripts, assets,
   optional certificates, manual/brief PDF, source code and supporting materials. Ensure all references
   are local and included. External URLs remain links and cannot be promised as offline downloads.
2. Create `pack-spec.json` with identity, version, publisher/authors and items. Include **mandatory
   `modules` course order** and **mandatory `schedule` study plan**, covering every counted item including
   projects. Attachments (`for`) and optional prerequisites are excluded from coverage/progress.
3. Check certificate choices separately: package and every training. Omit certificate references where
   not wanted. Use dedicated HTML/CSS/JavaScript designs and `certificate/index_preview.html` for new ones.
   Never invent accreditation or signing authority. Certificates are optional and require no SemiTec approval.
4. Every training has `index_preview.html` with all sections open. Format 1 uses JSON; format 2 uses local
   HTML/CSS/JavaScript and declares `progress.mode: bridge` or `manual` with unique steps. Test bridge
   resume/completion or manual marking. A slide framework alone does not report learning completion.
5. If requested, generate a password verifier with `node scripts/stlp.js password-hash`. Never store a
   plaintext password in the spec. Use `pack.access.scope: "preview"` to keep normal learning/downloads
   open while excluding previews until password entry. `scope: "package"` locks everything. Explain that
   `.stlp` is a ZIP, not encrypted content; source recipients can edit it. Distribute passwords separately. To change one, generate a new verifier and increment the package
   version before rebuilding; existing learner progress should remain when item ids remain stable.
6. Run `node scripts/stlp.js check <spec>`. Resolve every error, including missing files, missing plan/order
   entries and unsupported formats. Do not bypass validation. Inspect warnings with the author.
7. Run `node scripts/stlp.js create <spec> --unsigned --out <local-drafts>` for a local test or use
   `--key <private.pem>` for an authorized signed delivery. Never put private keys in packages or repos.
8. Import into the target Academy version and test By type/Course order, full-folder downloads, locked
   preview filtering, custom progress, optional certificates, and PDF links/text if included. Academy
   rechecks content before replacing an installation. A valid signature does not bypass the checker.

## Final author handoff

Always report: source spec, output `.stlp`, version and minimum Academy version, signature status,
validation/test results, course order and study plan coverage, password scope, **package certificate:
 offered/not offered**, and **each training certificate: offered/not offered**. Link every offered
certificate preview and every training's all-open preview. Do not describe untested behavior as verified.
Downloads preserve full folders and attached materials; they never provide just one PDF or HTML as the
training/lab/project export. Without an explicit successful password unlock, author preview HTML is excluded, including when no password is configured. Open access to normal learning does not authorize author previews.
Academy clears the previous preview/package unlocks each time it installs a package, even for the same version; state this to publishers so they can tell learners to enter the password again after every installation.
After a successful preview-password unlock, Academy opens a training's `index_preview.html` as an
all-sections author review that must not save learner progress. The UI separately offers **Study normally**;
do not make the normal entry an unlocked preview or use author-preview behavior for learner progress.

Publishing a catalog, pushing sources, uploading a package or creating a release is a separate action.
Do not publish test or private materials without explicit user instruction naming that material.

Signing and partner trust: Academy's
[KEYS.md](https://github.com/SemiTecFoundation/semitec-academy/blob/main/docs/KEYS.md). A publisher generates
its own key pair, retains the private key and distributes the public key. Trust is separate from certificates.
