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
    VALUES ('Wechat Announcement', '2018-01-01 12:00', '2018-01-01 13:00', 'Tencent Tower', 'Download the most popular instant messenger now!', 1); -- 1
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('Grand Celebration', '2018-02-01 12:00', '2018-02-01 13:00', 'Shenzhen', 'We are now one of the Top 10 Tech Companies in the world!', 1); -- 2
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('Double 11 Big Sale', '2018-11-11 00:00', '2018-11-11 23:59', 'Tmall & Taobao', 'Over 253 billion RMB sales last year! Go shopping in Tmall & Taobao!', 2); -- 3
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('WWDC 2018', '2018-06-05 00:00', '2018-06-09 00:00', 'San Jose, California', 'Meet the brand-new MacBook and IPhone!', 4); -- 4
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('Google Conference', '2018-10-04 00:00', '2018-10-04 01:00', 'California', 'Come and see how Google plans the future of AI!', 5); -- 5

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
INSERT INTO Comments (event, creator, content) VALUES (1, 2, 'QQ is a copy of ICQ. Wechat is a copy of QQ. Disappointed');
INSERT INTO Comments (event, creator, content) VALUES (2, 5, 'Cong! Welcome to join us!');
INSERT INTO Comments (event, creator, content) VALUES (2, 4, 'Cong! Please also join our WWDC 2018!');
INSERT INTO Comments (event, creator, content) VALUES (2, 2, 'Money does not mean anything for me.');
INSERT INTO Comments (event, creator, content) VALUES (3, 2, 'It is something far more amazing than Black Friday! Come and join!');
INSERT INTO Comments (event, creator, content) VALUES (3, 3, 'My Chinese wife really loves Double 11...');
INSERT INTO Comments (event, creator, content) VALUES (4, 5, 'Your products suck without Steve Jobs.');
INSERT INTO Comments (event, creator, content) VALUES (4, 4, 'Hey Larry, do you know how much money we made from China? Can Google even get into China? :)');
INSERT INTO Comments (event, creator, content) VALUES (5, 3, 'Far more impressive than WWDC');
INSERT INTO Comments (event, creator, content) VALUES (5, 1, 'Larry please come back to China and help me crush Baidu.');









