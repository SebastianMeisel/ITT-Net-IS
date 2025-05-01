import gnupg
import os

class GPGHandler:
    def __init__(self, gnupg_home=None):
        """
        Initialize GPG handler with optional custom home directory
        
        :param gnupg_home: Custom directory for GPG keyring (optional)
        """
        if gnupg_home is None:
            gnupg_home = os.path.expanduser('~/.gnupg')
        
        # Sicherstellen, dass das Verzeichnis existiert
        os.makedirs(gnupg_home, exist_ok=True)
        
        # Kompatible Initialisierung
        try:
            # Versuch mit gnupghome
            self.gpg = gnupg.GPG(gnupghome=gnupg_home)
        except TypeError:
            try:
                # Fallback ohne gnupghome
                self.gpg = gnupg.GPG()
                # Manuell Homeverzeichnis setzen
                os.environ['GNUPGHOME'] = gnupg_home
            except Exception as e:
                print(f"Fehler bei GPG-Initialisierung: {e}")
                raise

        self.gpg.encoding = 'utf-8'

    def generate_key(self, name, email, passphrase, key_length=4096, expire_date='2y'):
        """
        Generate a new GPG key pair
        
        :param name: Full name for the key
        :param email: Email address
        :param passphrase: Passphrase for the key
        :param key_length: Key length (default 4096)
        :param expire_date: Key expiration (default 2 years)
        :return: Generated key details
        """
        input_data = self.gpg.gen_key_input(
            name_real=name,
            name_email=email,
            passphrase=passphrase,
            key_type='RSA',
            key_length=key_length,
            expire_date=expire_date
        )
        return self.gpg.gen_key(input_data)

    def export_public_key(self, email, output_file=None):
        """
        Export public key for a specific email
        
        :param email: Email address of the key to export
        :param output_file: Optional output file path
        :return: Public key as string or exported file path
        """
        keys = self.list_keys()
        for key in keys:
            for uid in key.get('uids', []):
                if email in uid:
                    if output_file:
                        with open(output_file, 'wb') as f:
                            f.write(self.gpg.export_keys(key['keyid']).encode('utf-8'))
                        return output_file
                    return self.gpg.export_keys(key['keyid'])
        
        raise ValueError(f"No key found for email {email}")

    def list_keys(self, secret=False):
        """
        List available GPG keys
        
        :param secret: List secret keys if True, public keys if False
        :return: List of keys
        """
        try:
            if secret:
                return self.gpg.list_keys(secret=True)
            return self.gpg.list_keys()
        except Exception as e:
            print(f"Fehler beim Auflisten der Schlüssel: {e}")
            return []

    def encrypt_string(self, message, recipients):
        """
        Encrypt a string for specified recipients
        
        :param message: String to encrypt
        :param recipients: List of recipient email addresses or key IDs
        :return: Encrypted message
        """
        # Überprüfen und ggf. Schlüssel exportieren
        try:
            encrypted_data = self.gpg.encrypt(message, recipients, always_trust=True)
            
            if not encrypted_data.ok:
                print(f"Encryption status details: {encrypted_data}")
                raise ValueError(f"Encryption failed: {encrypted_data.status}")
            
            return str(encrypted_data)
        except Exception as e:
            print(f"Detaillierter Verschlüsselungsfehler: {e}")
            raise

    def decrypt_string(self, encrypted_message, passphrase):
        """
        Decrypt an encrypted message
        
        :param encrypted_message: Encrypted message to decrypt
        :param passphrase: Passphrase for the key
        :return: Decrypted message
        """
        decrypted_data = self.gpg.decrypt(encrypted_message, passphrase=passphrase)
        
        if not decrypted_data.ok:
            raise ValueError(f"Decryption failed: {decrypted_data.status}")
        
        return str(decrypted_data)

def main():
    try:
        # GPG-Handler initialisieren
        gpg_handler = GPGHandler()

        # Vorhandene Schlüssel auflisten
        print("Vorhandene öffentliche Schlüssel:")
        keys = gpg_handler.list_keys()
        if keys:
            for key in keys:
                print(f"Fingerabdruck: {key.get('fingerprint', 'N/A')}")
                print(f"Benutzer-IDs: {key.get('uids', 'N/A')}\n")
        else:
            print("Keine Schlüssel gefunden.")

        # Schlüssel generieren
        print("Generiere neuen Schlüssel...")
        new_key = gpg_handler.generate_key(
            name='Max Mustermann', 
            email='max@beispiel.de', 
            passphrase='sicherespasswort123'
        )
        print(f"Neuer Schlüssel generiert: {new_key}")

        # Öffentlichen Schlüssel exportieren
        public_key_file = 'max_public_key.asc'
        gpg_handler.export_public_key('max@beispiel.de', public_key_file)
        print(f"Öffentlicher Schlüssel exportiert nach: {public_key_file}")

        # Nachricht verschlüsseln und entschlüsseln
        original_message = "Geheime Nachricht für Max"
        print("\nVerschlüsselung und Entschlüsselung:")
        encrypted = gpg_handler.encrypt_string(
            original_message, 
            recipients=['max@beispiel.de']
        )
        print(f"Verschlüsselte Nachricht: {encrypted}")

        decrypted = gpg_handler.decrypt_string(
            encrypted, 
            passphrase='sicherespasswort123'
        )
        print(f"Entschlüsselte Nachricht: {decrypted}")

        # Überprüfen, ob Entschlüsselung erfolgreich war
        assert original_message == decrypted, "Entschlüsselung fehlgeschlagen!"

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

# Installationshinweise:
# 1. GPG installieren:
#    - Ubuntu/Debian: sudo apt-get install gpg
#    - MacOS: brew install gpg
#    - Windows: https://www.gpg4win.org/
#
# 2. Python-Bibliothek installieren:
#    pip install python-gnupg
