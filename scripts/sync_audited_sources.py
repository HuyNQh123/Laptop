"""Apply the audited source CSV to existing SQLite source rows, never laptop data."""
import argparse
from collections import Counter
from contextlib import closing
import csv
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import uuid

ROOT = Path(__file__).resolve().parents[1]
KEY = ('laptop_name', 'field_name')
FIELDS = ('source_name', 'source_url', 'verified_date', 'status', 'note')
STATUSES = {'Đã xác minh', 'Chưa xác minh được', 'Chưa có nguồn xác minh'}


def sync_sources(database, source_csv, backup_dir, apply=False):
    database = Path(database).resolve()
    if not database.is_file():
        raise ValueError('Existing SQLite database required')
    with Path(source_csv).open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source)
        if not set(KEY + FIELDS).issubset(reader.fieldnames or []):
            raise ValueError('Source CSV schema mismatch')
        rows = list(reader)
    keys = [tuple(row[k] for k in KEY) for row in rows]
    if len(keys) != len(set(keys)) or any(not all(k) for k in keys):
        raise ValueError('Duplicate or empty source identity')
    if any(row['status'] not in STATUSES for row in rows):
        raise ValueError('Unknown audited status')
    connection = sqlite3.connect(f'file:{database.as_posix()}?mode=rw', uri=True)
    connection.row_factory = sqlite3.Row
    try:
        columns = {r['name'] for r in connection.execute('PRAGMA table_info(laptop_sources)')}
        if not set(('id',) + KEY + FIELDS).issubset(columns):
            raise ValueError('Source database schema mismatch')
        current = list(connection.execute('SELECT * FROM laptop_sources'))
        existing = {tuple(row[k] for k in KEY): row for row in current}
        names = {r[0] for r in connection.execute('SELECT name FROM laptops')}
        if len(existing) != len(current) or set(existing) != set(keys):
            raise ValueError('CSV/database source identities must match exactly')
        if any(row['laptop_name'] not in names for row in rows):
            raise ValueError('Source references an unknown laptop')
        changed = [row for row in rows if any((row[f] or '') != (existing[tuple(row[k] for k in KEY)][f] or '') for f in FIELDS)]
        backup_path = None
        if apply and changed:
            backup_dir = Path(backup_dir).resolve()
            backup_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            backup_path = backup_dir / f'laptops-before-source-sync-{stamp}-{uuid.uuid4().hex[:8]}.db'
            with closing(sqlite3.connect(backup_path)) as backup:
                connection.backup(backup)
            with connection:
                connection.executemany(
                    'UPDATE laptop_sources SET source_name=?, source_url=?, verified_date=?, status=?, note=? '
                    'WHERE laptop_name=? AND field_name=?',
                    [tuple(row[f] or None for f in FIELDS) + tuple(row[k] for k in KEY) for row in changed],
                )
        return {'rows': len(rows), 'changed': len(changed), 'applied': bool(apply),
                'backup': str(backup_path) if backup_path else None,
                'statuses': dict(Counter(row['status'] for row in rows))}
    finally:
        connection.close()


if __name__ == '__main__':
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=ROOT / 'data/laptops.db')
    parser.add_argument('--csv', type=Path, default=ROOT / 'data/laptop_sources.csv')
    parser.add_argument('--backup-dir', type=Path, default=ROOT / '.runtime/source-backups')
    parser.add_argument('--apply', action='store_true', help='Without this flag, report changes only')
    args = parser.parse_args()
    print(json.dumps(sync_sources(args.database, args.csv, args.backup_dir, args.apply), ensure_ascii=True, indent=2))
