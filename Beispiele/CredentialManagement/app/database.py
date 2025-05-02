import mysql.connector

def connect_to_database():
    # PROBLEM: Hartcodierte Credentials im Code
    connection = mysql.connector.connect(
        host="mysql",
        database="inventory",
        user="admin_user",
        password="admin_password"  # Sensible Information im Klartext!
    )
    return connection

def get_all_products():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

import mysql.connector
from vault_client import get_static_credentials, get_dynamic_credentials

def connect_with_static_credentials():
    """Verbindung mit statischen Credentials herstellen"""
    # Credentials aus Vault abrufen
    creds = get_static_credentials('mysql/admin')
    
    # Mit den abgerufenen Credentials verbinden
    connection = mysql.connector.connect(
        host="mysql",
        database="inventory",
        user=creds['user'],
        password=creds['password']
    )
    return connection

def connect_with_dynamic_credentials():
    """Verbindung mit dynamischen Credentials herstellen"""
    # Dynamische Credentials für die Admin-Rolle erstellen
    creds = get_dynamic_credentials('database/creds/admin')
    
    # Mit den dynamisch erstellten Credentials verbinden
    connection = mysql.connector.connect(
        host="mysql",
        database="inventory",
        user=creds['username'],
        password=creds['password']
    )
    return connection

def get_all_products(use_dynamic=True):
    """Alle Produkte aus der Datenbank abrufen"""
    if use_dynamic:
        connection = connect_with_dynamic_credentials()
    else:
        connection = connect_with_static_credentials()
        
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products
