import requests
import json
from flask import request
from flask_restx import Resource, Namespace
from datetime import datetime

from app.main.utils.utils import Utils

api = Namespace("Nectar", description="Integração client CRM")

util = Utils()
client = util.get_nectar()

params = {"api_token": client.api_key}
menu_cpf = "cpf"
menu_cnpj = "cnpj"
menu_phone = "telefone"
menu_email = "email"
menu_next_activity = "next_activity"


def get_url():
    return util.get_url() + "nectar/"


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


def response_information(text, urldoc):
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
                "url": urldoc,
            },
        ],
    }


def invalid_information(msg_menu, url_callback):
    if msg_menu == menu_cpf:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            url_callback,
        )
    elif msg_menu == menu_cnpj:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            url_callback,
        )
    elif msg_menu == menu_phone:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            url_callback,
        )
    elif msg_menu == menu_email:
        return response_question(
            "O "
            + msg_menu
            + " é inválido. Por favor informe um "
            + msg_menu
            + " válido.",
            url_callback,
        )
    else:
        return home_menu("Olá, por favor informe uma das seguintes informações.")


def getUser(request_mz, msg_menu):

    if request_mz.status_code == 200:
        print("The request was a success!")
        json_response = request_mz.json()
        json_size = len(json_response)

        print(
            f"Status Code: {request_mz.status_code}, Content: {json_response}, Size Json {json_size}"
        )

        if json_size == 0:
            return invalid_information(msg_menu, ""), 201
        else:

            s1 = json.dumps(json_response)
            user = json.loads(s1)

            if "message" not in user:

                user_id = json_response[0]["id"]
                request_user = requests.get(
                    client.api + str(user_id),
                    params=params,
                    headers=util.get_headers(client.api_key),
                )
                user_json = request_user.json()

                msg = (
                    "Olá " + user_json["nome"] + ", informe qual opção deseja consultar"
                )

                return menu_user(user_json, msg), 201
            else:
                return invalid_information(msg_menu, ""), 201

    elif request_mz.status_code == 404:
        return {"error": "Request must be JSON"}, 404


@api.route("/")
class NectarController(Resource):
    def post(self):

        if request.is_json:
            mz = request.get_json()
            phone = mz["contact"]["key"]

            request_mz = requests.get(
                client.api + "telefone/" + phone,
                params=params,
                headers=util.get_headers(client.api_key),
            )

            return getUser(request_mz, "home_menu")

        return {"error": "Request must be JSON"}, 415


@api.route("/search_cpf")
class PersonCpfController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(
                client.api + "cpf/" + text,
                params=params,
                headers=util.get_headers(client.api_key),
            )

            return getUser(request_mz, menu_cpf)

        return {"error": "Request must be JSON"}, 415


@api.route("/search_cnpj")
class PersonCnpjController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(
                client.api + "cnpj/" + text,
                params=params,
                headers=util.get_headers(client.api_key),
            )

            return getUser(request_mz, menu_cnpj)

        return {"error": "Request must be JSON"}, 415


@api.route("/search_phone")
class PersonPhoneController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(
                client.api + "telefone/" + text,
                params=params,
                headers=util.get_headers(client.api_key),
            )

            return getUser(request_mz, menu_phone)

        return {"error": "Request must be JSON"}, 415


@api.route("/search_email")
class PersonEmailController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(
                client.api + "email/" + text,
                params=params,
                headers=util.get_headers(client.api_key),
            )

            return getUser(request_mz, menu_email)

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
            elif data["user"]["id"]:

                user_id = data["user"]["id"]
                user_cpf = data["user"]["cpf"]

                print(f"User id: {user_id} User CPF: {user_cpf}")

                request_mz = requests.get(
                    client.api + str(user_id) + "/proximaAtividade",
                    params=params,
                    headers=util.get_headers(client.api_key),
                )

                print(f"Status Code: {request_mz.status_code}, Url: {request_mz.url}")

                if request_mz.status_code == 200:
                    print("The request was a success!")
                    json_response = request_mz.json()
                    json_size = len(json_response)

                    print(
                        f"Status Code: {request_mz.status_code}, Content: {json_response}, Size Json {json_size}"
                    )

                    if json_size == 0:
                        return (
                            invalid_information(
                                menu_next_activity,
                                get_url() + "/search_next_activity",
                            ),
                            201,
                        )
                    else:
                        title = json_response["titulo"]
                        description = json_response["descricao"]
                        responsible = json_response["responsavel"]["nome"]
                        client_name = json_response["cliente"]["nome"]
                        task = json_response["tarefaTipo"]["nome"]
                        data_limit = json_response["dataLimite"]

                        f = "%Y-%m-%dT%H:%M:%S.%fZ"
                        data_limit_f = datetime.strptime(data_limit, f)

                        data_create_f = datetime.strptime(data_limit, f)

                        msg_information = (
                            f"Titulo: {title},"
                            f"\n Descrição: {description},"
                            f"\n Responsavel: {responsible},"
                            f"\n Cliente: {client_name},"
                            f"\n Tarefa: {task},"
                            f"\n Criada em: {data_create_f},"
                            f"\n Limite de entrega: {data_limit_f}"
                        )

                        return response_information(msg_information, ""), 201

                elif request_mz.status_code == 404:
                    return {"error": "Request must be JSON"}, 404

        return {"error": "Request must be JSON"}, 415
