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

    if (db.select_account_info(11111111)) is None:
        db.execute(
            """
            INSERT INTO USER
            SELECT * FROM (SELECT 
                11111111, 
                'adimin',
                'f8c6e58692da68991e92494a67414766ecd4db590666dc45c7f446953797df8544bb77f823095d3b5f2106a217b36ab40d73f0ac95b9aca5fafcc46c46473b66',
                '$2b$12$BEJ0KFPNZ.exUUKPDCp4j.',
                1,
                1
            )
        """
        )


def login_setup():
    login_manager.init_app(app)
    app.config["SESSION_PERMANENT"] = False
    app.secret_key = getenv("FLASK_SECRET_KEY", "secretKeyForTest")


def setup():
    db_setup()
    login_setup()
