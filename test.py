import unittest
from app import app, db
from app.models import User, Event


class Tests(unittest.TestCase):
    first = True

    # executed prior to each test
    def setUp(self):
        if Tests.first:
            print("FIRST!")
            self.run_sql_file('create.sql')
            self.run_sql_file('fake_data.sql')
            Tests.first = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    @staticmethod
    def run_sql_file(filename):
        sqlfile = open(filename, 'r')
        sql = " ".join(sqlfile.readlines())
        connection = db.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        sqlfile.close()

    # executed after each test
    def tearDown(self):
        self.run_sql_file('create.sql')
        self.run_sql_file('fake_data.sql')

    # tests for model
    def test_user_create_auth(self):
        create = User().create('testuser@te.st', 'password', 'test user')
        self.assertEqual(create, 6)
        create = User().create('testuser@te.st', 'passw0rd', 'bug user')
        self.assertIsNone(create)
        auth = User().authenticate('testuser@te.st', 'password')
        self.assertIsNotNone(auth)
        self.assertTupleEqual(auth, (6, 'test user'))
        invalid = User().authenticate('hacker@ha.ck', 'intruding')
        self.assertIsNone(invalid)

    def test_user_find(self):
        user = User(1).find()
        self.assertIsNotNone(user)
        self.assertTupleEqual(user, (1, 'Xi Jinping', 'xjp@ccp.gov'))
        self.assertIsNone(User(6).find())
        self.assertIsNone(User().find())

    def test_user_check_register(self):
        self.assertTrue(User(1).check_register(1))
        self.assertTrue(User(3).check_register(1))
        self.assertFalse(User(1).check_register(2))

    def test_user_register(self):
        self.assertTrue(User(1).register(2))
        self.assertFalse(User(1).register(2))
        self.assertFalse(User(1).register(1))
        self.assertFalse(User(3).register(1))
        self.assertFalse(User(1).register(12345))

    def test_user_unregister(self):
        self.assertTrue(User(3).check_register(1))
        User(3).unregister(1)
        self.assertFalse(User(3).check_register(1))

    def test_user_check_follow(self):
        self.assertTrue(User(1).check_follow(1))
        self.assertTrue(User(1).check_follow(2))
        self.assertFalse(User(2).check_follow(3))

    def test_user_follow(self):
        self.assertTrue(User(2).follow(3))
        self.assertFalse(User(2).follow(3))
        self.assertFalse(User(2).follow(2))
        self.assertFalse(User(2).follow(1))
        self.assertFalse(User(123).follow(1))

    def test_user_unfollow(self):
        self.assertTrue(User(1).check_follow(2))
        User(1).unfollow(2)
        self.assertFalse(User(1).check_follow(2))

    def test_user_get_followings(self):
        users = User(1).get_followings()
        self.assertTupleEqual(users, ((2, 'Li Hongzhi', 'lhz@falundafa.org'), (3, 'Jiang Zemin', 'haha@zhangzhe.wang'),
                                      (4, 'Liu Xiaobo', 'lxb@anticcp.com'), (5, 'Wang Dan', 'wangdan@pku.edu.cn')))

    def test_user_get_followers(self):
        users = User(1).get_followers()
        self.assertTupleEqual(users, ((2, 'Li Hongzhi', 'lhz@falundafa.org'), (3, 'Jiang Zemin', 'haha@zhangzhe.wang'),
                                      (4, 'Liu Xiaobo', 'lxb@anticcp.com'), (5, 'Wang Dan', 'wangdan@pku.edu.cn')))

    def test_user_get_following_events(self):
        events = User(1).get_following_events()
        self.assertTupleEqual(events, ((2, 'Falun Dafa', '1997-10-01 00:00', '1997-10-01 23:59', 'Xinghai Square',
                                        'Falun Dafa is good', 2),
                                       (3, '8964', '1989-06-04 00:00', '1989-06-04 06:00', 'Tiananmen Square',
                                        'China needs democracy', 4)))

    def test_user_get_events_created(self):
        events = User(2).get_events_created()
        self.assertTupleEqual(events, ((2, 'Falun Dafa', '1997-10-01 00:00', '1997-10-01 23:59', 'Xinghai Square',
                                        'Falun Dafa is good', 2),))
        self.assertTupleEqual(User(5).get_events_created(), ())

    def test_user_get_events_participated(self):
        self.assertTupleEqual(User(1).get_events_participated(), ())
        events = User(3).get_events_participated()
        self.assertTupleEqual(events, ((1, '19 Da', '2017-10-01 00:00', '2017-10-01 23:59', 'Renmin Dahuitang',
                                        'Follow the party', 1),
                                       (2, 'Falun Dafa', '1997-10-01 00:00', '1997-10-01 23:59', 'Xinghai Square',
                                        'Falun Dafa is good', 2),
                                       (3, '8964', '1989-06-04 00:00', '1989-06-04 06:00', 'Tiananmen Square',
                                        'China needs democracy', 4)))

    def test_user_post_comment(self):
        self.assertFalse(User(1).post_comment(123, 'foo bar'))
        self.assertTrue(User(3).post_comment(2, "Let's get rid of you guys!"))
        self.assertTupleEqual(Event(2).get_comments(), ((3, 'Jiang Zemin', "Let's get rid of you guys!"),))

    def test_search_user(self):
        self.assertTupleEqual(User.search_user('Kim'), ())
        self.assertTupleEqual(User.search_user('xjp@ccp.gov'), ((1, 'Xi Jinping', 'xjp@ccp.gov'),))
        self.assertTupleEqual(User.search_user('Xi Jinping'), ((1, 'Xi Jinping', 'xjp@ccp.gov'),))

    def test_event_find(self):
        event = Event().find()
        self.assertIsNone(event)
        event = Event(1).find()
        self.assertIsNotNone(event)
        self.assertTupleEqual(event, (1, '19 Da', '2017-10-01 00:00', '2017-10-01 23:59', 'Renmin Dahuitang',
                                      'Follow the party', 1))
        self.assertIsNone(Event(4).find())

    def test_event_create(self):
        ret = Event().create(10, '20 Da', "I'm still the president", 'Renmin Dahuitang', '2022-10-02 00:00',
                             '2022-10-01 00:00')
        self.assertIsNone(Event(4).find())
        self.assertIsNone(ret)
        ret = Event().create(1, '20 Da', "I'm still the president", 'Renmin Dahuitang', '2022-10-02 00:00',
                             '2022-10-01 00:00')
        self.assertIsNone(ret)
        ret = Event().create(1, '20 Da', "I'm still the president", 'Renmin Dahuitang', '2022-10-01 00:00',
                             '2022-10-02 00:00')
        self.assertEqual(ret, 4)
        self.assertTupleEqual(Event(4).find(), (4, '20 Da', '2022-10-01 00:00', '2022-10-02 00:00', 'Renmin Dahuitang',
                                                "I'm still the president", 1))

    def test_event_get_participants(self):
        self.assertTupleEqual(Event(3).get_participants(), ((3, 'Jiang Zemin', 'haha@zhangzhe.wang'),
                                                            (5, 'Wang Dan', 'wangdan@pku.edu.cn')))
        self.assertTupleEqual(Event(4).get_participants(), ())

    def test_event_get_comments(self):
        self.assertTupleEqual(Event(1).get_comments(), ((1, 'Xi Jinping', 'Jiang Zemin is the enemy of us!'),
                                                        (3, 'Jiang Zemin', 'I spoke with American Wallace.')))
        self.assertTupleEqual(Event(2).get_comments(), ())

    # tests for view
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password,
            remember=True
            ), follow_redirects=True)

    def create_event(self, name, start_time, end_time, location, description):
        return self.app.post('/create_event', data=dict(
            name=name,
            start_date=start_time,
            end_date=end_time,
            location=location,
            description=description
        ), follow_redirects=True)

    def test_login_success(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Falun Dafa', rv.data)
        self.assertIn(b'8964', rv.data)

    def test_login_fail(self):
        rv = self.login('xjp@ccp.gov', 'wrong_password')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_logout(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_event_detail_no_session(self):
        rv = self.app.get('/event_detail/2', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_event_detail_exist(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/event_detail/2', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'1997-10-01', rv.data)

    def test_event_detail_non_exist(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/event_detail/100', follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_profile_no_session(self):
        rv = self.app.get('/event_detail/2', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_profile_exist(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/profile/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'19 Da', rv.data)

    def test_profile_non_exist(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/profile/100', follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_create_event_no_session(self):
        rv = self.create_event('20 Da', '2022-10-01 10:00', '2022-10-07 10:00', 'Renmindahuitang', 'hello world')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'login', rv.data)

    def test_create_event(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.create_event('20 Da', '2022-10-01 10:00', '2022-10-07 10:00', 'Renmindahuitang', 'hello world')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/profile/1', follow_redirects=True)
        self.assertIn(b'20 Da', rv.data)

    def test_add_friend_no_session(self):
        rv = self.app.get('/add_friend', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_add_friend(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.post('/add_friend', data=dict(
            userinfo='Li Hongzhi'
        ))
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Li Hongzhi', rv.data)

    def test_add_no_session(self):
        rv = self.app.get('/add/3', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_show_friends_no_session(self):
        rv = self.app.get('/show_friends', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_show_friends(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/show_friends', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Jiang Zemin', rv.data)

    def test_add_comment_no_session(self):
        rv = self.app.get('/add_comment/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)

    def test_add_comment_(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.post('/add_comment/1', data=dict(
            comment='hahaha'
        ), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'hahaha', rv.data)


if __name__ == "__main__":
    log_file = 'test_log.txt'
    f = open(log_file, 'w')
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()
