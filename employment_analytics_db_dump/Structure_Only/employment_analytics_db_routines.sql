-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: employment_analytics_db
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `company_summary_view`
--

DROP TABLE IF EXISTS `company_summary_view`;
/*!50001 DROP VIEW IF EXISTS `company_summary_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `company_summary_view` AS SELECT 
 1 AS `company_id`,
 1 AS `company_name`,
 1 AS `industry`,
 1 AS `company_size`,
 1 AS `verified`,
 1 AS `registration_date`,
 1 AS `total_jobs`,
 1 AS `total_skills`,
 1 AS `City`,
 1 AS `sub_category_name`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `job_detailed_view`
--

DROP TABLE IF EXISTS `job_detailed_view`;
/*!50001 DROP VIEW IF EXISTS `job_detailed_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `job_detailed_view` AS SELECT 
 1 AS `job_id`,
 1 AS `job_title`,
 1 AS `job_type`,
 1 AS `status`,
 1 AS `posted_date`,
 1 AS `expiry_date`,
 1 AS `main_category_id`,
 1 AS `sub_category_id`,
 1 AS `main_category_name`,
 1 AS `sub_category_name`,
 1 AS `company_id`,
 1 AS `company_name`,
 1 AS `industry`,
 1 AS `company_size`,
 1 AS `verified`,
 1 AS `registration_date`,
 1 AS `area`,
 1 AS `city`,
 1 AS `country`,
 1 AS `min_salary`,
 1 AS `max_salary`,
 1 AS `currency`,
 1 AS `period`,
 1 AS `source_type`,
 1 AS `scraped_from`,
 1 AS `hard_skill_corpus`,
 1 AS `soft_skill_corpus`,
 1 AS `combine_skill_corpus`,
 1 AS `share_link`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `job_skill_flattened_view`
--

DROP TABLE IF EXISTS `job_skill_flattened_view`;
/*!50001 DROP VIEW IF EXISTS `job_skill_flattened_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `job_skill_flattened_view` AS SELECT 
 1 AS `job_id`,
 1 AS `job_title`,
 1 AS `main_category_name`,
 1 AS `sub_category_name`,
 1 AS `company_industry`,
 1 AS `skill_name`,
 1 AS `skill_type`,
 1 AS `posted_date`,
 1 AS `min_salary`,
 1 AS `max_salary`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `job_skills_view`
--

DROP TABLE IF EXISTS `job_skills_view`;
/*!50001 DROP VIEW IF EXISTS `job_skills_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `job_skills_view` AS SELECT 
 1 AS `job_id`,
 1 AS `combine_skill_corpus`,
 1 AS `soft_skills`,
 1 AS `hard_skills`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `job_hard&soft_skill`
--

DROP TABLE IF EXISTS `job_hard&soft_skill`;
/*!50001 DROP VIEW IF EXISTS `job_hard&soft_skill`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `job_hard&soft_skill` AS SELECT 
 1 AS `job_id`,
 1 AS `title`,
 1 AS `share_link`,
 1 AS `main_category_name`,
 1 AS `sub_category_name`,
 1 AS `hard_skill_corpus`,
 1 AS `soft_skill_corpus`,
 1 AS `combine_skill_corpus`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `company_summary_view`
--

/*!50001 DROP VIEW IF EXISTS `company_summary_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `company_summary_view` AS select `cmp`.`company_id` AS `company_id`,`cmp`.`name` AS `company_name`,`cmp`.`industry` AS `industry`,`cmp`.`company_size` AS `company_size`,`cmp`.`verified` AS `verified`,`cmp`.`registration_date` AS `registration_date`,count(`j`.`job_id`) AS `total_jobs`,count(distinct `js`.`skill_name`) AS `total_skills`,`lcn`.`city` AS `City`,`sc`.`name` AS `sub_category_name` from ((((((`company` `cmp` left join `jobs` `j` on((`cmp`.`company_id` = `j`.`company_id`))) left join `jobs_skill` `js` on((`j`.`job_id` = `js`.`job_id`))) left join `jobs_source` `src` on((`j`.`job_id` = `src`.`job_id`))) left join `location` `lcn` on((`j`.`job_id` = `lcn`.`job_id`))) left join `classification` `csf` on((`j`.`job_id` = `csf`.`job_id`))) left join `sub_category` `sc` on((`csf`.`sub_category_id` = `sc`.`sub_category_id`))) where ((`src`.`source_type` = 'scraping') and (`src`.`scraped_from` = 'jobsdb')) group by `cmp`.`company_id`,`lcn`.`city`,`sc`.`name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `job_detailed_view`
--

/*!50001 DROP VIEW IF EXISTS `job_detailed_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `job_detailed_view` AS select `j`.`job_id` AS `job_id`,`b`.`title` AS `job_title`,`b`.`type` AS `job_type`,`b`.`status` AS `status`,`b`.`posted_date` AS `posted_date`,`b`.`expiry_date` AS `expiry_date`,`c`.`main_category_id` AS `main_category_id`,`c`.`sub_category_id` AS `sub_category_id`,`mc`.`name` AS `main_category_name`,`sc`.`name` AS `sub_category_name`,`cmp`.`company_id` AS `company_id`,`cmp`.`name` AS `company_name`,`cmp`.`industry` AS `industry`,`cmp`.`company_size` AS `company_size`,`cmp`.`verified` AS `verified`,`cmp`.`registration_date` AS `registration_date`,`l`.`area` AS `area`,`l`.`city` AS `city`,`l`.`country` AS `country`,`s`.`min_salary` AS `min_salary`,`s`.`max_salary` AS `max_salary`,`s`.`currency` AS `currency`,`s`.`period` AS `period`,`src`.`source_type` AS `source_type`,`src`.`scraped_from` AS `scraped_from`,`jhss`.`hard_skill_corpus` AS `hard_skill_corpus`,`jhss`.`soft_skill_corpus` AS `soft_skill_corpus`,`jhss`.`combine_skill_corpus` AS `combine_skill_corpus`,`jhss`.`share_link` AS `share_link` from (((((((((`jobs` `j` join `basicinfo` `b` on((`j`.`job_id` = `b`.`job_id`))) join `classification` `c` on((`j`.`job_id` = `c`.`job_id`))) join `main_category` `mc` on((`c`.`main_category_id` = `mc`.`main_category_id`))) join `sub_category` `sc` on((`c`.`sub_category_id` = `sc`.`sub_category_id`))) join `company` `cmp` on((`j`.`company_id` = `cmp`.`company_id`))) join `salary` `s` on((`j`.`job_id` = `s`.`job_id`))) join `location` `l` on((`j`.`job_id` = `l`.`job_id`))) join `jobs_source` `src` on((`j`.`job_id` = `src`.`job_id`))) join `job_hard&soft_skill` `jhss` on((`j`.`job_id` = `jhss`.`job_id`))) where ((`src`.`source_type` = 'scraping') and (`src`.`scraped_from` = 'jobsdb')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `job_skill_flattened_view`
--

/*!50001 DROP VIEW IF EXISTS `job_skill_flattened_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `job_skill_flattened_view` AS select `j`.`job_id` AS `job_id`,`b`.`title` AS `job_title`,`mc`.`name` AS `main_category_name`,`sc`.`name` AS `sub_category_name`,`cmp`.`industry` AS `company_industry`,`js`.`skill_name` AS `skill_name`,`js`.`skill_type` AS `skill_type`,`b`.`posted_date` AS `posted_date`,`slr`.`min_salary` AS `min_salary`,`slr`.`max_salary` AS `max_salary` from ((((((((`jobs` `j` join `basicinfo` `b` on((`j`.`job_id` = `b`.`job_id`))) join `classification` `c` on((`j`.`job_id` = `c`.`job_id`))) join `main_category` `mc` on((`c`.`main_category_id` = `mc`.`main_category_id`))) join `sub_category` `sc` on((`c`.`sub_category_id` = `sc`.`sub_category_id`))) join `company` `cmp` on((`j`.`company_id` = `cmp`.`company_id`))) join `jobs_skill` `js` on((`j`.`job_id` = `js`.`job_id`))) join `jobs_source` `src` on((`j`.`job_id` = `src`.`job_id`))) join `salary` `slr` on((`j`.`job_id` = `slr`.`job_id`))) where ((`src`.`source_type` = 'scraping') and (`src`.`scraped_from` = 'jobsdb') and (`js`.`skill_type` in ('hard_skill','soft_skill'))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `job_skills_view`
--

/*!50001 DROP VIEW IF EXISTS `job_skills_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `job_skills_view` AS select `j`.`job_id` AS `job_id`,(select json_arrayagg(`js`.`skill_name`) from `jobs_skill` `js` where (`js`.`job_id` = `j`.`job_id`)) AS `combine_skill_corpus`,(select json_arrayagg(`js`.`skill_name`) from `jobs_skill` `js` where ((`js`.`job_id` = `j`.`job_id`) and (`js`.`skill_type` = 'soft_skill'))) AS `soft_skills`,(select json_arrayagg(`js`.`skill_name`) from `jobs_skill` `js` where ((`js`.`job_id` = `j`.`job_id`) and (`js`.`skill_type` = 'hard_skill'))) AS `hard_skills` from `jobs` `j` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `job_hard&soft_skill`
--

/*!50001 DROP VIEW IF EXISTS `job_hard&soft_skill`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `job_hard&soft_skill` AS select `j`.`job_id` AS `job_id`,`jb`.`title` AS `title`,`j`.`share_link` AS `share_link`,`m`.`name` AS `main_category_name`,`s`.`name` AS `sub_category_name`,concat('[',group_concat((case when (`jsk`.`skill_type` = 'hard_skill') then concat('"',`jsk`.`skill_name`,'"') end) separator ', '),']') AS `hard_skill_corpus`,concat('[',group_concat((case when (`jsk`.`skill_type` = 'soft_skill') then concat('"',`jsk`.`skill_name`,'"') end) separator ', '),']') AS `soft_skill_corpus`,json_arrayagg(`jsk`.`skill_name`) AS `combine_skill_corpus` from (((((((`jobs` `j` join `basicinfo` `jb` on((`j`.`job_id` = `jb`.`job_id`))) join `jobs_source` `js` on((`j`.`job_id` = `js`.`job_id`))) join `classification` `c` on((`j`.`job_id` = `c`.`job_id`))) join `main_category` `m` on((`c`.`main_category_id` = `m`.`main_category_id`))) join `sub_category` `s` on((`c`.`sub_category_id` = `s`.`sub_category_id`))) join `jobs_skill_status` `jss` on((`j`.`job_id` = `jss`.`job_id`))) join `jobs_skill` `jsk` on((`j`.`job_id` = `jsk`.`job_id`))) where ((`js`.`source_type` = 'scraping') and (`js`.`scraped_from` = 'jobsdb')) group by `j`.`job_id`,`jb`.`title`,`j`.`share_link`,`m`.`name`,`s`.`name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-14  2:28:13
