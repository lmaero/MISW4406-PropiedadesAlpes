import os

from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


# noinspection PyUnresolvedReferences
def import_sql_alchemy_models():
    import pda.modules.cliente.infraestructura.dto
    import pda.modules.hoteles.infraestructura.dto
    import pda.modules.pagos.infraestructura.dto
    import pda.modules.precios_dinamicos.infraestructura.dto
    import pda.modules.vehiculos.infraestructura.dto
    import pda.modules.properties.infrastructure.dto


def create_app(configuracion=None):
    # Init la application de Flask
    app = Flask(__name__, instance_relative_config=True)

    # Configuracion de BD
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa la DB
    from pda.config.db import init_db

    init_db(app)

    from pda.config.db import db

    import_sql_alchemy_models()

    with app.app_context():
        db.create_all()

    # Importa Blueprints
    from . import cliente
    from . import hoteles
    from . import pagos
    from . import precios_dinamicos
    from . import vehiculos
    from . import properties

    # Registro de Blueprints
    app.register_blueprint(cliente.bp)
    app.register_blueprint(hoteles.bp)
    app.register_blueprint(pagos.bp)
    app.register_blueprint(precios_dinamicos.bp)
    app.register_blueprint(vehiculos.bp)
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
