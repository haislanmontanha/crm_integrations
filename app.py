# app.py
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

api_contact = 'https://app.nectarcrm.com.br/crm/api/1/contatos/'
api_oportunidades = 'https://app.nectarcrm.com.br/crm/api/1/oportunidades/'

headers = {
    'Accept': 'application/json', 
    'Access-Token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw',
    'User-Agent':'request'}

params = {'api_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw'}

@app.route("/")
def nectarcrm():
  return "Hello, World!"

@app.post("/nectarcrm")
def start_nectarcrm():
    if request.is_json:
        wz = request.get_json()
        telefone = wz["contact"]["key"]

        request_telefone = requests.get(api_contact+'telefone/'+telefone, params=params, headers=headers)
        
        if (request_telefone.status_code == 200):
            print("The request was a success!")
            # Code here will only run if the request is successful
            resposta_json = request_telefone.json()
            json_size = len(resposta_json)

            print(f"Status Code: {request_telefone.status_code}, Content: {request_telefone.json()}, Size Json {json_size}")

            if json_size == 0:
                json_menu = {
                    "type":"MENU",
                    "text":"Olá, não encontramos seu contato pelo número do celular. Informe qual o opção que deseja informar: ",
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
                                "endpoint":"https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us29.gitpod.io/nectarcrm_cpf",
                                "data":{
                                }
                            }
                        },
                        {
                            "number":2,
                            "text":"CNPJ",
                            "callback":{
                                "endpoint":"https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us29.gitpod.io/nectarcrm_cnpj",
                                "data":{
                                }
                            }
                        },
                        {
                            "number":3,
                            "text":"Telefone",
                            "callback":{
                                "endpoint":"https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us29.gitpod.io/nectarcrm_telefone",
                                "data":{
                                }
                            }
                        },
                        {
                            "number":4,
                            "text":"Email",
                            "callback":{
                                "endpoint":"https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us29.gitpod.io/nectarcrm_email",
                                "data":{
                                }
                            }
                        }
                    ]
                }
                return json_menu, 201
            else:
                userId = resposta_json[0]["id"]
                request_user = requests.get(api_contact+str(userId), params=params, headers=headers)
                resposta_json = request_user.json()

                json_question = {
                    "type": "QUESTION",
                    "text": "Olá "+resposta_json['nome']+", informe o email para buscar a oportunidade em aberto.",
                    "attachments": [{
                        "position": "BEFORE",
                        "type": "IMAGE",
                        "name": "image.png",
                        "url": "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
                    }],
                    "callback": {
                        "endpoint": "https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us29.gitpod.io/nectarcrm_oportunidade",
                        "data": {
                            
                        }
                    }
                    }

                return json_question, 201

        elif (request_telefone.status_code == 404):
            print("Result not found!")
    return {"error": "Request must be JSON"}, 415


@app.post("/nectarcrm_oportunidade")
def getoportunidade_nectarcrm():
    if request.is_json:
        return {'msg':'Chegou aqui - nectarcrm_oportunidade'}, 201
    elif (request_telefone.status_code == 404):
        print("Result not found!")
        return {'msg':'Result not found!'}, 201
    #sreturn wz, 201
    return {"error": "Request must be JSON"}, 415


@app.post("/nectarcrm_cpf")
def getcpf_nectarcrm():
    if request.is_json:
        return {'msg':'Chegou aqui - nectarcrm_cpf'}, 201
    elif (request_telefone.status_code == 404):
        print("Result not found!")
        return {'msg':'Result not found!'}, 201
    #sreturn wz, 201
    return {"error": "Request must be JSON"}, 415

@app.post("/nectarcrm_cnpj")
def getcnpj_nectarcrm():
    if request.is_json:
        return {'msg':'Chegou aqui - nectarcrm_cnpj'}, 201
    elif (request_telefone.status_code == 404):
        print("Result not found!")
        return {'msg':'Result not found!'}, 201
    #sreturn wz, 201
    return {"error": "Request must be JSON"}, 415

@app.post("/nectarcrm_telefone")
def gettelefone_nectarcrm():
    if request.is_json:
        return {'msg':'Chegou aqui - nectarcrm_telefone'}, 201
    elif (request_telefone.status_code == 404):
        print("Result not found!")
        return {'msg':'Result not found!'}, 201
    #sreturn wz, 201
    return {"error": "Request must be JSON"}, 415


@app.post("/nectarcrm_email")
def getemail_nectarcrm():
    if request.is_json:
        return {'msg':'Chegou aqui = nectarcrm_email'}, 201
    elif (request_telefone.status_code == 404):
        print("Result not found!")
        return {'msg':'Result not found!'}, 201
    #sreturn wz, 201
    return {"error": "Request must be JSON"}, 415
