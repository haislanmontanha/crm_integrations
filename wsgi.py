from app import app
from os import environ

if __name__ == "__main__":
    SERVER_HOST = environ.get("SERVER_HOST", "0.0.0.0")
    app.run(
        host=SERVER_HOST,
        port=5005,
        debug=(not environ.get("ENV") == "PRODUCTION"),
        threaded=True,
    )
