import re
from .models import SchemeCustomer

def validate_nin(nin_number):
    if not nin_number:
        return "NIN is required"

    nin_number = nin_number.strip().upper()

    if len(nin_number) != 14:
        return "NIN number must be 14 characters long"

    if not nin_number.startswith(("CF", "CM")):
        return "NIN number must start with CF or CM"

    if not re.match(r'^[A-Z]{2}[0-9]{9}[A-Z]{3}$', nin_number):
        return "Invalid NIN format"

    if SchemeCustomer.objects.filter(nin_number=nin_number).exists():
        return "A customer with this NIN already exists"

    return None

def validate_phone(phone_number):
    if not phone_number:
        return "Phone number is required"

    phone_number = phone_number.strip()

    # normalize +256 format
    if phone_number.startswith("+256"):
        phone_number = "0" + phone_number[4:]

    if not phone_number.isdigit():
        return "Phone number must contain only digits"

    if len(phone_number) != 10:
        return "Phone number must be 10 digits"

    if not phone_number.startswith("0"):
        return "Phone number must start with 0 or +256"

    return None