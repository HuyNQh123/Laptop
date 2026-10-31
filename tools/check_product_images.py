"""Validate unique mappings, catalogue evidence and optimized local assets."""
import csv
import hashlib
import json
from pathlib import Path
import sys
from collections import Counter
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.product_images import unique_object, image_metadata

def check():
    with (ROOT/'data/laptops.csv').open(encoding='utf-8') as source:
        names=[row['name'] for row in csv.DictReader(source)]
    assert len(names)==len(set(names)), 'Duplicate catalog names'
    manifest=json.loads((ROOT/'data/laptop_images.json').read_text(encoding='utf-8'),object_pairs_hook=unique_object)
    assert set(manifest)==set(names), 'Manifest must cover exactly the catalog'
    counts=Counter(entry['verification_status'] for entry in manifest.values())
    shipped=set()
    for name,entry in manifest.items():
        assert entry['laptop_key']==name==entry['laptop_name'], f'Key mismatch: {name}'
        if entry['verification_status']!='verified':
            assert not entry.get('path'), f'Unverified asset must not ship: {name}'
            assert entry.get('note'), f'Missing reason: {name}'
            continue
        assert image_metadata(name,manifest)['has_image'], f'Incomplete verification metadata: {name}'
        assert entry['source_name'] and entry['model_evidence'] and entry['matched_model']
        assert entry['gallery_binding'] and entry['visual_checked'] is True
        assert entry['image_type']=='catalogue' and entry['checked_date']
        assert entry['rights_status'] in ('not_declared','licensed','permission_granted')
        if entry['rights_status']=='not_declared':
            assert not entry.get('license'), f'Undeclared rights must not claim an open license: {name}'
            assert entry['rights_note']
        if entry['match_level']=='same_series_representative':
            assert entry['representative_evidence']
            source=manifest[entry['representative_source_key']]
            assert source['verification_status']=='verified' and source['match_level']=='exact_model'
            for field in ('path','sha256','image_url','rights_status'):
                assert source[field]==entry[field], f'Representative must reuse source asset/rights: {name}'
            comparison=entry['representative_comparison']
            for field in ('body_model','generation','screen_size','source_color','target_color','differences','evidence_urls','checked_date'):
                assert comparison.get(field), f'Missing representative comparison {field}: {name}'
            assert comparison['source_color']==comparison['target_color']
        asset=ROOT/'static'/entry['path']
        assert hashlib.sha256(asset.read_bytes()).hexdigest()==entry['sha256'], f'Image checksum: {name}'
        assert asset.stat().st_size<=150000, f'Oversized asset: {name}'
        with Image.open(asset) as image:
            assert image.width<=1000 and image.height<=1000, f'Oversized dimensions: {name}'
            assert image.size==(entry['width'],entry['height']), f'Wrong intrinsic dimensions: {name}'
            assert image.width<=entry['original_width'] and image.height<=entry['original_height'], f'Upscaled image: {name}'
            image.verify()
        shipped.add(asset.resolve())
    actual={p.resolve() for p in (ROOT/'static/images/laptops').glob('*') if p.suffix.lower() in ('.webp','.png','.jpg','.jpeg')}
    assert actual==shipped, 'Unmapped product images in directory'
    assert len(shipped)==len({hashlib.sha256(p.read_bytes()).hexdigest() for p in shipped}), 'Duplicate image bytes should share one file'
    levels=Counter(e['match_level'] for e in manifest.values() if e['verification_status']=='verified')
    report={'catalog':len(names),'unique_keys':len(manifest),'verified':counts['verified'],'exact_model':levels['exact_model'],'same_series_representative':levels['same_series_representative'],'missing':len(names)-counts['verified'],'unique_image_files':len(shipped),'statuses':dict(counts)}
    summary=json.loads((ROOT/'data/image_audit_summary.json').read_text(encoding='utf-8'))
    for field in ('verified','exact_model','same_series_representative','missing'):
        assert summary[field]==report[field], f'Stale summary: {field}'
    assert summary['unique_image_files']==len(shipped)
    assert summary['optimized_total_bytes']==sum(p.stat().st_size for p in shipped), 'Count shared files once'
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__': check()
