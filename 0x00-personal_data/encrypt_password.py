#!/usr/bin/env python3
"""
Module for generating and validating salted, hashed passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generates a salted, hashed password from a plaintext password.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that a plaintext password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plaintext password to validate.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
