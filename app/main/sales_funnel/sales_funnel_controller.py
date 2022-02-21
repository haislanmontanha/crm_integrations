import requests
import json
from flask import request
from flask_restx import Resource, Namespace
from app.main.utils.utils import Utils

api = Namespace("Funil de Vendas", description="Integração client CRM")

util = Utils()
client = util.get_sales_funnel()

headers_post = {"Content-Type": "application/json"}
params = {"IntegrationKey": client.api_key}

menu_cpf = "cpf"
menu_cnpj = "cnpj"
menu_phone = "telefone"
menu_email = "email"


def get_url():
    return util.get_url() + "sales_funnel/"


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
class SalesFunnelController(Resource):
    def post(self):

        if request.is_json:
            mz = request.get_json()
            text = mz["text"]

            data = {
                "oportunidades": [
                    {
                        "codigo_vendedor": 48575,
                        "codigo_metodologia": 1,
                        "codigo_etapa": 1,
                        "codigo_canal_venda": 85439,
                        "titulo": "Título da oportunidade",
                        "valor": 100,
                        "empresa": {
                            "nome": "Nome da empresa",
                            "cnpj": "",
                            "ie": "",
                            "segmento": "",
                            "endereco_completo": {
                                "logradouro": "",
                                "numero": "",
                                "complemento": "",
                                "bairro": "",
                                "cidade": "",
                                "uf": "",
                                "cep": "",
                            },
                        },
                        "contato": {
                            "nome": "Nome do contato",
                            "email": "email@contato.com.br",
                            "telefone1": "",
                            "telefone2": "",
                            "cargo": "",
                            "cpf": "",
                        },
                    }
                ]
            }

            request_mz = requests.post(
                client.api + "opportunity?IntegrationKey" + client.api_key,
                data=json.dumps(data),
                headers=headers_post,
            )

            print(
                f"Status Code: {request_mz.status_code}, URL: {request_mz.url} Return: {request_mz.headers}"
            )

            return getUser(request_mz, "home_menu")

        return {"sucess": "Post Sales Funnel"}, 201
