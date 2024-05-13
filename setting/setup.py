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
                    NAME TEXT NOT NULL, 
                    HASHED_PASSWORD TEXT NOT NULL,
                    SALT TEXT NOT NULL,
                    IS_ADMIN INTEGER NOT NULL,
                    IS_CONFIRMED INTEGER
                    );
                """)