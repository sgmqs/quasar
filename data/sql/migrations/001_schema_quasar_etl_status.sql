# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: quasar-staging.c9ajz690mens.us-east-1.rds.amazonaws.com (MySQL 5.7.17-log)
# Database: quasar_etl_status
# Generation Time: 2017-07-11 17:32:09 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP DATABASE IF EXISTS quasar_etl_status;
CREATE DATABASE quasar_etl_status;
USE quasar_etl_status;

# Dump of table northstar_ingestion
# ------------------------------------------------------------

CREATE TABLE `northstar_ingestion` (
  `counter_name` varchar(32) NOT NULL,
  `counter_value` int(11) DEFAULT NULL,
  PRIMARY KEY (`counter_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table rogue_ingestion
# ------------------------------------------------------------

CREATE TABLE `rogue_ingestion` (
  `counter_name` varchar(32) NOT NULL,
  `counter_value` int(11) DEFAULT NULL,
  PRIMARY KEY (`counter_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table thor_northstar_ingestion
# ------------------------------------------------------------

CREATE TABLE `thor_northstar_ingestion` (
  `counter_name` varchar(32) NOT NULL,
  `counter_value` int(11) DEFAULT NULL,
  PRIMARY KEY (`counter_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
