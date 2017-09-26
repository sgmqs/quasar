# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: quasar.c9ajz690mens.us-east-1.rds.amazonaws.com (MySQL 5.7.17-log)
# Database: gladiator
# Generation Time: 2017-09-25 15:50:02 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table competitions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `competitions`;

CREATE TABLE `competitions` (
  `id` int(11) NOT NULL,
  `leaderboard_msg_day` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rules` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `competition_dates_start` datetime DEFAULT NULL,
  `competition_dates_end` datetime DEFAULT NULL,
  `contest_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`contest_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table contest
# ------------------------------------------------------------

DROP TABLE IF EXISTS `contest`;

CREATE TABLE `contest` (
  `id` int(11) NOT NULL,
  `campaign_id` int(11) NOT NULL,
  `campaign_run_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `sender_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sender_email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`,`campaign_id`,`campaign_run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table messages
# ------------------------------------------------------------

DROP TABLE IF EXISTS `messages`;

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `contest_id` int(11) NOT NULL,
  `label` text COLLATE utf8mb4_unicode_ci,
  `subject` text COLLATE utf8mb4_unicode_ci,
  `body` text COLLATE utf8mb4_unicode_ci,
  `signoff` text COLLATE utf8mb4_unicode_ci,
  `protip` text COLLATE utf8mb4_unicode_ci,
  `show_images` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `type_name` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type_key` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`contest_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contest_id` int(11) NOT NULL,
  `campaign_id` int(11) NOT NULL,
  `subscribed` tinyint(1) DEFAULT NULL,
  `unsubscribed` tinyint(1) DEFAULT NULL,
  `waiting_room_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`contest_id`,`campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table waiting_room
# ------------------------------------------------------------

DROP TABLE IF EXISTS `waiting_room`;

CREATE TABLE `waiting_room` (
  `id` int(11) NOT NULL,
  `open` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `contest_id` int(11) NOT NULL,
  `signup_date_start` datetime DEFAULT NULL,
  `signup_date_end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`contest_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
