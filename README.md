# Hospital Management System (Final Project - HI 741)

This project is a Tkinter-based GUI application for managing a clinical data warehouse at a hospital. It allows authorized users to manage patient records, visit notes, and generate statistical insights — all through a secure, role-based interface.

---

## ✅ Features

- **User Authentication** from `PA3_credentials.csv`
- **Role-based Access** for admin, nurse, clinician, and management
- GUI-based actions:
  - Add/Retrieve/Remove Patients
  - View Clinical Notes
  - Count Visits on a Specific Date
  - Generate Key Statistics (Management/Admin only)
- **Usage Logging** to `usage_log.csv`
- **Data Persistence** via `PA3_data.csv` and `PA3_Notes.csv`

---

## 📂 File Structure

```
📁 project/
├── main.py
├── gui.py
├── hospital.py
├── patient.py
├── user.py
├── notes.py
├── plots.py
├── PA3_data.csv
├── PA3_Notes.csv
├── PA3_credentials.csv
├── usage_log.csv
├── README.md
└── requirements.txt
```

---

## 🚀 How to Run

1. **Install dependencies** (if any):

```
pip install -r requirements.txt
```

2. **Start the program**:

```
python gui.py
```

---

## 🔐 User Roles & Permissions

| Role        | Allowed Actions                                                                 |
|-------------|----------------------------------------------------------------------------------|
| `nurse` / `clinician` | Add, remove, retrieve patient, count visits, view notes |
| `admin`     | Count visits only                                                               |
| `management`| Generate statistics only                                                        |

---

## 🧪 Data Files

- **`PA3_data.csv`**: Contains patient and visit info.
- **`PA3_Notes.csv`**: Stores notes with columns: `Patient_ID`, `Visit_ID`, `Note_ID`, `Note_text`
- **`PA3_credentials.csv`**: Stores login credentials.
- **`usage_log.csv`**: Tracks each user’s login and activity.

---

## 📊 Statistics Output

On login, if the role is `management`, statistical plots are automatically generated and saved as:
- `visit_trend.png`
- `insurance_distribution.png`
- `gender_distribution.png`
- `race_distribution.png`
- `ethnicity_distribution.png`

---

## 🧾 License

For educational use only – HI 741 Final Project, Spring 2025
