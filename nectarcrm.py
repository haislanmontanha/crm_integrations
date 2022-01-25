
import os
import requests

api_contact = 'https://app.nectarcrm.com.br/crm/api/1/contatos/'
api_oportunidades = 'https://app.nectarcrm.com.br/crm/api/1/oportunidades/'

headers = {
    'Accept': 'application/json', 
    'Access-Token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw',
    'User-Agent':'request'}

params = {'api_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw'}

def getPedido(operacao):

    if operacao == '1':    
        getCpf()
        input('PRESS ENTER')
        os.system('clear')
    
    elif operacao == '2':    
        getTelefone()
        input('PRESS ENTER')
        os.system('clear')

    elif operacao == '3':    
        getEmail()
        input('PRESS ENTER')
        os.system('clear')

    elif operacao == '4':    
        getCNPJ()
        input('PRESS ENTER')
        os.system('clear')
    else:
        print('Operação Invalida')
        input('PRESS ENTER')
        os.system('clear')

def getCpf():
    # Perguntar o CPF 38724981850
    cpf = str(input('Digite o CPF: '))

    request = requests.get(api_contact+'cpf/'+cpf, params=params, headers=headers)
    getDataContatos(request)

def getCNPJ():
    # Perguntar o CNPJ 06087547000152
    cnpj = str(input('Digite o CNPJ: '))

    request = requests.get(api_contact+'cnpj/'+cnpj, params=params, headers=headers)
    getDataContatos(request)

def getTelefone():
    # Perguntar o Telefone +5514991670521
    telefone = str(input('Digite o telefone: '))

    request = requests.get(api_contact+'telefone/'+telefone, params=params, headers=headers)
    getDataContatos(request)

def getEmail():
    # Perguntar o email eloide@gmail.com
    email = str(input('Digite o email: '))

    request = requests.get(api_contact+'email/'+email, params=params, headers=headers)
    getDataContatos(request)
       
def getUser(userId):
    request = requests.get(api_contact+str(userId), params=params, headers=headers)
    resposta_json = request.json()
    # print(resposta_json)

    welcomeUser(resposta_json)

def welcomeUser(user):
    # Perguntar qual é o tipo de operação
    operacao = input('Olá '+user['nome']+' escolhe o que deseja: '+'\n'+
                    '1 - Próxima Atividade'+'\n'+
                    '2 - Oportunidade em aberto'+'\n'+
                     '0 - MENU INICIAL'+'\n')

    if operacao == '0' or operacao == '0':
        crm_nectar()
        os.system('clear')
    elif operacao == '1':    
        getAtividadeByUserID(user['cpf'])
        input('PRESS ENTER')
        os.system('clear')
    
    elif operacao == '2':    
        getOportunidadeByUserID(user['id'])
        input('PRESS ENTER')
        os.system('clear')
    else:
        print('Operação Invalida')
        input('PRESS ENTER')
        os.system('clear')

def getAtividadeByUserID(cpf):
    request = requests.get(api_oportunidades+str(cpf)+'/proximaAtividade', params=params, headers=headers)
    resposta_json = request.json()

def getOportunidadeByUserID(userId):
    request = requests.get(api_oportunidades+'contatoId/'+str(userId), params=params, headers=headers)
    resposta_json = request.json()
    oportunidadeId = resposta_json[0]["id"]
    getOportunidadeById(oportunidadeId)

def getOportunidadeById(oportunidadeId):
    request = requests.get(api_oportunidades+str(oportunidadeId), params=params, headers=headers)
    oportunidade = request.json()

    operacao = input(str(oportunidade['nome'])+'\n'+
                        'Codigo: '+str(oportunidade['codigo'])+'\n'+
                        'Etapa Nome: '+str(oportunidade['etapaNome'])+'\n'+
                        'Valor Avulso: '+str(oportunidade['valorAvulso'])+'\n'+
                        'Valor Mensal: '+str(oportunidade['valorMensal'])+'\n'+
                        'Valor Total: '+str(oportunidade['valorTotal'])+'\n'+
                        '0 - MENU INICIAL'+'\n')
    if operacao == '0' or operacao == '0':
        crm_nectar()
        os.system('clear')

def crm_nectar():
    while True:
        # Perguntar qual é o tipo de operação
        operacao = input('1 - CPF'+'\n'+
                        '2 - Telefone'+'\n'+
                        '3 - Email'+'\n'+
                        '4 - CNPJ'+'\n'+
                        '0 - SAIR'+'\n')
        if operacao == '0' or operacao == '0':
            break
        else:
            getPedido(operacao)

def getDataContatos(request):

    if (request.status_code == 200):
        # print("The request was a success!")
        # Code here will only run if the request is successful
        # print(request.url)
        # print(f"Status Code: {request.status_code}, Content: {request.json()}")
        resposta_json = request.json()
        # print(resposta_json[0]["id"])

        userId = resposta_json[0]["id"]
        getUser(userId)

    elif (request.status_code == 404):
        print("Result not found!")
        # Code here will react to failed requests
 
if __name__ == '__main__':
   crm_nectar()