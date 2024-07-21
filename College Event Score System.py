import customtkinter as ctk
import CTkMenuBar as ctkmb
from gui.login import Login
from utils.file import save, restore_latest, restore_custom
from utils.edit import add_record, update_record, delete_record
from utils.settings import colour_scheme, scale, logout
from utils.about import website, github, description


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("College Event Score System")
        self.geometry(f"{350}x{312}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.title_menu = ctkmb.CTkTitleMenu(self)

        self.file_button = self.title_menu.add_cascade("File", fg_color="transparent", hover_color="#CCCCCC")
        self.edit_button = self.title_menu.add_cascade("Edit", fg_color="transparent", hover_color="#CCCCCC")
        self.settings_button = self.title_menu.add_cascade("Settings", fg_color="transparent", hover_color="#CCCCCC")
        self.about_button = self.title_menu.add_cascade("About", fg_color="transparent", hover_color="#CCCCCC")

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
        self.settings_dropdown.add_option(option="Colour Scheme", command=colour_scheme)
        self.settings_dropdown.add_option(option="Scale", command=scale)
        self.settings_dropdown.add_option(option="Logout", command=logout)

        self.about_dropdown = ctkmb.CustomDropdownMenu(widget=self.about_button)
        self.about_dropdown.add_option(option="Website", command=website)
        self.about_dropdown.add_option(option="GitHub", command=github)
        self.about_dropdown.add_option(option="Description", command=description)

        self.login = Login(self)

        self.login.load_page(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()