from flask_restx import Resource, Namespace
from app.main.client.client import Client


utils = Namespace("Utils", description="Classe de informações")

PRODUCTION = True


class Utils(Resource):
    def get_url(self):
        if bool(PRODUCTION):
            return "https://crmintegrations.herokuapp.com/api/"
        else:
            return "http://localhost:5500/api/"

    def get_headers(self, api_key):
        return {
            "Accept": "application/json",
            "Access-Token": api_key,
            "User-Agent": "request",
        }

    def get_headers_G(self, api_key):
        return {
            "Accept": "application/json",
            "Authorization": "Basic " + api_key,
            "User-Agent": "request",
        }

    def get_nectar(self):
        return Client(
            "https://app.nectarcrm.com.br/crm/api/1/contatos/",
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw",
            "https://leadster.com.br/blog/wp-content/uploads/2021/09/8.png",
        )

    def get_hubspot(self):
        return Client(
            "https://api.hubapi.com/crm/v3/objects/",
            "1558c7be-9e9c-40f2-931a-a72be68a200f",
            "https://leadster.com.br/blog/wp-content/uploads/2021/09/9.png",
        )

    def get_rdstation(self):
        return Client(
            "https://api.rd.services/platform/contacts/",
            "adf54a9d729dea6410155f75bf251198",
            "https://leadster.com.br/blog/wp-content/uploads/2021/09/3.png",
        )

    def get_sales_funnel(self):
        return Client(
            "https://sandbox.funildevendas.com.br/api/",
            "7c13e23a-670c-47c9-b1a5-ac0ea6575792",
            "https://app.funildevendas.com.br/Content/assets/img/funildevendas.png",
        )
