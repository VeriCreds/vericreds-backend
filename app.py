from dotenv import dotenv_values
from flask import Flask, render_template
from util import mongo

app = Flask(__name__)

config = dotenv_values("../.env")


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'
    print(mongo.users)
    return render_template('index.html')


if __name__ == '__main__':

    SECRET_KEY = config['SECRET_KEY'] or 'this is a secret'
    print(SECRET_KEY)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.run(host="127.0.0.1", debug=True, load_dotenv=True)

