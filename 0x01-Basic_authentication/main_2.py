#!/usr/bin/env python3
""" 
Main script for BasicAuth class methods demonstration.
"""
from api.v1.auth.basic_auth import BasicAuth

# Initialize the BasicAuth instance
auth_instance = BasicAuth()

# Example usage of extract_base64_authorization_header method with different inputs
print(auth_instance.extract_base64_authorization_header(None))
print(auth_instance.extract_base64_authorization_header(89))
print(auth_instance.extract_base64_authorization_header("Holberton School"))
print(auth_instance.extract_base64_authorization_header("Basic Holberton"))
print(auth_instance.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
print(auth_instance.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
print(auth_instance.extract_base64_authorization_header("Basic1234"))
