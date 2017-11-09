import unittest
from app import app
from app.models import User


class Tests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    # test for view
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password,
            remember=True
            ), follow_redirects=True)

    def create_event(self, name, location, start_time, end_time, description):
        return self.app.post('/create_event', data=dict(
            name=name,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
        ))

    def test_login_success(self):
        rv = self.login('xjp@ccp.gov', 'qwer1234')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Falun Dafa', rv.data)
        self.assertIn(b'8964', rv.data)

        rv = self.app.get('/event_detail/2', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'1997-10-01', rv.data)

        rv = self.app.get('/profile/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'19 Da', rv.data)

        rv = self.app.get('/home', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'8964', rv.data)

    def test_login_fail(self):
        rv = self.login('xjp@ccp.gov', 'wrong_password')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'sign in', rv.data)


if __name__ == "__main__":
    unittest.main()