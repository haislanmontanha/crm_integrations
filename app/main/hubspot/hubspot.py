# app.py
import os
import requests
import json
from flask import Flask, request, jsonify
from datetime import datetime


app = Flask(__name__)

api_contact = 'https://api.hubapi.com/crm/v3/objects/contacts/'

api_local= "https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us30.gitpod.io/"

menu_cpf = "cpf"
menu_cnpj = "cnpj"
menu_telefone = "telefone"
menu_email = "email"

api_key = '1558c7be-9e9c-40f2-931a-a72be68a200f'
headers = {
    'Accept': 'application/json', 
    'Access-Token':'1558c7be-9e9c-40f2-931a-a72be68a200f',
    'User-Agent':'request'}

headers_post = { 'Content-Type': 'application/json'}

params = {'api_token': '1558c7be-9e9c-40f2-931a-a72be68a200f'}

def menu_inicial(msg):
    return {
        "type":"MENU",
        "text": msg,
        "attachments":[
            {
                "position":"BEFORE",
                "type":"IMAGE",
                "name":"image.png",
                "url":"https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
            }
        ],
        "items":[
            {
                "number":1,
                "text":"CPF",
                "callback":{
                    "endpoint": api_local+"hubspot_cpf",
                    "data":{
                    }
                }
            },
            {
                "number":2,
                "text":"CNPJ",
                "callback":{
                    "endpoint": api_local+"hubspot_cnpj",
                    "data":{
                    }
                }
            },
            {
                "number":3,
                "text":"Telefone",
                "callback":{
                    "endpoint": api_local+"hubspot_telefone",
                    "data":{
                    }
                }
            },
            {
                "number":4,
                "text":"Email",
                "callback":{
                    "endpoint": api_local+"hubspot_email",
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
                "url":"https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
            }
        ],
        "items":[
            {
                "number":1,
                "text":"Próxima tarefa",
                "callback":{
                    "endpoint": api_local+"hubspot_proximaAtividade",
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
            "url": "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
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
                "url":"https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
            },
            {
                "position":"AFTER",
                "type":"DOCUMENT",
                "name":"document.pdf",
                "url":"http://www.africau.edu/images/default/sample.pdf"
            }
        ]
    }

def invalid_information(msg_menu):
    if msg_menu == menu_cpf:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"hubspot_cpf")
    elif msg_menu == menu_cnpj:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"hubspot_cnpj")
    elif msg_menu == menu_telefone:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"hubspot_telefone")
    elif msg_menu == menu_email:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"hubspot_email")
    else:
        return menu_inicial("Olá, por favor informe uma das seguintes informações.")

def getUser(request_mz, msg_menu):

    if (request_mz.status_code == 200):
        print("The request was a success!")
        # Code here will only run if the request is successful
        resposta_json = request_mz.json()
        json_size = len(resposta_json)

        print(f"Status Code: {request_mz.status_code}, Content: {resposta_json}, Size Json {json_size}")

        msg_erro_menu = "Olá, não encontramos seu contato pelo "+msg_menu+". Informe uma das seguintes opções: "

        if json_size == 0:
            return invalid_information(msg_menu), 201
        else:

            s1 = json.dumps(resposta_json)
            user = json.loads(s1)
            
            if 'results' in user:

                user_json = resposta_json[1]["results"]['properties']['firstname']
            
                msg = "Olá "+user_json['nome']+", informe qual opção deseja consultar"

                return menu_user(user_json, msg), 201
            else:
                return invalid_information(msg_menu), 201
                
    elif (request_mz.status_code == 404):
        return {"error": "Request must be JSON"}, 404

@app.get("/")
def start():
    return "Hello World!", 201

@app.post("/hubspot")
def start_hubspot():
    if request.is_json:
        mz = request.get_json()
        nome = mz["contact"]["name"]

        data = {
            "filterGroups":[
            {
                "filters":[
                {
                    "propertyName": "firstname",
                    "operator": "EQ",
                    "value": nome
                }
                ]
            }
            ]
        }

        request_mz = requests.post(api_contact+'search?hapikey='+api_key, data=json.dumps(data), headers=headers_post)
        
        return getUser(request_mz, "menu_inicial")

    return {"error": "Request must be JSON"}, 415

@app.post("/hubspot_cpf")
def getcpf_hubspot():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'cpf/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_cpf)

    return {"error": "Request must be JSON"}, 415

@app.post("/hubspot_cnpj")
def getcnpj_hubspot():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'cnpj/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_cnpj)

    return {"error": "Request must be JSON"}, 415

@app.post("/hubspot_telefone")
def gettelefone_hubspot():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'telefone/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_telefone)

    return {"error": "Request must be JSON"}, 415

@app.post("/hubspot_email")
def getemail_hubspot():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'email/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_email)

    return {"error": "Request must be JSON"}, 415

@app.post("/hubspot_proximaAtividade")
def getproximaAtividade_hubspot():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]
        data = mz["data"]
        data_size = len(data)

        print(f"Content: {data} Size: {data_size}")

        if data_size==0:
            return menu_inicial("Olá, não foi possivel encontrar nenhuma atividade, por favor informe uma das seguintes informações.")
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
                        return invalid_information(menu_proximaAtividade), 201
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

