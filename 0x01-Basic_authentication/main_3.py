#!/usr/bin/env python3
""" 
Main script for BasicAuth class methods demonstration.
"""
from api.v1.auth.basic_auth import BasicAuth

# Initialize the BasicAuth instance
auth_instance = BasicAuth()

# Example usage of decode_base64_authorization_header method with different inputs
print(auth_instance.decode_base64_authorization_header(None))
print(auth_instance.decode_base64_authorization_header(89))
print(auth_instance.decode_base64_authorization_header("Holberton School"))
print(auth_instance.decode_base64_authorization_header("SG9sYmVydG9u"))  # Decodes to "Holberton"
print(auth_instance.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))  # Decodes to "Holberton School"
encoded_header = auth_instance.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")
print(auth_instance.decode_base64_authorization_header(encoded_header))
