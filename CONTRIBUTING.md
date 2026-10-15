# Contributing to Academy Templates

Academy Templates is one versioned authoring product. Contributors can improve an existing skill or add
a new one without changing real course material, signing keys, or Academy releases.

## Working agreement

1. Choose the smallest relevant skill. A lab, training, project brief or diploma document is useful on
   its own; do not involve the package skill unless the intended result is an Academy course file.
2. Keep `SKILL.md` focused on decisions an agent needs for that one job. Put detailed format rules in its
   `reference/` folder and reusable templates or scripts beside the skill.
3. Use fictional, minimal test fixtures only. Real lessons and released `.stlp` files belong in
   `semitec-academy-materials`.
4. Run `python3 tools/skills.py check` and `python3 tools/skills.py test` before review.
5. When a format, shared tool, or release behavior changes, update the workflow and compatibility docs
   in `docs/` in the same change.

## Adding a skill

Create `skills/<name>/SKILL.md` with a lowercase hyphenated name, a concise description,
and only the templates, scripts and references the job requires. Add it to the plugin README and the test
runner. A new skill is accepted only when it has a meaningful smoke test and a clear standalone use case.

## Cross-repository contract

The Academy app owns the `.stlp` format. The packaging skill carries a generated copy of the app's packer
so it can work offline; never hand-edit that copy. Update it with `bundle-skill`, then run the compatibility
test against the current app checkout. Details: [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).
