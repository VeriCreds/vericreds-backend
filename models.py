import bson
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from mongo import MongoConnection

load_dotenv()

mongo = MongoConnection.get_instance()


class User:
    """
    The User model
    """

    @staticmethod
    def register_user(first_name="", last_name="", email_address="", metamask_address="", password=""):
        """
        Create a new user
        """
        user = User.get_user_by_email(email_address)
        if user:
            return
        new_user = mongo.db.users.insert_one(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email_address": email_address,
                "metamask_address": metamask_address,
                "password": User.encrypt_password(password),
                "active": True
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
        user = mongo.db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    @staticmethod
    def get_user_by_email(email_address):
        """Get a user by email"""
        user = mongo.db.users.find_one({"email": email_address, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def update_user(user_id, first_name="", last_name="", email_address=""):
        """Update a user"""
        data = {}
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if email_address:
            data["email_address"] = email_address
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
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user
