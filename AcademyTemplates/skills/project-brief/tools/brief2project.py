#!/usr/bin/env python3
"""brief2project.py — turn a project brief (this template's LaTeX) into the SemiTec Academy project:
<brief>/project/project.json + brief.pdf.  The app shows it as a project with a weekly plan mapped onto the
calendar from the day the student enrolls (tick weeks, notes, milestones, deliverables, rubric, brief PDF).

    python3 tools/brief2project.py <brief-folder> [--pdf <compiled brief.pdf>] [--id <project-id>] [--out <dir>]
                                   [--category research|diploma|thesis|course-project|capstone|internship|other]

Reads (from the brief's latex files — the folder with main.tex, metadata.tex, sections/):
  metadata.tex      title, supervisors, work type, level, slots, duration, areas, keywords, tools, prerequisites
  \\weekbreak / \\weekrow      (tracker)        -> weeks: [{week, phase, tasks, doneWhen}]
  \\milestone{1--4}{…}{…}       (work plan)      -> milestones
  \\deliverable{…}{…}{…}{…}                     -> deliverables (dueWeek from "week N")
  \\criterion{…}{…}{…}{…}{…}    (rubric)         -> assessment
  \\learngroup / \\learn          (learning path)  -> learning
  goals / learning outcomes (first enumerate / itemize of the goals chapter), summary (problem chapter)
Then put the project/ folder into a SemiTec Learning Package: "projects": [{ "id": …, "source": "<brief>/project" }]."""
import json, os, re, shutil, sys

SUP = str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')


def args_of(text, macro, n):
    """All occurrences of \\macro{a1}…{an} (balanced braces) -> list of tuples."""
    out, i = [], 0
    pat = re.compile(r'\\' + macro + r'(?![A-Za-z])\s*')
    while True:
        m = pat.search(text, i)
        if not m:
            return out
        j, vals = m.end(), []
        for _ in range(n):
            while j < len(text) and text[j] in ' \t\n':
                j += 1
            if j >= len(text) or text[j] != '{':
                break
            depth, k = 0, j
            while k < len(text):
                if text[k] == '\\':
                    k += 2; continue
                if text[k] == '{':
                    depth += 1
                elif text[k] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            vals.append(text[j + 1:k]); j = k + 1
        if len(vals) == n:
            out.append((m.start(),) + tuple(vals))
        i = m.end()


class Tex:
    def __init__(self, labels, gloss, bib):
        self.labels, self.gloss, self.bib = labels, gloss, bib

    def cites(self, keys):
        return '; '.join(self.bib.get(k.strip(), k.strip()) for k in keys.split(',') if k.strip())

    def md(self, s, keep_cites=False):
        if s is None:
            return ''
        if keep_cites:
            s = re.sub(r'\\cite[pt]?\*?(\[[^\]]*\])?\{([^}]*)\}', lambda m: self.cites(m.group(2)), s)
        s = re.sub(r'(?<!\\)%.*', '', s)
        s = re.sub(r'(Chapter|Section|Figure|Table|Chapters|Sections)~?\\ref\{([^}]*)\}',
                   lambda m: ('“' + self.labels[m.group(2)] + '”') if m.group(2) in self.labels else 'the brief', s)
        s = re.sub(r'\\ref\{([^}]*)\}', lambda m: self.labels.get(m.group(1), ''), s)
        s = re.sub(r'~?\\cite[pt]?\*?(\[[^\]]*\])?\{[^}]*\}', '', s)
        s = re.sub(r'\\glspl\{([^}]*)\}', lambda m: self.gloss.get(m.group(1), m.group(1)) + 's', s)
        s = re.sub(r'\\[Gg]ls\{([^}]*)\}', lambda m: self.gloss.get(m.group(1), m.group(1)), s)
        s = re.sub(r'\\textsuperscript\{([^}]*)\}', lambda m: m.group(1).translate(SUP), s)
        for mac, wrap in (('textbf', '**'), ('emph', '*'), ('textit', '*'), ('texttt', '`')):
            s = re.sub(r'\\' + mac + r'\{([^{}]*)\}', lambda m, w=wrap: w + m.group(1) + w, s)
        s = re.sub(r'\\(missing|textrm|textsf|mbox|text|underline|url)\{([^{}]*)\}', r'\2', s)
        s = re.sub(r'\\href\{([^}]*)\}\{([^}]*)\}', r'[\2](\1)', s)
        rep = [('---', '—'), ('--', '–'), ('``', '“'), ("''", '”'), ('\\%', '%'), ('\\&', '&'), ('\\_', '_'), ('\\#', '#'),
               ('\\ldots', '…'), ('\\dots', '…'), ('\\,', ' '), ('\\ ', ' '), ('\\\\', ' '), ('~', ' '), ('\\optionaltask', '(optional) ')]
        for a, b in rep:
            s = s.replace(a, b)
        s = re.sub(r'\\[A-Za-z]+\*?(\[[^\]]*\])?', '', s)        # any other command name
        s = s.replace('{', '').replace('}', '')
        return re.sub(r'\s+', ' ', s).strip()


