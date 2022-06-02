from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import etc.config as config

_connection_string = f'mysql+mysqlconnector://{config.MYSQL_CONFIG["user"]}:{config.MYSQL_CONFIG["password"]}' \
                     f'@{config.MYSQL_CONFIG["host"]}/{config.MYSQL_CONFIG["database"]}'
engine = create_engine(_connection_string)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()
