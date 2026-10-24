import pandas as pd
import numpy as np
import sqlite3
import os
from sqlalchemy import create_engine
from src.config import get_database_uri

def load_data_from_db():
    """Đọc dữ liệu laptop trực tiếp từ Database (MySQL hoặc SQLite dự phòng)."""
    try:
        db_uri, _ = get_database_uri()
        engine = create_engine(db_uri)
        df = pd.read_sql_table("laptops", engine)
        return df
    except Exception:
        db_path = 'data/laptops.db'
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                df = pd.read_sql_query("SELECT * FROM laptops", conn)
                conn.close()
                return df
            except Exception:
                pass
        return None

def load_data(filepath='data/laptops.csv', prefer_db=True):
    """Đọc dữ liệu từ Database (MySQL/SQLite) hoặc từ file CSV."""
    if prefer_db:
        df_db = load_data_from_db()
        if df_db is not None and not df_db.empty:
            return df_db

    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' không tồn tại.")
        return None

def remove_duplicates(df):
    """Xóa các dòng dữ liệu trùng lặp."""
    initial_rows = len(df)
    df = df.drop_duplicates(keep='first')
    df = df.reset_index(drop=True)
    removed_rows = initial_rows - len(df)
    return df, removed_rows

def normalize_brand(df):
    """Chuẩn hóa tên hãng (Viết hoa chữ cái đầu hoặc viết hoa toàn bộ tùy hãng)."""
    if 'brand' in df.columns:
        # Chuyển tất cả về chữ thường trước, sau đó Title Case
        df['brand'] = df['brand'].str.strip().str.title()
        # Chỉnh lại một số hãng viết hoa toàn bộ
        df['brand'] = df['brand'].replace({'Hp': 'HP', 'Msi': 'MSI', 'Asus': 'ASUS'})
    return df

def convert_numeric_columns(df):
    """Chuyển đổi các cột có chứa chữ thành số hợp lệ."""
    # Xử lý cột ram (vd: "8GB" -> 8)
    if 'ram' in df.columns:
        df['ram'] = df['ram'].astype(str).str.replace('GB', '', regex=False).str.strip()
        df['ram'] = pd.to_numeric(df['ram'], errors='coerce')
        
    # Xử lý các cột khác thành kiểu numeric để tránh lỗi
    numeric_cols = ['cpu_score', 'gpu_score', 'storage', 'screen_size', 
                    'refresh_rate', 'weight', 'battery', 'rating', 'price', 'units_sold']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def handle_missing_values(df):
    """Xử lý các giá trị bị thiếu."""
    # Điền giá trị trung bình (median/mean) cho các cột số quan trọng
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        # Dùng median cho an toàn với outlier (đặc biệt là giá tiền)
        df[col] = df[col].fillna(df[col].median())
    
    # Với Categorical (String), có thể điền "Unknown" hoặc "N/a"
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].fillna("N/a")
        
    return df

def clean_data(df, verbose=False):
    """Hàm tổng hợp để chạy toàn bộ quy trình làm sạch dữ liệu."""
    if verbose:
        print("--- BAT DAU CLEANING ---")
        print(f"So dong ban dau: {len(df)}")
    
    # 1. Xóa duplicate
    df, removed = remove_duplicates(df)
    if verbose:
        print(f"Da xoa {removed} dong duplicate.")
    
    # 2. Chuẩn hóa brand
    df = normalize_brand(df)
    
    # 3. Chuyển kiểu dữ liệu
    df = convert_numeric_columns(df)
    
    # 4. In ra missing values trước khi xử lý (nếu verbose)
    if verbose:
        print("\nMissing values cua tung column (Truoc khi xu ly):")
        print(df.isnull().sum())
    
    # 5. Xử lý missing values
    df = handle_missing_values(df)
    
    if verbose:
        print("\nSo dong sau cleaning:", len(df))
        print("\nData Types:")
        print(df.dtypes)
        print("--- HOAN THANH CLEANING ---")
    
    return df

if __name__ == '__main__':
    # Chạy thử
    df_raw = load_data('data/laptops.csv')
    if df_raw is not None:
        df_clean = clean_data(df_raw)
        print("\n5 laptop đầu tiên sau khi clean:")
        print(df_clean.head())
