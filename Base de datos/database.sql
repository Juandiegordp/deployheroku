CREATE DATABASE  IF NOT EXISTS aplicaciongym /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE aplicaciongym;
-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: aplicaciongym
-- ------------------------------------------------------
-- Server version	5.7.29-log

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
-- Table structure for table ejercicio
--

DROP TABLE IF EXISTS ejercicio;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE ejercicio (
  id_ejercicio int(11) NOT NULL AUTO_INCREMENT,
  nombre varchar(30) DEFAULT NULL,
  descripcion varchar(60) DEFAULT NULL,
  PRIMARY KEY (id_ejercicio)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table ejercicio
--

LOCK TABLES ejercicio WRITE;
/*!40000 ALTER TABLE ejercicio DISABLE KEYS */;
INSERT INTO ejercicio VALUES (1,'ejercicio1','ASDASDADSadasdfadsasd'),(2,'ejercicio2','ASasafsdasfafkjfdjslkqwqwe'),(3,'ejercicio3','asñkjñqwourjas'),(5,'Ejercicio4','asdfkadlsja');
/*!40000 ALTER TABLE ejercicio ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table entrenador
--

DROP TABLE IF EXISTS entrenador;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE entrenador (
  id_entrenador int(11) NOT NULL AUTO_INCREMENT,
  nombre varchar(45) DEFAULT NULL,
  apellido varchar(45) DEFAULT NULL,
  dni varchar(45) DEFAULT NULL,
  cargo varchar(45) DEFAULT NULL,
  PRIMARY KEY (id_entrenador)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table entrenador
--

LOCK TABLES entrenador WRITE;
/*!40000 ALTER TABLE entrenador DISABLE KEYS */;
/*!40000 ALTER TABLE entrenador ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table prueba
--

DROP TABLE IF EXISTS prueba;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE prueba (
  id_prueba int(11) NOT NULL,
  descripcion varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (id_prueba)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table prueba
--

LOCK TABLES prueba WRITE;
/*!40000 ALTER TABLE prueba DISABLE KEYS */;
/*!40000 ALTER TABLE prueba ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table rutina
--

DROP TABLE IF EXISTS rutina;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE rutina (
  id_rutina int(11) NOT NULL AUTO_INCREMENT,
  fecha date NOT NULL,
  nombre varchar(45) DEFAULT NULL,
  estado varchar(45) DEFAULT NULL,
  PRIMARY KEY (id_rutina,fecha)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table rutina
--

LOCK TABLES rutina WRITE;
/*!40000 ALTER TABLE rutina DISABLE KEYS */;
INSERT INTO rutina VALUES (1,'2021-07-24','Abdomen','Creada'),(2,'2021-07-25','Abdomen','Creada'),(3,'2021-10-08','Piernas','Creada'),(33,'2021-10-10','brazos','Creada'),(34,'2021-10-11','Piernas','Creada'),(39,'2021-10-11','prueba','Creada'),(40,'2021-10-11','1','Creada'),(41,'2021-10-11','2','Creada'),(42,'2021-10-11','3','Creada'),(43,'2021-10-11','4','Creada'),(44,'2021-10-11','5','Creada'),(45,'2021-10-11','6','Creada'),(46,'2021-10-11','Natalia','Creada'),(47,'2021-10-11','7','Creada'),(48,'2021-10-11','8','Creada'),(49,'2021-10-11','9','Creada'),(50,'2021-10-11','10','Creada'),(51,'2021-10-11','11','Creada'),(52,'2021-10-11','12','Creada'),(53,'2021-10-11','13','Creada'),(54,'2021-10-11','14','Creada'),(55,'2021-10-11','15','Creada'),(56,'2021-10-11','16','Creada'),(57,'2021-10-11','17','Creada'),(58,'2021-10-11','18','Creada'),(59,'2021-10-11','19','Creada'),(60,'2021-10-11','20','Creada'),(61,'2021-10-11','21','Creada'),(62,'2021-10-11','22','Creada'),(63,'2021-10-11','23','Creada'),(64,'2021-10-11','24','Creada'),(65,'2021-10-11','25','Creada'),(66,'2021-10-11','26','Creada'),(67,'2021-10-11','27','Creada'),(68,'2021-10-11','28','Creada'),(70,'2021-10-11','29','Creada'),(71,'2021-10-11','30','Creada'),(72,'2021-10-11','31','Creada'),(90,'2021-10-11','32','Creada'),(93,'2021-10-23','56','Creada');
/*!40000 ALTER TABLE rutina ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table rutina_ejercicio
--

DROP TABLE IF EXISTS rutina_ejercicio;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE rutina_ejercicio (
  fecha_rutina date NOT NULL,
  id_rutina int(11) NOT NULL,
  id_ejercicio int(11) NOT NULL,
  descanso int(11) DEFAULT NULL,
  repeticiones int(11) DEFAULT NULL,
  peso int(11) DEFAULT NULL,
  series int(11) DEFAULT NULL,
  PRIMARY KEY (fecha_rutina,id_rutina,id_ejercicio),
  KEY rutina_ejercicio_rutina_idx (id_rutina),
  KEY rutina_ejercicio_ejercicio_idx (id_ejercicio),
  CONSTRAINT rutina_ejercicio_ejercicio FOREIGN KEY (id_ejercicio) REFERENCES ejercicio (id_ejercicio) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT rutina_ejercicio_rutina FOREIGN KEY (id_rutina) REFERENCES rutina (id_rutina) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table rutina_ejercicio
--

LOCK TABLES rutina_ejercicio WRITE;
/*!40000 ALTER TABLE rutina_ejercicio DISABLE KEYS */;
INSERT INTO rutina_ejercicio VALUES ('2021-07-24',1,1,1,1,1,1),('2021-07-24',1,2,1,1,1,1),('2021-07-24',1,5,1,1,1,11),('2021-10-08',3,1,5,15,30,2),('2021-10-08',3,3,3,12,25,3),('2021-10-10',33,1,4,12,11,3),('2021-10-10',33,2,2,15,11,5),('2021-10-11',34,2,3,12,11,3),('2021-10-11',34,3,4,15,15,5),('2021-10-11',90,1,4,12,11,3),('2021-10-11',90,2,2,15,11,5);
/*!40000 ALTER TABLE rutina_ejercicio ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table usuario
--

DROP TABLE IF EXISTS usuario;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE usuario (
  id_usuario int(11) NOT NULL AUTO_INCREMENT,
  usuario varchar(10) DEFAULT NULL,
  nombre varchar(45) DEFAULT NULL,
  apellido varchar(45) DEFAULT NULL,
  mail varchar(45) DEFAULT NULL,
  contra varchar(45) DEFAULT NULL,
  PRIMARY KEY (id_usuario)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table usuario
--

LOCK TABLES usuario WRITE;
/*!40000 ALTER TABLE usuario DISABLE KEYS */;
INSERT INTO usuario VALUES (6,'Danwife','Daniel','Medina','danielmedina012@gmail.com','Alexander1');
/*!40000 ALTER TABLE usuario ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table usuario_rutina
--

DROP TABLE IF EXISTS usuario_rutina;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE usuario_rutina (
  id_usuario int(11) NOT NULL,
  id_rutina int(11) NOT NULL,
  fecha_rutina date NOT NULL,
  PRIMARY KEY (id_usuario,id_rutina,fecha_rutina),
  KEY usuario_rutina_rutina_idx (fecha_rutina),
  KEY usuario_rutina_rutina_idx1 (fecha_rutina,id_rutina),
  KEY usuario_rutina_rutina_idx2 (id_rutina),
  CONSTRAINT usuario_rutina_rutina FOREIGN KEY (id_rutina) REFERENCES rutina (id_rutina) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT usuario_rutina_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table usuario_rutina
--

LOCK TABLES usuario_rutina WRITE;
/*!40000 ALTER TABLE usuario_rutina DISABLE KEYS */;
INSERT INTO usuario_rutina VALUES (6,33,'2021-10-10'),(6,34,'2021-10-11'),(6,39,'2021-10-11'),(6,40,'2021-10-11'),(6,41,'2021-10-11'),(6,42,'2021-10-11'),(6,43,'2021-10-11'),(6,44,'2021-10-11'),(6,45,'2021-10-11'),(6,46,'2021-10-11'),(6,47,'2021-10-11'),(6,48,'2021-10-11'),(6,49,'2021-10-11'),(6,50,'2021-10-11'),(6,51,'2021-10-11'),(6,52,'2021-10-11'),(6,53,'2021-10-11'),(6,54,'2021-10-11'),(6,55,'2021-10-11'),(6,56,'2021-10-11'),(6,57,'2021-10-11'),(6,58,'2021-10-11'),(6,59,'2021-10-11'),(6,60,'2021-10-11'),(6,61,'2021-10-11'),(6,62,'2021-10-11'),(6,63,'2021-10-11'),(6,64,'2021-10-11'),(6,65,'2021-10-11'),(6,66,'2021-10-11'),(6,67,'2021-10-11'),(6,68,'2021-10-11'),(6,70,'2021-10-11'),(6,71,'2021-10-11'),(6,72,'2021-10-11'),(6,93,'2021-10-23');
/*!40000 ALTER TABLE usuario_rutina ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-23 18:01:56
