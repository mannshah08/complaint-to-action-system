import sqlite3

DB_NAME = "complaints.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            text TEXT NOT NULL,
            category TEXT NOT NULL,
            urgency TEXT NOT NULL,
            status TEXT NOT NULL,
            visibility TEXT NOT NULL,
            upvotes INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
