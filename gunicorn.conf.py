"""Render entrypoint: gunicorn --config gunicorn.conf.py app:app."""
import os
from pathlib import Path

bind = f"0.0.0.0:{int(os.environ.get('PORT', '10000'))}"
workers = 1
preload_app = False
accesslog = '-'
errorlog = '-'

# Share the build-time font cache with runtime workers; respect explicit settings.
os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parent / '.mpl-cache'))
