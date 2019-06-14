CREATE DATABASE  IF NOT EXISTS `detection` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `detection`;
-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: detection
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `area` (
  `areaID` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(15) NOT NULL,
  `city` varchar(15) NOT NULL,
  `nameOfArea` varchar(20) NOT NULL,
  PRIMARY KEY (`areaID`),
  KEY `nameOfArea` (`nameOfArea`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `detectedobject`
--

DROP TABLE IF EXISTS `detectedobject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `detectedobject` (
  `sightingUrl` varchar(100) NOT NULL,
  `objectNumber` int(11) NOT NULL,
  `property1Value` varchar(20) NOT NULL,
  `property2Value` varchar(20) DEFAULT NULL,
  `objectName` varchar(20) NOT NULL,
  `accuracy` double DEFAULT '50',
  `url` varchar(100) DEFAULT '/resources/wallpaper.jpg',
  PRIMARY KEY (`sightingUrl`,`objectNumber`),
  KEY `objectName` (`objectName`),
  CONSTRAINT `detectedobject_ibfk_2` FOREIGN KEY (`objectName`) REFERENCES `objectkind` (`objectname`) ON UPDATE CASCADE,
  CONSTRAINT `detectedobject_ibfk_3` FOREIGN KEY (`sightingUrl`) REFERENCES `sighting` (`sightingurl`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drone`
--

DROP TABLE IF EXISTS `drone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `drone` (
  `droneID` int(11) NOT NULL AUTO_INCREMENT,
  `specifications` text NOT NULL,
  PRIMARY KEY (`droneID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `isfoundin`
--

DROP TABLE IF EXISTS `isfoundin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `isfoundin` (
  `areaID` int(11) NOT NULL,
  `objectName` varchar(20) NOT NULL,
  PRIMARY KEY (`areaID`,`objectName`),
  KEY `objectName` (`objectName`),
  CONSTRAINT `isfoundin_ibfk_1` FOREIGN KEY (`areaID`) REFERENCES `area` (`areaid`) ON UPDATE CASCADE,
  CONSTRAINT `isfoundin_ibfk_2` FOREIGN KEY (`objectName`) REFERENCES `objectkind` (`objectname`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mission`
--

DROP TABLE IF EXISTS `mission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `mission` (
  `missionID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `droneID` int(11) NOT NULL,
  `pathID` int(11) NOT NULL,
  `startingTimeStamp` datetime DEFAULT NULL,
  `endingTimeStamp` datetime DEFAULT NULL,
  `length` int(11) NOT NULL,
  `numberOfVideos` int(11) NOT NULL,
  `state` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`missionID`),
  KEY `droneID` (`droneID`),
  KEY `username` (`username`),
  KEY `pathID` (`pathID`),
  KEY `startingTimeStamp` (`startingTimeStamp`),
  CONSTRAINT `mission_ibfk_1` FOREIGN KEY (`droneID`) REFERENCES `drone` (`droneid`) ON UPDATE CASCADE,
  CONSTRAINT `mission_ibfk_2` FOREIGN KEY (`username`) REFERENCES `operator` (`username`) ON UPDATE CASCADE,
  CONSTRAINT `mission_ibfk_3` FOREIGN KEY (`pathID`) REFERENCES `path` (`pathid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `objectkind`
--

DROP TABLE IF EXISTS `objectkind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `objectkind` (
  `objectName` varchar(20) NOT NULL,
  `property1` varchar(20) NOT NULL,
  `property2` varchar(20) NOT NULL,
  PRIMARY KEY (`objectName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `operator`
--

DROP TABLE IF EXISTS `operator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `operator` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(20) NOT NULL,
  `e-mail` varchar(30) NOT NULL,
  `address` varchar(60) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `path`
--

DROP TABLE IF EXISTS `path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `path` (
  `pathID` int(11) NOT NULL AUTO_INCREMENT,
  `areaID` int(11) NOT NULL,
  `numberOfSteps` int(11) NOT NULL,
  PRIMARY KEY (`pathID`),
  KEY `areaID` (`areaID`),
  CONSTRAINT `path_ibfk_1` FOREIGN KEY (`areaID`) REFERENCES `area` (`areaid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pathsteps`
--

DROP TABLE IF EXISTS `pathsteps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `pathsteps` (
  `pathID` int(11) NOT NULL,
  `stepNumber` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  PRIMARY KEY (`pathID`,`stepNumber`),
  CONSTRAINT `pathsteps_ibfk_1` FOREIGN KEY (`pathID`) REFERENCES `path` (`pathid`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sighting`
--

DROP TABLE IF EXISTS `sighting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sighting` (
  `sightingUrl` varchar(100) NOT NULL,
  `videoUrl` varchar(100) NOT NULL,
  `timeOfAppearance` int(11) NOT NULL DEFAULT '1',
  `numberOfObjects` int(11) NOT NULL,
  PRIMARY KEY (`sightingUrl`),
  KEY `videoUrl` (`videoUrl`),
  CONSTRAINT `sighting_ibfk_1` FOREIGN KEY (`videoUrl`) REFERENCES `video` (`videourl`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `video` (
  `videoUrl` varchar(100) NOT NULL,
  `missionID` int(11) NOT NULL,
  `videoName` varchar(20) DEFAULT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `startingTime` int(11) DEFAULT '30',
  PRIMARY KEY (`videoUrl`),
  KEY `missionID` (`missionID`),
  CONSTRAINT `video_ibfk_1` FOREIGN KEY (`missionID`) REFERENCES `mission` (`missionid`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-14 17:00:51
