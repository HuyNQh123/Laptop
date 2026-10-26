"""Startup must not wait for chart libraries or train a model."""
import os
import hashlib
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class StartupTests(unittest.TestCase):
    def test_catalog_starts_without_scientific_libraries_or_font_cache(self):
        # A fresh interpreter is necessary: workflow tests already load these modules.
        code = r'''
import importlib.abc
import sys
from pathlib import Path
from unittest.mock import patch

class BlockScientificImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'matplotlib', 'seaborn', 'sklearn', 'joblib', 'pandas', 'numpy'}:
            raise AssertionError('Startup tried to import ' + fullname)

sys.meta_path.insert(0, BlockScientificImports())
uri = 'sqlite:///file:' + (Path.cwd() / 'data/laptops.db').as_posix() + '?mode=ro&uri=true'
with patch('src.config.get_database_uri', return_value=(uri, 'sqlite')):
    import app
client = app.app.test_client()
for route in ['/', '/laptops', '/api/laptop-sources/1']:
    response = client.get(route)
    assert response.status_code == 200, (route, response.status_code)
assert 'src.price_prediction' not in sys.modules
assert 'src.data_analysis' not in sys.modules
assert 'src.radar_chart' not in sys.modules
'''
        with tempfile.TemporaryDirectory() as cache:
            result = subprocess.run(
                [sys.executable, '-c', code], cwd=ROOT, capture_output=True,
                text=True, timeout=30,
                env={**os.environ, 'MPLCONFIGDIR': cache, 'MPLBACKEND': 'Agg'},
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(list(Path(cache).iterdir()), [])

    def test_gunicorn_binds_all_interfaces_on_render_port(self):
        with patch.dict(os.environ, {'PORT': '12345'}):
            config = runpy.run_path(str(ROOT / 'gunicorn.conf.py'))
        self.assertEqual(config['bind'], '0.0.0.0:12345')
        self.assertEqual(config['workers'], 1)
        self.assertFalse(config['preload_app'])
        self.assertNotIn('timeout', config)  # Keep Gunicorn's default; do not mask slow boot.

    def test_gunicorn_default_port(self):
        with patch.dict(os.environ):
            os.environ.pop('PORT', None)
            config = runpy.run_path(str(ROOT / 'gunicorn.conf.py'))
        self.assertEqual(config['bind'], '0.0.0.0:10000')

    def test_build_and_runtime_share_warm_cache_before_matplotlib_import(self):
        cache = ROOT / '.mpl-cache'
        build_env = {**os.environ, 'MPLCONFIGDIR': str(cache), 'MPLBACKEND': 'Agg'}
        build = subprocess.run(
            [sys.executable, '-c', 'import matplotlib.font_manager'],
            cwd=ROOT, env=build_env, capture_output=True, text=True, timeout=45,
        )
        self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
        cache_files = list(cache.glob('fontlist*.json'))
        self.assertTrue(cache_files)
        before = {p.name: (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
                  for p in cache_files}
        runtime_env = dict(os.environ)
        runtime_env.pop('MPLCONFIGDIR', None)
        runtime_env.pop('MPLBACKEND', None)
        code = r'''
import os, runpy, sys
from pathlib import Path
assert 'matplotlib' not in sys.modules
runpy.run_path('gunicorn.conf.py')
assert 'matplotlib' not in sys.modules
expected = Path.cwd() / '.mpl-cache'
assert Path(os.environ['MPLCONFIGDIR']).resolve() == expected.resolve()
assert os.environ['MPLBACKEND'] == 'Agg'
import matplotlib.font_manager
import matplotlib
assert Path(matplotlib.get_cachedir()).resolve() == expected.resolve()
assert matplotlib.get_backend().lower() == 'agg'
'''
        runtime = subprocess.run(
            [sys.executable, '-c', code], cwd=ROOT, env=runtime_env,
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(runtime.returncode, 0, runtime.stdout + runtime.stderr)
        after = {p.name: (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
                 for p in cache.glob('fontlist*.json')}
        self.assertEqual(after, before, 'Runtime must reuse the font cache built earlier')


if __name__ == '__main__':
    unittest.main()
