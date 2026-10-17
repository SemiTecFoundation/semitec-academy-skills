# Interactive training template

Create standalone learning material with the [training skill](SKILL.md). Format 1 uses maintained JSON
topics and quizzes; format 2 runs custom local HTML/CSS/JavaScript. Both support optional HTML certificates.

Run `python3 tools/build_single_file.py <folder>` for format 1, then `python3 tools/validate.py <folder>`.
The builder writes `index_offline.html` for normal study and `index_preview.html` with all sections open.
Keep the whole folder, including runtime, JSON, assets and optional certificate files. Custom format-2
authors supply and test both learner and preview entries themselves.

See [content fields](reference/content-format.md), [certificate designs](reference/certificates.md), and
[packaging](../package/README.md). Packaging is optional; Academy downloads full training folders and
omits author previews when the preview password has not been entered. Every author handoff states whether
a certificate is offered and links its preview when present.
