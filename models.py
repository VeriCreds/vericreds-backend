import uuid
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import dotenv_values

config = dotenv_values("../.env")


class User(BaseModel):
    user_id: str = Field(default_factory=uuid.uuid4, alias="_user_id")
    meta_mask_address: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "meta_mask_address": "Don Quixote",
                "first_name": "Kris",
                "last_name": "Stern",
                "email": "krisstern@outlook.com"
            }
        }