"""Exercise real routes/model in an isolated output directory; never overwrite artifacts."""
import csv
import hashlib
import json
from decimal import Decimal
from html.parser import HTMLParser
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.product_images import unique_object, load_manifest, image_metadata

class ImageManifestTests(unittest.TestCase):
    def test_complete_unique_mapping_and_verified_assets(self):
        with (ROOT/'data/laptops.csv').open(encoding='utf-8') as source:
            rows = list(csv.DictReader(source))
        manifest = load_manifest()
        self.assertEqual(set(manifest), {r['name'] for r in rows})
        self.assertEqual(len(manifest), 225)
        verified = []
        for name, entry in manifest.items():
            metadata = image_metadata(name)
            if entry['verification_status'] == 'verified':
                verified.append(entry)
                self.assertTrue(metadata['has_image'])
                asset=ROOT/'static'/entry['path']
                self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), entry['sha256'])
                with Image.open(asset) as image:
                    image.verify()
                self.assertLess(asset.stat().st_size, 150000)
                self.assertTrue(entry['source_url'].startswith('https://'))
                self.assertEqual(entry['image_type'],'catalogue')
                self.assertTrue(entry['visual_checked'])
                self.assertIn(entry['match_level'],['exact_model','same_series_representative'])
                self.assertTrue(entry['model_evidence'])
            else:
                self.assertFalse(metadata['has_image'])
                self.assertEqual(metadata['image_path'], 'images/laptop-placeholder.svg')
        summary=json.loads((ROOT/'data/image_audit_summary.json').read_text(encoding='utf-8'))
        self.assertEqual(len(verified),summary['verified'])
        self.assertGreaterEqual(summary['pilot_verified'],10)

    def test_duplicate_or_normalized_duplicate_keys_are_rejected(self):
        for content in ['{"Laptop":{},"Laptop":{}}','{"Laptop":{}," laptop ":{}}']:
            with self.assertRaises(ValueError):
                json.loads(content, object_pairs_hook=unique_object)

    def test_shared_assets_have_matching_exterior_evidence_and_separate_rights(self):
        manifest=load_manifest()
        representatives={name:entry for name,entry in manifest.items()
                         if entry.get('match_level')=='same_series_representative'}
        self.assertEqual(len(representatives),2)
        for name,entry in representatives.items():
            source=manifest[entry['representative_source_key']]
            self.assertEqual(entry['path'],source['path'])
            self.assertEqual(entry['sha256'],source['sha256'])
            self.assertEqual(entry['rights_status'],source['rights_status'])
            self.assertEqual(entry['representative_comparison']['source_color'],entry['representative_comparison']['target_color'])
            self.assertGreaterEqual(len(entry['representative_comparison']['evidence_urls']),2)
            self.assertIn(name,source['shared_with'])
            self.assertIn(entry['representative_source_key'],image_metadata(name)['image_alt'])
        assets={e['path'] for e in manifest.values() if e['verification_status']=='verified'}
        summary=json.loads((ROOT/'data/image_audit_summary.json').read_text(encoding='utf8'))
        self.assertEqual(len(assets),summary['unique_image_files'])
        self.assertGreaterEqual(summary['verified']-len(assets),len(representatives))
        self.assertEqual(len(assets),len({e['sha256'] for e in manifest.values() if e['verification_status']=='verified'}))

    def test_status_not_just_file_existence_controls_visibility(self):
        manifest=load_manifest()
        name=next(k for k,v in manifest.items() if v['verification_status']=='verified')
        entry=dict(manifest[name],verification_status='model_unverified')
        self.assertFalse(image_metadata(name,{name:entry})['has_image'])

    def test_catalogue_visual_and_rights_checks_are_independent(self):
        manifest=load_manifest()
        name=next(k for k,v in manifest.items() if v['verification_status']=='verified')
        entry=dict(manifest[name],license='',license_url='',rights_status='not_declared')
        self.assertTrue(image_metadata(name,{name:entry})['has_image'])
        for change in [{'image_type':'user_photo'},{'visual_checked':False},
                       {'match_level':'unverified'},{'rights_status':'restricted'},
                       {'rights_status':'licensed','license':''},
                       {'match_level':'same_series_representative','representative_evidence':''},
                       {'path':'../app.py'},{'image_url':'javascript:alert(1)'}]:
            with self.subTest(change=change):
                self.assertFalse(image_metadata(name,{name:{**entry,**change}})['has_image'])
        representative={**entry,'match_level':'same_series_representative',
                        'representative_evidence':'Test fixture: same exterior, only RAM/SSD differ.'}
        self.assertTrue(image_metadata(name,{name:representative})['image_representative'])

