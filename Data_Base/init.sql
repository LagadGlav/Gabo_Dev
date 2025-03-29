DROP DATABASE IF EXISTS Gabo_base;
CREATE DATABASE Gabo_base;
USE Gabo_base;

DROP TABLE IF EXISTS Joueurs;
DROP TABLE if exists Partie;


CREATE TABLE Joueurs (
                         joueur_id INT PRIMARY KEY,
                         joueur_nom VARCHAR(50),
                         nombre_partie INT DEFAULT 0,
                         score_total INT DEFAULT 0,
                         ratio_score FLOAT DEFAULT 0,
                         ratio_rang FLOAT DEFAULT 0,
                         elo FLOAT DEFAULT 500
);

CREATE TABLE Partie (
                        partie_id INT,
                        nombre_joueur INT,
                        joueur_id INT,
                        joueur_score INT,
                        rang INT,
                        date_partie DATETIME DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT id PRIMARY KEY (partie_id, joueur_id),
                        FOREIGN KEY (joueur_id) REFERENCES Joueurs(joueur_id) ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER after_insert_partie
    AFTER INSERT ON Partie
    FOR EACH ROW
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            -- Handle the exception by rolling back the parent statement
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error in after_insert_partie trigger';
        END;

    -- Perform updates without transaction control
    UPDATE Joueurs
    SET nombre_partie = nombre_partie + 1
    WHERE joueur_id = NEW.joueur_id;

    UPDATE Joueurs
    SET score_total = score_total + NEW.joueur_score
    WHERE joueur_id = NEW.joueur_id;

    UPDATE Joueurs
    SET ratio_score = IF(nombre_partie > 0, score_total / nombre_partie, 0)
    WHERE joueur_id = NEW.joueur_id;

    UPDATE Joueurs
    SET ratio_rang = IF(nombre_partie > 0, (ratio_rang * (nombre_partie - 1) + NEW.rang / NEW.nombre_joueur) / nombre_partie, 0)
    WHERE joueur_id = NEW.joueur_id;
END;
//

CREATE TRIGGER after_delete_partie
    AFTER DELETE ON Partie
    FOR EACH ROW
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            -- Handle the exception by rolling back the parent statement
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error in after_delete_partie trigger';
        END;

    -- Perform updates without transaction control
    UPDATE Joueurs
    SET nombre_partie = nombre_partie - 1
    WHERE joueur_id = OLD.joueur_id;

    UPDATE Joueurs
    SET score_total = score_total - OLD.joueur_score
    WHERE joueur_id = OLD.joueur_id;

    UPDATE Joueurs
    SET ratio_score = IF(nombre_partie > 0, score_total / nombre_partie, 0)
    WHERE joueur_id = OLD.joueur_id;

    UPDATE Joueurs
    SET ratio_rang = 1
    WHERE joueur_id = OLD.joueur_id;
END;
//

DELIMITER ;
