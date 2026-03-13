import sqlite3
import os

DB_NAME = 'wellness_tracker.db'

def get_connection():
    """Returns a connection to the SQLite database."""
    # Ensure the directory exists if we eventually move it, but here it's root
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Users table (for future scaling/relations)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create Daily Metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date DATE NOT NULL,
            steps INTEGER,
            calories INTEGER,
            heart_rate INTEGER,
            screen_time REAL,
            sleep_hours REAL,
            productivity INTEGER,
            UNIQUE(username, date),
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
