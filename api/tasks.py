# -*- coding: utf-8 -*-
"""Declare the celery tasks."""
from .extensions import celery
from .email import EmailMessage


@celery.task(name="send_email")
def celery_send_email(
    id: str, email_address: str, email_title: str, api_email_link: str
) -> dict:
    """Send the reset email."""
    email_message = EmailMessage(
        user_id=id,
        email_title=email_title,
        api_email_link=api_email_link,
        email_address=email_address,
    )

    return email_message.send_message()
