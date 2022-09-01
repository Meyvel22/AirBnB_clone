#!/usr/bin/python3
""" Creates a unique FileStorage instance for your application """
from .engine.file_storage import FileStorage
from .base_model import BaseModel

storage = FileStorage()
storage.reload()
