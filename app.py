import jwt, os
from dotenv import dotenv_values
from flask import Flask, render_template, request
from util import mongo
from cerberus import Validator


app = Flask(__name__)

config = dotenv_values("../.env")

from models import User
from auth_middleware import token_required


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'
    print(mongo.users)
    return render_template('index.html')


@app.route("/users/", methods=["POST"])
def add_user():
    try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = Validator(**user)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().create(**user)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        return {
            "message": "Successfully created new user",
            "data": user
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500


@app.route("/users/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        schema = {
            'email': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            },
            'password': {
                'string': {'minlength': 8, 'maxlength': 50}
            }}
        v = Validator(schema)
        credentials = {'email': data.get('email'), 'password': data.get('password')}
        is_validated = v.validate(credentials)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().login(
            data["email"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = jwt.encode(
                    {"user_id": user["_id"]},
                    app.config["SECRET_KEY"],
                    algorithm="HS512"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500




if __name__ == '__main__':

    SECRET_KEY = config['SECRET_KEY'] or 'this is a secret'
    print(SECRET_KEY)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.run(host="127.0.0.1", debug=True, load_dotenv=True)

