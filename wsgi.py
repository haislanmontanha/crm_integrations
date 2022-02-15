from app import app
from os import environ

if __name__ == "__main__":
    #SERVER_HOST = environ.get("SERVER_HOST", "localhost")
    port = int(os.environ.get("PORT", 5500))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=(not environ.get("ENV") == "PRODUCTION"),
        threaded=True,
    )
