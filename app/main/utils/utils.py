import os
import requests
import json
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace

utils = Namespace('Utils',description='Classe de informações')

if __name__ == '__main__':
    app.run(debug=True)

class Utils(Resource):

    def getUrlLocal():
        return "https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us30.gitpod.io/"
