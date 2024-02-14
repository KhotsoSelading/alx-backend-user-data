#!/usr/bin/env python3

"""
Topic: Session Authentication
Author: Khotso Selading
Date: 14-02-2024
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Handles session authorization and authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieves the user associated with the request.

        Args:
            request (Request, optional): The Flask request object.

        Returns:
            User: The user associated with the request.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(session_id)
        return User.get(user_id)
