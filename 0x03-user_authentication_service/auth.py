#!/usr/bin/env python3

"""Module providing authentication functionalities.
"""

import logging
from typing import Union
from uuid import uuid4

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User

# Disable logging of warnings
logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a new UUID.

    Returns:
        str: A string representation of the generated UUID.
    """
    return str(uuid4())


class Auth:
    """Class providing methods for user authentication and session management.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password.

        Args:
            email (str): The email address of the new user.
            password (str): The password for the new user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for the user.

        Args:
            email (str): The email address of the user.

        Returns:
            str: The session ID, or None if the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                return None
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on the session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Union[User, None]: The User object if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session for the specified user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for the user.

        Args:
            email (str): The user's email address.

        Raises:
            ValueError: If no user is found with the given email address.

        Returns:
            str: The generated reset token.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                raise ValueError()
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password using a reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is None:
                raise ValueError("Invalid reset token")
            new_hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=new_hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")
