import os
import requests
import json
from flask import request
from flask_restx import Resource, Namespace
from app.main.utils.utils import Utils

api = Namespace("HubSpot", description="Integração client CRM")

util = Utils()
client = util.get_hubspot()

headers_post = {"Content-Type": "application/json"}
params = {"api_token": client.api_key}

menu_cpf = "cpf"
menu_cnpj = "cnpj"
menu_phone = "telefone"
menu_email = "email"


def get_url():
    return util.get_url() + "client/"


def home_menu(msg):
    return {
        "type": "MENU",
        "text": msg,
        "attachments": [
            {
                "position": "BEFORE",
                "type": "IMAGE",
                "name": "image.png",
                "url": client.company_logo,
            }
        ],
        "items": [
            {
                "number": 1,
                "text": "CPF",
                "callback": {
                    "endpoint": get_url() + "search_cpf",
                    "data": {},
                },
            },
            {
                "number": 2,
                "text": "CNPJ",
                "callback": {
                    "endpoint": get_url() + "search_cnpj",
                    "data": {},
                },
            },
            {
                "number": 3,
                "text": "Telefone",
                "callback": {
                    "endpoint": get_url() + "search_phone",
                    "data": {},
                },
            },
            {
                "number": 4,
                "text": "Email",
                "callback": {
                    "endpoint": get_url() + "search_email",
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
                "url": client.company_logo,
            }
        ],
        "items": [
            {
                "number": 1,
                "text": "Próxima tarefa",
                "callback": {
                    "endpoint": get_url() + "search_next_activity",
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
                "url": client.company_logo,
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
                "url": client.company_logo,
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
    if msg_menu == menu_cpf:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            get_url + "search_cpf",
        )
    elif msg_menu == menu_cnpj:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            get_url + "search_cnpj",
        )
    elif msg_menu == menu_phone:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            get_url + "search_phone",
        )
    elif msg_menu == menu_email:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            util.get_url() + "search_email",
        )
    else:
        return home_menu("Olá, por favor informe uma das seguintes informações.")


def get_user(request_mz, msg_menu):

    if request_mz.status_code == 200:
        print("The request was a success!")

        json_response = request_mz.json()
        json_size = len(json_response)

        print(
            f"Status Code: {request_mz.status_code}, Content: {json_response}, Size Json {json_size}"
        )

        if json_size == 0:
            return invalid_information(msg_menu), 201
        else:

            s1 = json.dumps(json_response)
            user = json.loads(s1)

            if "results" in user:

                print(json_response["results"])
                print(json_response["results"][0]["properties"])
                print(json_response["results"][0]["properties"]["firstname"])

                user_json = json_response["results"][0]["properties"]

                msg = (
                    "Olá "
                    + user_json["firstname"]
                    + " "
                    + user_json["lastname"]
                    + ", informe qual opção deseja consultar"
                )

                return menu_user(user_json, msg), 201
            else:
                return invalid_information(msg_menu), 201

    elif request_mz.status_code == 404:
        return {"error": "Request must be JSON"}, 404


@api.route("/")
class HubSpotController(Resource):
    def post(self):
        if request.is_json:
            mz = request.get_json()
            nome = mz["contact"]["name"]

            data = {
                "filterGroups": [
                    {
                        "filters": [
                            {
                                "propertyName": "firstname",
                                "operator": "EQ",
                                "value": nome,
                            }
                        ]
                    }
                ]
            }

            request_mz = requests.post(
                client.api + "search?hapikey=" + client.api_key,
                data=json.dumps(data),
                headers=headers_post,
            )

            return get_user(request_mz, "home_menu")

        return {"error": "Request must be JSON"}, 415
