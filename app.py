from dotenv import dotenv_values
from flask import Flask, render_template
from routes.users import users
import urllib.parse
from flask_pymongo import PyMongo


app = Flask(__name__, template_folder='routes')


config = dotenv_values("../.env")
username = urllib.parse.quote_plus(config['MONGO_DB_USERNAME'])
password = urllib.parse.quote_plus(config['MONGO_DB_PASSWORD'])

app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@vericreds.gjtihuc.mongodb.net/vericreds-db"
mongo = PyMongo(app)


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'
    print(mongo.db.users)
    return render_template('index.html')


app.register_blueprint(users, url_prefix="/users/")


if __name__ == '__main__':

    SECRET_KEY = config['SECRET_KEY'] or 'this is a secret'
    # print(SECRET_KEY)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.run(host="127.0.0.1", debug=True, load_dotenv=True)
