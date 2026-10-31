import os
import urllib.parse

# Tự động đọc file .env nếu có
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

# Cấu hình kết nối MySQL
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_DB = os.getenv('MYSQL_DB', 'laptop_db')

# Encode password đề phòng ký tự đặc biệt như @, #, $, %, etc.
encoded_password = urllib.parse.quote_plus(MYSQL_PASSWORD) if MYSQL_PASSWORD else ""

# Chuỗi kết nối MySQL
MYSQL_URI = f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

# Chuỗi kết nối SQLite dự phòng
SQLITE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'laptops.db'))
SQLITE_URI = f"sqlite:///{SQLITE_PATH}"

def get_database_uri():
    """Kiểm tra kết nối MySQL. Nếu thành công dùng MySQL, nếu chưa kết nối được thì dùng SQLite dự phòng."""
    # The Render demo can explicitly select the audited database shipped with Git.
    backend = os.getenv('DATABASE_BACKEND', 'auto').strip().lower()
    if backend == 'sqlite':
        return SQLITE_URI, 'sqlite'
    if backend != 'auto':
        raise ValueError('DATABASE_BACKEND must be auto or sqlite')
    try:
        import pymysql
        # Thử kết nối đến MySQL server
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=int(MYSQL_PORT),
            connect_timeout=2
        )
        with conn.cursor() as cursor:
            # Tự động tạo database nếu chưa có
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        return MYSQL_URI, "mysql"
    except Exception as e:
        # Nếu MySQL chưa thể kết nối (vd: chưa có password đúng), dùng SQLite dự phòng để web không bị crash
        return SQLITE_URI, "sqlite"
