from pymongo import MongoClient
from dotenv import dotenv_values
import urllib.parse

config = dotenv_values("../.env")


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    username = urllib.parse.quote_plus(config['MONGO_DB_USERNAME'])
    password = urllib.parse.quote_plus(config['MONGO_DB_PASSWORD'])

    connection_string = f"mongodb+srv://{username}:{password}@vericreds.gjtihuc.mongodb.net/vericreds-db"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(connection_string)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client["vericreds-db"]


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    db = get_database()
