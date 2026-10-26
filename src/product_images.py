"""Product imagery is presentation metadata, never a model feature."""
from functools import lru_cache
import json
import logging
from pathlib import Path
import unicodedata
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/laptop_images.json'
IMAGE_ROOT = ROOT / 'static/images/laptops'
PLACEHOLDER = 'images/laptop-placeholder.svg'

def unique_object(pairs):
    result = {}
    normalized = set()
    for key, value in pairs:
        canonical = unicodedata.normalize('NFC', key).strip().casefold()
        if canonical in normalized:
            raise ValueError(f'Duplicate image mapping key: {key}')
        normalized.add(canonical)
        result[key] = value
    return result

@lru_cache(maxsize=2)
def _read_manifest(path, stamp):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_object)

def load_manifest():
    try:
        manifest = _read_manifest(str(MANIFEST), MANIFEST.stat().st_mtime_ns)
        if not isinstance(manifest, dict):
            raise ValueError('Image manifest must be an object keyed by full laptop name')
        return manifest
    except (OSError, ValueError) as error:
        logging.getLogger(__name__).error('Product image manifest rejected: %s', error)
        return {}

def public_url(value):
    if not isinstance(value, str):
        return ''
    try:
        parts = urlsplit(value or '')
        return value if parts.scheme in ('https', 'http') and parts.netloc else ''
    except ValueError:
        return ''

def image_metadata(name, manifest=None):
    image = (load_manifest() if manifest is None else manifest).get(name, {})
    if not isinstance(image, dict):
        image = {}
    path = image.get('path', '') or ''
    if not isinstance(path, str):
        path = ''
    asset = (ROOT / 'static' / path).resolve()
    rights = image.get('rights_status')
    rights_ok = (rights == 'not_declared' and bool(image.get('rights_note'))
                 or rights == 'licensed' and bool(image.get('license')) and bool(public_url(image.get('license_url')))
                 or rights == 'permission_granted' and bool(image.get('permission_evidence')))
    match = image.get('match_level')
    match_ok = (match == 'exact_model'
                or match == 'same_series_representative' and bool(image.get('representative_evidence')))
    valid = (image.get('verification_status') == 'verified' and bool(path)
             and image.get('image_type') == 'catalogue'
             and match_ok
             and image.get('visual_checked') is True and bool(image.get('checked_date'))
             and rights_ok
             and bool(public_url(image.get('image_url')))
             and bool(public_url(image.get('source_url'))) and bool(image.get('model_evidence'))
             and bool(image.get('matched_model')) and bool(image.get('gallery_binding'))
             and asset.is_relative_to(IMAGE_ROOT.resolve()) and asset.is_file()
             and asset.suffix.lower() in ('.webp', '.png', '.jpg', '.jpeg'))
    return {
        'image_path': path if valid else PLACEHOLDER,
        'image_alt': image.get('alt') or name if valid else 'Chưa có ảnh: ' + name,
        'has_image': valid,
        'image_status': image.get('verification_status', 'not_reviewed'),
        'image_note': image.get('note', 'Chưa xác minh được ảnh catalogue đúng model.'),
        'image_source_url': public_url(image.get('source_url')),
        'image_author': image.get('source_name', '') if valid else '',
        'image_representative': valid and image.get('match_level') == 'same_series_representative',
        'image_source_model': image.get('representative_source_key', '') if valid else '',
        'image_width': image.get('width') if valid and type(image.get('width')) is int and 0 < image['width'] <= 1000 else 800,
        'image_height': image.get('height') if valid and type(image.get('height')) is int and 0 < image['height'] <= 1000 else 600,
        'image_license': image.get('license', '') if valid else '',
        'image_license_url': public_url(image.get('license_url')) if valid else '',
        'image_changes': image.get('modifications', '') if valid else '',
    }
