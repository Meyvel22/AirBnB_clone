#!/usr/bin/python3
"""
This module contains code about the BaseModel
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    Defines the BaseModel Class

    Arguments:
        id(str): a unique identifier for the BaseModel instance
        created_at(date): represents the time the object was created
        updated_at(date): represents the last time the object was updated
    """

    DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self, *args, **kwargs):
        """Contructor of the BaseModel class"""
        if not kwargs:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            for key, value in kwargs.items():
                print(kwargs)
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.strptime(
                        value, '%Y-%m-%dT%H:%M:%S.%f')
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value
        self.id = str(uuid.uuid4())
        models.storage.new(self)

    def __str__(self):
        """Returns the string representation of the class"""
        created_at = self.created_at
        updated_at = self.updated_at
        return "[{}] ({}) {}". format(type(self).__name__, self.id,
                                      self.__dict__)

    def save(self):
        """
           Upates the BaseModel instance and sets the public
           instance updated_at to the current date
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys and their values
        """
        to_dict = {}
        for key, value in self.__dict__.items():
            to_dict[key] = value

        to_dict['__class__'] = self.__class__.__name__

        to_dict['created_at'] = self.created_at.isoformat()

        self.updated_at = datetime.now()
        to_dict['updated_at'] = self.updated_at.isoformat()

        return to_dict
