# main.py
from password_generator import PasswordGenerator
from password_strength import PasswordStrengthChecker
from password_manager import PasswordManager
import getpass

def main():
    print("🔐 Gestionnaire de Mots de Passe")
    print("=" * 40)
    
    # Initialisation
    generator = PasswordGenerator()
    checker = PasswordStrengthChecker()
    
    # Demander le mot de passe maître (optionnel)
    use_encryption = input("Utiliser un mot de passe maître ? (o/n): ").lower() == 'o'
    master_password = None
    
    if use_encryption:
        master_password = getpass.getpass("Mot de passe maître: ")
    
    manager = PasswordManager(master_password=master_password)
    
    while True:
        print("\n📋 Menu Principal")
        print("1. Générer un mot de passe")
        print("2. Vérifier la force d'un mot de passe")
        print("3. Sauvegarder un mot de passe")
        print("4. Récupérer un mot de passe")
        print("5. Lister les services")
        print("6. Supprimer un mot de passe")
        print("7. Exporter les mots de passe")
        print("8. Quitter")
        
        choice = input("\nVotre choix (1-8): ")
        
        if choice == '1':
            generate_password_menu(generator, checker)
        elif choice == '2':
            check_password_strength(checker)
        elif choice == '3':
            save_password_menu(manager)
        elif choice == '4':
            retrieve_password_menu(manager)
        elif choice == '5':
            list_services_menu(manager)
        elif choice == '6':
            delete_password_menu(manager)
        elif choice == '7':
            export_passwords_menu(manager)
        elif choice == '8':
            print("Au revoir ! 👋")
            break
        else:
            print("❌ Choix invalide")

def generate_password_menu(generator, checker):
    print("\n🎲 Génération de Mot de Passe")
    
    try:
        length = int(input("Longueur (défaut: 12): ") or "12")
        use_uppercase = input("Majuscules ? (O/n): ").lower() != 'n'
        use_lowercase = input("Minuscules ? (O/n): ").lower() != 'n'
        use_digits = input("Chiffres ? (O/n): ").lower() != 'n'
        use_symbols = input("Symboles ? (O/n): ").lower() != 'n'
        exclude_ambiguous = input("Exclure caractères ambigus (0,O,l,1) ? (o/N): ").lower() == 'o'
        
        count = int(input("Nombre de mots de passe (défaut: 1): ") or "1")
        
        if count == 1:
            password = generator.generate_password(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_ambiguous=exclude_ambiguous
            )
            
            print(f"\n🔑 Mot de passe généré: {password}")
            
            # Vérifier la force
            strength = checker.check_strength(password)
            print(f"💪 Force: {strength['strength']} ({strength['score']}/100)")
            
            if strength['feedback']:
                print("💡 Suggestions:")
                for suggestion in strength['feedback']:
                    print(f"   • {suggestion}")
        else:
            passwords = generator.generate_multiple(
                count=count,
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_ambiguous=exclude_ambiguous
            )
            
            print(f"\n🔑 {count} mots de passe générés:")
            for i, pwd in enumerate(passwords, 1):
                strength = checker.check_strength(pwd)
                print(f"{i}. {pwd} - {strength['strength']}")
                
    except ValueError as e:
        print(f"❌ Erreur: {e}")

def check_password_strength(checker):
    print("\n💪 Vérification de la Force")
    password = getpass.getpass("Entrez le mot de passe à vérifier: ")
    
    result = checker.check_strength(password)
    
    print(f"\n📊 Résultat:")
    print(f"Force: {result['strength']}")
    print(f"Score: {result['score']}/100")
    
    if result['feedback']:
        print("\n💡 Suggestions d'amélioration:")
        for suggestion in result['feedback']:
            print(f"   • {suggestion}")

def save_password_menu(manager):
    print("\n💾 Sauvegarder un Mot de Passe")
    
    service = input("Service/Site: ")
    username = input("Nom d'utilisateur: ")
    password = getpass.getpass("Mot de passe: ")
    notes = input("Notes (optionnel): ")
    
    manager.save_password(service, username, password, notes)
    print(f"✅ Mot de passe sauvegardé pour {service}")

def retrieve_password_menu(manager):
    print("\n🔍 Récupérer un Mot de Passe")
    
    service = input("Service/Site: ")
    entry = manager.get_password(service)
    
    if entry:
        print(f"\n📋 Informations pour {service}:")
        print(f"Utilisateur: {entry['username']}")
        print(f"Mot de passe: {entry['password']}")
        if entry['notes']:
            print(f"Notes: {entry['notes']}")
        print(f"Créé le: {entry['created_at'][:10]}")
    else:
        print(f"❌ Aucun mot de passe trouvé pour {service}")

def list_services_menu(manager):
    print("\n📋 Services Sauvegardés")
    
    services = manager.list_services()
    
    if services:
        for i, service in enumerate(services, 1):
            print(f"{i}. {service}")
    else:
        print("Aucun service sauvegardé")

def delete_password_menu(manager):
    print("\n🗑️ Supprimer un Mot de Passe")
    
    service = input("Service/Site à supprimer: ")
    
    if manager.delete_password(service):
        print(f"✅ Mot de passe supprimé pour {service}")
    else:
        print(f"❌ Aucun mot de passe trouvé pour {service}")

def export_passwords_menu(manager):
    print("\n📤 Exporter les Mots de Passe")
    
    filename = input("Nom du fichier d'export (défaut: export.json): ") or "export.json"
    
    try:
        manager.export_passwords(filename)
        print(f"✅ Mots de passe exportés vers {filename}")
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")

if __name__ == "__main__":
    main()