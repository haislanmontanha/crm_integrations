from app import app
from os import environ

if __name__ == "__main__":
    app.debug = True
    app.run()
