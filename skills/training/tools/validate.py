#!/usr/bin/env python3
"""Validate a training folder: JSON syntax, ids, block/question types, review links,
correct answers and referenced files.   Usage:  python3 tools/validate.py [training-folder]"""
import json, os, re, sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
BLOCKS = {'text', 'callout', 'image', 'svg', 'compare', 'accordion', 'tabs', 'flipcards', 'reveal',
          'scrolly', 'stepper', 'sort', 'categorize', 'code', 'table', 'video'}
QTYPES = {'single', 'truefalse', 'multiple', 'order', 'match', 'hotspot'}
errors, warnings = [], []
LOCAL_WEB_ENTRY = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._/-]*\.html?$')

def err(where, msg): errors.append(f'{where}: {msg}')
def warn(where, msg): warnings.append(f'{where}: {msg}')

def load(rel):
    p = os.path.join(ROOT, rel)
    try:
        with open(p, encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError: err(rel, 'file not found')
    except json.JSONDecodeError as e: err(rel, f'invalid JSON — {e}')

def asset(where, src):
    if not src: err(where, 'missing "src"'); return
    if src.startswith(('http://', 'https://', 'data:', '<svg')): return
    if not os.path.isfile(os.path.join(ROOT, src)): err(where, f'file not found: {src}')

def local_web_entry(value):
    if not isinstance(value, str) or not LOCAL_WEB_ENTRY.fullmatch(value): return False
    return all(part not in ('.', '..') for part in value.split('/'))

def print_result(topics, label='topics'):
    for w in warnings: print('WARN ', w)
    for e in errors: print('ERROR', e)
    print(f'\n{topics} {label} checked — {len(errors)} error(s), {len(warnings)} warning(s).')

def spots(where, sp, need_id=False):
    for i, s in enumerate(sp or []):
        for k in ('x', 'y', 'w', 'h'):
            if not isinstance(s.get(k), (int, float)): err(f'{where} spot {i+1}', f'"{k}" must be a number (percent)')
        if (s.get('x', 0) + s.get('w', 0) > 100.5) or (s.get('y', 0) + s.get('h', 0) > 100.5): warn(f'{where} spot {i+1}', 'extends beyond the picture (x+w or y+h > 100)')
        if need_id and not s.get('id'): err(f'{where} spot {i+1}', 'missing "id"')

def block(where, b):
    t = b.get('type')
    if t not in BLOCKS: err(where, f'unknown block type "{t}"'); return
    if t in ('image', 'svg', 'scrolly', 'stepper', 'reveal'): asset(where, b.get('src'))
    if t == 'compare': asset(where, b.get('before')); asset(where, b.get('after'))
    if t == 'video' and not b.get('src'): err(where, 'missing "src"')
    if t in ('scrolly', 'stepper'):
        if not b.get('steps'): err(where, 'needs "steps"')
        src = b.get('src', '')
        p = os.path.join(ROOT, src)
        if os.path.isfile(p) and 'data-step' not in open(p, encoding='utf-8').read(): warn(where, f'{src} has no data-step elements')
    if t == 'reveal': spots(where, b.get('spots'))
    if t == 'sort' and len(b.get('items', [])) < 2: err(where, 'sort needs at least 2 items')
    if t == 'categorize':
        cats = {c.get('id') for c in b.get('categories', [])}
        for it in b.get('items', []):
            if it.get('category') not in cats: err(where, f'item "{it.get("text")}" has unknown category "{it.get("category")}"')
    if t == 'accordion':
        for i, it in enumerate(b.get('items', [])):
            for j, bb in enumerate(it.get('blocks', [])): block(f'{where} > item {i+1} block {j+1}', bb)
    if t == 'tabs':
        for i, it in enumerate(b.get('tabs', [])):
            for j, bb in enumerate(it.get('blocks', [])): block(f'{where} > tab {i+1} block {j+1}', bb)
    if t == 'table':
        n = len(b.get('columns', []))
        for r in b.get('rows', []):
            if len(r) != n: warn(where, f'row has {len(r)} cells, table has {n} columns')

def question(where, q, subs):
    t = q.get('type', 'single')
    if t not in QTYPES: err(where, f'unknown question type "{t}"'); return
    if not q.get('text'): err(where, 'missing "text"')
    if t in ('single', 'truefalse', 'multiple'):
        n, c = len(q.get('options', [])), q.get('correct', [])
        if n < 2: err(where, 'needs at least 2 options')
        if not c: err(where, '"correct" is empty')
        if any((not isinstance(i, int)) or i < 0 or i >= n for i in c): err(where, f'"correct" index out of range (0..{n-1})')
        if t in ('single', 'truefalse') and len(c) != 1: err(where, f'type "{t}" must have exactly one correct index — use "multiple"')
    if t == 'order' and len(q.get('items', [])) < 2: err(where, 'order needs at least 2 items')
    if t == 'match':
        cats = {c.get('id') for c in q.get('categories', [])}
        for it in q.get('items', []):
            if it.get('category') not in cats: err(where, f'item "{it.get("text")}" has unknown category')
    if t == 'hotspot':
        asset(where, q.get('src')); spots(where, q.get('spots'), True)
        ids = {s.get('id') for s in q.get('spots', [])}
        if not q.get('correct'): err(where, '"correct" is empty')
        for c in q.get('correct', []):
            if c not in ids: err(where, f'correct spot "{c}" is not in spots')
    if not q.get('review'): warn(where, 'no "review" subsections — a failed student gets no reading hint')
    for r in q.get('review', []):
        if r not in subs: err(where, f'review "{r}" is not a subsection id of this topic')

def main():
    tr = load('training.json')
    if not tr: return
    for k in ('id', 'title'):
        if not tr.get(k): err('training.json', f'missing "{k}"')
    fmt = tr.get('format', 1)
    if fmt not in (1, 2):
        err('training.json', '"format" must be 1 (Academy JSON) or 2 (custom web training)')
        print_result(0, 'custom web trainings')
        return
    if fmt == 2:
        runtime = tr.get('runtime')
        if not isinstance(runtime, dict):
            err('training.json', 'format 2 needs "runtime": { "kind": "web", "entry": "index.html" }')
        else:
            for key in runtime:
                if key not in ('kind', 'entry'): err('training.json runtime', f'unknown field "{key}"')
            if runtime.get('kind') != 'web': err('training.json runtime', '"kind" must be "web"')
            entry = runtime.get('entry')
            if not local_web_entry(entry):
                err('training.json runtime', '"entry" must be a local .html file inside this training, such as "index.html"')
            else:
                root = os.path.realpath(ROOT)
                target = os.path.realpath(os.path.join(ROOT, entry))
                if os.path.commonpath((root, target)) != root or not os.path.isfile(target):
                    err('training.json runtime', f'entry file not found: {entry}')
        if tr.get('certificate'):
            err('training.json', 'format 2 does not support an individual training certificate; use an optional package certificate instead')
        print_result(1, 'custom web training')
        return
    if not tr.get('topics'): err('training.json', 'missing "topics"')
    thr = tr.get('passThreshold', 0.8)
    if not (0 < thr <= 1): err('training.json', 'passThreshold must be between 0 and 1 (e.g. 0.8)')
    if tr.get('layout', 'sidebar') not in ('sidebar', 'topbar'): err('training.json', 'layout must be "sidebar" or "topbar"')
    dl = tr.get('delivery', {})
    if dl.get('mode', 'standalone') not in ('standalone', 'preview', 'platform'): err('training.json', 'delivery.mode must be standalone, preview or platform')
    if dl.get('progress') and dl['progress'] not in ('local', 'none', 'rest', 'postMessage', 'custom'): err('training.json', 'delivery.progress must be local, none, rest, postMessage or custom')
    if dl.get('progress') == 'rest' and not dl.get('progressUrl'): err('training.json', 'delivery.progress "rest" needs delivery.progressUrl')
    for th in set(tr.get('themes', []) + [tr.get('theme', 'foundation')]):
        if not os.path.isfile(os.path.join(ROOT, 'css', 'themes', th + '.css')): err('training.json', f'theme file css/themes/{th}.css not found')
    topic_ids = set()
    for f in tr.get('topics', []):
        rel = 'topics/' + f
        t = load(rel)
        if not t: continue
        tid = t.get('id')
        if not tid: err(rel, 'missing "id"')
        elif tid in topic_ids: err(rel, f'duplicate topic id "{tid}"')
        topic_ids.add(tid)
        if not t.get('title'): err(rel, 'missing "title"')
        subs = []
        for i, s in enumerate(t.get('subsections', [])):
            w = f'{rel} > {s.get("id", "subsection " + str(i+1))}'
            if not s.get('id'): err(w, 'missing "id"')
            elif s['id'] in subs: err(w, 'duplicate subsection id')
            subs.append(s.get('id'))
            if '/' in (s.get('id') or ''): err(w, 'id must not contain "/"')
            for j, b in enumerate(s.get('blocks', [])): block(f'{w} block {j+1}', b)
        quiz = t.get('quiz')
        if not quiz or not quiz.get('questions'): warn(rel, 'no quiz — topic is completed with a button')
        else:
            qt = quiz.get('passThreshold', thr)
            if not (0 < qt <= 1): err(rel, 'quiz passThreshold must be between 0 and 1')
            for i, q in enumerate(quiz['questions']): question(f'{rel} > quiz q{i+1}', q, subs)
    sc = tr.get('schedule')
    if sc:   # optional study plan: { "weeks": N, "topics": [ { "week": 1 | "weeks": [2, 3], "topics": [ids] } ] }
        n = sc.get('weeks')
        if not isinstance(n, int) or not 1 <= n <= 104: err('training.json', 'schedule.weeks must be a whole number 1–104')
        planned = set()
        for i, x in enumerate(sc.get('topics', [])):
            wk = x.get('weeks', x.get('week'))
            span = wk if isinstance(wk, list) else [wk, wk]
            if not all(isinstance(v, int) and v >= 1 for v in span) or (isinstance(n, int) and span[-1] > n):
                err('training.json', f'schedule.topics[{i}]: week must be within 1–{n}')
            for tid in x.get('topics', []):
                if tid not in topic_ids: err('training.json', f'schedule.topics[{i}]: unknown topic id "{tid}"')
                planned.add(tid)
        missing = [t for t in topic_ids if t not in planned]
        if missing: warn('training.json', 'schedule: topics without a week: ' + ', '.join(sorted(missing)))
    if tr.get('certificate'):
        c = load(tr['certificate'])
        if c:
            d = c.get('style', {}).get('design', 'classic')
            if d not in ('classic', 'modern', 'minimal'): err(tr['certificate'], f'unknown design "{d}"')
            if c.get('logo'): asset(tr['certificate'], c['logo'])
    print_result(len(tr.get("topics", [])))

main()
sys.exit(1 if errors else 0)
