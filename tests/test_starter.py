import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'checks.py'

class ChecksTests(unittest.TestCase):
    def call_check(self, config, mode='app'):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'checks.json'
            path.write_text(json.dumps(config), encoding='utf-8')
            return subprocess.run([sys.executable, str(SCRIPT), mode, '--config', str(path)], capture_output=True, text=True)

    def test_script_exists(self):
        self.assertTrue(SCRIPT.is_file(), 'checks.py implementation is missing')

    def test_unconfigured_blocks(self):
        p = self.call_check({'commands': []})
        self.assertEqual(p.returncode, 2)
        self.assertIn('BLOCKED', p.stdout)

    def test_success_command_runs(self):
        p = self.call_check({'commands': [{'name': 'test', 'argv': [sys.executable, '-c', 'print("actual-check-ran")'], 'timeout_seconds': 5}]})
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn('actual-check-ran', p.stdout)

    def test_failure_propagates(self):
        p = self.call_check({'commands': [{'name': 'test', 'argv': [sys.executable, '-c', 'raise SystemExit(7)'], 'timeout_seconds': 5}]})
        self.assertEqual(p.returncode, 1)
        self.assertIn('FAIL', p.stdout)

    def test_shell_string_rejected(self):
        p = self.call_check({'commands': [{'name': 'bad', 'argv': 'echo fake'}]})
        self.assertEqual(p.returncode, 2)

    def test_missing_executable_blocks(self):
        p = self.call_check({'commands': [{'name': 'test', 'argv': ['this-command-must-not-exist-cc-starter']}]})
        self.assertEqual(p.returncode, 2)

    def test_timeout_fails(self):
        p = self.call_check({'commands': [{'name': 'test', 'argv': [sys.executable, '-c', 'import time; time.sleep(3)'], 'timeout_seconds': 0.05}]})
        self.assertEqual(p.returncode, 1)

    def test_invalid_json_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.json'
            path.write_text('{', encoding='utf-8')
            p = subprocess.run([sys.executable, str(SCRIPT), 'app', '--config', str(path)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 2)

    def test_template_check_passes(self):
        p = subprocess.run([sys.executable, str(SCRIPT), 'template'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

if __name__ == '__main__':
    unittest.main()
