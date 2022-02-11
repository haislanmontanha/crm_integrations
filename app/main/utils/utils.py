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
            return "https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us30.gitpod.io/"
        else:
            return "http://localhost:5500/api/"
