#!/usr/bin/env python3
"""Maintain the one-file Academy Templates release.

Run from the repository root:

    python3 AcademyTemplates/tools/skills.py check
    python3 AcademyTemplates/tools/skills.py test [--academy /path/to/semitec-academy]
    python3 AcademyTemplates/tools/skills.py release --out /tmp/AcademyTemplates-1.4.0.zip

`release` contains every skill in one AcademyTemplates ZIP. The individual skills remain usable from
their own folders; this tool deliberately does not create per-skill ZIP files.
"""
import argparse
import filecmp
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parent
SKILLS = ROOT / 'skills'
PACKAGE = SKILLS / 'package'
NAME = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$')
SEMVER = re.compile(r'^\d+\.\d+\.\d+$')
IGNORED_DIRS = {'__pycache__', '.dev-progress', 'dist'}
IGNORED_NAMES = {'.DS_Store'}
PRIVATE_SUFFIXES = ('.key', '.key.pem', '.p12', '.pfx', '.p8')


def read(path):
    return Path(path).read_text(encoding='utf-8')


def skills():
    return sorted(path for path in SKILLS.iterdir() if (path / 'SKILL.md').is_file())


def frontmatter(path):
    match = re.match(r'^---\n(.*?)\n---\n', read(path), re.S)
    if not match:
        return None
    values = {}
    current = None
    for line in match.group(1).splitlines():
        entry = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
        if entry:
            current, value = entry.groups()
            values[current] = '' if value.strip() in ('>', '>-', '|', '|-') else value.strip()
        elif current and line.startswith(' '):
            values[current] = (values[current] + ' ' + line.strip()).strip()
    return values


def release_files():
    """Files included in the product ZIP, excluding generated or local state."""
    for base, dirs, files in os.walk(ROOT):
        current = Path(base)
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        for name in sorted(files):
            if name in IGNORED_NAMES or name.endswith(('.pyc', '.aux', '.log', '.toc', '.out', '.fls', '.fdb_latexmk', '.xdv', '.bbl', '.bcf', '.blg', '.run.xml', '.synctex.gz')):
                continue
            path = current / name
            yield path, path.relative_to(ROOT).as_posix()


def bundle_files(path):
    return {relative: source for source, relative in release_files() if source.is_file()}


def run(command, cwd=None):
    print('+ ' + ' '.join(str(part) for part in command))
    subprocess.run(command, cwd=cwd, check=True)


def validate():
    errors = []
    manifest = ROOT / '.claude-plugin' / 'plugin.json'
    try:
        plugin = json.loads(read(manifest))
        if plugin.get('name') != 'academy-templates':
            errors.append('plugin name must be academy-templates')
        if not SEMVER.match(str(plugin.get('version', ''))):
            errors.append('plugin version must use MAJOR.MINOR.PATCH')
    except Exception as exc:
        errors.append(f'cannot read {manifest.relative_to(REPOSITORY)}: {exc}')
        plugin = {}

    marketplace = REPOSITORY / '.claude-plugin' / 'marketplace.json'
    try:
        listed = json.loads(read(marketplace)).get('plugins', [])
        if not any(item.get('name') == 'academy-templates' for item in listed):
            errors.append('marketplace.json does not list academy-templates')
    except Exception as exc:
        errors.append(f'cannot read marketplace.json: {exc}')

    for skill in skills():
        metadata = frontmatter(skill / 'SKILL.md')
        name = skill.name
        if metadata is None:
            errors.append(f'{name}: SKILL.md has no frontmatter')
            continue
        if metadata.get('name') != name:
            errors.append(f'{name}: frontmatter name must match its folder')
        if not NAME.match(name):
            errors.append(f'{name}: folder name must use lowercase letters, digits and hyphens')
        if not metadata.get('description'):
            errors.append(f'{name}: frontmatter description is missing')
        if not (skill / 'README.md').is_file():
            errors.append(f'{name}: README.md is missing')

    if (PACKAGE / 'examples').exists():
        errors.append('package: examples/ is shipped although tests own the fictional fixture')
    for generated in [ROOT / 'dist', *(skill / 'dist' for skill in skills())]:
        if generated.exists():
            errors.append(f'generated directory must not be tracked or released: {generated.relative_to(ROOT)}')

    expected = [PACKAGE / 'scripts' / relative for relative in (
        'stlp.js', 'VERSION.json', 'README.md', 'lib/packfmt.js', 'lib/validate.js', 'lib/spec.js',
        'lib/versions.js', 'lib/schedule.js', 'node_modules/fflate/package.json')]
    errors.extend(f'package: missing bundled runtime file {path.relative_to(PACKAGE)}' for path in expected if not path.is_file())

    for source, relative in release_files():
        if relative.endswith('.stlp'):
            errors.append(f'release contains a course package: {relative}')
        if source.name.endswith(PRIVATE_SUFFIXES):
            errors.append(f'release contains a private signing key: {relative}')

    print(f'AcademyTemplates {plugin.get("version", "?")} — {len(skills())} skills')
    if errors:
        for error in errors:
            print('ERROR ' + error)
        print(f'\n{len(errors)} validation error(s)')
        return False
    print('Structure and release boundaries are valid.')
    return True


