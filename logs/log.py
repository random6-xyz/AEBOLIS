from json import dumps, loads


# Save json to userbooks.log
def save_userbooks_log(json_data):
    open("./logs/userbooks.log", "a+").write(dumps(json_data) + ", ")


# reset log file
def reset_uesrbooks_log(json_data):
    open("./logs/userbooks.log", "w+").write(dumps(json_data).lstrip("[").rstrip("]"))


# Load json from userbooks.log
def load_userbooks_log():
    return loads("[" + open("./logs/userbooks.log", "r").read().rstrip(", ") + "]")


import logging
from logging.handlers import RotatingFileHandler
import json
import pytz
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record):
        seoul_tz = pytz.timezone("Asia/Seoul")
        current_time = datetime.now(seoul_tz)
        formatted_time = current_time.isoformat()

        log_record = {
            "level": record.levelname,
            "logger_name": record.name,
            "message": record.getMessage(),
            "time": formatted_time,
        }
        for key, value in record.__dict__.items():
            if key in ("remote_addr", "id"):
                log_record[key] = value

        return json.dumps(log_record)


def setup_acces_logger():
    logger = logging.getLogger("accessLogger")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler("./logs/access.log", maxBytes=10000, backupCount=1)
    handler.setFormatter(JSONFormatter())

    logger.addHandler(handler)
    return logger


def setup_signup_logger():
    logger = logging.getLogger("signupLogger")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler("./logs/signup.log", maxBytes=10000, backupCount=1)
    handler.setFormatter(JSONFormatter())

    logger.addHandler(handler)
    return logger
