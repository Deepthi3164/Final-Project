# patient.py
from datetime import datetime


class Visit:
    def __init__(self, visit_id, visit_time, visit_department, chief_complaint, note_id, note_type):
        self.visit_id = visit_id
        self.visit_time = datetime.strptime(visit_time.strip(), "%m/%d/%Y").date()

        self.visit_department = visit_department
        self.chief_complaint = chief_complaint
        self.note_id = note_id
        self.note_type = note_type

class Patient:
    def __init__(self, patient_id, gender, race, age, ethnicity, insurance, zip_code):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)
