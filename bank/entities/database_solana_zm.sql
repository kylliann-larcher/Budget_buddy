-- Création de la base de données
CREATE DATABASE IF NOT EXISTS database_solana;
USE gestion_financiere;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL, -- Pour stocker le hash du mot de passe
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP,
    derniere_connexion DATETIME DEFAULT NULL,
    CONSTRAINT check_email_format CHECK (email REGEXP '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$')
);

-- Table des comptes, relation 1:N avec utilisateurs (un utilisateur peut avoir plusieurs comptes)
CREATE TABLE IF NOT EXISTS comptes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    libelle VARCHAR(100) NOT NULL,
    solde DECIMAL(15, 2) DEFAULT 0.00,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    est_actif BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table des transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(50) NOT NULL UNIQUE,
    compte_id INT NOT NULL,
    categorie_id INT,
    type ENUM('retrait', 'depot', 'transfert') NOT NULL,
    montant DECIMAL(15, 2) NOT NULL,
    date_transaction DATETIME NOT NULL,
    description TEXT,
    compte_destination_id INT DEFAULT NULL, -- Pour les transferts
    FOREIGN KEY (compte_id) REFERENCES comptes(id) ON DELETE CASCADE,
    FOREIGN KEY (compte_destination_id) REFERENCES comptes(id) ON DELETE SET NULL
);

-- Table des sessions utilisateur
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(255) PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_expiration DATETIME NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table des budgets par catégorie
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    categorie_id INT NOT NULL,
    montant DECIMAL(15, 2) NOT NULL,
    periode ENUM('mensuel', 'trimestriel', 'annuel') DEFAULT 'mensuel',
    date_debut DATE NOT NULL,
    date_fin DATE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);