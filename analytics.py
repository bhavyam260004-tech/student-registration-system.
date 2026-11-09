"""Business intelligence reports using basic Python dictionaries and loops."""

from collections import Counter


def generate_report(students, rejected):
    total = len(students) + len(rejected)
    accepted = len(students)
    accuracy = (accepted / total * 100) if total else 0

    phone_prefixes = Counter()
    email_domains = Counter()
    rejection_reasons = Counter()

    for student in students:
        phone = student["phone"]
        email = student["email"]
        if phone:
            phone_prefixes[phone[0]] += 1
        if "@" in email:
            domain = email.rsplit("@", 1)[1].lower()
            email_domains[domain] += 1

    for item in rejected:
        rejection_reasons[item["reason"]] += 1

    print("\n" + "=" * 55)
    print("       STUDENT REGISTRATION - BUSINESS INTELLIGENCE")
    print("=" * 55)
    print(f"Total Contacts Processed : {total}")
    print(f"Valid Registrations      : {accepted}")
    print(f"Rejected Records         : {len(rejected)}")
    print(f"Data Quality Accuracy    : {accuracy:.1f}%")

    print("\n--- Rejection Reason Breakdown ---")
    if rejection_reasons:
        for reason, count in rejection_reasons.most_common():
            print(f"{reason:<38}: {count}")
    else:
        print("No rejected records.")

    print("\n--- Telecom Network Breakdown ---")
    prefix_labels = {
        "9": "9-Series", "8": "8-Series",
        "7": "7-Series", "6": "6-Series"
    }
    for prefix in ["9", "8", "7", "6"]:
        print(f"{prefix_labels[prefix]:<15}: {phone_prefixes.get(prefix, 0)} students")

    print("\n--- Top Email Domains ---")
    if email_domains:
        for domain, count in email_domains.most_common():
            print(f"@{domain:<28}: {count} students")
    else:
        print("No valid email domains available.")

    print("=" * 55 + "\n")

    return {
        "total": total,
        "accepted": accepted,
        "rejected": len(rejected),
        "accuracy": accuracy,
        "phone_prefixes": dict(phone_prefixes),
        "email_domains": dict(email_domains),
        "rejection_reasons": dict(rejection_reasons)
    }
