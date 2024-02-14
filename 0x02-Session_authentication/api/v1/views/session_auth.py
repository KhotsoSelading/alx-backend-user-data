#!/usr/bin/env python3

"""
Topic: Session Authentication
Author: Khotso Selading
Date: 14-02-2024
"""
from api.v1.views import app_views
from os import getenv
from flask import jsonify, request, abort
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def handle_session_login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented with session ID set as a cookie
      - 400 if email or password is missing
      - 404 if no user found for the provided email
      - 401 if the password is wrong
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user = None
    email_missing = {"error": "email missing"}
    password_missing = {"error": "password missing"}
    user_not_found = {"error": "no user found for this email"}
    wrong_password = {"error": "wrong password"}

    if (email is None):
        return jsonify(email_missing), 400
    elif (password is None):
        return jsonify(password_missing), 400
    try:
        users = User.search({'email': email})
        if not users or users == []:
            return jsonify(user_not_found), 404
        for u in users:
            if u.is_valid_password(password):
                user = u
        if (user is None):
            return jsonify(wrong_password), 401
    except Exception:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie_response = getenv('SESSION_NAME')
    user_dict = jsonify(user.to_json())

    user_dict.set_cookie(cookie_response, session_id)
    return user_dict


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """Implements logout of session.

    This function destroys the session associated with the current request.

    Returns:
        str: An empty JSON response indicating successful logout.

    Raises:
        HTTPException: If session destruction fails, a 404 error is raised.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
