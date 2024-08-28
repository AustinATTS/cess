import customtkinter as ctk
import CTkListbox as ctkl
import CTkMessagebox as ctkm
from utils.database import get_db
import time
from utils.logging import logger

class Events:
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

        self.title_label = ctk.CTkLabel(self.title_frame, text="Events", width=682)
        self.id_label = ctk.CTkLabel(self.entry_frame, text="ID", width=120)
        self.name_label = ctk.CTkLabel(self.entry_frame, text="Name", width=120)
        self.type_label = ctk.CTkLabel(self.entry_frame, text="Type", width=120)
        self.date_label = ctk.CTkLabel(self.entry_frame, text="Date", width=120)
        self.location_label = ctk.CTkLabel(self.entry_frame, text="Location", width=120)

        self.title_label.grid_propagate(False)
        self.id_label.grid_propagate(False)
        self.name_label.grid_propagate(False)
        self.type_label.grid_propagate(False)
        self.date_label.grid_propagate(False)
        self.location_label.grid_propagate(False)

        self.title_label.grid(row=0, column=0, padx=20, pady=10)
        self.id_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        self.name_label.grid(row=0, column=1, padx=10, pady=10)
        self.type_label.grid(row=0, column=2, padx=10, pady=10)
        self.date_label.grid(row=0, column=3, padx=10, pady=10)
        self.location_label.grid(row=0, column=4, padx=(10, 20), pady=10)

        self.id_entry = ctk.CTkEntry(self.entry_frame, width=120, placeholder_text="Leave for New", )
        self.name_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.type_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.date_entry = ctk.CTkEntry(self.entry_frame, width=120)
        self.location_entry = ctk.CTkEntry(self.entry_frame, width=120)

        self.id_entry.grid_propagate(False)
        self.name_entry.grid_propagate(False)
        self.type_entry.grid_propagate(False)
        self.date_entry.grid_propagate(False)
        self.location_entry.grid_propagate(False)

        self.id_entry.grid(row=1, column=0, padx=(20, 10), pady=10)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)
        self.type_entry.grid(row=1, column=2, padx=10, pady=10)
        self.date_entry.grid(row=1, column=3, padx=10, pady=10)
        self.location_entry.grid(row=1, column=4, padx=(10, 20), pady=10)

        self.add_update_button = ctk.CTkButton(self.button_frame, text="Add/Update",
                                               command=self.add_or_update_event, width=331)
        self.delete_button = ctk.CTkButton(self.button_frame, text="Delete", command=self.delete_selected_event,
                                           width=331)

        self.add_update_button.grid(row=0, column=0, padx=(20, 10), pady=20)
        self.delete_button.grid(row=0, column=1, padx=(10, 20), pady=20)

        self.event_listbox = ctkl.CTkListbox(self.listbox_frame, width=654, height=300)
        self.event_listbox.bind('<<ListboxSelect>>', self.update_entry_fields)

        self.event_listbox.grid(row=4, column=0, padx=20, pady=10)

        self.refresh_listbox()

        user_id = self.app.app.login.user_id
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        role = str(cursor.fetchone())
        conn.close()

        if role == "('Viewer',)":
            self.id_entry.configure(state="disabled")
            self.name_entry.configure(state="disabled")
            self.type_entry.configure(state="disabled")
            self.date_entry.configure(state="disabled")
            self.location_entry.configure(state="disabled")
            self.add_update_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

    def get_events(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_event(self, name, type, date, location):
        if name == "" or type == "" or date == "" or location == "":
            ctkm.CTkMessagebox(title="Error", message="Cannot add event. Ensure there is a name, type, date and location0 assigned", icon="cancel")
            logger.warning(f"Event could not be added, insufficient data")
            return

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (name, type, date, location) VALUES (?, ?, ?, ?)",
                       (name, type, date, location))
        conn.commit()
        conn.close()
        logger.info(f"event {name} has been added")

    def update_event(self, event_id, name, type, date, location):
        if name == "" or type == "" or date == "" or location == "":
            ctkm.CTkMessagebox(title="Error", message="Cannot update event. Ensure there is a name, type, date and location assigned", icon="cancel")
            logger.warning(f"Event could not be updated, insufficient data")
            return

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET name=?, type=?, date=?, location=? WHERE id=?",
                       (name, type, date, location, event_id))
        conn.commit()
        conn.close()
        logger.info(f"event {name} has been updated")

    def delete_event(self, event_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
        conn.commit()
        conn.close()
        logger.info(f"event {event_id} has been deleted")

    def update_entry_fields(self, event):
        selected_item = self.event_listbox.get(self.event_listbox.curselection())
        event_id, name, type, date, location = selected_item.split(" | ")

        self.clear_entry_fields()

        self.id_entry.insert(0, event_id)
        self.name_entry.insert(0, name)
        self.type_entry.insert(0, type)
        self.date_entry.insert(0, date)
        self.location_entry.insert(0, location)

    def refresh_listbox(self):
        self.event_listbox.delete(0, ctk.END)
        for row in self.get_events():
            self.event_listbox.insert(ctk.END, " | ".join(map(str, row)))

    def clear_entry_fields(self):
        self.id_entry.delete(0, ctk.END)
        self.name_entry.delete(0, ctk.END)
        self.type_entry.delete(0, ctk.END)
        self.date_entry.delete(0, ctk.END)
        self.location_entry.delete(0, ctk.END)

    def debounce(self):
        current_time = time.time()
        if current_time - self.last_button_press_time < self.button_press_interval:
            return False
        self.last_button_press_time = current_time
        return True

    def add_or_update_event(self):
        if not self.debounce():
            return
        event_id = self.id_entry.get()
        name = self.name_entry.get()
        type = self.type_entry.get()
        date = self.date_entry.get()
        location = self.location_entry.get()

        if event_id:
            self.update_event(event_id, name, type, date, location)
        else:
            self.add_event(name, type, date, location)

        self.refresh_listbox()
        self.clear_entry_fields()

    def delete_selected_event(self):
        if not self.debounce():
            return
        event_id = self.id_entry.get()
        if event_id:
            self.delete_event(event_id)
            self.refresh_listbox()
            self.clear_entry_fields()
