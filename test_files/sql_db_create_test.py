#create database

import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE hashprojectpy")

#return list of system's databases

import mysql.connector
mydb = mysql.connector.connect(
  host ="localhost",
  user ="root",
  password =""
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

#connecting to the database
import mysql.connector

mydb = mysql.connector.connect(
  host ="localhost",
  user ="root",
  password ="",
  database ="hashprojectpy"
)

#creating ssdeep_hashes table including PK

import mysqlconnector

mydb = my.sql.connector.connect(
    host = "localhost"
    user = "root"
    password = ""
    database = "hashprojectpy"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE ssdeep_hashes (hash_id INT PRIMARY KEY, hash VARCHAR(40)")

#creating a table chunks
import mysqlconnector

mydb = mysql.connector.connect(
    host = "localhost"
    user = "root"
    password = ""
    database = "hashprojectpy"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE ssdeep_hashes (hash_id INT, chunk size INT, chunk INT")

#Check if table exists

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="hashprojectpy"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)

  #create PK on an existing table
  import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="hashprojectpy"
)

mycursor = mydb.cursor()

mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY") #change customers with name of table
