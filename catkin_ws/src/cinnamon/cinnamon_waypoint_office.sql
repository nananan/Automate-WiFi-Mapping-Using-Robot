-- MySQL dump 10.15  Distrib 10.0.36-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: cinnamon
-- ------------------------------------------------------
-- Server version	10.0.36-MariaDB-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `APs`
--

DROP TABLE IF EXISTS `APs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `APs` (
  `access_point_name` varchar(150) DEFAULT NULL,
  `access_point_address` varchar(30) NOT NULL,
  `channel` int(2) DEFAULT NULL,
  `type` varchar(50) NOT NULL,
  `subtype` varchar(50) NOT NULL,
  `strength` varchar(6) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`access_point_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `APs`
--

LOCK TABLES `APs` WRITE;
/*!40000 ALTER TABLE `APs` DISABLE KEYS */;
/*!40000 ALTER TABLE `APs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EAP`
--

DROP TABLE IF EXISTS `EAP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EAP` (
  `BSSID` varchar(30) NOT NULL,
  `source` varchar(30) NOT NULL,
  `destination` varchar(30) NOT NULL,
  `channel` varchar(5) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `strength` varchar(6) DEFAULT NULL,
  `encrypted` char(1) DEFAULT NULL,
  `to_ds` varchar(10) DEFAULT NULL,
  `from_ds` varchar(10) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EAP`
--

LOCK TABLES `EAP` WRITE;
/*!40000 ALTER TABLE `EAP` DISABLE KEYS */;
/*!40000 ALTER TABLE `EAP` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Packets`
--

DROP TABLE IF EXISTS `Packets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Packets` (
  `BSSID` varchar(30) NOT NULL,
  `source` varchar(30) NOT NULL,
  `destination` varchar(30) NOT NULL,
  `channel` varchar(5) DEFAULT NULL,
  `type` varchar(50) NOT NULL,
  `subtype` varchar(50) NOT NULL,
  `strength` varchar(6) DEFAULT NULL,
  `encrypted` char(1) DEFAULT NULL,
  `to_ds` varchar(10) DEFAULT NULL,
  `from_ds` varchar(10) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Packets`
--

LOCK TABLES `Packets` WRITE;
/*!40000 ALTER TABLE `Packets` DISABLE KEYS */;
/*!40000 ALTER TABLE `Packets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Waypoints`
--

DROP TABLE IF EXISTS `Waypoints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Waypoints` (
  `id_waypoint` int(11) NOT NULL AUTO_INCREMENT,
  `position_x` float NOT NULL,
  `position_y` float NOT NULL,
  `position_z` float NOT NULL,
  `orientation_x` float NOT NULL,
  `orientation_y` float NOT NULL,
  `orientation_z` float NOT NULL,
  `orientation_w` float NOT NULL,
  PRIMARY KEY (`id_waypoint`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Waypoints`
--

LOCK TABLES `Waypoints` WRITE;
/*!40000 ALTER TABLE `Waypoints` DISABLE KEYS */;
INSERT INTO `Waypoints` VALUES (2,0.982275,-0.0891954,0,0,0,0,1),(3,1.02084,0.799337,0,0,0,0.705737,0.708474),(4,1.66029,0.809369,0,0,0,0,1);
/*!40000 ALTER TABLE `Waypoints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Waypoints_AP`
--

DROP TABLE IF EXISTS `Waypoints_AP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Waypoints_AP` (
  `id_waypoint` int(11) NOT NULL AUTO_INCREMENT,
  `position_x` float NOT NULL,
  `position_y` float NOT NULL,
  `position_z` float NOT NULL,
  `orientation_x` float NOT NULL,
  `orientation_y` float NOT NULL,
  `orientation_z` float NOT NULL,
  `orientation_w` float NOT NULL,
  `AP` varchar(30) NOT NULL,
  `strength` varchar(6) NOT NULL,
  PRIMARY KEY (`id_waypoint`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Waypoints_AP`
--

LOCK TABLES `Waypoints_AP` WRITE;
/*!40000 ALTER TABLE `Waypoints_AP` DISABLE KEYS */;
/*!40000 ALTER TABLE `Waypoints_AP` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-14 12:05:26
