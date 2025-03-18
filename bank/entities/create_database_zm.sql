-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_financiere;
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

-- Table des comptes ,  relation 1:N avec utilisateurs (un utilisateur peut avoir plusieurs comptes)
CREATE TABLE IF NOT EXISTS comptes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    libelle VARCHAR(100) NOT NULL,
    solde DECIMAL(15, 2) DEFAULT 0.00,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    est_actif BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table des catégories de transactions
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    description TEXT,
    icone VARCHAR(50) DEFAULT NULL
);

-- Table des transactions
-- - Relation N:1 avec comptes (un compte peut avoir plusieurs transactions)
-- - Relation N:1 avec categories (une catégorie peut concerner plusieurs transactions)
-- - Relation avec elle-même pour les transferts (compte source vers compte destination)
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
    FOREIGN KEY (categorie_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (compte_destination_id) REFERENCES comptes(id) ON DELETE SET NULL
);

-- Table des alertes
 -- - relation N:1 avec utilisateurs (un utilisateur peut avoir plusieurs alertes)
CREATE TABLE IF NOT EXISTS alertes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    type ENUM('decouvert', 'budget_depasse', 'transaction_suspecte', 'rappel_facture', 'autre') NOT NULL,
    message TEXT NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    est_lue BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table des préférences utilisateur
-- - Table dépendante de utilisateurs avec relation 1:1 (un utilisateur a exactement une ligne de préférences)
CREATE TABLE IF NOT EXISTS preferences_utilisateur (
    utilisateur_id INT PRIMARY KEY,
    theme VARCHAR(20) DEFAULT 'light',
    notifications_email BOOLEAN DEFAULT TRUE,
    notifications_app BOOLEAN DEFAULT TRUE,
    budget_mensuel DECIMAL(15, 2) DEFAULT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table des sessions utilisateur
-- relation N:1 avec utilisateurs (un utilisateur peut avoir plusieurs sessions)
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
-- - Table de relation N:N entre utilisateurs et catégories avec attributs
-- - (un utilisateur peut définir plusieurs budgets par catégorie et une catégorie peut être budgétée par plusieurs utilisateurs)
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    categorie_id INT NOT NULL,
    montant DECIMAL(15, 2) NOT NULL,
    periode ENUM('mensuel', 'trimestriel', 'annuel') DEFAULT 'mensuel',
    date_debut DATE NOT NULL,
    date_fin DATE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (categorie_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Table des tentatives de connexion (pour la sécurité)
-- -Table principale (entité) sans clé étrangère explicite mais liée conceptuellement aux utilisateurs via l'email
CREATE TABLE IF NOT EXISTS tentatives_connexion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    date_tentative DATETIME DEFAULT CURRENT_TIMESTAMP,
    reussie BOOLEAN DEFAULT FALSE
);

-- Insertion des catégories de base
INSERT INTO categories (nom, description, icone) VALUES
('Alimentation', 'Dépenses alimentaires, courses, restaurants', 'food'),
('Logement', 'Loyer, prêt immobilier, charges', 'home'),
('Transport', 'Essence, transports en commun, entretien véhicule', 'car'),
('Loisirs', 'Sorties, voyages, activités culturelles', 'entertainment'),
('Santé', 'Frais médicaux, médicaments, assurance santé', 'health'),
('Éducation', 'Frais de scolarité, livres, formations', 'education'),
('Vêtements', 'Achats de vêtements et accessoires', 'clothing'),
('Services', 'Abonnements, télécommunications, services publics', 'services'),
('Revenus', 'Salaires, primes, revenus divers', 'income'),
('Épargne', 'Économies, investissements', 'savings'),
('Cadeaux', 'Cadeaux offerts ou reçus', 'gift'),
('Impôts', 'Impôts et taxes', 'tax'),
('Divers', 'Dépenses diverses non catégorisées', 'misc');

-- Procédure stockée pour créer un nouvel utilisateur avec vérification de mot de passe
DELIMITER //
CREATE PROCEDURE creer_utilisateur(
    IN p_nom VARCHAR(100),
    IN p_prenom VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_mot_de_passe VARCHAR(255),
    OUT p_utilisateur_id INT
)
BEGIN
    DECLARE est_valide BOOLEAN DEFAULT FALSE;
    
    -- Vérification du mot de passe (au moins 10 caractères, une majuscule, une minuscule, un chiffre, un caractère spécial)
    IF LENGTH(p_mot_de_passe) >= 10 
       AND p_mot_de_passe REGEXP '[A-Z]' 
       AND p_mot_de_passe REGEXP '[a-z]' 
       AND p_mot_de_passe REGEXP '[0-9]' 
       AND p_mot_de_passe REGEXP '[!@#$%^&*(),.?":{}|<>]' THEN
        SET est_valide = TRUE;
    END IF;
    
    IF est_valide THEN
        -- Insérer l'utilisateur avec le mot de passe haché
        INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe)
        VALUES (p_nom, p_prenom, p_email, SHA2(p_mot_de_passe, 256));
        
        SET p_utilisateur_id = LAST_INSERT_ID();
        
        -- Créer un compte par défaut pour l'utilisateur
        INSERT INTO comptes (utilisateur_id, libelle)
        VALUES (p_utilisateur_id, 'Compte principal');
        
        -- Créer les préférences par défaut
        INSERT INTO preferences_utilisateur (utilisateur_id)
        VALUES (p_utilisateur_id);
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le mot de passe ne respecte pas les critères de sécurité';
    END IF;
