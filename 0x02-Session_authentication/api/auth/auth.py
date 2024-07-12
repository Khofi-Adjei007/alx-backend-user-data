#!/usr/bin/env python3
"""
Module for Authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv

class Auth:
    """ Class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Validate if an endpoint requires authentication.
        
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.
        
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        l_path = len(path)
        if l_path == 0:
            return True

        slash_path = True if path[l_path - 1] == '/' else False

        tmp_path = path
        if not slash_path:
            tmp_path += '/'

        for exc in excluded_paths:
            l_exc = len(exc)
            if l_exc == 0:
                continue

            if exc[l_exc - 1] != '*':
                if tmp_path == exc:
                    return False
            else:
                if exc[:-1] == path[:l_exc - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the request.
        
        Args:
            request (flask.Request, optional): The request object.
        
        Returns:
            str: The value of the Authorization header, or None if not present.
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Validate and return the current user.
        
        Args:
            request (flask.Request, optional): The request object.
        
        Returns:
            User: The current user, or None if not authenticated.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieve the session cookie value from the request.
        
        Args:
            request (flask.Request, optional): The request object.
        
        Returns:
            str: The session ID from the cookie, or None if not present.
        """
        if request is None:
            return None

        SESSION_NAME = getenv("SESSION_NAME")

        if SESSION_NAME is None:
            return None

        return request.cookies.get(SESSION_NAME)
