CREATE DATABASE budget_buddy_finance;
USE budget_buddy_finance;

CREATE TABLE users (
    id_users        INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    pass_word       VARCHAR(255) NOT NULL,
    date_creation   DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_connection DATETIME DEFAULT NULL
);

CREATE TABLE accounts (
    id_account    INT AUTO_INCREMENT PRIMARY KEY,
    id_users      INT NOT NULL UNIQUE,
    amount        DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_users) REFERENCES users(id_users)
);

CREATE TABLE categories (
    id_category  INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description VARCHAR(255) DEFAULT NULL
);

CREATE TABLE transactions (
    id_transaction         INT AUTO_INCREMENT PRIMARY KEY,
    reference              VARCHAR(50) DEFAULT NULL,
    description            VARCHAR(255) DEFAULT NULL,
    amount                 DECIMAL(15,2) NOT NULL,
    date_transaction       DATETIME DEFAULT CURRENT_TIMESTAMP,
    type_transaction       VARCHAR(10) DEFAULT NULL,
    id_account             INT NOT NULL,
    id_account_destination INT DEFAULT NULL,
    id_category            INT DEFAULT NULL,
    FOREIGN KEY (id_account) REFERENCES accounts(id_account),
    FOREIGN KEY (id_account_destination) REFERENCES accounts(id_account),
    FOREIGN KEY (id_category) REFERENCES categories(id_category)
);
