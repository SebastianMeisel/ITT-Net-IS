import os
import hvac
from dotenv import load_dotenv

load_dotenv()

def get_vault_client():
    """Verbindung zum Vault-Server herstellen und authentifizieren"""
    client = hvac.Client(url=os.environ.get('VAULT_ADDR', 'http://vault:8200'))
    
    # Mit AppRole authentifizieren
    role_id = os.environ.get('VAULT_ROLE_ID')
    secret_id = os.environ.get('VAULT_SECRET_ID')
    
    if not role_id or not secret_id:
        raise ValueError("VAULT_ROLE_ID und VAULT_SECRET_ID müssen gesetzt sein")
    
    # AppRole-Authentifizierung durchführen
    client.auth.approle.login(
        role_id=role_id,
        secret_id=secret_id
    )
    
    return client

def get_static_credentials(path):
    """Statische Credentials von Vault abrufen"""
    client = get_vault_client()
    response = client.secrets.kv.v2.read_secret_version(path=path)
    return response['data']['data']

def get_dynamic_credentials(path):
    """Dynamische Credentials von Vault abrufen"""
    client = get_vault_client()
    response = client.read(path)
    return response['data']
