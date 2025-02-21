import re
import hashlib

def clean_phone_number(phone_number):
    """Removes non-numeric characters and validates phone number length."""
    cleaned_number = re.sub(r"\D", "", phone_number)  # Remove non-digit characters

    # Ensure length is between 10-15 digits (standard phone number range)
    if len(cleaned_number) < 10 or len(cleaned_number) > 15:
        return None  # Invalid phone number
    
    return f"+{cleaned_number}"  # Convert to E.164 format

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()
