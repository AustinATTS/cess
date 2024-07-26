import customtkinter as ctk
import CTkMenuBar as ctkmb
import CTkMessagebox as ctkm
from PIL import Image
import os
import webbrowser
import urllib.parse
from gui.events import Events
from gui.participants import Participants
from gui.rankings import Rankings
from gui.reports import Reports
from gui.scores import Scores


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

        self.logo = ctk.CTkImage(Image.open(os.path.join("assets", "icons", "logo.jpg")), size=(100, 100))

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

