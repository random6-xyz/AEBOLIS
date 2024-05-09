from databases.db import Database
from os import getenv

# settings
ip = "0.0.0.0"
ports = getenv("PORT", 7777)

def db_setup():
    db = Database()

    # create table if not exist
    db.execute(";")