import customtkinter as ctk
import CTkMenuBar as ctkmb
from gui.login import Login
import CTkMessagebox as ctkm
from utils.file import save, restore_latest, restore_custom
from utils.settings import colour_scheme, scale, logout
from utils.about import website, github, description
from utils.database import get_db


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.original_width = 350
        self.original_height = 312

        self.title("College Event Score System")
        self.geometry(f"{self.original_width}x{self.original_height}")
        self.iconbitmap("assets/icons/logo.ico")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.title_menu = ctkmb.CTkTitleMenu(self)

        self.file_button = self.title_menu.add_cascade("File", fg_color="transparent", hover_color="#CCCCCC")
        self.settings_button = self.title_menu.add_cascade("Settings", fg_color="transparent", hover_color="#CCCCCC")
        self.about_button = self.title_menu.add_cascade("About", fg_color="transparent", hover_color="#CCCCCC")

        self.file_dropdown = ctkmb.CustomDropdownMenu(widget=self.file_button)
        self.file_dropdown.add_option(option="Save", command=save)

        self.file_sub_menu = self.file_dropdown.add_submenu("Open")
        self.file_sub_menu.add_option(option="Restore Latest", command=restore_latest)
        self.file_sub_menu.add_option(option="Restore Custom", command=restore_custom)

        self.settings_dropdown = ctkmb.CustomDropdownMenu(widget=self.settings_button)
        self.settings_dropdown.add_option(option="Colour Scheme", command=lambda: colour_scheme(self))
        self.settings_dropdown.add_option(option="Scale", command=scale)
        self.settings_dropdown.add_option(option="Logout", command=lambda: logout(self))

        self.about_dropdown = ctkmb.CustomDropdownMenu(widget=self.about_button)
        self.about_dropdown.add_option(option="Website", command=website)
        self.about_dropdown.add_option(option="GitHub", command=github)
        self.about_dropdown.add_option(option="Description", command=description)

        self.login = Login(self)
        self.main = None  # Will hold the instance of the Main class

        self.login.load_page(self)

    def set_main(self, main_instance):
        self.main = main_instance

    def perform_logout(self):
        if self.main:
            self.main.clear_page()
        self.geometry(f"{self.original_width}x{self.original_height}")
        self.login.load_page(self)

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        ctkm.CTkMessagebox(title="Error", message=f"There is an error\n{e}", icon="cancel")
