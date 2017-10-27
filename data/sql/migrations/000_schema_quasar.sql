# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: quasar.c9ajz690mens.us-east-1.rds.amazonaws.com (MySQL 5.7.17-log)
# Database: quasar
# Generation Time: 2017-09-25 15:42:06 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table campaign_activity
# ------------------------------------------------------------

DROP TABLE IF EXISTS `campaign_activity`;

CREATE TABLE `campaign_activity` (
  `northstar_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `signup_id` int(11) NOT NULL,
  `campaign_id` int(11) NOT NULL,
  `campaign_run_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `why_participated` text COLLATE utf8mb4_unicode_ci,
  `signup_source` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `signup_created_at` datetime NOT NULL,
  `signup_updated_at` datetime NOT NULL,
  `post_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` text COLLATE utf8mb4_unicode_ci,
  `caption` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `remote_addr` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_source` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `submission_created_at` datetime DEFAULT NULL,
  `submission_updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`northstar_id`,`signup_id`,`campaign_id`,`campaign_run_id`,`post_id`),
  UNIQUE KEY `updates` (`northstar_id`,`signup_id`,`signup_created_at`,`signup_updated_at`,`submission_created_at`),
  KEY `northstar_id` (`northstar_id`),
  KEY `campaign_id` (`campaign_id`),
  KEY `campaign_run_id` (`campaign_run_id`),
  KEY `submission_updated_at` (`submission_updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`quasaradm`@`%` */ /*!50003 TRIGGER `log` AFTER INSERT ON `campaign_activity` FOR EACH ROW BEGIN  
INSERT IGNORE INTO campaign_activity_log SELECT * FROM campaign_activity WHERE northstar_id = NEW.northstar_id AND signup_id = NEW.signup_id AND campaign_id = NEW.campaign_id AND campaign_run_id = NEW.campaign_run_id AND post_id = NEW.post_id;
END */;;
DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;


# Dump of table campaign_activity_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `campaign_activity_log`;

CREATE TABLE `campaign_activity_log` (
  `northstar_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `signup_id` int(11) NOT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `campaign_run_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `why_participated` text COLLATE utf8mb4_unicode_ci,
  `signup_source` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `signup_created_at` datetime NOT NULL,
  `signup_updated_at` datetime NOT NULL,
  `post_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `url` text COLLATE utf8mb4_unicode_ci,
  `caption` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `remote_addr` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_source` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `submission_created_at` datetime NOT NULL,
  `submission_updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`northstar_id`,`signup_id`,`signup_created_at`,`signup_updated_at`,`submission_created_at`),
  KEY `northstar_id` (`northstar_id`),
  KEY `campaign_id` (`campaign_id`),
  KEY `campaign_run_id` (`campaign_run_id`),
  KEY `submission_updated_at` (`submission_updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table campaign_info
# ------------------------------------------------------------

DROP TABLE IF EXISTS `campaign_info`;

CREATE TABLE `campaign_info` (
  `campaign_node_id` int(11) DEFAULT NULL,
  `campaign_node_id_title` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_run_id` int(11) NOT NULL,
  `campaign_run_id_title` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_url` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_type` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_language` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `campaign_run_start_date` datetime DEFAULT NULL,
  `campaign_run_end_date` datetime DEFAULT NULL,
  `campaign_created_date` datetime DEFAULT NULL,
  `campaign_action_type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_cause_type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_cta` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_noun` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `campaign_verb` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`campaign_run_id`,`campaign_language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table phoenix_user_log_poc
# ------------------------------------------------------------

DROP TABLE IF EXISTS `phoenix_user_log_poc`;

CREATE TABLE `phoenix_user_log_poc` (
  `uid` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `mail` varchar(254) NOT NULL,
  `created` int(11) NOT NULL,
  `access` int(11) NOT NULL,
  `login` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `timezone` varchar(32) DEFAULT NULL,
  `language` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`uid`,`created`,`access`,`login`),
  KEY `uid-index` (`uid`),
  KEY `mail` (`mail`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `northstar_id` varchar(26) COLLATE utf8mb4_unicode_ci NOT NULL,
  `northstar_created_at_timestamp` datetime DEFAULT NULL,
  `last_logged_in` datetime DEFAULT NULL,
  `last_accessed` datetime DEFAULT NULL,
  `drupal_uid` int(24) DEFAULT NULL,
  `northstar_id_source_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `facebook_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `first_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_street1` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_street2` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_city` varchar(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_state` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_zip` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `language` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `agg_id` int(16) DEFAULT NULL,
  `cgg_id` int(16) DEFAULT NULL,
  `customer_io_subscription_status` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_io_subscription_timestamp` datetime DEFAULT NULL,
  `mailchimp_first_subscribed` datetime DEFAULT NULL,
  `mailchimp_unsubscribed_time` datetime DEFAULT NULL,
  `mailchimp_subscription_status` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mailchimp_list_id` varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mailchimp_avg_open_rate` float DEFAULT NULL,
  `mailchimp_avg_click_rate` float DEFAULT NULL,
  `mailchimp_latitude` float DEFAULT NULL,
  `mailchimp_longitude` float DEFAULT NULL,
  `mailchimp_country_code` varchar(4) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moco_commons_profile_id` varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moco_current_status` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moco_source_detail` varchar(96) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`northstar_id`),
  KEY `drupal_uid` (`drupal_uid`),
  KEY `cgg_id` (`cgg_id`),
  KEY `agg_id` (`agg_id`),
  KEY `email` (`email`),
  KEY `mobile` (`mobile`),
  KEY `customer_io_subscription_status` (`customer_io_subscription_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `userlog` AFTER UPDATE ON `users` FOR EACH ROW BEGIN  
INSERT IGNORE INTO users_log SELECT * FROM users WHERE northstar_id = NEW.northstar_id;
END */;;
DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;


# Dump of table users_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users_log`;

CREATE TABLE `users_log` (
  `northstar_id` varchar(26) COLLATE utf8mb4_unicode_ci NOT NULL,
  `northstar_created_at_timestamp` datetime DEFAULT NULL,
  `last_logged_in` datetime NOT NULL,
  `last_accessed` datetime NOT NULL,
  `drupal_uid` int(24) DEFAULT NULL,
  `northstar_id_source_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `facebook_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `first_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_street1` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_street2` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_city` varchar(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_state` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `addr_zip` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `language` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `agg_id` int(16) DEFAULT NULL,
  `cgg_id` int(16) DEFAULT NULL,
  `customer_io_subscription_status` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_io_subscription_timestamp` datetime DEFAULT NULL,
  `mailchimp_first_subscribed` datetime DEFAULT NULL,
  `mailchimp_unsubscribed_time` datetime DEFAULT NULL,
  `mailchimp_subscription_status` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mailchimp_list_id` varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mailchimp_avg_open_rate` float DEFAULT NULL,
  `mailchimp_avg_click_rate` float DEFAULT NULL,
  `mailchimp_latitude` float DEFAULT NULL,
  `mailchimp_longitude` float DEFAULT NULL,
  `mailchimp_country_code` varchar(4) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moco_commons_profile_id` varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moco_current_status` varchar(48) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moco_source_detail` varchar(96) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`northstar_id`,`last_logged_in`,`last_accessed`),
  KEY `drupal_uid` (`drupal_uid`),
  KEY `cgg_id` (`cgg_id`),
  KEY `agg_id` (`agg_id`),
  KEY `email` (`email`),
  KEY `mobile` (`mobile`),
  KEY `customer_io_subscription_status` (`customer_io_subscription_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
