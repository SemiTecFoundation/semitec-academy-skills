# Compatibility contract with SemiTec Academy

The Academy app is the authority for the `.stlp` format. The package skill bundles a snapshot of the
app's packer so it can build packages on a device that has only the plugin ZIP and Node.js installed.

## Rules

1. Never edit `skills/package/scripts/` by hand. Regenerate it from an Academy checkout:

   ```bash
   node /path/to/semitec-academy/packer/stlp.js bundle-skill \
     /path/to/semitec-academy-skills/skills/package/scripts
   ```

2. Commit the regenerated packer only with its `VERSION.json` record.
3. Run `python3 tools/skills.py test --academy /path/to/semitec-academy`.
   It compares the bundled files with a newly generated app bundle and checks that the app can inspect a
   fictional package made by the plugin.
4. If an app change adds a format, requires a new minimum app version, or changes package validation,
   update the package skill in the same release window. If the format is unchanged, document why no
   package-skill update is needed.

## Version meanings

| Version | Meaning |
|---|---|
| `.claude-plugin/plugin.json` | complete authoring product release; one ZIP for all skills |
| `skills/package/scripts/VERSION.json` | Academy app version that generated the bundled packer and its supported formats |
| package manifest `version` | a specific course update; owned by the materials repository |
| app `version` | installed Academy application release |

A plugin release can change documentation or an independent skill without changing the package builder.
An app release can change the UI without changing `.stlp` compatibility. Only the automated comparison
and package smoke test decide whether the bundled tool is current.
