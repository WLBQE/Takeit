from passlib.hash import bcrypt

from app import db


class User:
    def __init__(self, user_id=None):
        self.id = user_id

    def create(self, email, password, username):
        if self.id is not None:
            return None
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users(email, password, username) VALUES('{}', '{}', '{}')"
                       .format(email, bcrypt.encrypt(password), username))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id

    def find(self):
        if self.id is None:
            return None
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE id={}".format(self.id))
        data = cursor.fetchone()
        conn.close()
        return data

    def authenticate(self, email, password):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM Users WHERE email='{}'".format(email))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return None
        password_encrypted = data[1]
        if not bcrypt.verify(password, password_encrypted):
            return None
        self.id = data[0]
        return data[0]

    def register(self, event_id):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Regs (event, user) VALUES ({}, {})".format(event_id, self.id))
        conn.commit()
        conn.close()

    def get_friends(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id2 FROM Friends WHERE id1={}".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_friends_events(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events WHERE creator IN (SELECT id2 FROM Friends WHERE id1={})".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_events_created(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Events WHERE creator={}".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_events_participated(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT event FROM Regs WHERE user={})".format(self.id))
        data = cursor.fetchall()
        conn.close()
        return data


class Event:
    def __init__(self, event_id=None):
        self.id = event_id

    def find(self):
        if self.id is None:
            return False
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
        creator.register(self.id)
        return self.id
