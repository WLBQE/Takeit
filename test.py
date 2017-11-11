import unittest
from app import app, db


class Tests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def run_sql_file(self, filename):
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

    # test for view
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
        ))

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
        self.assertEqual(rv.status_code, 302)
        self.assertIn(b'login', rv.data)

    def test_create_event(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        rv = self.create_event('20 Da', '2022-10-01 10:00', '2022-10-07 10:00', 'Renmindahuitang', 'hello world')
        self.assertEqual(rv.status_code, 302)
        rv = self.app.get('/profile/1', follow_redirects=True)
        self.assertIn(b'20 Da', rv.data)


if __name__ == "__main__":
    log_file = 'log_file.txt'
    f = open(log_file, 'w')
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()


