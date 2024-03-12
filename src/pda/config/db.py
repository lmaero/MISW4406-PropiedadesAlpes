import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None

DB_USERNAME = os.getenv("DB_USERNAME", default="root")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="admin")
DB_HOSTNAME = os.getenv("DB_HOSTNAME", default="localhost")


class DatabaseConfigException(Exception):
    def _init_(self, message="Configuration file is null or malformed"):
        self.message = message
        super().__init__(self.message)


def database_connection(
    config, basedir=os.path.abspath(os.path.dirname(__file__))
) -> str:
    if not isinstance(config, dict):
        raise DatabaseConfigException

    return f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/pda"


def init_db(app: Flask):
    global db
    db = SQLAlchemy(app)
