/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.11-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: data_base    Database: Gabo_base
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Joueurs`
--

DROP TABLE IF EXISTS `Joueurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Joueurs` (
  `joueur_id` int NOT NULL,
  `joueur_nom` varchar(50) DEFAULT NULL,
  `nombre_partie` int DEFAULT '0',
  `score_total` int DEFAULT '0',
  `ratio_score` float DEFAULT '0',
  `ratio_rang` float DEFAULT '0',
  `elo` float DEFAULT '500',
  PRIMARY KEY (`joueur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Joueurs`
--

LOCK TABLES `Joueurs` WRITE;
/*!40000 ALTER TABLE `Joueurs` DISABLE KEYS */;
INSERT INTO `Joueurs` VALUES
(1,'Marco',0,0,0,0,500),
(2,'Gervor',0,0,0,0,500),
(3,'Andrée',0,0,0,0,500);
/*!40000 ALTER TABLE `Joueurs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Partie`
--

DROP TABLE IF EXISTS `Partie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Partie` (
  `partie_id` int NOT NULL,
  `nombre_joueur` int DEFAULT NULL,
  `joueur_id` int NOT NULL,
  `joueur_score` int DEFAULT NULL,
  `rang` int DEFAULT NULL,
  `var_elo` float DEFAULT NULL,
  `date_partie` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`partie_id`,`joueur_id`),
  KEY `joueur_id` (`joueur_id`),
  CONSTRAINT `Partie_ibfk_1` FOREIGN KEY (`joueur_id`) REFERENCES `Joueurs` (`joueur_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Partie`
--

LOCK TABLES `Partie` WRITE;
/*!40000 ALTER TABLE `Partie` DISABLE KEYS */;
/*!40000 ALTER TABLE `Partie` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_partie` AFTER INSERT ON `Partie` FOR EACH ROW BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error in after_insert_partie trigger';
        END;

    
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

    UPDATE Joueurs
    SET elo = elo + NEW.var_elo
    WHERE joueur_id = NEW.joueur_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_delete_partie` AFTER DELETE ON `Partie` FOR EACH ROW BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error in after_delete_partie trigger';
        END;

    
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-03 21:04:41
