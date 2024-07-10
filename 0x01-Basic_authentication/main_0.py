#!/usr/bin/env python3
""" 
Main script for API authentication demonstration.
"""
from api.v1.auth.auth import Auth

# Initialize the Auth instance
auth_instance = Auth()

# Example usage of Auth methods
print(auth_instance.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(auth_instance.authorization_header())
print(auth_instance.current_user())
