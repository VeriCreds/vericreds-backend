import uuid
from typing import Optional
import bson, os
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel, Field
from dotenv import dotenv_values
from util.mongo import db

config = dotenv_values("../.env")


# class User(BaseModel):
#     id: str = Field(default_factory=uuid.uuid4, alias="_id")
#     metamask_address: str = Field(...)
#     first_name: str = Field(...)
#     last_name: str = Field(...)
#     email_address: str = Field(...)
#
#     class Config:
#         allow_population_by_field_name = True
#         schema_extra = {
#             "example": {
#                 "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "metamask_address": "0xccEbe5DEf67b45be78FdDCF0AF21A6C0130624dB",
#                 "first_name": "Kris",
#                 "last_name": "Stern",
#                 "email_address": "krisstern@outlook.com"
#             }
#         }


# class UserUpdate(BaseModel):
#     metamask_address: Optional[str]
#     first_name: Optional[str]
#     last_name: Optional[str]
#     email_address: Optional[str]
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "metamask_address": "0xccEbe5DEf67b45be78FdDCF0AF21A6C0130624dB",
#                 "first_name": "Kris",
#                 "last_name": "Stern",
#                 "email_address": "krisstern@outlook.com"
#             }
#         }


class User:
    """
    User Model
    """
    def __init__(self):
        return

    def register_user(self, first_name="", last_name="", email_address="", password=""):
        """
        Create a new user
        """
        user = self.get_by_email(email_address)
        if user:
            return
        new_user = db.users.insert_one(
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
        users = db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]


    def get_user_by_id(self, id):
        """Get a user by id"""
        user = db.users.find_one({"_id": bson.ObjectId(id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user


    def get_user_by_email(self, email_address):
        """Get a user by email"""
        user = db.users.find_one({"email": email_address, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user


    def update_user(self, user_id, name=""):
        """Update a user"""
        data = {}
        if name:
            data["name"] = name
        user = db.users.update_one(
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
        user = db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = self.get_user_by_id(user_id)
        return user


    def disable_user_account(self, user_id):
        """
        Disable a user account
        """
        user = db.users.update_one(
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
        user = self.get_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user
