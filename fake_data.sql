USE TakeIt;

INSERT INTO Users (email, password, username)
  VALUES ('xjp@ccp.gov', '$2b$12$5xlUGbjZvpIhbSynpjM8veyfNtV62wKrqynR3GGEajIi.0DT70.pa', 'Xi Jinping'); -- 1
INSERT INTO Users (email, password, username)
  VALUES ('lhz@falundafa.org', '$2b$12$y2kh3SchJ8fpY8Z0Q0BSb.FFWYaPzXqkOKhtdNSD5jdCnDLn6PiMC', 'Li Hongzhi'); -- 2
INSERT INTO Users (email, password, username)
  VALUES ('haha@zhangzhe.wang', '$2b$12$zLL7mM9f0GbjlwLIXGdBbOuSj.hOMDJWFVpahUW0AC1RCTrF/9.aa', 'Jiang Zemin'); -- 3
INSERT INTO Users (email, password, username)
  VALUES ('lxb@anticcp.com', '$2b$12$8i.JaIqRff7YIceIZ2pldOHWuS9X1ZVmbfB/jKjOojzxWB4lk6Jma', 'Liu Xiaobo'); -- 4
INSERT INTO Users (email, password, username)
  VALUES ('wangdan@pku.edu.cn', '$2b$12$gR3xq9z5ykSaJa3OFT0YEegTmrlXsZX8zdDxo/rj2G5RpcpaTA3nm', 'Wang Dan'); -- 5

INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('19 Da', '2017-10-01 00:00', '2017-10-01 23:59', 'Renmin Dahuitang', 'Follow the party', 1); -- 1
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('Falun Dafa', '1997-10-01 00:00', '1997-10-01 23:59', 'Xinghai Square', 'Falun Dafa is good', 2); -- 2
INSERT INTO Events (name, start_time, end_time, location, description, creator)
    VALUES ('8964', '1989-06-04 00:00', '1989-06-04 06:00', 'Tiananmen Square', 'China needs democracy'my, 4); -- 3

INSERT INTO Friends (id1, id2) VALUES(1, 2);
INSERT INTO Friends (id1, id2) VALUES(1, 3);
INSERT INTO Friends (id1, id2) VALUES(1, 4);
INSERT INTO Friends (id1, id2) VALUES(1, 5);
INSERT INTO Friends (id1, id2) VALUES(2, 1);
INSERT INTO Friends (id1, id2) VALUES(3, 1);
INSERT INTO Friends (id1, id2) VALUES(4, 1);
INSERT INTO Friends (id1, id2) VALUES(4, 5);
INSERT INTO Friends (id1, id2) VALUES(5, 1);
INSERT INTO Friends (id1, id2) VALUES(5, 4);

INSERT INTO Regs (event, user) VALUES(1, 3);
INSERT INTO Regs (event, user) VALUES(2, 3);
INSERT INTO Regs (event, user) VALUES(3, 3);
INSERT INTO Regs (event, user) VALUES(3, 5);
