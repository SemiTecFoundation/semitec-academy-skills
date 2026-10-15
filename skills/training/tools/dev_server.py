#!/usr/bin/env python3
"""Development server: serves the training folder AND a tiny progress REST API, so you can test
platform integration without a real backend. It is the reference for what your platform must implement.

    python3 tools/dev_server.py            -> http://localhost:8000/examples/

API (JSON, stored in .dev-progress/ next to this training):
    GET    /api/progress/<trainingId>/<userId>   -> 200 state | 404 when the user has no progress yet
    PUT    /api/progress/<trainingId>/<userId>   <- state (body)  -> 204
    DELETE /api/progress/<trainingId>/<userId>   -> 204
    GET    /api/progress/<trainingId>            -> 200 [{userId, name, percent, completedAt, updatedAt}]  (teacher overview)
No authentication — for local testing only."""
import json, os, re, sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, '.dev-progress')
SAFE = re.compile(r'^[\w.@-]{1,120}$')
os.makedirs(DATA, exist_ok=True)

class H(SimpleHTTPRequestHandler):
    def _api(self):
        m = re.match(r'^/api/progress/([^/?]+)(?:/([^/?]+))?/?(?:\?.*)?$', self.path)
        if not m: return None
        t, u = m.group(1), m.group(2)
        if not SAFE.match(t) or (u is not None and not SAFE.match(u)): return ('bad', None)
        return (t, u)
    def _send(self, code, obj=None):
        body = b'' if obj is None else json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if body: self.wfile.write(body)
    def _file(self, t, u): return os.path.join(DATA, f'{t}__{u}.json')
    def do_GET(self):
        a = self._api()
        if not a: return super().do_GET()
        t, u = a
        if t == 'bad': return self._send(400, {'error': 'bad id'})
        if u is None:
            rows = []
            for f in sorted(os.listdir(DATA)):
                if f.startswith(t + '__') and f.endswith('.json'):
                    s = json.load(open(os.path.join(DATA, f), encoding='utf-8'))
                    rows.append({'userId': f[len(t) + 2:-5], 'name': (s.get('user') or {}).get('name'),
                                 'percent': s.get('percent'), 'completedAt': s.get('completedAt'), 'updatedAt': s.get('updatedAt')})
            return self._send(200, rows)
        p = self._file(t, u)
        if not os.path.isfile(p): return self._send(404, {'error': 'no progress yet'})
        return self._send(200, json.load(open(p, encoding='utf-8')))
    def do_PUT(self):
        a = self._api()
        if not a or a[1] is None or a[0] == 'bad': return self._send(400, {'error': 'use /api/progress/<trainingId>/<userId>'})
        n = int(self.headers.get('Content-Length') or 0)
        if n > 1_000_000: return self._send(413, {'error': 'too large'})
        try: state = json.loads(self.rfile.read(n) or b'null')
        except ValueError: return self._send(400, {'error': 'invalid JSON'})
        if not isinstance(state, dict) or state.get('trainingId') != a[0]: return self._send(400, {'error': 'state.trainingId does not match the URL'})
        with open(self._file(*a), 'w', encoding='utf-8') as f: json.dump(state, f, ensure_ascii=False, indent=1)
        self._send(204)
    do_POST = do_PUT
    def do_DELETE(self):
        a = self._api()
        if not a or a[1] is None or a[0] == 'bad': return self._send(400, {'error': 'bad path'})
        p = self._file(*a)
        if os.path.isfile(p): os.remove(p)
        self._send(204)
    def log_message(self, fmt, *args):
        if '/api/' in (args[0] if args else ''): sys.stderr.write('API ' + (fmt % args) + '\n')

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f'Training dev server: http://localhost:{port}/examples/   (progress files in {DATA})')
    ThreadingHTTPServer(('127.0.0.1', port), partial(H, directory=ROOT)).serve_forever()
