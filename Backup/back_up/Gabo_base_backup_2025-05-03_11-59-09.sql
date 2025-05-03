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
(1,'Marco',14,1169,83.5,0.815476,435.172),
(2,'Gervor',13,446,34.3077,0.602564,533.86),
(3,'Andrée',13,572,44,0.532052,520.568),
(10,'Nathan',1,104,104,1,492),
(11,'Baptiste',1,54,54,0.666667,500),
(12,'Lou',0,0,0,0,500),
(13,'Pauline',1,12,12,0.333333,506),
(14,'Marcel',1,104,104,1,490),
(15,'Jack',1,104,104,1,493);
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
(3,3,3,53,2,0.75,'2025-04-04 17:15:38'),
(4,3,1,104,3,-6.9,'2025-04-04 17:15:38'),
(5,3,3,18,1,5.25,'2025-04-04 17:15:38'),
(6,3,2,37,2,2.4,'2025-04-04 17:15:38'),
(7,3,1,104,3,-7.65,'2025-04-04 17:15:38'),
(8,3,1,18,1,7.37016,'2025-04-04 17:16:46'),
(9,3,3,74,2,-1.24909,'2025-04-04 17:16:46'),
(10,3,2,102,3,-5.40977,'2025-04-04 17:16:46'),
(11,3,2,17,1,5.73078,'2025-04-04 17:17:42'),
(12,3,3,46,2,1.33455,'2025-04-04 17:17:42'),
(13,3,1,103,3,-7.29944,'2025-04-04 17:17:42'),
(14,3,3,17,1,5.48422,'2025-04-04 17:19:06'),
(15,3,2,47,2,1.09945,'2025-04-04 17:19:06'),
(16,3,1,102,3,-7.38728,'2025-04-04 17:19:06'),
(17,3,2,17,1,4.03977,'2025-04-04 17:20:07'),
(18,3,3,17,2,3.99874,'2025-04-04 17:20:07'),
(19,3,1,102,3,-8.96148,'2025-04-04 17:20:07'),
(20,3,1,17,1,7,'2025-04-04 18:58:31'),
(20,3,2,28,2,4,'2025-04-04 18:58:31'),
(20,3,3,135,3,-11,'2025-04-04 18:58:31'),
(22,3,1,130,3,-13,'2025-04-04 19:12:21'),
(22,3,2,18,2,4,'2025-04-04 19:12:21'),
(22,3,3,14,1,5,'2025-04-04 19:12:21'),
(23,3,1,130,3,-13,'2025-04-04 19:12:25'),
(23,3,2,18,2,4,'2025-04-04 19:12:25'),
(23,3,3,14,1,5,'2025-04-04 19:12:25'),
(24,3,1,130,3,-13,'2025-04-04 19:12:31'),
(24,3,2,18,2,4,'2025-04-04 19:12:31'),
(24,3,3,14,1,5,'2025-04-04 19:12:31'),
(26,3,1,52,2,0,'2025-04-05 19:51:24'),
(26,3,2,17,1,5,'2025-04-05 19:51:23'),
(26,3,15,104,3,-7,'2025-04-05 19:51:24'),
(28,3,10,104,3,-8,'2025-04-05 21:38:59'),
(28,3,11,54,2,0,'2025-04-05 21:38:59'),
(28,3,13,12,1,6,'2025-04-05 21:38:59'),
(30,3,1,105,3,-9,'2025-04-06 13:31:23'),
(30,3,2,51,2,0,'2025-04-06 13:31:23'),
(30,3,3,17,1,5,'2025-04-06 13:31:23'),
(32,4,1,55,3,0,'2025-04-08 20:01:20'),
(32,4,2,48,2,1,'2025-04-08 20:01:20'),
(32,4,3,18,1,7,'2025-04-08 20:01:20'),
(32,4,14,104,4,-10,'2025-04-08 20:01:20');
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

-- Dump completed on 2025-05-03 11:59:09
