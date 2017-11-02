INSERT INTO TakeIt.Users (email, password, username) VALUES ('xjp@ccp.gov', 'qwer1234', 'Xi Jinipng');
INSERT INTO TakeIt.Users (email, password, username) VALUES ('lhz@falundafa.org', 'qwer1234', 'Li Hongzhi');
INSERT INTO TakeIt.Users (email, password, username) VALUES ('haha@zhangzhe.wang', 'qwer1234', 'Jiang Zemin');
INSERT INTO TakeIt.Users (email, password, username) VALUES ('lxb@anticcp.com', 'qwer1234', 'Liu Xiaobo');
INSERT INTO TakeIt.Users (email, password, username) VALUES ('wangdan@pku.edu.cn', 'qwer1234', 'Wang Dan');

INSERT INTO TakeIt.Events (name, start_time, end_time, location, description, creator)
    VALUES ('19 Da', '2017-10-01 00:00', '2017-10-01 23:59', 'Renmin Dahuitang 19', 'Ting Dang Zhi Hui 19', 1);
INSERT INTO TakeIt.Events (name, start_time, end_time, location, description, creator)
    VALUES ('Falun Dafa', '1997-10-01 00:00', '1997-10-01 23:59', 'Xinghai Square', 'Falun Dafa is good', 2);
INSERT INTO TakeIt.Events (name, start_time, end_time, location, description, creator)
    VALUES ('8964', '1989-06-04 00:00', '1989-06-04 06:00', 'Tiananmen Square', 'China needs democracy', 4);

INSERT INTO TakeIt.Friends (id1, id2) VALUES(1, 1);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(1, 2);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(1, 3);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(1, 4);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(1, 5);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(2, 1);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(3, 1);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(4, 1);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(4, 5);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(5, 1);
INSERT INTO TakeIt.Friends (id1, id2) VALUES(5, 4);

INSERT INTO TakeIt.Regs (event, user) VALUES(1, 1);
INSERT INTO TakeIt.Regs (event, user) VALUES(1, 3);
INSERT INTO TakeIt.Regs (event, user) VALUES(2, 2);
INSERT INTO TakeIt.Regs (event, user) VALUES(2, 3);
INSERT INTO TakeIt.Regs (event, user) VALUES(3, 3);
INSERT INTO TakeIt.Regs (event, user) VALUES(3, 4);
INSERT INTO TakeIt.Regs (event, user) VALUES(3, 5);
