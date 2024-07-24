import customtkinter as ctk
import CTkListbox as ctkl
import CTkMessagebox as ctkm
import assets.CTkPDFViewer as ctkpdfv
from utils.database import get_db
from fpdf import FPDF
import time
import os


class Reports:
    def __init__(self, app):
        self.app = app
        self.last_button_press_time = 0
        self.button_press_interval = 2.0
        self.reports_dir = "reports"

        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def load_page(self, frame):
        self.title_frame = ctk.CTkFrame(frame, width=722, height=48)
        self.label_frame = ctk.CTkFrame(frame, width=722, height=48)
        self.button_frame = ctk.CTkFrame(frame, width=722, height=68)
        self.listbox_frame = ctk.CTkFrame(frame, width=722, height=398)

        self.title_frame.grid_propagate(False)
        self.label_frame.grid_propagate(False)
        self.button_frame.grid_propagate(False)
        self.listbox_frame.grid_propagate(False)

        self.title_frame.grid(row=0, column=0, padx=20, pady=0)
        self.label_frame.grid(row=1, column=0, padx=20, pady=0)
        self.button_frame.grid(row=2, column=0, padx=20, pady=0)
        self.listbox_frame.grid(row=3, column=0, padx=20, pady=0)

        self.title_label = ctk.CTkLabel(self.title_frame, text="Reports", width=682)
        self.id_label = ctk.CTkLabel(self.label_frame, text="ID", width=120)
        self.name_label = ctk.CTkLabel(self.label_frame, text="Name", width=120)
        self.date_label = ctk.CTkLabel(self.label_frame, text="Date", width=120)
        self.details_label = ctk.CTkLabel(self.label_frame, text="Details", width=260)

        self.title_label.grid_propagate(False)
        self.id_label.grid_propagate(False)
        self.name_label.grid_propagate(False)
        self.date_label.grid_propagate(False)
        self.details_label.grid_propagate(False)

        self.title_label.grid(row=0, column=0, padx=20, pady=10)
        self.id_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        self.name_label.grid(row=0, column=1, padx=10, pady=10)
        self.date_label.grid(row=0, column=2, padx=10, pady=10)
        self.details_label.grid(row=0, column=3, padx=10, pady=10)

        self.generate_reports_button = ctk.CTkButton(self.button_frame, text="Generate Reports",
                                                     command=self.generate_reports,
                                                     width=331)
        self.view_report_button = ctk.CTkButton(self.button_frame, text="View Report", command=self.view_report,
                                                width=331)

        self.generate_reports_button.grid(row=0, column=0, padx=(20, 10), pady=20)
        self.view_report_button.grid(row=0, column=1, padx=(10, 20), pady=20)

        self.report_listbox = ctkl.CTkListbox(self.listbox_frame, width=654, height=350)

        self.report_listbox.grid(row=4, column=0, padx=20, pady=10)

        self.refresh_listbox()

    def get_reports(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def refresh_listbox(self):
        self.report_listbox.delete(0, ctk.END)
        for row in self.get_reports():
            self.report_listbox.insert(ctk.END, " | ".join(map(str, row)))

    def debounce(self):
        current_time = time.time()
        if current_time - self.last_button_press_time < self.button_press_interval:
            return False
        self.last_button_press_time = current_time
        return True

    def generate_reports(self):
        if not self.debounce():
            return

        def create_report(report_type):
            if report_type == "Participant Report":
                data = self.get_participant_data()
            elif report_type == "Team Report":
                data = self.get_team_data()
            elif report_type == "Score Report":
                data = self.get_score_data()
            elif report_type == "Event Directory":
                data = self.get_event_directory_data()
            else:
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=report_type, ln=True, align='C')

            for row in data:
                pdf.cell(200, 10, txt=" | ".join(map(str, row)), ln=True, align='L')

            report_filename = f"{self.reports_dir}/{report_type.replace(' ', '_')}_{int(time.time())}.pdf"
            pdf.output(report_filename)

            self.add_report_to_db(report_filename, report_type)

            self.refresh_listbox()

        report_toplevel = ctk.CTkToplevel()
        report_toplevel.geometry("300x200")
        report_toplevel.title("Generate Report")

        ctk.CTkLabel(report_toplevel, text="Select Report Type").pack(pady=20)
        ctk.CTkButton(report_toplevel, text="Participant Report", command=lambda: create_report("Participant Report")).pack(pady=5)
        ctk.CTkButton(report_toplevel, text="Team Report", command=lambda: create_report("Team Report")).pack(pady=5)
        ctk.CTkButton(report_toplevel, text="Score Report", command=lambda: create_report("Score Report")).pack(pady=5)
        ctk.CTkButton(report_toplevel, text="Event Directory", command=lambda: create_report("Event Directory")).pack(pady=5)

    def view_report(self):
        if not self.debounce():
            return

        selected_report = self.report_listbox.get(self.report_listbox.curselection())
        if not selected_report:
            ctkm.CTkMessagebox(title="Error", message="No report selected")
            return

        report_path = selected_report.split(" | ")[-1]

        if not os.path.exists(report_path):
            ctkm.CTkMessagebox(title="Error", message="Report file not found")
            return

        viewer_toplevel = ctk.CTkToplevel()
        viewer_toplevel.geometry("800x600")
        viewer_toplevel.title("View Report")

        pdf_viewer = ctkpdfv.CTkPDFViewer(viewer_toplevel, file=report_path, width=800, height=600)
        pdf_viewer.pack(expand=True, fill="both")

    def add_report_to_db(self, filename, report_type):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reports (name, date, details) VALUES (?, ?, ?)",
                       (report_type, time.strftime('%Y-%m-%d %H:%M:%S'), filename))
        conn.commit()
        conn.close()

    def get_participant_data(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participants")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_team_data(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_score_data(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scores")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_event_directory_data(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.name as event_name, e.date, p.name as participant_name
            FROM scores s
            JOIN events e ON s.event_id = e.id
            JOIN participants p ON s.participant_id = p.id
            ORDER BY e.date, e.name, p.name
        """)
        data = cursor.fetchall()
        conn.close()
        return data