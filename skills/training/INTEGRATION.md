# Integration guide — standalone, preview, platform

A training is a static folder (or one HTML file). It never talks to a database directly.
Instead it keeps **one JSON object per user and training** — the *state* — and hands it to a
**progress adapter**. Pick the adapter that fits your platform; nothing in the training changes.

```
            ┌──────────── training (browser) ────────────┐
 student →  │ pages · quizzes · certificate               │
            │        │ state (JSON)                       │
            │   progress adapter ── local | none | rest | postMessage | custom
            └────────┼────────────────────────────────────┘
                     ▼
     browser storage · nothing · your REST API · your host page · your JS code  →  your DB
```

---

## 1. Delivery modes

| Mode | Topics | Progress | How to open |
|---|---|---|---|
| `standalone` (default) | unlocked one by one by quizzes | browser `localStorage` | `index.html`, `dist/training.html` |
| `preview` | **all open**, certificate preview with style controls | not saved | `index.html?mode=preview`, `dist/training-preview.html` |
| `platform` | unlocked by quizzes | **your platform** (REST, iframe or JS adapter) | embedded by the platform, see §3 |

In every mode the student reads **one subsection per page**, scrolls inside it and moves on with
**Next** (or the topic pills / contents). The last page of a topic is its quiz.

Build both shareable files at once: `python3 tools/build_single_file.py` →
`dist/training.html` (standalone) and `dist/training-preview.html` (preview).

## 2. Configuration

The configuration is merged in this order (later wins):

1. defaults
2. `training.json → "delivery"`
3. `window.TRAINING_CONFIG` (set by the page that hosts the training)
4. URL parameters (only when `urlParams` is `true`)

| Key | URL parameter | Default | Meaning |
|---|---|---|---|
| `mode` | `mode` | `standalone` | `standalone` \| `preview` \| `platform` |
| `progress` | `progress` | automatic* | `local` \| `none` \| `rest` \| `postMessage` \| `custom` |
| `user` | `userId`, `userName` | `null` | `{ "id": "...", "name": "..." }`; the name fills the certificate |
| `lockName` | — | `false` | `true` = the student cannot change the certificate name |
| `progressUrl` | `progressUrl` | — | REST URL, may contain `{trainingId}` and `{userId}` |
| `token` | `token` | — | sent as `Authorization: Bearer <token>` (REST) |
| `headers` | — | — | extra HTTP headers (REST) |
| `credentials` | — | `same-origin` | fetch credentials (`include` for cookies on another domain) |
| `saveMethod` | — | `PUT` | `PUT` or `POST` |
| `adapter` | — | — | `{ load(trainingId, user), save(state, trainingId, user) }` (custom) |
| `parentOrigin` | `parentOrigin` | `*` | origin of the host page (iframe); set it in production |
| `initTimeout` | — | `4000` | ms to wait for the host page's `init` message |
| `resume` | — | `true` | open the last visited page when no `#page` is given |
| `allowReset` | — | `true` (not in platform) | show *Reset progress* in the View menu |
| `postMessage` | — | `true` | send events to a parent frame |
| `urlParams` | — | `true` | allow the URL to change the settings above |

\* automatic `progress`: preview → `none`; platform → `custom` if `adapter`, `rest` if `progressUrl`,
`postMessage` if inside an iframe, otherwise `local`; standalone → `local`.

> **Production:** set `urlParams: false` in `window.TRAINING_CONFIG` or `training.json`
> so a student cannot open `?mode=preview` or change the user id.

## 3. Platform integration — three options

### 3a. REST (simplest for a web platform with a database)

Your backend implements two endpoints; the training calls them.

```
GET  {progressUrl}   → 200 + state JSON      (404 or 204 = no progress yet)
PUT  {progressUrl}   ← state JSON            → 2xx
```

Open the training with:

```
https://your.site/trainings/ecc/index.html?mode=platform&progressUrl=/api/progress/{trainingId}/me
```

or render a config block into the page (preferred — no URL tricks):

```html
<script>
  window.TRAINING_CONFIG = {
    mode: 'platform', urlParams: false,
    user: { id: '42', name: 'Anna Petrosyan' }, lockName: true,
    progressUrl: '/api/progress/{trainingId}/me',   // the server knows who "me" is from the session
    credentials: 'include'                           // send the session cookie
  };
</script>
```

