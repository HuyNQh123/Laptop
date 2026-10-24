import os
import sys
import pandas as pd
from flask import Flask

# Đảm bảo console Windows hỗ trợ UTF-8
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Đảm bảo import được các module trong src
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.config import get_database_uri, MYSQL_USER, MYSQL_HOST, MYSQL_PORT, MYSQL_DB
from src.models import db, Laptop, LaptopSource
from src.data_cleaning import load_data, clean_data

def create_app_for_db():
    app = Flask(__name__)
    db_uri, db_type = get_database_uri()
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app, db_type

def migrate_csv_to_db():
    app, db_type = create_app_for_db()
    with app.app_context():
        if db_type == "mysql":
            print(f"[*] Ket noi MySQL thanh cong: {MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")
            print("[*] Khoi tao cau truc bang trong MySQL...")
        else:
            print("[*] Su dung SQLite du phong (kiem tra cau hinh MySQL trong file .env)...")
            print("[*] Khoi tao cau truc bang trong SQLite...")

        db.create_all()

        # 1. Migrate dữ liệu laptops
        csv_laptops_path = os.path.join('data', 'laptops.csv')
        if os.path.exists(csv_laptops_path):
            df_raw = load_data(csv_laptops_path, prefer_db=False)
            if df_raw is not None:
                df_clean = clean_data(df_raw)
                
                # Xóa dữ liệu cũ nếu muốn nạp mới
                Laptop.query.delete()
                
                laptops_to_add = []
                for _, row in df_clean.iterrows():
                    laptop = Laptop(
                        name=str(row.get('name', '')).strip(),
                        brand=str(row.get('brand', '')).strip(),
                        cpu=str(row.get('cpu', '')).strip(),
                        cpu_score=int(row.get('cpu_score', 0)),
                        gpu=str(row.get('gpu', '')).strip(),
                        gpu_score=int(row.get('gpu_score', 0)),
                        ram=int(row.get('ram', 8)),
                        storage=int(row.get('storage', 512)),
                        screen_size=float(row.get('screen_size', 14.0)),
                        resolution=str(row.get('resolution', '1920x1080')).strip(),
                        refresh_rate=int(row.get('refresh_rate', 60)),
                        weight=float(row.get('weight', 1.5)),
                        battery=float(row.get('battery', 50.0)),
                        operating_system=str(row.get('operating_system', 'Windows 11 Home')).strip(),
                        rating=float(row.get('rating', 4.5)),
                        price=float(row.get('price', 0.0)),
                        units_sold=float(row.get('units_sold', 0.0))
                    )
                    laptops_to_add.append(laptop)
                
                db.session.bulk_save_objects(laptops_to_add)
                db.session.commit()
                print(f"[OK] Da nap thanh cong {len(laptops_to_add)} laptop tu '{csv_laptops_path}' vao {db_type.upper()}!")
        else:
            print(f"[WARN] Khong tim thay file '{csv_laptops_path}'.")

        # 2. Migrate dữ liệu laptop_sources
        csv_sources_path = os.path.join('data', 'laptop_sources.csv')
        if os.path.exists(csv_sources_path):
            try:
                df_sources = pd.read_csv(csv_sources_path)
                LaptopSource.query.delete()
                
                sources_to_add = []
                for _, row in df_sources.iterrows():
                    source = LaptopSource(
                        laptop_name=str(row.get('laptop_name', '')).strip(),
                        field_name=str(row.get('field_name', '')).strip() if pd.notna(row.get('field_name')) else None,
                        source_name=str(row.get('source_name', '')).strip() if pd.notna(row.get('source_name')) else None,
                        source_url=str(row.get('source_url', '')).strip() if pd.notna(row.get('source_url')) else None,
                        verified_date=str(row.get('verified_date', '')).strip() if pd.notna(row.get('verified_date')) else None,
                        status=str(row.get('status', '')).strip() if pd.notna(row.get('status')) else None,
                        note=str(row.get('note', '')).strip() if pd.notna(row.get('note')) else None
                    )
                    sources_to_add.append(source)
                
                db.session.bulk_save_objects(sources_to_add)
                db.session.commit()
                print(f"[OK] Da nap thanh cong {len(sources_to_add)} ban ghi nguon kiem chung vao {db_type.upper()}!")
            except Exception as e:
                print(f"[ERROR] Loi khi nap laptop_sources: {e}")

        # Kiểm tra kết quả
        total_laptops = Laptop.query.count()
        total_sources = LaptopSource.query.count()
        print(f"[INFO] Tong ket {db_type.upper()} Database: {total_laptops} laptops, {total_sources} nguon doi chieu.")

if __name__ == '__main__':
    migrate_csv_to_db()
