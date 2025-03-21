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
