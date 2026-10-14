#!/usr/bin/env python3
"""build.py — build the lab manual and prepare the lab folder for a SemiTec Learning Package (.stlp).

    python3 tools/build.py [lab-manual-folder] [--sync-steps] [--update-style] [--no-check]

1. compiles latex/main.tex with latexmk (XeLaTeX + Biber); falls back to xelatex/biber/xelatex/xelatex
2. copies latex/main.pdf to lab/<manual> (default lab/manual.pdf)
3. writes the page of every \\labstep{id}{…} into lab.json → steps[].manualPage (the app's "Manual, page N" link)
   --sync-steps also adds steps that are in the manual but missing in lab.json (title from the manual)
4. runs tools/check_lab.py
Needs a TeX distribution with XeLaTeX (TeX Live, MacTeX, MiKTeX) and the FreeSerif fonts (gnu-freefont)."""
import json, os, re, shutil, subprocess, sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
ROOT = os.path.abspath(args[0] if args else os.path.join(os.path.dirname(__file__), '..'))
TEX, LAB = os.path.join(ROOT, 'latex'), os.path.join(ROOT, 'lab')
HERE = os.path.dirname(os.path.abspath(__file__))


STYLE = os.path.normpath(os.path.join(HERE, '..', 'latex'))   # the template's labstyle.sty + lang/


def ensure_style():
    """Every lab keeps its own copy of labstyle.sty, lang/ and .latexmkrc (so it also compiles on Overleaf).
    Missing files are copied from the template; --update-style replaces older copies."""
    if os.path.normpath(TEX) == STYLE:
        return
    upd = '--update-style' in sys.argv
    for rel in ['labstyle.sty', '.latexmkrc'] + ['lang/' + f for f in os.listdir(os.path.join(STYLE, 'lang'))]:
        src, dst = os.path.join(STYLE, rel), os.path.join(TEX, rel)
        if not os.path.exists(dst) or (upd and open(src, 'rb').read() != open(dst, 'rb').read()):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            print('   style: copied ' + rel)
        elif open(src, 'rb').read() != open(dst, 'rb').read():
            print(f'   style: {rel} differs from the template (run with --update-style to refresh)')


def run(cmd):
    print('  $ ' + ' '.join(cmd))
    r = subprocess.run(cmd, cwd=TEX, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        log = os.path.join(TEX, 'main.log')
        tail = open(log, encoding='utf-8', errors='replace').read()[-3000:] if os.path.exists(log) else r.stdout[-3000:]
        sys.exit('LaTeX failed:\n' + tail)


def compile_pdf():
    if shutil.which('latexmk'):
        run(['latexmk', '-xelatex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'])
    else:
        run(['xelatex', '-interaction=nonstopmode', 'main.tex'])
        if shutil.which('biber'): run(['biber', 'main'])
        run(['xelatex', '-interaction=nonstopmode', 'main.tex']); run(['xelatex', '-interaction=nonstopmode', 'main.tex'])


def step_pages():
    """{step id: page} from main.aux (\\newlabel{labstep:<id>}{{<n>}{<page>}…})"""
    pages = {}
    aux = os.path.join(TEX, 'main.aux')
    if os.path.exists(aux):
        for m in re.finditer(r'\\newlabel\{labstep:([^}]*)\}\{\{[^}]*\}\{(\d+)\}', open(aux, encoding='utf-8', errors='replace').read()):
            pages[m.group(1)] = int(m.group(2))
    return pages


def main():
    if not os.path.isfile(os.path.join(TEX, 'main.tex')):
        sys.exit('latex/main.tex not found in ' + ROOT)
    print('1. Compiling the manual')
    ensure_style()
    compile_pdf()
    p = os.path.join(LAB, 'lab.json')
    lab = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'title': '', 'steps': []}
    manual = lab.get('manual') or 'manual.pdf'
    lab['manual'] = manual
    os.makedirs(LAB, exist_ok=True)
    shutil.copyfile(os.path.join(TEX, 'main.pdf'), os.path.join(LAB, manual))
    print(f'2. Copied latex/main.pdf → lab/{manual}')
    pages = step_pages()
    if '--sync-steps' in sys.argv:
        sys.path.insert(0, HERE)
        import check_lab
        have = {s.get('id') for s in lab.get('steps', [])}
        for sid, title in check_lab.tex_steps():
            if sid not in have:
                lab.setdefault('steps', []).append({'id': sid, 'title': title, 'md': '[short instruction — the manual has the details]'})
                print(f'   + added step "{sid}" to lab.json')
    n = 0
    for s in lab.get('steps', []):
        if s.get('id') in pages and s.get('manualPage') != pages[s['id']]:
            s['manualPage'] = pages[s['id']]; n += 1
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(lab, f, indent=2, ensure_ascii=False); f.write('\n')
    print(f'3. Step pages: {len(pages)} steps found in the manual, {n} page number(s) updated in lab.json')
    if '--no-check' not in sys.argv:
        print('4. Checking the lab folder')
        r = subprocess.run([sys.executable, os.path.join(HERE, 'check_lab.py'), ROOT])
        sys.exit(r.returncode)


main()
