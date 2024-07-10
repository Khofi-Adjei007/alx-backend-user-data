#!/usr/bin/env python3
""" 
Main script for user creation and basic authentication demonstration.
"""
import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

# Create a user for testing
user_email = "bob100@hbtn.io"
user_clear_pwd = "H0lberton:School:98!"

user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user created with ID: {}".format(user.id))
user.save()

# Encode user credentials for Basic Auth
basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Auth Base64 encoded: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
