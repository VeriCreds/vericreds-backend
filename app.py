from flask import Flask, render_template, request
from util import mongo
from moralis import auth
from flask_cors import CORS
from dotenv import dotenv_values


app = Flask(__name__)
CORS(app)

config = dotenv_values("./.env")
api_key = config["MORALIS_API_KEY"]


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'
    # print(mongo.users)
    return render_template('index.html')


@app.route('/requestChallenge', methods=["GET"])
def reqChallenge():
    args = request.args
    body = {
        "domain": "localhost:3000",
        "chainId": args.get("chainId"),
        "address": args.get("address"),
        "statement": "Please confirm login",
        "uri": "http://localhost:3000/",
        "expirationTime": "2023-01-01T00:00:00.000Z",
        "notBefore": "2023-01-01T00:00:00.000Z",
        "resources": ['https://docs.moralis.io/'],
        "timeout": 30,
    }
    result = auth.challenge.request_challenge_evm(
        api_key=api_key,
        body=body,
    )
    return result


@app.route('/verifyChallenge', methods=["GET"])
def verifyChallenge():
    args = request.args
    body = {
        "message": args.get("message"),
        "signature": args.get("signature"),
    }
    result = auth.challenge.verify_challenge_evm(
        api_key=api_key,
        body=body
    )
    return result


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, load_dotenv=True)
