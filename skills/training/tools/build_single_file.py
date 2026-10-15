#!/usr/bin/env python3
"""Bundle a training into ONE self-contained HTML file (opens by double-click, no server).
Inlines CSS, JS, all JSON files, all themes and turns asset paths into data: URIs.

Usage:
  python3 tools/build_single_file.py                      -> dist/training.html (standalone, progress in the browser)
                                                             dist/training-preview.html (preview: everything open)
  python3 tools/build_single_file.py --mode preview --out share.html
  python3 tools/build_single_file.py path/to/training --mode standalone
A mode baked into the file can still be overridden by ?mode=... unless training.json delivery.urlParams is false."""
import argparse, base64, json, mimetypes, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument('root', nargs='?', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ap.add_argument('--mode', choices=['standalone', 'preview', 'platform', 'both'], default='both')
ap.add_argument('--out', help='output file (only with a single --mode)')
args = ap.parse_args()
ROOT = os.path.abspath(args.root)
read = lambda rel: open(os.path.join(ROOT, rel), encoding='utf-8').read()
loadj = lambda rel: json.loads(read(rel))

def data_uri(rel):
    p = os.path.join(ROOT, rel)
    mime = mimetypes.guess_type(p)[0] or 'application/octet-stream'
    if rel.endswith('.svg'): mime = 'image/svg+xml'
    with open(p, 'rb') as f: return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()

def embed_assets(obj):
    """Replace every string that is a path to an existing local file by a data: URI."""
    if isinstance(obj, dict): return {k: embed_assets(v) for k, v in obj.items()}
    if isinstance(obj, list): return [embed_assets(v) for v in obj]
    if isinstance(obj, str) and re.match(r'^[\w./-]+\.(svg|png|jpe?g|gif|webp|mp4|webm)$', obj, re.I) \
            and os.path.isfile(os.path.join(ROOT, obj)):
        return data_uri(obj)
    return obj

tr = loadj('training.json')
files = {'training.json': tr}
for f in tr.get('topics', []): files['topics/' + f] = embed_assets(loadj('topics/' + f))
if tr.get('certificate'): files[tr['certificate']] = embed_assets(loadj(tr['certificate']))
themes = list(dict.fromkeys(tr.get('themes') or ['foundation', 'midnight', 'paper']) )
if tr.get('theme', 'foundation') not in themes: themes.insert(0, tr.get('theme', 'foundation'))

def build(mode, out):
    html = read('index.html')
    def css_tag(m):
        href = m.group(1)
        if 'themes/' in href: return ''
        return '<style>\n' + read(href) + '\n</style>'
    html = re.sub(r'<link rel="stylesheet"[^>]*?href="([^"]+)"[^>]*>', css_tag, html)
    default = tr.get('theme', 'foundation')
    theme_css = '\n'.join(f'<style data-theme="{t}"{"" if t == default else " disabled"}>\n{read("css/themes/" + t + ".css")}\n</style>' for t in themes)
    html = html.replace('</head>', theme_css + '\n<link id="theme-css">\n</head>')
    payload = json.dumps({'files': files, 'themes': themes}, ensure_ascii=False).replace('</', '<\\/')
    boot = '<script>window.TRAINING_DATA = ' + payload + ';\n  window.TRAINING_CONFIG = Object.assign({ mode: ' + json.dumps(mode) + ' }, window.TRAINING_CONFIG || {});</script>'
    html = html.replace('<script src="js/md.js"></script>', boot + '\n  <script src="js/md.js"></script>')
    html = re.sub(r'<script src="([^"]+)"></script>', lambda m: '<script>\n' + read(m.group(1)).replace('</script', '<\\/script') + '\n</script>', html)

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f: f.write(html)
    print(f'Wrote {out} [{mode}] ({os.path.getsize(out) // 1024} KB, {len(files)} JSON files, themes: {", ".join(themes)})')

if args.mode == 'both':
    build('standalone', os.path.join(ROOT, 'dist', 'training.html'))
    build('preview', os.path.join(ROOT, 'dist', 'training-preview.html'))
else:
    build(args.mode, args.out or os.path.join(ROOT, 'dist', 'training.html' if args.mode == 'standalone' else f'training-{args.mode}.html'))