class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        uri=f'sqlite:///file:{(ROOT/"data/laptops.db").as_posix()}?mode=ro&uri=true'
        with patch('src.config.get_database_uri',return_value=(uri,'sqlite')):
            from app import app
        cls.app=app
        cls.app.config.update(TESTING=True)
        cls.client=app.test_client()
        cls.uri=uri
        with (ROOT/'data/laptops.csv').open(encoding='utf-8') as source:
            cls.rows=list(csv.DictReader(source))
        cls.verified_names=[name for name,entry in load_manifest().items() if entry['verification_status']=='verified']
        cls.input_paths=[*list((ROOT/'data').glob('*.csv')),ROOT/'data/laptops.db',ROOT/'models/laptop_price_model.pkl']
        cls.hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in cls.input_paths}

    def setUp(self):
        self.old_cwd=Path.cwd()
        self.temp=tempfile.TemporaryDirectory()
        temp=Path(self.temp.name)
        (temp/'models').mkdir();(temp/'data').mkdir();(temp/'static/charts').mkdir(parents=True)
        shutil.copyfile(ROOT/'models/laptop_price_model.pkl',temp/'models/laptop_price_model.pkl')
        shutil.copyfile(ROOT/'data/laptops.csv',temp/'data/laptops.csv')
        os.chdir(temp)
        self.database=patch('src.data_cleaning.get_database_uri',return_value=(self.uri,'sqlite'))
        self.database.start()
        self.training=patch('src.price_prediction.train_and_evaluate_models',side_effect=AssertionError('UI checks must not retrain'))
        self.training.start()

    def tearDown(self):
        self.training.stop();self.database.stop()
        os.chdir(self.old_cwd);self.temp.cleanup()
        for path, expected in self.hashes.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected,str(path))

    def test_all_page_routes_run_with_real_data(self):
        for route in ['/', '/laptops', '/compare', '/predict', '/analysis', '/clustering']:
            with self.subTest(route=route):
                response=self.client.get(route)
                self.assertEqual(response.status_code,200)
                self.assertIn(b'<html lang="vi">',response.data)

    def test_merged_analysis_uses_new_context_without_undefined_variables(self):
        from flask import template_rendered
        from jinja2 import StrictUndefined
        from src.data_analysis import NUM_COLS, NUMERIC_COLS
        contexts=[]
        def capture(sender, template, context, **extra):
            contexts.append(context)
        old_undefined=self.app.jinja_env.undefined
        self.app.jinja_env.undefined=StrictUndefined
        template_rendered.connect(capture,self.app)
        try:
            response=self.client.get('/analysis')
            self.assertEqual(response.status_code,200)
            self.assertEqual(self.client.get('/stats').status_code,200)
        finally:
            self.app.jinja_env.undefined=old_undefined
            template_rendered.disconnect(capture,self.app)
        context=contexts[0]
        self.assertEqual(context['num_cols'],NUM_COLS)
        self.assertIn('units_sold',NUMERIC_COLS)  # main's clustering compatibility export
        self.assertEqual(len(context['stats']),len(NUM_COLS)*(len(context['brands'])+1))
        self.assertEqual(len(context['best_value_laptops']),5)
        self.assertEqual(len(context['top_selling']),5)
        html=response.get_data(as_text=True)
        for col in NUM_COLS:
            self.assertEqual(len(context['top_bottom'][col]['top3']),3)
            for prefix in ['hist_overall_','hist_by_brand_']:
                self.assertIn('charts/'+prefix+col+'.png',html)
                self.assertTrue((ROOT/'static/charts'/f'{prefix}{col}.png').is_file())
        self.assertIn('hardware_vs_price_analysis.png',html)
        price=next(s for s in context['stats'] if s['brand']=='Toàn bộ' and s['feature']=='price')
        self.assertIn(self.app.jinja_env.filters['vnd'](price['median']),html)
        self.assertIn('id="stats-brand"',html)
        self.assertIn('id="stats-search"',html)
        self.assertIn('/download/results',html)
        self.assertTrue(Path('data/laptop_results.csv').exists())

    def test_download_statistics_and_strict_catalog_contract(self):
        from jinja2 import StrictUndefined
        response=self.client.get('/download/results')
        self.assertEqual(response.status_code,200)
        self.assertIn('attachment',response.headers['Content-Disposition'])
        header=response.get_data(as_text=True).lstrip('\ufeff').splitlines()[0]
        self.assertTrue({'brand','feature','mean','median','std','count'} <= set(header.split(',')))
        response.close()
        old_undefined=self.app.jinja_env.undefined
        self.app.jinja_env.undefined=StrictUndefined
        try:
            html=self.client.get('/laptops?quick=apple&sort=price&direction=desc&per_page=10&page=2').get_data(as_text=True)
            self.assertIn('name="per_page"',html)
            self.assertIn('Ảnh sản phẩm:',html)
            self.assertIn('data-source-id=',html)
            self.assertIn('quick=apple',html)
        finally:
            self.app.jinja_env.undefined=old_undefined

    def test_real_comparison_and_invalid_selections(self):
        form={'laptop1':self.verified_names[0],'laptop2':self.verified_names[1],
              'attributes':['cpu_score','gpu_score','ram','storage','price']}
        response=self.client.post('/compare',data=form)
        self.assertEqual(response.status_code,200)
        self.assertIn('Thông số và chênh lệch',response.get_data(as_text=True))
        self.assertEqual(response.get_data(as_text=True).count('Ảnh sản phẩm:'),2)
        for name in self.verified_names[:2]:
            self.assertIn(load_manifest()[name]['path'],response.get_data(as_text=True))
        self.assertTrue(Path('static/charts/radar_comparison.png').exists())
        for change in [{'laptop2':form['laptop1']},{'laptop1':'unknown model'},{'attributes':['price']},{'attributes':['name','brand','price']}]:
            with self.subTest(change=change):
                html=self.client.post('/compare',data={**form,**change}).get_data(as_text=True)
                self.assertIn('role="alert"',html)

    def valid_form(self):
        return dict(cpu_score='18000',gpu_score='12000',ram='16',storage='512',screen_size='15.6',refresh_rate='144',weight='2.1',battery='70',rating='4.5')

    def test_real_prediction_and_recommendations_keep_features(self):
        from src.price_prediction import FEATURE_COLS
        self.assertEqual(FEATURE_COLS,['cpu_score','gpu_score','ram','storage','screen_size','refresh_rate','weight','battery','rating'])
        response=self.client.post('/predict',data=self.valid_form())
        self.assertEqual(response.status_code,200)
        html=response.get_data(as_text=True)
        self.assertIn('Kết quả ước tính',html)
        self.assertEqual(html.count('class="product-card"'),5)
        self.assertIn('Chênh lệch',html)

    def test_default_numeric_inputs_follow_native_min_step_constraints(self):
        class NumberInputs(HTMLParser):
            def __init__(self): super().__init__(); self.inputs=[]
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs)
                if tag=='input' and attrs.get('type')=='number': self.inputs.append(attrs)
        parser=NumberInputs()
        parser.feed(self.client.get('/predict').get_data(as_text=True))
        self.assertEqual(len(parser.inputs),9)
        for field in parser.inputs:
            value=Decimal(field['value']); minimum=Decimal(field['min'])
            self.assertGreaterEqual(value,minimum,field['name'])
            if field['step']!='any':
                self.assertEqual((value-minimum)%Decimal(field['step']),0,field['name'])

    def test_prediction_validation_and_preserved_form(self):
        for change in [{'cpu_score':''},{'cpu_score':'abc'},{'gpu_score':'-1'},{'ram':'NaN'},{'storage':'Infinity'},{'rating':'6'},{'screen_size':'31'},{'weight':'16'}]:
            with self.subTest(change=change):
                response=self.client.post('/predict',data={**self.valid_form(),**change})
                self.assertEqual(response.status_code,200)
                html=response.get_data(as_text=True)
                self.assertIn('role="alert"',html)
                self.assertIn('name="refresh_rate" value="144"',html)
                self.assertNotIn('class="estimated-price"',html)

    def test_verified_image_shared_in_recommendation_cards(self):
        row=next(r for r in self.rows if r['name']==self.verified_names[0])
        row={**row,**{key:float(row[key]) for key in ['price','ram','storage','cpu_score','gpu_score','screen_size','refresh_rate','weight','battery','rating']},'price_diff_str':'+0 đ','similarity_pct':99.5}
        with patch('src.price_prediction.recommend_similar_laptops',return_value=[row]):
            html=self.client.post('/predict',data=self.valid_form()).get_data(as_text=True)
        self.assertIn('Ảnh sản phẩm:',html)
        self.assertIn(load_manifest()[row['name']]['path'],html)

    def test_representative_badge_and_source_identity_in_all_product_views(self):
        name=next(n for n,e in load_manifest().items() if e['match_level']=='same_series_representative')
        source=load_manifest()[name]['representative_source_key']
        from urllib.parse import urlencode
        html=self.client.get('/laptops?'+urlencode({'q':name})).get_data(as_text=True)
        self.assertIn('Ảnh đại diện cùng dòng',html)
        self.assertIn(source,html)
        html=self.client.post('/compare',data={'laptop1':name,'laptop2':source,'attributes':['ram','storage','price']}).get_data(as_text=True)
        self.assertIn('Ảnh đại diện cùng dòng',html)
        row=next(r for r in self.rows if r['name']==name)
        row={**row,**{key:float(row[key]) for key in ['price','ram','storage','cpu_score','gpu_score','screen_size','refresh_rate','weight','battery','rating']},'price_diff_str':'+0 đ','similarity_pct':99.5}
        with patch('src.price_prediction.recommend_similar_laptops',return_value=[row]):
            html=self.client.post('/predict',data=self.valid_form()).get_data(as_text=True)
        self.assertIn('Ảnh đại diện cùng dòng',html)
        self.assertIn(load_manifest()[name]['path'],html)

if __name__=='__main__': unittest.main()
