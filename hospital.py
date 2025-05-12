# hospital.py
import pandas as pd
import csv
import os
import random
from datetime import datetime
from patient import Patient, Visit
from notes import NoteManager

class HospitalSystem:
    def __init__(self, data_file, notes_file):
        self.data_file = data_file
        self.notes = NoteManager(notes_file)
        self.patients = self.load_data()

    def create_patient(self, pid, gender, race, age, ethnicity, insurance, zip_code):
        return Patient(pid, gender, race, age, ethnicity, insurance, zip_code)

    def create_visit(self, visit_id, visit_time_str, department, complaint, note_id, note_type):
        return Visit(visit_id, visit_time_str, department, complaint, note_id, note_type)

    def load_data(self):
        patients = {}
        if os.path.exists(self.data_file):
            df = pd.read_csv(self.data_file)
            df.columns = df.columns.str.strip()
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(-1).astype(int)
            for _, row in df.iterrows():
                pid = str(row['Patient_ID'])
                if pid not in patients:
                    patients[pid] = Patient(
                        pid, row['Gender'], row['Race'], row['Age'],
                        row['Ethnicity'], row['Insurance'], row['Zip_code']
                    )
                visit = Visit(
                    row['Visit_ID'], row['Visit_time'], row['Visit_department'],
                    row['Chief_complaint'], row['Note_ID'], row['Note_type']
                )
                patients[pid].add_visit(visit)
        return patients

    def add_patient_visit(self, pid):
        if pid not in self.patients:
            print(f"Adding new patient {pid}...")
            gender = input("Gender: ")
            race = input("Race: ")
            age = int(input("Age: "))
            ethnicity = input("Ethnicity: ")
            insurance = input("Insurance: ")
            zip_code = input("Zip Code: ")
            self.patients[pid] = Patient(pid, gender, race, age, ethnicity, insurance, zip_code)
        else:
            print(f"Adding visit for existing patient {pid}...")

        visit_id = str(random.randint(100000, 999999))
        visit_time_str = input("Visit Time (MM/DD/YYYY): ")
        visit_time = datetime.strptime(visit_time_str, "%m/%d/%Y").date()
        department = input("Department: ")
        complaint = input("Chief Complaint: ")
        note_id = str(random.randint(100000, 999999))
        note_type = input("Note Type: ")

        visit = Visit(visit_id, visit_time_str, department, complaint, note_id, note_type)
        self.patients[pid].add_visit(visit)

        with open(self.data_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                pid, visit_id, visit_time_str, department,
                gender, race, age, ethnicity, insurance, zip_code,
                complaint, note_id, note_type
            ])
        print("Visit added.")

    def retrieve_patient(self, pid):
        pid = str(pid)
        if pid in self.patients:
            patient = self.patients[pid]
            print(f"\nPatient ID: {pid}\nGender: {patient.gender}\nRace: {patient.race}\nAge: {patient.age}\nEthnicity: {patient.ethnicity}\nInsurance: {patient.insurance}\nZip Code: {patient.zip_code}")
            for visit in patient.visits:
                print(f"Visit on {visit.visit_time} | Dept: {visit.visit_department} | Complaint: {visit.chief_complaint} | Note: {visit.note_id} ({visit.note_type})")
        else:
            print("Patient not found.")

    def remove_patient(self, pid):
        pid = str(pid)
        if pid in self.patients:
            del self.patients[pid]
            df = pd.read_csv(self.data_file)
            df = df[df['Patient_ID'].astype(str) != pid]
            df.to_csv(self.data_file, index=False)
            print("Patient removed.")
        else:
            print("Patient not found.")

    def review_visits(self, date_str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        count = 0
        for patient in self.patients.values():
            for visit in patient.visits:
                if visit.visit_time == target_date:
                    count += 1
        print(f"Total visits on {date_str}: {count}")

    def view_note(self, date_str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        print(f"Notes on {date_str}:")
        for patient in self.patients.values():
            for visit in patient.visits:
                if visit.visit_time == target_date:
                    text = self.notes.get_note_text(visit.note_id)
                    print(f"Patient {patient.patient_id}: Note {visit.note_id} - {visit.note_type}\n{text}\n")
