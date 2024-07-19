import customtkinter as ctk
import CTkMenuBar as ctkmb


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("College Event Score System")
        self.geometry("800x600")

        self.title_menu = ctkmb.CTkTitleMenu(self)

        file_button = self.title_menu.add_cascade("File", fg_color="transparent")
        edit_button = self.title_menu.add_cascade("Edit", fg_color="transparent")
        settings_button = self.title_menu.add_cascade("Settings", fg_color="transparent")
        about_button = self.title_menu.add_cascade("About", fg_color="transparent")

        file_dropdown = ctkmb.CustomDropdownMenu(widget=file_button)
        file_dropdown.add_option(option="Save", command=lambda: print("Save, add create backup"))

        file_sub_menu = file_dropdown.add_submenu("Open")
        file_sub_menu.add_option(option="Restore Latest", command=lambda: print("Open Latest, add restore latest"))
        file_sub_menu.add_option(option="Restore Custom", command=lambda: print("Open Custom, add restore custom"))

        edit_dropdown = ctkmb.CustomDropdownMenu(widget=edit_button)
        edit_dropdown.add_option(option="Add Record", command=lambda: print("Add"))
        edit_dropdown.add_option(option="Update Record", command=lambda: print("Update"))
        edit_dropdown.add_option(option="Delete Record", command=lambda: print("Delete"))

        settings_dropdown = ctkmb.CustomDropdownMenu(widget=settings_button)
        settings_dropdown.add_option(option="Logout", command=lambda: print("Logout"))
        settings_dropdown.add_option(option="Colour Scheme", command=lambda: print("Colour Scheme"))
        settings_dropdown.add_option(option="Scale", command=lambda: print("Scale"))

        about_dropdown = ctkmb.CustomDropdownMenu(widget=about_button)
        about_dropdown.add_option(option="Website", command=lambda: print("Website"))
        about_dropdown.add_option(option="GitHub", command=lambda: print("GitHub"))
        about_dropdown.add_option(option="Description", command=lambda: print("Description"))

if __name__ == "__main__":
    app = App()
    app.mainloop()