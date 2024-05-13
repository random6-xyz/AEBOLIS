from databases.db import Database
from os import getenv

# settings
ip = "0.0.0.0"
ports = getenv("PORT", 7777)


def db_setup():
    db = Database()

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS USER(
            ID INTEGER PRIMARY KEY,
            NAME TEXT, 
            HASHED_PASSWORD TEXT,
            SALT TEXT,
            IS_CONFIRMED INTEGER
        );
    """
    )

    db.execute(
        "CREATE TABLE IF NOT EXISTS userbooks \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, \
            available INTEGER NOT NULL,\
            title TEXT NOT NULL, \
            writer TEXT NOT NULL, \
            publisher TEXT NOT NULL, \
            amount INTEGERS NOT NULL);"
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS userapplys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            publisher TEXT NOT NULL,
            writer TEXT NOT NULL,
            reason TEXT NOT NULL,
            confirm INTEGER NOT NULL
        );
    """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS checkout_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            return INTEGER NOT NULL,
            time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
        );
    """
    )
