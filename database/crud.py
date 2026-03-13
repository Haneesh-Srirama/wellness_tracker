import pandas as pd
from .db import get_connection

def add_user(username):
    """Add a new user if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
        conn.commit()
    finally:
        conn.close()

def save_daily_metrics(username, date_str, steps, calories, heart_rate, screen_time, sleep_hours, productivity):
    """Save or update metrics for a user on a given date."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO daily_metrics (username, date, steps, calories, heart_rate, screen_time, sleep_hours, productivity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username, date) DO UPDATE SET
                steps=excluded.steps,
                calories=excluded.calories,
                heart_rate=excluded.heart_rate,
                screen_time=excluded.screen_time,
                sleep_hours=excluded.sleep_hours,
                productivity=excluded.productivity
        ''', (username, date_str, steps, calories, heart_rate, screen_time, sleep_hours, productivity))
        conn.commit()
    finally:
        conn.close()

def get_user_data_df(username):
    """Retrieve all metrics for a user and return as a pandas DataFrame."""
    conn = get_connection()
    try:
        query = "SELECT * FROM daily_metrics WHERE username = ? ORDER BY date ASC"
        df = pd.read_sql_query(query, conn, params=(username,))
        if not df.empty:
            df['date'] = pd.to_datetime(df['date']).dt.date
        return df
    finally:
        conn.close()
