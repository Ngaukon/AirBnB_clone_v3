#!/usr/bin/python3
"""
BaseModel Class of Models Module
"""

import os
import json
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

"""
Creates instance of Base if storage type is a database.
If not using database storage, uses class Base.
"""
if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
    Attributes and methods for BaseModel class
    """

    if storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new BaseModel object"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __is_serializable(self, obj_v):
        """
        Checks if an object is serializable
        :param obj_v: Object to be checked
        :return: True if serializable, False otherwise
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def bm_update(self, name, value):
        """
        Updates the BaseModel object and sets the correct attributes
        :param name: Attribute name to be updated
        :param value: Value to be set
        """
        setattr(self, name, value)
        if storage_type != 'db':
            self.save()

    def save(self):
        """
        Updates attribute `updated_at` to current time and saves the object
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_json(self):
        """
        Returns JSON representation of the BaseModel object
        :return: JSON dictionary of the object
        """
        bm_dict = {}
        for key, value in self.__dict__.items():
            if self.__is_serializable(value):
                bm_dict[key] = value
            else:
                bm_dict[key] = str(value)
        bm_dict['__class__'] = type(self).__name__
        bm_dict.pop('_sa_instance_state', None)
        if storage_type == "db" and 'password' in bm_dict:
            bm_dict.pop('password')
        return bm_dict

    def __str__(self):
        """
        Returns string representation of the object instance
        :return: String representation
        """
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
        Deletes current instance from storage
        """
        models.storage.delete(self)
