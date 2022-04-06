-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: cheesecake-rds.cviuuuldzzde.ap-southeast-1.rds.amazonaws.com    Database: ESD
-- ------------------------------------------------------
-- Server version	8.0.27

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES ('A001','Caramelised Salmon (2pc)',3.8,'http://www.sushiexpress.com.sg/Resources/Menu/5ccfc451f0924add9fd67aa13257aedf.png',1),('A002','Cheese Abalone (2pc)',3.9,'http://www.sushiexpress.com.sg/Resources/Menu/9c9627bc8dbc4248bc42bc199e120f8d.png',1),('A003','Aburi Salmon (2pc)',5.9,'http://www.sushiexpress.com.sg/Resources/Menu/9f7ac5c7be094764a8f4fb876de27b84.png',1),('A004','Jumbo Salmon (1pc)',9.9,'http://www.sushiexpress.com.sg/Resources/Menu/71a41f85b4be41a3a87262843318f6ea.png',1),('A005','Grilled Eel Sushi (2pc)',9.9,'http://www.sushiexpress.com.sg/Resources/Menu/f0a42712e6114ed8a7bba85d1054f460.png',1),('A006','Grilled Salmon Belly (2pc)',12.9,'http://www.sushiexpress.com.sg/Resources/Menu/6231ebf64a28416bbb54378071b68125.png',1),('B001','Salmon Sashimi (6pc) ',12.9,'https://aubreyskitchen.com/wp-content/uploads/2021/01/sushi-grade-salmon-sashimi.jpg',1),('B002','Tamagoyaki (6pc)',6.9,'https://www.justonecookbook.com/wp-content/uploads/2019/08/tamagoyaki-1058.jpg',1),('B003','Saikyo Miso Saba (1pc)',3.9,'http://cdn.shopify.com/s/files/1/0367/0074/9957/products/SabaSaikyo_1200x1200.jpg?v=1593098707',1),('B004','Hana Maki (1pc)',5.9,'http://www.sushiexpress.com.sg/Resources/Menu/fb0ed0fc26684271a8dc4635b947c424.png',1),('B005','Miso Soup (1 bowl)',4.9,'http://www.sushiexpress.com.sg/Resources/Menu/fdbdc14ddd364b65b91d132b82584496.png',1),('C001','Okra',2.5,'http://www.sushiexpress.com.sg/Resources/Menu/b9c658ae46564c5fbf5ae6495f97e7a9.png',1),('D001','Chocolate Cake (1pc)',5.9,'http://www.sushiexpress.com.sg/Resources/Menu/562149f9fc614cedac44cef052361fb5.png',1),('D002','Cream Puff (3pc)',5.9,'http://www.sushiexpress.com.sg/Resources/Menu/182491026aff4b558fc05dd314b79852.png',1),('D003','Blueberry Cheesecake (1pc)',3.9,'http://www.sushiexpress.com.sg/Resources/Menu/e190121ad3ca4913b28c976de0e238e4.png',1);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-06 12:12:35
