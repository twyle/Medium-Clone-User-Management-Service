# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for email sending."""
from flask import jsonify
from .helpers import send_confirm_email, send_password_reset_email

def handle_send_confirm_email(user_id: str, role: str, email_data: dict) -> dict:
    """Send the confirmation email."""
    try:
        confirm_email_data = send_confirm_email(user_id, role, email_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)})
    else:
        return confirm_email_data


def handle_send_reset_password_email(id: str, role: str, email_data: dict) -> dict:
    """Handle request to send reset password email."""
    try:
        email_sent = send_password_reset_email(id, role, email_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)})
    else:
        return email_sent