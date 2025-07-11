# password_strength.py
import re

class PasswordStrengthChecker:
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "password123", "admin", "qwerty",
            "letmein", "welcome", "monkey", "1234567890"
        ]
    
    def check_strength(self, password):
        """
        Évalue la force d'un mot de passe
        Retourne un dictionnaire avec le score et les détails
        """
        score = 0
        feedback = []
        
        # Longueur
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
            feedback.append("Augmentez la longueur à 12+ caractères")
        else:
            score += 5
            feedback.append("Mot de passe trop court (minimum 8 caractères)")
        
        # Minuscules
        if re.search(r'[a-z]', password):
            score += 15
        else:
            feedback.append("Ajoutez des lettres minuscules")
        
        # Majuscules
        if re.search(r'[A-Z]', password):
            score += 15
        else:
            feedback.append("Ajoutez des lettres majuscules")
        
        # Chiffres
        if re.search(r'\d', password):
            score += 15
        else:
            feedback.append("Ajoutez des chiffres")
        
        # Symboles
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 20
        else:
            feedback.append("Ajoutez des caractères spéciaux")
        
        # Variété de caractères
        unique_chars = len(set(password))
        if unique_chars >= len(password) * 0.7:
            score += 10
        else:
            feedback.append("Évitez la répétition de caractères")
        
        # Mots de passe communs
        if password.lower() in self.common_passwords:
            score = max(0, score - 50)
            feedback.append("Évitez les mots de passe communs")
        
        # Patterns séquentiels
        if self._has_sequential_pattern(password):
            score = max(0, score - 20)
            feedback.append("Évitez les séquences (123, abc, etc.)")
        
        # Déterminer le niveau
        if score >= 80:
            strength = "Très Fort"
        elif score >= 60:
            strength = "Fort"
        elif score >= 40:
            strength = "Moyen"
        elif score >= 20:
            strength = "Faible"
        else:
            strength = "Très Faible"
        
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        }
    
    def _has_sequential_pattern(self, password):
        """
        Détecte les patterns séquentiels
        """
        sequences = [
            "123456789", "abcdefghijklmnopqrstuvwxyz", "qwertyuiop",
            "987654321", "zyxwvutsrqponmlkjihgfedcba"
        ]
        
        password_lower = password.lower()
        for seq in sequences:
            for i in range(len(seq) - 2):
                if seq[i:i+3] in password_lower:
                    return True
        return False