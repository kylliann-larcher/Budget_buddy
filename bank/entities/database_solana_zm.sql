

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_financiere1;
USE gestion_financiere1;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,  -- Contrainte UNIQUE pour garantir un seul compte par email
    mot_de_passe VARCHAR(255) NOT NULL,  -- Pour stocker le mot de passe haché
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    derniere_connexion DATETIME
);

-- Table des comptes bancaires
CREATE TABLE IF NOT EXISTS comptes (
    id_compte INT PRIMARY KEY AUTO_INCREMENT,
    id_utilisateur INT NOT NULL UNIQUE,  -- Contrainte UNIQUE pour garantir un seul compte par utilisateur
    solde DECIMAL(15, 2) DEFAULT 0.00 NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE
);

-- Table des catégories de transactions
CREATE TABLE IF NOT EXISTS categories (
    id_categorie INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- Insertion des catégories par défaut
INSERT INTO categories (nom, description) VALUES
    ('Loisir', 'Dépenses liées aux loisirs et divertissements'),
    ('Repas', 'Dépenses liées à l''alimentation'),
    ('Pot-de-vin', 'Transactions diverses'),
    ('Factures', 'Paiement de factures'),
    ('Salaire', 'Revenus provenant du travail'),
    ('Autres', 'Autres types de transactions');

-- Table des transactions
CREATE TABLE IF NOT EXISTS transactions (
    id_transaction INT PRIMARY KEY AUTO_INCREMENT,
    reference VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    montant DECIMAL(15, 2) NOT NULL,
    date_transaction DATETIME DEFAULT CURRENT_TIMESTAMP,
    type_transaction ENUM('retrait', 'depot', 'transfert') NOT NULL,
    id_compte INT NOT NULL,
    id_compte_destination INT, -- Pour les transferts uniquement
    id_categorie INT NOT NULL,
    FOREIGN KEY (id_compte) REFERENCES comptes(id_compte) ON DELETE CASCADE,
    FOREIGN KEY (id_compte_destination) REFERENCES comptes(id_compte) ON DELETE SET NULL,
    FOREIGN KEY (id_categorie) REFERENCES categories(id_categorie)
);

-- Créer un index pour améliorer les performances des recherches
CREATE INDEX idx_transactions_date ON transactions(date_transaction);
CREATE INDEX idx_transactions_type ON transactions(type_transaction);
CREATE INDEX idx_transactions_categorie ON transactions(id_categorie);


