# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: quasar-staging.c9ajz690mens.us-east-1.rds.amazonaws.com (MySQL 5.7.17-log)
# Database: quasar
# Generation Time: 2017-07-11 17:31:21 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP DATABASE IF EXISTS quasar;
CREATE DATABASE quasar;
USE quasar;

# Dump of table all_moco_users
# ------------------------------------------------------------

CREATE TABLE `all_moco_users` (
  `phone_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `us_phone_number` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `source_type` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source_name` longtext COLLATE utf8mb4_unicode_ci,
  `opt_in_path_id` bigint(20) DEFAULT NULL,
  `status` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`phone_number`),
  KEY `us_phone_number` (`us_phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table blink_queue_backlog
# ------------------------------------------------------------

CREATE TABLE `blink_queue_backlog` (
  `email` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_io_subscription_status` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_io_subscription_timestamp` datetime NOT NULL,
  PRIMARY KEY (`email`,`customer_io_subscription_status`,`customer_io_subscription_timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table c_io_export_fix_missing
# ------------------------------------------------------------

CREATE TABLE `c_io_export_fix_missing` (
  `id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subscribed_at` varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unsubscribed` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unsubscribed_at` varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`,`email`,`unsubscribed`),
  KEY `unsubscribed_at` (`unsubscribed_at`),
  KEY `id` (`id`),
  KEY `email` (`email`),
  KEY `subscribed_at` (`subscribed_at`),
  KEY `unsubscribed` (`unsubscribed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table campaign_activity
# ------------------------------------------------------------

CREATE TABLE `campaign_activity` (
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
  KEY `campaign_run_id` (`campaign_run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table campaign_activity_orig
# ------------------------------------------------------------

CREATE TABLE `campaign_activity_orig` (
  `northstar_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `signup_id` int(11) DEFAULT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `campaign_run_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `why_participated` text COLLATE utf8mb4_unicode_ci,
  `signup_source` varchar(24) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `signup_created_at` datetime DEFAULT NULL,
  `signup_updated_at` datetime DEFAULT NULL,
  `post_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `url` text COLLATE utf8mb4_unicode_ci,
  `caption` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `remote_addr` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_source` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `submission_created_at` datetime DEFAULT NULL,
  `submission_updated_at` datetime DEFAULT NULL,
  KEY `northstar_id` (`northstar_id`),
  KEY `campaign_id` (`campaign_id`),
  KEY `campaign_run_id` (`campaign_run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# Dump of table campaign_info
# ------------------------------------------------------------

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

CREATE TABLE `users` (
  `northstar_id` varchar(26) COLLATE utf8mb4_unicode_ci NOT NULL,
  `northstar_created_at_timestamp` datetime DEFAULT NULL,
  `last_logged_in` datetime DEFAULT NULL,
  `last_accessed` datetime DEFAULT NULL,
  `drupal_uid` int(24) DEFAULT NULL,
  `northstar_id_source_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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



# Dump of table users_test
# ------------------------------------------------------------

CREATE TABLE `users_test` (
  `northstar_id` varchar(26) COLLATE utf8mb4_unicode_ci NOT NULL,
  `northstar_created_at_timestamp` datetime DEFAULT NULL,
  `last_logged_in` datetime DEFAULT NULL,
  `last_accessed` datetime DEFAULT NULL,
  `drupal_uid` int(24) DEFAULT NULL,
  `northstar_id_source_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
