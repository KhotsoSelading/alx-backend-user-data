#!/usr/bin/env python3
"""
Topic: Session Authentication
Author: Khotso Selading
Date: 14-02-2024
"""
from datetime import datetime, timedelta, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """
    def create_session(self, user_id=None):
        """Generates a session ID and creates a new user session.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID, or None if user_id is None.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user ID associated with a session ID if valid.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID, or None if invalid.
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        is_valid_user = UserSession.search({'session_id': session_id})
        if not is_valid_user:
            return None
        is_valid_user = is_valid_user[0]
        start_time = is_valid_user.created_at
        time_delta = timedelta(seconds=self.session_duration)
        if (start_time + time_delta) < datetime.now():
            return None
        return is_valid_user.user_id

    def destroy_session(self, request=None):
        """Destroys a user session based on the session ID from the request
        cookie.

        Args:
            request (Request, optional): The Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, False
            otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
