CREATE TABLE Joueurs (
                        joueur_id INT AUTO_INCREMENT PRIMARY KEY,
                        joueur_nom VARCHAR(50),

                        nombre_partie INT DEFAULT 0,
                        score_total INT DEFAULT 0,
                        ratio_score FLOAT DEFAULT 0,
                        ratio_rang FLOAT DEFAULT 0,
                        elo FLOAT DEFAULT 500
);

CREATE TABLE Partie (
                        partie_id INT PRIMARY KEY,
                        nombre_joueur INT,

                        joueur_id INT,
                        joueur_score INT,
                        rang int,

                        date_partie DATETIME DEFAULT CURRENT_TIMESTAMP,

                        FOREIGN KEY (joueur_id) REFERENCES Joueurs(joueur_id) ON DELETE CASCADE
                            id_game, nb_joueurs, id_joueur, score, rang
);

CREATE TRIGGER after_insert_partie
AFTER INSERT ON Partie
FOR EACH ROW
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- Annule toutes les opérations si une erreur survient
    END;

    START TRANSACTION;
        UPDATE Joueurs SET nombre_partie = nombre_partie + 1 WHERE joueur_id = NEW.joueur_id;
        UPDATE Joueurs SET Joueurs.score_total = score_total  + NEW.joueur_score WHERE joueur_id = NEW.joueur_id;
        UPDATE Joueurs SET Joueurs.ratio_score = IF(nombre_partie > 0, score_total / nombre_partie, 0) WHERE joueur_id = NEW.joueur_id;
        UPDATE Joueurs SET Joueurs.ratio_rang  = IF(nombre_partie > 0, (ratio_rang * (nombre_partie -1) + NEW.rang / NEW.nombre_joueur) / nombre_partie, 0) WHERE joueur_id = NEW.joueur_id;
    COMMIT;
END;

CREATE TRIGGER after_delete_partie
AFTER DELETE ON Partie
FOR EACH ROW
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION

    BEGIN
        ROLLBACK; -- Annule toutes les opérations si une erreur survient
    END;

    START TRANSACTION;
        UPDATE Joueurs SET nombre_partie = nombre_partie - 1 WHERE joueur_id = OLD.joueur_id;
        UPDATE Joueurs SET Joueurs.score_total = score_total  - OLD.joueur_score WHERE joueur_id = OLD.joueur_id;
        UPDATE Joueurs SET Joueurs.ratio_score = IF(nombre_partie > 0, score_total / nombre_partie, 0) WHERE joueur_id = OLD.joueur_id;
        UPDATE Joueurs SET Joueurs.ratio_rang  = 1 WHERE joueur_id = OLD.joueur_id;
    COMMIT;
END;
