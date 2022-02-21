from ast import Return
from crypt import methods
from flask import Flask
from flask_restx import Namespace

api = Namespace("health_check", description="Health check")


@api.route("/alive", methods=["GET"])
def alive():
    return "OK"
