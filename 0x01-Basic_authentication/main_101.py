#!/usr/bin/env python3
""" 
Main script for API authentication scenarios.
"""
from api.v1.auth.auth import Auth

# Initialize the Auth instance
auth_instance = Auth()

# Example usage of require_auth method with different parameters
print(auth_instance.require_auth(None, None))
print(auth_instance.require_auth(None, []))
print(auth_instance.require_auth("/api/v1/users", ["/api/v1/stat*"]))
print(auth_instance.require_auth("/api/v1/status", ["/api/v1/stat*"]))
print(auth_instance.require_auth("/api/v1/stats", ["/api/v1/stat*"]))
