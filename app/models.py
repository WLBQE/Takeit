from passlib.hash import bcrypt
from pymysql import escape_string
from pymysql.err import Error

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
                '''.format(escape_string(email), bcrypt.encrypt(password), escape_string(username)))
        except Error:
            conn.close()
            return None
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id

    def find(self):
        if self.id is None:
            return None
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM Users WHERE id={}".format(self.id))
        data = cursor.fetchone()
        conn.close()
        return data

    def authenticate(self, email, password):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM Users WHERE email='{}'".format(escape_string(email)))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        password_encrypted = data[2]
        if not bcrypt.verify(password, password_encrypted):
            return None
        self.id = data[0]
        return data[0], data[1]

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
        if self.check_register(event_id):
            return False
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Regs (event, user) VALUES ({}, {})".format(event_id, self.id))
        except Error:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True

    def unregister(self, event_id):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Regs WHERE event={} AND user={}".format(event_id, self.id))
        conn.commit()
        conn.close()

    def check_follow(self, user_id):
        if user_id == self.id:
            return True
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Follow WHERE id1={} AND id2={}".format(self.id, user_id))
        data = cursor.fetchone()
        conn.close()
        return data is not None

    def follow(self, user_id):
        if self.id == user_id:
            return False
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Follow (id1, id2) VALUES ({}, {})".format(self.id, user_id))
        except Error:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True

    def unfollow(self, user_id):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Follow WHERE id1={} AND id2={}".format(self.id, user_id))
        conn.commit()
        conn.close()

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
                '''.format(event_id, self.id, escape_string(content)))
        except Error:
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
            '''.format(escape_string(keyword), escape_string(keyword)))
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
        if start_time >= end_time:
            return None
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Events (name, start_time, end_time, location, description, creator)
            VALUES ('{}', '{}', '{}', '{}', '{}', {})
            '''.format(escape_string(event_name), escape_string(start_time), escape_string(end_time),
                       escape_string(event_location), escape_string(event_description), creator_id))
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
