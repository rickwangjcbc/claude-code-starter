"""Template checks and explicitly configured application checks. Python 3.10+."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'CLAUDE.md', '.claude/settings.json', '.claude/rules/security.md',
    '.claude/skills/team-plan/SKILL.md', '.claude/skills/team-implement/SKILL.md',
    '.claude/skills/team-fix-bug/SKILL.md', '.claude/skills/team-review/SKILL.md',
    '.claude/skills/team-handoff/SKILL.md', 'project-checks.json',
    'docs/PROJECT.md', 'docs/SETUP.md', 'templates/TASK.md',
    'prompts/00-bootstrap.md', 'prompts/01-feature.md', 'prompts/02-bug.md',
    'prompts/03-review.md', 'prompts/04-handoff.md',
    '.github/pull_request_template.md', '.github/workflows/ai-standard.yml',
    'tests/test_starter.py', 'README.md', 'SOURCES.md',
]

def template_check():
    problems = []
    for relative in REQUIRED:
        p = ROOT / relative
        if not p.is_file() or not p.read_text(encoding='utf-8').strip():
            problems.append(f'Missing or empty: {relative}')
    for relative in ['.claude/settings.json', 'project-checks.json']:
        try:
            json.loads((ROOT / relative).read_text(encoding='utf-8'))
        except (OSError, ValueError) as e:
            problems.append(f'Invalid JSON: {relative} ({type(e).__name__})')
    for name in ['team-plan', 'team-implement', 'team-fix-bug', 'team-review', 'team-handoff']:
        p = ROOT / '.claude/skills' / name / 'SKILL.md'
        if not p.is_file():
            continue
        text = p.read_text(encoding='utf-8')
        if not text.startswith('---\n') or f'name: {name}\n' not in text or '\ndescription:' not in text:
            problems.append(f'Invalid skill header: {name}')
    if problems:
        print('FAIL: template structure')
        print('\n'.join(problems))
        return 1
    print('PASS: template structure only; NOT application acceptance or Claude runtime verification')
    return 0

def app_check(config):
    try:
        data = json.loads(config.read_text(encoding='utf-8'))
        commands = data.get('commands') if isinstance(data, dict) else None
        if not isinstance(commands, list) or not commands:
            print('BLOCKED: configure actual application checks in project-checks.json')
            return 2
        # Validate the entire list before executing anything.
        for item in commands:
            if not isinstance(item, dict):
                raise ValueError('each check must be an object')
            argv = item.get('argv')
            timeout = item.get('timeout_seconds', 300)
            if not isinstance(item.get('name'), str) or not item['name'].strip():
                raise ValueError('each check needs a name')
            if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x and '\x00' not in x for x in argv):
                raise ValueError('argv must be a nonempty string array, not a shell string')
            if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
                raise ValueError('timeout_seconds must be positive and finite')
    except (OSError, ValueError, TypeError):
        print('BLOCKED: missing or invalid checks configuration')
        return 2
    for item in commands:
        print(f'RUN: {item["name"]}', flush=True)
        try:
            result = subprocess.run(item['argv'], cwd=ROOT, shell=False, timeout=item.get('timeout_seconds', 300))
        except OSError:
            print(f'BLOCKED: cannot launch {item["name"]}')
            return 2
        except subprocess.TimeoutExpired:
            print(f'FAIL: timeout in {item["name"]}')
            return 1
        if result.returncode:
            print(f'FAIL: {item["name"]} (exit {result.returncode})')
            return 1
    print('PASS: configured commands completed; human acceptance and unconfigured checks are not covered')
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['template', 'app'])
    parser.add_argument('--config', type=Path, default=ROOT / 'project-checks.json')
    args = parser.parse_args()
    return template_check() if args.mode == 'template' else app_check(args.config)

if __name__ == '__main__':
    sys.exit(main())
