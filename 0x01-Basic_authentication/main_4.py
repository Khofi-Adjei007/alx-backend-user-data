#!/usr/bin/env python3
""" 
Main script for BasicAuth class methods demonstration.
"""
from api.v1.auth.basic_auth import BasicAuth

# Initialize the BasicAuth instance
auth_instance = BasicAuth()

# Example usage of extract_user_credentials method with different inputs
print(auth_instance.extract_user_credentials(None))
print(auth_instance.extract_user_credentials(89))
print(auth_instance.extract_user_credentials("Holberton School"))  # Returns None (invalid format)
print(auth_instance.extract_user_credentials("Holberton:School"))  # Returns ('Holberton', 'School')
print(auth_instance.extract_user_credentials("bob@gmail.com:toto1234"))  # Returns ('bob@gmail.com', 'toto1234')
