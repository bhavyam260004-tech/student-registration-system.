"""Field validation for the Student Registration & Contact Intelligence System."""

def validate_contact(name, phone, email):
    """
    Validate one contact.

    Returns:
        (True, "Valid") when all fields pass.
        (False, reason) when the first validation rule fails.
    """
    name = str(name or "").strip()
    phone = str(phone or "").strip()
    email = str(email or "").strip()

    if not name:
        return False, "Name is blank"

    if len(phone) != 10 or not phone.isdigit():
        return False, "Phone must contain exactly 10 digits"
    if phone[0] not in "6789":
        return False, "Phone must start with 6, 7, 8, or 9"

    if email.count("@") != 1:
        return False, "Email must contain exactly one @ symbol"
    if any(char.isspace() for char in email):
        return False, "Email must not contain whitespace"

    local, domain = email.split("@")
    if not local:
        return False, "Email must contain text before @"
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False, "Email domain must contain a valid period"

    return True, "Valid"
