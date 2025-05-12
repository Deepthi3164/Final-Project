# user.py
import csv

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

def authenticate_user(username, password, credentials_file="Credentials.csv"):
    try:
        with open(credentials_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure stripping for accurate matching
                if row['username'].strip() == username and row['password'].strip() == password:
                    return User(username, row['role'].strip())
    except FileNotFoundError:
        print("Credential file not found.")
    return None
