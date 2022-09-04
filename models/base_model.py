#!/usr/bin/python3
"""
This module contains code about the BaseModel
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Definition of the class BaseModel. Defines all common attributes and
       methods for other classes in the AirBnB project
    """

    def __init__(self, *args, **kwargs):
        """
            Initialize a new instance of the BaseModel class.
            Also recreate a class instance from a dictiornary.
            Attributes:
              id (str) - a unique identification number for each class instance
              created_at (datetime) - a datetime object indicating the date
                                    and time the instance was created
              updated_at (datetime) - a datetime object that is updated every
                                    time the instance object is modified
        """

        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key not in ['created_at', 'updated_at']:
                        self.__setattr__(key, value)
                    else:
                        self.__setattr__(key, datetime.fromisoformat(value))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)
            models.storage.save()

    def __str__(self):
        """Returns the string representation of the class"""

        return "[{}] ({}) {}". format(self.__class__.__name__, self.id,
                                      self.__dict__)

    def save(self):
        """
           Upates the BaseModel instance and sets the public
           instance updated_at to the current date
        """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys and their values
                - all key/value pairs from the __dict__ of the instance
                    - the created_at and updated_at attributes in string format
                      i.e (year-month-day T hour.minute.second.microsecond
                - a key __class__ whose value is the class of the instance
        """

        to_dict = {}
        for key, value in self.__dict__.items():
            to_dict[key] = value

        to_dict['__class__'] = self.__class__.__name__

        to_dict['created_at'] = self.created_at.isoformat()

        self.updated_at = datetime.now()
        to_dict['updated_at'] = self.updated_at.isoformat()

        return to_dict
