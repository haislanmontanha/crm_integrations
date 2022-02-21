from flask import Flask, Blueprint, request, redirect
from flask_restx import Api

from app.main.nectar.nectar_controller import api as nectar_controller
from app.main.hubspot.hubspot_controller import api as hubspot_controller
from app.main.rdstation.rdstation_controller import api as rdstation_controller
from app.main.sales_funnel.sales_funnel_controller import api as sales_funnel_controller

app = Flask(__name__)
blueprint = Blueprint("api", __name__)
app.register_blueprint(blueprint)


@app.route("/alive", methods=["GET"])
def alive():
    return "OK"


api = Api(
    app,
    title="Api de integracoes com CRMs",
    version="1.0",
    description="Api de integracoes com os seguintes CRMs:",
    prefix="/api",
)

# Route namespacing
api.add_namespace(nectar_controller, path="/nectar")
api.add_namespace(hubspot_controller, path="/hubspot")
# api.add_namespace(rdstation_controller, path="/rdstation")
api.add_namespace(sales_funnel_controller, path="/sales_funnel")
