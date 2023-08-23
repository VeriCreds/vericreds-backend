import bson
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime

from mongo import MongoConnection

load_dotenv()

mongo = MongoConnection.get_instance()


class User:
    """
    The User model
    """

    @staticmethod
    def register_user(first_name="", last_name="", email_address="", metamask_address="", password="", created_at=None):
        """
        Create a new user
        """
        if not created_at:
            created_at = datetime.now()
        user = User.get_user_by_metamask_address(metamask_address)
        if user:
            return
        new_user = mongo.db.users.insert_one(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email_address": email_address,
                "metamask_address": metamask_address,
                "password": password,
                "created_at": created_at,
                "updated_at": created_at
            }
        )
        return User.get_user_by_id(new_user.inserted_id)

    @staticmethod
    def get_all_users():
        """
        Get all users
        """
        users = mongo.db.users.find()
        return [{**user, "_id": str(user["_id"])} for user in users]

    @staticmethod
    def get_user_by_id(user_id):
        """Get a user by id"""
        user = mongo.db.users.find_one({"_id": bson.ObjectId(user_id)})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    @staticmethod
    def get_user_by_email(email_address):
        """Get a user by email"""
        user = mongo.db.users.find_one({"email_address": email_address})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def get_user_by_metamask_address(metamask_address):
        """Get a user by email"""
        user = mongo.db.users.find_one({"email": metamask_address})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def update_user(user_id, first_name="", last_name="", email_address="", password="", updated_at=None):
        """Update a user"""
        if not updated_at:
            updated_at = datetime.now()
        data = {}
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if email_address:
            data["email_address"] = email_address
        if password:
            data["password"] = generate_password_hash(password)
        if updated_at:
            data["updated_at"] = updated_at
        mongo.db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = User.get_user_by_id(user_id)
        return user

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user
        """
        mongo.db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = User.get_user_by_id(user_id)
        return user

    @staticmethod
    def disable_user_account(user_id):
        """
        Disable a user account
        """
        mongo.db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = User.get_user_by_id(user_id)

        return user

    @staticmethod
    def encrypt_password(password):
        """
        Encrypt password
        """
        return generate_password_hash(password)

    @staticmethod
    def login(email_address, password):
        """
        Login a user"""
        user = User.get_user_by_email(email_address)
        if not user or not (user["password"] == password):
            return
        user.pop("password")
        return user


class Transaction:
    """
    The Transaction model
    """

    @staticmethod
    def log_transaction(transaction_id="", user_id="", amount=0.00, status="", nft_id="", created_at=None):
        """
        log a transaction
        """
        if not created_at:
            created_at = datetime.now()

        transaction = mongo.db.transactions.insert_one(
            {
                "transaction_id_pk": transaction_id,
                "user_id": user_id,
                "amount": amount,
                "status": status,
                "nft_id": nft_id,
                "created_at": created_at
            }
        )

        return transaction.inserted_id

    @staticmethod
    def get_all_transactions():
        """
        Get all transactions
        """
        transactions = mongo.db.transactions.find()
        return [{**transaction, "_id": str(transaction["_id"])} for transaction in transactions]

    @staticmethod
    def get_transaction_by_id(transaction_id):
        """Get a transaction by id"""
        transaction = mongo.db.transactions.find_one({"_id": bson.ObjectId(transaction_id)})
        if not transaction:
            return
        transaction["_id"] = str(transaction["_id"])
        return transaction

    @staticmethod
    def get_transaction_by_status(status):
        """Get transactions by status"""
        transactions = mongo.db.transactions.find({"status": status})
        return [{**transaction, "_id": str(transaction["_id"])} for transaction in transactions]

    @staticmethod
    def update_transaction(transaction_id, status="", amount=0.00, user_id="", nft_id="", updated_at=None):
        """Update a transaction"""
        if not updated_at:
            updated_at = datetime.now()
        data = {}
        if status:
            data["status"] = status
        if amount:
            data["amount"] = amount
        if user_id:
            data["user_id"] = user_id
        if nft_id:
            data["nft_id"] = nft_id
        if updated_at:
            data["updated_at"] = updated_at

        mongo.db.transactions.update_one(
            {"_id": bson.ObjectId(transaction_id)},
            {"$set": data}
        )

        return Transaction.get_transaction_by_id(transaction_id)

    @staticmethod
    def delete_transaction(transaction_id):
        """
        Delete a transaction
        """
        mongo.db.transactions.delete_one({"_id": bson.ObjectId(transaction_id)})
        return True


class SmartContract:

    @staticmethod
    def add_smart_contract(contract_id="", contract_address="", contract_abi="", created_at=None):
        """
        add a smart contract
        """
        if not created_at:
            created_at = datetime.now()

        contract = mongo.db.smart_contracts.insert_one(
            {
                "contract_id": contract_id,
                "contract_address": contract_address,
                "contract_abi": contract_abi,
                "created_at": created_at,
                "updated_at": created_at
            }
        )

        return contract.inserted_id

    @staticmethod
    def get_all_contracts():
        """
        Get all smart contracts
        """
        contracts = mongo.db.smart_contracts.find()
        return [{**contract, "_id": str(contract["_id"])} for contract in contracts]

    @staticmethod
    def get_contract_by_id(contract_id):
        """Get a smart contract by id"""
        contract = mongo.db.smart_contracts.find_one({"_id": bson.ObjectId(contract_id)})
        if not contract:
            return
        contract["_id"] = str(contract["_id"])
        return contract

    @staticmethod
    def get_contract_by_address(contract_address):
        """Get a smart contract by its address"""
        contract = mongo.db.smart_contracts.find_one({"contract_address": contract_address})
        if not contract:
            return
        contract["_id"] = str(contract["_id"])
        return contract


    @staticmethod
    def update_contract(contract_id, contract_address="", contract_abi="", updated_at=None):
        """Update a smart contract"""
        if not updated_at:
            updated_at = datetime.now()
        data = {}
        if contract_address:
            data["contract_address"] = contract_address
        if contract_abi:
            data["contract_abi"] = contract_abi
        if updated_at:
            data["updated_at"] = updated_at

        mongo.db.smart_contracts.update_one(
            {"_id": bson.ObjectId(contract_id)},
            {"$set": data}
        )

        return SmartContract.get_contract_by_id(contract_id)

    @staticmethod
    def delete_contract(contract_id):
        """
        Delete a smart contract
        """
        mongo.db.smart_contracts.delete_one({"_id": bson.ObjectId(contract_id)})
        return True


class NFT:

    @staticmethod
    def add_nft(nft_id="", user_id="", meta_data="", contract_id="", name="", format="", image="", status="",
                category="", created_at=None):
        """
        add a NFT
        """
        if not created_at:
            created_at = datetime.now()

        nft = mongo.db.nfts.insert_one(
            {
                "nft_id": nft_id,
                "user_id": user_id,
                "meta_data": meta_data,
                "contract_id": contract_id,
                "name": name,
                "format": format,
                "image": image,
                "status": status,
                "category": category,
                "created_at": created_at
            }
        )

        return nft.inserted_id

    @staticmethod
    def get_all_nfts():
        """
        Get all NFTs
        """
        nfts = mongo.db.nfts.find()
        return [{**nft, "_id": str(nft["_id"])} for nft in nfts]

    @staticmethod
    def get_nft_by_id(nft_id):
        """Get an NFT by id"""
        nft = mongo.db.nfts.find_one({"_id": bson.ObjectId(nft_id)})
        if not nft:
            return
        nft["_id"] = str(nft["_id"])
        return nft

    @staticmethod
    def get_nfts_by_user(user_id):
        """Get all NFTs for a specific user"""
        nfts = mongo.db.nfts.find({"user_id": user_id})
        return [{**nft, "_id": str(nft["_id"])} for nft in nfts]

    @staticmethod
    def update_nft(nft_id, user_id="", meta_data="", contract_id="", name="", format="", image="", status="",
                   category="", updated_at=None):
        """Update an NFT"""
        if not updated_at:
            updated_at = datetime.now()
        data = {}
        if user_id:
            data["user_id"] = user_id
        if meta_data:
            data["meta_data"] = meta_data
        if contract_id:
            data["contract_id"] = contract_id
        if name:
            data["name"] = name
        if format:
            data["format"] = format
        if image:
            data["image"] = image
        if status:
            data["status"] = status
        if category:
            data["category"] = category
        if updated_at:
            data["updated_at"] = updated_at

        mongo.db.nfts.update_one(
            {"_id": bson.ObjectId(nft_id)},
            {"$set": data}
        )

        return NFT.get_nft_by_id(nft_id)

    @staticmethod
    def delete_nft(nft_id):
        """
        Delete an NFT
        """
        mongo.db.nfts.delete_one({"_id": bson.ObjectId(nft_id)})
        return True

