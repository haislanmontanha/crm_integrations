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
def add_nectarcrm():
    if request.is_json:
        wz = request.get_json()
        telefone = wz["contact"]["key"]

        request_telefone = requests.get(api_contact+'telefone/'+telefone, params=params, headers=headers)
        
        if (request_telefone.status_code == 200):
            # print("The request was a success!")
            # Code here will only run if the request is successful
            # print(request.url)
            # print(f"Status Code: {request.status_code}, Content: {request.json()}")
            resposta_json = request_telefone.json()
            # print(resposta_json[0]["id"])

            userId = resposta_json[0]["id"]
            request_user = requests.get(api_contact+str(userId), params=params, headers=headers)
            resposta_json = requrequest_userest.json()
            # print(resposta_json)
            return resposta_json, 201

        elif (request_telefone.status_code == 404):
            print("Result not found!")
        #sreturn wz, 201
    return {"error": "Request must be JSON"}, 415


