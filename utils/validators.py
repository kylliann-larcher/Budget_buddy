# Verification info login
import re

def verif_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def verif_password(password):
    if len(password) < 5 or \
        not re.search(r"[A-Za-z]", password) or \
        not re.search(r"\d", password) or \
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    else:
        return True