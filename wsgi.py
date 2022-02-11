from app import app
from os import environ

if __name__ == "__main__":
    SERVER_HOST = environ.get("SERVER_HOST", "https://crmintegrations.herokuapp.com/")
    app.run(
        host=SERVER_HOST,
        port=5500,
        debug=(not environ.get("ENV") == "PRODUCTION"),
        threaded=True,
    )
