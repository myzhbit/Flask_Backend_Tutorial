import hashlib
import imghdr
import os
from typing import Optional

import sqlalchemy.exc
from werkzeug.datastructures import FileStorage

import utils
from models import db_session
from models.user import User


class UserController:

    @classmethod
    def create_user(cls, email: str, password: str, nickname: str) -> bool:
        salt = utils.gen_random_salt()
        hashed_password = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        user_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
        user = User(email=email, password=hashed_password, salt=salt, nickname=nickname, hash=user_hash)
        try:
            db_session.add(user)
            db_session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()
            return False

    @classmethod
    def login(cls, email: str, password: str) -> bool:
        user = db_session.query(User).filter(User.email == email).first()
        if not user:
            return False
        hashed_password = hashlib.sha1((user.salt + password).encode('utf-8')).hexdigest()
        if hashed_password == user.password:
            return True
        return False

    @classmethod
    def get_user_info(cls, email: str) -> Optional[User]:
        user = db_session.query(User).filter(User.email == email).first()
        if not user:
            return None
        return user.to_dict()

    @classmethod
    def get_user_avatar(cls, user_hash: str) -> (Optional[bytes], Optional[str]):
        user = db_session.query(User).filter(User.hash == user_hash).first()
        if not user:
            return None, None

        cwd = os.getcwd()
        avatar_file = os.path.join(cwd, 'avatar', user.user_hash)
        if not os.path.exists(avatar_file):
            avatar_file = os.path.join(cwd, 'avatar', 'default.jpg')
        with open(avatar_file, 'rb') as f:
            mimetype = imghdr.what(f)
            return f.read(), f'image/{mimetype}'

    @classmethod
    def modify_user_avatar(cls, user, avatar: FileStorage) -> bool:
        img_type = imghdr.what(avatar.stream)
        if not img_type:
            return False

        cwd = os.getcwd()
        avatar_path = os.path.join(cwd, 'avatar', user.user_hash)
        with open(avatar_path, 'wb') as fp:
            fp.write(avatar.read())
        return True
