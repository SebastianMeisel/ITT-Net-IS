from database import get_all_products

def show_all_products():
    try:
        products = get_all_products()
        print("\n=== Produkte im Inventar ===")
        for product in products:
            print(f"ID: {product['id']}, Name: {product['name']}, "
                  f"Preis: €{product['price']}, Menge: {product['quantity']}")
    except Exception as e:
        print(f"Fehler beim Abrufen der Produkte: {e}")

if __name__ == "__main__":
    show_all_products()
