from flask import Blueprint, request, jsonify
from cerberus import Validator
from models import SmartContract

smart_contracts = Blueprint('smart_contracts', __name__, template_folder='routes')


@smart_contracts.route('/', methods=['POST'])
def add_smart_contract():
    try:
        contract = request.get_json()
        if not contract:
            return jsonify({
                "message": "Please provide contract details",
                "data": None,
                "error": "Bad request"
            }), 400

        # Assuming a Validator checks the schema of the contract
        try:
            # Placeholder: Adjust validation as per your schema
            is_validated = Validator(**contract)
        except Exception as validation_error:
            return jsonify(dict(message='Invalid data', data=None, error=str(validation_error))), 400

        contract_id = SmartContract.add_smart_contract(**contract)
        if not contract_id:
            return jsonify({
                "message": "Smart contract could not be added",
                "error": "Conflict",
                "data": None
            }), 409

        return jsonify({
            "message": "Successfully added new smart contract",
            "data": {"_id": contract_id}
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@smart_contracts.route('/', methods=['GET'])
def get_all_smart_contracts():
    try:
        all_contracts = SmartContract.get_all_contracts()
        return jsonify({
            "message": "Successfully retrieved all smart contracts",
            "data": all_contracts
        })

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@smart_contracts.route('/address/<contract_address>', methods=['GET'])
def get_smart_contract_by_address(contract_address):
    try:
        contract = SmartContract.get_contract_by_address(contract_address)
        if not contract:
            return jsonify({
                "message": "Smart contract with specified address not found",
                "data": None,
                "error": "Not Found"
            }), 404

        return jsonify({
            "message": "Successfully retrieved smart contract by address",
            "data": contract
        })

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@smart_contracts.route('/<contract_id>', methods=['GET'])
def get_smart_contract_by_id(contract_id):
    try:
        contract = SmartContract.get_contract_by_id(contract_id)
        if not contract:
            return jsonify({
                "message": "Contract not found",
                "data": None,
                "error": "Not Found"
            }), 404

        return jsonify({
            "message": "Successfully retrieved contract",
            "data": contract
        })

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@smart_contracts.route('/<contract_id>', methods=['PUT'])
def update_smart_contract(contract_id):
    try:
        data = request.json
        updated_contract = SmartContract.update_contract(contract_id, **data)
        if not updated_contract:
            return jsonify({
                "message": "Failed to update contract",
                "data": None,
                "error": "Not Modified"
            }), 304

        return jsonify({
            "message": "Successfully updated smart contract",
            "data": updated_contract
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to update contract",
            "error": str(e),
            "data": None
        }), 400


@smart_contracts.route('/<contract_id>', methods=['DELETE'])
def delete_smart_contract(contract_id):
    try:
        deleted = SmartContract.delete_contract(contract_id)
        if not deleted:
            return jsonify({
                "message": "Failed to delete contract or contract not found",
                "data": None,
                "error": "Not Found"
            }), 404

        return jsonify({
            "message": "Successfully deleted smart contract",
            "data": None
        }), 204

    except Exception as e:
        return jsonify({
            "message": "Failed to delete contract",
            "error": str(e),
            "data": None
        }), 400
