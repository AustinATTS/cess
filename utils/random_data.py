import random
import string
import os
import sqlite3
from datetime import datetime, timedelta
import hashlib

def get_db():
    database_path = os.path.join("..", "data", "database.db")
    conn = sqlite3.connect(database_path)
    return conn

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")


def add_random_events():
    conn = get_db()
    cursor = conn.cursor()

    # Set date range for events
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)  # One year from now

    for _ in range(20):
        name = random_string(10)
        event_type = random.choice(['Conference', 'Workshop', 'Seminar', 'Webinar', 'Meetup'])
        date = random_date(start_date, end_date)
        location = random_string(12)

        cursor.execute("INSERT INTO events (name, type, date, location) VALUES (?, ?, ?, ?)",
                       (name, event_type, date, location))

    conn.commit()
    conn.close()


def verify_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return events


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


def hash_password(password):
    """Hash a password using SHA-256."""
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def add_users():
    conn = get_db()
    cursor = conn.cursor()

    # Define users with their roles and passwords
    users = [
        ('user', 'atts', 'Viewer'),
        ('judge', 'atts', 'Judge'),
        ('admin', 'atts', 'Admin')
    ]

    # Insert each user into the database with a hashed password
    for username, password, role in users:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, role))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_users()
    add_random_events()
    add_random_participants()
