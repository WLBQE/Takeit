USE TakeIt;

INSERT INTO Users (email, password, username)
  VALUES ('ponyma@tencent.com', '$2b$12$5xlUGbjZvpIhbSynpjM8veyfNtV62wKrqynR3GGEajIi.0DT70.pa', 'Pony Ma'); -- 1
INSERT INTO Users (email, password, username)
  VALUES ('jackma@alibaba.com', '$2b$12$y2kh3SchJ8fpY8Z0Q0BSb.FFWYaPzXqkOKhtdNSD5jdCnDLn6PiMC', 'Jack Ma'); -- 2
INSERT INTO Users (email, password, username)
  VALUES ('markzuckerberg@facebook.com', '$2b$12$8i.JaIqRff7YIceIZ2pldOHWuS9X1ZVmbfB/jKjOojzxWB4lk6Jma', 'Mark Zuckerberg'); -- 3
INSERT INTO Users (email, password, username)
  VALUES ('timcook@apple.com', '$2b$12$zLL7mM9f0GbjlwLIXGdBbOuSj.hOMDJWFVpahUW0AC1RCTrF/9.aa', 'Tim Cook'); -- 4
INSERT INTO Users (email, password, username)
  VALUES ('larrypage@google.com', '$2b$12$gR3xq9z5ykSaJa3OFT0YEegTmrlXsZX8zdDxo/rj2G5RpcpaTA3nm', 'Larry Page'); -- 5

INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('New Wechat Announcement', '2018-01-01 12:00', '2018-01-01 13:00', 'Tencent Tower', 'Download the most popular instant messenger now!', 1); -- 1
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('Double 11 Big Sale', '2018-11-11 00:00', '2018-11-11 23:59', 'Tmall & Taobao', 'Over 253 billion RMB sales last year! Go shopping in Tmall & Taobao!', 2); -- 2
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('WWDC 2018', '2018-06-05 00:00', '2018-06-09 00:00', 'San Jose, California', 'Meet the brand-new MacBook and IPhone!', 4); -- 3

INSERT INTO Follow (id1, id2) VALUES (1, 2);
INSERT INTO Follow (id1, id2) VALUES (1, 3);
INSERT INTO Follow (id1, id2) VALUES (1, 4);
INSERT INTO Follow (id1, id2) VALUES (1, 5);
INSERT INTO Follow (id1, id2) VALUES (2, 1);
INSERT INTO Follow (id1, id2) VALUES (3, 1);
INSERT INTO Follow (id1, id2) VALUES (4, 1);
INSERT INTO Follow (id1, id2) VALUES (4, 5);
INSERT INTO Follow (id1, id2) VALUES (5, 1);
INSERT INTO Follow (id1, id2) VALUES (5, 4);

INSERT INTO Regs (event, user) VALUES(1, 3);
INSERT INTO Regs (event, user) VALUES(2, 3);
INSERT INTO Regs (event, user) VALUES(3, 3);
INSERT INTO Regs (event, user) VALUES(3, 5);

INSERT INTO Comments (event, creator, content) VALUES (1, 1, 'Come and join Tencent! Wechat is the best social media!');
INSERT INTO Comments (event, creator, content) VALUES (1, 3, 'I still prefer Facebook :)');
