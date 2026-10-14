# Content format reference

Everything a training shows comes from JSON. This page lists every field.
Text fields marked *md* accept light Markdown: `**bold**`, `*italic*`, `` `code` ``, `[link](url)`,
lists (`- item`, `1. item`), `> quote`, `### heading`, blank line = new paragraph. HTML is escaped.

---

## 1. `training.json`

| Field | Type | Default | Meaning |
|---|---|---|---|
| `id` | string | — | Unique id. Progress is saved per id — change it for a new training. |
| `version` | string | — | Content version, copied into the saved state (`trainingVersion`). |
| `title`, `subtitle` | string | — | Shown in the header (title also on the certificate). |
| `language` | string | `en` | `en`, `hy`, `ru` … Used for date format and `<html lang>`. |
| `layout` | `sidebar` \| `topbar` | `sidebar` | Default layout. |
| `theme` | string | `foundation` | Default theme = file `css/themes/<name>.css`. |
| `themes` | string[] | 3 built-in | Themes offered in *View ▾*. |
| `allowViewSwitch` | bool | `true` | Show layout/theme selectors in *View ▾*. |
| `passThreshold` | 0–1 | `0.8` | Share of correct answers needed to pass a quiz. |
| `showCorrectAnswers` | `never` \| `afterPass` \| `always` | `afterPass` | When to reveal correct answers + `explain`. |
| `requireSequential` | bool | `true` | Topic N+1 opens only after topic N is passed. |
| `topicWord` | string | `Topic` | Word in the kicker "Topic 2 / 10". |
| `hours` | string | — | Used by `{hours}` on the certificate. |
| `labels` | object | — | Override any UI text (see `T.labels` in `js/core.js`), e.g. `{"next": "Հաջորդը"}`. |
| `topics` | string[] | — | File names in `topics/`, in order. |
| `certificate` | string | — | Path of the certificate file (omit = no certificate). |
| `delivery` | object | `{mode: "standalone"}` | Delivery mode and progress storage — see `INTEGRATION.md` §2 (`mode`, `progress`, `progressUrl`, `urlParams`, `resume`, `allowReset`, …). |

## 2. Topic file `topics/NN-name.json`

```json
{
  "id": "scroll-and-learn",           // unique, no "/" — used in URLs (#scroll-and-learn)
  "title": "Scroll and Learn",
  "duration": "8 min",                 // optional, shown in the kicker
  "summary": "md",                     // optional
  "objectives": ["md", "md"],          // optional bullet list
  "subsections": [
    { "id": "shift-register", "title": "Example", "blocks": [ { "type": "text", "md": "..." } ] }
  ],
  "quiz": { "title": "optional", "passThreshold": 0.8, "questions": [ ... ] }
}
```

Each subsection is shown as **one page**; the quiz is the last page of the topic (`#topic-id/quiz`).
No `quiz` → the last page ends with a **Mark topic as complete** button.

## 3. Blocks (inside `subsections[].blocks`)

| `type` | Fields | What the student sees |
|---|---|---|
| `text` | `md` | Paragraphs, lists. |
| `callout` | `kind`: `info`\|`tip`\|`warning`\|`key`, `title`, `md` | Coloured note box. |
| `image` | `src`, `alt`, `caption`, `width` (CSS), `zoom` (default true) | Picture; click opens the **zoom viewer**. |
| `svg` | `src`, `caption`, `controls` (Pause/Play), `zoom`, `width` | Inlined SVG (its own CSS animations run). |
| `compare` | `before`, `after`, `labels: [l, r]`, `caption` | **Before/after slider** (same-size pictures). |
| `accordion` | `items: [{title, md \| blocks, open}]`, `single` | **Click to expand** rows. |
| `tabs` | `tabs: [{label, md \| blocks}]` | **Multi tabs**. |
| `flipcards` | `md`, `cards: [{front, back}]` (md) | Cards that flip on click. |
| `reveal` | `src`, `hint`, `caption`, `layout` (`side` = explanation next to the picture; default: under it, picture full width), `spots: [{x,y,w,h,label,title,md,badge}]` | **Click to reveal** hotspots. `badge`: corner of the number — `tl` (default), `tr`, `bl`, `br`. |
| `scrolly` | `src` (SVG with `data-step`), `steps: [{title, md}]` | **Scroll and learn**: sticky picture follows the text. |
| `stepper` | `src` (SVG with `data-step`), `steps: [{title, md}]`, `interval` ms | Step player: picture, then Back / Play / Next (fixed place, also ← → keys), then the step text. |
| `sort` | `prompt`, `items` (in the **correct** order) | Drag-to-order practice (not graded). |
| `categorize` | `prompt`, `categories: [{id,label}]`, `items: [{text, category}]` | Drag-into-groups practice (not graded). |
| `code` | `language`, `code`, `caption` | Code with Copy button. |
| `table` | `columns`, `rows` (md cells), `caption` | Table. |
| `video` | `src` (`.mp4`/`.webm` or embed URL), `caption` | Video player. |

