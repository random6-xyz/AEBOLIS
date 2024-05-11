from databases.db import Database
from os import getenv

# settings
ip = "0.0.0.0"
ports = getenv("PORT", 7777)


def db_setup():
    db = Database()

    # create table if not exist
    db.execute("""
                CREATE TABLE IF NOT EXISTS USER(
                    ID INTEGER PRIMARY KEY,
                    NAME TEXT, 
                    HASHED_PASSWORD TEXT,
                    SALT TEXT,
                    IS_CONFIRMED INTEGER
                    );
                """)
    db.execute(
        "CREATE TABLE IF NOT EXISTS userbooks \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, \
            title TEXT NOT NULL, \
            writer TEXT NOT NULL,\
            publisher TEXT NOT NULL,\
            ISBN TEXT NOT NULL,\
            pages INTEGERS, number\
            INTEGERS NOT NULL);"
    )
