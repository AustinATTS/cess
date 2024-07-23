import _tkinter
import sqlite3
import customtkinter as ctk
import CTkListbox as ctkl
import CTkMessagebox as ctkm
from utils.database import get_db
import time


class Participants:
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

        self.title_label = ctk.CTkLabel(self.title_frame, text="Participants", width=682)
        self.id_label = ctk.CTkLabel(self.entry_frame, text="ID", width=120)
        self.name_label = ctk.CTkLabel(self.entry_frame, text="Name", width=120)
        self.email_label = ctk.CTkLabel(self.entry_frame, text="Email", width=120)
        self.phone_label = ctk.CTkLabel(self.entry_frame, text="Phone", width=120)
        self.team_label = ctk.CTkLabel(self.entry_frame, text="Team", width=120)

        self.title_label.grid_propagate(False)
        self.id_label.grid_propagate(False)
        self.name_label.grid_propagate(False)
        self.email_label.grid_propagate(False)
        self.phone_label.grid_propagate(False)
        self.team_label.grid_propagate(False)

        self.title_label.grid(row=0, column=0, padx=20, pady=10)
        self.id_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        self.name_label.grid(row=0, column=1, padx=10, pady=10)
        self.email_label.grid(row=0, column=2, padx=10, pady=10)
        self.phone_label.grid(row=0, column=3, padx=10, pady=10)
        self.team_label.grid(row=0, column=4, padx=(10, 20), pady=10)

        self.id_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.name_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.email_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.phone_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.team_entry = ctk.CTkEntry(self.entry_frame, width=120)

        self.id_entry.grid_propagate(False)
        self.name_entry.grid_propagate(False)
        self.email_entry.grid_propagate(False)
        self.phone_entry.grid_propagate(False)
        self.team_entry.grid_propagate(False)

        self.id_entry.grid(row=1, column=0, padx=(20, 10), pady=10)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)
        self.email_entry.grid(row=1, column=2, padx=10, pady=10)
        self.phone_entry.grid(row=1, column=3, padx=10, pady=10)
        self.team_entry.grid(row=1, column=4, padx=(10, 20), pady=10)

        self.add_update_button = ctk.CTkButton(self.button_frame, text="Add/Update", command=self.add_or_update_participant, width=331)
        self.delete_button = ctk.CTkButton(self.button_frame, text="Delete", command=self.delete_selected_participant, width=331)

        self.add_update_button.grid(row=0, column=0, padx=(20, 10), pady=20)
        self.delete_button.grid(row=0, column=1, padx=(10, 20), pady=20)

        self.participant_listbox = ctkl.CTkListbox(self.listbox_frame, width=654, height=300)
        self.participant_listbox.bind('<<ListboxSelect>>', self.update_entry_fields)

        self.participant_listbox.grid(row=4, column=0, padx=20, pady=10)

        self.refresh_listbox()

    def get_participants(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participants")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_participant(self, name, email, phone, team):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO participants (name, email, phone, team_id) VALUES (?, ?, ?, ?)",
                       (name, email, phone, team))
        conn.commit()
        conn.close()

    def update_participant(self, participant_id, name, email, phone, team):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE participants SET name=?, email=?, phone=?, team_id=? WHERE id=?",
                       (name, email, phone, team, participant_id))
        conn.commit()
        conn.close()

    def delete_participant(self, participant_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM participants WHERE id=?", (participant_id,))
        conn.commit()
        conn.close()

    def update_entry_fields(self, event):
        selected_item = self.participant_listbox.get(self.participant_listbox.curselection())
        participant_id, name, email, phone, team = selected_item.split(" | ")

        self.id_entry.delete(0, ctk.END)
        self.id_entry.insert(0, participant_id)

        self.name_entry.delete(0, ctk.END)
        self.name_entry.insert(0, name)

        self.email_entry.delete(0, ctk.END)
        self.email_entry.insert(0, email)

        self.phone_entry.delete(0, ctk.END)
        self.phone_entry.insert(0, phone)

        self.team_entry.delete(0, ctk.END)
        self.team_entry.insert(0, team)

    def refresh_listbox(self):
        self.participant_listbox.delete(0, ctk.END)
        for row in self.get_participants():
            self.participant_listbox.insert(ctk.END, " | ".join(map(str, row)))

    def clear_entry_fields(self):
        self.id_entry.delete(0, ctk.END)
        self.name_entry.delete(0, ctk.END)
        self.email_entry.delete(0, ctk.END)
        self.phone_entry.delete(0, ctk.END)
        self.team_entry.delete(0, ctk.END)

    def debounce(self):
        current_time = time.time()
        if current_time - self.last_button_press_time < self.button_press_interval:
            return False
        self.last_button_press_time = current_time
        return True

    def add_or_update_participant(self):
        if not self.debounce():
            return
        participant_id = self.id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        team = self.team_entry.get()

        if participant_id:
            self.update_participant(participant_id, name, email, phone, team)
        else:
            self.add_participant(name, email, phone, team)

        self.refresh_listbox()
        self.clear_entry_fields()

    def delete_selected_participant(self):
        if not self.debounce():
            return
        participant_id = self.id_entry.get()
        if participant_id:
            self.delete_participant(participant_id)
            self.refresh_listbox()
            self.clear_entry_fields()
