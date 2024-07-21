import customtkinter as ctk


class Scores:
    def __init__(self, app):
        self.app = app

    def load_page(self, frame):
        self.title_label = ctk.CTkLabel(frame, text="Scores")

        self.title_label.grid(row=0, column=0, padx=20, pady=10)