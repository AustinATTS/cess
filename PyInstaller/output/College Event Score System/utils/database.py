import sqlite3
import CTkMessagebox as ctkm
import os
from utils.logging import logger

def get_db():
    database_path = os.path.join("data", "database.db")
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except Exception as e:
        ctkm.CTkMessagebox(title="Error", message=f"Error: {e}", icon="cancel")
        logger.warning(f"Error {e}")
        raise


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        theme_path TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS participants (
                        id INTEGER PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT,
                        team_id INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        member_count INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        type TEXT NOT NULL,
                        date TEXT NOT NULL,
                        location TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY NOT NULL,
                        participant_id INTEGER NOT NULL,
                        event_id INTEGER NOT NULL,
                        score INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        team_id INTEGER)''')
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

    for team_id, team_name, member_count in [(1, 'Team 1', 0), (2, 'Team 2', 0), (3, 'Team 3', 0), (4, 'Team 4', 0),
                                             (5, 'Team 5', 0)]:
        cursor.execute("INSERT OR IGNORE INTO teams (id, name, member_count) VALUES (?, ?, ?)",
                       (team_id, team_name, member_count))

    cursor.execute('''CREATE TRIGGER IF NOT EXISTS restrict_team1_events
                      BEFORE INSERT ON scores
                      FOR EACH ROW
                      WHEN (SELECT team_id FROM participants WHERE id = NEW.participant_id) = 1
                      BEGIN
                          SELECT RAISE(FAIL, 'Participant in Team 1 cannot attend more than 5 events')
                          WHERE (SELECT COUNT(*) FROM scores WHERE participant_id = NEW.participant_id) >= 5;
                      END;''')

    cursor.execute('''CREATE TRIGGER IF NOT EXISTS enforce_team_events
                      BEFORE INSERT ON scores
                      FOR EACH ROW
                      WHEN (SELECT team_id FROM participants WHERE id = NEW.participant_id) BETWEEN 2 AND 5
                      BEGIN
                          INSERT INTO scores (participant_id, event_id, score, date, team_id)
                          SELECT p.id, NEW.event_id, NEW.score, NEW.date, p.team_id
                          FROM participants p
                          WHERE p.team_id = (SELECT team_id FROM participants WHERE id = NEW.participant_id)
                          AND NOT EXISTS (SELECT 1 FROM scores WHERE participant_id = p.id AND event_id = NEW.event_id);
                          SELECT RAISE(IGNORE);
                      END;''')

    conn.commit()
    conn.close()
    logger.info(f"Database Initialised")



if __name__ == "__main__":
    init_db()