from flask import Flask, Blueprint
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix

from app.main.nectar.nectar_controller import api as nectar_crm

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)

api = Api(app, title='Api Flask Expieriments', version='1.0', description='Api de experimentos com python flask',prefix='/api')

#adicionado namespace nectar_crm para rotas
api.add_namespace(nectar_crm, path='/nectar_crm')