Your server must **identify the user from the session or token**, never trust `{userId}` from
the browser alone. `tools/dev_server.py` is a working reference implementation (no auth):

```
python3 tools/dev_server.py   →  http://localhost:8000/examples/
```

### 3b. iframe + postMessage (platform page owns the data)

Embed `index.html?mode=platform` in an `<iframe>`. The training and the host page exchange
messages; the host stores the state wherever it wants. Working demo: `examples/platform-iframe.html`.

```js
const frame = document.querySelector('#training');
window.addEventListener('message', (e) => {
  if (e.source !== frame.contentWindow || e.data?.source !== 'semitec-training') return;
  const { type, detail, trainingId } = e.data;
  if (type === 'requestState') {                       // training asks for saved progress
    loadFromMyDb(trainingId).then(state => frame.contentWindow.postMessage(
      { target: 'semitec-training', type: 'init', state, user: { id: '42', name: 'Anna' }, lockName: true },
      'https://trainings.your.site'));
  }
  if (type === 'progress') saveToMyDb(trainingId, detail.state);   // every change
  if (type === 'completed') markCourseDone(trainingId);
});
```

Messages **to** the training (`{ target: 'semitec-training', type, ... }`):

| `type` | Fields | Effect |
|---|---|---|
| `init` | `state`, `user`, `lockName` | answer to `requestState` (if no answer within `initTimeout`, the training starts empty) |
| `navigate` | `hash` (e.g. `#certificate`, `#topic/quiz`) | open a page |
| `getState` | — | the training answers with a `state` event |
| `reset` | — | clears the user's progress (then a `progress` event with the empty state) |

### 3c. Same page, JavaScript adapter

When the platform renders the training into its own page, give it an adapter object.
Demo: `examples/platform-same-page.html`.

```js
window.TRAINING_CONFIG = {
  mode: 'platform', urlParams: false,
  user: { id: '42', name: 'Anna Petrosyan' },
  adapter: {
    load: (trainingId, user) => fetch(`/api/u/${user.id}/t/${trainingId}`).then(r => r.ok ? r.json() : null),
    save: (state, trainingId, user) => fetch(`/api/u/${user.id}/t/${trainingId}`, { method: 'PUT', body: JSON.stringify(state) })
  }
};
```

`load` and `save` may return a value or a Promise. If the training files live in another folder,
add `<base href="path/to/training/">` to the page.

## 4. Events (for analytics, notifications, grades)

Every event is sent three ways: a DOM event `training:<type>` on `document`, `TrainingAPI.on(type, fn)`,
and — inside an iframe — `postMessage({ source: 'semitec-training', type, trainingId, detail })`.

| Event | `detail` |
|---|---|
| `ready` | `{ mode, progress, percent, state }` |
| `requestState` | `{ trainingId }` (iframe adapter only) |
| `pageView` | `{ topicId, page, index, pages }` |
| `progress` | `{ reason, state, detail }` — reason: `visit`, `position`, `quiz`, `complete`, `completed`, `certificate`, `reset` |
| `quizAttempt` | `{ topicId, score, passed, correct, total, wrong: [questionIds], threshold }` |
| `topicPassed` | `{ topicId, score }` |
| `completed` | `{ completedAt, averageScore, state }` — all topics passed (once) |
| `certificate` | `{ name, id, issuedAt, score }` |
| `saved` / `error` | save confirmation / `{ where: 'load' \| 'save', message }` |

JavaScript API on the training page: `TrainingAPI.getState()`, `.navigate(hash)`, `.reset()`,
`.flush()` (save now), `.on(type, fn)`, `.getConfig()`.

## 5. State format (schema 1)

