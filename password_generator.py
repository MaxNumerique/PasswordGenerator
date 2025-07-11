# password_generator.py
import random
import string

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(self, length=12, use_uppercase=True, use_lowercase=True, 
                        use_digits=True, use_symbols=True, exclude_ambiguous=False):
        """
        Génère un mot de passe selon les critères spécifiés
        """
        if length < 4:
            raise ValueError("La longueur doit être d'au moins 4 caractères")
        
        # Construction du jeu de caractères
        characters = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = chars.replace('l', '').replace('o', '')
            characters += chars
            required_chars.append(random.choice(chars))
        
        if use_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = chars.replace('I', '').replace('O', '')
            characters += chars
            required_chars.append(random.choice(chars))
        
        if use_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = chars.replace('0', '').replace('1', '')
            characters += chars
            required_chars.append(random.choice(chars))
        
        if use_symbols:
            characters += self.symbols
            required_chars.append(random.choice(self.symbols))
        
        if not characters:
            raise ValueError("Au moins un type de caractère doit être sélectionné")
        
        # Génération du mot de passe
        password = required_chars.copy()
        
        # Compléter avec des caractères aléatoires
        for _ in range(length - len(required_chars)):
            password.append(random.choice(characters))
        
        # Mélanger le mot de passe
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_multiple(self, count=5, **kwargs):
        """
        Génère plusieurs mots de passe
        """
        return [self.generate_password(**kwargs) for _ in range(count)]