import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from user import authenticate_user
from hospital import HospitalSystem
from datetime import datetime
import csv
import os
import random

class HospitalUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("700x500")
        self.root.configure(bg="#e8f0fe")
        self.hospital = HospitalSystem("Patient_data.csv", "Notes.csv")
        self.user = None
        self.login_time = None
        self.log_file = "usage_log.csv"
        self.init_login_screen()

    def style_button(self, btn):
        btn.configure(bg="#007acc", fg="white", font=("Arial", 12, "bold"), relief="raised", padx=10, pady=6, bd=0, activebackground="#005f99")

    def style_label(self, lbl):
        lbl.configure(bg="#e8f0fe", fg="#333", font=("Arial", 12))

    def style_entry(self, entry):
        entry.configure(font=("Arial", 12), relief="groove", bd=2, bg="white")

    def init_login_screen(self):
        self.clear_screen()

        title = tk.Label(self.root, text="🏥 Hospital Management System", bg="#e8f0fe", fg="#2c3e50", font=("Arial", 20, "bold"))
        title.pack(pady=(30, 10))

        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove", padx=40, pady=30)
        frame.pack(pady=20)

        lbl1 = tk.Label(frame, text="Username")
        self.style_label(lbl1)
        lbl1.pack(pady=(0, 5))
        self.username_entry = tk.Entry(frame, width=30)
        self.style_entry(self.username_entry)
        self.username_entry.pack(pady=(0, 10))

        lbl2 = tk.Label(frame, text="Password")
        self.style_label(lbl2)
        lbl2.pack(pady=(0, 5))
        self.password_entry = tk.Entry(frame, show="*", width=30)
        self.style_entry(self.password_entry)
        self.password_entry.pack(pady=(0, 15))

        login_btn = tk.Button(frame, text="Login", command=self.handle_login)
        self.style_button(login_btn)
        login_btn.pack()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user = authenticate_user(username, password)
        self.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.user:
            self.log_action("login", success=True)
            self.show_dashboard()
        else:
            self.log_action("login", success=False)
            messagebox.showerror("Login Failed", "Invalid credentials")

    def show_dashboard(self):
        self.clear_screen()

        title = tk.Label(self.root, text="🏥 Hospital Management System", bg="#e8f0fe", fg="#2c3e50", font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        header = tk.Label(self.root, text=f"Welcome {self.user.username} ({self.user.role})", bg="#e8f0fe", font=("Arial", 14, "bold"))
        header.pack(pady=(0, 20))

        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove", padx=30, pady=30)
        frame.pack(pady=10)

        role = self.user.role
        if role in ["nurse", "clinician"]:
            actions = [
                ("Add Patient", self.add_patient),
                ("Retrieve Patient", self.retrieve_patient),
                ("Remove Patient", self.remove_patient),
                ("Count Visits", self.count_visits),
                ("View Note", self.view_note),
                ("Exit", self.root.quit)
            ]
        elif role == "admin":
            actions = [
                ("Count Visits", self.count_visits),
                ("Exit", self.root.quit)
            ]
        elif role == "management":
            actions = [
                ("Generate Statistics", self.generate_statistics),
                ("Exit", self.root.quit)
            ]
        else:
            messagebox.showerror("Role Error", "Unknown user role")
            return

        for (label, action) in actions:
            btn = tk.Button(frame, text=label, command=action, width=25)
            self.style_button(btn)
            btn.pack(pady=6)

    def add_patient(self):
        window = tk.Toplevel(self.root)
        window.title("Add Patient")
        window.geometry("600x650")
        window.configure(bg="#e8f0fe")

        form = tk.Frame(window, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        form.pack(padx=20, pady=20)

        labels = [
            "Patient_ID", "Visit_time (MM/DD/YYYY)", "Visit_department", "Race", "Gender",
            "Ethnicity", "Age", "Zip_code", "Insurance", "Chief_complaint", "Note_type"
        ]
        entries = {}

        for i, label_text in enumerate(labels):
            lbl = tk.Label(form, text=label_text, bg="#ffffff", anchor="w")
            self.style_label(lbl)
            lbl.grid(row=i, column=0, sticky="e", pady=5, padx=5)

            entry = tk.Entry(form, width=30)
            self.style_entry(entry)
            entry.grid(row=i, column=1, pady=5, padx=5)

            entries[label_text] = entry

        # Add Note_text input field
        note_text_label = tk.Label(form, text="Note_text", bg="#ffffff", anchor="w")
        self.style_label(note_text_label)
        note_text_label.grid(row=len(labels), column=0, sticky="e", pady=5, padx=5)

        note_text_entry = tk.Entry(form, width=30)
        self.style_entry(note_text_entry)
        note_text_entry.grid(row=len(labels), column=1, pady=5, padx=5)

        def submit():
            try:
                pid = entries["Patient_ID"].get()
                visit_time_str = entries["Visit_time (MM/DD/YYYY)"].get()
                department = entries["Visit_department"].get()
                race = entries["Race"].get()
                gender = entries["Gender"].get()
                ethnicity = entries["Ethnicity"].get()
                age = int(entries["Age"].get())
                zip_code = entries["Zip_code"].get()
                insurance = entries["Insurance"].get()
                complaint = entries["Chief_complaint"].get()
                note_type = entries["Note_type"].get()
                note_text = note_text_entry.get()

                if pid not in self.hospital.patients:
                    self.hospital.patients[pid] = self.hospital.create_patient(pid, gender, race, age, ethnicity, insurance, zip_code)

                visit_id = str(random.randint(100000, 999999))
                note_id = str(random.randint(100000, 999999))
                visit = self.hospital.create_visit(visit_id, visit_time_str, department, complaint, note_id, note_type)
                self.hospital.patients[pid].add_visit(visit)

                with open(self.hospital.data_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        pid, visit_id, visit_time_str, department, race, gender, ethnicity, age,
                        zip_code, insurance, complaint, note_id, note_type
                    ])

                self.write_note_to_file(pid, visit_id, note_id, note_text)

                messagebox.showinfo("Success", "Patient added successfully.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        submit_btn = tk.Button(form, text="Submit", command=submit)
        self.style_button(submit_btn)
        submit_btn.grid(row=len(labels)+1, columnspan=2, pady=20)

    def retrieve_patient(self):
        window = tk.Toplevel(self.root)
        window.title("Retrieve Patient")
        window.geometry("400x200")
        window.configure(bg="#e8f0fe")

        frame = tk.Frame(window, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        frame.pack(pady=20)

        lbl = tk.Label(frame, text="Enter Patient ID:")
        self.style_label(lbl)
        lbl.pack()
        entry = tk.Entry(frame, width=30)
        self.style_entry(entry)
        entry.pack(pady=10)

        def submit():
            pid = entry.get()
            self.log_action("retrieve_patient")
            if pid in self.hospital.patients:
                patient = self.hospital.patients[pid]
                info = f"Patient ID: {pid}\nGender: {patient.gender}\nRace: {patient.race}\nAge: {patient.age}\nEthnicity: {patient.ethnicity}\nInsurance: {patient.insurance}\nZip Code: {patient.zip_code}\n"
                for visit in patient.visits:
                    info += f"\nVisit Date: {visit.visit_time}\nDepartment: {visit.visit_department}\nComplaint: {visit.chief_complaint}\nNote ID: {visit.note_id} ({visit.note_type})\n"
                self.show_text_window("Patient Info", info)
                window.destroy()
            else:
                messagebox.showinfo("Not Found", "Patient not found.")

        btn = tk.Button(frame, text="Submit", command=submit)
        self.style_button(btn)
        btn.pack(pady=10)

    def remove_patient(self):
        window = tk.Toplevel(self.root)
        window.title("Remove Patient")
        window.geometry("400x200")
        window.configure(bg="#e8f0fe")

        frame = tk.Frame(window, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        frame.pack(pady=20)

        lbl = tk.Label(frame, text="Enter Patient ID:")
        self.style_label(lbl)
        lbl.pack()
        entry = tk.Entry(frame, width=30)
        self.style_entry(entry)
        entry.pack(pady=10)

        def submit():
            pid = entry.get()
            self.log_action("remove_patient")
            if pid in self.hospital.patients:
                self.hospital.remove_patient(pid)
                messagebox.showinfo("Success", "Patient removed.")
                window.destroy()
            else:
                messagebox.showinfo("Not Found", "Patient not found.")

        btn = tk.Button(frame, text="Remove", command=submit)
        self.style_button(btn)
        btn.pack(pady=10)

    def count_visits(self):
        window = tk.Toplevel(self.root)
        window.title("Count Visits")
        window.geometry("400x200")
        window.configure(bg="#e8f0fe")

        frame = tk.Frame(window, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        frame.pack(pady=20)

        lbl = tk.Label(frame, text="Enter Date (YYYY-MM-DD):")
        self.style_label(lbl)
        lbl.pack()
        entry = tk.Entry(frame, width=30)
        self.style_entry(entry)
        entry.pack(pady=10)

        def submit():
            date = entry.get()
            self.log_action("count_visits")
            count = 0
            for patient in self.hospital.patients.values():
                for visit in patient.visits:
                    if str(visit.visit_time) == date:
                        count += 1
            messagebox.showinfo("Visit Count", f"Total visits on {date}: {count}")
            window.destroy()

        btn = tk.Button(frame, text="Count", command=submit)
        self.style_button(btn)
        btn.pack(pady=10)

    def view_note(self):
        window = tk.Toplevel(self.root)
        window.title("View Note")
        window.geometry("400x200")
        window.configure(bg="#e8f0fe")

        frame = tk.Frame(window, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        frame.pack(pady=20)

        lbl = tk.Label(frame, text="Enter date (YYYY-MM-DD):")
        self.style_label(lbl)
        lbl.pack()
        entry = tk.Entry(frame, width=30)
        self.style_entry(entry)
        entry.pack(pady=10)

        def submit():
            date = entry.get()
            self.log_action("view_note")
            notes = ""
            for patient in self.hospital.patients.values():
                for visit in patient.visits:
                    if str(visit.visit_time) == date:
                        text = self.hospital.notes.get_note_text(visit.note_id)
                        notes += f"\nPatient {patient.patient_id}: Note {visit.note_id} - {visit.note_type}\n{text}\n"
            if notes:
                self.show_text_window("Notes", notes)
            else:
                messagebox.showinfo("No Notes", "No notes found for that date.")
            window.destroy()

        btn = tk.Button(frame, text="Submit", command=submit)
        self.style_button(btn)
        btn.pack(pady=10)

    def generate_statistics(self):
        from plots import display_statistics
        self.log_action("generate_statistics")
        display_statistics("Patient_data.csv")
        messagebox.showinfo("Statistics", "Statistics generated and saved as PNG files in the current directory.")

    def show_text_window(self, title, content):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("800x500")
        window.configure(bg="#e8f0fe")

        text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Consolas", 12), bg="white", padx=10, pady=10)
        text_area.insert(tk.END, content)
        text_area.pack(expand=True, fill='both', padx=10, pady=10)
        text_area.configure(state='disabled')

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def write_note_to_file(self, patient_id, visit_id, note_id, note_text):
        notes_path = "Notes.csv"
        file_exists = os.path.isfile(notes_path)

        with open(notes_path, "a", newline='') as notes_file:
            writer = csv.writer(notes_file)
            if not file_exists:
                writer.writerow(["Patient_ID", "Visit_ID", "Note_ID", "Note_text"])
            writer.writerow([patient_id, visit_id, note_id, note_text])



    def log_action(self, action, success=True):
        """Logs user activity with timestamp and outcome into usage_log.csv."""
        log_exists = os.path.exists(self.log_file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if not log_exists:
                writer.writerow(["username", "role", "action", "timestamp", "success"])
            status = "success" if success else "fail"
            username = self.user.username if self.user else self.username_entry.get()
            role = self.user.role if self.user else "unknown"
            writer.writerow([username, role, action, timestamp, status])

if __name__ == '__main__':
    root = tk.Tk()
    app = HospitalUI(root)
    root.mainloop()
