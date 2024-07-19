#!/usr/bin/env python3
"""User module defining the User class and its attributes.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """Represents a user in the system.

    Attributes:
        __tablename__ (str): The name of the table
        storing user records.
        id (int): The unique identifier for the user.
        email (str): The user's email address.
        hashed_password (str): The user's hashed password.
        session_id (str, optional): The user's session ID
        for maintaining sessions.
        reset_token (str, optional): The user's reset token
        for password resets.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
