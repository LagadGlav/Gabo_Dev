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
(10,'Amaz',15,1009,67.2667,0.57,526),
(11,'Drey',3,227,75.6667,0.527778,499),
(12,'Lou',18,1472,81.7778,0.674074,459),
(13,'Baptiste',22,1849,84.0455,0.7,424),
(14,'Margot',36,2178,60.5,0.404167,586),
(15,'Harold',12,1006,83.8333,0.691667,459),
(16,'Nathan',3,180,60,0.5,506),
(17,'Maël',36,3200,88.8889,0.762037,393),
(18,'Goran',15,1107,73.8,0.658889,507),
(19,'Emma',1,101,101,1,494),
(20,'Tobias',1,52,52,0.666667,501),
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
(9,6,17,45,4,3,'2025-05-04 13:28:42'),
(11,4,13,82,2,1,'2025-06-10 21:27:57'),
(11,4,14,72,1,3,'2025-06-10 21:27:57'),
(11,4,17,104,4,-3,'2025-06-10 21:27:57'),
(11,4,18,104,3,-3,'2025-06-10 21:27:57'),
(13,4,13,63,2,2,'2025-06-10 21:30:45'),
(13,4,14,57,1,3,'2025-06-10 21:30:45'),
(13,4,17,110,4,-7,'2025-06-10 21:30:45'),
(13,4,18,76,3,0,'2025-06-10 21:30:45'),
(14,3,13,63,2,1,'2025-06-12 12:35:20'),
(14,3,14,51,1,3,'2025-06-12 12:35:20'),
(14,3,17,110,3,-6,'2025-06-12 12:35:20'),
(15,5,13,120,5,-12,'2025-06-12 12:36:32'),
(15,5,14,52,1,5,'2025-06-12 12:36:32'),
(15,5,15,71,3,1,'2025-06-12 12:36:32'),
(15,5,17,68,2,2,'2025-06-12 12:36:32'),
(15,5,18,82,4,-2,'2025-06-12 12:36:32'),
(16,3,14,40,1,4,'2025-06-12 12:38:08'),
(16,3,17,107,3,-6,'2025-06-12 12:38:08'),
(16,3,18,78,2,-1,'2025-06-12 12:38:08'),
(17,3,14,52,1,2,'2025-06-12 12:39:29'),
(17,3,17,53,2,2,'2025-06-12 12:39:29'),
(17,3,18,100,3,-5,'2025-06-12 12:39:29'),
(19,5,10,17,1,12,'2025-06-12 12:40:59'),
(19,5,12,113,5,-11,'2025-06-12 12:40:59'),
(19,5,14,66,2,1,'2025-06-12 12:40:59'),
(19,5,15,88,4,-5,'2025-06-12 12:40:59'),
(19,5,17,83,3,-4,'2025-06-12 12:40:59'),
(20,3,10,104,3,-4,'2025-06-12 12:41:43'),
(20,3,14,65,2,1,'2025-06-12 12:41:43'),
(20,3,17,59,1,3,'2025-06-12 12:41:43'),
(21,5,10,53,2,2,'2025-06-12 12:43:10'),
(21,5,13,109,5,-13,'2025-06-12 12:43:10'),
(21,5,14,6,1,13,'2025-06-12 12:43:10'),
(21,5,15,78,3,-4,'2025-06-12 12:43:10'),
(21,5,17,97,4,-9,'2025-06-12 12:43:10'),
(22,5,10,113,5,-9,'2025-06-12 12:44:15'),
(22,5,13,63,2,3,'2025-06-12 12:44:15'),
(22,5,14,77,3,-1,'2025-06-12 12:44:15'),
(22,5,15,82,4,-2,'2025-06-12 12:44:15'),
(22,5,17,33,1,11,'2025-06-12 12:44:15'),
(23,5,10,47,1,5,'2025-06-12 12:45:11'),
(23,5,12,85,4,-4,'2025-06-12 12:45:11'),
(23,5,14,55,2,3,'2025-06-12 12:45:11'),
(23,5,15,106,5,-9,'2025-06-12 12:45:11'),
(23,5,17,77,3,-2,'2025-06-12 12:45:11'),
(24,4,14,71,2,2,'2025-06-12 12:46:10'),
(24,4,15,113,4,-7,'2025-06-12 12:46:10'),
(24,4,17,98,3,-3,'2025-06-12 12:46:10'),
(24,4,18,58,1,5,'2025-06-12 12:46:10'),
(25,4,14,38,2,1,'2025-06-12 12:46:54'),
(25,4,15,71,4,-6,'2025-06-12 12:46:54'),
(25,4,17,31,1,3,'2025-06-12 12:46:54'),
(25,4,18,51,3,-1,'2025-06-12 12:46:54'),
(26,4,10,112,3,-3,'2025-06-12 12:47:39'),
(26,4,12,101,2,-1,'2025-06-12 12:47:39'),
(26,4,14,69,1,5,'2025-06-12 12:47:39'),
(26,4,17,118,4,-5,'2025-06-12 12:47:39'),
(27,4,10,101,4,-5,'2025-06-12 12:48:37'),
(27,4,12,85,3,-3,'2025-06-12 12:48:37'),
(27,4,14,34,1,6,'2025-06-12 12:48:37'),
(27,4,17,85,2,-3,'2025-06-12 12:48:37'),
(28,4,12,93,3,-5,'2025-06-12 12:49:28'),
(28,4,13,46,2,5,'2025-06-12 12:49:28'),
(28,4,14,45,1,4,'2025-06-12 12:49:28'),
(28,4,17,113,4,-9,'2025-06-12 12:49:28'),
(29,4,14,72,1,3,'2025-06-12 12:51:02'),
(29,4,15,86,2,1,'2025-06-12 12:51:02'),
(29,4,17,99,3,-2,'2025-06-12 12:51:02'),
(29,4,18,117,4,-5,'2025-06-12 12:51:02'),
(30,3,14,129,3,-5,'2025-06-12 12:51:37'),
(30,3,17,113,2,-4,'2025-06-12 12:51:37'),
(30,3,18,39,1,8,'2025-06-12 12:51:37'),
(31,6,12,70,5,-3,'2025-06-12 12:53:00'),
(31,6,13,42,1,6,'2025-06-12 12:53:00'),
(31,6,14,51,3,2,'2025-06-12 12:53:00'),
(31,6,15,50,2,3,'2025-06-12 12:53:00'),
(31,6,17,103,6,-14,'2025-06-12 12:53:00'),
(31,6,18,58,4,0,'2025-06-12 12:53:00'),
(32,6,12,70,4,1,'2025-06-12 12:54:28'),
(32,6,13,138,6,-20,'2025-06-12 12:54:28'),
(32,6,14,48,2,6,'2025-06-12 12:54:28'),
(32,6,15,121,5,-14,'2025-06-12 12:54:28'),
(32,6,17,56,3,6,'2025-06-12 12:54:28'),
(32,6,18,30,1,12,'2025-06-12 12:54:28'),
(33,3,12,98,2,-2,'2025-06-12 13:20:31'),
(33,3,14,67,1,2,'2025-06-12 13:20:31'),
(33,3,17,113,3,-4,'2025-06-12 13:20:31'),
(34,4,13,63,2,2,'2025-06-12 13:21:24'),
(34,4,14,57,1,2,'2025-06-12 13:21:24'),
(34,4,17,110,4,-9,'2025-06-12 13:21:24'),
(34,4,18,76,3,-1,'2025-06-12 13:21:24'),
(35,4,13,82,2,1,'2025-06-12 13:22:06'),
(35,4,14,72,1,2,'2025-06-12 13:22:06'),
(35,4,17,104,3,-4,'2025-06-12 13:22:06'),
(35,4,18,104,4,-3,'2025-06-12 13:22:06'),
(36,3,14,74,2,0,'2025-06-12 13:45:26'),
(36,3,17,113,3,-7,'2025-06-12 13:45:26'),
(36,3,18,55,1,3,'2025-06-12 13:45:26'),
(37,3,14,72,1,1,'2025-06-12 13:46:09'),
(37,3,17,102,3,-4,'2025-06-12 13:46:09'),
(37,3,18,79,2,0,'2025-06-12 13:46:09'),
(38,3,12,119,3,-7,'2025-06-12 13:47:29'),
(38,3,14,52,1,2,'2025-06-12 13:47:29'),
(38,3,17,75,2,0,'2025-06-12 13:47:29'),
(39,3,12,16,1,8,'2025-06-12 13:48:02'),
(39,3,14,78,2,-1,'2025-06-12 13:48:02'),
(39,3,17,119,3,-9,'2025-06-12 13:48:02'),
(40,4,12,111,4,-8,'2025-06-12 13:49:22'),
(40,4,13,93,3,-5,'2025-06-12 13:49:22'),
(40,4,14,42,1,4,'2025-06-12 13:49:22'),
(40,4,17,55,2,4,'2025-06-12 13:49:22'),
(41,4,12,20,1,7,'2025-06-12 13:50:16'),
(41,4,13,104,4,-11,'2025-06-12 13:50:16'),
(41,4,14,47,2,1,'2025-06-12 13:50:16'),
(41,4,17,64,3,-2,'2025-06-12 13:50:16'),
(42,3,10,50,1,4,'2025-06-12 13:51:15'),
(42,3,14,100,2,-2,'2025-06-12 13:51:15'),
(42,3,17,113,3,-6,'2025-06-12 13:51:15'),
(43,3,10,108,3,-6,'2025-06-12 13:52:49'),
(43,3,14,45,2,2,'2025-06-12 13:52:49'),
(43,3,17,41,1,4,'2025-06-12 13:52:49'),
(44,3,13,27,1,6,'2025-06-15 18:39:58'),
(44,3,19,101,3,-6,'2025-06-15 18:39:58'),
(44,3,20,52,2,1,'2025-06-15 18:39:58'),
(45,4,12,86,2,1,'2025-06-16 20:33:15'),
(45,4,13,94,3,-1,'2025-06-16 20:33:15'),
(45,4,14,85,1,1,'2025-06-16 20:33:15'),
(45,4,17,113,4,-5,'2025-06-16 20:33:15'),
(46,4,12,59,1,6,'2025-06-16 21:30:09'),
(46,4,13,111,3,-5,'2025-06-16 21:30:09'),
(46,4,14,83,2,0,'2025-06-16 21:30:09'),
(46,4,17,114,4,-6,'2025-06-16 21:30:09');
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

-- Dump completed on 2025-06-23 21:27:45
