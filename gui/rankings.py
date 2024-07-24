import customtkinter as ctk
import CTkListbox as ctkl
import CTkMessagebox as ctkm
from utils.database import get_db
import time


class Rankings:
    def __init__(self, app):
        self.app = app
        self.last_button_press_time = 0
        self.button_press_interval = 2.0

    def load_page(self, frame):
        self.title_frame = ctk.CTkFrame(frame, width=722, height=48)
        self.label_frame = ctk.CTkFrame(frame, width=722, height=48)
        self.button_frame = ctk.CTkFrame(frame, width=722, height=68)
        self.listbox_frame = ctk.CTkFrame(frame, width=722, height=398)

        self.title_frame.grid_propagate(False)
        self.label_frame.grid_propagate(False)
        self.button_frame.grid_propagate(False)
        self.listbox_frame.grid_propagate(False)

        self.title_frame.grid(row=0, column=0, padx=20, pady=0)
        self.label_frame.grid(row=1, column=0, padx=20, pady=0)
        self.button_frame.grid(row=2, column=0, padx=20, pady=0)
        self.listbox_frame.grid(row=3, column=0, padx=20, pady=0)

        self.title_label = ctk.CTkLabel(self.title_frame, text="Scores", width=682)
        self.rank_label = ctk.CTkLabel(self.label_frame, text="Rank", width=120)
        self.participant_label = ctk.CTkLabel(self.label_frame, text="Participant", width=120)
        self.event_label = ctk.CTkLabel(self.label_frame, text="Event", width=120)
        self.score_label = ctk.CTkLabel(self.label_frame, text="Score", width=120)
        self.date_label = ctk.CTkLabel(self.label_frame, text="Date", width=120)

        self.title_label.grid_propagate(False)
        self.rank_label.grid_propagate(False)
        self.participant_label.grid_propagate(False)
        self.event_label.grid_propagate(False)
        self.score_label.grid_propagate(False)
        self.date_label.grid_propagate(False)

        self.title_label.grid(row=0, column=0, padx=20, pady=10)
        self.rank_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        self.participant_label.grid(row=0, column=1, padx=10, pady=10)
        self.event_label.grid(row=0, column=2, padx=10, pady=10)
        self.score_label.grid(row=0, column=3, padx=10, pady=10)
        self.date_label.grid(row=0, column=4, padx=(10, 20), pady=10)

        self.calculate_rankings_button = ctk.CTkButton(self.button_frame, text="Calculate Rankings", command=self.calculate_rankings,
                                               width=331)
        self.view_rankings_button = ctk.CTkButton(self.button_frame, text="View Rankings", command=self.view_rankings,
                                           width=331)

        self.calculate_rankings_button.grid(row=0, column=0, padx=(20, 10), pady=20)
        self.view_rankings_button.grid(row=0, column=1, padx=(10, 20), pady=20)

        self.rank_listbox = ctkl.CTkListbox(self.listbox_frame, width=654, height=350)

        self.rank_listbox.grid(row=4, column=0, padx=20, pady=10)

        self.refresh_listbox()

    def get_scores(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scores")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def refresh_listbox(self):
        self.rank_listbox.delete(0, ctk.END)
        for row in self.get_scores():
            self.rank_listbox.insert(ctk.END, " | ".join(map(str, row)))

    def debounce(self):
        current_time = time.time()
        if current_time - self.last_button_press_time < self.button_press_interval:
            return False
        self.last_button_press_time = current_time
        return True

    def calculate_rankings(self):
        pass

    def view_rankings(self):
        pass