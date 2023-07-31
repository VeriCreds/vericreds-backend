from flask import Flask, render_template, request
from datetime import datetime, timedelta, timezone
from util import mongo
from moralis import auth
from flask_cors import CORS
from dotenv import dotenv_values


app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

config = dotenv_values("./.env")
api_key = config["MORALIS_API_KEY"]

print("api_key", api_key)

@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'
    # print(mongo.users)
    return render_template('index.html')


@app.route('/requestChallenge', methods=["GET"])
def reqChallenge():
    args = request.args

    # get current UTC time
    now = datetime.now(timezone.utc)

    # create timestamps for expiration and not_before
    # for instance, the message will be valid for the next 5 minutes
    expiration_time = now + timedelta(minutes=5)
    not_before_time = now

    # format as ISO 8601
    expiration_time_str = expiration_time.isoformat().replace("+00:00", "Z")
    not_before_time_str = not_before_time.isoformat().replace("+00:00", "Z")

    body = {
        "domain": "localhost:3000",
        "chainId": args.get("chainId"),
        "address": args.get("address"),
        "statement": "Please confirm login",
        "uri": "http://localhost:3000/",
        "expirationTime": expiration_time_str,
        "notBefore": not_before_time_str,
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

    # Log the message and the current server time
    print("Message: ", args.get("message"))
    print("Current Server Time: ", datetime.now().isoformat())

    result = auth.challenge.verify_challenge_evm(
        api_key=api_key,
        body=body
    )
    return result


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, load_dotenv=True)
