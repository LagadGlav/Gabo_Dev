/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.11-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: data_base    Database: Gabo_base
-- ------------------------------------------------------
-- Server version	8.0.42

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
(1,'Marco',14,1169,83.5,0.815476,10),
(2,'Gervor',13,446,34.3077,0.602564,10),
(3,'Andrée',13,572,44,0.532052,10),
(5,'Louis',0,0,0,0,500),
(10,'Amaz',6,304,50.6667,0.444444,530),
(11,'Drey',3,227,75.6667,0.527778,499),
(12,'Lou',4,346,86.5,0.708333,480),
(13,'Baptiste',6,549,91.5,0.847222,464),
(14,'Margot',3,154,51.3333,0.361111,511),
(15,'Harold',2,140,70,0.416667,501),
(16,'Nathan',3,180,60,0.5,506),
(17,'Maël',3,247,82.3333,0.805556,491);
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
INSERT INTO `Partie` VALUES
(0,3,1,17,1,7,'2025-04-04 18:11:26'),
(0,3,2,28,2,4,'2025-04-04 18:11:26'),
(0,3,3,135,3,-11,'2025-04-04 18:11:26'),
(1,3,1,17,1,7,'2025-04-04 18:11:26'),
(1,3,2,28,2,4,'2025-04-04 18:11:26'),
(1,3,3,135,3,-11,'2025-04-04 18:11:26'),
(3,4,10,46,1,7,'2025-05-04 12:56:44'),
(3,4,11,90,3,-2,'2025-05-04 12:56:44'),
(3,4,12,88,2,-2,'2025-05-04 12:56:44'),
(3,4,13,104,4,-5,'2025-05-04 12:56:44'),
(4,4,10,103,4,-7,'2025-05-04 13:01:12'),
(4,4,13,55,2,3,'2025-05-04 13:01:12'),
(4,4,14,38,1,6,'2025-05-04 13:01:12'),
(4,4,17,87,3,-4,'2025-05-04 13:01:12'),
(6,4,10,36,1,8,'2025-05-04 13:10:31'),
(6,4,13,88,3,-2,'2025-05-04 13:10:31'),
(6,4,14,77,2,0,'2025-05-04 13:10:31'),
(6,4,17,115,4,-8,'2025-05-04 13:10:31'),
(7,6,10,75,5,-4,'2025-05-04 13:24:36'),
(7,6,11,44,2,5,'2025-05-04 13:24:36'),
(7,6,12,51,3,3,'2025-05-04 13:24:36'),
(7,6,13,105,6,-13,'2025-05-04 13:24:36'),
(7,6,15,41,1,6,'2025-05-04 13:24:36'),
(7,6,16,67,4,-1,'2025-05-04 13:24:36'),
(8,6,10,26,1,16,'2025-05-04 13:26:30'),
(8,6,11,93,3,-4,'2025-05-04 13:26:30'),
(8,6,12,102,5,-6,'2025-05-04 13:26:30'),
(8,6,13,104,6,-7,'2025-05-04 13:26:30'),
(8,6,15,99,4,-5,'2025-05-04 13:26:30'),
(8,6,16,71,2,3,'2025-05-04 13:26:30'),
(9,6,10,18,1,10,'2025-05-04 13:28:42'),
(9,6,12,105,6,-15,'2025-05-04 13:28:42'),
(9,6,13,93,5,-12,'2025-05-04 13:28:42'),
(9,6,14,39,2,5,'2025-05-04 13:28:42'),
(9,6,16,42,3,4,'2025-05-04 13:28:42'),
(9,6,17,45,4,3,'2025-05-04 13:28:42');
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

-- Dump completed on 2025-06-06 17:40:13
