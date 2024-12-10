import sqlite3
import os

def execute_sql_file(database, file_path):
    """
    Thực thi một tệp SQL trên cơ sở dữ liệu SQLite.
    """
    try:
        with sqlite3.connect(database) as conn:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            conn.executescript(sql_script)
            print(f"Successfully executed {file_path}")
    except Exception as e:
        print(f"Error executing {file_path}: {e}")

def init_db():
    """
    Hàm khởi tạo cơ sở dữ liệu và chạy các tệp SQL từ thư mục migrations.
    """
    database = "ebook.db"

    # Kiểm tra xem tệp cơ sở dữ liệu đã tồn tại chưa
    if os.path.exists(database):
        print(f"Cơ sở dữ liệu {database} đã tồn tại. Đang thực thi các tệp SQL...")
    else:
        print(f"Tạo mới cơ sở dữ liệu {database}...")

    # Thực thi file schema.sql (tạo bảng)
    execute_sql_file(database, "migrations/schema.sql")

    # Thực thi file seed.sql (nếu có dữ liệu mẫu)
    if os.path.exists("migrations/seed.sql"):
        execute_sql_file(database, "migrations/seed.sql")

    print(f"Khởi tạo cơ sở dữ liệu {database} hoàn tất.")

if __name__ == "__main__":
    init_db()
