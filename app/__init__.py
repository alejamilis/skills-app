from config import Config

from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Obtener la configuracion del ambiente elegido
    app.config.from_object(get_environment_config())

    # Inicializa la conexion a la BD
    db.init_app(app)

    from app.schema import schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )

    @app.before_first_request
    def initialize_database():
        """ Crea las tablas de la BD """
        db.create_all()

    @ app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/")
    def test():
        return "Test ok!"

    return app

def get_environment_config():
    if Config.ENV == "TESTING":
        return "config.TestingConfig"
    elif Config.ENV == "DEVELOPMENT":
        return "config.DevelopmentConfig"