CATEGORIES = ('research', 'diploma', 'thesis', 'course-project', 'capstone', 'internship', 'other')


def category_of(work_type):
    """work type of the brief -> app category (projects page filter)"""
    w = work_type.lower()
    for key, cat in (('capstone', 'capstone'), ('intern', 'internship'), ('thesis', 'thesis'), ('master', 'thesis'), ('diploma', 'diploma'),
                     ('course', 'course-project'), ('research', 'research'), ('դիպլոմ', 'diploma'), ('մագիստր', 'thesis'), ('հետազոտ', 'research')):
        if key in w:
            return cat
    return 'other'


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__); return 1
    src = os.path.abspath(argv[0])
    opt = {argv[i][2:]: argv[i + 1] for i in range(1, len(argv) - 1) if argv[i].startswith('--')}
    latex = src if os.path.exists(os.path.join(src, 'metadata.tex')) else os.path.join(src, 'latex')
    if not os.path.exists(os.path.join(latex, 'metadata.tex')):
        print('✗ no metadata.tex in', src, '(or its latex/ folder)'); return 1
    read = lambda p: open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    meta = read(os.path.join(latex, 'metadata.tex'))
    secdir = os.path.join(latex, 'sections')
    secs = {f: read(os.path.join(secdir, f)) for f in sorted(os.listdir(secdir)) if f.endswith('.tex')} if os.path.isdir(secdir) else {}
    alltex = '\n'.join(secs.values())

    labels = {}
    for f, t in secs.items():
        for m in re.finditer(r'\\(chapter|section)\*?\{([^}]*)\}\s*\\label\{([^}]*)\}', t):
            labels[m.group(3)] = re.sub(r'\\[a-z]+\{([^}]*)\}', r'\1', m.group(2))
    gloss = {}
    gt = read(os.path.join(latex, 'abbreviations.tex')) + read(os.path.join(latex, 'glossary.tex'))
    for _, key, short, _l in args_of(gt, 'newacronym', 3):
        gloss[key] = short
    for m in re.finditer(r'\\newglossaryentry\{([^}]*)\}\s*\{[^}]*?name=\{?([^,}]*)', gt):
        gloss.setdefault(m.group(1), m.group(2))
    bib = {}
    for chunk in read(os.path.join(latex, 'references.bib')).split('@')[1:]:
        km = re.match(r'\s*\w+\s*\{\s*([^,\s]+)\s*,', chunk)
        if not km:
            continue
        fields = {k.lower(): v for k, v in re.findall(r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}', chunk)}
        raw = fields.get('author', '').strip()
        if raw.startswith('{'):                                   # corporate author {{AMD}} -> "AMD: <short title>"
            au = raw.strip('{}') + ': ' + ' '.join(re.sub(r'[{}]', '', fields.get('title', '')).split()[:5])
        else:
            au = re.sub(r'[{}]', '', raw).split(' and ')[0].strip()
            au = au.split(',')[0] if ',' in au else (au.split()[-1] if au else '')
        name = au or re.sub(r'[{}]', '', fields.get('title', ''))[:40] or re.sub(r'[{}]', '', fields.get('organization', fields.get('publisher', '')))
        bib[km.group(1)] = (name + (' ' + fields['year'] if fields.get('year') else '')).strip()
    T = Tex(labels, gloss, bib)

    def meta1(name):
        a = args_of(meta, name, 1)
        return T.md(a[0][1]) if a else ''

    title = meta1('settopictitle')
    if not title:
        print('✗ \\settopictitle is empty'); return 1
    lang = 'en'
    mm = re.search(r'\\usepackage\[([^\]]*)\]\{briefstyle\}', read(os.path.join(latex, 'main.tex')))
    if mm and 'armenian' in mm.group(1):
        lang = 'hy'

    # weekly tracker
    weeks, phase = [], ''
    events = sorted([(p, 'b', a) for p, a in args_of(alltex, 'weekbreak', 1)] + [(p, 'w', a, b, c) for p, a, b, c in args_of(alltex, 'weekrow', 3)])
    for e in events:
        if e[1] == 'b':
            phase = T.md(e[2])
        else:
            nums = re.findall(r'\d+', e[2])
            if not nums:
                continue
            weeks.append({'week': int(nums[0]), 'phase': phase, 'tasks': T.md(e[3]), 'doneWhen': T.md(e[4])})
    milestones = []
    for _, w, work, ms in args_of(alltex, 'milestone', 3):
        nums = [int(x) for x in re.findall(r'\d+', w)]
        if nums:
            milestones.append({'weeks': [nums[0], nums[-1]], 'work': T.md(work), 'milestone': T.md(ms)})
    deliverables = []
    for _, what, form, when, who in args_of(alltex, 'deliverable', 4):
        nums = re.findall(r'\d+', when)
        deliverables.append({'title': T.md(what), 'form': T.md(form), 'when': T.md(when), 'dueWeek': int(nums[-1]) if nums else None, 'who': T.md(who)})
    assessment = [{'criterion': T.md(a), 'weight': T.md(b), 'pass': T.md(c), 'good': T.md(d), 'excellent': T.md(e)}
                  for _, a, b, c, d, e in args_of(alltex, 'criterion', 5)]
    learning, group = [], ''
    lev = lambda s: 'apply' if '\\apply' in s else 'understand' if '\\understand' in s else 'aware' if '\\aware' in s else T.md(s)
    for e in sorted([(p, 'g', a) for p, a in args_of(alltex, 'learngroup', 1)] + [(p, 'l', a, b, c, d) for p, a, b, c, d in args_of(alltex, 'learn', 4)]):
        if e[1] == 'g':
            group = T.md(e[2])
        else:
            learning.append({'group': group, 'topic': T.md(e[2]), 'level': lev(e[3]), 'usedFor': T.md(e[4]), 'sources': T.md(e[5], True)})

    def items_of(text, env):
        m = re.search(r'\\begin\{' + env + r'\}(.*?)\\end\{' + env + r'\}', text, re.S)
        return [T.md(x) for x in re.split(r'\\item\s*', m.group(1))[1:]] if m else []
    goals_tex = next((t for f, t in secs.items() if re.search(r'goal', f)), '')
    goals = items_of(goals_tex, 'enumerate')
    after = goals_tex.split('Learning outcomes', 1)[1] if 'Learning outcomes' in goals_tex else ''
    outcomes = items_of(after, 'itemize')
    prob = next((t for f, t in secs.items() if re.search(r'problem|context', f)), '')
    paras = [p for p in re.split(r'\n\s*\n', re.sub(r'\\(chapter|section|label)\*?\{[^}]*\}', '', prob)) if p.strip() and not p.strip().startswith('\\begin')]
    summary = T.md(paras[0]) if paras else ''
    if len(summary) > 700:
        summary = summary[:summary.rfind(' ', 0, 680)] + ' …'

    dur = re.findall(r'(\d+)\s*weeks', meta1('setduration'))
    duration = max([w['week'] for w in weeks] + [int(dur[-1])] if dur else [w['week'] for w in weeks] or [0])
    slots = re.findall(r'\d+', meta1('setslots'))
    project = {
        'format': 1,
        'id': opt.get('id') or re.sub(r'[^a-z0-9]+', '-', os.path.basename(src.rstrip('/')).lower()).strip('-'),
        'title': title, 'subtitle': meta1('settopicsubtitle'), 'summary': summary, 'language': lang,
        'category': opt.get('category') or category_of(meta1('setworktype')),
        'workType': meta1('setworktype'), 'level': meta1('setdegreelevel'), 'slots': int(slots[0]) if slots else 1,
        'durationWeeks': duration, 'duration': meta1('setduration'),
        'supervisors': [x for x in (meta1('setsupervisorone'), meta1('setsupervisortwo')) if x],
        'mentor': meta1('setmentor'), 'partner': meta1('setpartnerorg'),
        'areas': [a.strip() for a in meta1('setareas').split(',') if a.strip()],
        'keywords': [a.strip() for a in meta1('setkeywords').split(',') if a.strip()],
        'tools': meta1('settools'), 'prerequisites': meta1('setprerequisites'),
        'goals': goals, 'outcomes': outcomes,
        'weeks': weeks, 'milestones': milestones, 'deliverables': deliverables, 'assessment': assessment, 'learning': learning,
        'brief': 'brief.pdf', 'version': meta1('setversion') or '1.0'
    }
    out = os.path.abspath(opt.get('out') or os.path.join(src, 'project'))
    os.makedirs(out, exist_ok=True)
    pdf = opt.get('pdf')
    if not pdf:
        cands = [os.path.join(d, f) for d in (src, latex) for f in sorted(os.listdir(d)) if f.endswith('.pdf') and not f.startswith('sample-output')]
        pdf = next((c for c in cands if 'brief' in os.path.basename(c)), cands[0] if cands else None)
    if pdf and os.path.exists(pdf):
        shutil.copyfile(pdf, os.path.join(out, 'brief.pdf'))
    else:
        project.pop('brief'); print('⚠ no compiled brief PDF found — build it (latexmk -xelatex main.tex) or pass --pdf')
    with open(os.path.join(out, 'project.json'), 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2); f.write('\n')

    problems = []
    if not weeks: problems.append('no \\weekrow entries (weekly tracker) — the app needs the weekly plan')
    if len({w['week'] for w in weeks}) != len(weeks): problems.append('a week number appears twice in the tracker')
    left = [w for w in weeks if '[' in w['tasks'] or not w['tasks']]
    if left: problems.append(f'{len(left)} week(s) still contain [placeholders]')
    print(f"{'✓' if not problems else '⚠'} {os.path.relpath(out)}/project.json — {title}")
    print(f"  {len(weeks)} weeks, {len(milestones)} milestones, {len(deliverables)} deliverables, {len(assessment)} rubric rows, {len(learning)} learning topics, duration {duration} weeks")
    for p in problems: print('  ⚠ ' + p)
    print('  Add to a package spec:  "projects": [{ "id": "%s", "source": "%s" }]' % (project['id'], os.path.relpath(out)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
