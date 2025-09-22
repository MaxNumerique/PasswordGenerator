# password_manager.py
import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
import base64
import hashlib


class PasswordManager:
    def __init__(self, filename="passwords.json", master_password=None):
        self.filename = filename
        self.master_password = master_password
        self.cipher = None

        if master_password:
            self._setup_encryption()

    def _setup_encryption(self):
        # Créer une clé à partir du mot de passe maître
        key = hashlib.pbkdf2_hmac(
            "sha256", self.master_password.encode(), b"salt_", 100000
        )
        key = base64.urlsafe_b64encode(key)
        self.cipher = Fernet(key)

    def save_password(self, service, username, password, notes=""):
        data = self._load_data()

        entry = {
            "username": username,
            "password": password,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        if self.cipher:
            entry["password"] = self.cipher.encrypt(password.encode()).decode()

        data[service] = entry
        self._save_data(data)

    def get_password(self, service):
        data = self._load_data()

        if service not in data:
            return None

        entry = data[service].copy()

        if self.cipher and "password" in entry:
            try:
                entry["password"] = self.cipher.decrypt(
                    entry["password"].encode()
                ).decode()
            except:
                entry["password"] = "[Erreur de déchiffrement]"

        return entry

    def list_services(self):
        data = self._load_data()
        return list(data.keys())

    def delete_password(self, service):
        data = self._load_data()

        if service in data:
            del data[service]
            self._save_data(data)
            return True
        return False

    def export_passwords(self, export_filename):
        data = self._load_data()
        # Déchiffrer si nécessaire
        if self.cipher:
            for service, entry in data.items():
                try:
                    entry["password"] = self.cipher.decrypt(
                        entry["password"].encode()
                    ).decode()
                except:
                    entry["password"] = "[Erreur de déchiffrement]"

        with open(export_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_data(self):
        if not os.path.exists(self.filename):
            return {}

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_data(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
