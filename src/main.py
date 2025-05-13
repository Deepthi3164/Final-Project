import argparse
from user import authenticate_user
from hospital import HospitalSystem
from plots import display_statistics
import sys

def main():
    parser = argparse.ArgumentParser(description="Hospital Management System")
    parser.add_argument("-username", required=True, help="Username")
    parser.add_argument("-password", required=True, help="Password")
    args = parser.parse_args()

    user = authenticate_user(args.username, args.password)

    if not user:
        print("Access denied. Invalid credentials.")
        sys.exit()

    print(f"Welcome, {user.username}! Your role is: {user.role}")

    hospital = HospitalSystem("PA3_data.csv", "PA3_Notes.csv")

    if user.role == "management":
        display_statistics("PA3_data.csv")
    elif user.role == "admin":
        date = input("Enter date to count visits (YYYY-MM-DD): ")
        hospital.review_visits(date)
    elif user.role in ["nurse", "clinician"]:
        while True:
            print("\nAvailable actions: add_patient, remove_patient, retrieve_patient, count_visits, view_note, Stop")
            action = input("Enter action: ").strip().lower()

            if action == "add_patient":
                patient_id = input("Enter Patient ID: ")
                hospital.add_patient_visit(patient_id)
            elif action == "remove_patient":
                patient_id = input("Enter Patient ID to remove: ")
                hospital.remove_patient(patient_id)
            elif action == "retrieve_patient":
                patient_id = input("Enter Patient ID to retrieve: ")
                hospital.retrieve_patient(patient_id)
            elif action == "count_visits":
                date = input("Enter date (YYYY-MM-DD): ")
                hospital.review_visits(date)
            elif action == "view_note":
                date = input("Enter date (YYYY-MM-DD): ")
                hospital.view_note(date)
            elif action == "stop":
                print("Goodbye.")
                break
            else:
                print("Invalid action. Try again.")
    else:
        print("Role not recognized or not authorized for any actions.")

if __name__ == "__main__":
    main()
