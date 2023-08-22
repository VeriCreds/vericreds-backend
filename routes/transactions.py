from flask import Blueprint, request, jsonify
from cerberus import Validator
from models import Transaction  # Assuming you have a Transaction model like the User model

transactions = Blueprint('transactions', __name__, template_folder='routes')


@transactions.route('/', methods=['POST'])
def add_transaction():
    try:
        transaction = request.get_json()
        if not transaction:
            return jsonify({
                "message": "Please provide transaction details",
                "data": None,
                "error": "Bad request"
            }), 400

        # Assuming Validator is a class that raises an exception if validation fails
        try:
            is_validated = Validator(**transaction)
        except Exception as validation_error:
            return jsonify(dict(message='Invalid data', data=None, error=str(validation_error))), 400

        new_transaction = Transaction.log_transaction(**transaction)
        if not new_transaction:
            return jsonify({
                "message": "Transaction already exists",
                "error": "Conflict",
                "data": None
            }), 409

        return jsonify({
            "message": "Successfully created new transaction",
            "data": new_transaction
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@transactions.route("/", methods=["GET"])
def get_all_transactions():
    all_transactions = Transaction.get_all_transactions()
    return jsonify({
        "message": "Successfully retrieved all transactions data",
        "data": all_transactions
    })


@transactions.route("/<transaction_id>", methods=["GET"])
def get_single_transaction(transaction_id):
    transaction = Transaction.get_transaction_by_id(
        transaction_id)  # Assuming this function exists in your Transaction model.
    return jsonify({
        "message": "Successfully retrieved transaction details",
        "data": transaction
    })


@transactions.route("/status/<status>", methods=["GET"])
def get_transactions_by_status(status):
    try:
        transactions_by_status = Transaction.get_transaction_by_status(status)
        return jsonify({
            "message": f"Successfully retrieved transactions with status {status}",
            "data": transactions_by_status
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }), 500


@transactions.route("/<transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    try:
        data = request.json
        updated_transaction = Transaction.update_transaction(
            transaction_id,
            status=data.get("status"),
            amount=data.get("amount"),
            user_id=data.get("user_id"),
            nft_id=data.get("nft_id")
        )
        return jsonify({
            "message": "Successfully updated transaction data",
            "data": updated_transaction
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Failed to update transaction",
            "error": str(e),
            "data": None
        }), 400


@transactions.route("/<transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    try:
        Transaction.delete_transaction(transaction_id)
        return jsonify({
            "message": "Successfully deleted transaction",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "Failed to delete transaction",
            "error": str(e),
            "data": None
        }), 400
