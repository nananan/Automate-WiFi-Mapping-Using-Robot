CREATE DATABASE IF NOT EXISTS cinnamon;

USE cinnamon;

CREATE TABLE IF NOT EXISTS APs (
     access_point_name VARCHAR(150),
     access_point_address VARCHAR(30) PRIMARY KEY NOT NULL,
     channel INT(2),
     type VARCHAR(50) NOT NULL,
     subtype VARCHAR(50) NOT NULL,
     strength VARCHAR(6),  
     timestamp DATETIME
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Waypoints (
     id_waypoint INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
     position_x FLOAT NOT NULL,
     position_y FLOAT NOT NULL,
     position_z FLOAT NOT NULL,
     orientation_x FLOAT NOT NULL,
     orientation_y FLOAT NOT NULL,
     orientation_z FLOAT NOT NULL,
     orientation_w FLOAT NOT NULL
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Waypoints_AP (
     id_waypoint INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
     position_x FLOAT NOT NULL,
     position_y FLOAT NOT NULL,
     position_z FLOAT NOT NULL,
     orientation_x FLOAT NOT NULL,
     orientation_y FLOAT NOT NULL,
     orientation_z FLOAT NOT NULL,
     orientation_w FLOAT NOT NULL,
     AP VARCHAR(30) NOT NULL,
     strength VARCHAR(6) NOT NULL
) ENGINE=InnoDB CHARSET=utf8;


CREATE TABLE IF NOT EXISTS Packets (
     BSSID VARCHAR(30) NOT NULL,
     source VARCHAR(30) NOT NULL,
     destination VARCHAR(30) NOT NULL,
     channel VARCHAR(5),
     type VARCHAR(50) NOT NULL,
     subtype VARCHAR(50) NOT NULL,
     strength VARCHAR(6),
     encrypted CHAR(1),  
     to_ds VARCHAR(10),  
     from_ds VARCHAR(10),  
     timestamp DATETIME);


CREATE TABLE IF NOT EXISTS EAP (
     BSSID VARCHAR(30) NOT NULL,
     source VARCHAR(30) NOT NULL,
     destination VARCHAR(30) NOT NULL,
     channel VARCHAR(5),
     type VARCHAR(50), #if is PEAP or EAP... if is PEAP the code will be Request, else Success/Failed
     code VARCHAR(50),
     strength VARCHAR(6),
     encrypted CHAR(1),  
     to_ds VARCHAR(10),  
     from_ds VARCHAR(10),  
     timestamp DATETIME);