END //
DELIMITER ;

-- Procédure stockée pour effectuer un dépôt
DELIMITER //
CREATE PROCEDURE effectuer_depot(
    IN p_compte_id INT,
    IN p_montant DECIMAL(15, 2),
    IN p_description TEXT,
    IN p_categorie_id INT
)
BEGIN
    DECLARE v_reference VARCHAR(50);
    
    -- Générer une référence unique
    SET v_reference = CONCAT('DEP', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s'), FLOOR(RAND() * 1000));
    
    -- Insérer la transaction
    INSERT INTO transactions (reference, compte_id, categorie_id, type, montant, date_transaction, description)
    VALUES (v_reference, p_compte_id, p_categorie_id, 'depot', p_montant, NOW(), p_description);
    
    -- Mettre à jour le solde du compte
    UPDATE comptes SET solde = solde + p_montant WHERE id = p_compte_id;
END //
DELIMITER ;

-- Procédure stockée pour effectuer un retrait
DELIMITER //
CREATE PROCEDURE effectuer_retrait(
    IN p_compte_id INT,
    IN p_montant DECIMAL(15, 2),
    IN p_description TEXT,
    IN p_categorie_id INT
)
BEGIN
    DECLARE v_reference VARCHAR(50);
    DECLARE v_solde DECIMAL(15, 2);
    DECLARE v_utilisateur_id INT;
    
    -- Récupérer le solde actuel et l'ID de l'utilisateur
    SELECT solde, utilisateur_id INTO v_solde, v_utilisateur_id FROM comptes WHERE id = p_compte_id;
    
    -- Générer une référence unique
    SET v_reference = CONCAT('RET', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s'), FLOOR(RAND() * 1000));
    
    -- Insérer la transaction
    INSERT INTO transactions (reference, compte_id, categorie_id, type, montant, date_transaction, description)
    VALUES (v_reference, p_compte_id, p_categorie_id, 'retrait', p_montant, NOW(), p_description);
    
    -- Mettre à jour le solde du compte
    UPDATE comptes SET solde = solde - p_montant WHERE id = p_compte_id;
    
    -- Vérifier si le compte est à découvert après le retrait
    IF (v_solde - p_montant) < 0 THEN
        INSERT INTO alertes (utilisateur_id, type, message)
        VALUES (v_utilisateur_id, 'decouvert', CONCAT('Attention : votre compte est à découvert de ', ABS(v_solde - p_montant), ' €'));
    END IF;
END //
DELIMITER ;

-- Procédure stockée pour effectuer un transfert
DELIMITER //
CREATE PROCEDURE effectuer_transfert(
    IN p_compte_source_id INT,
    IN p_compte_destination_id INT,
    IN p_montant DECIMAL(15, 2),
    IN p_description TEXT
)
BEGIN
    DECLARE v_reference VARCHAR(50);
    DECLARE v_solde DECIMAL(15, 2);
    DECLARE v_utilisateur_id INT;
    
    -- Récupérer le solde actuel et l'ID de l'utilisateur
    SELECT solde, utilisateur_id INTO v_solde, v_utilisateur_id FROM comptes WHERE id = p_compte_source_id;
    
    -- Générer une référence unique
    SET v_reference = CONCAT('TRF', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s'), FLOOR(RAND() * 1000));
    
    -- Insérer la transaction
    INSERT INTO transactions (reference, compte_id, type, montant, date_transaction, description, compte_destination_id)
    VALUES (v_reference, p_compte_source_id, 'transfert', p_montant, NOW(), p_description, p_compte_destination_id);
    
    -- Mettre à jour les soldes des comptes
    UPDATE comptes SET solde = solde - p_montant WHERE id = p_compte_source_id;
    UPDATE comptes SET solde = solde + p_montant WHERE id = p_compte_destination_id;
    
    -- Vérifier si le compte source est à découvert après le transfert
    IF (v_solde - p_montant) < 0 THEN
        INSERT INTO alertes (utilisateur_id, type, message)
        VALUES (v_utilisateur_id, 'decouvert', CONCAT('Attention : votre compte est à découvert de ', ABS(v_solde - p_montant), ' €'));
    END IF;
END //
DELIMITER ;

-- Procédure stockée pour récupérer l'historique des transactions
DELIMITER //
CREATE PROCEDURE obtenir_historique(
    IN p_utilisateur_id INT,
    IN p_date_debut DATE,
    IN p_date_fin DATE,
    IN p_categorie_id INT,
    IN p_type VARCHAR(20),
    IN p_tri VARCHAR(20),
    IN p_ordre VARCHAR(4)
)
BEGIN
    DECLARE where_clause VARCHAR(500) DEFAULT ' WHERE c.utilisateur_id = p_utilisateur_id';
    DECLARE order_clause VARCHAR(100) DEFAULT ' ORDER BY t.date_transaction DESC';
    
    -- Construction de la clause WHERE
    IF p_date_debut IS NOT NULL THEN
        SET where_clause = CONCAT(where_clause, ' AND DATE(t.date_transaction) >= ''', p_date_debut, '''');
    END IF;
    
    IF p_date_fin IS NOT NULL THEN
        SET where_clause = CONCAT(where_clause, ' AND DATE(t.date_transaction) <= ''', p_date_fin, '''');
    END IF;
    
    IF p_categorie_id IS NOT NULL THEN
        SET where_clause = CONCAT(where_clause, ' AND t.categorie_id = ', p_categorie_id);
    END IF;
    
    IF p_type IS NOT NULL THEN
        SET where_clause = CONCAT(where_clause, ' AND t.type = ''', p_type, '''');
    END IF;
    
    -- Construction de la clause ORDER
    IF p_tri = 'montant' THEN
        IF p_ordre = 'ASC' THEN
            SET order_clause = ' ORDER BY t.montant ASC';
        ELSE
            SET order_clause = ' ORDER BY t.montant DESC';
        END IF;
    ELSEIF p_tri = 'date' THEN
        IF p_ordre = 'ASC' THEN
            SET order_clause = ' ORDER BY t.date_transaction ASC';
        ELSE
            SET order_clause = ' ORDER BY t.date_transaction DESC';
        END IF;
    END IF;
    
    -- Exécution de la requête dynamique
    SET @sql = CONCAT('
        SELECT t.id, t.reference, t.type, t.montant, t.date_transaction, t.description,
               c.libelle AS compte_nom, cat.nom AS categorie_nom,
               cd.libelle AS compte_destination_nom
        FROM transactions t
        JOIN comptes c ON t.compte_id = c.id
        LEFT JOIN categories cat ON t.categorie_id = cat.id
        LEFT JOIN comptes cd ON t.compte_destination_id = cd.id',
        where_clause,
        order_clause
    );
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Procédure stockée pour le récapitulatif mensuel
DELIMITER //
CREATE PROCEDURE obtenir_recap_mensuel(
    IN p_utilisateur_id INT,
    IN p_annee INT,
    IN p_mois INT
)
BEGIN
    DECLARE debut_mois DATE;
    DECLARE fin_mois DATE;
    
    SET debut_mois = CONCAT(p_annee, '-', LPAD(p_mois, 2, '0'), '-01');
    SET fin_mois = LAST_DAY(debut_mois);
    
    -- Récapitulatif des dépenses par catégorie
    SELECT cat.nom AS categorie, SUM(t.montant) AS total_depenses
    FROM transactions t
    JOIN comptes c ON t.compte_id = c.id
    JOIN categories cat ON t.categorie_id = cat.id
    WHERE c.utilisateur_id = p_utilisateur_id
    AND t.type = 'retrait'
    AND t.date_transaction BETWEEN debut_mois AND fin_mois
    GROUP BY cat.nom
    ORDER BY total_depenses DESC;
    
    -- Récapitulatif des revenus
    SELECT SUM(t.montant) AS total_revenus
    FROM transactions t
    JOIN comptes c ON t.compte_id = c.id
    WHERE c.utilisateur_id = p_utilisateur_id
    AND t.type = 'depot'
    AND t.date_transaction BETWEEN debut_mois AND fin_mois;
    
    -- Solde total des comptes
    SELECT SUM(solde) AS solde_total
    FROM comptes
    WHERE utilisateur_id = p_utilisateur_id
    AND est_actif = TRUE;
    
    -- Évolution du solde sur le mois
    SELECT 
        DATE(t.date_transaction) AS jour,
        SUM(CASE WHEN t.type = 'depot' THEN t.montant ELSE 0 END) AS revenus,
        SUM(CASE WHEN t.type = 'retrait' THEN t.montant ELSE 0 END) AS depenses
    FROM transactions t
    JOIN comptes c ON t.compte_id = c.id
    WHERE c.utilisateur_id = p_utilisateur_id
    AND t.date_transaction BETWEEN debut_mois AND fin_mois
    GROUP BY DATE(t.date_transaction)
    ORDER BY jour;
END //
DELIMITER ;

-- Procédure stockée pour vérifier le dépassement de budget
DELIMITER //
CREATE PROCEDURE verifier_budgets(IN p_utilisateur_id INT)
BEGIN
    DECLARE v_categorie_id INT;
    DECLARE v_montant DECIMAL(15, 2);
    DECLARE v_periode VARCHAR(20);
    DECLARE v_date_debut DATE;
    DECLARE v_date_fin DATE;
    DECLARE v_depenses DECIMAL(15, 2);
    DECLARE v_nom_categorie VARCHAR(50);
    DECLARE done INT DEFAULT FALSE;
    
    -- Curseur pour parcourir les budgets de l'utilisateur
    DECLARE cur CURSOR FOR 
        SELECT b.categorie_id, b.montant, b.periode, b.date_debut, b.date_fin, cat.nom
        FROM budgets b
        JOIN categories cat ON b.categorie_id = cat.id
        WHERE b.utilisateur_id = p_utilisateur_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    budget_loop: LOOP
        FETCH cur INTO v_categorie_id, v_montant, v_periode, v_date_debut, v_date_fin, v_nom_categorie;
        
        IF done THEN
            LEAVE budget_loop;
        END IF;
        
        -- Calculer les dépenses pour la période et la catégorie
        SELECT COALESCE(SUM(t.montant), 0) INTO v_depenses
        FROM transactions t
        JOIN comptes c ON t.compte_id = c.id
        WHERE c.utilisateur_id = p_utilisateur_id
        AND t.categorie_id = v_categorie_id
        AND t.type = 'retrait'
        AND t.date_transaction BETWEEN v_date_debut AND COALESCE(v_date_fin, NOW());
        
        -- Vérifier si le budget est dépassé
        IF v_depenses > v_montant THEN
            INSERT INTO alertes (utilisateur_id, type, message)
            VALUES (p_utilisateur_id, 'budget_depasse', 
                    CONCAT('Budget dépassé pour la catégorie ', v_nom_categorie, 
                           '. Budget: ', v_montant, ' €, Dépenses: ', v_depenses, ' €'));
        END IF;
    END LOOP;
    
    CLOSE cur;
END //
DELIMITER ;

-- Trigger pour vérifier les budgets après chaque transaction
DELIMITER //
CREATE TRIGGER verifier_budgets_apres_transaction
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE v_utilisateur_id INT;
    
    -- Récupérer l'ID de l'utilisateur
    SELECT utilisateur_id INTO v_utilisateur_id
    FROM comptes
    WHERE id = NEW.compte_id;
    
    -- Vérifier les budgets si c'est un retrait
    IF NEW.type = 'retrait' THEN
        CALL verifier_budgets(v_utilisateur_id);
    END IF;
END //
DELIMITER ;

-- Vues pour faciliter les requêtes fréquentes

-- Vue pour le solde total par utilisateur
CREATE VIEW vue_solde_total AS
SELECT 
    u.id AS utilisateur_id,
    u.nom,
    u.prenom,
    SUM(c.solde) AS solde_total
FROM utilisateurs u
JOIN comptes c ON u.id = c.utilisateur_id
WHERE c.est_actif = TRUE
GROUP BY u.id, u.nom, u.prenom;

-- Vue pour le récapitulatif des dépenses par catégorie et par mois
CREATE VIEW vue_depenses_par_categorie_mois AS
SELECT 
    c.utilisateur_id,
    YEAR(t.date_transaction) AS annee,
    MONTH(t.date_transaction) AS mois,
    cat.nom AS categorie,
    SUM(t.montant) AS total_depenses
FROM transactions t
JOIN comptes c ON t.compte_id = c.id
JOIN categories cat ON t.categorie_id = cat.id
WHERE t.type = 'retrait'
GROUP BY c.utilisateur_id, YEAR(t.date_transaction), MONTH(t.date_transaction), cat.nom;

-- Vue pour les alertes non lues
CREATE VIEW vue_alertes_non_lues AS
SELECT 
    a.id,
    a.utilisateur_id,
    u.nom,
    u.prenom,
    a.type,
    a.message,
    a.date_creation
FROM alertes a
JOIN utilisateurs u ON a.utilisateur_id = u.id
WHERE a.est_lue = FALSE
ORDER BY a.date_creation DESC;

-- Vue pour les transactions récentes
CREATE VIEW vue_transactions_recentes AS
SELECT 
    t.id,
    t.reference,
    c.utilisateur_id,
    t.type,
    t.montant,
    t.date_transaction,
    t.description,
    cat.nom AS categorie,
    c.libelle AS compte_nom
FROM transactions t
JOIN comptes c ON t.compte_id = c.id
LEFT JOIN categories cat ON t.categorie_id = cat.id
ORDER BY t.date_transaction DESC;

-- Fonction pour calculer le solde à une date donnée
DELIMITER //
CREATE FUNCTION calculer_solde_a_date(p_compte_id INT, p_date DATE) RETURNS DECIMAL(15, 2)
DETERMINISTIC
BEGIN
    DECLARE v_solde_initial DECIMAL(15, 2);
    DECLARE v_transactions DECIMAL(15, 2);
    
    -- Récupérer le solde actuel
    SELECT solde INTO v_solde_initial FROM comptes WHERE id = p_compte_id;
    
    -- Calculer les transactions après la date spécifiée
    SELECT 
        COALESCE(SUM(
            CASE 
                WHEN type = 'depot' THEN -montant
                WHEN type = 'retrait' THEN montant
                WHEN type = 'transfert' AND compte_id = p_compte_id THEN montant
                WHEN type = 'transfert' AND compte_destination_id = p_compte_id THEN -montant
                ELSE 0
            END
        ), 0) INTO v_transactions
    FROM transactions
    WHERE (compte_id = p_compte_id OR compte_destination_id = p_compte_id)
    AND date_transaction > p_date;
    
    -- Retourner le solde à la date spécifiée
    RETURN v_solde_initial - v_transactions;
END //
DELIMITER ;

-- Fonction pour vérifier si un mot de passe est valide
DELIMITER //
CREATE FUNCTION est_mot_de_passe_valide(p_mot_de_passe VARCHAR(255)) RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE est_valide BOOLEAN DEFAULT FALSE;
    
    -- Vérification du mot de passe (au moins 10 caractères, une majuscule, une minuscule, un chiffre, un caractère spécial)
    IF LENGTH(p_mot_de_passe) >= 10 
       AND p_mot_de_passe REGEXP '[A-Z]' 
       AND p_mot_de_passe REGEXP '[a-z]' 
       AND p_mot_de_passe REGEXP '[0-9]' 
       AND p_mot_de_passe REGEXP '[!@#$%^&*(),.?":{}|<>]' THEN
        SET est_valide = TRUE;
    END IF;
    
    RETURN est_valide;
END //
DELIMITER ;

-- Événement pour purger les anciennes tentatives de connexion
DELIMITER //
CREATE EVENT purger_tentatives_connexion
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    DELETE FROM tentatives_connexion 
    WHERE date_tentative < DATE_SUB(NOW(), INTERVAL 30 DAY);
END //
DELIMITER ;

-- Événement pour purger les anciennes sessions expirées
DELIMITER //
CREATE EVENT purger_sessions_expirees
ON SCHEDULE EVERY 1 HOUR
DO
BEGIN
    DELETE FROM sessions 
    WHERE date_expiration < NOW();
END //
DELIMITER ;

-- Créer un utilisateur de test avec un mot de passe fort
CALL creer_utilisateur('Dupont', 'Jean', 'jean.dupont@example.com', 'P@ssw0rd123!', @id);

-- Insérer quelques transactions de test
CALL effectuer_depot(@id, 5000.00, 'Salaire de janvier', 9);
CALL effectuer_retrait(@id, 120.50, 'Courses supermarché', 1);
CALL effectuer_retrait(@id, 45.00, 'Restaurant', 1);
CALL effectuer_retrait(@id, 800.00, 'Loyer', 2);
CALL effectuer_retrait(@id, 60.00, 'Abonnement internet', 8);