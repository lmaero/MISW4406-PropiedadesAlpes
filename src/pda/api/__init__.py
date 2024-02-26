import os

from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


# noinspection PyUnresolvedReferences
def import_sql_alchemy_models():
    import pda.modules.properties.infrastructure.dto


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from pda.config.db import init_db

    init_db(app)

    from pda.config.db import db

    import_sql_alchemy_models()

    with app.app_context():
        db.create_all()

    from . import properties

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
