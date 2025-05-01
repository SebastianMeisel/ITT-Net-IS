import os
import hashlib
import base64
import configparser
import logging

# Konfiguriere das Logging
def setup_logging():
    """Konfiguriert das Logging-System"""
    # Erstelle einen Logger
    logger = logging.getLogger('password_hashing')
    logger.setLevel(logging.INFO)
    
    # Erstelle einen Konsolen-Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Optional: Erstelle einen Datei-Handler für persistentes Logging
    file_handler = logging.FileHandler('password_hashing.log')
    file_handler.setLevel(logging.INFO)
    
    # Erstelle ein Formatter für die Log-Nachrichten
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Füge die Handler zum Logger hinzu
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Initialisiere den Logger
logger = setup_logging()

def load_config():
    """Lädt die Konfiguration aus einer Datei (simuliert)"""
    logger.debug("Lade Konfiguration")
    config = configparser.ConfigParser()
    # In der Praxis würde die Konfiguration aus einer Datei geladen werden
    # Für dieses Beispiel verwenden wir einen hartcodierten Wert
    config["SECURITY"] = {"PEPPER": "mein_geheimer_pepper_wert"}
    return config

def get_secret_pepper_from_config():
    """Liest den Pepper-Wert aus der Konfiguration"""
    logger.debug("Hole Pepper aus Konfiguration")
    config = load_config()
    return config["SECURITY"]["PEPPER"]

def generate_random_bytes(length):
    """Generiert zufällige Bytes als Salt"""
    logger.debug(f"Generiere zufällige Bytes mit Länge {length}")
    return os.urandom(length)

def hash(password_string, pepper_string, salt_bytes):
    """
    Berechnet einen sicheren Hash unter Verwendung von Passwort, Pepper und Salt
    Verwendet SHA-256 als Hash-Funktion
    """
    logger.debug("Berechne Hash mit Passwort, Pepper und Salt")
    
    # Kombiniere Passwort, Pepper und Salt
    combined = password_string.encode('utf-8') + pepper_string.encode('utf-8') + salt_bytes
    
    # Berechne den Hash
    hash_obj = hashlib.sha256(combined)
    hashed_value = hash_obj.digest()
    
    # Logge den Hash (ohne das Passwort selbst zu loggen)
    hash_base64 = base64.b64encode(hashed_value).decode('utf-8')
    salt_base64 = base64.b64encode(salt_bytes).decode('utf-8')
    logger.info(f"Hash berechnet - Salt (Base64): {salt_base64}, Hash (Base64): {hash_base64}")
    
    return hashed_value

def store_in_database(username, salt, hashed_password):
    """
    Speichert die Benutzerdaten in einer Datenbank (simuliert)
    In der Praxis würde hier eine echte Datenbankverbindung verwendet werden
    """
    logger.info(f"Speichere Benutzerdaten für {username} in der Datenbank")
    
    # Hier würde die Speicherung in der Datenbank erfolgen
    # Für dieses Beispiel speichern wir die Daten in einem Dictionary
    user_database = {}
    user_database[username] = {
        'salt': salt,
        'hash': hashed_password
    }
    
    salt_base64 = base64.b64encode(salt).decode('utf-8')
    hash_base64 = base64.b64encode(hashed_password).decode('utf-8')
    
    logger.debug(f"Benutzer {username} gespeichert - Salt: {salt_base64}, Hash: {hash_base64}")
    print(f"Benutzer {username} wurde in der Datenbank gespeichert")
    print(f"Salt (Base64): {salt_base64}")
    print(f"Hash (Base64): {hash_base64}")
    
    return user_database

def get_user_data_from_database(username, user_database):
    """
    Holt die Benutzerdaten aus der Datenbank (simuliert)
    In der Praxis würde hier eine echte Datenbankabfrage erfolgen
    """
    logger.debug(f"Suche Benutzerdaten für {username} in der Datenbank")
    
    if username not in user_database:
        logger.warning(f"Benutzer {username} wurde nicht gefunden")
        raise ValueError(f"Benutzer {username} wurde nicht gefunden")
    
    user_data = user_database[username]
    logger.debug(f"Benutzerdaten für {username} gefunden")
    return user_data['salt'], user_data['hash']

def register_user(username, password):
    """Registriert einen neuen Benutzer"""
    logger.info(f"Registriere neuen Benutzer: {username}")
    
    # Generiere einen zufälligen Salt
    salt = generate_random_bytes(16)
    
    # Hole den Pepper aus einer sicheren Quelle (nicht in der DB)
    pepper = get_secret_pepper_from_config()
    
    # Berechne den Hash mit Salt und Pepper
    hashed_password = hash(password, pepper, salt)
    
    # Speichere Benutzername, Salt und Hash in der Datenbank
    return store_in_database(username, salt, hashed_password)

def verify_login(username, password, user_database):
    """Überprüft die Anmeldedaten eines Benutzers"""
    logger.info(f"Überprüfe Login für Benutzer: {username}")
    
    try:
        # Hole Salt und Hash aus der Datenbank
        salt, stored_hash = get_user_data_from_database(username, user_database)
        
        # Hole den Pepper aus einer sicheren Quelle
        pepper = get_secret_pepper_from_config()
        
        # Berechne den Hash mit dem eingegebenen Passwort
        computed_hash = hash(password, pepper, salt)
        
        # Vergleiche den berechneten Hash mit dem gespeicherten Hash
        result = computed_hash == stored_hash
        
        if result:
            logger.info(f"Login für {username} erfolgreich")
        else:
            logger.warning(f"Login für {username} fehlgeschlagen - Falsches Passwort")
        
        return result
    except ValueError:
        # Benutzer nicht gefunden
        logger.warning(f"Login für {username} fehlgeschlagen - Benutzer nicht gefunden")
        return False

# Beispiel für die Verwendung
if __name__ == "__main__":
    logger.info("Starte Passwort-Hashing-Beispiel")
    
    # Registriere einen neuen Benutzer
    username = "max_mustermann"
    password = "sicheres_passwort123"
    
    # Registriere den Benutzer und erhalte die simulierte Datenbank zurück
    user_db = register_user(username, password)
    
    # Überprüfe einen erfolgreichen Login
    success = verify_login(username, password, user_db)
    print(f"Login erfolgreich: {success}")
    
    # Überprüfe einen fehlgeschlagenen Login
    wrong_password = "falsches_passwort"
    failure = verify_login(username, wrong_password, user_db)
    print(f"Login mit falschem Passwort erfolgreich: {failure}")
    
    logger.info("Passwort-Hashing-Beispiel abgeschlossen")
