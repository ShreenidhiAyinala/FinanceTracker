import sqlite3
import os

DB_PATH = 'data/finance_tracker.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = sqlite3.connect('finance_tracker.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT,
        transaction_type TEXT,
        tags TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS recurring_transactions (
        id INTEGER PRIMARY KEY,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT,
        transaction_type TEXT,
        tags TEXT,
        frequency TEXT
    )
    ''')

    conn.commit()
    conn.close()

initialize_database()