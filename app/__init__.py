from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from .models import db
from .routes import api as routes_api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config_class='config.ProductionConfig'):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_class)
    db.init_app(app)
    # Initialize Flask-JWT-Extended
    jwt = JWTManager(app)
    api = Api(app, version='1.0', title='Delivery API',
              description='A simple Delivery API')
    api.add_namespace(routes_api, path='/api')

    return app
