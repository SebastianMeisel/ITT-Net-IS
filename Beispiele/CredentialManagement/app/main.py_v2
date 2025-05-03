from database import get_all_products
import argparse

def show_all_products(use_dynamic):
    try:
        products = get_all_products(use_dynamic=use_dynamic)
        print("\n=== Produkte im Inventar ===")
        for product in products:
            print(f"ID: {product['id']}, Name: {product['name']}, "
                  f"Preis: €{product['price']}, Menge: {product['quantity']}")
        
        credential_type = "dynamischen" if use_dynamic else "statischen"
        print(f"\nErfolgreich mit {credential_type} Credentials verbunden!")
    except Exception as e:
        print(f"Fehler beim Abrufen der Produkte: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Credential Demo mit HashiCorp Vault')
    parser.add_argument('--static', action='store_true', help='Statische Credentials verwenden')
    args = parser.parse_args()
    
    show_all_products(not args.static)
