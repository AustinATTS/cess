import customtkinter as ctk
import CTkMenuBar as ctkmb
import CTkMessagebox as ctkm
from PIL import Image
import os
import webbrowser
import urllib.parse
from utils.file import save, restore_latest, restore_custom
from utils.edit import add_record, update_record, delete_record
from utils.settings import logout, colour_scheme, scale
from utils.about import website, github, description


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("College Event Score System")
        self.geometry(f"{1000}x{580}")
        self.bind("<1>", lambda event: event.widget.focus_set())

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.title_menu = ctkmb.CTkTitleMenu(self)

        self.file_button = self.title_menu.add_cascade("File", fg_color="transparent")
        self.edit_button = self.title_menu.add_cascade("Edit", fg_color="transparent")
        self.settings_button = self.title_menu.add_cascade("Settings", fg_color="transparent")
        self.about_button = self.title_menu.add_cascade("About", fg_color="transparent")

        self.file_dropdown = ctkmb.CustomDropdownMenu(widget=self.file_button)
        self.file_dropdown.add_option(option="Save", command=save)

        self.file_sub_menu = self.file_dropdown.add_submenu("Open")
        self.file_sub_menu.add_option(option="Restore Latest", command=restore_latest)
        self.file_sub_menu.add_option(option="Restore Custom", command=restore_custom)

        self.edit_dropdown = ctkmb.CustomDropdownMenu(widget=self.edit_button)
        self.edit_dropdown.add_option(option="Add Record", command=add_record)
        self.edit_dropdown.add_option(option="Update Record", command=update_record)
        self.edit_dropdown.add_option(option="Delete Record", command=delete_record)

        self.settings_dropdown = ctkmb.CustomDropdownMenu(widget=self.settings_button)
        self.settings_dropdown.add_option(option="Logout", command=logout)
        self.settings_dropdown.add_option(option="Colour Scheme", command=colour_scheme)
        self.settings_dropdown.add_option(option="Scale", command=scale)

        self.about_dropdown = ctkmb.CustomDropdownMenu(widget=self.about_button)
        self.about_dropdown.add_option(option="Website", command=website)
        self.about_dropdown.add_option(option="GitHub", command=github)
        self.about_dropdown.add_option(option="Description", command=description)

        self.navigation_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.logo = ctk.CTkImage(Image.open(os.path.join("..", "assets", "icons", "logo.jpg")), size=(100, 100))

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

        self.participants_button = ctk.CTkButton(self.navigation_frame, text="Participants", command=self.participants)
        self.events_button = ctk.CTkButton(self.navigation_frame, text="Events", command=self.events)
        self.scores_button = ctk.CTkButton(self.navigation_frame, text="Scores", command=self.scores)
        self.rankings_button = ctk.CTkButton(self.navigation_frame, text="Rankings", command=self.rankings)
        self.reports_button = ctk.CTkButton(self.navigation_frame, text="Reports", command=self.reports)

        self.participants_button.grid(row=2, column=0, padx=20, pady=10)
        self.events_button.grid(row=3, column=0, padx=20, pady=10)
        self.scores_button.grid(row=4, column=0, padx=20, pady=10)
        self.rankings_button.grid(row=5, column=0, padx=20, pady=10)
        self.reports_button.grid(row=6, column=0, padx=20, pady=10)

        self.feedback_label.bind("<Button-1>", lambda event: self.feedback())
        self.feedback_label.bind("<Enter>", lambda event: self.feedback_label.configure(font=("", 13, "underline"), cursor="hand2"))
        self.feedback_label.bind("<Leave>", lambda event: self.feedback_label.configure(font=("", 13), cursor="arrow"))

    def appearance(self, appearance: str):
        pass

    def participants(self):
        pass

    def events(self):
        pass

    def scores(self):
        pass

    def rankings(self):
        pass

    def reports(self):
        pass

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
