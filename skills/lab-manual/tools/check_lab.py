#!/usr/bin/env python3
"""check_lab.py — check a lab folder before it goes into a SemiTec Learning Package (.stlp).

    python3 tools/check_lab.py [lab-manual-folder]        (folder that contains latex/ and lab/)

Checks lab/lab.json (title, steps, ids, quiz, review links), lab/manual.pdf, the source files ("files"),
and that the \\labstep ids in latex/sections/*.tex are the same as the steps in lab.json.
Exit code 1 when there are errors. The same rules are used by `stlp check` when the pack is created."""
import json, os, re, sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
LAB = os.path.join(ROOT, 'lab')
TEX = os.path.join(ROOT, 'latex')
ID = re.compile(r'^[a-z0-9][a-z0-9._-]{0,80}$')
QTYPES = {'single', 'truefalse', 'multiple', 'order', 'match', 'hotspot'}
errors, warnings = [], []
E = lambda m: errors.append(m)
W = lambda m: warnings.append(m)


def tex_steps():
    """[(id, title)] of \\labstep in the LaTeX sources, in order."""
    out = []
    sec = os.path.join(TEX, 'sections')
    files = sorted(os.listdir(sec)) if os.path.isdir(sec) else []
    for f in files:
        if not f.endswith('.tex'):
            continue
        txt = open(os.path.join(sec, f), encoding='utf-8').read()
        txt = re.sub(r'(?<!\\)%.*', '', txt)                       # drop comments
        for m in re.finditer(r'\\labstep\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}\s*\{([^}]*)\}', txt):
            out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def main():
    p = os.path.join(LAB, 'lab.json')
    if not os.path.isfile(p):
        E('lab/lab.json not found'); return None
    try:
        lab = json.load(open(p, encoding='utf-8'))
    except ValueError as e:
        E(f'lab/lab.json is not valid JSON — {e}'); return None
    if not lab.get('title'):
        E('lab.json: missing "title"')
    ph = re.findall(r'(?<![\w\]\)])\[[A-Za-z][^\]\n"]*\](?!\()', json.dumps(lab, ensure_ascii=False))
    if ph:
        W('lab.json still contains placeholders: ' + ', '.join(sorted(set(ph))[:5]))
    steps = lab.get('steps') or []
    if not steps:
        E('lab.json: no steps')
    sids = []
    for i, s in enumerate(steps):
        sid = s.get('id', '')
        if not ID.match(sid):
            E(f'step {i + 1}: id "{sid}" must be lowercase letters, digits, - . _')
        if sid in sids:
            E(f'duplicate step id "{sid}"')
        sids.append(sid)
        if not s.get('title'):
            E(f'step "{sid}": missing title')
    # manual
    if lab.get('manual'):
        mp = os.path.join(LAB, lab['manual'])
        if not os.path.isfile(mp):
            E(f'manual "{lab["manual"]}" not found in lab/ — run tools/build.py')
        elif open(mp, 'rb').read(5) != b'%PDF-':
            E(f'{lab["manual"]} is not a PDF')
    else:
        W('no "manual" — the lab has no PDF manual')
    # files
    src = []
    f = lab.get('files')
    if f is not None:
        entries = [f] if isinstance(f, str) else f if isinstance(f, list) else None
        if entries is None:
            E('"files" must be a folder name or a list of paths'); entries = []
        for ent in entries:
            rel = str(ent).rstrip('/')
            if not rel or rel.startswith('/') or '..' in rel.split('/'):
                E(f'files: "{ent}" must be a path inside lab/'); continue
            ap = os.path.join(LAB, rel)
            if os.path.isdir(ap):
                for r, ds, fs in os.walk(ap):
                    ds[:] = [d for d in ds if not d.startswith('.')]
                    src += [os.path.relpath(os.path.join(r, x), LAB).replace(os.sep, '/') for x in fs if not x.startswith('.')]
            elif os.path.isfile(ap):
                src.append(rel)
            else:
                E(f'files: not found {ent}')
        if not src:
            W('"files" lists no files')
    for s in steps:
        for x in s.get('files') or []:
            if x not in src:
                E(f'step "{s.get("id")}" links "{x}" which is not in "files"')
    # quiz
    q = lab.get('quiz')
    if not q:
        W('no check quiz')
    else:
        for i, x in enumerate(q.get('questions') or []):
            w = f'quiz q{i + 1}'
            t = x.get('type', 'single')
            if t not in QTYPES:
                E(f'{w}: unknown type "{t}"'); continue
            if t in ('single', 'truefalse', 'multiple'):
                n, c = len(x.get('options') or []), x.get('correct') or []
                if n < 2: E(f'{w}: needs 2+ options')
                if not c or any((not isinstance(k, int)) or k < 0 or k >= n for k in c): E(f'{w}: "correct" index out of range')
                if t != 'multiple' and len(c) != 1: E(f'{w}: type {t} needs exactly one correct answer')
            if not x.get('review'): W(f'{w}: no "review" step ids')
            for r in x.get('review') or []:
                if r not in sids: E(f'{w}: review "{r}" is not a step id')
    # LaTeX ↔ lab.json
    ts = tex_steps()
    if ts:
        tids = [t[0] for t in ts]
        for t in tids:
            if t not in sids: E(f'\\labstep{{{t}}} in the manual has no step in lab.json')
        for s in sids:
            if s not in tids: E(f'step "{s}" in lab.json has no \\labstep in the manual')
        if [s for s in sids if s in tids] != [t for t in tids if t in sids]:
            W('steps are in a different order in lab.json and in the manual')
        titles = dict(ts)
        for s in steps:
            if s.get('id') in titles and titles[s['id']] != s.get('title'):
                W(f'step "{s["id"]}": title differs — manual "{titles[s["id"]]}" / lab.json "{s.get("title")}"')
        if any(not s.get('manualPage') for s in steps if s.get('id') in tids) and lab.get('manual'):
            W('some steps have no "manualPage" — run tools/build.py to fill them')
    elif os.path.isdir(TEX):
        W('no \\labstep found in latex/sections — steps are not linked to the manual')
    return lab, src


if __name__ == '__main__':
    r = main()
    for w in warnings: print('  ⚠ ' + w)
    for e in errors: print('  ✗ ' + e)
    if r:
        lab, src = r
        print(f'\n{lab.get("title")}: {len(lab.get("steps") or [])} steps, {len(src)} source files, '
              f'quiz {len((lab.get("quiz") or {}).get("questions") or [])} questions — {len(errors)} error(s), {len(warnings)} warning(s)')
    sys.exit(1 if errors else 0)
