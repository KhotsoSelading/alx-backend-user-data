#!/usr/bin/env python3
"""
Topic: Session Authentication
Author: Khotso Selading
Date: 14-02-2024
"""
from os import getenv
from datetime import datetime, timedelta, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Expiration authentication """

    def __init__(self):
        """ Initializes class """
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Generates a session ID and creates a new session.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID, or None if user_id is None.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        SessionAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user ID associated with a session ID if valid.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID, or None if
            invalid.
        """
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id.keys():
            return None
        session_dictionary = SessionAuth.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary["user_id"]
        if "created_at" not in session_dictionary.keys():
            return None
        create_time = session_dictionary["created_at"]
        time_delta = timedelta(seconds=self.session_duration)
        if (create_time + time_delta) < datetime.now():
            return None
        return session_dictionary["user_id"]
