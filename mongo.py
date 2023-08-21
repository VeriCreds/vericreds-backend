import os
import urllib.parse
from flask import Flask
from flask_pymongo import PyMongo


class MongoConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoConnection._instance is None:
            MongoConnection._instance = MongoConnection.connect_to_db()
        return MongoConnection._instance

    @staticmethod
    def connect_to_db():
        app = Flask(__name__, template_folder='routes')

        username = urllib.parse.quote_plus(os.getenv("MONGO_DB_USERNAME"))
        password = urllib.parse.quote_plus(os.getenv("MONGO_DB_PASSWORD"))

        app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@vericreds.gjtihuc.mongodb.net/vericreds-db"
        return PyMongo(app)
