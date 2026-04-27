import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number"""
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone) is not None

def validate_age(age):
    """Validate age"""
    try:
        age_int = int(age)
        return 5 <= age_int <= 100
    except ValueError:
        return False