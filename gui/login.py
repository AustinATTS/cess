import customtkinter as ctk
from gui.main import Main


class Login:
    def __init__(self, app):
        self.app = app

        self.main = Main(self)

    def load_page(self, frame):

        def submit():
            self.submit(frame)

        self.title_label = ctk.CTkLabel(frame, text="Login")

        self.title_label.grid(row=0, column=0, padx=20, pady=10)

        self.test_textbox = ctk.CTkTextbox(frame)
        self.test_textbox.grid(row=1, column=0)

        self.submit_button = ctk.CTkButton(frame, text="Submit", command=submit)
        self.submit_button.grid(row=2, column=0)

    def submit(self, frame):
        self.value = self.test_textbox.get("1.0", "end-1c")
        print(self.value)
        if self.value == "2":
            self.main.load_page(frame)
        else:
            print("Fuk of")
