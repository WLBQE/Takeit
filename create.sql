DROP DATABASE IF EXISTS TakeIt;
CREATE DATABASE TakeIt;
USE TakeIt;

CREATE TABLE Users (
  id INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(64) NOT NULL,
  password VARCHAR(64) NOT NULL,
  username VARCHAR(64) NOT NULL,
  PRIMARY KEY(id),
  UNIQUE(email)
);

CREATE TABLE Events (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(64) NOT NULL,
  start_time VARCHAR(20),
  end_time VARCHAR(20),
  location TINYTEXT,
  description TEXT,
  creator INT NOT NULL,
  PRIMARY KEY(id),
  CHECK(STRCMP(start_time, end_time) = -1),
  FOREIGN KEY (creator) REFERENCES Users(id)
);

CREATE TABLE Follow (
  id1 INT NOT NULL,
  id2 INT NOT NULL,
  CONSTRAINT UNIQUE(id1, id2),
  CHECK(id1 <> id2),
  FOREIGN KEY (id1) REFERENCES Users(id),
  FOREIGN KEY (id2) REFERENCES Users(id)
); -- id1 follows id2

CREATE TABLE Regs (
  event INT NOT NULL,
  user INT NOT NULL,
  CONSTRAINT UNIQUE(event, user),
  FOREIGN KEY (user) REFERENCES Users(id),
  FOREIGN KEY (event) REFERENCES Events(id)
);