-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema hashproject
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `hashproject` ;

-- -----------------------------------------------------
-- Schema hashproject
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hashproject` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `hashproject` ;

-- -----------------------------------------------------
-- Table `hashproject`.`fuzzy_hash_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hashproject`.`fuzzy_hash_table` (
  `hash_id` INT NOT NULL,
  `ssdeep_hash` VARCHAR(148) NOT NULL,
  PRIMARY KEY (`hash_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hashproject`.`crypto_hash_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hashproject`.`crypto_hash_table` (
  `crypto_id` INT NOT NULL,
  `md5_hash` VARCHAR(32) NULL DEFAULT NULL,
  `sha1_hash` VARCHAR(40) NULL DEFAULT NULL,
  `sha256_hash` VARCHAR(148) NULL DEFAULT NULL,
  `fuzzy_hash_table_hash_id` INT NOT NULL,
  PRIMARY KEY (`crypto_id`),
  INDEX `fk_crypto_hash_table_fuzzy_hash_table1_idx` (`fuzzy_hash_table_hash_id` ASC) VISIBLE,
  CONSTRAINT `fk_crypto_hash_table_fuzzy_hash_table1`
    FOREIGN KEY (`fuzzy_hash_table_hash_id`)
    REFERENCES `hashproject`.`fuzzy_hash_table` (`hash_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hashproject`.`ssdeep_chunk_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hashproject`.`ssdeep_chunk_table` (
  `chunk_id` INT NOT NULL,
  `chunk_size` INT NOT NULL,
  `chunk` BIGINT(20) NOT NULL,
  `fuzzy_hash_table_hash_id` INT NOT NULL,
  PRIMARY KEY (`chunk_id`),
  INDEX `fk_ssdeep_chunk_table_fuzzy_hash_table1_idx` (`fuzzy_hash_table_hash_id` ASC) VISIBLE,
  CONSTRAINT `fk_ssdeep_chunk_table_fuzzy_hash_table1`
    FOREIGN KEY (`fuzzy_hash_table_hash_id`)
    REFERENCES `hashproject`.`fuzzy_hash_table` (`hash_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
