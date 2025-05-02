USE inventory;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

INSERT INTO products (name, price, quantity) VALUES
    ('Laptop', 999.99, 10),
    ('Smartphone', 499.99, 20),
    ('Headphones', 99.99, 50),
    ('Tablet', 299.99, 15);

CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'readonly_password';
GRANT SELECT ON inventory.products TO 'readonly_user'@'%';

CREATE USER 'admin_user'@'%' IDENTIFIED BY 'admin_password';
GRANT ALL PRIVILEGES ON inventory.* TO 'admin_user'@'%';
