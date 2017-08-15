# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: quasar.c9ajz690mens.us-east-1.rds.amazonaws.com (MySQL 5.7.17-log)
# Database: users_and_activities
# Generation Time: 2017-08-15 20:53:53 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP DATABASE IF EXISTS users_and_activities;
CREATE DATABASE users_and_activities;
USE users_and_activities;

# Dump of table action_gender
# ------------------------------------------------------------

DROP TABLE IF EXISTS `action_gender`;

CREATE TABLE `action_gender` (
  `name` varchar(255) CHARACTER SET ucs2 NOT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table action_income
# ------------------------------------------------------------

DROP TABLE IF EXISTS `action_income`;

CREATE TABLE `action_income` (
  `name` varchar(255) CHARACTER SET ucs2 NOT NULL,
  `income_level` varchar(19) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table active_by_month
# ------------------------------------------------------------

DROP TABLE IF EXISTS `active_by_month`;

CREATE TABLE `active_by_month` (
  `date` date NOT NULL,
  `average_active` int(11) DEFAULT NULL,
  `days_in_month` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table all_traffic
# ------------------------------------------------------------

DROP TABLE IF EXISTS `all_traffic`;

CREATE TABLE `all_traffic` (
  `nid` int(11) NOT NULL,
  `date` date NOT NULL,
  `visitors` int(11) DEFAULT NULL,
  `status` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`nid`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_mobile_age
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_mobile_age`;

CREATE TABLE `baseline_mobile_age` (
  `age` bigint(21) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_mobile_gender
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_mobile_gender`;

CREATE TABLE `baseline_mobile_gender` (
  `gender` varchar(6) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_mobile_income
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_mobile_income`;

CREATE TABLE `baseline_mobile_income` (
  `income_level` varchar(19) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_mobile_race
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_mobile_race`;

CREATE TABLE `baseline_mobile_race` (
  `race` varchar(1) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_web_age
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_web_age`;

CREATE TABLE `baseline_web_age` (
  `age` bigint(21) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_web_gender
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_web_gender`;

CREATE TABLE `baseline_web_gender` (
  `gender` varchar(6) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_web_income
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_web_income`;

CREATE TABLE `baseline_web_income` (
  `income_level` varchar(19) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table baseline_web_race
# ------------------------------------------------------------

DROP TABLE IF EXISTS `baseline_web_race`;

CREATE TABLE `baseline_web_race` (
  `race` varchar(1) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table bod
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bod`;

CREATE TABLE `bod` (
  `date` date DEFAULT NULL,
  `total_members_abs` int(11) DEFAULT NULL,
  `new_membrs_abs` int(11) DEFAULT NULL,
  `engaged_members_abs` int(11) DEFAULT NULL,
  `active_members_abs` int(11) DEFAULT NULL,
  `verified_members_abs` int(11) DEFAULT NULL,
  `campaigns_verified_abs` int(11) DEFAULT NULL,
  `sms_game_verified_abs` int(11) DEFAULT NULL,
  `new_members_last_12` int(11) DEFAULT NULL,
  `engaged_members_last_12` int(11) DEFAULT NULL,
  `active_members_last_12` int(11) DEFAULT NULL,
  `verified_members_last_12` int(11) DEFAULT NULL,
  `campaigns_verified_last_12` int(11) DEFAULT NULL,
  `sms_games_verified_last_12` int(11) DEFAULT NULL,
  `new_members_last_12_percent` float DEFAULT NULL,
  `engaged_members_last_12_percent` float DEFAULT NULL,
  `active_members_last_12_percent` float DEFAULT NULL,
  `verified_members_last_12_percent` float DEFAULT NULL,
  `campaigns_verified_last_12_percent` float DEFAULT NULL,
  `sms_games_verified_last_12_percent` float DEFAULT NULL,
  `site_speed` float DEFAULT NULL,
  `avg_conv` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table campaign_master
# ------------------------------------------------------------

DROP TABLE IF EXISTS `campaign_master`;

CREATE TABLE `campaign_master` (
  `nid` int(11) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `alias` varchar(200) DEFAULT NULL,
  `status` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table cause_gender
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cause_gender`;

CREATE TABLE `cause_gender` (
  `name` varchar(255) CHARACTER SET ucs2 NOT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table cause_income
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cause_income`;

CREATE TABLE `cause_income` (
  `name` varchar(255) CHARACTER SET ucs2 NOT NULL,
  `income_level` varchar(19) DEFAULT NULL,
  `count` bigint(21) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table entrances
# ------------------------------------------------------------

DROP TABLE IF EXISTS `entrances`;

CREATE TABLE `entrances` (
  `nid` int(11) NOT NULL,
  `site` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `entrances` int(11) DEFAULT NULL,
  PRIMARY KEY (`nid`,`site`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table list_tracking
# ------------------------------------------------------------

DROP TABLE IF EXISTS `list_tracking`;

CREATE TABLE `list_tracking` (
  `date` date NOT NULL,
  `mobile_created` int(11) DEFAULT NULL,
  `mail_created` int(11) DEFAULT NULL,
  `mobile_opt_out` int(11) DEFAULT NULL,
  `mail_opt_out` int(11) DEFAULT NULL,
  `net` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mailchimp_sub
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mailchimp_sub`;

CREATE TABLE `mailchimp_sub` (
  `email_address` varchar(200) NOT NULL,
  `confirm_time` datetime DEFAULT NULL,
  PRIMARY KEY (`email_address`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mailchimp_sub_daily
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mailchimp_sub_daily`;

CREATE TABLE `mailchimp_sub_daily` (
  `email_address` varchar(200) NOT NULL,
  `confirm_time` datetime DEFAULT NULL,
  PRIMARY KEY (`email_address`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mailchimp_unsub
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mailchimp_unsub`;

CREATE TABLE `mailchimp_unsub` (
  `email_address` varchar(200) NOT NULL,
  `confirm_time` datetime DEFAULT NULL,
  `unsub_time` datetime DEFAULT NULL,
  PRIMARY KEY (`email_address`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mailchimp_unsub_daily
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mailchimp_unsub_daily`;

CREATE TABLE `mailchimp_unsub_daily` (
  `email_address` varchar(200) NOT NULL,
  `confirm_time` datetime DEFAULT NULL,
  `unsub_time` datetime DEFAULT NULL,
  PRIMARY KEY (`email_address`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mob_sub_test
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mob_sub_test`;

CREATE TABLE `mob_sub_test` (
  `phone_number` varchar(20) NOT NULL,
  `campaign_id` int(11) NOT NULL,
  `opt_in_id` int(11) NOT NULL,
  `activated_at` datetime DEFAULT NULL,
  `opted_out_at_campaign` datetime DEFAULT NULL,
  `web_alpha` tinyint(4) DEFAULT NULL,
  `first_seen_campaign` tinyint(4) DEFAULT NULL,
  `been_alpha` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`phone_number`,`campaign_id`,`opt_in_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_campaign_id_lookup
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_campaign_id_lookup`;

CREATE TABLE `mobile_campaign_id_lookup` (
  `opt_in_path_id` bigint(20) NOT NULL,
  `opt_in_path_id_name` varchar(255) DEFAULT NULL,
  `mobile_campaign_id` bigint(20) DEFAULT NULL,
  `mobile_campaign_id_name` varchar(255) DEFAULT NULL,
  `nid` bigint(20) DEFAULT NULL,
  `run_nid` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`opt_in_path_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_campaign_id_lookup_lite
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_campaign_id_lookup_lite`;

CREATE TABLE `mobile_campaign_id_lookup_lite` (
  `mobile_campaign_id` bigint(20) DEFAULT NULL,
  `run_nid` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_campaign_ids
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_campaign_ids`;

CREATE TABLE `mobile_campaign_ids` (
  `nid` int(11) NOT NULL,
  `campaign_id` int(11) NOT NULL,
  `opt_in_id` int(11) NOT NULL,
  `web_alpha` tinyint(4) DEFAULT NULL,
  `campaign_run` int(11) DEFAULT NULL,
  PRIMARY KEY (`nid`,`campaign_id`,`opt_in_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_master_lookup
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_master_lookup`;

CREATE TABLE `mobile_master_lookup` (
  `ms_phone_number` varchar(20) NOT NULL,
  `ms_campaign_id` int(11) NOT NULL,
  `ms_opt_in_id` int(11) NOT NULL,
  `ms_activated_at` datetime DEFAULT NULL,
  `ms_opted_out_at_campaign` datetime DEFAULT NULL,
  `ms_web_alpha` tinyint(4) DEFAULT NULL,
  `ms_first_seen_campaign` tinyint(4) DEFAULT NULL,
  `ms_been_alpha` tinyint(4) DEFAULT NULL,
  `mc_opt_in_path_id` bigint(20) DEFAULT NULL,
  `mc_opt_in_path_id_name` varchar(255) DEFAULT NULL,
  `mc_mobile_campaign_id` bigint(20) DEFAULT NULL,
  `mc_nid` bigint(20) DEFAULT NULL,
  `mc_run_id` bigint(20) DEFAULT NULL,
  `n_nid` int(10) unsigned DEFAULT NULL,
  `n_vid` int(10) unsigned DEFAULT NULL,
  `n_type` varchar(32) CHARACTER SET ucs2 DEFAULT NULL,
  `n_language` varchar(12) CHARACTER SET ucs2 DEFAULT NULL,
  `n_title` varchar(255) CHARACTER SET ucs2 DEFAULT NULL,
  `n_uid` int(11) DEFAULT NULL,
  `n_status` int(11) DEFAULT NULL,
  `n_created` int(11) DEFAULT NULL,
  `n_changed` int(11) DEFAULT NULL,
  `n_comment` int(11) DEFAULT NULL,
  `n_promote` int(11) DEFAULT NULL,
  `n_sticky` int(11) DEFAULT NULL,
  `n_tnid` int(10) unsigned DEFAULT NULL,
  `n_translate` int(11) DEFAULT NULL,
  `n_uuid` varchar(36) CHARACTER SET ucs2 DEFAULT NULL,
  `mu_phone_number` varchar(256) DEFAULT NULL,
  `mu_us_phone_number` bigint(20) DEFAULT NULL,
  `mu_uid` int(11) DEFAULT NULL,
  `mu_created_at` datetime DEFAULT NULL,
  `mu_source_type` varchar(255) DEFAULT NULL,
  `mu_opt_in_path_id` bigint(20) DEFAULT NULL,
  `mu_status` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_master_lookup_lite
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_master_lookup_lite`;

CREATE TABLE `mobile_master_lookup_lite` (
  `ms_phone_number` varchar(20) NOT NULL,
  `ms_activated_at` datetime DEFAULT NULL,
  `mc_run_id` bigint(20) DEFAULT NULL,
  `n_title` varchar(255) CHARACTER SET ucs2,
  `mu_uid` int(11) DEFAULT NULL,
  `mu_created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_subscriptions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_subscriptions`;

CREATE TABLE `mobile_subscriptions` (
  `phone_number` varchar(20) NOT NULL,
  `campaign_id` int(11) NOT NULL,
  `opt_in_id` int(11) NOT NULL,
  `activated_at` datetime DEFAULT NULL,
  `opted_out_at_campaign` datetime DEFAULT NULL,
  `web_alpha` tinyint(4) DEFAULT NULL,
  `first_seen_campaign` tinyint(4) DEFAULT NULL,
  `been_alpha` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`phone_number`,`campaign_id`,`opt_in_id`),
  KEY `campaigns` (`campaign_id`),
  KEY `opt_in_id` (`opt_in_id`),
  KEY `web_alpha` (`web_alpha`),
  KEY `activated_at` (`activated_at`),
  KEY `phone_number` (`phone_number`),
  KEY `campaign_id` (`campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_user_lookup
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_user_lookup`;

CREATE TABLE `mobile_user_lookup` (
  `phone_number` varchar(256) NOT NULL,
  `us_phone_number` bigint(20) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `source_type` varchar(255) DEFAULT NULL,
  `source_name` longtext,
  `opt_in_path_id` bigint(20) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`phone_number`),
  KEY `opt_in_path_id` (`opt_in_path_id`),
  KEY `created_at` (`created_at`),
  KEY `us_phone_number` (`us_phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_users`;

CREATE TABLE `mobile_users` (
  `phone_number` varchar(20) NOT NULL,
  `first_name` varchar(200) DEFAULT NULL,
  `last_name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `status` varchar(18) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `opted_out_at` datetime DEFAULT NULL,
  `source_type` varchar(200) DEFAULT NULL,
  `source_name` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `street2` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `zip` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  `income_level` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_users_back
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_users_back`;

CREATE TABLE `mobile_users_back` (
  `phone_number` varchar(20) NOT NULL,
  `first_name` varchar(200) DEFAULT NULL,
  `last_name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `status` varchar(18) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `opted_out_at` datetime DEFAULT NULL,
  `source_type` varchar(200) DEFAULT NULL,
  `source_name` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `street2` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `zip` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  `income_level` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mobile_users_backfill
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mobile_users_backfill`;

CREATE TABLE `mobile_users_backfill` (
  `phone_number` varchar(20) NOT NULL,
  `first_name` varchar(200) DEFAULT NULL,
  `last_name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `status` varchar(18) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `opted_out_at` datetime DEFAULT NULL,
  `source_type` varchar(200) DEFAULT NULL,
  `source_name` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `street2` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `zip` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table new_by_month
# ------------------------------------------------------------

DROP TABLE IF EXISTS `new_by_month`;

CREATE TABLE `new_by_month` (
  `date` date NOT NULL,
  `average_new` int(11) DEFAULT NULL,
  `days_in_month` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table niche_data_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `niche_data_users`;

CREATE TABLE `niche_data_users` (
  `uid` int(11) NOT NULL,
  `register_date` datetime DEFAULT NULL,
  `first_name` varchar(100) CHARACTER SET ucs2 DEFAULT NULL,
  `last_name` varchar(100) CHARACTER SET ucs2 DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `email` varchar(200) CHARACTER SET ucs2 DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET ucs2 DEFAULT NULL,
  `street1` varchar(200) CHARACTER SET ucs2 DEFAULT NULL,
  `street2` varchar(200) CHARACTER SET ucs2 DEFAULT NULL,
  `city` varchar(200) CHARACTER SET ucs2 DEFAULT NULL,
  `state` varchar(50) CHARACTER SET ucs2 DEFAULT NULL,
  `zip` varchar(20) CHARACTER SET ucs2 DEFAULT NULL,
  `race` varchar(1) CHARACTER SET ucs2 DEFAULT NULL,
  `religion` varchar(33) CHARACTER SET ucs2 DEFAULT NULL,
  `college_name` varchar(200) CHARACTER SET ucs2 DEFAULT NULL,
  `major_name` varchar(200) CHARACTER SET ucs2 DEFAULT NULL,
  `degree_type` varchar(11) CHARACTER SET ucs2 DEFAULT NULL,
  `gpa` float DEFAULT NULL,
  `sat_math` int(11) DEFAULT NULL,
  `sat_verbal` int(11) DEFAULT NULL,
  `sat_writing` int(11) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table reportbacks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `reportbacks`;

CREATE TABLE `reportbacks` (
  `nid` int(11) DEFAULT NULL,
  `reportbacks` int(11) DEFAULT NULL,
  `impact` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `hour` int(11) DEFAULT NULL,
  `week` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table sources
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sources`;

CREATE TABLE `sources` (
  `nid` int(11) NOT NULL,
  `site` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `visitors` int(11) DEFAULT NULL,
  PRIMARY KEY (`nid`,`site`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table test_mobile_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `test_mobile_users`;

CREATE TABLE `test_mobile_users` (
  `phone_number` varchar(20) NOT NULL,
  `first_name` varchar(200) DEFAULT NULL,
  `last_name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `status` varchar(18) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `opted_out_at` datetime DEFAULT NULL,
  `source_type` varchar(200) DEFAULT NULL,
  `source_name` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `street2` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `zip` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  `income_level` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table test_web_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `test_web_users`;

CREATE TABLE `test_web_users` (
  `uid` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  `income_level` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table verified_by_month
# ------------------------------------------------------------

DROP TABLE IF EXISTS `verified_by_month`;

CREATE TABLE `verified_by_month` (
  `date` date NOT NULL,
  `average_verified_web` int(11) DEFAULT NULL,
  `average_verified_sms` int(11) DEFAULT NULL,
  `days_in_month` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table web_signups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `web_signups`;

CREATE TABLE `web_signups` (
  `nid` int(11) DEFAULT NULL,
  `signups` int(11) DEFAULT NULL,
  `new_members` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `hour` int(11) DEFAULT NULL,
  `week` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table web_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `web_users`;

CREATE TABLE `web_users` (
  `uid` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  `income_level` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table web_users_back
# ------------------------------------------------------------

DROP TABLE IF EXISTS `web_users_back`;

CREATE TABLE `web_users_back` (
  `uid` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  `income_level` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table web_users_backfill
# ------------------------------------------------------------

DROP TABLE IF EXISTS `web_users_backfill`;

CREATE TABLE `web_users_backfill` (
  `uid` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `street1` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  `race` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
