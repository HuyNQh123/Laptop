"""Source updates preserve laptop data and source IDs and are repeatable."""
import csv
from contextlib import closing
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest

from scripts.sync_audited_sources import sync_sources

ROOT = Path(__file__).resolve().parents[1]


class SourceSyncTests(unittest.TestCase):
    def test_selective_backup_and_idempotent_update(self):
        with tempfile.TemporaryDirectory() as folder:
            db = Path(folder) / 'laptops.db'
            shutil.copyfile(ROOT / 'data/laptops.db', db)
            with closing(sqlite3.connect(db)) as conn, conn:
                laptops = conn.execute('SELECT * FROM laptops ORDER BY id').fetchall()
                identities = conn.execute('SELECT id,laptop_name,field_name FROM laptop_sources ORDER BY id').fetchall()
                conn.execute("UPDATE laptop_sources SET status='Verified'")
            preview = sync_sources(db, ROOT/'data/laptop_sources.csv', Path(folder)/'backups')
            self.assertEqual(preview['changed'], 1125)
            result = sync_sources(db, ROOT/'data/laptop_sources.csv', Path(folder)/'backups', True)
            self.assertTrue(Path(result['backup']).is_file())
            with closing(sqlite3.connect(result['backup'])) as backup:
                self.assertEqual(backup.execute("SELECT count(*) FROM laptop_sources WHERE status='Verified'").fetchone()[0], 1125)
            with closing(sqlite3.connect(db)) as conn:
                self.assertEqual(laptops, conn.execute('SELECT * FROM laptops ORDER BY id').fetchall())
                self.assertEqual(identities, conn.execute('SELECT id,laptop_name,field_name FROM laptop_sources ORDER BY id').fetchall())
                self.assertEqual(dict(conn.execute('SELECT status,count(*) FROM laptop_sources GROUP BY status')), {'Đã xác minh':571,'Chưa xác minh được':60,'Chưa có nguồn xác minh':494})
            repeat = sync_sources(db, ROOT/'data/laptop_sources.csv', Path(folder)/'backups', True)
            self.assertEqual(repeat['changed'], 0)
            self.assertIsNone(repeat['backup'])

    def test_duplicate_csv_identity_rejected_without_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            with (ROOT/'data/laptop_sources.csv').open(encoding='utf-8-sig', newline='') as source:
                reader = csv.DictReader(source)
                fields, row = reader.fieldnames, next(reader)
            duplicate = Path(folder)/'duplicate.csv'
            with duplicate.open('w', encoding='utf-8', newline='') as out:
                writer = csv.DictWriter(out, fieldnames=fields)
                writer.writeheader(); writer.writerows([row, row])
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                sync_sources(ROOT/'data/laptops.db', duplicate, folder, True)


if __name__ == '__main__':
    unittest.main()
