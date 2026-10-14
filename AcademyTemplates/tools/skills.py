#!/usr/bin/env python3
"""skills.py — maintain and install the Academy Templates skills.

Academy Templates is a Claude Code plugin (`academy-templates`) with one skill per template in
skills/<name>/SKILL.md. In Claude Code the skills are called `academy-templates:<name>`; installed on
their own (Claude app, ~/.claude/skills) they are called `academy-<name>`.

    python3 tools/skills.py list                  the skills, their names and what they need
    python3 tools/skills.py check                 frontmatter, files named in SKILL.md, README, plugin
                                                  manifest, dist/ zips up to date — exit code 1 on errors
    python3 tools/skills.py zip                   build dist/academy-<name>.zip for every skill
                                                  (upload in the Claude app: Settings → Skills)
    python3 tools/skills.py install [--project DIR]
                                                  copy every skill as academy-<name> into ~/.claude/skills
                                                  (or DIR/.claude/skills) — for use without the plugin
    python3 tools/skills.py plugin                print how to add the plugin to Claude Code

A skill folder name is the skill name: lowercase letters, digits and '-', at most 64 characters."""
import io, json, os, re, shutil, sys, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKILLS = os.path.join(ROOT, 'skills')
DIST = os.path.join(ROOT, 'dist')
MARKET = os.path.abspath(os.path.join(ROOT, '..'))
PREFIX = 'academy-'
NAME = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$')
REF = re.compile(r'`((?:reference|examples|scripts|tools|latex|lab|templates|sections|css|js|topics|assets|slides)/[^`\s*<>]*)`')
JUNK = re.compile(r'(^|/)(\.DS_Store|__pycache__|.*\.pyc|.*\.(aux|log|toc|out|fls|fdb_latexmk|xdv|bbl|bcf|blg|run\.xml|synctex\.gz))$')
NEEDS = {'project-brief': 'XeLaTeX', 'diploma-project': 'pdfLaTeX / XeLaTeX', 'lab-manual': 'XeLaTeX, Python 3',
         'training': 'Python 3 (checks, single-file build)', 'package': 'Node.js 18+'}


def skills():
    return [os.path.join(SKILLS, d) for d in sorted(os.listdir(SKILLS))
            if os.path.isfile(os.path.join(SKILLS, d, 'SKILL.md'))]


def frontmatter(txt):
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.S)
    if not m:
        return None
    fm, key = {}, None
    for line in m.group(1).split('\n'):
        k = re.match(r'^([a-zA-Z_-]+):\s*(.*)$', line)
        if k:
            key = k.group(1); val = k.group(2).strip()
            fm[key] = '' if val in ('>-', '>', '|', '|-') else val
        elif key and line.startswith(' '):
            fm[key] = (fm[key] + ' ' + line.strip()).strip()
    return fm


def read(p):
    return open(p, encoding='utf-8').read()


def standalone_skill_md(d):
    """SKILL.md with the stand-alone name academy-<name>."""
    txt = read(os.path.join(d, 'SKILL.md'))
    return re.sub(r'^name: *(.*)$', lambda m: 'name: ' + PREFIX + m.group(1).strip(), txt, count=1, flags=re.M)


def files_of(d):
    for r, ds, fs in os.walk(d):
        ds[:] = sorted(x for x in ds if x not in ('node_modules_unused', '__pycache__') and (not x.startswith('.') or x == '.latexmkrc'))
        for f in sorted(fs):
            rp = os.path.relpath(os.path.join(r, f), d).replace(os.sep, '/')
            if not JUNK.search(rp):
                yield rp


def zip_name(d):
    return os.path.join(DIST, PREFIX + os.path.basename(d) + '.zip')


