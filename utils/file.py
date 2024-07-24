from utils.database import get_db
import CTkMessagebox as ctkm
import os
import tkinter.filedialog as tkf
import shutil
import time

backup_dir = "backups"

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def save():
    try:
        conn = get_db()
        conn.close()
        backup_filename = os.path.join(backup_dir, f"backup_{int(time.time())}.db")
        shutil.copyfile(os.path.join("data", "database.db"), backup_filename)
        ctkm.CTkMessagebox(title="Success", message=f"Backup saved to {backup_filename}")
    except Exception as e:
        ctkm.CTkMessagebox(title="Error", message=f"Failed to save backup: {e}")

def restore_latest():
    pass


def restore_custom():
    pass
