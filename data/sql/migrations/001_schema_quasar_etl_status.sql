# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: quasar.c9ajz690mens.us-east-1.rds.amazonaws.com (MySQL 5.7.17-log)
# Database: quasar_etl_status
# Generation Time: 2017-09-25 15:45:08 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table moco_campaign_messages_list
# ------------------------------------------------------------

DROP TABLE IF EXISTS `moco_campaign_messages_list`;

CREATE TABLE `moco_campaign_messages_list` (
  `campaign_id` int(11) NOT NULL,
  `campaign_scrape_completed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table moco_campaign_messages_page
# ------------------------------------------------------------

DROP TABLE IF EXISTS `moco_campaign_messages_page`;

CREATE TABLE `moco_campaign_messages_page` (
  `last_page` int(11) NOT NULL,
  PRIMARY KEY (`last_page`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table moco_profile_scraper_page
# ------------------------------------------------------------

DROP TABLE IF EXISTS `moco_profile_scraper_page`;

CREATE TABLE `moco_profile_scraper_page` (
  `last_page_scraped` int(11) NOT NULL,
  PRIMARY KEY (`last_page_scraped`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table northstar_ingestion
# ------------------------------------------------------------

DROP TABLE IF EXISTS `northstar_ingestion`;

CREATE TABLE `northstar_ingestion` (
  `counter_name` varchar(32) NOT NULL,
  `counter_value` int(11) DEFAULT NULL,
  PRIMARY KEY (`counter_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table rogue_ingestion
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rogue_ingestion`;

CREATE TABLE `rogue_ingestion` (
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
