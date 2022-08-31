#!/usr/bin/python3
"""
This module contains code about the BaseModel
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    Defines the BaseModel Class

    Arguments:
        id(str): a unique identifier for the BaseModel instance
        created_at(date): represents the time the object was created
        updated_at(date): represents the last time the object was updated
    """

    def __init__(self):
        """Contructor of the BaseModel class"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Returns the string representation of the class"""
        class_name = type(self).__name__
        created_at = self.created_at
        updated_at = self.updated_at
        return "[{}] ({}) {}" .format(class_name,  created_at, self.__dict__)

    def save(self):
        """
        Upates the BaseModel instance and sets the public
        instance updated_at to the current date
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys and their values
        """
        properties = set()
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                properties[key] = value.isoformat()
            else:
                properties[key] = value
