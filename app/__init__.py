from flask import Flask, Blueprint
from flask_restx import Api

from app.main.nectar.nectar_controller import api as nectar_controller
from app.main.hubspot.hubspot_controller import api as hubspot_controller
from app.main.rdstation.rdstation_controller import api as rdstation_controller

app = Flask(__name__)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)

api = Api(app, 
            title='Api de integrações com CRMs', 
            version='1.0', 
            description='Api de integrações com os seguintes CRMs:',
            prefix='/api')

#adicionado namespace nectar_crm para rotas
api.add_namespace(nectar_controller, path='/nectar')
api.add_namespace(hubspot_controller, path='/hubspot')
api.add_namespace(rdstation_controller, path='/rdstation')