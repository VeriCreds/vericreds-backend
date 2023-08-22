from flask import Blueprint, request, jsonify
from cerberus import Validator
from models import NFT

nfts = Blueprint('nfts', __name__, template_folder='routes')


@nfts.route('/', methods=['POST'])
def add_nft():
    try:
        nft_data = request.get_json()
        if not nft_data:
            return jsonify({
                "message": "Please provide NFT details",
                "data": None,
                "error": "Bad request"
            }), 400

        # Assuming a Validator checks the schema of the NFT
        try:
            # Placeholder: Adjust validation as per your schema
            is_validated = Validator(**nft_data)
        except Exception as validation_error:
            return jsonify(dict(message='Invalid data', data=None, error=str(validation_error))), 400

        nft_id = NFT.add_nft(**nft_data)
        if not nft_id:
            return jsonify({
                "message": "NFT could not be added",
                "error": "Conflict",
                "data": None
            }), 409

        return jsonify({
            "message": "Successfully added new NFT",
            "data": {"_id": nft_id}
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@nfts.route('/', methods=['GET'])
def get_all_nfts():
    try:
        all_nfts = NFT.get_all_nfts()
        return jsonify({
            "message": "Successfully retrieved all NFTs",
            "data": all_nfts
        })

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@nfts.route('/<nft_id>', methods=['GET'])
def get_nft_by_id(nft_id):
    try:
        nft = NFT.get_nft_by_id(nft_id)
        if not nft:
            return jsonify({
                "message": "NFT not found",
                "data": None,
                "error": "Not Found"
            }), 404

        return jsonify({
            "message": "Successfully retrieved NFT",
            "data": nft
        })

    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@nfts.route('/<nft_id>', methods=['PUT'])
def update_nft(nft_id):
    try:
        data = request.json
        updated_nft = NFT.update_nft(nft_id, **data)
        if not updated_nft:
            return jsonify({
                "message": "Failed to update NFT",
                "data": None,
                "error": "Not Modified"
            }), 304

        return jsonify({
            "message": "Successfully updated NFT",
            "data": updated_nft
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to update NFT",
            "error": str(e),
            "data": None
        }), 400


@nfts.route('/<nft_id>', methods=['DELETE'])
def delete_nft(nft_id):
    try:
        deleted = NFT.delete_nft(nft_id)
        if not deleted:
            return jsonify({
                "message": "Failed to delete NFT or NFT not found",
                "data": None,
                "error": "Not Found"
            }), 404

        return jsonify({
            "message": "Successfully deleted NFT",
            "data": None
        }), 204

    except Exception as e:
        return jsonify({
            "message": "Failed to delete NFT",
            "error": str(e),
            "data": None
        }), 400
