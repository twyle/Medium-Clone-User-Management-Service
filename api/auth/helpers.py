# -*- coding: utf-8 -*-
"""This module contains all helper methods used by the auth package."""
from flask import current_app
import re


def is_user_password_valid(user_password: str):
    """Check if the user_password is valid."""
    if not user_password:
        raise ValueError("The user_password has to be provided.")

    if not isinstance(user_password, str):
        raise TypeError("The user_password has to be string")

    if len(user_password) >= current_app.config["PASSWORD_MAX_LENGTH"]:
        raise ValueError(
            f'The user_password has to be less than {current_app.config["PASSWORD_MAX_LENGTH"]}'
        )

    if len(user_password) <= current_app.config["PASSWORD_MIN_LENGTH"]:
        raise ValueError(
            f'The user_password has to be more than {current_app.config["PASSWORD_MIN_LENGTH"]}'
        )

    if not user_password.isalnum():
        raise ValueError("The user_password has to be alphanumeric.")

    return True


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        raise ValueError("The email_address cannot be an empty value")

    if not isinstance(email_address, str):
        raise ValueError("The email_address must be a string")

    #  Regular expression for validating an Email
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if re.fullmatch(regex, email_address):
        return True

    return False


def is_user_name_valid(user_name: str) -> bool:
    """Check if the user name is valid."""
    if not user_name:
        raise ValueError("The user_name has to be provided.")

    if not isinstance(user_name, str):
        raise ValueError("The user_name has to be string")

    if len(user_name) >= current_app.config["NAME_MAX_LENGTH"]:
        raise ValueError(
            f'The user_name has to be less than {current_app.config["NAME_MAX_LENGTH"]}'
        )

    if len(user_name) <= current_app.config["NAME_MIN_LENGTH"]:
        raise ValueError(
            f'The user_name has to be more than {current_app.config["NAME_MIN_LENGTH"]}'
        )

    return True


def check_if_email_id_match(cls, id: int, email: str) -> bool:
    """Check if user id and email belong to same user."""
    if not id:
        raise ValueError("The user id has to be provided!")

    if not isinstance(id, int):
        raise ValueError("The id has to be an int")

    if not email:
        raise ValueError("The email has to be provided.")

    if not isinstance(email, str):
        raise ValueError("The user_email has to be an string")

    user = cls.query.filter_by(id=id).first()

    if user.email == email:
        return True

    return False