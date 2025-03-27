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
        
        self.gpg = gnupg.GPG(gnupghome=gnupg_home)
        self.gpg.encoding = 'utf-8'

    def generate_key(self, name, email, passphrase):
        """
        Generate a new GPG key pair
        
        :param name: Full name for the key
        :param email: Email address
        :param passphrase: Passphrase for the key
        :return: Generated key details
        """
        input_data = self.gpg.gen_key_input(
            name_real=name,
            name_email=email,
            passphrase=passphrase,
            key_type='RSA',
            key_length=4096,
            expire_date='2y'
        )
        return self.gpg.gen_key(input_data)

    def encrypt_file(self, file_path, recipients, output_path=None):
        """
        Encrypt a file for specified recipients
        
        :param file_path: Path to the file to encrypt
        :param recipients: List of recipient email addresses
        :param output_path: Optional output file path
        :return: Path to encrypted file
        """
        with open(file_path, 'rb') as f:
            status = self.gpg.encrypt_file(
                f, 
                recipients, 
                output=output_path or f'{file_path}.gpg',
                always_trust=True
            )
        
        if not status.ok:
            raise ValueError(f"Encryption failed: {status.status}")
        
        return status.output

    def decrypt_file(self, encrypted_file_path, passphrase, output_path=None):
        """
        Decrypt an encrypted file
        
        :param encrypted_file_path: Path to the encrypted file
        :param passphrase: Passphrase for the key
        :param output_path: Optional output file path
        :return: Decrypted file path
        """
        with open(encrypted_file_path, 'rb') as f:
            status = self.gpg.decrypt_file(
                f, 
                passphrase=passphrase,
                output=output_path or encrypted_file_path.replace('.gpg', '')
            )
        
        if not status.ok:
            raise ValueError(f"Decryption failed: {status.status}")
        
        return status.output

    def sign_file(self, file_path, keyid, passphrase, detach=True):
        """
        Sign a file
        
        :param file_path: Path to the file to sign
        :param keyid: Key ID to use for signing
        :param passphrase: Passphrase for the key
        :param detach: Whether to create a detached signature
        :return: Signature
        """
        with open(file_path, 'rb') as f:
            status = self.gpg.sign_file(
                f, 
                keyid=keyid, 
                passphrase=passphrase,
                detach=detach
            )
        
        if not status.ok:
            raise ValueError(f"Signing failed: {status.status}")
        
        return status.data

    def verify_signature(self, signature_path, original_file_path):
        """
        Verify a signature
        
        :param signature_path: Path to the signature file
        :param original_file_path: Path to the original file
        :return: Verification status
        """
        with open(signature_path, 'rb') as sig_file, \
             open(original_file_path, 'rb') as orig_file:
            verified = self.gpg.verify_file(sig_file, orig_file)
        
        return {
            'valid': verified.valid,
            'status': verified.status,
            'key_id': verified.key_id,
            'username': verified.username
        }

# Beispielnutzung
def main():
    try:
        # GPG-Handler initialisieren
        gpg_handler = GPGHandler()

        # Neuen Schlüssel generieren
        key = gpg_handler.generate_key(
            name='Max Mustermann', 
            email='max@beispiel.de', 
            passphrase='sicherespasswort123'
        )
        print(f"Generated key: {key}")

        # Datei verschlüsseln
        encrypted_file = gpg_handler.encrypt_file(
            'geheim.txt', 
            recipients=['max@beispiel.de']
        )
        print(f"Encrypted file: {encrypted_file}")

        # Datei entschlüsseln
        decrypted_file = gpg_handler.decrypt_file(
            encrypted_file, 
            passphrase='sicherespasswort123'
        )
        print(f"Decrypted file: {decrypted_file}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == '__main__':
    main()

# Zusätzliche Hinweise zur Installation:
# pip install python-gnupg
# Benötigt GPG-Installation auf dem System
