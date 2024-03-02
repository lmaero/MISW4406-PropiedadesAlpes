import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None


DB_USERNAME = os.getenv("DB_USERNAME", default="root")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="admin")
DB_HOSTNAME = os.getenv("DB_HOSTNAME", default="localhost")


class DatabaseConfigException(Exception):
    def _init_(self, message="Configuration file is Null or malformed"):
        self.message = message
        super()._init_(self.message)


def database_connection(
    config, basedir=os.path.abspath(os.path.dirname(_file_))
) -> str:
    if not isinstance(config, dict):
        raise DatabaseConfigException

    if config.get("TESTING", False):
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        return f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/transactions"


def init_db(app: Flask):
    global db
    db = SQLAlchemy(app)