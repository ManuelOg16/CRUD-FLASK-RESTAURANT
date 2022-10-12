from flask import Flask,Blueprint
from flask_migrate import Migrate
from flask_restx import Api

from .config import Config   
from .models import db
from .views.orderView import nsOrder as nsorder
from .views.productView import nsProduct as nsproduct

def create_app():
    app = Flask(__name__)  

    if Config is None:
        app.config.from_object(Config.BaseConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)

    ###Routes
    bluePrint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(bluePrint, doc='/doc', version='1.0', title='Restaurant Configuration API', description='Swagger para Restaurant Configuration API')
    api.add_namespace(ns=nsorder)
    api.add_namespace(ns=nsproduct)
    

    app.register_blueprint(bluePrint)

   
    return app
    