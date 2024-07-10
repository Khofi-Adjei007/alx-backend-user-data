#!/usr/bin/env python3

"""Authentication module."""
from typing import List, TypeVar
import fnmatch
from flask import request


class Auth:
    """Handles authentication tasks."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path: The path of the request.
            excluded_paths: List of paths that do
            not require authentication.

        Returns:
            bool: True if authentication is required,
            False otherwise.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            str: Value of the Authorization header if present, otherwise None.
        """
        if request is not None:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method to retrieve the current user from the request.

        Args:
            request: Flask request object.

        Returns:
            TypeVar('User'): Current user object.
        """
        return None
