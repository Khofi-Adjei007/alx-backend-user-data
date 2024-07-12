#!/usr/bin/env python3
""" User session module: Manages user sessions
"""
from models.base import Base

class UserSession(Base):
    """
    User Session Class for managing user session data.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a new UserSession instance.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
