from passlib.hash import bcrypt
from pymysql.err import IntegrityError

from app import db


class User:
    def __init__(self, user_id=None):
        self.id = user_id

    def create(self, email, password, username):
        if self.id is not None:
            return None
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users(email, password, username) VALUES('{}', '{}', '{}')"
                           .format(email, bcrypt.encrypt(password), username))
        except IntegrityError:
            conn.close()
            return None
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id

    def find(self, email=None):
        if self.id is None:
            return None
        conn = db.connect()
        cursor = conn.cursor()
        if email is None:
            cursor.execute("SELECT * FROM Users WHERE id={}".format(self.id))
        else:
            cursor.execute("SELECT * FROM Users WHERE email={}".format(email))
        data = cursor.fetchone()
        conn.close()
        return data

    def authenticate(self, email, password):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM Users WHERE email='{}'".format(email))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        password_encrypted = data[1]
        if not bcrypt.verify(password, password_encrypted):
            return None
        self.id = data[0]
        return data[0]

    def check_register(self, event_id):
        event = Event(event_id).find()
        if event is None:
            return False
        if event[6] == self.id:
            return True
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Regs WHERE event={} and user={}".format(event_id, self.id))
        data = cursor.fetchone()
        conn.close()
        return data is not None

    def register(self, event_id):
        if Event(event_id).find() is None:
            return False
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Regs (event, user) VALUES ({}, {})".format(event_id, self.id))
        conn.commit()
        conn.close()
        return True

    def get_friends(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id2 FROM Friends WHERE id1={}".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_following_events(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events WHERE creator IN (SELECT id2 FROM Friends WHERE id1={})".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_events_created(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events WHERE creator={}".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_events_participated(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events WHERE id IN (SELECT event FROM Regs WHERE user={})".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def search_user(keyword):
        conn = db.connect()
        cursor = conn.cursor()


class Event:
    def __init__(self, event_id=None):
        self.id = event_id

    def find(self):
        if self.id is None:
            return None
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events WHERE id={}".format(self.id))
        data = cursor.fetchone()
        conn.close()
        return data

    def create(self, creator_id, event_name, event_description, event_location, start_time, end_time):
        creator = User(creator_id)
        if not creator.find():
            return None
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Events (name, start_time, end_time, location, description, creator)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
            '''.format(event_name, start_time, end_time, event_location, event_description, creator_id))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id

    def get_participants(self):
        if not self.find():
            return None
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE id IN (SELECT user FROM Regs WHERE event={})".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data