```json
{
  "schema": 1,
  "trainingId": "training-template-tour",
  "trainingVersion": "1.0",
  "user": { "id": "42", "name": "Anna Petrosyan" },
  "startedAt": "2026-10-13T09:00:00.000Z",
  "updatedAt": "2026-10-13T10:12:31.000Z",
  "completedAt": null,
  "percent": 30,
  "last": "click-to-expand/flipcards",
  "topics": {
    "welcome": {
      "visited": ["navigation", "quizzes", "content-source"],
      "passed": true, "score": 1, "bestScore": 1, "passedAt": "2026-10-13T09:20:00.000Z",
      "attempts": [
        { "date": "...", "score": 0.5, "passed": false, "correct": 2, "total": 4, "wrong": ["q1", "q3"] },
        { "date": "...", "score": 1,   "passed": true,  "correct": 4, "total": 4, "wrong": [] }
      ]
    }
  },
  "certificate": { "name": "Anna Petrosyan", "id": "SF-1X2Y3Z", "issuedAt": "...", "score": 0.95 }
}
```

- `percent` = share of passed topics; `last` = page to resume (`topic/subsection` or `topic/quiz`).
- At most 20 attempts per topic are kept. Typical size: 2–10 KB.
- Store it as-is (JSON/JSONB column). Keep `trainingVersion` to notice content updates.
- Topic and subsection **ids must stay stable** after publishing; new topics simply appear as not passed.

## 6. Suggested database tables

```sql
CREATE TABLE training_progress (
  user_id       VARCHAR(64)  NOT NULL,
  training_id   VARCHAR(120) NOT NULL,
  state         JSONB        NOT NULL,      -- the whole state object
  percent       SMALLINT     NOT NULL DEFAULT 0,
  completed_at  TIMESTAMPTZ,
  updated_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, training_id)
);
-- optional: one row per quiz attempt, for statistics (fill it from the quizAttempt event or from state)
CREATE TABLE training_quiz_attempt (
  id BIGSERIAL PRIMARY KEY, user_id VARCHAR(64), training_id VARCHAR(120), topic_id VARCHAR(120),
  score REAL, passed BOOLEAN, wrong_questions TEXT[], created_at TIMESTAMPTZ DEFAULT now()
);
-- optional: issued certificates, for public verification by id
CREATE TABLE training_certificate (
  certificate_id VARCHAR(40) PRIMARY KEY, user_id VARCHAR(64), training_id VARCHAR(120),
  name TEXT, score REAL, issued_at TIMESTAMPTZ
);
```

On `PUT`: upsert `state`, copy `percent` and `completedAt` into their columns (handy for lists and reports).

## 7. Security notes

- Quiz checking runs in the browser, and the correct answers are inside the topic JSON. That is fine
  for **learning** and self-paced certificates; for **graded exams** check answers on the server.
- Use `urlParams: false` on a platform; authenticate REST calls (session cookie or token);
  derive the user from the session on the server.
- With iframes set `parentOrigin` (training side) and the exact target origin in `postMessage` (host side).
- The certificate ID is a hash of name + training + date. To make certificates verifiable, store
  issued certificates (`certificate` event) and offer a lookup page.

## 8. LMS (Moodle, SCORM, xAPI)

The custom adapter is the bridge. Example for a SCORM 2004 package (`suspend_data` up to 64 000 characters):

```js
const api = window.parent.API_1484_11;   // provided by the LMS
api.Initialize('');
window.TRAINING_CONFIG = {
  mode: 'platform',
  user: { id: api.GetValue('cmi.learner_id'), name: api.GetValue('cmi.learner_name') },
  adapter: {
    load: () => { const s = api.GetValue('cmi.suspend_data'); return s ? JSON.parse(s) : null; },
    save: (state) => {
      api.SetValue('cmi.suspend_data', JSON.stringify(state));
      api.SetValue('cmi.progress_measure', String(state.percent / 100));
      if (state.completedAt) { api.SetValue('cmi.completion_status', 'completed'); api.SetValue('cmi.success_status', 'passed'); }
      api.Commit('');
    }
  }
};
```

(Packaging as a SCORM zip additionally needs an `imsmanifest.xml`; not included in this template.)

## 9. Checklist for a platform developer

1. Host the training folder (or `dist/training.html`) on your web server.
2. Choose REST, iframe or same-page; set `mode: 'platform'`, `urlParams: false`, `user`, `lockName`.
3. Store the state JSON per user + training; return it unchanged on load.
4. Listen to `completed` / `certificate` events if the platform should react (badges, grades, e-mail).
5. Test with two users and two browsers: progress must follow the user, not the browser.
