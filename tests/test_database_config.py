"""The demo must be able to serve the database included in its deployment artifact."""
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from src.config import get_database_uri, SQLITE_PATH, SQLITE_URI


class DatabaseConfigTests(unittest.TestCase):
    def test_explicit_sqlite_uses_bundled_file_without_mysql_probe(self):
        with patch.dict(os.environ, {'DATABASE_BACKEND': 'sqlite'}):
            with patch('pymysql.connect', side_effect=AssertionError('Must not contact MySQL')) as connect:
                self.assertEqual(get_database_uri(), (SQLITE_URI, 'sqlite'))
                connect.assert_not_called()
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(Path(SQLITE_PATH), root/'data/laptops.db')
        self.assertTrue(Path(SQLITE_PATH).is_file())

    def test_auto_preserves_existing_sqlite_fallback(self):
        with patch.dict(os.environ, {'DATABASE_BACKEND': 'auto'}):
            with patch('pymysql.connect', side_effect=OSError('Test MySQL unavailable')):
                self.assertEqual(get_database_uri(), (SQLITE_URI, 'sqlite'))

    def test_unknown_backend_fails_instead_of_silently_selecting_other_data(self):
        with patch.dict(os.environ, {'DATABASE_BACKEND': 'sqltie'}):
            with self.assertRaisesRegex(ValueError, 'DATABASE_BACKEND'):
                get_database_uri()


if __name__ == '__main__':
    unittest.main()
