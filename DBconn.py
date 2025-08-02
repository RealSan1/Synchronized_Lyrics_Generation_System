import sqlite3

def get_connection():
    conn = sqlite3.connect(r"C:\Users\San\Desktop\db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn
