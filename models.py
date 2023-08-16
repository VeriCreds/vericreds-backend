import uuid
from typing import Optional
import bson, os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import dotenv_values
from app import mongo

config = dotenv_values("../.env")


class User:
    """
    The User model
    """

    def __init__(self):
        return

    def register_user(self, first_name="", last_name="", email_address="", password=""):
        """
        Create a new user
        """
        user = self.get_user_by_email(email_address)
        if user:
            return
        new_user = mongo.db.users.insert_one(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email_address": email_address,
                "password": self.encrypt_password(password),
                "active": True
            }
        )
        return self.get_user_by_id(new_user.inserted_id)

    def get_all_users(self):
        """
        Get all users
        """
        users = mongo.db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]

    def get_user_by_id(self, user_id):
        """Get a user by id"""
        user = mongo.db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_user_by_email(self, email_address):
        """Get a user by email"""
        user = mongo.db.users.find_one({"email": email_address, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def update_user(self, user_id, first_name="", last_name="", email_address=""):
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
        user = self.get_user_by_id(user_id)
        return user

    def delete_user(self, user_id):
        """
        Delete a user
        """
        mongo.db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = self.get_user_by_id(user_id)
        return user

    def disable_user_account(self, user_id):
        """
        Disable a user account
        """
        mongo.db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_user_by_id(user_id)
        return user

    def encrypt_password(self, password):
        """
        Encrypt password
        """
        return generate_password_hash(password)

    def login(self, email, password):
        """
        Login a user"""
        user = self.get_user_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user
