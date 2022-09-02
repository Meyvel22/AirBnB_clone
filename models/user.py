#!/usr/bin/python3
""" User class definition that inherits from BaseModel """

from models.base_model import BaseModel


class User(BaseModel):
    """ A class User that inherits from BaseModel """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
