# -*- coding: utf-8 -*-
"""This module contains all helper methos used by the email package."""
from flask import jsonify
from ...admin.model import Admin
from ...moderator.model import Moderator
from ...author.model import Author
from ...tasks import celery_send_email
from flask_mail import Message

from ...extensions import mail
    

def send_confirm_email(user_id: str, role: str, email_data: dict) -> dict:
    """Send account confirmation email."""
    cls = None
    if not role:
        raise ValueError(f"The user role must be provided!")
    if not isinstance(role, str):
        raise TypeError("The user role must be a string")
    if role == 'author':
        cls = Author
    elif role == 'admin':
        cls = Admin
    else:
        cls = Moderator
    if not user_id:
        raise ValueError(f"The {role} id must be provided")
    if not isinstance(user_id, str):
        raise TypeError(f"The {role} id must be a string")
    if not email_data:
        raise ValueError("The email data cannot be empty")
    if not isinstance(email_data, dict):
        raise TypeError("The email data should be a dict")
    if "email" not in email_data.keys():
        raise ValueError("The email key is missing in email data")
    if not email_data["email"]:
        raise ValueError("The email cannot be empty")
    if not cls.validate_email(email_data["email"]):
        raise ValueError("The email address format is invalid")
    if not cls.user_with_id_exists(int(user_id)):
        raise ValueError(f"The {role} with id {user_id} does not exist!")
    if not  cls.user_with_email_exists(email_data["email"]):
        raise ValueError(
            f'The {role} with email {email_data["email"]} does not exist!'
        )

    if not cls.validate_user(int(user_id), email_data["email"]):
        raise ValueError(
            f'There is no {role} with the id {user_id} and email {email_data["email"]}'
        )

    if cls.user_active(int(user_id)): 
        raise ValueError("This account has already been activated!")

    # task = celery_send_email.delay(
    #     user_id, email_data["email"], "Confirm Account", "auth.confirm_email"
    # )
    
    celery_send_email(
        user_id, email_data["email"], "Confirm Account", "auth.confirm_email", role
    )

    # return (
    #     jsonify(
    #         {"task_id": task.id, "Confirm Account email sent to": email_data["email"]}
    #     ),
    #     202,
    # )
    return jsonify({'success': f'Confirm Account email sent to {email_data["email"]}'})


def send_password_reset_email(id: str, role: str, email_data: dict) -> dict:
    """Send password reset email."""
    cls = None
    if not role:
        raise ValueError("The user role must be provided!")
    if not isinstance(role, str):
        raise TypeError("The user role must be a string")
    if role == 'author':
        cls = Author
    elif role == 'admin':
        cls = Admin
    else:
        cls = Moderator
    if not id:
        raise ValueError(f"The {role} id has to be provided!")

    if not isinstance(id, str):
        raise ValueError("The id has to be a string")

    if not email_data:
        raise ValueError("The email is missing!")

    if not isinstance(email_data, dict):
        raise ValueError("The email data must be a dict")

    if "email" not in email_data.keys():
        raise ValueError("The email has to be provided")

    if not email_data["email"]:
        raise ValueError("The email has to be provided!")

    if not cls.validate_email(email_data["email"]):
        raise ValueError("The email address format is invalid")
    if not cls.user_with_id_exists(int(id)):
        raise ValueError(f"The {role} with id {id} does not exist!")
    if not  cls.user_with_email_exists(email_data["email"]):
        raise ValueError(
            f'The {role} with email {email_data["email"]} does not exist!'
        )

    if not cls.validate_user(int(id), email_data["email"]):
        raise ValueError(
            f'There is no {role} with the id {id} and email {email_data["email"]}'
        )
    if not cls.user_active(int(id)):
        raise ValueError("You cannot change password for unactivated account!")

    # task = celery_send_email.delay(
    #     id, email_data["email"], "Password Reset", "auth.reset_password"
    # )
    
    celery_send_email(
        id, email_data["email"], "Password Reset", "auth.reset_password", role
    )

    # return (
    #     jsonify(
    #         {"task_id": task.id, "Password Reset Email sent to": email_data["email"]}
    #     ),
    #     202,
    # )
    return jsonify({'success': f'Password Reset Email sent to {email_data["email"]}'})


def send_email(sender, to):
    msg = Message('[Subscriber]',
    sender=sender, recipients=[to])
    msg.body = "Email body"
    mail.send(msg)


def send_subscriber_emails(sender, emails) -> dict:
    """Send password reset email."""
    for email in emails:
        send_email(sender, email)
    return jsonify({'success': f'{sender} emails sent.'})