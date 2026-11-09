"""CSV ingestion, validation, duplicate prevention, and clean CSV export."""

import csv
from pathlib import Path
from validator import validate_contact

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "contacts.csv"
CLEAN_FILE = BASE_DIR / "students_clean.csv"


def load_contacts(input_file=INPUT_FILE, clean_file=CLEAN_FILE):
    """Read contacts.csv, validate rows, reject duplicates, and export clean rows."""
    students = []
    seen_phones = set()
    seen_emails = set()
    rejected = []
    total_rows = 0

    with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"name", "phone", "email"}
        if not reader.fieldnames or not required.issubset(
            {heading.strip().lower() for heading in reader.fieldnames}
        ):
            raise ValueError("CSV must contain name, phone, and email headers.")

        for row_number, row in enumerate(reader, start=2):
            total_rows += 1
            # Normalize header names and safely handle missing cells.
            normalized = {str(k).strip().lower(): (v or "").strip()
                          for k, v in row.items() if k is not None}
            name = normalized.get("name", "")
            phone = normalized.get("phone", "")
            email = normalized.get("email", "")

            is_valid, reason = validate_contact(name, phone, email)
            if not is_valid:
                rejected.append({"row": row_number, "name": name,
                                 "phone": phone, "email": email,
                                 "reason": reason})
                continue

            phone_key = phone
            email_key = email.lower()
            if phone_key in seen_phones:
                rejected.append({"row": row_number, "name": name,
                                 "phone": phone, "email": email,
                                 "reason": "Duplicate phone number"})
                continue
            if email_key in seen_emails:
                rejected.append({"row": row_number, "name": name,
                                 "phone": phone, "email": email,
                                 "reason": "Duplicate email address"})
                continue

            student = {
                "id": len(students) + 1,
                "name": name,
                "phone": phone,
                "email": email
            }
            students.append(student)
            seen_phones.add(phone_key)
            seen_emails.add(email_key)

    with open(clean_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "phone", "email"])
        writer.writeheader()
        writer.writerows(students)

    print("\n========== DATA INGESTION LOG ==========")
    print(f"Total rows read     : {total_rows}")
    print(f"Valid rows accepted : {len(students)}")
    print(f"Rejected rows       : {len(rejected)}")
    if rejected:
        print("\nReasons for rejected rows:")
        for item in rejected:
            print(f"  CSV row {item['row']}: {item['reason']}")
    print(f"\nClean data saved to : {clean_file.name}")
    print("========================================\n")

    return students, rejected


def save_students(students, clean_file=CLEAN_FILE):
    """Save the current in-memory student list to students_clean.csv."""
    with open(clean_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "phone", "email"])
        writer.writeheader()
        writer.writerows(students)
