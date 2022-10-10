# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for email sending."""
from flask import jsonify
from .helpers import send_confirm_email

def handle_send_confirm_email(user_id: str, email_data: dict) -> dict:
    """Send the confirmation email."""
    try:
        confirm_email_data = send_confirm_email(user_id, email_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)})
    else:
        return confirm_email_data