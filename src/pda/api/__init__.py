import os

from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


# noinspection PyUnresolvedReferences
def register_handlers():
    import pda.modules.client.application
    import pda.modules.properties.application
    import pda.modules.tenant.application


# noinspection PyUnresolvedReferences
def import_sql_alchemy_models():
    import pda.modules.client.infrastructure.dto
    import pda.modules.properties.infrastructure.dto


def start_consumer(app):
    import threading
    import pda.modules.client.infrastructure.consumers as client
    import pda.modules.properties.infrastructure.consumers as properties

    threading.Thread(target=client.subscribe_to_events).start()
    threading.Thread(target=properties.subscribe_to_events, args=[app]).start()

    threading.Thread(target=client.subscribe_to_commands).start()
    threading.Thread(target=properties.subscribe_to_commands, args=[app]).start()


def create_app(configuration={}):
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = "9d58f98f-3ae8-4149-a09f-3a8c2012e32c"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["TESTING"] = configuration.get("TESTING")

    from pda.config.db import init_db, database_connection

    app.config["SQLALCHEMY_DATABASE_URI"] = database_connection(
        configuration, basedir=basedir
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)

    from pda.config.db import db

    import_sql_alchemy_models()
    register_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get("TESTING"):
            start_consumer(app)

    # noinspection PyUnresolvedReferences
    from . import client
    from . import properties

    app.register_blueprint(client.bp)
    app.register_blueprint(properties.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0"
        swag["info"]["title"] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
