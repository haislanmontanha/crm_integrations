import requests

def buscar_dados():
    request = requests.get('https://reqbin.com/echo/get/json', 
                 headers={'Accept': 'application/json'})
    print(f"Status Code: {request.status_code}, Content: {request.json()}")

def buscar_list():
    request_list = requests.get('http://dummy.restapiexample.com/api/v1/employees',
                         headers={
                             'Accept': 'application/json', 
                             'User-Agent':'request'})

    resposta_json = request_list.json()
    
    print(resposta_json['data'])

if __name__ == '__main__':
    buscar_list()