from flask import Flask, Blueprint
from flask_restx import Api

from app.main.nectar.nectar_controller import api as nectar_controller

app = Flask(__name__)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)

api = Api(app, title='Api Flask Expieriments', version='1.0', description='Api de experimentos com python flask',prefix='/api')

#adicionado namespace nectar_crm para rotas
api.add_namespace(nectar_controller, path='/nectar_crm')