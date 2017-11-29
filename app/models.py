from passlib.hash import bcrypt
from pymysql.err import IntegrityError

from app import db


class User:
    def __init__(self, user_id=None):
        self.id = user_id

    def create(self, email, password, username):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Users (email, password, username) VALUES('{}', '{}', '{}')
                '''.format(email, bcrypt.encrypt(password), username))
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
            cursor.execute("SELECT id, username, email FROM Users WHERE id={}".format(self.id))
        else:
            cursor.execute("SELECT id, username, email FROM Users WHERE email={}".format(email))
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
        cursor.execute("SELECT * FROM Regs WHERE event={} AND user={}".format(event_id, self.id))
        data = cursor.fetchone()
        conn.close()
        return data is not None

    def register(self, event_id):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Regs (event, user) VALUES ({}, {})".format(event_id, self.id))
        except IntegrityError:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True

    def unregister(self, event_id):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Regs WHERE event={} AND user={}".format(event_id, self.id))
        except IntegrityError:
            conn.close()
            return
        conn.commit()
        conn.close()
        return

    def follow(self, user_id):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Follow (id1, id2) VALUES ({}, {})".format(self.id, user_id))
        except IntegrityError:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True

    def unfollow(self, user_id):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Follow WHERE id1={} AND id2={}".format(self.id, user_id))
        except IntegrityError:
            conn.close()
            return
        conn.commit()
        conn.close()
        return

    def get_followings(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email FROM Follow, Users WHERE id1={} AND Users.id=Follow.id2
            '''.format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_followers(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email FROM Follow, Users WHERE id2={} AND Users.id=Follow.id1
            '''.format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_following_events(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events WHERE creator IN (SELECT id2 FROM Follow WHERE id1={})".format(self.id))
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

    def post_comment(self, event_id, content):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Comments (event, creator, content) VALUES ({}, {}, '{}')
                '''.format(event_id, self.id, content))
        except IntegrityError:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def search_user(keyword):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email FROM Users WHERE STRCMP('{}', username)=0 OR STRCMP('{}', email)=0
            '''.format(keyword, keyword))
        data = cursor.fetchall()
        conn.close()
        return data


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
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Events (name, start_time, end_time, location, description, creator)
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(event_name, start_time, end_time, event_location, event_description, creator_id))
        except IntegrityError:
            conn.close()
            return None
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id

    def get_participants(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email FROM Users WHERE id IN (SELECT user FROM Regs WHERE event={})
            '''.format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_comments(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Users.id, username, content FROM Users, Comments
            WHERE Users.id=Comments.creator AND Comments.event={}
            '''.format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data
