"""Regression checks against the bundled catalog, without running or writing ML artifacts."""
import sqlite3
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.catalog import catalog_context, product_view


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connection = sqlite3.connect(f'file:{ROOT / "data/laptops.db"}?mode=ro', uri=True)
        connection.row_factory = sqlite3.Row
        cls.rows = [dict(row) for row in connection.execute('SELECT * FROM laptops ORDER BY id')]
        connection.close()
        database_uri = f'sqlite:///file:{(ROOT / "data/laptops.db").as_posix()}?mode=ro&uri=true'
        with patch('src.config.get_database_uri', return_value=(database_uri, 'sqlite')):
            from app import app
        cls.client = app.test_client()
        cls.app = app

    def context(self, **args):
        return catalog_context(self.rows, args)

    def test_combined_filters_match_raw_data(self):
        expected = [row for row in self.rows if row['brand'] == 'ASUS' and row['price'] <= 30000000
                    and row['ram'] >= 16 and row['weight'] <= 1.5]
        actual = self.context(brand='ASUS', budget='30000000', ram='16', weight='1.5', per_page='100')
        self.assertGreater(len(expected), 0)
        self.assertEqual([r['id'] for r in actual['laptops']], [r['id'] for r in expected])

    def test_existing_quick_filters(self):
        predicates = {'budget': lambda r: r['price'] <= 20000000, 'light': lambda r: r['weight'] <= 1.5,
                      'gaming': lambda r: r['gpu_score'] >= 7000, 'ram16': lambda r: r['ram'] >= 16,
                      'apple': lambda r: r['brand'].lower() == 'apple'}
        for quick, predicate in predicates.items():
            with self.subTest(quick=quick):
                self.assertEqual(self.context(quick=quick)['total'], len(list(filter(predicate, self.rows))))

    def test_numeric_sort_and_pagination_do_not_drop_or_duplicate_rows(self):
        expected = [r['id'] for r in sorted(self.rows, key=lambda r: r['price'])]
        actual = []
        for page in range(1, self.context()['pages'] + 1):
            actual.extend(r['id'] for r in self.context(sort='price', page=str(page))['laptops'])
        self.assertEqual(actual, expected)
        self.assertEqual(self.context(sort='price', direction='desc')['laptops'][0]['price'], max(r['price'] for r in self.rows))

    def test_search_and_invalid_query_parameters(self):
        self.assertEqual(self.context(q='zenbook')['total'], self.context(q='ZENBOOK')['total'])
        self.assertGreater(self.context(q='core i5')['total'], 0)
        self.assertEqual(self.context(q='no-such-laptop-xyz')['total'], 0)
        result = self.context(page='99999', per_page='invalid', sort='__dict__', direction='bad')
        self.assertEqual(result['page'], result['pages'])
        self.assertEqual(result['state']['sort'], 'id')
        self.assertEqual(self.context(page='-1')['page'], 1)

    def test_missing_and_outside_images_use_placeholder(self):
        self.assertFalse(product_view(self.rows[0])['has_image'])
        with patch('src.catalog.json.loads', return_value={self.rows[0]['name']: {'path': '../app.py'}}):
            self.assertEqual(product_view(self.rows[0])['image_path'], 'images/laptop-placeholder.svg')

    def test_pages_escape_search_and_preserve_query_in_pagination(self):
        for path in ['/', '/laptops', '/compare']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        response = self.client.get('/laptops?' + urlencode({'q': '<script>alert(1)</script>'}))
        html = response.get_data(as_text=True)
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('Chưa tìm thấy laptop phù hợp', html)
        html = self.client.get('/laptops?brand=ASUS&sort=price&per_page=10').get_data(as_text=True)
        self.assertIn('brand=ASUS', html)
        self.assertIn('page=2', html)
        self.assertEqual(html.count('class="product-card"'), 10)

    def test_source_api_and_assets(self):
        row = self.rows[0]
        response = self.client.get(f'/api/laptop-sources/{row["id"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['laptop_name'], row['name'])
        self.assertGreater(len(response.json['sources']), 0)
        self.assertIn('verified_date', response.json['sources'][0])
        self.assertEqual(self.client.get('/api/laptop-sources/99999999').status_code, 404)
        for asset in ['css/style.css', 'js/ui.js', 'js/catalog.js', 'images/laptop-placeholder.svg']:
            with self.client.get('/static/' + asset) as response:
                self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
