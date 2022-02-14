import os
import requests
import json
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace

utils = Namespace("Utils", description="Classe de informações")

PRODUCTION = False


class Utils(Resource):
    def get_url(self):
        if bool(PRODUCTION):
            return "https://crmintegrations.herokuapp.com/"
        else:
            return "http://localhost:5500/api/"

    def get_headers(self, api_key):
        return {
            "Accept": "application/json",
            "Access-Token": api_key,
            "User-Agent": "request",
        }
