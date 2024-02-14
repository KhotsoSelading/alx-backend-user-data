#!/usr/bin/env python3
"""
Topic: Session Authentication
Author: Khotso Selading
Date: 14-02-2024
"""
from models.base import Base


class UserSession(Base):
    """User session class.

    This class represents a user session entity.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a User session instance.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
