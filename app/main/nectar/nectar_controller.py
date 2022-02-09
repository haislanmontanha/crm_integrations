import os
import requests
import json
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace
from datetime import datetime

api = Namespace('Nectar',description='Integração Nectar CRM')

api_contact = 'https://app.nectarcrm.com.br/crm/api/1/contatos/'
url_logo = "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"

api_local= "https://5500-haislanmontanha-gev-55t1r8kq5qw.ws-us30.gitpod.io/api/nectar/"

menu_cpf = "cpf"
menu_cnpj = "cnpj"
menu_phone = "telefone"
menu_email = "email"
menu_next_activity = "next_activity"

headers = {
    'Accept': 'application/json', 
    'Access-Token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw',
    'User-Agent':'request'}

params = {'api_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw'}

def json_start():
    return {
            "id": 215123,
            "text": "Hello world!",
            "contact": {
                "uid": "15295",
                "type": "WHATSAPP",
                "key": "+5514991670521",
                "name": "Haislan",
                "fields": {
                "cpf": "38724981850",
                "celular": "(11) 11111-1111"
                }
            },
            "data": {}
        }

def home_menu(msg):
    return {
        "type":"MENU",
        "text": msg,
        "attachments":[
            {
                "position":"BEFORE",
                "type":"IMAGE",
                "name":"image.png",
                "url": url_logo
            }
        ],
        "items":[
            {
                "number":1,
                "text":"CPF",
                "callback":{
                    "endpoint": api_local+"/search_cpf",
                    "data":{
                    }
                }
            },
            {
                "number":2,
                "text":"CNPJ",
                "callback":{
                    "endpoint":api_local+"/search_cnpj",
                    "data":{
                    }
                }
            },
            {
                "number":3,
                "text":"Telefone",
                "callback":{
                    "endpoint": api_local+"/search_phone",
                    "data":{
                    }
                }
            },
            {
                "number":4,
                "text":"Email",
                "callback":{
                    "endpoint": api_local+"/search_email",
                    "data":{
                    }
                }
            }
        ]
    }

def menu_user(user_json, msg):
    return {
        "type":"MENU",
        "text": msg,
        "attachments":[
            {
                "position":"BEFORE",
                "type":"IMAGE",
                "name":"image.png",
                "url": url_logo
            }
        ],
        "items":[
            {
                "number":1,
                "text":"Próxima tarefa",
                "callback":{
                    "endpoint": api_local+"/search_next_activity",
                    "data":{
                        "user": user_json
                    }
                }
            }
        ]
    }

def response_question(text, callback):
    return {
        "type": "QUESTION",
        "text": text,
        "attachments": [{
            "position": "BEFORE",
            "type": "IMAGE",
            "name": "image.png",
            "url":url_logo
        }],
        "callback": {
            "endpoint": callback,
            "data": {
                
            }
        }
    }

def response_information(text, urldoc):
    return {
        "type":"INFORMATION",
        "text":text,
        "attachments":[
            {
                "position":"BEFORE",
                "type":"IMAGE",
                "name":"image.png",
                "url": url_logo
            },
            {
                "position":"AFTER",
                "type":"DOCUMENT",
                "name":"document.pdf",
                "url": urldoc
            }
        ]
    }

def invalid_information(msg_menu, url_callback):
    if msg_menu == menu_cpf:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", url_callback)
    elif msg_menu == menu_cnpj:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", url_callback )
    elif msg_menu == menu_phone:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", url_callback)
    elif msg_menu == menu_email:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", url_callback )
    else:
        return home_menu("Olá, por favor informe uma das seguintes informações.")

def getUser(request_mz, msg_menu):

    if (request_mz.status_code == 200):
        print("The request was a success!")
        resposta_json = request_mz.json()
        json_size = len(resposta_json)

        print(f"Status Code: {request_mz.status_code}, Content: {resposta_json}, Size Json {json_size}")

        msg_erro_menu = "Olá, não encontramos seu contato pelo "+msg_menu+". Informe uma das seguintes opções: "

        if json_size == 0:
            return invalid_information(msg_menu, ""), 201
        else:

            s1 = json.dumps(resposta_json)
            user = json.loads(s1)
            
            if 'message' not in user:

                userId = resposta_json[0]["id"]
                request_user = requests.get(api_contact+str(userId), params=params, headers=headers)
                user_json = request_user.json()

                msg = "Olá "+user_json['nome']+", informe qual opção deseja consultar"

                return menu_user(user_json, msg), 201
            else:
                return invalid_information(msg_menu,""), 201
                
    elif (request_mz.status_code == 404):
        return {"error": "Request must be JSON"}, 404

