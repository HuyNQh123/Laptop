"""Conservative family inventory for manual imagery review; never assigns an image."""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.product_images import image_metadata, load_manifest


def family(row):
    name = row['name']
    brand = row['brand'].casefold()
    if brand == 'apple':
        body = re.split(r'\)\s', name, maxsplit=1)[0] + ')'
    elif brand == 'asus':
        body = name.rsplit('-', 1)[0]
    elif brand == 'lenovo':
        body = name.rsplit(' ', 1)[0]
    elif brand == 'dell':
        body = re.split(r'\s(?:\d{7,}|i[3579]\s)', name, maxsplit=1)[0]
        if body == name:
            body = name.rsplit(' ', 1)[0]
    elif brand == 'hp':
        body = name.rsplit(' ', 1)[0]
    elif brand == 'acer':
        body = name.rsplit(' ', 1)[0].rsplit('-', 1)[0]
    elif brand in ('lg', 'lg gram'):
        body = name.split('-')[0]
    else:
        body = name.rsplit('-', 1)[0]
    # Keeping model generation and diagonal distinct prevents unsafe name-only merges.
    return f"{body} | {float(row['screen_size']):g} inch"


def inventory():
    manifest = load_manifest()
    with (ROOT / 'data/laptops.csv').open(encoding='utf-8') as source:
        rows = list(csv.DictReader(source))
    if len({row['name'] for row in rows}) != len(rows):
        raise ValueError('Laptop names must be unique')
    groups = defaultdict(list)
    for row in rows:
        groups[family(row)].append(row)
    result = []
    verified_rows = [r for r in rows if image_metadata(r['name'], manifest)['has_image']]
    for key, members in groups.items():
        missing = [r for r in members if not image_metadata(r['name'], manifest)['has_image']]
        if not missing:
            continue
        available = [r['name'] for r in members if image_metadata(r['name'], manifest)['has_image']]
        def nearby(row):
            # Discovery only: same commercial line/diagonal may span incompatible bodies.
            prefix = re.split(r'\s(?=[A-Z]*\d)', row['name'], maxsplit=1)[0]
            return [v['name'] for v in verified_rows if family(v)!=key
                    and v['brand'].casefold()==row['brand'].casefold()
                    and float(v['screen_size'])==float(row['screen_size'])
                    and re.split(r'\s(?=[A-Z]*\d)', v['name'], maxsplit=1)[0]==prefix]
        result.append(dict(group=key, brand=members[0]['brand'],
                           screen_size=members[0]['screen_size'],
                           color_in_dataset='not_recorded',
                           existing_image_models=available,
                           missing=[dict(name=r['name'], cpu=r['cpu'], gpu=r['gpu'],
                                         ram=r['ram'], storage=r['storage'],
                                         previous_reason=manifest[r['name']].get('missing_reason'),
                                         cross_model_candidates=nearby(r),
                                         previous_urls=manifest[r['name']].get('discovered_product_urls', []))
                                    for r in missing],
                           reuse_decision='requires_manual_body_generation_color_evidence' if available
                                         else 'no_verified_image_in_same_conservative_family'))
    return dict(catalog_count=len(rows), missing_count=sum(len(g['missing']) for g in result),
                missing_groups=len(result), groups=sorted(result, key=lambda g:(-bool(g['existing_image_models']),-len(g['missing']),g['group'])))


if __name__ == '__main__':
    result = inventory()
    dest = ROOT / 'data/image_family_inventory.json'
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='groups'}, ensure_ascii=True))
