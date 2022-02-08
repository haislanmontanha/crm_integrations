import os
import requests
import json
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace
from datetime import datetime

api = Namespace('HubSpot',description='Integração HubSpot CRM')

@api.route('/')
class HubSpotController(Resource):

    @api.response(200, "Busca realizada com sucesso") #documentação para tipo de respostas
    
    def get(self):
         return "Hello World!", 200