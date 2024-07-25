from gui.login import Login
import customtkinter as ctk
from utils.ThemeMaker import ThemeMaker


def colour_scheme(app):
    theme_maker = ThemeMaker()
    theme_maker.mainloop()


def scale():
    scale_input_dialog = ctk.CTkInputDialog(text="Enter a value between 50% and 200%:", title="Scale")
    scale = scale_input_dialog.get_input()
    scale_float = float(scale) / 100
    ctk.set_widget_scaling(scale_float)
    ctk.set_window_scaling(scale_float)


def logout(app):
    app.perform_logout()