`accordion` items and `tabs` can contain any blocks (`"blocks": [...]`) — also nested.

### Hotspot coordinates
Keep picture labels out of the corner where the spot's number sits (top-left by default), or move the number with `badge`.
`x, y` = top-left corner, `w, h` = size, all in **percent of the picture**.
For an SVG `viewBox="0 0 800 500"`: `x = px_x / 8`, `y = px_y / 5`.

### Step animations (`scrolly`, `stepper`)
Inside the SVG mark elements:

```svg
<g data-step="1"> visible from step 1 on </g>
<g data-step="2" data-until="2"> visible only in step 2 </g>
```
The element(s) of the current step are highlighted, earlier steps are dimmed, later ones hidden.
Give the SVG its own white background `<rect>` so it reads well in dark themes.

### Continuous animations (`svg` block)
Put CSS animations inside the SVG (`<style>@keyframes …</style>`). With `"controls": true` a Pause/Play button freezes them.

## 4. Quiz questions (`quiz.questions[]`)

Common fields: `id`, `type`, `text` (md), `image` (optional), `review` (subsection ids to re-read when wrong), `explain` (md, shown per `showCorrectAnswers`).

| `type` | Fields | Correct when |
|---|---|---|
| `single` | `options`, `correct: [i]`, `shuffle` (default true) | the one option is selected |
| `truefalse` | `options: ["True","False"]`, `correct: [0 or 1]`, `"shuffle": false` | as `single` |
| `multiple` | `options`, `correct: [i, j, …]` | **exactly** the correct set is selected |
| `order` | `items` (in correct order) | final order equals `items` |
| `match` | `categories: [{id,label}]`, `items: [{text, category}]` | every item is in its category |
| `hotspot` | `src`, `spots: [{id,x,y,w,h}]`, `correct: [ids]` | exactly the correct spots are chosen |

Option indices start at **0**. Score = correct questions / all questions; pass when score ≥ threshold.
On a fail the result lists the `review` subsections as links, then **Try again** rebuilds the quiz (re-shuffled).

## 5. `certificate.json`

| Field | Meaning |
|---|---|
| `enabled` | `false` hides the certificate. |
| `title`, `subtitle`, `presented`, `body` | Texts. `subtitle` and `body` accept md. |
| placeholders | `{name}` `{training}` `{date}` `{score}` (average) `{hours}` `{id}` `{issuer}` |
| `issuer`, `logo` (image path) or `logoText` (2–3 letters in a circle) | Top line. |
| `signatures: [{name, role}]` | Signature lines. |
| `idPrefix` | Prefix of the certificate ID (ID is a hash of name + training + date). |
| `topicsList` | `true` lists all topic titles. |
| `sealText` | Text in the seal. |
| `style.design` | `classic` (double frame) \| `modern` (colour band) \| `minimal`. |
| `style.font` | `serif` \| `sans`. |
| `style.orientation` | `landscape` \| `portrait`. |
| `style.accent`, `accent2`, `paper`, `ink` | Colours. |
| `style.seal` | `false` hides the seal. |

Printing (*Print / save as PDF*) outputs only the certificate on one A4 page.
In preview mode (`?mode=preview`) the certificate page has live controls for these style fields and shows the resulting JSON.

## 6. Theme file `css/themes/<name>.css`

Only variables on `:root`:

`--bg --surface --surface-2 --text --heading --muted --accent --accent-ink --accent-soft --good --bad --warn --border --track --focus --radius --radius-sm --font --font-head --font-mono --font-size --shadow --shadow-sm --head-bg --head-ink --toc-bg --toc-ink --code-bg --code-ink --quiz-bg`

Copy `foundation.css`, change values, add the name to `themes` in `training.json`.
