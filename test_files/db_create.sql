DROP DATABASE IF EXISTS hashproject;

CREATE DATABASE hashproject;

USE hashproject;

DROP TABLE IF EXISTS ssdeep_hashes;

CREATE TABLE ssdeep_hashes (hash_id INT PRIMARY KEY, 
                            hash VARCHAR(40));

DROP TABLE IF EXISTS chunks;

CREATE TABLE chunks (hash_id INT, 
                    chunk_size INT,
                    chunk INT);