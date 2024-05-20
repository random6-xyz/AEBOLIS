from databases.db import Database
from os import getenv
from flask_login import LoginManager
from modules import app

from logs.log import setup_acces_logger, setup_signup_logger


# settings
ip = "0.0.0.0"
ports = getenv("PORT", 7777)


login_manager = LoginManager()
access_logger = setup_acces_logger()
signup_logger = setup_signup_logger()


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

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS book_field (
            book_id INTEGER NOT NULL,
            category TEXT NOT NULL
        );
    """
    )

    # create table if not exist
    db.execute(
        """
                CREATE TABLE IF NOT EXISTS USER(
                    ID INTEGER PRIMARY KEY,
                    NAME TEXT NOT NULL, 
                    HASHED_PASSWORD TEXT NOT NULL,
                    SALT TEXT NOT NULL,
                    IS_ADMIN INTEGER NOT NULL,
                    IS_CONFIRMED INTEGER
                    );
                """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS category (
        category TEXT NOT NULL
        );
    """
    )

def login_setup():
    login_manager.init_app(app)
    app.config["SESSION_PERMANENT"] = False
    app.secret_key = getenv("FLASK_SECRET_KEY", "secretKeyForTest")


def setup():
    db_setup()
    login_setup()