@api.route('/')
class NectarController(Resource):

    def post(self):

        if request.is_json:
            mz = request.get_json()
            telefone = mz["contact"]["key"]

            request_mz = requests.get(api_contact+'telefone/'+telefone, params=params, headers=headers) 
            
            return getUser(request_mz, "home_menu")

        return {"error": "Request must be JSON"}, 415

@api.route('/search_cpf')#classe que atende requisições 
class PersonCpfController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(api_contact+'cpf/'+text, params=params, headers=headers)

            return getUser(request_mz, menu_cpf)

        return {"error": "Request must be JSON"}, 415

@api.route('/search_cnpj')#classe que atende requisições 
class PersonCnpjController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(api_contact+'cnpj/'+text, params=params, headers=headers)

            return getUser(request_mz, menu_cnpj)

        return {"error": "Request must be JSON"}, 415

@api.route('/search_phone')#classe que atende requisições 
class PersonPhoneController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(api_contact+'telefone/'+text, params=params, headers=headers)

            return getUser(request_mz, menu_phone)

        return {"error": "Request must be JSON"}, 415

@api.route('/search_email')#classe que atende requisições 
class PersonEmailController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]

            request_mz = requests.get(api_contact+'email/'+text, params=params, headers=headers)

            return getUser(request_mz, menu_email)

        return {"error": "Request must be JSON"}, 415

@api.route('/search_next_activity')#classe que atende requisições 
class PersonNextActivityController(Resource):
    def post(self):
        if request.is_json:

            mz = request.get_json()
            text = mz["text"]
            data = mz["data"]
            data_size = len(data)

            print(f"Content: {data} Size: {data_size}")

            if data_size==0:
                return home_menu("Olá, não foi possivel encontrar nenhuma atividade, por favor informe uma das seguintes informações.")
            elif data["user"]["id"]:

                user_id = data["user"]["id"]
                user_cpf = data["user"]["cpf"]

                print(f"User id: {user_id} User CPF: {user_cpf}")

                request_mz = requests.get(api_contact+str(user_id)+'/proximaAtividade', params=params, headers=headers)

                print(f"Status Code: {request_mz.status_code}, Url: {request_mz.url}")

                if (request_mz.status_code == 200):
                        print("The request was a success!")
                        # Code here will only run if the request is successful
                        resposta_json = request_mz.json()
                        json_size = len(resposta_json)

                        print(f"Status Code: {request_mz.status_code}, Content: {resposta_json}, Size Json {json_size}")

                        if json_size == 0:
                            return invalid_information(menu_next_activity, util.getUrlLocal()+"nectarcrm_proximaAtividade"), 201
                        else:
                            titulo = resposta_json["titulo"]
                            descricao = resposta_json["descricao"]
                            responsavel = resposta_json["responsavel"]["nome"]
                            cliente = resposta_json["cliente"]["nome"]
                            tarefa = resposta_json["tarefaTipo"]["nome"]
                            dataLimite = resposta_json["dataLimite"]
                            dataCriacao = resposta_json["dataCriacao"]

                            f = "%Y-%m-%dT%H:%M:%S.%fZ"
                            dataLimite_f = datetime.strptime(dataLimite, f)

                            dataCriacao_f = datetime.strptime(dataLimite, f)

                            msg_information = f"Titulo: {titulo},\n Descrição: {descricao},\n Responsavel: {responsavel},\n Cliente: {cliente},\n Tarefa: {tarefa},\n Criada em: {dataCriacao_f},\n Limite de entrega: {dataLimite_f}"

                            return response_information(msg_information, ""), 201
                                
                elif (request_mz.status_code == 404):
                    return {"error": "Request must be JSON"}, 404

        return {"error": "Request must be JSON"}, 415