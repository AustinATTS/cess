import customtkinter as ctk
import CTkMessagebox as ctkm
from gui.main import Main
import hashlib
from utils.database import get_db
import os

class Login:
    def __init__(self, app):
        self.app = app
        self.main = None

    def load_page(self, frame):

        def authenticate():
            username = self.username_entry.get()
            password = self.password_entry.get()
            self.authenticate(frame, username, password)

        self.title_label = ctk.CTkLabel(frame, text="Login", font=ctk.CTkFont(size=20, weight="bold"))
        self.username_label = ctk.CTkLabel(frame, text="Username", anchor="w")
        self.password_label = ctk.CTkLabel(frame, text="Password", anchor="w")

        self.username_entry = ctk.CTkEntry(frame, width=230, height=50)
        self.password_entry = ctk.CTkEntry(frame, width=230, height=50, show='*')

        self.submit_button = ctk.CTkButton(frame, text="Submit", command=authenticate)

        self.username_entry.grid(row=2, column=0, padx=60, pady=10, sticky="nsew")
        self.password_entry.grid(row=4, column=0, padx=60, pady=10, sticky="nsew")

        self.submit_button.grid(row=5, column=0, padx=60, pady=(0, 20))

        self.title_label.grid(row=0, column=0, padx=60, pady=(20, 10))
        self.username_label.grid(row=1, column=0, padx=60, pady=(10, 0))
        self.password_label.grid(row=3, column=0, padx=60, pady=(10, 0))

    def authenticate(self, frame, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, password_hash))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.user_id = user[0]
            global user_id
            user_id = self.user_id
            self.submit(frame)
        else:
            ctkm.CTkMessagebox(title="Error", message="Invalid username or password", icon="cancel")

    def apply_user_theme(self, user_id):
        """ Apply the theme based on the user's theme_path """
        self.main = Main(self)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT theme_path FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result[0] and os.path.exists(result[0]):
            theme_path = result[0]
        else:
            theme_path = 'themes/default.json'

        try:
            self.main.set_theme(theme_path)
        except Exception as e:
            self.main.set_theme("blue")

    def submit(self, frame):
        self.apply_user_theme(user_id)
        self.clear_page()
        self.app.geometry(f"{1000}x{580}")
        self.main = Main(self.app)
        self.app.set_main(self.main)
        self.main.load_page(frame)

    def clear_page(self):
        self.title_label.destroy()
        self.username_label.destroy()
        self.password_label.destroy()
        self.username_entry.destroy()
        self.password_entry.destroy()
        self.submit_button.destroy()

    def get_id(self):
        id = user_id
        return id

