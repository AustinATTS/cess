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

    # Ensure teams are initialized
    for team_id, team_name, member_count in [(1, 'Team 1', 0), (2, 'Team 2', 0), (3, 'Team 3', 0), (4, 'Team 4', 0),
                                             (5, 'Team 5', 0)]:
        cursor.execute("INSERT OR IGNORE INTO teams (id, name, member_count) VALUES (?, ?, ?)",
                       (team_id, team_name, member_count))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()