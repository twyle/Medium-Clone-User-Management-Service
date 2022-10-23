# -*- coding: utf-8 -*-
"""This package declares all the authorization functionality."""
from .auth import (
    handle_create_admin,
    handle_create_author,
    handle_create_moderator,
    handle_log_in_user
)


__all__ = [
    "handle_create_author",
    "handle_create_admin",
    "handle_create_moderator",
    "handle_log_in_user"
]
