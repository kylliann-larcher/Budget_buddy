

utilisateurs (users)
  ├── comptes (accounts)
  │     └── transactions (transactions)
  │           ├── types_transaction (transaction_types)
  │           └── catégories (categories)
  └── alertes (alerts)


-- Création de la base de données
CREATE DATABASE IF NOT EXISTS database_solana_zm;
USE database_solana_zm;

-- Table des utilisateurs
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    lastname VARCHAR(50) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table des comptes bancaires
CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    account_name VARCHAR(50) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table des catégories de transaction
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- Table des types de transaction
CREATE TABLE transaction_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(20) NOT NULL UNIQUE
);

-- Table des transactions
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    type_id INT NOT NULL,
    category_id INT,
    account_id INT NOT NULL,
    recipient_account_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id) REFERENCES transaction_types(type_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_account_id) REFERENCES accounts(account_id)
);

-- Table des alertes
CREATE TABLE alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Insertion des types de transaction
INSERT INTO transaction_types (type_name) VALUES 
('Dépôt'), 
('Retrait'), 
('Transfert');

-- Insertion des catégories de base
INSERT INTO categories (category_name, description) VALUES 
('Loisir', 'Dépenses liées aux activités de loisir'),
('Repas', 'Dépenses alimentaires'),
('Transport', 'Dépenses liées aux transports'),
('Logement', 'Dépenses liées au logement'),
('Santé', 'Dépenses médicales'),
('Salaire', 'Revenus professionnels'),
('Autre', 'Autres types de transactions');

-- Création d'un index pour optimiser les recherches par date
CREATE INDEX idx_transaction_date ON transactions(transaction_date);
CREATE INDEX idx_transaction_amount ON transactions(amount);
CREATE INDEX idx_transaction_type ON transactions(type_id);
CREATE INDEX idx_transaction_category ON transactions(category_id);




--Users - Accounts: Relation (1,n)

---Un utilisateur peut avoir plusieurs comptes (n)
---Un compte appartient à un seul utilisateur (1)
---C'est une relation de type "un à plusieurs"


--Users - Alerts: Relation (1,n)

---Un utilisateur peut recevoir plusieurs alertes (n)
---Une alerte est liée à un seul utilisateur (1)
---C'est une relation de type "un à plusieurs"


--Accounts - Transactions: Relation (1,n)

---Un compte peut avoir plusieurs transactions (n)
---Une transaction est liée à un compte source (1)
---C'est une relation de type "un à plusieurs"


--Categories - Transactions: Relation (1,n)

---Une catégorie peut être associée à plusieurs transactions (n)
---Une transaction appartient à une seule catégorie (1)
---C'est une relation de type "un à plusieurs"


--Transaction_Types - Transactions: Relation (1,n)

---Un type de transaction peut être associé à plusieurs transactions (n)
---Une transaction est d'un seul type (1)
---C'est une relation de type "un à plusieurs"


--Accounts - Transactions (pour recipient_account_id): Relation (0,n)

---Un compte peut être destinataire de plusieurs transferts (n)
---Une transaction de type transfert a un seul compte destinataire (1)
---Cette relation est optionnelle (0) car seules les transactions de type transfert ont un compte destinataire
---C'est une relation de type "zéro ou un à plusieurs"
