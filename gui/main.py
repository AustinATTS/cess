import customtkinter as ctk
import CTkMenuBar as ctkmb
from utils.file import save, restore_latest, restore_custom
from utils.edit import add_record, update_record, delete_record
from utils.settings import logout, colour_scheme, scale
from utils.about import website, github, description

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("College Event Score System")
        self.geometry("800x600")

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

        self.navigation_frame = ctk.CTkFrame(self)
        self.navigation_frame.pack()

        self.participants_button = ctk.CTkButton(self.navigation_frame)
        self.events_button = ctk.CTkButton(self.navigation_frame)
        self.scores_button = ctk.CTkButton(self.navigation_frame)
        self.rankings_button = ctk.CTkButton(self.navigation_frame)
        self.reports_button = ctk.CTkButton(self.navigation_frame)

        self.participants_button.pack()
        self.events_button.pack()
        self.scores_button.pack()
        self.rankings_button.pack()
        self.reports_button.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()