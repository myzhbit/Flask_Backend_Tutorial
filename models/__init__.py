import mysql.connector
import etc.config as config

my_conn = mysql.connector.connect(host=config.MYSQL_CONFIG['host'], user=config.MYSQL_CONFIG['user'],
                                  password=config.MYSQL_CONFIG['password'], database=config.MYSQL_CONFIG['database'])


def create_user_table():
    cursor = my_conn.cursor()
    command = """
create table if not exists user
(
    id       int auto_increment
        primary key,
    email    varchar(32) not null,
    password char(40)    not null,
    salt     char(32)    not null,
    hash     char(32)    not null,
    nickname varchar(20) not null,
    constraint user_email_uindex
        unique (email),
    constraint user_hash_uindex
        unique (hash)
);

"""
    cursor.execute(command)
    my_conn.commit()


create_user_table()
