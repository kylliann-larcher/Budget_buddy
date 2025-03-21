# Verification password user
import hashlib
import re
from database import Database

class Utilisateur:
    def __init__(self, name, first_name, email, password):
        self.name = name
        self.first_name = first_name
        self.email = email
        self.password = password

    """@staticmethod
    def hasher_password(password):
        return hashlib.sha256(password.encode()).hexdigest()"""

    @staticmethod   # To organise functions in class without access instances (without self.password)
    def verif_password(password):
        return bool(re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{10,}$', password))