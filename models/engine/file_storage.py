""" file_storage.py """

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """a class FileStorage that serializes instances to a JSON file and
       deserializes JSON file to instances:

       __file_path: string - path to the JSON file
       __objects:
           dictionary - empty but will store all objects by <class name>.id
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary """

        return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        clname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(clname, obj.id)] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """
            deserializes the JSON file to __objects (only if the JSON file
            (__file_path) exists ; otherwise, do nothing.
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def update(self, updated_object):
        """Sets __object to a new dictionary"""
        if not isinstance(updated_object, dict):
            return
            
        __object = updated_object
