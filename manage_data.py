import os
import sys
import argparse
from datetime import date
import pandas as pd
from flask import Flask

# Đảm bảo console Windows hỗ trợ UTF-8
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import models
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.models import db, Laptop, LaptopSource

def create_app():
    app = Flask(__name__)
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'laptops.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def cmd_summary():
    """Hiển thị tóm tắt tình trạng dữ liệu trong Database."""
    app = create_app()
    with app.app_context():
        total_laptops = Laptop.query.count()
        total_sources = LaptopSource.query.count()
        avg_price = db.session.query(db.func.avg(Laptop.price)).scalar() or 0
        min_price = db.session.query(db.func.min(Laptop.price)).scalar() or 0
        max_price = db.session.query(db.func.max(Laptop.price)).scalar() or 0

        print("=" * 60)
        print("📊 TỔNG QUAN CƠ SỞ DỮ LIỆU LAPTOP (SQLITE)")
        print("=" * 60)
        print(f"• Tổng số laptop:           {total_laptops} mẫu")
        print(f"• Tổng số nguồn kiểm chứng:  {total_sources} bản ghi (PassMark, CellphoneS...)")
        print(f"• Giá trung bình thị trường: {avg_price:,.0f} VNĐ")
        print(f"• Khoảng giá niêm yết:      {min_price:,.0f} VNĐ - {max_price:,.0f} VNĐ")
        print("=" * 60)

def cmd_update_price(laptop_name, new_price, source_url=None):
    """Cập nhật giá thị trường của laptop và ghi log nguồn đối chiếu mới."""
    app = create_app()
    with app.app_context():
        laptop = Laptop.query.filter(Laptop.name.ilike(f"%{laptop_name}%")).first()
        if not laptop:
            print(f"[ERROR] Không tìm thấy laptop có tên chứa '{laptop_name}'!")
            return

        old_price = laptop.price
        laptop.price = float(new_price)

        # Cập nhật nguồn kiểm chứng trong bảng laptop_sources
        today_str = str(date.today())
        source = LaptopSource.query.filter_by(laptop_name=laptop.name, field_name='price & rating').first()
        if source:
            source.verified_date = today_str
            source.note = f"Cập nhật giá thị trường: {new_price:,.0f} VNĐ (Cũ: {old_price:,.0f} VNĐ)"
            if source_url:
                source.source_url = source_url
        else:
            new_source = LaptopSource(
                laptop_name=laptop.name,
                field_name='price & rating',
                source_name='CellphoneS / Retailer Verified',
                source_url=source_url or 'https://cellphones.com.vn/',
                verified_date=today_str,
                status='Verified',
                note=f"Cập nhật giá thị trường: {new_price:,.0f} VNĐ"
            )
            db.session.add(new_source)

        db.session.commit()
        print(f"[OK] Đã cập nhật giá cho '{laptop.name}':")
        print(f"     Giá cũ: {old_price:,.0f} VNĐ -> Giá mới: {new_price:,.0f} VNĐ")
        print(f"     Ngày xác minh: {today_str}")

def cmd_export_csv():
    """Xuất ngược dữ liệu từ SQLite ra file CSV để backup hoặc làm báo cáo."""
    app = create_app()
    with app.app_context():
        laptops = Laptop.query.order_by(Laptop.id.asc()).all()
        data = [l.to_dict() for l in laptops]
        df = pd.DataFrame(data)
        
        # Bỏ cột id nếu muốn giữ đúng format file cũ
        if 'id' in df.columns:
            df = df.drop(columns=['id'])
            
        csv_path = os.path.join('data', 'laptops.csv')
        df.to_csv(csv_path, index=False)
        print(f"[OK] Đã đồng bộ {len(df)} dòng dữ liệu từ SQLite sang file '{csv_path}'!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Công cụ dòng lệnh quản trị dữ liệu Laptop (Code/CLI Data Management)")
    subparsers = parser.add_subparsers(dest='command', help='Lệnh thực thi')

    # Lệnh summary
    subparsers.add_parser('summary', help='Xem tổng quan dữ liệu trong SQLite')

    # Lệnh update-price
    parser_price = subparsers.add_parser('update-price', help='Cập nhật giá thị trường cho laptop')
    parser_price.add_argument('--name', required=True, help='Tên hoặc mã model laptop cần cập nhật')
    parser_price.add_argument('--price', required=True, type=float, help='Giá bán thị trường mới (VNĐ)')
    parser_price.add_argument('--url', required=False, default=None, help='Link kiểm chứng nguồn giá (nếu có)')

    # Lệnh export-csv
    subparsers.add_parser('export-csv', help='Đồng bộ dữ liệu từ SQLite ra lại data/laptops.csv')

    args = parser.parse_args()

    if args.command == 'summary':
        cmd_summary()
    elif args.command == 'update-price':
        cmd_update_price(args.name, args.price, args.url)
    elif args.command == 'export-csv':
        cmd_export_csv()
    else:
        cmd_summary()
