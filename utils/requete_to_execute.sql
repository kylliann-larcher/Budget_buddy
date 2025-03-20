INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES
('LARCHER', 'Kylliann', 'kylliann.larcher@example.com', 'password123'),
('MAANANE', 'Zakaria', 'zakaria.maanane@example.com', 'password123'),
('ACHART', 'Axel', 'axel.achart@example.com', 'password123');


INSERT INTO comptes (utilisateur_id, libelle, solde) VALUES
((SELECT id FROM utilisateurs WHERE email = 'kylliann.larcher@example.com'), 'Compte Kylliann', 3000.00),
((SELECT id FROM utilisateurs WHERE email = 'zakaria.maanane@example.com'), 'Compte Zakaria', 3500.00),
((SELECT id FROM utilisateurs WHERE email = 'axel.achart@example.com'), 'Compte Axel', 4000.00);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    type ENUM('revenu', 'depense') NOT NULL
);

INSERT INTO categories (nom, type) VALUES
('Salaire', 'revenu'),
('Vente d\'objet', 'revenu'),
('Investissements', 'revenu'),
('Alimentation', 'depense'),
('Loyer', 'depense'),
('Transport', 'depense'),
('Loisirs', 'depense'),
('Santé', 'depense');

INSERT INTO transactions (reference, compte_id, categorie_id, type, montant, date_transaction, description) VALUES
('TXN001', 1, (SELECT id FROM categories WHERE nom='Salaire'), 'depot', 2500.00, '2024-03-01', 'Salaire mensuel'),
('TXN002', 1, (SELECT id FROM categories WHERE nom='Loyer'), 'retrait', -900.00, '2024-03-03', 'Paiement du loyer'),
('TXN003', 1, (SELECT id FROM categories WHERE nom='Alimentation'), 'retrait', -200.00, '2024-03-05', 'Courses alimentaires'),
('TXN004', 1, (SELECT id FROM categories WHERE nom='Transport'), 'retrait', -50.00, '2024-03-07', 'Ticket de transport'),
('TXN005', 1, (SELECT id FROM categories WHERE nom='Loisirs'), 'retrait', -100.00, '2024-03-10', 'Sortie entre amis'),
('TXN006', 1, (SELECT id FROM categories WHERE nom='Investissements'), 'depot', 500.00, '2024-03-12', 'Achat d\'actions');


INSERT INTO transactions (reference, compte_id, categorie_id, type, montant, date_transaction, description) VALUES
-- 📅 Jour 1
('TXN001', 1, (SELECT id FROM categories WHERE nom='Salaire'), 'depot', 2500.00, '2024-03-01', 'Salaire Kylliann'),
('TXN002', 2, (SELECT id FROM categories WHERE nom='Salaire'), 'depot', 2300.00, '2024-03-01', 'Salaire Zakaria'),
('TXN003', 3, (SELECT id FROM categories WHERE nom='Salaire'), 'depot', 2200.00, '2024-03-01', 'Salaire Axel'),

-- 📅 Jour 2
('TXN004', 1, (SELECT id FROM categories WHERE nom='Loyer'), 'retrait', -900.00, '2024-03-02', 'Loyer Kylliann'),
('TXN005', 2, (SELECT id FROM categories WHERE nom='Loyer'), 'retrait', -850.00, '2024-03-02', 'Loyer Zakaria'),
('TXN006', 3, (SELECT id FROM categories WHERE nom='Loyer'), 'retrait', -800.00, '2024-03-02', 'Loyer Axel'),

-- 📅 Jour 3
('TXN007', 1, (SELECT id FROM categories WHERE nom='Alimentation'), 'retrait', -50.00, '2024-03-03', 'Courses alimentaires'),
('TXN008', 2, (SELECT id FROM categories WHERE nom='Alimentation'), 'retrait', -60.00, '2024-03-03', 'Courses alimentaires'),
('TXN009', 3, (SELECT id FROM categories WHERE nom='Alimentation'), 'retrait', -55.00, '2024-03-03', 'Courses alimentaires'),

-- 📅 Jour 4
('TXN010', 1, (SELECT id FROM categories WHERE nom='Transport'), 'retrait', -20.00, '2024-03-04', 'Ticket de transport'),
('TXN011', 2, (SELECT id FROM categories WHERE nom='Transport'), 'retrait', -25.00, '2024-03-04', 'Ticket de transport'),
('TXN012', 3, (SELECT id FROM categories WHERE nom='Transport'), 'retrait', -18.00, '2024-03-04', 'Ticket de transport'),

-- 📅 Jour 5
('TXN013', 1, (SELECT id FROM categories WHERE nom='Loisirs'), 'retrait', -100.00, '2024-03-05', 'Cinéma et sortie'),
('TXN014', 2, (SELECT id FROM categories WHERE nom='Loisirs'), 'retrait', -80.00, '2024-03-05', 'Concert'),
('TXN015', 3, (SELECT id FROM categories WHERE nom='Loisirs'), 'retrait', -90.00, '2024-03-05', 'Théâtre'),

-- 📅 Jour 6
('TXN016', 1, (SELECT id FROM categories WHERE nom='Investissements'), 'depot', 300.00, '2024-03-06', 'Achat d\'actions'),
('TXN017', 2, (SELECT id FROM categories WHERE nom='Investissements'), 'depot', 200.00, '2024-03-06', 'Crypto-monnaie'),
('TXN018', 3, (SELECT id FROM categories WHERE nom='Investissements'), 'depot', 250.00, '2024-03-06', 'Bourse'),

-- 📅 Jour 7
('TXN019', 1, (SELECT id FROM categories WHERE nom='Santé'), 'retrait', -80.00, '2024-03-07', 'Médecin'),
('TXN020', 2, (SELECT id FROM categories WHERE nom='Santé'), 'retrait', -50.00, '2024-03-07', 'Dentiste'),
('TXN021', 3, (SELECT id FROM categories WHERE nom='Santé'), 'retrait', -70.00, '2024-03-07', 'Pharmacie'),

-- 📅 Jour 8
('TXN022', 1, (SELECT id FROM categories WHERE nom='Vente d\'objet'), 'depot', 150.00, '2024-03-08', 'Vente sur eBay'),
('TXN023', 2, (SELECT id FROM categories WHERE nom='Vente d\'objet'), 'depot', 200.00, '2024-03-08', 'Vente de PC'),
('TXN024', 3, (SELECT id FROM categories WHERE nom='Vente d\'objet'), 'depot', 180.00, '2024-03-08', 'Vente de vêtements'),

-- 📅 Jour 9
('TXN025', 1, (SELECT id FROM categories WHERE nom='Alimentation'), 'retrait', -30.00, '2024-03-09', 'Petit-déjeuner'),
('TXN026', 2, (SELECT id FROM categories WHERE nom='Alimentation'), 'retrait', -40.00, '2024-03-09', 'Déjeuner'),
('TXN027', 3, (SELECT id FROM categories WHERE nom='Alimentation'), 'retrait', -35.00, '2024-03-09', 'Dîner'),

-- 📅 Jour 10
('TXN028', 1, (SELECT id FROM categories WHERE nom='Transport'), 'retrait', -15.00, '2024-03-10', 'Essence'),
('TXN029', 2, (SELECT id FROM categories WHERE nom='Transport'), 'retrait', -20.00, '2024-03-10', 'Essence'),
('TXN030', 3, (SELECT id FROM categories WHERE nom='Transport'), 'retrait', -18.00, '2024-03-10', 'Essence');
