"""Main menu-driven application for Student Registration & Contact Intelligence."""

from pathlib import Path
from loader import load_contacts, save_students
from validator import validate_contact
from analytics import generate_report

BASE_DIR = Path(__file__).resolve().parent
CLEAN_FILE = BASE_DIR / "students_clean.csv"


def display_students(students):
    if not students:
        print("\nNo student records found.")
        return
    print("\n" + "-" * 82)
    print(f"{'ID':<5}{'NAME':<24}{'PHONE':<16}{'EMAIL'}")
    print("-" * 82)
    for s in students:
        print(f"{s['id']:<5}{s['name'][:22]:<24}{s['phone']:<16}{s['email']}")
    print("-" * 82)


def find_student(students, search_term):
    term = search_term.strip().lower()
    return [s for s in students if
            term in s["name"].lower() or
            term in s["phone"] or
            term in s["email"].lower()]


def next_id(students):
    return max((int(s["id"]) for s in students), default=0) + 1


def register_student(students):
    print("\n--- REGISTER STUDENT ---")
    name = input("Enter student name: ").strip()
    phone = input("Enter 10-digit phone number: ").strip()
    email = input("Enter email address: ").strip()

    valid, reason = validate_contact(name, phone, email)
    if not valid:
        print(f"Registration rejected: {reason}")
        return

    if any(s["phone"] == phone for s in students):
        print("Registration rejected: Phone number is already registered.")
        return
    if any(s["email"].lower() == email.lower() for s in students):
        print("Registration rejected: Email address is already registered.")
        return

    students.append({"id": next_id(students), "name": name,
                     "phone": phone, "email": email})
    save_students(students)
    print("Student registered successfully!")


def search_record(students):
    term = input("\nEnter name, phone number, or email to search: ")
    matches = find_student(students, term)
    display_students(matches)


def update_student(students):
    term = input("\nEnter student ID, phone number, name, or email: ").strip()
    matches = [s for s in students if
               str(s["id"]) == term or
               term.lower() in s["name"].lower() or
               term in s["phone"] or
               term.lower() in s["email"].lower()]
    if not matches:
        print("No matching student found.")
        return
    if len(matches) > 1:
        display_students(matches)
        print("More than one match. Search using the exact student ID.")
        return

    student = matches[0]
    print("Press Enter to keep the existing value.")
    name = input(f"Name [{student['name']}]: ").strip() or student["name"]
    phone = input(f"Phone [{student['phone']}]: ").strip() or student["phone"]
    email = input(f"Email [{student['email']}]: ").strip() or student["email"]

    valid, reason = validate_contact(name, phone, email)
    if not valid:
        print(f"Update rejected: {reason}")
        return
    for other in students:
        if other["id"] != student["id"]:
            if other["phone"] == phone:
                print("Update rejected: Phone number already belongs to another student.")
                return
            if other["email"].lower() == email.lower():
                print("Update rejected: Email already belongs to another student.")
                return

    student.update({"name": name, "phone": phone, "email": email})
    save_students(students)
    print("Student record updated successfully!")


def delete_student(students):
    term = input("\nEnter student ID or phone number to delete: ").strip()
    matches = [s for s in students
               if str(s["id"]) == term or s["phone"] == term]
    if not matches:
        print("No matching student found.")
        return
    student = matches[0]
    display_students(matches)
    confirm = input("Are you sure you want to delete this record? (y/n): ").lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student record deleted.")
    else:
        print("Delete cancelled.")


def print_menu():
    print("""
========== STUDENT REGISTRATION SYSTEM ==========
1. View All Students
2. Search Record
3. Register Student
4. Update Student
5. Delete Student
6. Analytics Report
7. Exit
=================================================
""")


def main():
    print("Loading student registration data...")
    students, rejected = load_contacts()

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            display_students(students)
        elif choice == "2":
            search_record(students)
        elif choice == "3":
            register_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            generate_report(students, rejected)
        elif choice == "7":
            save_students(students)
            print(f"Data saved to {CLEAN_FILE.name}. Thank you!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
