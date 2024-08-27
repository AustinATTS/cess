import customtkinter as ctk
import CTkMenuBar as ctkmb
import CTkMessagebox as ctkm
from PIL.ImageOps import expand
import assets.CTkCodeBox as ctkcb
import tkinter as tk
import io
import sys
from tkinter import scrolledtext
from PIL import Image
import os
import webbrowser
import urllib.parse
from gui.events import Events
from gui.participants import Participants
from gui.rankings import Rankings
from gui.reports import Reports
from gui.scores import Scores
from utils.database import get_db


class Main:
    def __init__(self, app):
        self.app = app

        self.events = Events(self)
        self.participants = Participants(self)
        self.rankings = Rankings(self)
        self.reports = Reports(self)
        self.scores = Scores(self)

    def load_page(self, frame):
        self.navigation_frame = ctk.CTkFrame(frame, width=250, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.content_frame = ctk.CTkFrame(frame, width=750, corner_radius=0)
        self.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.logo = ctk.CTkImage(Image.open(os.path.join("assets", "icons", "logo.png")), size=(100, 103))

        self.logo_label = ctk.CTkLabel(self.navigation_frame, text="", image=self.logo)
        self.title_label = ctk.CTkLabel(self.navigation_frame, text="College Event Score\nSystem", font=ctk.CTkFont(size=20, weight="bold"))
        self.appearance_label = ctk.CTkLabel(self.navigation_frame, text="Appearance:", anchor="w")
        self.feedback_label = ctk.CTkLabel(self.navigation_frame, text="Submit Feedback", font=("", 13))

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.title_label.grid(row=1, column=0, padx=20, pady=10)
        self.appearance_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.feedback_label.grid(row=9, column=0)

        self.appearance_optionmenu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.appearance)

        self.appearance_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.participants_button = ctk.CTkButton(self.navigation_frame, text="Participants", command=self.participant)
        self.events_button = ctk.CTkButton(self.navigation_frame, text="Events", command=self.event)
        self.scores_button = ctk.CTkButton(self.navigation_frame, text="Scores", command=self.score)
        self.rankings_button = ctk.CTkButton(self.navigation_frame, text="Rankings", command=self.ranking)
        self.reports_button = ctk.CTkButton(self.navigation_frame, text="Reports", command=self.report)

        self.participants_button.grid(row=2, column=0, padx=20, pady=10)
        self.events_button.grid(row=3, column=0, padx=20, pady=10)
        self.scores_button.grid(row=4, column=0, padx=20, pady=10)
        self.rankings_button.grid(row=5, column=0, padx=20, pady=10)
        self.reports_button.grid(row=6, column=0, padx=20, pady=10)

        self.feedback_label.bind("<Button-1>", lambda event: self.feedback())
        self.feedback_label.bind("<Enter>", lambda event: self.feedback_label.configure(font=("", 13, "underline"), cursor="hand2"))
        self.feedback_label.bind("<Leave>", lambda event: self.feedback_label.configure(font=("", 13), cursor="arrow"))

        user_id = self.app.login.user_id
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        self.role = str(cursor.fetchone())
        conn.close()

        role = self.role
        if role == "('Viewer',)":
            self.participants_button.configure(state="disabled")
            self.reports_button.configure(state="disabled")
            self.app.file_dropdown.configure(state="disabled")
            self.app.file_sub_menu.configure(state="disabled")
        elif role == "('Judge',)":
            self.app.file_dropdown.configure(state="normal")
            self.app.file_sub_menu.configure(state="disabled")
        elif role == "('Admin',)":
            self.app.file_dropdown.configure(state="normal")
            self.app.file_sub_menu.configure(state="normal")
            self.logo_label.bind("<Button-1>", lambda event: self.config())

    def appearance(self, appearance: str):
        ctk.set_appearance_mode(appearance.lower())

    def set_theme(self, theme_path):
        ctk.set_default_color_theme(theme_path)

    def clear_page(self):
        self.navigation_frame.destroy()
        self.content_frame.destroy()

    def clear(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def participant(self):
        self.clear(self.content_frame)
        self.participants.load_page(self.content_frame)

    def event(self):
        self.clear(self.content_frame)
        self.events.load_page(self.content_frame)

    def score(self):
        self.clear(self.content_frame)
        self.scores.load_page(self.content_frame)

    def ranking(self):
        self.clear(self.content_frame)
        self.rankings.load_page(self.content_frame)

    def report(self):
        self.clear(self.content_frame)
        self.reports.load_page(self.content_frame)

    def open_terminal(self):
        terminal_toplevel = ctk.CTkToplevel()
        terminal_toplevel.title("Terminal")
        terminal_toplevel.geometry(f"{600}x{400}")

        self.code_input = ctkcb.CTkCodeBox(terminal_toplevel, language="python")
        self.code_input.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(terminal_toplevel, wrap=tk.WORD, height=10, bg="black", fg="white")
        self.output_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        execute_button = ctk.CTkButton(terminal_toplevel, text="Execute", command=self.execute_code)
        execute_button.pack(pady=(0, 10))

    def execute_code(self):
        code = self.code_input.get("1.0", tk.END)
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        try:
            exec(code)
        except Exception as e:
            print(f"Error: {e}")
        sys.stdout = old_stdout
        self.output_text.insert(tk.END, redirected_output.getvalue())

    def config(self):
        # TODO add config menu to add users, init db, and other admin features
        config_toplevel = ctk.CTkToplevel()
        config_toplevel.title("Admin Config")
        config_toplevel.geometry(f"{894}x{900}")

        config_toplevel.after(250, lambda: config_toplevel.iconbitmap(os.path.join("assets", "icons", "logo.ico")))

        terminal_button = ctk.CTkButton(config_toplevel, text="Open Terminal", command=self.open_terminal)
        terminal_button.grid(row=0, column=0, pady=(20, 10), padx=20)

        example_scrollable_frame = ctk.CTkScrollableFrame(config_toplevel, width=832, height=812)
        example_scrollable_frame.grid(row=1, padx=20, pady=(10, 20))

        user_codebox = ctkcb.CTkCodeBox(example_scrollable_frame, language="python", width=800, height=350)
        user_codebox.grid(row=0, column=0, pady=(20, 10), padx=20)

        add_user_code = """# Example Code To Add A New User
        
    import sqlite3
    import os
    import hashlib
        
    conn = sqlite3.connect(os.path.join("path", "to", "database.db"))
    cursor = conn.cursor()
        
    users = [
        ('username', 'password', 'role'),
        ('username', 'password', 'role')
    ]
        
    for username, password, role in users:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexadigest()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                    (username, hashed_password, role))
        
    conn.commit()
    conn.close()
        
        """

        user_codebox.insert("0.0", add_user_code)

        database_codebox = ctkcb.CTkCodeBox(example_scrollable_frame, language="python", width=800, height=1260)
        database_codebox.grid(row=1, column=0, pady=10, padx=20)

        initialise_database__code = """# Example Code To Initialise A New Database

import sqlite3
import os

def init_db(database_path):
	conn = sqlite3.connect(database_path)
	cursor = conn.cursor()

	cursor.execute('''CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY,
		username TEXT UNIQUE,
		password TEXT,
		role TEXT,
		theme_path TEXT)''')
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
		date TEXT,
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
	
init_db(os.path.join("path", "to", "database.db")


        """

        database_codebox.insert("0.0", initialise_database__code)

        path_codebox = ctkcb.CTkCodeBox(example_scrollable_frame, language="python", width=800, height=250)
        path_codebox.grid(row=2, column=0, pady=(10, 20), padx=20)

        change_database__code = """# Example Code To Change Database Path
import os

path_to_file = os.path.join("path", "to", "database.py")
line_to_edit = 5
new_content = ''    database_path = os.path.join("path", "to", "new", "database.db")

with open(path_to_file, 'r') as file:
	lines = file.readlines()

if 0 <= line_to_edit < len(lines):
	lines[line_to_edit] = new_content

with open(path_to_file, 'w') as file:
	file.writelines(lines)
                """

        path_codebox.insert("0.0", change_database__code)


    def feedback(self):

        def submit():
            email = "CollegeEventScoreSystem@austinatts.co.uk"
            subject = subject_textbox.get("1.0", "end-1c")
            feedback = feedback_textbox.get("1.0", "end-1c")

            subject_encoded = urllib.parse.quote(subject)
            feedback_encoded = urllib.parse.quote(feedback)

            mailto_link = f"mailto:{email}?subject={subject_encoded}&body={feedback_encoded}"

            if subject != "" and feedback != "":
                webbrowser.open(mailto_link)
                feedback_toplevel.destroy()
            else:
                ctkm.CTkMessagebox(title="Error", message="Something went wrong!!!", icon="cancel")

        feedback_toplevel = ctk.CTkToplevel()
        feedback_toplevel.title("Feedback Form")
        feedback_toplevel.geometry(f"{350}x{312}")

        feedback_toplevel.after(250, lambda: feedback_toplevel.iconbitmap(os.path.join("assets", "icons", "logo.ico")))

        title_label = ctk.CTkLabel(feedback_toplevel, text="Feedback Form", font=ctk.CTkFont(size=20, weight="bold"))
        subject_label = ctk.CTkLabel(feedback_toplevel, text="Subject", anchor="w")
        feedback_label = ctk.CTkLabel(feedback_toplevel, text="Feedback", anchor="w")

        title_label.grid(row=0, column=0, padx=60, pady=(20, 0))
        subject_label.grid(row=1, column=0, padx=60, pady=(10, 0))
        feedback_label.grid(row=3, column=0, padx=60, pady=(10, 0))

        subject_textbox = ctk.CTkTextbox(feedback_toplevel, width=230, height=50)
        feedback_textbox = ctk.CTkTextbox(feedback_toplevel, width=230, height=50)

        subject_textbox.grid(row=2, column=0, padx=60, pady=10, sticky="nsew")
        feedback_textbox.grid(row=4, column=0, padx=60, pady=10, sticky="nsew")

        submit_button = ctk.CTkButton(feedback_toplevel, text="Submit", command=submit)

        submit_button.grid(row=5, column=0, padx=60, pady=(0, 20))