def compare_bundled_packer(academy, generated):
    current = academy / 'packer' / 'stlp.js'
    if not current.is_file():
        raise RuntimeError(f'not an Academy checkout: {current} is missing')
    run(['node', str(current), 'bundle-skill', str(generated)])
    committed = PACKAGE / 'scripts'
    expected = {p.relative_to(generated).as_posix(): p for p in generated.rglob('*') if p.is_file() and p.name != 'VERSION.json'}
    actual = {p.relative_to(committed).as_posix(): p for p in committed.rglob('*') if p.is_file() and p.name != 'VERSION.json'}
    if expected.keys() != actual.keys():
        missing = sorted(expected.keys() - actual.keys())
        extra = sorted(actual.keys() - expected.keys())
        raise RuntimeError(f'bundled packer file set differs from Academy; missing={missing}, extra={extra}')
    changed = [name for name in expected if not filecmp.cmp(expected[name], actual[name], shallow=False)]
    if changed:
        raise RuntimeError('bundled packer is not regenerated from Academy: ' + ', '.join(changed))
    app_version = json.loads(read(academy / 'app' / 'package.json'))['version']
    recorded = json.loads(read(committed / 'VERSION.json'))
    if recorded.get('release') != app_version or recorded.get('builtFrom') != 'SemiTec Academy ' + app_version:
        raise RuntimeError(f'package VERSION.json says {recorded.get("builtFrom")}, expected SemiTec Academy {app_version}')


def test(academy=None):
    if not validate():
        return False
    fixture = REPOSITORY / 'tests' / 'fixtures' / 'package' / 'minimal' / 'pack-spec.json'
    if not fixture.is_file():
        print('ERROR missing package fixture: ' + str(fixture))
        return False
    with tempfile.TemporaryDirectory(prefix='academy-templates-test-') as temp:
        temp = Path(temp)
        training = SKILLS / 'training'
        run([sys.executable, 'tools/validate.py', '.'], cwd=training)
        standalone = temp / 'training.html'
        run([sys.executable, 'tools/build_single_file.py', '.', '--mode', 'standalone', '--out', str(standalone)], cwd=training)
        if not standalone.is_file() or standalone.stat().st_size < 1000:
            raise RuntimeError('training standalone build did not produce a usable HTML file')

        lab = SKILLS / 'lab-manual'
        run([sys.executable, 'tools/check_lab.py', 'examples/lab-01-shift-register'], cwd=lab)

        brief = SKILLS / 'project-brief'
        brief_fixture = REPOSITORY / 'tests' / 'fixtures' / 'project-brief' / 'minimal'
        project_out = temp / 'project'
        sample_pdf = brief / 'sample-output-english.pdf'
        run([sys.executable, 'tools/brief2project.py', str(brief_fixture), '--pdf', str(sample_pdf), '--out', str(project_out)], cwd=brief)
        project = json.loads(read(project_out / 'project.json'))
        if project.get('durationWeeks') != 30 or len(project.get('weeks', [])) != 2 or not (project_out / 'brief.pdf').is_file():
            raise RuntimeError('brief fixture did not export its duration and weekly plan')

        builder = PACKAGE / 'scripts' / 'stlp.js'
        run(['node', str(builder), 'check', str(fixture)])
        package_out = temp / 'packages'
        run(['node', str(builder), 'create', str(fixture), '--unsigned', '--out', str(package_out)])
        packages = list(package_out.glob('*.stlp'))
        if len(packages) != 1:
            raise RuntimeError(f'expected one fictional package, found {packages}')
        run(['node', str(builder), 'inspect', str(packages[0])])

        # A release must retain a runnable copy of the package tool.  Exercise the
        # tool after extraction rather than only trusting the source tree.
        archive = temp / 'AcademyTemplates-test.zip'
        write_release(archive)
        extracted = temp / 'extracted'
        with zipfile.ZipFile(archive) as release_zip:
            release_zip.extractall(extracted)
        released_builder = extracted / ROOT.name / 'skills' / 'package' / 'scripts' / 'stlp.js'
        run(['node', str(released_builder), 'check', str(fixture)])

        if academy:
            academy = Path(academy).resolve()
            generated = temp / 'bundled-packer'
            compare_bundled_packer(academy, generated)
            run(['node', str(academy / 'packer' / 'stlp.js'), 'inspect', str(packages[0])])
    print('All standalone, package and compatibility checks passed.')
    return True


def write_release(output):
    """Write the one product archive after validation has completed."""
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise RuntimeError('write release ZIP outside AcademyTemplates; generated artifacts are not source files')
    if output.exists() and output.is_dir():
        raise RuntimeError(f'release path is a directory: {output}')
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for source, relative in release_files():
            archive.write(source, ROOT.name + '/' + relative)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f'Created {output} ({output.stat().st_size // 1024} KB)')
    print(f'SHA256 {digest}  {output.name}')


def release(output):
    if not validate():
        return False
    write_release(output)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('check')
    tests = sub.add_parser('test')
    tests.add_argument('--academy', help='path to a current semitec-academy checkout for cross-repository verification')
    release_parser = sub.add_parser('release')
    release_parser.add_argument('--out', required=True, help='path for the single AcademyTemplates ZIP')
    args = parser.parse_args()
    if args.command == 'check':
        ok = validate()
    elif args.command == 'test':
        ok = test(args.academy)
    else:
        ok = release(args.out)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
