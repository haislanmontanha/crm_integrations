import os
import requests
import json
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace
from datetime import datetime

api = Namespace("RDStation", description="Integração RD Station CRM")


@api.route("/")
class RdStationController(Resource):
    @api.response(
        200, "Busca realizada com sucesso"
    )  # documentação para tipo de respostas
    def get(self):
        return "Hello World!", 200
