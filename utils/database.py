import sqlite3
import CTkMessagebox as ctkm
import os

def get_db():
    database_path = os.path.join("data", "database.db")
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except sqlite3.OperationalError as e:
        ctkm.CTkMessagebox(title="Error", message=f"SQLite error: {e}", icon="cancel")
        raise

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS participants (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        phone TEXT,
                        team_id INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        member_count INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        type TEXT,
                        date TEXT,
                        location TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY,
                        participant_id INTEGER,
                        event_id INTEGER,
                        score INTEGER,
                        date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        date TEXT,
                        details TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS backups (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        date TEXT,
                        details TEXT)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()