DROP DATABASE IF EXISTS TakeIt;
CREATE DATABASE TakeIt;

CREATE TABLE TakeIt.Users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL,
  password VARCHAR(64) NOT NULL,
  name VARCHAR(64) NOT NULL,
  PRIMARY KEY(id),
  UNIQUE(username)
);

CREATE TABLE TakeIt.Events (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(64) NOT NULL,
  start_time DATETIME,
  end_time DATETIME,
  location TINYTEXT,
  description TEXT,
  creator INT NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE TakeIt.Friends (
  id1 INT NOT NULL,
  id2 INT NOT NULL,
  CONSTRAINT UNIQUE(id1, id2)
);

CREATE TABLE TakeIt.Regs (
  event INT NOT NULL,
  user INT NOT NULL,
  CONSTRAINT UNIQUE(event, user)
);