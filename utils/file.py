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
    try:
        backup_files = sorted(
            [f for f in os.listdir(backup_dir) if f.startswith("backup_") and f.endswith(".db")],
            key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)),
            reverse=True
        )
        if not backup_files:
            ctkm.CTkMessagebox(title="Warning", message="No backup files found.")
            return

        latest_backup = os.path.join(backup_dir, backup_files[0])
        shutil.copyfile(latest_backup, os.path.join("data", "database.db"))
        ctkm.CTkMessagebox(title="Success", message=f"Restored from latest backup: {latest_backup}")
    except Exception as e:
        ctkm.CTkMessagebox(title="Error", message=f"Failed to restore from latest backup: {e}")


def restore_custom():
    try:
        custom_backup = tkf.askopenfilename(
            title="Select Backup File",
            initialdir=backup_dir,
            filetypes=[("Database Files", "*.db")]
        )
        if not custom_backup:
            return

        shutil.copyfile(custom_backup, os.path.join("data", "database.db"))
        ctkm.CTkMessagebox(title="Success", message=f"Restored from custom backup: {custom_backup}")
    except Exception as e:
        ctkm.CTkMessagebox(title="Error", message=f"Failed to restore from custom backup: {e}")
