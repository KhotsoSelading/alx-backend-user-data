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
