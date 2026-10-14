# Skill roadmap (proposals)

Ideas for the next skill releases. They are proposals — see also the app's `docs/PROPOSALS.md`.

| Idea | What the skill would do |
|---|---|
| **Video check and conversion** | detect codec / resolution with ffprobe, offer to convert to 720p H.264 MP4 with ffmpeg, add chapters from a text list |
| **Quiz drafting from readings** | read a PDF / Markdown reading and propose a check quiz for it (needs a "reading quiz", app format change) |
| **Package diff and changelog** | compare two versions of a package, list added / changed / removed items, warn when ids changed (progress loss), write release notes shown in the app |
| **Translation run** | produce an Armenian (or Russian) version of all trainings, labs and Markdown readings with stable ids, as a second package or a language variant |
| **Accessibility check** | missing image alt texts, low-contrast SVG colours, videos without captions, very long subsections |
| **Size budget** | warn when a package gets too large for e-mail / USB, suggest splitting into several packages |
| **Cover generator** | create a cover SVG from the title and the Foundation style |
| **Prerequisites** | let the spec say "lab 2 opens after lab 1" (needs app support) |
| **Package catalogue entry** | write a catalogue JSON / web page for the package (title, description, contents, minimum app version, download link) |
| **CI check** | a ready GitHub / GitLab workflow that runs `stlp check` on every change in a packs repository |
