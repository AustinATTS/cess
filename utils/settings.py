from gui.login import Login
import customtkinter as ctk
from utils.ThemeMaker import ThemeMaker

def colour_scheme(app):
    theme_maker = ThemeMaker()
    theme_maker.mainloop()


def scale():
    pass

def logout(app):
    app.perform_logout()
