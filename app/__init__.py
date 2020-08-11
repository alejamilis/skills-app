from config import Config

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
cors = CORS(app)

def create_app():
    # Obtener la configuracion del ambiente elegido
    app.config.from_object(get_environment_config())
    app.config['CORS_HEADERS'] = 'Content-Type'

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
    @cross_origin()
    def test():
        return "Test ok!"

    return app

def get_environment_config():
    if Config.ENV == "TESTING":
        return "config.TestingConfig"
    elif Config.ENV == "DEVELOPMENT":
        return "config.DevelopmentConfig"