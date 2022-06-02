import hashlib
import imghdr
import os
from typing import Optional

from werkzeug.datastructures import FileStorage

from models.user import User


class UserController:

    @classmethod
    def create_user(cls, email: str, password: str, nickname: str) -> bool:
        return User.register(email, password, nickname)

    @classmethod
    def login(cls, email: str, password: str) -> bool:
        user = User.get_user(email)
        if not user:
            return False
        hashed_password = hashlib.sha1((user.salt + password).encode('utf-8')).hexdigest()
        if hashed_password == user.password:
            return True
        return False

    @classmethod
    def get_user_info(cls, email: str) -> Optional[User]:
        user = User.get_user(email)
        if not user:
            return None
        return user.to_dict()

    @classmethod
    def get_user_avatar(cls, user_hash: str) -> (Optional[bytes], Optional[str]):
        user = User.get_user_by_hash(user_hash)
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
