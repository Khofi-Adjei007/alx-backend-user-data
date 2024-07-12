#!/usr/bin/env python3

"""
Base module for handling core functionalities of model classes.
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}

class Base:
    """
    Base class for providing common functionalities to model classes.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a new instance of Base.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = datetime.strptime(kwargs.get('created_at'), TIMESTAMP_FORMAT) if kwargs.get('created_at') else datetime.utcnow()
        self.updated_at = datetime.strptime(kwargs.get('updated_at'), TIMESTAMP_FORMAT) if kwargs.get('updated_at') else datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """
        Check if two Base instances are equal based on their IDs.

        Args:
            other (Base): The other Base instance to compare against.

        Returns:
            bool: True if both instances have the same ID, otherwise False.
        """
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """
        Convert the instance to a JSON-serializable dictionary.

        Args:
            for_serialization (bool): Flag indicating if the conversion is for serialization.

        Returns:
            dict: JSON-serializable dictionary representation of the instance.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """
        Load all objects of the class from a JSON file.
        """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """
        Save all objects of the class to a JSON file.
        """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {obj_id: obj.to_json(True) for obj_id, obj in DATA[s_class].items()}

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """
        Save the current instance to the data store and file.
        """
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """
        Remove the current instance from the data store and file.
        """
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id):
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """
        Count the total number of objects of the class.

        Returns:
            int: The number of objects.
        """
        s_class = cls.__name__
        return len(DATA[s_class])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """
        Retrieve all objects of the class.

        Returns:
            Iterable[Base]: An iterable of all objects.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """
        Retrieve a single object by its ID.

        Args:
            id (str): The ID of the object to retrieve.

        Returns:
            Base: The object with the given ID, or None if not found.
        """
        s_class = cls.__name__
        return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """
        Search for objects matching specific attributes.

        Args:
            attributes (dict): Attributes to match against.

        Returns:
            List[Base]: A list of matching objects.
        """
        s_class = cls.__name__

        def _search(obj):
            if not attributes:
                return True
            for k, v in attributes.items():
                if getattr(obj, k) != v:
                    return False
            return True

        return list(filter(_search, DATA[s_class].values()))