def check():
    bad = 0
    plugin = os.path.join(ROOT, '.claude-plugin', 'plugin.json')
    try:
        pj = json.load(open(plugin))
        print(f'plugin {pj.get("name")} {pj.get("version")}  ({os.path.relpath(plugin, MARKET)})')
        if pj.get('name') != 'academy-templates': print('    ✗ plugin name must be academy-templates'); bad += 1
    except Exception as e:
        print(f'✗ {os.path.relpath(plugin, MARKET)}: {e}'); bad += 1
    try:
        mj = json.load(open(os.path.join(MARKET, '.claude-plugin', 'marketplace.json')))
        if not any(p.get('name') == 'academy-templates' for p in mj.get('plugins', [])):
            print('    ✗ marketplace.json does not list academy-templates'); bad += 1
    except Exception as e:
        print(f'⚠ marketplace.json: {e}')
    print()
    for d in skills():
        base = os.path.basename(d)
        errs, warns = [], []
        txt = read(os.path.join(d, 'SKILL.md'))
        fm = frontmatter(txt)
        if fm is None:
            errs.append('SKILL.md has no YAML frontmatter (--- name / description ---)'); fm = {}
        n, desc = fm.get('name', ''), fm.get('description', '')
        if n != base: errs.append(f'name "{n}" must be the folder name "{base}"')
        if not NAME.match(base) or len(PREFIX + base) > 64: errs.append('folder name: lowercase letters, digits and -, max 64 with the academy- prefix')
        if 'claude' in base or 'anthropic' in base: errs.append('name must not contain "claude" or "anthropic"')
        if not desc: errs.append('description missing')
        elif len(desc) > 1024: errs.append(f'description too long ({len(desc)} > 1024)')
        if not os.path.exists(os.path.join(d, 'README.md')): warns.append('no README.md')
        for ref in sorted(set(REF.findall(txt))):
            p = ref.rstrip('/').split('#')[0]
            if any(c in p for c in '…<*['):
                continue
            if not os.path.isdir(os.path.join(d, p.split('/')[0])) and '.' not in p.split('/')[-1]:
                continue                     # a folder of something else (e.g. the lab/ of a user's lab)
            if not os.path.exists(os.path.join(d, p)): warns.append(f'SKILL.md mentions `{ref}`, not found in the skill folder')
        z = zip_name(d)
        if not os.path.exists(z): warns.append(f'no dist/{os.path.basename(z)} (run: skills.py zip)')
        else:
            with zipfile.ZipFile(z) as zf:
                inner = PREFIX + base + '/SKILL.md'
                if inner not in zf.namelist() or zf.read(inner).decode('utf-8') != standalone_skill_md(d):
                    warns.append(f'dist/{os.path.basename(z)} is out of date (run: skills.py zip)')
        state = '✗' if errs else '⚠' if warns else '✓'
        print(f'{state} academy-templates:{base:18s} skills/{base}')
        for e in errs: print('    ✗ ' + e)
        for w in warns: print('    ⚠ ' + w)
        bad += len(errs)
    print(f'\n{len(skills())} skills, {bad} error(s)')
    return bad


def make_zips():
    os.makedirs(DIST, exist_ok=True)
    for d in skills():
        base, z = os.path.basename(d), zip_name(d)
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
            for rp in files_of(d):
                arc = PREFIX + base + '/' + rp
                if rp == 'SKILL.md': zf.writestr(arc, standalone_skill_md(d))
                else: zf.write(os.path.join(d, rp), arc)
        print(f'zipped dist/{os.path.basename(z)} ({os.path.getsize(z) // 1024} KB)')


def install(argv):
    target = os.path.expanduser('~/.claude/skills')
    if '--project' in argv:
        target = os.path.join(os.path.abspath(argv[argv.index('--project') + 1]), '.claude', 'skills')
    os.makedirs(target, exist_ok=True)
    for d in skills():
        name = PREFIX + os.path.basename(d)
        dst = os.path.join(target, name)
        if os.path.islink(dst) or os.path.isfile(dst): os.remove(dst)
        elif os.path.isdir(dst): shutil.rmtree(dst)
        for rp in files_of(d):
            os.makedirs(os.path.dirname(os.path.join(dst, rp)), exist_ok=True)
            if rp == 'SKILL.md': open(os.path.join(dst, rp), 'w', encoding='utf-8').write(standalone_skill_md(d))
            else: shutil.copy2(os.path.join(d, rp), os.path.join(dst, rp))
        print(f'installed {name:26s} → {dst}')
    print('\nStart a new Claude Code session to load them (/skills lists them).'
          '\nTip: the plugin (python3 tools/skills.py plugin) gives the same skills as academy-templates:<name>.')


def plugin():
    print(f'''Academy Templates as a Claude Code plugin

  In Claude Code:
    /plugin marketplace add {MARKET}
    /plugin install academy-templates@semitec-skills

  From a terminal:
    claude plugin marketplace add {MARKET}
    claude plugin install academy-templates@semitec-skills

  Try without installing (one session, edits are live):
    claude --plugin-dir {ROOT}

  After changes: /plugin marketplace update semitec-skills  (and raise "version" in .claude-plugin/plugin.json)''')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd == 'list':
        for d in skills():
            fm = frontmatter(read(os.path.join(d, 'SKILL.md'))) or {}
            b = os.path.basename(d)
            print(f'academy-templates:{b:16s} {PREFIX + b:26s} needs {NEEDS.get(b, "-")}')
    elif cmd == 'check': sys.exit(1 if check() else 0)
    elif cmd == 'zip': make_zips()
    elif cmd == 'install': install(sys.argv[2:])
    elif cmd == 'plugin': plugin()
    else: print(__doc__); sys.exit(1)
