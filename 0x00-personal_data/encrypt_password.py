#!/usr/bin/env python3
"""
Topic: 0x00 - Personal Data
Author: Khotso Selading
Date: 07-02-2024
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check whether a password is valid
    Args:
        hashed_password (bytes): hashed password
        password (str): password in string
    Return:
        bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
