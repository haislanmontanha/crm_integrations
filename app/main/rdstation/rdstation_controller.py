import os
import requests
import json
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace
from datetime import datetime
from app.main.utils.utils import Utils


api = Namespace("RDStation", description="Integração RD Station CRM")

app = Flask(__name__)
util = Utils()

api_contact = "https://api.rd.services/platform/contacts/"
api_key = "adf54a9d729dea6410155f75bf251198"

headers_post = {"Content-Type": "application/json"}
params = {"refresh_token": api_key}

MENU_CPF = "cpf"
MENU_CNPJ = "cnpj"
MENU_PHONE = "telefone"
MENU_EMAIL = "email"


def get_url():
    return util.get_url() + "rdstation/"


def home_menu(msg):
    return {
        "type": "MENU",
        "text": msg,
        "attachments": [
            {
                "position": "BEFORE",
                "type": "IMAGE",
                "name": "image.png",
                "url": "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png",
            }
        ],
        "items": [
            {
                "number": 1,
                "text": "CPF",
                "callback": {
                    "endpoint": get_url() + "/search_cpf",
                    "data": {},
                },
            },
            {
                "number": 2,
                "text": "CNPJ",
                "callback": {
                    "endpoint": get_url() + "/search_cnpj",
                    "data": {},
                },
            },
            {
                "number": 3,
                "text": "Telefone",
                "callback": {
                    "endpoint": get_url() + "/search_phone",
                    "data": {},
                },
            },
            {
                "number": 4,
                "text": "Email",
                "callback": {
                    "endpoint": get_url() + "/search_email",
                    "data": {},
                },
            },
        ],
    }


def menu_user(user_json, msg):
    return {
        "type": "MENU",
        "text": msg,
        "attachments": [
            {
                "position": "BEFORE",
                "type": "IMAGE",
                "name": "image.png",
                "url": "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png",
            }
        ],
        "items": [
            {
                "number": 1,
                "text": "Próxima tarefa",
                "callback": {
                    "endpoint": get_url() + "/search_next_activity",
                    "data": {"user": user_json},
                },
            }
        ],
    }


def response_question(text, callback):
    return {
        "type": "QUESTION",
        "text": text,
        "attachments": [
            {
                "position": "BEFORE",
                "type": "IMAGE",
                "name": "image.png",
                "url": "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png",
            }
        ],
        "callback": {"endpoint": callback, "data": {}},
    }


def response_information(text, url_document):
    return {
        "type": "INFORMATION",
        "text": text,
        "attachments": [
            {
                "position": "BEFORE",
                "type": "IMAGE",
                "name": "image.png",
                "url": "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png",
            },
            {
                "position": "AFTER",
                "type": "DOCUMENT",
                "name": "document.pdf",
                "url": url_document,
            },
        ],
    }


def invalid_information(msg_menu):
    if msg_menu == MENU_CPF:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            get_url + "/search_cpf",
        )
    elif msg_menu == MENU_CNPJ:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            get_url + "/search_cnpj",
        )
    elif msg_menu == MENU_PHONE:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            get_url + "/search_phone",
        )
    elif msg_menu == MENU_EMAIL:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            get_url() + "/search_email",
        )
    else:
        return home_menu("Olá, por favor informe uma das seguintes informações.")


def get_user(request_mz, msg_menu):
    print("get_user")

    if request_mz.status_code == 200:
        print("The request was a success!")
        # Code here will only run if the request is successful
        json_response = request_mz.json()
        json_size = len(json_response)

        print(
            f"Status Code: {request_mz.status_code}, Content: {json_response}, Size Json {json_size}"
        )

        if json_size == 0:
            return invalid_information(msg_menu), 201
        else:

            s1 = json.dumps(json_response)
            # user = json.loads(s1)

            # if "results" in user:
            #
            #     print(json_response["results"])
            #     print(json_response["results"][0]["properties"])
            #     print(json_response["results"][0]["properties"]["firstname"])
            #
            #     user_json = json_response["results"][0]["properties"]
            #
            #     msg = (
            #         "Olá "
            #         + user_json["firstname"]
            #         + " "
            #         + user_json["lastname"]
            #         + ", informe qual opção deseja consultar"
            #     )
            #
            #     return menu_user(user_json, msg), 201
            # else:
            return invalid_information(msg_menu), 201

    elif request_mz.status_code == 404:
        return {"error": "Request must be JSON"}, 404
    elif request_mz.status_code == 401:
        return request_mz.json(), 401


@api.route("/")
class RdStationController(Resource):
    def post(self):
        if request.is_json:
            mz = request.get_json()
            email = mz["text"]

            request_mz = requests.get(
                api_contact + "email:" + email,
                params=params,
                headers=util.get_headers(api_key),
            )

            return get_user(request_mz, "home_menu")

        return {"error": "Request must be JSON"}, 415
