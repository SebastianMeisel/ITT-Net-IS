#!/bin/bash

# Warten, bis Vault gestartet ist
sleep 5

# Vault-Adresse und Token setzen
export VAULT_ADDR=http://vault:8200
export VAULT_TOKEN=myroot

# KV Secrets Engine aktivieren
vault secrets enable -path=secret kv-v2

# MySQL Secrets in Vault speichern
vault kv put secret/mysql/admin \
    user=admin_user \
    password=admin_password

vault kv put secret/mysql/readonly \
    user=readonly_user \
    password=readonly_password

# Database Secrets Engine aktivieren
vault secrets enable database

# MySQL-Verbindung konfigurieren
vault write database/config/mysql \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(mysql-db:3306)/" \
    allowed_roles="readonly,admin" \
    username="root" \
    password="rootpassword"

# Readonly-Rolle erstellen
vault write database/roles/readonly \
    db_name=mysql \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}'; GRANT SELECT ON inventory.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"

# Admin-Rolle erstellen
vault write database/roles/admin \
    db_name=mysql \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}'; GRANT ALL PRIVILEGES ON inventory.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"

# AppRole Auth Method aktivieren
vault auth enable approle

# Policies erstellen
vault policy write readonly-policy -<<EOF
path "secret/data/mysql/readonly" {
  capabilities = ["read"]
}

path "database/creds/readonly" {
  capabilities = ["read"]
}
EOF

vault policy write admin-policy -<<EOF
path "secret/data/mysql/admin" {
  capabilities = ["read"]
}

path "database/creds/admin" {
  capabilities = ["read"]
}
EOF

# AppRoles erstellen
vault write auth/approle/role/readonly \
    token_policies=readonly-policy \
    token_ttl=1h \
    token_max_ttl=4h

vault write auth/approle/role/admin \
    token_policies=admin-policy \
    token_ttl=1h \
    token_max_ttl=4h

# AppRole IDs und Secrets abrufen und anzeigen
READONLY_ROLE_ID=$(vault read -format=json auth/approle/role/readonly/role-id | jq -r '.data.role_id')
READONLY_SECRET_ID=$(vault write -format=json -f auth/approle/role/readonly/secret-id | jq -r '.data.secret_id')

ADMIN_ROLE_ID=$(vault read -format=json auth/approle/role/admin/role-id | jq -r '.data.role_id')
ADMIN_SECRET_ID=$(vault write -format=json -f auth/approle/role/admin/secret-id | jq -r '.data.secret_id')

echo "Readonly Role ID: $READONLY_ROLE_ID"
echo "Readonly Secret ID: $READONLY_SECRET_ID"
echo "Admin Role ID: $ADMIN_ROLE_ID"
echo "Admin Secret ID: $ADMIN_SECRET_ID"
