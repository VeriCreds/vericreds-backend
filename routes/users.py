import jwt
from flask import Blueprint, request, jsonify
from cerberus import Validator
from models import User
from auth_middleware import token_required
import app


users = Blueprint('users', __name__, template_folder='routes')


@users.route('/', methods=['POST'])
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
        user = User().register_user(**user)
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


@users.route("/login", methods=["POST"])
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
            data["email_address"],
            data["password"]
        )
        if user:
            try:
                # The token will expire after 24 hrs
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


@users.route("/", methods=["GET"])
def get_all_users():
    all_users = User.get_all_users()
    return jsonify({
        "message": "Successfully retrieved all user data",
        "data": all_users
    })


@users.route("/user_id", methods=["GET"])
# @token_required
def get_single_user(user_id):
    user = User.get_user_by_id(user_id)
    return jsonify({
        "message": "Successfully retrieved user profile",
        "data": user
    })


@users.route("/", methods=["PUT"])
# @token_required
def update_user(current_user):
    try:
        user = request.json
        if user.get("first_name"):
            if user.get("last_name"):
                if user.get("email_address"):
                    user = User().update_user(current_user["_id"], user["first_name"], user["last_name"], user["email_address"])
                    return jsonify({
                        "message": "Successfully updated user's data",
                        "data": user
                    }), 201
                else:
                    user = User().update_user(current_user["_id"], user["first_name"], user["last_name"])
                    return jsonify({
                        "message": "Successfully updated user's data",
                        "data": user
                    }), 201
        return {
            "message": "Invalid data, you can only update your account name!",
            "data": None,
            "error": "Bad Request"
        }, 400
    except Exception as e:
        return jsonify({
            "message": "failed to update account",
            "error": str(e),
            "data": None
        }), 400


@users.route("/", methods=["DELETE"])
# @token_required
def disable_user_account(current_user):
    try:
        User().disable_user_account(current_user["_id"])
        return jsonify({
            "message": "Successfully disabled account",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "Failed to disable account",
            "error": str(e),
            "data": None
        }), 400
