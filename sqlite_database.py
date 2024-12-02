import sqlite3

def create_connection(db_file):
    """ ایجاد اتصال به دیتابیس SQLite """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    return conn

def create_table(conn):
    """ ایجاد جدول در دیتابیس برای ذخیره داده‌ها """
    try:
        sql_create_table = '''CREATE TABLE IF NOT EXISTS documents (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                content TEXT NOT NULL,
                                embedding BLOB NOT NULL
                            );'''
        conn.execute(sql_create_table)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def insert_document(conn, title, content, embedding):
    """ افزودن سند جدید به دیتابیس """
    try:
        sql_insert = '''INSERT INTO documents (title, content, embedding) VALUES (?, ?, ?)'''
        conn.execute(sql_insert, (title, content, embedding))
        conn.commit()
        print(f"Document '{title}' inserted successfully")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def fetch_all_documents(conn):
    """ دریافت تمام اسناد از دیتابیس """
    try:
        cursor = conn.execute('SELECT * FROM documents')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []
