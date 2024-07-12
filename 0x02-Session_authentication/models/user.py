#!/usr/bin/env python3

""" User module: Handles User-related functionalities
"""
import hashlib
from models.base import Base

class User(Base):
    """
    User class for managing user-related data and functionalities.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a new User instance.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """
        Get the user's password.

        Returns:
            str: The hashed password.
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """
        Set a new password and hash it using SHA256.

        Args:
            pwd (str): The new password to set.
        """
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """
        Validate a given password against the stored hashed password.

        Args:
            pwd (str): The password to validate.

        Returns:
            bool: True if the password is valid, otherwise False.
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        return hashlib.sha256(pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """
        Generate a display name for the user based on available attributes.

        Returns:
            str: The display name.
        """
        if not self.email and not self.first_name and not self.last_name:
            return ""
        if not self.first_name and not self.last_name:
            return self.email
        if not self.last_name:
            return self.first_name
        if not self.first_name:
            return self.last_name
        return f"{self.first_name} {self.last_name}"
