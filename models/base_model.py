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

    def __init__(self, **kwargs):
        """Contructor of the BaseModel class"""
        if kwargs:
            for key in kwargs.keys():
                if key != "__class__":
                    if key not in ["created_at", "updated_at"]:
                        self.__setattr__(key, kwargs[key])
                    else:
                        self.__setattr__(key, datetime.fromisoformat(kwargs[key]))
                        
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
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
