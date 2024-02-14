#!/usr/bin/env python3

"""
Topic: Basic authentication
Author: Khotso Selading
Date: 12-02-2024
"""

import os
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Class to manage API authentication.

    Methods:
    - require_auth(self, path: str, excluded_paths: List[str]) -> bool:
    Returns False.
    - authorization_header(self, request=None) -> str: Returns None.
    - current_user(self, request=None) -> TypeVar('User'): Returns None.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): List of paths that are excluded from
            authentication checks.

        Returns:
            bool: False, indicating that authentication is not required.
        """
        if path is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                regex_pattern = re.escape(excluded_path[:-1]) + ".*"
                if re.match(regex_pattern, path):
                    return False
            elif path.startswith(excluded_path.rstrip('/')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header.

        Args:
            request: The Flask request object.

        Returns:
            str: None, indicating no authorization header is present.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        Get the current user.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): None, indicating no current user is authenticated.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Gets the value of the cookie named SESSION_NAME.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
