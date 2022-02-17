import os
import requests
import json
from flask import request
from flask_restx import Resource, Namespace
from app.main.utils.utils import Utils

api = Namespace("Funil de Vendas", description="Integração client CRM")

util = Utils()
client = util.get_sales_funnel()

headers_post = {"Content-Type": "application/json"}
params = {"api_token": client.api_key}


def get_url():
    return util.get_url() + "sales_funnel/"


@api.route("/")
class SalesFunnelController(Resource):
    def post(self):
        return {"sales funnel"}, 201
