from sqlalchemy import Column, VARCHAR, Integer, CHAR

from models import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(32), nullable=False, unique=True)
    password = Column(CHAR(40), nullable=False)
    salt = Column(CHAR(32), nullable=False)
    hash = Column(CHAR(32), nullable=False, unique=True)
    nickname = Column(VARCHAR(20), nullable=False)

    def to_dict(self):
        return {
            'email': self.email,
            'hash': self.hash,
            'nickname': self.nickname
        }
