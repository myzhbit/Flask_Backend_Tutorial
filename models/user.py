import hashlib
from typing import Optional

import mysql.connector
import utils
from models import my_conn


class User:
    def __init__(self, email: str, password: str, salt: str, user_hash: str, nickname: str):
        self.email = email
        self.password = password
        self.salt = salt
        self.user_hash = user_hash
        self.nickname = nickname

    def to_dict(self):
        return {
            'email': self.email,
            'nickname': self.nickname,
            'user_hash': self.user_hash
        }

    @classmethod
    def get_user(cls, email: str) -> Optional['User']:
        with my_conn.cursor() as cursor:
            command = "SELECT * FROM user WHERE email = %s"
            cursor.execute(command, (email,))
            user = cursor.fetchone()
            if user:
                return cls(user[1], user[2], user[3], user[4], user[5])
            else:
                return None

    @classmethod
    def get_user_by_hash(cls, user_hash: str) -> Optional['User']:
        with my_conn.cursor() as cursor:
            command = "SELECT * FROM user WHERE hash = %s"
            cursor.execute(command, (user_hash,))
            user = cursor.fetchone()
            if user:
                return cls(user[1], user[2], user[3], user[4], user[5])
            else:
                return None

    @classmethod
    def register(cls, email: str, password: str, nickname: str) -> bool:
        salt = utils.gen_random_salt()
        hashed_password = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        user_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
        with my_conn.cursor() as cursor:
            try:
                command = "INSERT INTO user (email, password, salt, hash, nickname) " \
                          "VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(command, (email, hashed_password, salt, user_hash, nickname))
                my_conn.commit()
                return True
            except mysql.connector.errors.IntegrityError:
                return False
