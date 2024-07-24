import random
import string
import os
import sqlite3

def get_db():
    database_path = os.path.join("..", "data", "database.db")
    conn = sqlite3.connect(database_path)
    return conn

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def random_email():
    return random_string(5) + '@example.com'


def random_phone():
    return ''.join(random.choice(string.digits) for i in range(10))


def add_random_participants():
    conn = get_db()
    cursor = conn.cursor()

    # Add 20 participants to Team 1
    for _ in range(20):
        name = random_string()
        email = random_email()
        phone = random_phone()
        team_id = 1
        cursor.execute("INSERT INTO participants (name, email, phone, team_id) VALUES (?, ?, ?, ?)",
                       (name, email, phone, team_id))

    # Add 5 participants to each of Teams 2-5
    for team_id in range(2, 6):
        for _ in range(5):
            name = random_string()
            email = random_email()
            phone = random_phone()
            cursor.execute("INSERT INTO participants (name, email, phone, team_id) VALUES (?, ?, ?, ?)",
                           (name, email, phone, team_id))

    conn.commit()

    # Update the member_count for each team
    update_team_member_count(conn)

    conn.close()


def update_team_member_count(conn):
    cursor = conn.cursor()

    # Update the member_count for each team
    for team_id in range(1, 6):
        cursor.execute("SELECT COUNT(*) FROM participants WHERE team_id = ?", (team_id,))
        member_count = cursor.fetchone()[0]
        cursor.execute("UPDATE teams SET member_count = ? WHERE id = ?", (member_count, team_id))

    conn.commit()

add_random_participants()