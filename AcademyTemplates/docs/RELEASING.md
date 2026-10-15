# Releasing Academy Templates

Every release produces one portable plugin archive: `AcademyTemplates-<version>.zip`. It contains the
entire `AcademyTemplates/` folder, not one ZIP per skill. GitHub Releases is the distribution channel;
the repository does not track `dist/` outputs.

## Before tagging

1. Update `.claude-plugin/plugin.json` and `CHANGELOG.md`.
2. If the `.stlp` contract changed, regenerate the package builder from the Academy app and update
   `COMPATIBILITY.md`.
3. Run:

   ```bash
   python3 AcademyTemplates/tools/skills.py check
   python3 AcademyTemplates/tools/skills.py test --academy /path/to/semitec-academy
   python3 AcademyTemplates/tools/skills.py release --out /tmp/AcademyTemplates-<version>.zip
   ```

4. Inspect the ZIP in a clean temporary folder. It must contain `AcademyTemplates/`, its plugin manifest,
   all skills and the package runtime; it must not contain `.stlp` courses, private keys, generated `dist/`
   folders, personal data or test fixtures.

## Publish

Tag the commit `v<plugin-version>`. The release workflow repeats validation, builds the ZIP, creates a
SHA-256 checksum and attaches both files to the GitHub Release. State the app version used by the bundled
package tool in the release notes.

Do not publish a course from this repository. Course packages are released from
`semitec-academy-materials` after they have been tested in the app.
