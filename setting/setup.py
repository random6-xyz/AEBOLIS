from databases.db import Database
from os import getenv
from flask_login import LoginManager
from modules import app
import os

# settings
ip = "0.0.0.0"
ports = getenv("PORT", 7777)

login_manager = LoginManager()


def db_setup():
    db = Database()

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


def login_setup():
    login_manager.init_app(app)
    app.config["SESSION_PERMANENT"] = False
    # app.secret_key = os.environ.get('FLASK_SECRET_KEY')
    app.secret_key = "secretKeyForTest"


def setup():
    db_setup()
    login_setup()
