#!/usr/bin/env python3

"""
Module for encrypting passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generates a salted, hashed password.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: The salted, hashed password.
    """
    encoded_password = password.encode()
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that a plaintext password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plaintext password to validate.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    encoded_password = password.encode()
    return bcrypt.checkpw(encoded_password, hashed_password)
