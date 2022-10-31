# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for email sending."""
from flask import jsonify

from .helpers import send_confirm_email, send_password_reset_email
from ...author.model import Author
from .helpers import send_subscriber_emails


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
    
    
def send_subscribers_email(user_id: str):
    """Send your subscribers emails"""
    if not user_id:
        raise ValueError('The author follower id has to be provided')
    if not isinstance(user_id, str):
        raise TypeError('The author follow id has to be a string.')
    if not Author.user_with_id_exists(int(user_id)):
        raise ValueError(f'The author with id {user_id} does not exist')
    author = Author.get_user(int(user_id))
    subscriber_emails = [subscriber.email_address for subscriber in Author.get_subscriberss(int(user_id))]
    return send_subscriber_emails(author.email_address, subscriber_emails)
    

def handle_send_subscribers_email(id: str) -> dict:
    """Handle request to send subscribers email."""
    try:
        emails_sent = send_subscribers_email(id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)})
    else:
        return emails_sent