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
params = {"hapikey": client.api_key, "limit": 1}

menu_cpf = "cpf"
menu_cnpj = "cnpj"
menu_phone = "telefone"
menu_email = "email"


def get_url():
    return util.get_url() + "hubspot/"


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
                "text": "Email",
                "callback": {
                    "endpoint": get_url() + "search_email",
                    "data": {},
                },
            }
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
            get_url() + "search_email",
        )
    else:
        return response_question("Olá, por favor informe seu email:", get_url())


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

            result_size = len(json_response["results"])

            if result_size > 0:

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
            text = mz["text"]

            data = {
                "filterGroups": [
                    {
                        "filters": [
                            {
                                "propertyName": "email",
                                "operator": "EQ",
                                "value": text,
                            }
                        ]
                    }
                ]
            }

            request_mz = requests.post(
                client.api + "contacts/search?hapikey=" + client.api_key,
                data=json.dumps(data),
                headers=headers_post,
            )

            return get_user(request_mz, "home_menu")

        return {"error": "Request must be JSON"}, 415


@api.route("/search_next_activity")
class PersonNextActivityController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            data = mz["data"]
            data_size = len(data)

            print(f"Content: {data} Size: {data_size}")

            if data_size == 0:
                return home_menu(
                    "Olá, não foi possivel encontrar nenhuma atividade, por favor informe uma das seguintes informações."
                )
            elif data["user"]["hs_object_id"]:

                user_id = data["user"]["hs_object_id"]

                print(f"User id: {user_id}")

                request_mz = requests.get(
                    client.api + "tickets",
                    params=params,
                    headers=util.get_headers(client.api_key),
                )

                print(f"Url: {request_mz.url} Content: {request_mz.json()}")

                return response_information("", ""), 201

        return {"error": "Request must be JSON"}, 415
