import customtkinter as ctk
import CTkListbox as ctkl
import CTkMessagebox as ctkm
from utils.database import get_db
import time


class Scores:
    def __init__(self, app):
        self.app = app
        self.last_button_press_time = 0
        self.button_press_interval = 2.0

    def load_page(self, frame):
        self.title_frame = ctk.CTkFrame(frame, width=722, height=48)
        self.entry_frame = ctk.CTkFrame(frame, width=722, height=96)
        self.button_frame = ctk.CTkFrame(frame, width=722, height=68)
        self.listbox_frame = ctk.CTkFrame(frame, width=722, height=348)

        self.title_frame.grid_propagate(False)
        self.entry_frame.grid_propagate(False)
        self.button_frame.grid_propagate(False)
        self.listbox_frame.grid_propagate(False)

        self.title_frame.grid(row=0, column=0, padx=20, pady=0)
        self.entry_frame.grid(row=1, column=0, padx=20, pady=0)
        self.button_frame.grid(row=2, column=0, padx=20, pady=0)
        self.listbox_frame.grid(row=3, column=0, padx=20, pady=0)

        self.title_label = ctk.CTkLabel(self.title_frame, text="Scores", width=682)
        self.id_label = ctk.CTkLabel(self.entry_frame, text="ID", width=120)
        self.participant_label = ctk.CTkLabel(self.entry_frame, text="Participant", width=120)
        self.event_label = ctk.CTkLabel(self.entry_frame, text="Event", width=120)
        self.score_label = ctk.CTkLabel(self.entry_frame, text="Score", width=120)
        self.date_label = ctk.CTkLabel(self.entry_frame, text="Date", width=120)

        self.title_label.grid_propagate(False)
        self.id_label.grid_propagate(False)
        self.participant_label.grid_propagate(False)
        self.event_label.grid_propagate(False)
        self.score_label.grid_propagate(False)
        self.date_label.grid_propagate(False)

        self.title_label.grid(row=0, column=0, padx=20, pady=10)
        self.id_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        self.participant_label.grid(row=0, column=1, padx=10, pady=10)
        self.event_label.grid(row=0, column=2, padx=10, pady=10)
        self.score_label.grid(row=0, column=3, padx=10, pady=10)
        self.date_label.grid(row=0, column=4, padx=(10, 20), pady=10)

        self.id_entry = ctk.CTkEntry(self.entry_frame, width=120, placeholder_text="Leave for New")
        self.participant_combo = ctk.CTkComboBox(self.entry_frame, width=120)
        self.event_combo = ctk.CTkComboBox(self.entry_frame, width=120)
        self.score_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.date_entry = ctk.CTkEntry(self.entry_frame, width=120)

        self.id_entry.grid_propagate(False)
        self.participant_combo.grid_propagate(False)
        self.event_combo.grid_propagate(False)
        self.score_entry.grid_propagate(False)
        self.date_entry.grid_propagate(False)

        self.id_entry.grid(row=1, column=0, padx=(20, 10), pady=10)
        self.participant_combo.grid(row=1, column=1, padx=10, pady=10)
        self.event_combo.grid(row=1, column=2, padx=10, pady=10)
        self.score_entry.grid(row=1, column=3, padx=10, pady=10)
        self.date_entry.grid(row=1, column=4, padx=(10, 20), pady=10)

        self.add_update_button = ctk.CTkButton(self.button_frame, text="Add/Update", command=self.add_or_update_score,
                                               width=331)
        self.delete_button = ctk.CTkButton(self.button_frame, text="Delete", command=self.delete_selected_score,
                                           width=331)

        self.add_update_button.grid(row=0, column=0, padx=(20, 10), pady=20)
        self.delete_button.grid(row=0, column=1, padx=(10, 20), pady=20)

        self.score_listbox = ctkl.CTkListbox(self.listbox_frame, width=654, height=300)
        self.score_listbox.bind('<<ListboxSelect>>', self.update_entry_fields)

        self.score_listbox.grid(row=4, column=0, padx=20, pady=10)

        self.refresh_listbox()
        self.populate_comboboxes()

        user_id = self.app.app.login.user_id
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        role = str(cursor.fetchone())
        conn.close()

        if role == "('Viewer',)":
            self.id_entry.configure(state="disabled")
            self.participant_combo.configure(state="disabled")
            self.event_combo.configure(state="disabled")
            self.score_entry.configure(state="disabled")
            self.date_entry.configure(state="disabled")
            self.add_update_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

    def get_scores(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scores")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_participants(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM participants")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_events(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM events")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_score(self, participant_id, event_id, score, date):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT team_id FROM participants WHERE id = ?", (participant_id,))
        team_id = cursor.fetchone()[0]

        if team_id == 1:
            cursor.execute("SELECT COUNT(*) FROM scores WHERE participant_id = ?", (participant_id,))
            event_count = cursor.fetchone()[0]
            if event_count >= 5:
                ctkm.CTkMessagebox(title="Error", message="Participant in Team 1 cannot attend more than 5 events",
                                   icon="cancel")
                conn.close()
                return

            cursor.execute("INSERT INTO scores (participant_id, event_id, score, date, team_id) VALUES (?, ?, ?, ?, ?)",
                           (participant_id, event_id, score, date, team_id))
        else:
            cursor.execute("SELECT id FROM participants WHERE team_id = ?", (team_id,))
            team_members = cursor.fetchall()
            for member in team_members:
                cursor.execute(
                    "INSERT OR IGNORE INTO scores (participant_id, event_id, score, date, team_id) VALUES (?, ?, ?, ?, ?)",
                    (member[0], event_id, score, date, team_id))

        conn.commit()
        conn.close()

    def update_score(self, score_id, participant_id, event_id, score, date):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE scores SET participant_id=?, event_id=?, score=?, date=? WHERE id=?",
                       (participant_id, event_id, score, date, score_id))
        conn.commit()
        conn.close()

    def delete_score(self, score_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scores WHERE id=?", (score_id,))
        conn.commit()
        conn.close()

    def update_entry_fields(self, event):
        selected_item = self.score_listbox.get(self.score_listbox.curselection())
        score_id, participant_id, event_id, score, date, team_id = selected_item.split(" | ")

        self.id_entry.delete(0, ctk.END)
        self.id_entry.insert(0, score_id)

        self.participant_combo.set(participant_id)
        self.event_combo.set(event_id)

        self.score_entry.delete(0, ctk.END)
        self.score_entry.insert(0, score)

        self.date_entry.delete(0, ctk.END)
        self.date_entry.insert(0, date)

    def refresh_listbox(self):
        self.score_listbox.delete(0, ctk.END)
        for row in self.get_scores():
            self.score_listbox.insert(ctk.END, " | ".join(map(str, row)))

    def clear_entry_fields(self):
        self.id_entry.delete(0, ctk.END)
        self.participant_combo.set("")
        self.event_combo.set("")
        self.score_entry.delete(0, ctk.END)
        self.date_entry.delete(0, ctk.END)

    def debounce(self):
        current_time = time.time()
        if current_time - self.last_button_press_time < self.button_press_interval:
            return False
        self.last_button_press_time = current_time
        return True

    def populate_comboboxes(self):
        participants = self.get_participants()
        self.participant_combo.configure(values=[f"{id} - {name}" for id, name in participants])

        events = self.get_events()
        self.event_combo.configure(values=[f"{id} - {name}" for id, name in events])

        self.participant_combo.set("")
        self.event_combo.set("")

    def add_or_update_score(self):
        if not self.debounce():
            return
        score_id = self.id_entry.get()
        participant = self.participant_combo.get()
        event = self.event_combo.get()
        score = self.score_entry.get()
        date = self.date_entry.get()

        participant_id = participant.split(" - ")[0]
        event_id = event.split(" - ")[0]

        if score_id:
            self.update_score(score_id, participant_id, event_id, score, date)
        else:
            self.add_score(participant_id, event_id, score, date)

        self.refresh_listbox()
        self.clear_entry_fields()

    def delete_selected_score(self):
        if not self.debounce():
            return
        score_id = self.id_entry.get()
        if score_id:
            self.delete_score(score_id)
            self.refresh_listbox()
            self.clear_entry_fields()
